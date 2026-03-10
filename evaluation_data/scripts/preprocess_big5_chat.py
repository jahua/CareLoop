#!/usr/bin/env python3
"""
Preprocess BIG5-CHAT for Big5Loop evaluation.

- Drops nulls in train_input / train_output
- Removes exact duplicate (input, trait, level) rows
- Optionally samples stratified by (trait, level) for smaller eval sets
- Outputs JSONL and/or CSV in Big5Loop-ready format
"""
import argparse
import json
from pathlib import Path
from typing import Optional

import pandas as pd

EVAL_DIR = Path(__file__).resolve().parent.parent
RAW_DIR = EVAL_DIR / "raw"
PROCESSED_DIR = EVAL_DIR / "processed"


def preprocess(
    input_path: Path = RAW_DIR / "big5_chat_dataset.csv",
    output_dir: Path = PROCESSED_DIR,
    sample_per_cell: Optional[int] = None,
    seed: int = 42,
) -> pd.DataFrame:
    df = pd.read_csv(input_path)

    # 1. Drop nulls
    before = len(df)
    df = df.dropna(subset=["train_input", "train_output"])
    print(f"Dropped {before - len(df)} rows with null input/output")

    # 2. Remove exact duplicates (same input, trait, level)
    before = len(df)
    df = df.drop_duplicates(subset=["train_input", "trait", "level"], keep="first")
    print(f"Dropped {before - len(df)} duplicate (input, trait, level) rows")

    # 3. Optional stratified sampling
    if sample_per_cell is not None:
        sampled = []
        for (trait, level), group in df.groupby(["trait", "level"]):
            n = min(sample_per_cell, len(group))
            sampled.append(group.sample(n=n, random_state=seed))
        df = pd.concat(sampled, ignore_index=True)
        print(f"Sampled {sample_per_cell} per (trait, level) → {len(df)} rows")

    # 4. Trim whitespace
    df["train_input"] = df["train_input"].str.strip()
    df["train_output"] = df["train_output"].str.strip()

    # 5. Save outputs
    output_dir.mkdir(parents=True, exist_ok=True)

    # Big5Loop-ready JSONL: one object per line for easy streaming
    jsonl_path = output_dir / "big5_chat_eval.jsonl"
    with open(jsonl_path, "w") as f:
        for _, row in df.iterrows():
            obj = {
                "input": row["train_input"],
                "expected_output": row["train_output"],
                "trait": row["trait"],
                "level": row["level"],
                "ground_truth": f"{row['trait']}_{row['level']}",
            }
            f.write(json.dumps(obj, ensure_ascii=False) + "\n")
    print(f"Saved: {jsonl_path}")

    # Compact CSV for inspection
    csv_path = output_dir / "big5_chat_eval.csv"
    df[["trait", "level", "train_input", "train_output"]].to_csv(
        csv_path, index=False
    )
    print(f"Saved: {csv_path}")

    return df


def main():
    p = argparse.ArgumentParser(description="Preprocess BIG5-CHAT for Big5Loop eval")
    p.add_argument(
        "--sample",
        type=int,
        default=None,
        help="Sample N per (trait, level). Default: use all (after dedup).",
    )
    p.add_argument("--seed", type=int, default=42)
    args = p.parse_args()

    print("=== BIG5-CHAT Preprocessing ===\n")
    df = preprocess(sample_per_cell=args.sample, seed=args.seed)
    print(f"\nFinal: {len(df)} rows")
    print(df.groupby(["trait", "level"]).size().unstack(fill_value=0))


if __name__ == "__main__":
    main()
