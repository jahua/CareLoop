#!/usr/bin/env python3
"""
Phase 2 — Multi-Model Benchmark on PERSONAGE

Runs the winning prompt config from Phase 1 across multiple models.

Usage:
    cd offline_investigation/scripts
    export JULING_API_KEY=...  JULING_API_URL=...
    python benchmark_models.py --prompt-id strict_style --shots 0 --temp 0.1
    python benchmark_models.py --prompt-id strict_style --shots 0 --temp 0.1 --split test
"""
from __future__ import annotations

import argparse
import json
import os
import time
from datetime import datetime, timezone
from pathlib import Path

import requests

from prompt_bank import PROMPT_STRATEGIES, EXEMPLAR_IDS

DATA_DIR = Path(__file__).resolve().parent.parent / "data"
RESULTS_DIR = Path(__file__).resolve().parent.parent / "results"

BENCHMARK_MODELS = {
    "llama-3.3-70b": "meta/llama-3.3-70b-instruct",
    "deepseek-chat": "deepseek-chat",
    "gemini-3-flash": "gemini-3-flash-preview-nothinking",
    "gpt-5.1": "gpt-5.1",
    "claude-sonnet-4.6": "claude-sonnet-4.6",
    "qwen3.5-397b": "qwen/qwen3.5-397b-a17b",
    "kimi-k2.5": "moonshotai/kimi-k2.5",
    "grok-4": "grok-4",
}

TRAITS = ["O", "C", "E", "A", "N"]

# reuse helpers from harness
from harness_personage import load_jsonl, parse_ocean, build_messages, clamp


def call_api(messages, api_key, api_url, model, temperature):
    for attempt in range(3):
        try:
            resp = requests.post(
                api_url,
                json={"model": model, "messages": messages, "temperature": temperature, "max_tokens": 2000},
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


def run_model(
    model_key: str,
    model_id: str,
    system_prompt: str,
    n_shots: int,
    temperature: float,
    eval_rows: list[dict],
    dev_rows: list[dict],
    api_key: str,
    api_url: str,
    delay: float,
    out_path: Path,
):
    print(f"\n{'='*60}", flush=True)
    print(f"MODEL: {model_key} ({model_id})", flush=True)
    print(f"{'='*60}", flush=True)

    with open(out_path, "w", encoding="utf-8") as f:
        total = len(eval_rows)
        ok = 0
        for i, row in enumerate(eval_rows):
            msgs = build_messages(system_prompt, row["input"], dev_rows, n_shots)
            ocean, raw = call_api(msgs, api_key, api_url, model_id, temperature)
            result = {
                "model_key": model_key,
                "model_id": model_id,
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
                tag = " ".join(f"{t}={ocean[t]:+.2f}" for t in TRAITS)
                print(f"  [{i+1}/{total}] OK {tag}", flush=True)
            else:
                print(f"  [{i+1}/{total}] NO_JSON", flush=True)
            if delay > 0:
                time.sleep(delay)
        print(f"  Coverage: {ok}/{total} ({100*ok/total:.0f}%)", flush=True)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--split", default="dev", choices=["dev", "test"])
    parser.add_argument("--prompt-id", required=True, help="winning prompt strategy id")
    parser.add_argument("--shots", type=int, required=True)
    parser.add_argument("--temp", type=float, required=True)
    parser.add_argument("--models", nargs="*", default=None, help="subset of model keys")
    parser.add_argument("--limit", type=int, default=None)
    parser.add_argument("--delay", type=float, default=0.3)
    parser.add_argument("--api-url", default=os.environ.get("JULING_API_URL", ""))
    parser.add_argument("--api-key", default=os.environ.get("JULING_API_KEY", ""))
    args = parser.parse_args()

    if not args.api_key or not args.api_url:
        raise SystemExit("Set JULING_API_KEY and JULING_API_URL env vars")

    strat = next((s for s in PROMPT_STRATEGIES if s["id"] == args.prompt_id), None)
    if not strat:
        raise SystemExit(f"Unknown prompt id: {args.prompt_id}")

    dev_rows = load_jsonl(DATA_DIR / "personage_dev.jsonl")
    eval_rows = load_jsonl(DATA_DIR / f"personage_{args.split}.jsonl")
    if args.limit:
        eval_rows = eval_rows[: args.limit]

    models = BENCHMARK_MODELS
    if args.models:
        models = {k: v for k, v in models.items() if k in args.models}

    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    ts = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")

    for model_key, model_id in models.items():
        out_path = RESULTS_DIR / f"benchmark_{model_key}_{args.split}_{ts}.jsonl"
        run_model(
            model_key=model_key,
            model_id=model_id,
            system_prompt=strat["system"],
            n_shots=args.shots,
            temperature=args.temp,
            eval_rows=eval_rows,
            dev_rows=dev_rows,
            api_key=args.api_key,
            api_url=args.api_url,
            delay=args.delay,
            out_path=out_path,
        )
        print(f"  Saved: {out_path.name}", flush=True)

    print(f"\nAll models done. Results in {RESULTS_DIR}", flush=True)


if __name__ == "__main__":
    main()
