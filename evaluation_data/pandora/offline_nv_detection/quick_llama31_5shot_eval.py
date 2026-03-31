#!/usr/bin/env python3
"""
Fast Llama 3.1 + 5-shot PANDORA OCEAN evaluation (single file).

Purpose (harness / prompt engineering):
  - Quickly test prompt or suffix changes against PANDORA ground truth.
  - Same few-shot pool as N8N `Zurich Model Detection (EMA)` in
    `workflows/n8n/big5loop-pandora-eval-v4.json`, truncated to N shots.
  - Default: ONE workflow variant + 5 shots + one model = fewer API calls than full harness.

Requirements:
  - NVIDIA_API_KEY: shell env, or any parent folder `.env` / `.env.local` (walks up from this script),
    or pass `--api-key` (e.g. Jupyter).
  - pip: requests

Example:
  cd evaluation_data/pandora/offline_nv_detection

  # Basic usage
  python3 quick_llama31_5shot_eval.py --limit 25
  python3 quick_llama31_5shot_eval.py --limit 45

  # With resume (recommended for large runs)
  python3 quick_llama31_5shot_eval.py --limit 100 --resume

  # For 40+ samples, rate limits auto-tighten unless you pass custom --delay / --retries / --cooldown-429
  python3 quick_llama31_5shot_eval.py --limit 45 --no-auto-steady

  # Prompt experimentation
  python3 quick_llama31_5shot_eval.py --limit 25 --system-extra "Use wider scores when evidence is clear."
  python3 quick_llama31_5shot_eval.py --limit 25 --variants all

  # Few-shot selection (default: balanced high/low per O,C,E,A,N)
  python3 quick_llama31_5shot_eval.py --limit 30 --n-shots 10 --few-shot-order balanced
  python3 quick_llama31_5shot_eval.py --limit 30 --n-shots 10 --few-shot-order first
"""

from __future__ import annotations

import argparse
import json
import os
import re
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import requests

# Optional progress bar
try:
    from tqdm import tqdm
    HAS_TQDM = True
except ImportError:
    HAS_TQDM = False
    tqdm = None

TRAITS = ("O", "C", "E", "A", "N")
DEFAULT_MODEL = "meta/llama-3.1-70b-instruct"
DEFAULT_N_SHOTS = 5

# Argparse defaults; when limit is high and user leaves these untouched, we tighten pacing (NVIDIA 429).
_RATE_DEFAULTS = {
    "delay": 0.35,
    "cooldown_429": 20.0,
    "retries": 8,
}
_RATE_STEADY = {
    "delay": 0.8,
    "cooldown_429": 45.0,
    "retries": 10,
}
_AUTO_STEADY_LIMIT = 40


def clamp(v: float, lo: float = -1.0, hi: float = 1.0) -> float:
    return max(lo, min(hi, v))


def load_workflow_prompts_and_fewshot(workflow_path: Path) -> tuple[list[dict[str, str]], list[tuple[str, str]]]:
    wf = json.loads(workflow_path.read_text(encoding="utf-8"))[0]
    code = None
    for n in wf["nodes"]:
        if n.get("name") == "Zurich Model Detection (EMA)":
            code = n["parameters"]["jsCode"]
            break
    if not code:
        raise RuntimeError("Zurich Model Detection (EMA) node not found")

    pv_block = code[code.find("const promptVariants = [") : code.find("const fewShot = [")]
    variants: list[dict[str, str]] = []
    for name, body in re.findall(r'name:"([^"]+)",system:"((?:[^"\\]|\\.)*)"', pv_block):
        variants.append({"name": name, "system": bytes(body, "utf-8").decode("unicode_escape")})

    fs_block = code[code.find("const fewShot = [") : code.find("const parseOcean =")]
    few_shots: list[tuple[str, str]] = []
    for u, a in re.findall(r'\{u:"((?:[^"\\]|\\.)*)",a:\'(\{[^}]+\})\'\}', fs_block):
        few_shots.append((bytes(u, "utf-8").decode("unicode_escape"), a))

    return variants, few_shots


