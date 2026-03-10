#!/usr/bin/env python3
"""
Preprocess PERSONAGE for Big5Loop evaluation.

PERSONAGE has human ratings (1-7) for ALL five OCEAN traits per utterance:
avg.extra, avg.ems, avg.agree, avg.consc, avg.open

Scale: 1-7 -> [-1, 1] via (x-4)/3. Neutral=4 -> 0. Matches Big5Loop T in [-1,1]^5.
Neuroticism: N = -scale(EMS) (high emotional stability -> low N).

Output: personage_eval.jsonl with input, ground_truth_ocean {O,C,E,A,N}, id.
Best for evaluation: full OCEAN comparison (not single-trait like BIG5-CHAT)
"""
import argparse
import json
from pathlib import Path
from typing import List, Optional

import pandas as pd

EVAL_DIR = Path(__file__).resolve().parent.parent
RAW_DIR = EVAL_DIR / "raw"
PERSONAGE_DIR = EVAL_DIR / "personage"
PERSONAGE_PROCESSED = PERSONAGE_DIR / "processed"


def scale_1_7_to_minus1_1(x):
    """Map PERSONAGE 1-7 scale to [-1, 1]. Neutral (4) -> 0.
    Formula: (x - 4) / 3. Matches Big5Loop trait vector T in [-1,1]^5."""
    return (float(x) - 4) / 3


def ems_to_neuroticism(ems):
    """Emotional Stability (1-7) -> Neuroticism [-1, 1]. High EMS = low N.
    N = -scale(EMS): EMS high -> N negative, EMS low -> N positive."""
    return -scale_1_7_to_minus1_1(ems)


def preprocess(
    predefined_path: Path = RAW_DIR / "predefinedParams.tab",
    random_path: Path = RAW_DIR / "randomParams.tab",
    output_dir: Path = PERSONAGE_PROCESSED,
    limit: Optional[int] = None,
) -> List[dict]:
    """Load PERSONAGE tab files, output Big5Loop-ready JSONL with full OCEAN."""
    output_dir.mkdir(parents=True, exist_ok=True)

    records = []

    for path in [predefined_path, random_path]:
        if not path.exists():
            continue
        df = pd.read_csv(path, sep="\t")
        df = df.dropna(subset=["realization", "avg.extra", "avg.agree", "avg.consc", "avg.open"])
        if "avg.ems" in df.columns:
            df = df[df["avg.ems"].notna() & (df["avg.ems"] != "n/a")]
        else:
            continue

        for _, row in df.iterrows():
            try:
                ems = float(row["avg.ems"])
            except (ValueError, TypeError):
                continue
            gt = {
                "O": scale_1_7_to_minus1_1(row["avg.open"]),
                "C": scale_1_7_to_minus1_1(row["avg.consc"]),
                "E": scale_1_7_to_minus1_1(row["avg.extra"]),
                "A": scale_1_7_to_minus1_1(row["avg.agree"]),
                "N": ems_to_neuroticism(ems),
            }
            records.append({
                "id": row.get("id", ""),
                "input": str(row["realization"]).strip(),
                "ground_truth_ocean": gt,
            })
            if limit and len(records) >= limit:
                break
        if limit and len(records) >= limit:
            break

    out_path = output_dir / "personage_eval.jsonl"
    with open(out_path, "w") as f:
        for r in records:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")

    print(f"Saved {len(records)} rows to {out_path}")
    return records


def main():
    p = argparse.ArgumentParser(description="Preprocess PERSONAGE for full OCEAN evaluation")
    p.add_argument("--limit", type=int, default=None)
    p.add_argument("-o", "--output", default=str(PERSONAGE_PROCESSED))
    args = p.parse_args()

    preprocess(
        output_dir=Path(args.output),
        limit=args.limit,
    )


if __name__ == "__main__":
    main()
