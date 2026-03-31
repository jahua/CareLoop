#!/usr/bin/env python3
"""
Offline PANDORA OCEAN detection via NVIDIA Chat Completions (`NVIDIA_API_URL`, `NVIDIA_API_KEY`).

**Detection modes** (`--detection-mode`):

- **five_trait_agents** (default): Same as `five_trait_detectors/llama31_five_trait_detect.py` — five specialized
  system prompts (O, C, E, A, N), one API call per trait, few-shot pairs from the workflow
  `fewShot` list, single-trait JSON parsing. Sequential calls with light pacing to reduce 429s.

- **zurich_variants**: Legacy — same 3 system variants + few-shots as
  `workflows/n8n/big5loop-pandora-eval-v4.json` (Zurich Model Detection); average valid full OCEAN JSON.

Outputs under ./results/: timestamped JSONL + ANALYSIS.md. For reporting across reruns, use
`OFFLINE-Detection-Analysis.ipynb` offline section with `MERGE_ALL_OFFLINE_RUNS = True` (default):
it loads every `offline_detection_*.jsonl` and deduplicates by `(sample_id, model)` keeping the newest `run_id`.

Usage (from this directory):
  export NVIDIA_API_KEY=...
  python run_offline_detection.py --limit 20

  # 500 samples, thesis-style model pool (4 models × 5 trait calls ≈ 10k API calls; use resume + pacing):
  python run_offline_detection.py --limit 500 --pool thesis_final --trait-delay 0.5 --delay 0.25

  # Continue the same JSONL after interruption (same run_id, skips existing sample_id+model rows):
  python run_offline_detection.py --limit 500 --pool thesis_final --trait-delay 0.5 \\
    --resume-from results/offline_detection_<RUN_ID>.jsonl

From evaluation_data:
  python pandora/offline_nv_detection/run_offline_detection.py --limit 20
"""

from __future__ import annotations

import argparse
from concurrent.futures import ThreadPoolExecutor, as_completed
import json
import os
import re
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import requests

TRAITS = ("O", "C", "E", "A", "N")
OCEAN_LABELS = {"O": "Openness", "C": "Conscientiousness", "E": "Extraversion", "A": "Agreeableness", "N": "Neuroticism"}

# Model pools (some entries may be unavailable for a given NVIDIA account/region and return 404).
# Keep broad coverage for comparative benchmarking.
MODEL_POOLS: dict[str, list[str]] = {
    # Harness winner (20260327T105404Z): best single config baseline.
    "best_config": [
        "meta/llama-3.1-70b-instruct",
    ],
    # Winner-centered shortlist for practical reruns.
    "winner_plus": [
        "meta/llama-3.1-70b-instruct",
        "meta/llama-3.3-70b-instruct",
        "google/gemma-3-27b-it",
        "moonshotai/kimi-k2-instruct",
    ],
    # Stronger psychometric candidates around the winner setup.
    "psychometric_v2": [
        "meta/llama-3.1-70b-instruct",
        "meta/llama-3.3-70b-instruct",
        "qwen/qwen2.5-72b-instruct",
        "google/gemma-3-27b-it",
        "moonshotai/kimi-k2-instruct",
    ],
    # Thesis-ready shortlist based on current availability + correlation.
    "thesis_final": [
        "meta/llama-3.3-70b-instruct",
        "meta/llama-3.1-70b-instruct",
        "moonshotai/kimi-k2-instruct",
        "google/gemma-3-12b-it",
    ],
    # Conservative pool with higher availability.
    "stable": [
        "meta/llama-3.1-8b-instruct",
        "meta/llama-3.1-70b-instruct",
        "meta/llama-3.3-70b-instruct",
        "google/gemma-3-27b-it",
    ],
    # Broader pool for model discovery / psychometric-style comparison.
    "broad": [
        "meta/llama-3.1-8b-instruct",
        "meta/llama-3.1-70b-instruct",
        "meta/llama-3.3-70b-instruct",
        "google/gemma-3-27b-it",
        "google/gemma-3-12b-it",
        "qwen/qwen2.5-72b-instruct",
        "qwen/qwen2.5-32b-instruct",
        "deepseek-ai/deepseek-r1",
        "deepseek-ai/deepseek-v3",
        "moonshotai/kimi-k2-instruct",
        "mistralai/mistral-nemo-12b-instruct-2407",
        "mistralai/mixtral-8x7b-instruct-v0.1",
    ],
    # Models likely to do better on nuanced style/stance judgements.
    "psychometric": [
        "meta/llama-3.3-70b-instruct",
        "meta/llama-3.1-70b-instruct",
        "google/gemma-3-27b-it",
        "qwen/qwen2.5-72b-instruct",
        "deepseek-ai/deepseek-r1",
        "moonshotai/kimi-k2-instruct",
    ],
}
DEFAULT_MODELS = MODEL_POOLS["winner_plus"]

# Keep in sync with `workflows/n8n/big5loop-pandora-eval-v4.json` (Zurich Model Detection).
PANDORA_V3_ANTI_INFLATION = (
    "Bias control (PANDORA v3): Do not raise Openness from positive tone, enthusiasm, or fandom alone. "
    "Do not raise Extraversion from debate confidence or assertiveness alone; require social-energetic or "
    "sociability cues. Do not raise Neuroticism from dramatic topics alone; require rumination, self-criticism, "
    "or clearly dysregulated style. Long text is not automatically high O or high C. When evidence is thin or mixed, "
    "shrink scores toward 0."
)


