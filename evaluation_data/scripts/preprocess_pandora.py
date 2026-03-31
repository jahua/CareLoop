#!/usr/bin/env python3
"""
Preprocess PANDORA Big5 test split for Big5Loop Phase 5 evaluation.

Input (default): evaluation_data/pandora/raw/pandora_big5_test.csv
Output:
  - evaluation_data/pandora/processed/pandora_eval_test.jsonl
  - evaluation_data/pandora/processed/pandora_eval_test.csv

Normalization:
  PANDORA traits appear on [0, 100]. We map to [-1, 1] via:
    norm = (x - 50.0) / 50.0
  and clip to [-1.0, 1.0].
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import pandas as pd

EVAL_DIR = Path(__file__).resolve().parent.parent
RAW_DIR = EVAL_DIR / "pandora" / "raw"
PROCESSED_DIR = EVAL_DIR / "pandora" / "processed"

TRAITS = ["O", "C", "E", "A", "N"]


def scale_0_100_to_minus1_1(value: float) -> float:
    norm = (float(value) - 50.0) / 50.0
    return max(-1.0, min(1.0, norm))


def preprocess(
    input_path: Path = RAW_DIR / "pandora_big5_test.csv",
    output_dir: Path = PROCESSED_DIR,
    limit: int | None = None,
) -> pd.DataFrame:
    if not input_path.exists():
        raise FileNotFoundError(f"Input not found: {input_path}")

    df = pd.read_csv(input_path)
    required = set(TRAITS + ["text"]) 
    missing = required - set(df.columns)
    if missing:
        raise ValueError(f"Missing required columns: {sorted(missing)}")

    df = df.dropna(subset=["text", *TRAITS]).copy()
    if limit is not None:
        df = df.head(limit).copy()

    # Canonical eval table
    out = pd.DataFrame(
        {
            "sample_id": df.get("__index_level_0__", df.index).astype(str),
            "text": df["text"].astype(str).str.strip(),
            "ptype": df.get("ptype", None),
        }
    )

    for t in TRAITS:
        out[t] = df[t].apply(scale_0_100_to_minus1_1)

    output_dir.mkdir(parents=True, exist_ok=True)

    jsonl_path = output_dir / "pandora_eval_test.jsonl"
    with open(jsonl_path, "w", encoding="utf-8") as f:
        for _, row in out.iterrows():
            obj = {
                "sample_id": row["sample_id"],
                "input": row["text"],
                "ground_truth_ocean": {
                    "O": float(row["O"]),
                    "C": float(row["C"]),
                    "E": float(row["E"]),
                    "A": float(row["A"]),
                    "N": float(row["N"]),
                },
                "meta": {
                    "source": "pandora_big5_test",
                    "ptype": int(row["ptype"]) if pd.notna(row["ptype"]) else None,
                },
            }
            f.write(json.dumps(obj, ensure_ascii=False) + "\n")

    csv_path = output_dir / "pandora_eval_test.csv"
    out.to_csv(csv_path, index=False)

    print(f"Saved JSONL: {jsonl_path}")
    print(f"Saved CSV:   {csv_path}")
    print(f"Rows: {len(out)}")

    return out


def main() -> None:
    parser = argparse.ArgumentParser(description="Preprocess PANDORA Big5 test split")
    parser.add_argument(
        "--input",
        type=str,
        default=str(RAW_DIR / "pandora_big5_test.csv"),
        help="Path to pandora_big5_test.csv",
    )
    parser.add_argument(
        "--output-dir",
        type=str,
        default=str(PROCESSED_DIR),
        help="Output directory for processed files",
    )
    parser.add_argument("--limit", type=int, default=None, help="Optional row limit")
    args = parser.parse_args()

    preprocess(input_path=Path(args.input), output_dir=Path(args.output_dir), limit=args.limit)


if __name__ == "__main__":
    main()
