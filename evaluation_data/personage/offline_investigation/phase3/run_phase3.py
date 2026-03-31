#!/usr/bin/env python3
"""
Phase 3 — Final Test Evaluation + E-improved comparison

Runs on test set (288 samples):
  A) Original winner: trait_first v1, 11-shot (original exemplars), temp 0.3
  B) E-improved:      trait_first v2, 11-shot (rebalanced exemplars), temp 0.3

Also runs v2 on dev set first (80 samples) for quick validation.

Usage:
    cd phase3
    python run_phase3.py --mode dev-check   # quick v2 validation on 80 dev samples
    python run_phase3.py --mode test        # full test: v1 + v2 on 288 test samples
    python run_phase3.py --mode all         # both
"""
from __future__ import annotations

import argparse
import json
import os
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

import requests

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))
from harness_personage import load_jsonl, parse_ocean, clamp, TRAITS
from prompt_bank import PROMPT_STRATEGIES, EXEMPLAR_IDS

from prompt_bank_v2 import TRAIT_FIRST_V2, EXEMPLAR_IDS_V2

DATA_DIR = Path(__file__).resolve().parent.parent / "data"
RESULTS_DIR = Path(__file__).resolve().parent / "results"

MODEL = "meta/llama-3.3-70b-instruct"


def build_messages(system_prompt, text, dev_rows, exemplar_ids, n_shots):
    msgs = [{"role": "system", "content": system_prompt}]
    if n_shots > 0:
        emap = {r["id"]: r for r in dev_rows}
        used = 0
        for eid in exemplar_ids:
            if used >= n_shots:
                break
            row = emap.get(eid)
            if not row:
                continue
            gt = row.get("ground_truth_ocean", {})
            msgs.append({"role": "user", "content": f'Utterance: "{row["input"]}"'})
            msgs.append({"role": "assistant", "content": json.dumps(gt, ensure_ascii=False)})
            used += 1
    msgs.append({"role": "user", "content": f'Utterance: "{text[:600]}"'})
    return msgs


def call_api(messages, api_key, api_url, temperature=0.3):
    for attempt in range(3):
        try:
            resp = requests.post(
                api_url,
                json={"model": MODEL, "messages": messages, "temperature": temperature, "max_tokens": 200},
                headers={"Content-Type": "application/json", "Authorization": f"Bearer {api_key}"},
                timeout=120,
            )
            if resp.status_code == 429:
                time.sleep(2 ** (attempt + 1))
                continue
            resp.raise_for_status()
            raw = resp.json().get("choices", [{}])[0].get("message", {}).get("content", "")
            return parse_ocean(raw), raw
        except Exception as exc:
            if attempt < 2:
                time.sleep(2)
                continue
            return None, str(exc)
    return None, "max_retries"


def run_eval(tag, system_prompt, exemplar_ids, eval_rows, dev_rows, api_key, api_url, delay=0.3):
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    ts = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    out_path = RESULTS_DIR / f"phase3_{tag}_{ts}.jsonl"

    print(f"\n{'='*60}", flush=True)
    print(f"  {tag}  |  {len(eval_rows)} samples  |  {MODEL}", flush=True)
    print(f"{'='*60}", flush=True)

    ok = 0
    with open(out_path, "w", encoding="utf-8") as f:
        for i, row in enumerate(eval_rows):
            msgs = build_messages(system_prompt, row["input"], dev_rows, exemplar_ids, 11)
            ocean, raw = call_api(msgs, api_key, api_url)
            result = {
                "tag": tag,
                "sample_id": row.get("id", i),
                "input": row["input"],
                "ground_truth_ocean": row.get("ground_truth_ocean"),
                "detected_ocean": ocean,
                "raw_api": raw,
            }
            f.write(json.dumps(result, ensure_ascii=False) + "\n")
            f.flush()
            if ocean:
                ok += 1
                tag_str = " ".join(f"{t}={ocean[t]:+.2f}" for t in TRAITS)
                print(f"  [{i+1}/{len(eval_rows)}] OK {tag_str}", flush=True)
            else:
                print(f"  [{i+1}/{len(eval_rows)}] NO_JSON", flush=True)
            if delay > 0:
                time.sleep(delay)

    print(f"  Coverage: {ok}/{len(eval_rows)} ({100*ok/len(eval_rows):.0f}%)", flush=True)
    print(f"  Saved: {out_path.name}", flush=True)
    return out_path


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", choices=["dev-check", "test", "all"], default="all")
    parser.add_argument("--limit", type=int, default=None)
    parser.add_argument("--delay", type=float, default=0.3)
    args = parser.parse_args()

    api_key = os.environ.get("JULING_API_KEY", "")
    api_url = os.environ.get("JULING_API_URL", "")
    if not api_key or not api_url:
        raise SystemExit("Set JULING_API_KEY and JULING_API_URL env vars")

    dev_rows = load_jsonl(DATA_DIR / "personage_dev.jsonl")
    test_rows = load_jsonl(DATA_DIR / "personage_test.jsonl")
    if args.limit:
        test_rows = test_rows[:args.limit]

    v1_prompt = next(s for s in PROMPT_STRATEGIES if s["id"] == "trait_first")["system"]
    v2_prompt = TRAIT_FIRST_V2["system"]

    if args.mode in ("dev-check", "all"):
        dev_eval = dev_rows[:80]
        run_eval("v2_dev", v2_prompt, EXEMPLAR_IDS_V2, dev_eval, dev_rows, api_key, api_url, args.delay)

    if args.mode in ("test", "all"):
        run_eval("v1_test", v1_prompt, EXEMPLAR_IDS, test_rows, dev_rows, api_key, api_url, args.delay)
        run_eval("v2_test", v2_prompt, EXEMPLAR_IDS_V2, test_rows, dev_rows, api_key, api_url, args.delay)

    print("\nPhase 3 complete.", flush=True)


if __name__ == "__main__":
    main()