def clamp(v: float, lo: float = -1.0, hi: float = 1.0) -> float:
    return max(lo, min(hi, v))


def create_trait_specialized_prompts() -> dict[str, str]:
    """Same trait-only prompts as `five_trait_detectors/llama31_five_trait_detect.py` / n8n five-detector workflow."""
    return {
        "O": """You are an Openness detection specialist. Analyze the linguistic style of this Reddit-style message for Openness ONLY.

Focus on: abstract thinking, novelty-seeking, intellectual curiosity, unconventional framing, exploration of ideas vs concrete, literal, repetitive, or rigid thinking patterns.

You MUST use the FULL range [-1.0, 1.0]. Do not be conservative.
- +0.8 to +1.0 = highly abstract, philosophical, curious, novel thinking
- +0.3 to +0.7 = moderately open, some intellectual curiosity
- -0.3 to +0.2 = neutral or mixed evidence
- -0.8 to -1.0 = highly concrete, literal, repetitive, rigid thinking

Output ONLY a JSON with key "O" containing a float from -1.0 to 1.0.
Be decisive. Look for strong linguistic evidence of cognitive style.""",
        "C": """You are a Conscientiousness detection specialist. Analyze the linguistic style of this Reddit-style message for Conscientiousness ONLY.

Focus on: structured, planful, disciplined, organized language vs impulsive, disorganized, inconsistent, or scattered expression.

You MUST use the FULL range [-1.0, 1.0]. Do not be conservative.
- +0.8 to +1.0 = highly structured, planful, disciplined, organized communication
- +0.3 to +0.7 = moderately conscientious, some self-regulation
- -0.3 to +0.2 = neutral or mixed evidence
- -0.8 to -1.0 = highly impulsive, disorganized, inconsistent, scattered

Output ONLY a JSON with key "C" containing a float from -1.0 to 1.0.
Be decisive. Look for linguistic evidence of self-regulation and structure.""",
        "E": """You are an Extraversion detection specialist. Analyze the linguistic style of this Reddit-style message for Extraversion ONLY.

Focus on: energetic, assertive, socially engaging, outgoing style vs restrained, withdrawn, low-energy, or avoidant communication.

You MUST use the FULL range [-1.0, 1.0]. Do not be conservative.
- +0.8 to +1.0 = highly energetic, assertive, socially engaging, outgoing style
- +0.3 to +0.7 = moderately extraverted, some social energy
- -0.3 to +0.2 = neutral or mixed evidence
- -0.8 to -1.0 = restrained, withdrawn, low-energy, avoidant communication

Output ONLY a JSON with key "E" containing a float from -1.0 to 1.0.
Be decisive. Look for linguistic markers of social activation and energy.""",
        "A": """You are an Agreeableness detection specialist. Analyze the linguistic style of this Reddit-style message for Agreeableness ONLY.

Focus on: empathetic, cooperative, warm, tactful stance vs hostile, contemptuous, combative, or self-centered tone.

You MUST use the FULL range [-1.0, 1.0]. Do not be conservative.
- +0.8 to +1.0 = highly empathetic, cooperative, warm, tactful communication
- +0.3 to +0.7 = moderately agreeable, some warmth
- -0.3 to +0.2 = neutral or mixed evidence
- -0.8 to -1.0 = hostile, contemptuous, combative, self-centered tone

Output ONLY a JSON with key "A" containing a float from -1.0 to 1.0.
Be decisive. Focus on interpersonal stance and emotional tone.""",
        "N": """You are a Neuroticism detection specialist. Analyze the linguistic style of this Reddit-style message for Neuroticism ONLY.

Focus on: anxious, reactive, ruminative, emotionally volatile language vs calm, regulated, steady, emotionally stable expression.

You MUST use the FULL range [-1.0, 1.0]. Do not be conservative.
- +0.8 to +1.0 = high emotional volatility, rumination, anxiety markers
- +0.3 to +0.7 = moderately emotionally reactive
- -0.3 to +0.2 = neutral or mixed evidence
- -0.8 to -1.0 = calm, regulated, steady, emotionally stable communication

Output ONLY a JSON with key "N" containing a float from -1.0 to 1.0.
Be decisive. Look for linguistic markers of emotional regulation.""",
    }


def _extract_single_trait_score(raw: str, trait: str) -> float | None:
    """Parse one trait from model output (full OCEAN dict not required)."""
    if not raw:
        return None
    s = raw.strip()
    m = re.search(rf'"{trait}"\s*:\s*(-?[0-9]+\.?[0-9]*)', s)
    if m:
        return float(m.group(1))
    try:
        brace_start = s.find("{")
        brace_end = s.rfind("}")
        if brace_start >= 0 and brace_end > brace_start:
            obj = json.loads(s[brace_start : brace_end + 1])
            v = obj.get(trait) or obj.get(trait.lower())
            if isinstance(v, (int, float)) and not isinstance(v, bool):
                return float(v)
    except (json.JSONDecodeError, ValueError):
        pass
    return None