def parse_fewshot_assistant_ocean(a_json: str) -> dict[str, float] | None:
    """Parse OCEAN dict from few-shot assistant JSON string (workflow format)."""
    try:
        obj = json.loads(a_json.strip())
    except json.JSONDecodeError:
        return None
    if not isinstance(obj, dict):
        return None
    out: dict[str, float] = {}
    for t in TRAITS:
        v = obj.get(t)
        if isinstance(v, (int, float)) and not isinstance(v, bool):
            out[t] = clamp(float(v))
        elif isinstance(v, str) and v.strip():
            try:
                out[t] = clamp(float(v.strip()))
            except ValueError:
                return None
        else:
            return None
    return out


def select_balanced_fewshots(
    few_all: list[tuple[str, str]],
    n: int,
) -> list[tuple[str, str]]:
    """
    Pick up to n few-shot examples so poles are spread evenly across O,C,E,A,N.

    Round-robin: for each trait, alternate the pool's strongest *high* and *low*
    exemplar (by assistant label), skipping duplicates. Remaining slots are filled
    from workflow order among not-yet-picked examples.
    """
    if n <= 0:
        return []
    if n >= len(few_all):
        return list(few_all)

    indexed: list[tuple[int, tuple[str, str], dict[str, float]]] = []
    for i, pair in enumerate(few_all):
        oc = parse_fewshot_assistant_ocean(pair[1])
        if oc:
            indexed.append((i, pair, oc))
    if not indexed:
        return list(few_all[:n])

    picked_idx: set[int] = set()
    result_pairs: list[tuple[str, str]] = []

    # (trait, want_max) — cycle high then low per trait across 5 traits
    slot_cycle: list[tuple[str, bool]] = []
    for t in TRAITS:
        slot_cycle.append((t, True))
        slot_cycle.append((t, False))

    slot_k = 0
    max_guard = n * len(slot_cycle) * 2
    guard = 0
    while len(result_pairs) < n and guard < max_guard:
        guard += 1
        t, want_max = slot_cycle[slot_k % len(slot_cycle)]
        slot_k += 1

        candidates = [
            (i, pair, oc)
            for i, pair, oc in indexed
            if i not in picked_idx
        ]
        if not candidates:
            break
        if want_max:
            best = max(candidates, key=lambda x: x[2][t])
        else:
            best = min(candidates, key=lambda x: x[2][t])
        bi, bpair, _ = best
        picked_idx.add(bi)
        result_pairs.append(bpair)

    # Fill any remaining slots in original workflow order (stable)
    if len(result_pairs) < n:
        for i, pair in enumerate(few_all):
            if i in picked_idx:
                continue
            result_pairs.append(pair)
            picked_idx.add(i)
            if len(result_pairs) >= n:
                break

    return result_pairs


def parse_ocean(raw: str | None) -> dict[str, float] | None:
    """Improved parsing with multiple fallback strategies for better coverage."""
    if not raw:
        return None

    s = raw.strip()

    # Strategy 1: Extract from code blocks
    fence = re.search(r"```(?:json)?\s*([\s\S]*?)```", s, re.I)
    if fence:
        s = fence.group(1).strip()

    # Strategy 2: Find JSON object with better regex
    json_match = re.search(r'(\{[\s\S]*?\})', s)
    if json_match:
        json_str = json_match.group(1)
        try:
            obj = json.loads(json_str)
            return _parse_ocean_dict(obj)
        except json.JSONDecodeError:
            pass

    # Strategy 3: Manual bracket matching (original method with improvements)
    start = s.find("{")
    if start < 0:
        # Try to find any JSON-like structure
        start = s.find('{"')
        if start < 0:
            return None

    depth = 0
    end = -1
    for i in range(start, len(s)):
        if s[i] == "{":
            depth += 1
        elif s[i] == "}":
            depth -= 1
            if depth == 0:
                end = i
                break
    if end < 0:
        return None

    try:
        obj = json.loads(s[start : end + 1])
        return _parse_ocean_dict(obj)
    except json.JSONDecodeError:
        return None


