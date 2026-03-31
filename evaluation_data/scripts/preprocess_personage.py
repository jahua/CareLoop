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
import math
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


def _safe_float(val) -> Optional[float]:
    if val is None or (isinstance(val, str) and val.strip().lower() in ("", "n/a", "nan")):
        return None
    try:
        v = float(val)
        return None if math.isnan(v) else v
    except (ValueError, TypeError):
        return None


def preprocess(
    predefined_path: Path = RAW_DIR / "predefinedParams.tab",
    random_path: Path = RAW_DIR / "randomParams.tab",
    output_dir: Path = PERSONAGE_PROCESSED,
    limit: Optional[int] = None,
    full_ocean_only: bool = False,
) -> List[dict]:
    """Load PERSONAGE tab files, output Big5Loop-ready JSONL.

    If full_ocean_only=True, keep only rows with all 5 traits (legacy behaviour).
    If False (default), include rows with partial traits (E-only rows get
    ground_truth with only E; other traits are null).
    """
    output_dir.mkdir(parents=True, exist_ok=True)

    records = []

    for path in [predefined_path, random_path]:
        if not path.exists():
            continue
        df = pd.read_csv(path, sep="\t")
        df = df.dropna(subset=["realization", "avg.extra"])

        for _, row in df.iterrows():
            e_val = _safe_float(row["avg.extra"])
            if e_val is None:
                continue

            ems_val = _safe_float(row.get("avg.ems"))
            o_val = _safe_float(row.get("avg.open"))
            c_val = _safe_float(row.get("avg.consc"))
            a_val = _safe_float(row.get("avg.agree"))

            has_full = all(v is not None for v in [o_val, c_val, a_val, ems_val])
            if full_ocean_only and not has_full:
                continue

            gt = {"E": scale_1_7_to_minus1_1(e_val)}
            if o_val is not None:
                gt["O"] = scale_1_7_to_minus1_1(o_val)
            if c_val is not None:
                gt["C"] = scale_1_7_to_minus1_1(c_val)
            if a_val is not None:
                gt["A"] = scale_1_7_to_minus1_1(a_val)
            if ems_val is not None:
                gt["N"] = ems_to_neuroticism(ems_val)

            records.append({
                "id": row.get("id", ""),
                "input": str(row["realization"]).strip(),
                "ground_truth_ocean": gt,
                "has_full_ocean": has_full,
            })
            if limit and len(records) >= limit:
                break
        if limit and len(records) >= limit:
            break

    out_path = output_dir / "personage_eval.jsonl"
    with open(out_path, "w") as f:
        for r in records:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")

    n_full = sum(1 for r in records if r["has_full_ocean"])
    print(f"Saved {len(records)} rows to {out_path} ({n_full} full OCEAN, {len(records)-n_full} E-only)")
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