def build_five_agent_messages(
    trait: str,
    system_prompt: str,
    few_shots: list[tuple[str, str]],
    user_text: str,
    max_chars: int = 500,
) -> list[dict[str, str]]:
    msgs: list[dict[str, str]] = [{"role": "system", "content": system_prompt}]
    for u, a_json in few_shots:
        msgs.append({"role": "user", "content": f'Utterance: "{u}"'})
        msgs.append({"role": "assistant", "content": a_json})
    text = user_text[:max_chars] if len(user_text) > max_chars else user_text
    msgs.append({"role": "user", "content": f'Utterance: "{text}"'})
    return msgs


def call_five_agent_trait(
    session: requests.Session,
    api_url: str,
    api_key: str,
    model: str,
    trait: str,
    messages: list[dict[str, str]],
    timeout: int,
    temperature: float,
    max_tokens: int,
) -> dict[str, Any]:
    """One trait API call with 429 / transient retries (aligned with llama31_five_trait_detect)."""
    last_err: str | None = None
    for attempt in range(4):
        try:
            r = session.post(
                api_url,
                headers={"Content-Type": "application/json", "Authorization": f"Bearer {api_key}"},
                json={"model": model, "messages": messages, "temperature": temperature, "max_tokens": max_tokens},
                timeout=timeout,
            )
            if r.status_code == 429:
                wait = 2.0 * (2**attempt)
                last_err = f"429 rate limit (attempt {attempt + 1})"
                time.sleep(wait)
                continue
            if r.status_code in (500, 502, 503, 504):
                last_err = f"{r.status_code} transient"
                time.sleep(1.0 * (2**attempt))
                continue
            if r.status_code != 200:
                return {
                    "trait": trait,
                    "score": 0.0,
                    "raw": r.text[:200],
                    "error": f"HTTP {r.status_code}",
                    "success": False,
                }
            body = r.json()
            raw = (body.get("choices") or [{}])[0].get("message", {}).get("content", "")
            if not isinstance(raw, str):
                raw = str(raw)
            score = _extract_single_trait_score(raw, trait)
            if score is not None:
                return {"trait": trait, "score": clamp(score), "raw": raw[:200], "error": None, "success": True}
            return {"trait": trait, "score": 0.0, "raw": raw[:200], "error": "parse_failed", "success": False}
        except Exception as e:
            last_err = str(e)
            time.sleep(1.0 * (2**attempt))
    return {"trait": trait, "score": 0.0, "raw": None, "error": last_err or "max_retries", "success": False}


def five_trait_agent_detect(
    session: requests.Session,
    api_url: str,
    api_key: str,
    model: str,
    few_shots: list[tuple[str, str]],
    user_text: str,
    timeout: int,
    temperature: float,
    max_tokens: int,
    trait_delay_s: float,
) -> tuple[dict[str, float], dict[str, Any], bool]:
    """
    Run O→C→E→A→N sequentially (same order as n8n chain when not parallel).
    Returns (predicted_ocean, agent_details dict, all_traits_ok).
    """
    prompts = create_trait_specialized_prompts()
    predicted: dict[str, float] = {}
    agent_details: dict[str, Any] = {}
    all_ok = True
    for trait in TRAITS:
        msgs = build_five_agent_messages(trait, prompts[trait], few_shots, user_text)
        r = call_five_agent_trait(
            session, api_url, api_key, model, trait, msgs, timeout, temperature, max_tokens
        )
        predicted[trait] = float(r["score"])
        agent_details[trait] = {
            "score": r["score"],
            "raw": r.get("raw"),
            "error": r["error"],
            "success": r["success"],
        }
        if not r["success"]:
            all_ok = False
        if trait_delay_s > 0:
            time.sleep(trait_delay_s)
    return predicted, agent_details, all_ok


def _parse_zurich_js_code(code: str) -> tuple[list[dict[str, str]], list[tuple[str, str]]]:
    """Extract promptVariants + fewShot from legacy Zurich Model Detection (EMA) JavaScript."""
    if "const promptVariants = [" not in code or "const fewShot = [" not in code:
        return [], []
    pv_block = code[code.find("const promptVariants = [") : code.find("const fewShot = [")]
    variants = []
    for name, body in re.findall(r'name:"([^"]+)",system:"((?:[^"\\]|\\.)*)"', pv_block):
        system = bytes(body, "utf-8").decode("unicode_escape")
        variants.append({"name": name, "system": system})
    end_fs = code.find("const parseOcean =")
    if end_fs < 0:
        end_fs = code.find("];", code.find("const fewShot = ["))
    fs_block = code[code.find("const fewShot = [") : end_fs if end_fs > 0 else len(code)]
    few_shots: list[tuple[str, str]] = []
    # Assistant `a` may contain escaped JSON (not only [^}]+).
    fs_pat = re.compile(r'\{u:"((?:[^"\\]|\\.)*)",a:\'((?:[^\'\\]|\\.)*)\'\}')
    for m in fs_pat.finditer(fs_block):
        user = bytes(m.group(1), "utf-8").decode("unicode_escape")
        a_json = bytes(m.group(2), "utf-8").decode("unicode_escape")
        few_shots.append((user, a_json))
    return variants, few_shots


