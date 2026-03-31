#!/usr/bin/env python3
"""
Phase 1 — PERSONAGE Prompt Harness

Grid: prompt_strategy × n_shots × temperature on dev split.
Model fixed to llama-3.3-70b-instruct via JuLing API.

Usage:
    cd offline_investigation/scripts
    export JULING_API_KEY=...
    export JULING_API_URL=...
    python harness_personage.py                         # full grid
    python harness_personage.py --prompts strict_style minimal --shots 0 3 --temps 0.1
"""
from __future__ import annotations

import argparse
import json
import os
import re
import time
from datetime import datetime, timezone
from pathlib import Path

import requests

from prompt_bank import EXEMPLAR_IDS, PROMPT_STRATEGIES

TRAITS = ["O", "C", "E", "A", "N"]
DATA_DIR = Path(__file__).resolve().parent.parent / "data"
RESULTS_DIR = Path(__file__).resolve().parent.parent / "results"

DEFAULT_MODEL = "meta/llama-3.3-70b-instruct"


def load_jsonl(path: Path) -> list[dict]:
    rows = []
    with open(path, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                rows.append(json.loads(line))
    return rows


def clamp(v: float) -> float:
    return max(-1.0, min(1.0, float(v)))


def parse_ocean(text: str) -> dict | None:
    m = re.search(r"\{[^}]+\}", text)
    if not m:
        return None
    try:
        parsed = json.loads(m.group())
    except json.JSONDecodeError:
        return None
    if not all(isinstance(parsed.get(t), (int, float)) for t in TRAITS):
        return None
    return {t: clamp(parsed[t]) for t in TRAITS}


def build_messages(
    system_prompt: str,
    text: str,
    dev_rows: list[dict],
    n_shots: int,
) -> list[dict]:
    msgs = [{"role": "system", "content": system_prompt}]

    if n_shots > 0:
        exemplar_map = {r["id"]: r for r in dev_rows}
        used = 0
        for eid in EXEMPLAR_IDS:
            if used >= n_shots:
                break
            row = exemplar_map.get(eid)
            if not row:
                continue
            gt = row.get("ground_truth_ocean", {})
            msgs.append({"role": "user", "content": f'Utterance: "{row["input"]}"'})
            msgs.append({"role": "assistant", "content": json.dumps(gt, ensure_ascii=False)})
            used += 1

    msgs.append({"role": "user", "content": f'Utterance: "{text[:600]}"'})
    return msgs


def call_api(
    messages: list[dict],
    api_key: str,
    api_url: str,
    model: str,
    temperature: float,
) -> tuple[dict | None, str]:
    for attempt in range(3):
        try:
            resp = requests.post(
                api_url,
                json={"model": model, "messages": messages, "temperature": temperature, "max_tokens": 180},
                headers={"Content-Type": "application/json", "Authorization": f"Bearer {api_key}"},
                timeout=120,
            )
            if resp.status_code == 429:
                wait = 2 ** (attempt + 1)
                print(f"  429 rate-limited, waiting {wait}s...", flush=True)
                time.sleep(wait)
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


def run_config(
    config_id: str,
    system_prompt: str,
    n_shots: int,
    temperature: float,
    eval_rows: list[dict],
    dev_rows: list[dict],
    api_key: str,
    api_url: str,
    model: str,
    delay: float,
    out_path: Path,
):
    print(f"\n{'='*60}", flush=True)
    print(f"CONFIG: {config_id}  |  shots={n_shots}  temp={temperature}", flush=True)
    print(f"{'='*60}", flush=True)

    with open(out_path, "w", encoding="utf-8") as f:
        total = len(eval_rows)
        ok = 0
        for i, row in enumerate(eval_rows):
            msgs = build_messages(system_prompt, row["input"], dev_rows, n_shots)
            ocean, raw = call_api(msgs, api_key, api_url, model, temperature)

            result = {
                "config_id": config_id,
                "prompt_id": config_id.rsplit("_s", 1)[0],
                "n_shots": n_shots,
                "temperature": temperature,
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
    parser.add_argument("--prompts", nargs="*", default=None, help="subset of prompt ids")
    parser.add_argument("--shots", nargs="*", type=int, default=[0, 3, 5, 11])
    parser.add_argument("--temps", nargs="*", type=float, default=[0.1, 0.3])
    parser.add_argument("--model", default=DEFAULT_MODEL)
    parser.add_argument("--limit", type=int, default=None)
    parser.add_argument("--delay", type=float, default=0.3)
    parser.add_argument("--api-url", default=os.environ.get("JULING_API_URL", ""))
    parser.add_argument("--api-key", default=os.environ.get("JULING_API_KEY", ""))
    args = parser.parse_args()

    if not args.api_key:
        raise SystemExit("Set JULING_API_KEY env var")
    if not args.api_url:
        raise SystemExit("Set JULING_API_URL env var")

    dev_rows = load_jsonl(DATA_DIR / "personage_dev.jsonl")
    eval_path = DATA_DIR / f"personage_{args.split}.jsonl"
    eval_rows = load_jsonl(eval_path)
    if args.limit:
        eval_rows = eval_rows[: args.limit]

    strategies = PROMPT_STRATEGIES
    if args.prompts:
        strategies = [s for s in strategies if s["id"] in args.prompts]
        if not strategies:
            raise SystemExit(f"No matching prompts: {args.prompts}")

    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    ts = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")

    total_configs = len(strategies) * len(args.shots) * len(args.temps)
    done = 0
    for strat in strategies:
        for n_shots in args.shots:
            for temp in args.temps:
                done += 1
                config_id = f"{strat['id']}_s{n_shots}_t{str(temp).replace('.', '')}"
                out_path = RESULTS_DIR / f"harness_{config_id}_{ts}.jsonl"
                print(f"\n[{done}/{total_configs}] Starting {config_id}", flush=True)

                run_config(
                    config_id=config_id,
                    system_prompt=strat["system"],
                    n_shots=n_shots,
                    temperature=temp,
                    eval_rows=eval_rows,
                    dev_rows=dev_rows,
                    api_key=args.api_key,
                    api_url=args.api_url,
                    model=args.model,
                    delay=args.delay,
                    out_path=out_path,
                )
                print(f"  Saved: {out_path.name}", flush=True)

    print(f"\nAll {total_configs} configs complete. Results in {RESULTS_DIR}", flush=True)


if __name__ == "__main__":
    main()
