#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import os
import re
import time
from pathlib import Path

import requests

from prompt_bank import SYSTEM_PROMPTS, build_fewshot_messages, load_jsonl


MODELS = {
    "llama70b": "meta/llama-3.3-70b-instruct",
    "llama8b": "meta/llama-3.1-8b-instruct",
    "gemma": "google/gemma-3n-e4b-it",
    "mistral": "mistralai/mistral-7b-instruct-v0.3",
}

TRAITS = ["O", "C", "E", "A", "N"]


def clamp(v: float) -> float:
    return max(-1.0, min(1.0, float(v)))


def parse_json_object(text: str) -> dict | None:
    match = re.search(r"\{[^}]+\}", text)
    if not match:
        return None
    parsed = json.loads(match.group())
    if not isinstance(parsed.get("O"), (int, float)):
        return None
    return {trait: clamp(parsed.get(trait, 0.0)) for trait in TRAITS}


def call_variant(
    text: str,
    api_key: str,
    api_url: str,
    model: str,
    temperature: float,
    dataset_rows: list[dict],
    variant: str,
) -> tuple[dict | None, str]:
    messages = build_fewshot_messages(dataset_rows, variant=variant)
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


def ensemble_average(outputs: list[dict]) -> dict:
    return {
        trait: round(sum(out[trait] for out in outputs) / len(outputs), 6)
        for trait in TRAITS
    }


def write_jsonl(path: Path, rows: list[dict]) -> None:
    with open(path, "w", encoding="utf-8") as f:
        for row in rows:
            f.write(json.dumps(row, ensure_ascii=False) + "\n")


def main() -> None:
    parser = argparse.ArgumentParser(description="Run isolated PERSONAGE benchmark with multi-prompt ensembling")
    default_data_dir = Path(__file__).resolve().parent / "data"
    parser.add_argument("--split", choices=["dev", "test"], default="dev")
    parser.add_argument("--input")
    parser.add_argument("--delay", type=float, default=0.2)
    parser.add_argument("--temperature", type=float, default=0.1)
    parser.add_argument("--model", default="llama70b")
    parser.add_argument("--limit", type=int, default=None)
    parser.add_argument("--api-url", default=os.environ.get("NVIDIA_API_URL", "https://integrate.api.nvidia.com/v1/chat/completions"))
    parser.add_argument("--api-key", default=os.environ.get("NVIDIA_API_KEY", ""))
    parser.add_argument("--output-dir", default=str(Path(__file__).resolve().parent / "results"))
    parser.add_argument(
        "--variants",
        nargs="+",
        default=["benchmark", "trait_first", "anti_conflation"],
        help=f"Prompt variants to ensemble. Available: {', '.join(SYSTEM_PROMPTS)}",
    )
    args = parser.parse_args()

    if not args.api_key:
        raise SystemExit("NVIDIA_API_KEY is required")

    for variant in args.variants:
        if variant not in SYSTEM_PROMPTS:
            raise SystemExit(f"Unknown variant: {variant}")

    input_path = Path(args.input) if args.input else default_data_dir / f"personage_{args.split}.jsonl"
    if not input_path.exists():
        raise SystemExit(f"Missing split file: {input_path}. Run create_splits.py first.")

    eval_rows = load_jsonl(input_path)
    if args.limit:
        eval_rows = eval_rows[: args.limit]
    dev_rows = load_jsonl(default_data_dir / "personage_dev.jsonl")

    model = MODELS.get(args.model, args.model)
    results: list[dict] = []

    for idx, row in enumerate(eval_rows, start=1):
        print(f"[{idx}/{len(eval_rows)}] {row['id'][:60]}...", flush=True)
        variant_outputs = {}
        variant_errors = {}
        for variant in args.variants:
            try:
                ocean, raw = call_variant(
                    text=row["input"],
                    api_key=args.api_key,
                    api_url=args.api_url,
                    model=model,
                    temperature=args.temperature,
                    dataset_rows=dev_rows,
                    variant=variant,
                )
                variant_outputs[variant] = {"detected_ocean": ocean, "raw_api": raw}
                if ocean:
                    vals = " ".join(f"{k}={ocean[k]:+.2f}" for k in TRAITS)
                    print(f"  - {variant}: {vals}", flush=True)
                else:
                    variant_errors[variant] = "no_json"
                    print(f"  - {variant}: no_json", flush=True)
            except Exception as exc:
                variant_errors[variant] = str(exc)
                print(f"  - {variant}: ERR {exc}", flush=True)

        valid = [payload["detected_ocean"] for payload in variant_outputs.values() if payload["detected_ocean"]]
        detected = ensemble_average(valid) if valid else None
        results.append(
            {
                **row,
                "detected_ocean": detected,
                "variant_outputs": variant_outputs,
                "variant_errors": variant_errors or None,
                "error": None if detected else "No valid ensemble outputs",
            }
        )
        if args.delay > 0:
            time.sleep(args.delay)

    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    safe_model = model.replace("/", "_").replace(".", "_")
    variant_tag = "-".join(args.variants)
    out_path = output_dir / f"{args.split}_ensemble_{variant_tag}_{safe_model}_t{str(args.temperature).replace('.', '')}.jsonl"
    write_jsonl(out_path, results)
    print(f"Saved results: {out_path}")


if __name__ == "__main__":
    main()
