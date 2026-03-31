#!/usr/bin/env python3
"""
All-at-once OCEAN Detector — strict_style prompt, 1 call per sample

Strategy: single API call returns all 5 traits. Post-hoc linear calibration.
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

import sys
import requests

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from quick_llama31_5shot_eval import clamp, TRAITS, resolve_api_key

DEFAULT_MODEL = "meta/llama-3.3-70b-instruct"

SYSTEM_PROMPT = (
    "You are a psychometric rater. Infer Big Five O,C,E,A,N from writing style only. "
    "Ignore topic popularity, morality, and factual correctness. "
    "Return only JSON with O,C,E,A,N in [-1,1]."
)

PANDORA_FEW_SHOTS = [
    ("nope, you can transfer herpes 1 (cold sores) to genitals.",
     '{"O": 0.54, "C": 0.70, "E": -0.38, "A": -0.08, "N": 0.88}'),
    ("Use keys around your movement keys, and modifiers. For example, if your movement keys are WASD, then use numbers 1-4/5.",
     '{"O": 0.30, "C": 0.00, "E": -0.30, "A": -0.96, "N": 0.64}'),
    ("On Kilimanjaro Safari, the drivers do have predetermined animal facts that can be shared with the guests.",
     '{"O": 0.62, "C": 0.22, "E": 0.20, "A": -0.40, "N": -0.50}'),
    ("nothing to do with the story but one complaint i kinda have with oregairu is the studio change between seasons.",
     '{"O": -0.70, "C": -0.70, "E": -0.70, "A": -0.70, "N": 0.70}'),
    ("Fully agree, it's an incredible movie which absolutely deserved to win Best Picture.",
     '{"O": 0.74, "C": -0.86, "E": 0.58, "A": -0.98, "N": -0.02}'),
    ("Thought it was a cool show. Didn't care for the electronics and voice amp though.",
     '{"O": -0.80, "C": 0.60, "E": 0.48, "A": -0.46, "N": -0.64}'),
    ("Lol people REALLY don't pay attention to the stuff Todd says he likes.",
     '{"O": 0.82, "C": 0.80, "E": -0.60, "A": -0.14, "N": 0.46}'),
    ("I've been thinking about dropping Carlos. With the drafting of 2 wr's and rumors of poor OTA's I'm feeling pretty down on him.",
     '{"O": 0.10, "C": 0.68, "E": -0.14, "A": -1.00, "N": 0.16}'),
    ("Mentioning you have an ideology that we can then use to predict your actions on the economy is indeed much better.",
     '{"O": 0.98, "C": 0.80, "E": -0.12, "A": -0.72, "N": 0.94}'),
    ("I'm trans and I fly occasionally within the US and I have never seen the gender buttons you describe.",
     '{"O": 0.34, "C": 0.78, "E": -0.24, "A": -1.00, "N": 0.66}'),
    ("Nice if well-kept. I admire long luxurious beards in a non-sexual way.",
     '{"O": 0.08, "C": 0.26, "E": -0.24, "A": -0.88, "N": 0.70}'),
    ("Im sorry, but if your therapist knows your mother has NPD he should NOT be encouraging YOU try and change the relationship.",
     '{"O": -0.82, "C": -0.30, "E": 0.96, "A": 0.24, "N": -0.62}'),
    ("It's a really good song, but that one line is very questionable.",
     '{"O": -0.42, "C": 0.08, "E": -0.40, "A": -0.56, "N": 0.80}'),
    ("Dom getting hyped lmao wow first time I've heard him legitimately excited.",
     '{"O": -0.70, "C": -0.70, "E": 0.70, "A": 0.70, "N": 0.00}'),
    ("What is made 99.99% of air? Neither steel tubes nor this new alloy are.",
     '{"O": -0.96, "C": 0.70, "E": -0.96, "A": 0.72, "N": -0.40}'),
    ("serious question: if this take were made about blacks, would this post be ban worthy?",
     '{"O": -0.32, "C": 0.48, "E": 0.72, "A": -0.64, "N": 0.80}'),
    ("Last time I was on exercise, I woke up freezing. I had to get up to turn down my air conditioning.",
     '{"O": -0.54, "C": -0.32, "E": -0.88, "A": 0.00, "N": -0.38}'),
    ("Point of Order Mr Speaker! This motion no longer reflects the title of the motion.",
     '{"O": 0.12, "C": -0.08, "E": 0.08, "A": -0.16, "N": 0.90}'),
    ("Off for the night, sorry about the short window, I'll be back around 3pm cst.",
     '{"O": 0.80, "C": -0.74, "E": -0.60, "A": -0.96, "N": 0.98}'),
    ("Backup, ideally using the 3-2-1 backup strategy. AND test your backups regularly.",
     '{"O": 0.98, "C": -0.34, "E": -0.94, "A": -0.92, "N": 0.92}'),
]


# ── Parsing ───────────────────────────────────────────────────────────────────

def parse_ocean(raw: str | None) -> dict[str, float] | None:
    if not raw:
        return None
    s = raw.strip()
    fence = re.search(r"```(?:json)?\s*([\s\S]*?)```", s, re.I)
    if fence:
        s = fence.group(1).strip()
    braces = [(m.start(), m.end()) for m in re.finditer(r'\{[^{}]+\}', s)]
    for start, end in reversed(braces):
        try:
            obj = json.loads(s[start:end])
            out = {}
            for t in TRAITS:
                v = obj.get(t, obj.get(t.lower()))
                if isinstance(v, (int, float)) and not isinstance(v, bool):
                    out[t] = clamp(float(v))
            if len(out) == 5:
                return out
        except (json.JSONDecodeError, ValueError):
            continue
    return None


# ── API call ──────────────────────────────────────────────────────────────────

def _api_call(
    api_url: str, api_key: str, model: str,
    messages: list[dict], temperature: float,
    max_tokens: int, timeout: int,
) -> tuple[str | None, str | None]:
    for attempt in range(4):
        try:
            r = requests.post(
                api_url,
                headers={"Content-Type": "application/json",
                         "Authorization": f"Bearer {api_key}"},
                json={"model": model, "messages": messages,
                      "temperature": temperature, "max_tokens": max_tokens},
                timeout=timeout,
            )
            if r.status_code == 429:
                time.sleep(2.0 * (2 ** attempt))
                continue
            if r.status_code in (500, 502, 503, 504):
                time.sleep(1.0 * (2 ** attempt))
                continue
            if r.status_code != 200:
                return None, f"HTTP {r.status_code}: {r.text[:100]}"
            body = r.json()
            raw = body.get("choices", [{}])[0].get("message", {}).get("content", "")
            return raw, None
        except Exception as e:
            time.sleep(1.0 * (2 ** attempt))
            if attempt == 3:
                return None, str(e)
    return None, "max_retries"


# ── Detector ──────────────────────────────────────────────────────────────────

class OceanDetector:
    def __init__(self, model: str = DEFAULT_MODEL, api_url: str = None,
                 calibration: dict | None = None):
        self.model = model
        self.api_url = api_url or os.environ.get(
            "JULING_API_URL",
            os.environ.get("NVIDIA_API_URL",
                           "https://open.177911.com/v1/chat/completions")
        )
        self.calibration = calibration

    def _calibrate(self, scores: dict[str, float]) -> dict[str, float]:
        if not self.calibration:
            return scores
        out = {}
        for t in TRAITS:
            cfg = self.calibration.get(t, {})
            a, b = cfg.get("a", 1.0), cfg.get("b", 0.0)
            out[t] = clamp(a * scores[t] + b)
        return out

    def detect(self, text: str, temperature: float = 0.3,
               max_tokens: int = 150, timeout: int = 60,
               api_key: str = None, n_shots: int = 0) -> dict[str, Any]:
        if not api_key:
            api_key = os.environ.get("JULING_API_KEY", "").strip()
        if not api_key:
            api_key, _ = resolve_api_key(Path(__file__).resolve().parent.parent)

        msgs = [{"role": "system", "content": SYSTEM_PROMPT}]
        for u, a in PANDORA_FEW_SHOTS[:n_shots]:
            msgs.append({"role": "user", "content": u})
            msgs.append({"role": "assistant", "content": a})
        msgs.append({"role": "user", "content": text[:2500]})

        result = {
            "predicted_ocean": None,
            "model": self.model,
            "temperature": temperature,
            "n_shots": n_shots,
            "success": False,
            "method": "strict_style_allonce",
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }

        raw, err = _api_call(self.api_url, api_key, self.model,
                             msgs, temperature, max_tokens, timeout)
        result["raw_excerpt"] = (raw or "")[:300]
        result["error"] = err

        ocean = parse_ocean(raw) if raw else None
        if ocean:
            result["predicted_ocean_raw"] = dict(ocean)
            result["predicted_ocean"] = self._calibrate(ocean)
            result["success"] = True

        return result


# ── Calibration ───────────────────────────────────────────────────────────────

def load_calibration(path: Path | None) -> dict | None:
    if not path or not path.exists():
        return None
    with open(path) as f:
        data = json.load(f)
    return data.get("traits", data)


def train_calibration(results: list[dict]) -> dict[str, dict]:
    coef = {}
    for t in TRAITS:
        preds, gts = [], []
        for r in results:
            if not r.get("success"):
                continue
            p = (r.get("predicted_ocean_raw") or r.get("predicted_ocean", {})).get(t)
            g = (r.get("ground_truth_ocean") or {}).get(t)
            if p is not None and g is not None:
                preds.append(float(p))
                gts.append(float(g))
        if len(preds) < 5:
            coef[t] = {"a": 1.0, "b": 0.0}
            continue
        n = len(preds)
        mx, my = sum(preds) / n, sum(gts) / n
        vx = sum((x - mx) ** 2 for x in preds) / n
        if vx < 1e-8:
            coef[t] = {"a": 1.0, "b": my - mx}
            continue
        cov_xy = sum((preds[i] - mx) * (gts[i] - my) for i in range(n)) / n
        a = cov_xy / vx
        b = my - a * mx
        coef[t] = {"a": round(a, 6), "b": round(b, 6)}
    return coef


# ── Metrics ───────────────────────────────────────────────────────────────────

def compute_summary(results: list[dict]) -> dict:
    ok = [r for r in results if r.get("success") and r.get("predicted_ocean")]
    n_total, n_ok = len(results), len(ok)
    if n_ok < 3:
        return {"n_total": n_total, "n_ok": n_ok, "macro_r": 0, "macro_mae": 0,
                "coverage": n_ok / n_total if n_total else 0, "composite": 0, "traits": {}}

    trait_m = {}
    pears, maes = [], []
    for t in TRAITS:
        gt = [float((r.get("ground_truth_ocean") or {}).get(t, 0)) for r in ok]
        pr = [float((r.get("predicted_ocean") or {}).get(t, 0)) for r in ok]
        n = len(gt)
        mg, mp = sum(gt) / n, sum(pr) / n
        sg = (sum((g - mg) ** 2 for g in gt) / n) ** 0.5
        sp = (sum((p - mp) ** 2 for p in pr) / n) ** 0.5
        r_val = sum((gt[i] - mg) * (pr[i] - mp) for i in range(n)) / (n * sg * sp) if sg > 0 and sp > 0 else 0.0
        mae = sum(abs(pr[i] - gt[i]) for i in range(n)) / n
        bias = sum(pr[i] - gt[i] for i in range(n)) / n
        trait_m[t] = {"r": r_val, "mae": mae, "bias": bias}
        pears.append(r_val)
        maes.append(mae)

    macro_r = sum(pears) / 5
    macro_mae = sum(maes) / 5
    cov = n_ok / n_total if n_total else 0
    composite = 0.5 * macro_r + 0.3 * cov + 0.2 * (1 - macro_mae)

    return {"n_total": n_total, "n_ok": n_ok, "coverage": cov,
            "macro_r": macro_r, "macro_mae": macro_mae, "composite": composite,
            "traits": trait_m}


def print_summary(s: dict, label: str = "summary") -> None:
    print(f"\n--- {label} ---")
    print(f"  processed:   {s['n_total']} samples")
    print(f"  valid:       {s['n_ok']} ({s['coverage']:.0%})")
    print(f"  macro Pearson: {s['macro_r']:.4f}")
    print(f"  macro MAE:     {s['macro_mae']:.4f}")
    print(f"  composite:     {s.get('composite', 0):.4f}")
    for t in TRAITS:
        tm = s.get("traits", {}).get(t, {})
        print(f"    {t}: r={tm.get('r', 0):.4f}  mae={tm.get('mae', 0):.4f}  bias={tm.get('bias', 0):+.4f}")


# ── Main ──────────────────────────────────────────────────────────────────────

def main() -> None:
    root = Path(__file__).resolve().parent
    eval_data = root.parent.parent.parent

    ap = argparse.ArgumentParser(description="All-at-once OCEAN Detector (strict_style)")
    ap.add_argument("--input", default=str(eval_data / "pandora" / "processed" / "pandora_eval_results_v4_20260327-1.jsonl"))
    ap.add_argument("--limit", type=int, default=100)
    ap.add_argument("--model", default=DEFAULT_MODEL)
    ap.add_argument("--temperature", type=float, default=0.3)
    ap.add_argument("--timeout", type=int, default=60)
    ap.add_argument("--n-shots", type=int, default=0)
    ap.add_argument("--sample-delay", type=float, default=0.2)
    ap.add_argument("--output", default=None)
    ap.add_argument("--api-key", default=None)
    ap.add_argument("--calibration", default=None)
    ap.add_argument("--train-calibration", action="store_true")
    args = ap.parse_args()

    print(f"All-at-once OCEAN Detector (strict_style, {args.n_shots}-shot, temp={args.temperature})")
    print(f"  {args.limit} samples, model={args.model}")
    print("=" * 70)

    samples: list[dict[str, Any]] = []
    try:
        with open(args.input, encoding="utf-8") as f:
            for i, line in enumerate(f):
                if i >= args.limit:
                    break
                samples.append(json.loads(line))
        print(f"Loaded {len(samples)} samples")
    except Exception as e:
        print(f"Failed to load input: {e}")
        return

    calibration = load_calibration(Path(args.calibration)) if args.calibration else None
    detector = OceanDetector(model=args.model, calibration=calibration)

    api_key = args.api_key or os.environ.get("JULING_API_KEY", "").strip()
    if not api_key or len(api_key) < 10:
        api_key, key_src = resolve_api_key(root, cli_key=None)
    else:
        key_src = "$JULING_API_KEY" if not args.api_key else "--api-key"
    if not api_key or len(api_key) < 10:
        print("API key missing.")
        return

    print(f"API: {key_src} → {detector.api_url}")

    run_id = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    out_dir = root / "results"
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = Path(args.output) if args.output else out_dir / f"five_trait_ocean_{run_id}.jsonl"
    out_f = open(out_path, "w", encoding="utf-8")

    results = []
    for i, sample in enumerate(samples):
        text = str(sample.get("input") or sample.get("text") or "")
        gt = sample.get("ground_truth_ocean") or {}

        result = detector.detect(
            text=text, temperature=args.temperature,
            api_key=api_key, n_shots=args.n_shots,
        )
        result["sample_id"] = sample.get("sample_id")
        result["ground_truth_ocean"] = gt
        results.append(result)

        out_f.write(json.dumps(result, ensure_ascii=False) + "\n")
        out_f.flush()

        pred = result.get("predicted_ocean", {})
        if result["success"] and pred:
            brief = " ".join(f"{t}={pred.get(t, 0):+.2f}" for t in TRAITS)
            print(f"  [{i+1}/{len(samples)}] {brief}")
        else:
            print(f"  [{i+1}/{len(samples)}] FAIL")

        time.sleep(args.sample_delay)

    out_f.close()
    print(f"\nResults: {out_path}")

    summary = compute_summary(results)
    print_summary(summary, "raw summary")

    if args.train_calibration:
        cal = train_calibration(results)
        cal_path = out_path.with_suffix(".calibration.json")
        with open(cal_path, "w") as f:
            json.dump({"traits": cal, "source": str(out_path), "n": summary["n_ok"]}, f, indent=2)
        print(f"\nCalibration: {cal_path}")
        for t in TRAITS:
            print(f"  {t}: a={cal[t]['a']:.4f} b={cal[t]['b']:.4f}")

        for r in results:
            if r.get("success") and r.get("predicted_ocean_raw"):
                raw = r["predicted_ocean_raw"]
                r["predicted_ocean"] = {t: clamp(cal[t]["a"] * raw[t] + cal[t]["b"]) for t in TRAITS}

        with open(out_path, "w", encoding="utf-8") as f:
            for r in results:
                f.write(json.dumps(r, ensure_ascii=False) + "\n")

        cal_summary = compute_summary(results)
        print_summary(cal_summary, "calibrated summary")


if __name__ == "__main__":
    main()