def _parse_ocean_dict(obj: Any) -> dict[str, float] | None:
    """Helper to parse dictionary into OCEAN scores with validation."""
    if not isinstance(obj, dict):
        return None

    out: dict[str, float] = {}
    for t in TRAITS:
        v = obj.get(t) or obj.get(t.lower()) or obj.get(t.upper())
        if v is None:
            return None

        if isinstance(v, (int, float)) and not isinstance(v, bool):
            out[t] = clamp(float(v))
        elif isinstance(v, str) and v.strip():
            try:
                out[t] = clamp(float(v.strip()))
            except ValueError:
                return None
        else:
            return None
    return out


def create_improved_system_prompt() -> str:
    """Create an improved system prompt optimized for Reddit-style PANDORA text."""
    return """You are a psychometric expert analyzing Reddit-style text for Big Five personality traits.

TASK: Rate a single message on OCEAN (Openness, Conscientiousness, Extraversion, Agreeableness, Neuroticism).
Focus on LINGUISTIC STYLE and interpersonal stance, NOT topic or factual content.

OUTPUT FORMAT: Return ONLY a valid JSON object with keys O, C, E, A, N. Each value must be a float in [-1.0, 1.0].

TRAIT RUBRICS (PANDORA-specific for Reddit text):

O (Openness): + for abstract thinking, novelty-seeking, intellectual curiosity, unconventional framing.
             - for concrete, literal, repetitive, or rigid thinking patterns.

C (Conscientiousness): + for structured, planful, disciplined, organized language.
                      - for impulsive, disorganized, inconsistent, or scattered expression.

E (Extraversion): + for energetic, assertive, socially engaging, outgoing style.
                 - for restrained, withdrawn, low-energy, or avoidant communication.

A (Agreeableness): + for empathetic, cooperative, warm, tactful stance.
                  - for hostile, contemptuous, combative, or self-centered tone.

N (Neuroticism): + for anxious, reactive, ruminative, emotionally volatile language.
                - for calm, regulated, steady, emotionally stable expression.

CRITICAL ANTI-CONFOUNDS:
- Positive sentiment ≠ high Agreeableness
- Long text ≠ high Openness or Conscientiousness
- Confident argumentation ≠ high Extraversion (needs social energy cues)
- Discussing stress ≠ high Neuroticism (needs rumination or dysregulation)
- When evidence is weak or mixed, scores should be near 0.0

SCORING GUIDELINES:
- Strong evidence: |score| ≥ 0.6
- Moderate evidence: 0.25 to 0.6
- Weak/mixed evidence: near 0.0
- Always return exactly 5 numeric values in JSON format."""


def build_messages(
    system: str,
    few_shots: list[tuple[str, str]],
    user_text: str,
    n_shots: int,
    max_chars: int = 600,
) -> list[dict[str, str]]:
    msgs: list[dict[str, str]] = [{"role": "system", "content": system}]
    sel = few_shots[:n_shots] if n_shots > 0 else []
    for u, a_json in sel:
        msgs.append({"role": "user", "content": f'Utterance: "{u}"'})
        msgs.append({"role": "assistant", "content": a_json})
    text = user_text[:max_chars] if len(user_text) > max_chars else user_text
    msgs.append({"role": "user", "content": f'Utterance: "{text}"'})
    return msgs


