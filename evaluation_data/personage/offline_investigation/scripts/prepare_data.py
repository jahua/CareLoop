#!/usr/bin/env python3
"""
Create dev/test splits from the full 580-row personage_eval.jsonl.

Exemplar IDs are forced into dev. Rows are stratified by bucket (id prefix).
50/50 split within each bucket.
"""
from __future__ import annotations

import json
import random
from collections import defaultdict
from pathlib import Path

from prompt_bank import EXEMPLAR_IDS

ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT / "data"
SOURCE = ROOT.parent / "processed" / "personage_eval.jsonl"


def load_jsonl(path: Path) -> list[dict]:
    with open(path, encoding="utf-8") as f:
        return [json.loads(line) for line in f if line.strip()]


def write_jsonl(path: Path, rows: list[dict]):
    with open(path, "w", encoding="utf-8") as f:
        for r in rows:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")


def bucket_key(row_id: str) -> str:
    parts = row_id.split("-")
    return "-".join(parts[:2]) if len(parts) >= 2 else row_id


def make_splits(rows: list[dict], seed: int = 2026):
    rng = random.Random(seed)
    forced_dev = set(EXEMPLAR_IDS)

    buckets: dict[str, list[dict]] = defaultdict(list)
    for row in rows:
        buckets[bucket_key(row["id"])].append(row)

    dev, test = [], []
    for bk in sorted(buckets):
        items = list(buckets[bk])
        forced = [r for r in items if r["id"] in forced_dev]
        rest = [r for r in items if r["id"] not in forced_dev]
        rng.shuffle(rest)

        target_dev = len(items) // 2 + (len(items) % 2)
        take = max(0, target_dev - len(forced))
        dev.extend(forced)
        dev.extend(rest[:take])
        test.extend(rest[take:])

    dev = sorted(dev, key=lambda r: r["id"])
    test = sorted(test, key=lambda r: r["id"])
    return dev, test


def main():
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    rows = load_jsonl(SOURCE)
    dev, test = make_splits(rows)
    write_jsonl(DATA_DIR / "personage_dev.jsonl", dev)
    write_jsonl(DATA_DIR / "personage_test.jsonl", test)

    manifest = {
        "seed": 2026,
        "source": str(SOURCE),
        "total": len(rows),
        "dev_size": len(dev),
        "test_size": len(test),
        "full_ocean_dev": sum(1 for r in dev if r.get("has_full_ocean", True)),
        "full_ocean_test": sum(1 for r in test if r.get("has_full_ocean", True)),
    }
    (DATA_DIR / "split_manifest.json").write_text(json.dumps(manifest, indent=2))
    print(f"dev: {len(dev)}  test: {len(test)}  total: {len(dev)+len(test)}")
    print(f"full OCEAN — dev: {manifest['full_ocean_dev']}  test: {manifest['full_ocean_test']}")


if __name__ == "__main__":
    main()