def load_workflow_detection_prompts(
    workflow_path: Path,
    *,
    bundle_path: Path | None = None,
) -> tuple[list[dict[str, str]], list[tuple[str, str]]]:
    """
    Load 3 Zurich system variants + few-shot pairs.

    `big5loop-pandora-eval-v4.json` may no longer embed `promptVariants` / `fewShot` (multi-agent
    detection replaced that code while keeping the node name). In that case we fall back to
    `pandora_zurich_detection_bundle.json` next to this script (snapshotted from git history).
    """
    bundle_path = bundle_path or (Path(__file__).resolve().parent / "pandora_zurich_detection_bundle.json")
    wf = json.loads(workflow_path.read_text(encoding="utf-8"))[0]
    code = None
    for n in wf["nodes"]:
        if n.get("name") == "Zurich Model Detection (EMA)":
            code = n["parameters"].get("jsCode")
            break
    variants: list[dict[str, str]] = []
    few_shots: list[tuple[str, str]] = []
    if code:
        variants, few_shots = _parse_zurich_js_code(code)

    if len(variants) != 3 or len(few_shots) < 1:
        if not bundle_path.is_file():
            raise RuntimeError(
                f"Could not parse Zurich prompts from {workflow_path} "
                f"({len(variants)} variants, {len(few_shots)} few-shots) and bundle missing: {bundle_path}"
            )
        data = json.loads(bundle_path.read_text(encoding="utf-8"))
        variants = data["variants"]
        few_shots = [(str(a[0]), str(a[1])) for a in data["few_shots"]]
        if len(variants) != 3 or len(few_shots) < 1:
            raise RuntimeError(
                f"Invalid bundle {bundle_path}: {len(variants)} variants, {len(few_shots)} few-shots"
            )
        print(
            f"Note: using bundled Zurich prompts+few-shots ({bundle_path.name}); "
            f"workflow node has no legacy promptVariants/fewShot block.",
            flush=True,
        )

    if len(few_shots) < 10:
        print(
            f"Note: only {len(few_shots)} few-shot example(s) loaded (older v4 snapshot had 3; "
            "extend bundle or use a workflow export that includes more).",
            flush=True,
        )

    return variants, few_shots


def parse_ocean(raw: str | None) -> dict[str, float] | None:
    if not raw:
        return None
    s = raw.strip()
    fence = re.search(r"```(?:json)?\s*([\s\S]*?)```", s, re.I)
    if fence:
        s = fence.group(1).strip()
    start = s.find("{")
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


def build_messages(
    variant_system: str,
    few_shots: list[tuple[str, str]],
    user_text: str,
    max_chars: int = 600,
    system_suffix: str = "",
) -> list[dict[str, str]]:
    sys_full = variant_system.rstrip() + (f" {system_suffix.strip()}" if system_suffix.strip() else "")
    msgs: list[dict[str, str]] = [{"role": "system", "content": sys_full}]
    for u, a_json in few_shots:
        msgs.append({"role": "user", "content": f'Utterance: "{u}"'})
        msgs.append({"role": "assistant", "content": a_json})
    text = user_text[:max_chars] if len(user_text) > max_chars else user_text
    msgs.append({"role": "user", "content": f'Utterance: "{text}"'})
    return msgs


def call_variant(
    session: requests.Session,
    api_url: str,
    api_key: str,
    model: str,
    messages: list[dict[str, str]],
    timeout: int,
    retries: int,
    retry_backoff: float,
) -> tuple[str | None, str | None]:
    last_err: str | None = None
    for attempt in range(retries + 1):
        try:
            r = session.post(
                api_url,
                headers={"Content-Type": "application/json", "Authorization": f"Bearer {api_key}"},
                json={"model": model, "messages": messages, "temperature": 0.1, "max_tokens": 140},
                timeout=timeout,
            )
            status = r.status_code
            if status in (429, 500, 502, 503, 504):
                last_err = f"{status} transient"
                if attempt < retries:
                    time.sleep(retry_backoff * (2**attempt))
                    continue
            r.raise_for_status()
            data = r.json()
            content = (data.get("choices") or [{}])[0].get("message", {}).get("content")
            return (content if isinstance(content, str) else str(content)), None
        except Exception as e:
            last_err = str(e)
            low = last_err.lower()
            transient = any(
                k in low
                for k in ("429", "503", "502", "500", "timeout", "timed out", "connection reset")
            )
            if transient and attempt < retries:
                time.sleep(retry_backoff * (2**attempt))
                continue
            break
    return None, last_err


def ensemble_ocean(
    session: requests.Session,
    api_url: str,
    api_key: str,
    model: str,
    variants: list[dict[str, str]],
    few_shots: list[tuple[str, str]],
    user_text: str,
    timeout: int,
    retries: int,
    retry_backoff: float,
    system_suffix: str,
) -> tuple[dict[str, float] | None, list[dict[str, Any]]]:
    per: list[dict[str, Any]] = []
    valid_vecs: list[dict[str, float]] = []
    for v in variants:
        msgs = build_messages(v["system"], few_shots, user_text, system_suffix=system_suffix)
        raw, err = call_variant(
            session, api_url, api_key, model, msgs, timeout, retries, retry_backoff
        )
        oc = parse_ocean(raw) if raw else None
        per.append({"variant": v["name"], "raw": raw, "error": err, "ocean": oc})
        if oc:
            valid_vecs.append(oc)
    if not valid_vecs:
        return None, per
    out = {t: 0.0 for t in TRAITS}
    for oc in valid_vecs:
        for t in TRAITS:
            out[t] += oc[t]
    n = len(valid_vecs)
    for t in TRAITS:
        out[t] = clamp(out[t] / n)
    return out, per


