#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import os
import re
import time
from pathlib import Path

from prompt_bank import build_fewshot_messages, load_jsonl

try:
    import requests
except ImportError as exc:  # pragma: no cover
    raise SystemExit(f"requests is required: {exc}")


MODELS = {
    "llama70b": "meta/llama-3.3-70b-instruct",
    "llama8b": "meta/llama-3.1-8b-instruct",
    "gemma": "google/gemma-3n-e4b-it",
    "mistral": "mistralai/mistral-7b-instruct-v0.3",
}


def clamp(v: float) -> float:
    return max(-1.0, min(1.0, float(v)))


def parse_json_object(text: str) -> dict | None:
    match = re.search(r"\{[^}]+\}", text)
    if not match:
        return None
    parsed = json.loads(match.group())
    if not isinstance(parsed.get("O"), (int, float)):
        return None
    return {
        "O": clamp(parsed.get("O", 0)),
        "C": clamp(parsed.get("C", 0)),
        "E": clamp(parsed.get("E", 0)),
        "A": clamp(parsed.get("A", 0)),
        "N": clamp(parsed.get("N", 0)),
    }


def call_model(text: str, api_key: str, api_url: str, model: str, temperature: float, dataset_rows: list[dict]) -> tuple[dict | None, str]:
    messages = build_fewshot_messages(dataset_rows)
    messages.append({"role": "user", "content": f'Utterance: "{text[:600]}"'})

    resp = requests.post(
        api_url,
        json={
            "model": model,
            "messages": messages,
            "temperature": temperature,
            "max_tokens": 180,
        },
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}",
        },
        timeout=90,
    )
    resp.raise_for_status()
    body = resp.json()
    raw = body.get("choices", [{}])[0].get("message", {}).get("content", "")
    return parse_json_object(raw), raw


def run_eval(rows: list[dict], dataset_rows: list[dict], api_key: str, api_url: str, model: str, temperature: float, delay_sec: float) -> list[dict]:
    results: list[dict] = []
    total = len(rows)
    for idx, row in enumerate(rows, start=1):
        print(f"[{idx}/{total}] {row['id'][:60]}...", end=" ", flush=True)
        try:
            ocean, raw = call_model(row["input"], api_key, api_url, model, temperature, dataset_rows)
            out = {**row, "detected_ocean": ocean, "raw_api": raw, "error": None}
            results.append(out)
            if ocean:
                vals = " ".join(f"{k}={ocean[k]:+.2f}" for k in "OCEAN")
                print(f"OK {vals}", flush=True)
            else:
                print("NO_JSON", flush=True)
        except Exception as exc:
            out = {**row, "detected_ocean": None, "raw_api": None, "error": str(exc)}
            results.append(out)
            print(f"ERR {exc}", flush=True)
        if delay_sec > 0:
            time.sleep(delay_sec)
    return results


def write_jsonl(path: Path, rows: list[dict]) -> None:
    with open(path, "w", encoding="utf-8") as f:
        for row in rows:
            f.write(json.dumps(row, ensure_ascii=False) + "\n")


def main() -> None:
    parser = argparse.ArgumentParser(description="Run isolated PERSONAGE benchmark with a benchmark-only prompt")
    default_data_dir = Path(__file__).resolve().parent / "data"
    parser.add_argument("--split", choices=["dev", "test"], default="dev")
    parser.add_argument("--input")
    parser.add_argument("--seed", type=int, default=2026)
    parser.add_argument("--delay", type=float, default=0.2)
    parser.add_argument("--temperature", type=float, default=0.1)
    parser.add_argument("--model", default="llama70b")
    parser.add_argument("--limit", type=int, default=None)
    parser.add_argument("--api-url", default=os.environ.get("NVIDIA_API_URL", "https://integrate.api.nvidia.com/v1/chat/completions"))
    parser.add_argument("--api-key", default=os.environ.get("NVIDIA_API_KEY", ""))
    parser.add_argument("--output-dir", default=str(Path(__file__).resolve().parent / "results"))
    args = parser.parse_args()

    if not args.api_key:
        raise SystemExit("NVIDIA_API_KEY is required")

    input_path = Path(args.input) if args.input else default_data_dir / f"personage_{args.split}.jsonl"
    if not input_path.exists():
        raise SystemExit(f"Missing split file: {input_path}. Run create_splits.py first.")

    dataset_rows = load_jsonl(input_path)
    if args.limit:
        dataset_rows = dataset_rows[: args.limit]

    model = MODELS.get(args.model, args.model)
    results = run_eval(
        rows=dataset_rows,
        dataset_rows=load_jsonl(default_data_dir / "personage_dev.jsonl"),
        api_key=args.api_key,
        api_url=args.api_url,
        model=model,
        temperature=args.temperature,
        delay_sec=args.delay,
    )

    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    safe_model = model.replace("/", "_").replace(".", "_")
    out_path = output_dir / f"{args.split}_{safe_model}_t{str(args.temperature).replace('.', '')}.jsonl"
    write_jsonl(out_path, results)
    print(f"Saved results: {out_path}")


if __name__ == "__main__":
    main()