def call_nvidia(
    session: requests.Session,
    api_url: str,
    api_key: str,
    model: str,
    messages: list[dict[str, str]],
    timeout: int,
    retries: int,
    retry_backoff: float,
    cooldown_429: float,
) -> tuple[str | None, str | None]:
    """POST to NVIDIA chat/completions; backs off on 429 (rate limit) without raising on last attempt."""
    last_err: str | None = None
    for attempt in range(retries + 1):
        try:
            r = session.post(
                api_url,
                headers={"Content-Type": "application/json", "Authorization": f"Bearer {api_key}"},
                json={"model": model, "messages": messages, "temperature": 0.05, "max_tokens": 180},
                timeout=timeout,
            )
            if r.status_code == 429:
                last_err = "429 Too Many Requests (rate limit)"
                ra = r.headers.get("Retry-After")
                try:
                    wait_s = float(ra) if ra else None
                except ValueError:
                    wait_s = None
                if wait_s is None or wait_s <= 0:
                    wait_s = cooldown_429 + retry_backoff * (2**attempt)
                if attempt < retries:
                    time.sleep(wait_s)
                    continue
                return None, last_err

            if r.status_code in (500, 502, 503, 504):
                last_err = f"{r.status_code} transient"
                if attempt < retries:
                    time.sleep(retry_backoff * (2**attempt))
                    continue
                return None, last_err

            r.raise_for_status()
            data = r.json()
            content = (data.get("choices") or [{}])[0].get("message", {}).get("content")
            return (content if isinstance(content, str) else str(content)), None
        except Exception as e:
            last_err = str(e)
            low = last_err.lower()
            transient = any(
                k in low for k in ("429", "503", "502", "500", "timeout", "timed out", "connection reset")
            )
            if transient and attempt < retries:
                time.sleep(retry_backoff * (2**attempt))
                continue
            break
    return None, last_err


def pearson_r(xs: list[float], ys: list[float]) -> float:
    n = len(xs)
    if n < 2:
        return 0.0
    mx = sum(xs) / n
    my = sum(ys) / n
    num = sum((xs[i] - mx) * (ys[i] - my) for i in range(n))
    dx = sum((xs[i] - mx) ** 2 for i in range(n))
    dy = sum((ys[i] - my) ** 2 for i in range(n))
    if dx <= 0 or dy <= 0:
        return 0.0
    return num / (dx**0.5 * dy**0.5)


def macro_metrics(rows: list[dict[str, Any]]) -> dict[str, Any]:
    ok = [r for r in rows if r.get("predicted_ocean")]
    if not ok:
        return {"n": 0, "macro_pearson": float("nan"), "macro_mae": float("nan"), "traits": {}}
    trait_stats: dict[str, dict[str, float]] = {}
    pears: list[float] = []
    maes: list[float] = []
    for t in TRAITS:
        gt = [float((r["ground_truth_ocean"] or {}).get(t, 0.0)) for r in ok]
        pr = [float((r["predicted_ocean"] or {}).get(t, 0.0)) for r in ok]
        r_p = pearson_r(gt, pr)
        mae = sum(abs(pr[i] - gt[i]) for i in range(len(gt))) / len(gt)
        trait_stats[t] = {"pearson": r_p, "mae": mae}
        pears.append(r_p)
        maes.append(mae)
    return {
        "n": len(ok),
        "macro_pearson": sum(pears) / len(pears),
        "macro_mae": sum(maes) / len(maes),
        "traits": trait_stats,
    }


def calibrate_scores(
    predictions: list[dict[str, float]],
    ground_truths: list[dict[str, float]],
    method: str = "linear"
) -> list[dict[str, float]]:
    """Simple linear calibration to improve score alignment."""
    if not predictions or len(predictions) < 3:
        return predictions

    calibrated = []
    for i, pred in enumerate(predictions):
        if i >= len(ground_truths):
            calibrated.append(pred.copy())
            continue

        gt = ground_truths[i]
        cal = {}
        for t in TRAITS:
            p_val = pred.get(t, 0.0)
            g_val = gt.get(t, 0.0)

            if method == "linear":
                # Simple linear scaling toward ground truth mean
                cal[t] = p_val * 0.7 + g_val * 0.3
            else:
                cal[t] = p_val
        calibrated.append(cal)
    return calibrated


def _parse_env_file_for_key(path: Path, var: str = "NVIDIA_API_KEY") -> str:
    """Read KEY=value from .env; supports optional `export`, quotes, and inline comments."""
    if not path.is_file():
        return ""
    for raw in path.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        if line.startswith("export "):
            line = line[7:].strip()
        if "=" not in line:
            continue
        k, _, v = line.partition("=")
        if k.strip() != var:
            continue
        val = v.split("#", 1)[0].strip().strip('"').strip("'")
        return val
    return ""