def spearman_corr(x: list[float], y: list[float]) -> float:
    import pandas as pd

    a = pd.Series(x)
    b = pd.Series(y)
    if a.std() == 0 or b.std() == 0:
        return 0.0
    return float(a.rank().corr(b.rank(), method="pearson"))


def main() -> None:
    root = Path(__file__).resolve().parent
    eval_data = root.parent.parent  # evaluation_data
    big5loop = eval_data.parent

    p = argparse.ArgumentParser()
    p.add_argument("--workflow", default=str(big5loop / "workflows" / "n8n" / "big5loop-pandora-eval-v4.json"))
    p.add_argument("--input", default=str(eval_data / "pandora" / "processed" / "pandora_eval_test.jsonl"))
    p.add_argument("--limit", type=int, default=20)
    p.add_argument(
        "--models",
        default=None,
        help="Comma-separated NVIDIA model names (overrides --pool when set)",
    )
    p.add_argument(
        "--pool",
        default="winner_plus",
        choices=sorted(MODEL_POOLS.keys()),
        help="Predefined model pool to benchmark",
    )
    p.add_argument(
        "--pools",
        default=None,
        help="Comma-separated pool names to run together (e.g. winner_plus,psychometric_v2)",
    )
    p.add_argument(
        "--n-shots",
        type=int,
        default=5,
        help="Number of few-shot examples to use from workflow fewShot list (best config uses 5)",
    )
    p.add_argument(
        "--parallel-models",
        action="store_true",
        help="Evaluate all models for a sample concurrently (higher 429 risk). Default: one model at a time.",
    )
    p.add_argument(
        "--max-workers",
        type=int,
        default=4,
        help="With --parallel-models: max concurrent model jobs per sample (ignored when sequential).",
    )
    p.add_argument("--delay", type=float, default=0.15)
    p.add_argument("--timeout", type=int, default=90)
    p.add_argument(
        "--prompt-suffix",
        choices=("none", "v3"),
        default="none",
        help=(
            "Append extra system text: 'none' uses workflow prompts as-is (v4 JSON already includes PANDORA v3 "
            "when re-exported). 'v3' adds the anti-inflation block again (for A/B vs older workflow files)."
        ),
    )
    p.add_argument(
        "--detection-mode",
        "--detection_mode",
        choices=("five_trait_agents", "zurich_variants"),
        default="five_trait_agents",
        help="five_trait_agents: 5 calls like llama31_five_trait_detect.py. zurich_variants: 3 workflow system prompts + full OCEAN JSON ensemble.",
    )
    p.add_argument(
        "--temperature",
        type=float,
        default=0.3,
        help="Sampling temperature for five_trait_agents (zurich path uses 0.1).",
    )
    p.add_argument("--max-tokens", type=int, default=120, help="Max tokens per trait call (five_trait_agents).")
    p.add_argument(
        "--trait-delay",
        type=float,
        default=0.3,
        help="Seconds to sleep between O/C/E/A/N calls to reduce NVIDIA 429 rate limits.",
    )
    p.add_argument(
        "--variants",
        default=None,
        help="Comma subset of variant names from workflow (zurich_variants only; default: all 3).",
    )
    p.add_argument("--retries", type=int, default=3)
    p.add_argument("--retry-backoff", type=float, default=1.5)
    p.add_argument("--api-url", default=os.environ.get("NVIDIA_API_URL", "https://integrate.api.nvidia.com/v1/chat/completions"))
    p.add_argument(
        "--resume-from",
        default=None,
        metavar="PATH",
        help=(
            "Append to this existing JSONL and skip API calls for (sample_id, model) pairs already "
            "present. PATH can be relative to offline_nv_detection (e.g. results/offline_detection_....jsonl)."
        ),
    )
    args = p.parse_args()

    # Local convenience: if key not exported in shell, try Big5Loop .env
    api_key = os.environ.get("NVIDIA_API_KEY", "")
    if not api_key:
        env_candidate = big5loop / ".env"
        if env_candidate.exists():
            for line in env_candidate.read_text(encoding="utf-8").splitlines():
                if line.startswith("NVIDIA_API_KEY="):
                    api_key = line.split("=", 1)[1].strip()
                    break
    if not api_key or len(api_key) < 10:
        raise SystemExit("Set NVIDIA_API_KEY in the environment.")

    variants, few_shots = load_workflow_detection_prompts(Path(args.workflow))
    all_variant_names = [v["name"] for v in variants]
    if args.detection_mode == "zurich_variants" and args.variants:
        want = {x.strip() for x in args.variants.split(",") if x.strip()}
        variants = [v for v in variants if v["name"] in want]
        if not variants:
            raise SystemExit(
                f"--variants matched nothing. Known names: {', '.join(all_variant_names)}"
            )
        missing = want - {v["name"] for v in variants}
        if missing:
            raise SystemExit(f"Unknown variant name(s): {', '.join(sorted(missing))}")
    system_suffix = PANDORA_V3_ANTI_INFLATION if args.prompt_suffix == "v3" else ""
    if args.n_shots < 0:
        raise SystemExit("--n-shots must be >= 0")
    if args.n_shots > 0:
        few_shots = few_shots[: args.n_shots]
    else:
        few_shots = []
    selected_pools: list[str] = []
    if args.models:
        models = [m.strip() for m in args.models.split(",") if m.strip()]
        selected_pools = ["custom_models"]
    elif args.pools:
        selected_pools = [x.strip() for x in args.pools.split(",") if x.strip()]
        bad = [x for x in selected_pools if x not in MODEL_POOLS]
        if bad:
            raise SystemExit(f"Unknown pool(s): {', '.join(bad)}. Valid pools: {', '.join(sorted(MODEL_POOLS))}")
        models = []
        for pn in selected_pools:
            models.extend(MODEL_POOLS[pn])
    else:
        selected_pools = [args.pool]
        models = list(MODEL_POOLS[args.pool])
    # De-duplicate while preserving order.
    models = list(dict.fromkeys(models))

    input_path = Path(args.input)
    if not input_path.is_absolute():
        if not input_path.is_file():
            under_script = (root / input_path).resolve()
            if under_script.is_file():
                input_path = under_script
    if not input_path.is_file():
        default_input = eval_data / "pandora" / "processed" / "pandora_eval_test.jsonl"
        raise SystemExit(
            f"Input JSONL not found: {args.input!r}\n"
            f"  Looked for: {Path(args.input).resolve()}\n"
            f"  Omit --input to use the default dataset, or pass a real path (e.g. ../processed/pandora_eval_test.jsonl).\n"
            f"  Default path: {default_input}"
        )

    rows: list[dict[str, Any]] = []
    with open(input_path, encoding="utf-8") as f:
        for i, line in enumerate(f):
            if i >= args.limit:
                break
            rows.append(json.loads(line))

    run_id = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    results_dir = root / "results"
    results_dir.mkdir(parents=True, exist_ok=True)

    completed_pairs: set[tuple[str, str]] = set()
    if args.resume_from:
        resume_path = Path(args.resume_from)
        if not resume_path.is_absolute():
            resume_path = (root / resume_path).resolve()
        if not resume_path.is_file():
            raise SystemExit(f"--resume-from: file not found: {resume_path}")
        resume_run_id: str | None = None
        with open(resume_path, encoding="utf-8") as rf:
            for line in rf:
                line = line.strip()
                if not line:
                    continue
                try:
                    prev = json.loads(line)
                except json.JSONDecodeError:
                    continue
                if resume_run_id is None and prev.get("run_id"):
                    resume_run_id = str(prev["run_id"])
                sid_p = prev.get("sample_id")
                mod_p = prev.get("model")
                if sid_p is not None and mod_p:
                    completed_pairs.add((str(sid_p), str(mod_p)))
        out_path = resume_path
        if resume_run_id:
            run_id = resume_run_id
        print(
            f"Resume: appending to {out_path.name}, {len(completed_pairs)} (sample_id, model) pairs already done.",
            flush=True,
        )
    else:
        out_path = results_dir / f"offline_detection_{run_id}.jsonl"

    def eval_one_model(
        model: str, sample_id: Any, text: str, ground_truth: dict[str, Any]
    ) -> dict[str, Any]:
        # Create one session per thread/model call to avoid cross-thread state.
        print(f"START sample={sample_id} model={model} mode={args.detection_mode}", flush=True)
        local_session = requests.Session()
        if args.detection_mode == "five_trait_agents":
            ocean, agent_details, all_ok = five_trait_agent_detect(
                local_session,
                args.api_url,
                api_key,
                model,
                few_shots,
                text,
                args.timeout,
                args.temperature,
                args.max_tokens,
                args.trait_delay,
            )
            rec = {
                "run_id": run_id,
                "sample_id": sample_id,
                "model": model,
                "detection_mode": "five_trait_agents",
                "ground_truth_ocean": ground_truth,
                "predicted_ocean": ocean,
                "agent_details": agent_details,
                "five_agent_all_traits_ok": all_ok,
                "n_shots": len(few_shots),
                "temperature": args.temperature,
                "input_excerpt": text[:500],
            }
            status = "ok" if all_ok else "partial_or_fail"
        else:
            ocean, detail = ensemble_ocean(
                local_session,
                args.api_url,
                api_key,
                model,
                variants,
                few_shots,
                text,
                args.timeout,
                args.retries,
                args.retry_backoff,
                system_suffix,
            )
            rec = {
                "run_id": run_id,
                "sample_id": sample_id,
                "model": model,
                "detection_mode": "zurich_variants",
                "ground_truth_ocean": ground_truth,
                "predicted_ocean": ocean,
                "variant_details": detail,
                "input_excerpt": text[:500],
            }
            status = "ok" if rec.get("predicted_ocean") else "FAIL"
        print(f"END   sample={sample_id} model={model} status={status}", flush=True)
        return rec

    def write_rec(rec: dict[str, Any]) -> None:
        with open(out_path, "a", encoding="utf-8") as outf:
            outf.write(json.dumps(rec, ensure_ascii=False) + "\n")
        ok_line = (
            rec.get("five_agent_all_traits_ok")
            if rec.get("detection_mode") == "five_trait_agents"
            else bool(rec.get("predicted_ocean"))
        )
        print(rec.get("sample_id"), rec["model"], "ok" if ok_line else "FAIL", rec.get("predicted_ocean"), flush=True)
        if args.delay > 0:
            time.sleep(args.delay)

    for row in rows:
        sid = row.get("sample_id")
        text = row.get("input") or row.get("text") or ""
        gt = row.get("ground_truth_ocean") or {}
        if args.parallel_models:
            with ThreadPoolExecutor(max_workers=max(1, min(args.max_workers, len(models)))) as ex:
                futs = []
                for model in models:
                    if (str(sid), str(model)) in completed_pairs:
                        print(f"SKIP sample={sid} model={model} (already in output)", flush=True)
                        continue
                    futs.append(ex.submit(eval_one_model, model, sid, str(text), gt))
                for fut in as_completed(futs):
                    rec = fut.result()
                    write_rec(rec)
                    completed_pairs.add((str(rec.get("sample_id")), str(rec.get("model"))))
        else:
            for model in models:
                if (str(sid), str(model)) in completed_pairs:
                    print(f"SKIP sample={sid} model={model} (already in output)", flush=True)
                    continue
                rec = eval_one_model(model, sid, str(text), gt)
                write_rec(rec)
                completed_pairs.add((str(rec.get("sample_id")), str(rec.get("model"))))

    # Analysis
    by_model: dict[str, list[dict[str, Any]]] = {m: [] for m in models}
    with open(out_path, encoding="utf-8") as f:
        for line in f:
            r = json.loads(line)
            by_model.setdefault(r["model"], []).append(r)

    lines_md = [
        f"# Offline NVIDIA detection — analysis",
        "",
        f"- Run ID: `{run_id}`",
        f"- Detection mode: `{args.detection_mode}`",
        f"- Samples: {args.limit}",
        f"- Pools: {', '.join(selected_pools)}",
        f"- Model schedule: {'parallel' if args.parallel_models else 'sequential (one model at a time)'}",
    ]
    if args.detection_mode == "five_trait_agents":
        lines_md.extend(
            [
                f"- Five agents: O/C/E/A/N sequential; temperature={args.temperature}, max_tokens={args.max_tokens}, trait_delay={args.trait_delay}s",
                f"- Few-shots: {len(few_shots)} (workflow `fewShot`; n_shots={args.n_shots})",
            ]
        )
    else:
        lines_md.extend(
            [
                f"- Variants: {', '.join(v['name'] for v in variants)}",
                f"- Prompt suffix: {args.prompt_suffix}",
                f"- API retries: {args.retries}, backoff {args.retry_backoff}s",
                f"- Few-shots: {len(few_shots)} (from workflow; requested n_shots={args.n_shots})",
            ]
        )
    lines_md.extend(
        [
            f"- Models requested: {', '.join(models)}",
            f"- Results: `{out_path.name}`",
            "",
            "## Per-model metrics (Pearson / Spearman / MAE on [-1,1])",
            "",
            "| Model | n (strict ok) | macro r | macro rho | macro MAE |",
            "|-------|---------------|---------|-----------|-----------|",
        ]
    )
    total_samples = len(rows)
    model_metrics: dict[str, dict[str, float]] = {}

    def strict_ok(x: dict[str, Any]) -> bool:
        if x.get("detection_mode") == "five_trait_agents":
            return bool(x.get("five_agent_all_traits_ok")) and isinstance(x.get("predicted_ocean"), dict)
        return x.get("predicted_ocean") is not None

    for model in models:
        rs = by_model.get(model, [])
        ok = [x for x in rs if strict_ok(x)]
        n = len(ok)
        if n == 0:
            lines_md.append(f"| `{model}` | 0 | — | — | — |")
            continue
        pears: list[float] = []
        spears: list[float] = []
        maes: list[float] = []
        for t in TRAITS:
            gt_v = [float((x["ground_truth_ocean"] or {}).get(t, 0.0)) for x in ok]
            pr_v = [float(x["predicted_ocean"][t]) for x in ok]
            import pandas as pd

            gts = pd.Series(gt_v)
            prs = pd.Series(pr_v)
            r_p = float(gts.corr(prs, method="pearson")) if gts.std() > 0 and prs.std() > 0 else 0.0
            r_s = spearman_corr(gt_v, pr_v)
            mae = float((prs - gts).abs().mean())
            pears.append(r_p)
            spears.append(r_s)
            maes.append(mae)
        lines_md.append(
            f"| `{model}` | {n} | {sum(pears)/5:.4f} | {sum(spears)/5:.4f} | {sum(maes)/5:.4f} |"
        )
        model_metrics[model] = {
            "n": float(n),
            "coverage": float(n / total_samples) if total_samples else 0.0,
            "macro_r": float(sum(pears) / 5),
            "macro_rho": float(sum(spears) / 5),
            "macro_mae": float(sum(maes) / 5),
        }

    lines_md.extend(["", "## Coverage-aware ranking", ""])
    lines_md.extend(["| Model | coverage | macro r | macro MAE | composite (0.7*r + 0.3*coverage) |", "|-------|----------|---------|-----------|-----------------------------------|"])
    ranked = []
    for model in models:
        m = model_metrics.get(model)
        if not m:
            continue
        composite = 0.7 * m["macro_r"] + 0.3 * m["coverage"]
        ranked.append((model, composite, m))
    ranked.sort(key=lambda x: x[1], reverse=True)
    for model, comp, m in ranked:
        lines_md.append(
            f"| `{model}` | {m['coverage']:.2%} | {m['macro_r']:.4f} | {m['macro_mae']:.4f} | {comp:.4f} |"
        )

    lines_md.extend(["", "## Per trait (best macro Pearson model)", ""])
    best_m = max(models, key=lambda m: _macro_pearson(by_model[m]) if by_model[m] else -999)
    lines_md.append(f"Best on macro Pearson: `{best_m}` (tie broken by first listed).")
    lines_md.append("")

    lines_md.extend(["## Failure diagnostics", ""])
    err_counts: dict[tuple[str, str], int] = {}
    for model in models:
        for r in by_model.get(model, []):
            if strict_ok(r):
                continue
            err = ""
            if r.get("detection_mode") == "five_trait_agents":
                ad = r.get("agent_details") or {}
                for t in TRAITS:
                    d = ad.get(t) or {}
                    if d.get("error"):
                        err = str(d["error"])
                        break
                if not err.strip():
                    err = "one_or_more_trait_failed"
            else:
                details = r.get("variant_details") or []
                for d in details:
                    if d.get("error"):
                        err = str(d["error"])
                        break
            low = err.lower()
            if "429" in low:
                cls = "429_rate_limit"
            elif "404" in low:
                cls = "404_model_not_found"
            elif "401" in low or "403" in low:
                cls = "auth_error"
            elif "timeout" in low:
                cls = "timeout"
            elif err.strip() == "":
                cls = "invalid_json_no_error"
            else:
                cls = "other_error"
            key = (model, cls)
            err_counts[key] = err_counts.get(key, 0) + 1
    if err_counts:
        lines_md.extend(["| Model | error class | count |", "|-------|-------------|-------|"])
        for (model, cls), cnt in sorted(err_counts.items(), key=lambda x: (-x[1], x[0][0])):
            lines_md.append(f"| `{model}` | `{cls}` | {cnt} |")
    else:
        lines_md.append("No model-level failures were detected.")

    lines_md.extend(["", "## Interpretation", ""])
    if ranked:
        top_model, _, topm = ranked[0]
        if topm["coverage"] < 0.7:
            rel_note = "Top model has low coverage, so ranking may be unstable."
        elif topm["coverage"] < 0.95:
            rel_note = "Top model has moderate coverage; rerun with lower concurrency to reduce 429 errors."
        else:
            rel_note = "Top model has high coverage; ranking is relatively stable."
        if topm["macro_r"] >= 0.2:
            q_note = "Correlation is promising."
        elif topm["macro_r"] >= 0.05:
            q_note = "Correlation is weak-to-moderate."
        else:
            q_note = "Correlation is weak; prompt/model alignment needs further improvement."
        lines_md.append(f"- Recommended current model: `{top_model}`")
        lines_md.append(f"- Coverage: {topm['coverage']:.2%}; macro Pearson: {topm['macro_r']:.4f}; macro MAE: {topm['macro_mae']:.4f}")
        lines_md.append(f"- Reliability: {rel_note}")
        lines_md.append(f"- Quality: {q_note}")
        lines_md.append("- Next: rerun with `--max-workers 1-2` and larger sample size (>=100) for more stable ranking.")
    analysis_path = results_dir / f"ANALYSIS_{run_id}.md"
    analysis_path.write_text("\n".join(lines_md) + "\n", encoding="utf-8")
    latest = results_dir / "ANALYSIS_LATEST.md"
    latest.write_text(analysis_path.read_text(encoding="utf-8"), encoding="utf-8")

    print("\nWrote:", out_path)
    print("Wrote:", analysis_path)
    print("Wrote:", latest)


def _macro_pearson(rs: list[dict[str, Any]]) -> float:
    def _ok(x: dict[str, Any]) -> bool:
        if x.get("detection_mode") == "five_trait_agents":
            return bool(x.get("five_agent_all_traits_ok")) and isinstance(x.get("predicted_ocean"), dict)
        return x.get("predicted_ocean") is not None

    ok = [x for x in rs if _ok(x)]
    if not ok:
        return -999.0
    import pandas as pd

    pears = []
    for t in TRAITS:
        gt_v = [float((x["ground_truth_ocean"] or {}).get(t, 0.0)) for x in ok]
        pr_v = [float(x["predicted_ocean"][t]) for x in ok]
        gts = pd.Series(gt_v)
        prs = pd.Series(pr_v)
        pears.append(float(gts.corr(prs, method="pearson")) if gts.std() > 0 and prs.std() > 0 else 0.0)
    return sum(pears) / 5


if __name__ == "__main__":
    main()
