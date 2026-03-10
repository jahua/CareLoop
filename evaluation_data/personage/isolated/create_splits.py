#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import random
from collections import defaultdict
from pathlib import Path

from prompt_bank import EXEMPLAR_IDS


def load_jsonl(path: Path) -> list[dict]:
    rows: list[dict] = []
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                rows.append(json.loads(line))
    return rows


def write_jsonl(path: Path, rows: list[dict]) -> None:
    with open(path, "w", encoding="utf-8") as f:
        for row in rows:
            f.write(json.dumps(row, ensure_ascii=False) + "\n")


def bucket_key(row_id: str) -> str:
    parts = row_id.split("-")
    return "-".join(parts[:2]) if len(parts) >= 2 else row_id


def make_splits(rows: list[dict], seed: int) -> tuple[list[dict], list[dict]]:
    rows_by_id = {row["id"]: row for row in rows}
    missing = [row_id for row_id in EXEMPLAR_IDS if row_id not in rows_by_id]
    if missing:
        raise ValueError(f"Exemplar ids missing from dataset: {missing}")

    rng = random.Random(seed)
    buckets: dict[str, list[dict]] = defaultdict(list)
    for row in rows:
        buckets[bucket_key(row["id"])].append(row)

    dev: list[dict] = []
    test: list[dict] = []
    forced_dev_ids = set(EXEMPLAR_IDS)

    for bucket in sorted(buckets):
        bucket_rows = list(buckets[bucket])
        forced = [row for row in bucket_rows if row["id"] in forced_dev_ids]
        remaining = [row for row in bucket_rows if row["id"] not in forced_dev_ids]
        rng.shuffle(remaining)

        target_dev = len(bucket_rows) // 2
        if len(bucket_rows) % 2 == 1:
            target_dev += 1

        take_from_remaining = max(0, target_dev - len(forced))
        dev.extend(forced)
        dev.extend(remaining[:take_from_remaining])
        test.extend(remaining[take_from_remaining:])

        # If exemplars exceed the nominal half-split for a bucket, allow it.
        if len(forced) > target_dev:
            pass

    dev_ids = {row["id"] for row in dev}
    test = [row for row in test if row["id"] not in dev_ids]

    # Deterministic ordering for reproducibility.
    dev = sorted(dev, key=lambda row: row["id"])
    test = sorted(test, key=lambda row: row["id"])
    return dev, test


def main() -> None:
    parser = argparse.ArgumentParser(description="Create isolated stratified PERSONAGE dev/test splits")
    parser.add_argument(
        "--input",
        default=str(Path(__file__).resolve().parents[1] / "processed" / "personage_eval.jsonl"),
    )
    parser.add_argument(
        "--output-dir",
        default=str(Path(__file__).resolve().parent / "data"),
    )
    parser.add_argument("--seed", type=int, default=2026)
    args = parser.parse_args()

    input_path = Path(args.input)
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    rows = load_jsonl(input_path)
    dev, test = make_splits(rows, seed=args.seed)

    write_jsonl(output_dir / "personage_dev.jsonl", dev)
    write_jsonl(output_dir / "personage_test.jsonl", test)

    manifest = {
        "seed": args.seed,
        "input": str(input_path),
        "dev_size": len(dev),
        "test_size": len(test),
        "exemplar_ids": EXEMPLAR_IDS,
    }
    (output_dir / "split_manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")

    print(f"Saved dev split:  {output_dir / 'personage_dev.jsonl'} ({len(dev)} rows)")
    print(f"Saved test split: {output_dir / 'personage_test.jsonl'} ({len(test)} rows)")
    print(f"Saved manifest:   {output_dir / 'split_manifest.json'}")


if __name__ == "__main__":
    main()