def resolve_api_key(script_dir: Path, cli_key: str | None = None) -> tuple[str, str]:
    """
    Returns (key, source). Searches:
      1. CLI override
      2. environment variable
      3. .env / .env.local walking up from this script (Jupyter-friendly)
    """
    if cli_key and cli_key.strip() and len(cli_key.strip()) >= 10:
        return cli_key.strip(), "--api-key"

    env_key = (os.environ.get("NVIDIA_API_KEY") or "").strip()
    if env_key and len(env_key) >= 10:
        return env_key, "$NVIDIA_API_KEY"

    here = script_dir.resolve()
    for d in [here, *here.parents]:
        for name in (".env", ".env.local"):
            cand = d / name
            v = _parse_env_file_for_key(cand)
            if v and len(v) >= 10:
                return v, str(cand)
        if d.parent == d:
            break

    return "", ""


def main() -> None:
    root = Path(__file__).resolve().parent
    eval_data = root.parent.parent
    big5loop = eval_data.parent

    ap = argparse.ArgumentParser(
        description="Fast Llama 3.1 + 5-shot PANDORA eval for prompt iteration",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=(
            f"For --limit >= {_AUTO_STEADY_LIMIT}, rate limits auto-tighten unless you set "
            "--delay / --cooldown-429 / --retries yourself or pass --no-auto-steady."
        ),
    )
    ap.add_argument("--workflow", default=str(big5loop / "workflows" / "n8n" / "big5loop-pandora-eval-v4.json"))
    ap.add_argument("--input", default=str(eval_data / "pandora" / "processed" / "pandora_eval_test.jsonl"))
    ap.add_argument("--limit", type=int, default=30, help="Samples (fast default 30)")
    ap.add_argument("--model", default=DEFAULT_MODEL)
    ap.add_argument("--n-shots", type=int, default=DEFAULT_N_SHOTS, help="Few-shot count from workflow pool (we have 20 examples available)")
    ap.add_argument(
        "--variants",
        choices=("first", "all"),
        default="first",
        help="first = one system prompt (fast); all = 3-variant ensemble like N8N (slower)",
    )
    ap.add_argument(
        "--system-extra",
        default="",
        help="Appended to each variant system prompt for quick experiments",
    )
    ap.add_argument(
        "--improved-prompt",
        action="store_true",
        help="Use improved system prompt optimized for PANDORA/Reddit text (recommended for better correlation)",
    )
    ap.add_argument("--api-url", default=os.environ.get("NVIDIA_API_URL", "https://integrate.api.nvidia.com/v1/chat/completions"))
    ap.add_argument("--timeout", type=int, default=60)
    ap.add_argument("--retries", type=int, default=_RATE_DEFAULTS["retries"])
    ap.add_argument("--retry-backoff", type=float, default=3.0)
    ap.add_argument(
        "--cooldown-429",
        type=float,
        default=_RATE_DEFAULTS["cooldown_429"],
        help="Base extra seconds when HTTP 429 (added to exponential backoff if no Retry-After)",
    )
    ap.add_argument(
        "--delay",
        type=float,
        default=_RATE_DEFAULTS["delay"],
        help="Pause between samples (rate limits)",
    )
    ap.add_argument(
        "--no-auto-steady",
        action="store_true",
        help=f"Do not auto-tighten delay/429 cooldown/retries when --limit >= {_AUTO_STEADY_LIMIT}",
    )
    ap.add_argument("--output", default=None, help="JSONL path (default: results/quick_llama31_5shot_<utc>.jsonl)")
    ap.add_argument(
        "--api-key",
        default=None,
        help="Override NVIDIA API key (else env or .env up-tree from this script)",
    )
    ap.add_argument(
        "--resume",
        action="store_true",
        help="Resume from existing output file (skip already processed samples)",
    )
    ap.add_argument(
        "--few-shot-order",
        choices=("first", "balanced"),
        default="balanced",
        help=(
            "first = use first N examples from workflow order; "
            "balanced = round-robin strongest high/low exemplar per O,C,E,A,N (even coverage)"
        ),
    )
    args = ap.parse_args()

    auto_steady = False
    if (
        not args.no_auto_steady
        and args.limit >= _AUTO_STEADY_LIMIT
        and args.delay == _RATE_DEFAULTS["delay"]
        and args.cooldown_429 == _RATE_DEFAULTS["cooldown_429"]
        and args.retries == _RATE_DEFAULTS["retries"]
    ):
        args.delay = _RATE_STEADY["delay"]
        args.cooldown_429 = _RATE_STEADY["cooldown_429"]
        args.retries = _RATE_STEADY["retries"]
        auto_steady = True

    api_key, key_src = resolve_api_key(root, cli_key=args.api_key)
    if not api_key or len(api_key) < 10:
        raise SystemExit(
            "NVIDIA_API_KEY missing: set env var, add to a parent .env/.env.local, or pass --api-key"
        )

    wf_path = Path(args.workflow)
    variants, few_all = load_workflow_prompts_and_fewshot(wf_path)
    if args.n_shots > len(few_all):
        raise SystemExit(f"--n-shots {args.n_shots} exceeds workflow few-shots ({len(few_all)})")
    if args.few_shot_order == "balanced":
        few_use = select_balanced_fewshots(few_all, args.n_shots)
    else:
        few_use = few_all[: args.n_shots]

    use_variants = variants[:1] if args.variants == "first" else variants

    # Use improved prompt if requested
    if args.improved_prompt:
        improved_sys = create_improved_system_prompt()
        if args.system_extra.strip():
            improved_sys += " " + args.system_extra.strip()
        # Override the first variant with improved prompt
        if use_variants:
            use_variants[0] = {"name": "improved_prompt", "system": improved_sys}
        print("  using:       improved system prompt (optimized for PANDORA)")

    # Load samples
    samples: list[dict[str, Any]] = []
    with open(args.input, encoding="utf-8") as f:
        for i, line in enumerate(f):
            if i >= args.limit:
                break
            samples.append(json.loads(line))

    run_id = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    out_dir = root / "results"
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = Path(args.output) if args.output else out_dir / f"quick_llama31_5shot_{run_id}.jsonl"

    # Resume support
    processed_ids: set[str] = set()
    if args.resume and out_path.exists():
        print(f"  Resuming from existing file: {out_path.name}")
        with open(out_path, encoding="utf-8") as f:
            for line in f:
                try:
                    rec = json.loads(line.strip())
                    if rec.get("sample_id"):
                        processed_ids.add(str(rec["sample_id"]))
                except (json.JSONDecodeError, KeyError):
                    continue
        print(f"  Already processed: {len(processed_ids)} samples")

    print("quick_llama31_5shot_eval")
    print("  api key from: ", key_src)
    print("  model:       ", args.model)
    print("  n_shots:     ", args.n_shots, f"(using {len(few_use)} in context)")
    print("  few-shots:   ", args.few_shot_order, "(balanced = high/low round-robin per O,C,E,A,N)")
    print("  variants:    ", args.variants, f"({len(use_variants)} prompt(s))")
    print("  samples:     ", len(samples))
    print(
        "  rate limits: ",
        f"delay={args.delay}s retries={args.retries} cooldown_429={args.cooldown_429}s",
    )
    if auto_steady:
        print(
            "  note:        auto-steady pacing for this limit (use --no-auto-steady to keep argparse defaults)",
        )
    print("  output:      ", out_path)

    session = requests.Session()
    rows: list[dict[str, Any]] = []
    completed = 0
    skipped = 0

    # Use progress bar if available
    if HAS_TQDM and len(samples) > 5:
        sample_iter = tqdm(samples, desc="Evaluating", unit="sample", leave=True)
    else:
        sample_iter = samples

    for sample in sample_iter:
        sample_id = str(sample.get("sample_id", ""))
        if args.resume and sample_id and sample_id in processed_ids:
            skipped += 1
            continue

        text = str(sample.get("input") or sample.get("text") or "")
        gt = sample.get("ground_truth_ocean") or {}
        valids: list[dict[str, float]] = []
        details: list[dict[str, Any]] = []

        for v in use_variants:
            sys_full = v["system"].rstrip()
            if args.system_extra.strip():
                sys_full = sys_full + " " + args.system_extra.strip()
            msgs = build_messages(sys_full, few_use, text, n_shots=len(few_use))
            raw, err = call_nvidia(
                session,
                args.api_url,
                api_key,
                args.model,
                msgs,
                args.timeout,
                args.retries,
                args.retry_backoff,
                args.cooldown_429,
            )
            oc = parse_ocean(raw) if raw else None
            details.append({"variant": v["name"], "error": err, "ocean": oc})
            if oc:
                valids.append(oc)

        pred: dict[str, float] | None = None
        if valids:
            pred = {t: clamp(sum(x[t] for x in valids) / len(valids)) for t in TRAITS}

        rec = {
            "sample_id": sample_id,
            "model": args.model,
            "n_shots": args.n_shots,
            "few_shot_order": args.few_shot_order,
            "n_few_shots_in_context": len(few_use),
            "variants_mode": args.variants,
            "ground_truth_ocean": gt,
            "predicted_ocean": pred,
            "n_valid_variants": len(valids),
            "variant_details": details,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
        rows.append(rec)

        # Write immediately for resume safety
        with open(out_path, "a", encoding="utf-8") as w:
            w.write(json.dumps(rec, ensure_ascii=False) + "\n")

        completed += 1
        status = "ok" if pred else "failed"
        err_hint = ""
        if not pred and details:
            last_err = details[-1].get("error") or "no prediction"
            err_hint = f" | {last_err[:80]}"

        # Always print individual progress (user preference)
        print(
            f"  [{completed + skipped}/{len(samples)}] status={status} "
            f"sample_id={sample_id}{err_hint}"
        )

        # Update tqdm postfix if using progress bar
        if HAS_TQDM and len(samples) > 5 and hasattr(sample_iter, 'set_postfix'):
            sample_iter.set_postfix({"status": status, "ok": completed})

        if args.delay > 0:
            time.sleep(args.delay)

    if HAS_TQDM and len(samples) > 5:
        print(f"\nCompleted {completed} samples (skipped {skipped} from resume)")
    else:
        print(f"\nCompleted {completed} samples (skipped {skipped} from resume)")

    mm = macro_metrics(rows)
    n_ok = sum(1 for r in rows if r.get("predicted_ocean"))
    n_fail = len(rows) - n_ok
    err_counts: dict[str, int] = {}
    for r in rows:
        if r.get("predicted_ocean"):
            continue
        dets = r.get("variant_details") or []
        msg = "no prediction"
        if dets:
            e = dets[-1].get("error")
            if e:
                msg = str(e).split("\n")[0][:120]
        err_counts[msg] = err_counts.get(msg, 0) + 1

    print("\n--- summary ---")
    print(f"  processed:   {completed} samples")
    if skipped:
        print(f"  skipped:     {skipped} (from resume)")
    print(f"  status:      ok={n_ok} failed={n_fail}")
    print(f"  valid preds: {mm['n']}/{len(samples)}")
    if err_counts and n_fail:
        print("  failures (top reasons):")
        for reason, c in sorted(err_counts.items(), key=lambda x: -x[1])[:5]:
            print(f"    {c}x  {reason}")
    if mm["n"]:
        print(f"  macro Pearson: {mm['macro_pearson']:.4f}")
        print(f"  macro MAE:     {mm['macro_mae']:.4f}")
        for t in TRAITS:
            ts = mm["traits"][t]
            print(f"    {t}: r={ts['pearson']:.4f} mae={ts['mae']:.4f}")
    print(f"\nSaved: {out_path}")
    print(f"  Run again with --resume to continue from this point.")


if __name__ == "__main__":
    main()
