#!/usr/bin/env python3
"""
Visualize PERSONAGE evaluation: detected OCEAN vs ground truth OCEAN (all 5 traits).

Full OCEAN comparison -- best for evaluation.
Output: personage/processed/*.png, personage_summary.csv
"""
import argparse
import json
import random
from pathlib import Path
from typing import List

import pandas as pd

EVAL_DIR = Path(__file__).resolve().parent.parent
PERSONAGE_PROCESSED = EVAL_DIR / "personage" / "processed"
OCEAN_ORDER = ["O", "C", "E", "A", "N"]
OCEAN_LABELS = {"O": "Openness", "C": "Conscientiousness", "E": "Extraversion", "A": "Agreeableness", "N": "Neuroticism"}


def load_results(path: Path) -> List[dict]:
    rows = []
    with open(path) as f:
        for line in f:
            r = json.loads(line)
            if r.get("detected_ocean") and r.get("ground_truth_ocean"):
                rows.append(r)
    return rows


def plot_full_ocean(rows: List[dict], out_dir: Path) -> None:
    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
        import numpy as np
    except ImportError as e:
        print(f"Install matplotlib, numpy: pip install matplotlib numpy. {e}")
        return

    out_dir.mkdir(parents=True, exist_ok=True)

    # Build arrays: detected vs ground truth per trait
    data = {k: {"det": [], "gt": []} for k in OCEAN_ORDER}
    for r in rows:
        det = r.get("detected_ocean") or {}
        gt = r.get("ground_truth_ocean") or {}
        for k in OCEAN_ORDER:
            d = float(det.get(k, 0))
            g = float(gt.get(k, 0))
            data[k]["det"].append(d)
            data[k]["gt"].append(g)

    # 1. Scatter: detected vs ground truth per trait (2x3 grid)
    fig, axes = plt.subplots(2, 3, figsize=(12, 8))
    axes = axes.flatten()
    for idx, k in enumerate(OCEAN_ORDER):
        ax = axes[idx]
        det = np.array(data[k]["det"])
        gt = np.array(data[k]["gt"])
        ax.scatter(gt, det, alpha=0.6, s=30, c="steelblue")
        ax.plot([-1, 1], [-1, 1], "r--", alpha=0.5, label="y=x")
        r = np.corrcoef(gt, det)[0, 1] if len(gt) >= 2 and np.std(gt) > 1e-6 and np.std(det) > 1e-6 else np.nan
        ax.set_title(f"{OCEAN_LABELS[k]}\nr = {r:.3f}" if not np.isnan(r) else OCEAN_LABELS[k])
        ax.set_xlabel("Ground truth")
        ax.set_ylabel("Detected")
        ax.set_xlim(-1.1, 1.1)
        ax.set_ylim(-1.1, 1.1)
    axes[-1].axis("off")
    plt.suptitle("PERSONAGE: Detected vs Ground Truth OCEAN (full 5 traits)")
    plt.tight_layout()
    plt.savefig(out_dir / "personage_detected_vs_ground_truth.png", dpi=150)
    plt.close()
    print(f"Saved: {out_dir / 'personage_detected_vs_ground_truth.png'}")

    # 2. Correlation matrix (per-trait Pearson r)
    correlations = []
    for k in OCEAN_ORDER:
        det = np.array(data[k]["det"])
        gt = np.array(data[k]["gt"])
        r = np.corrcoef(gt, det)[0, 1] if len(gt) >= 2 and np.std(gt) > 1e-6 and np.std(det) > 1e-6 else np.nan
        mae = np.mean(np.abs(det - gt)) if len(det) > 0 else np.nan
        correlations.append({"trait": OCEAN_LABELS[k], "Pearson r": r, "MAE": mae})

    fig, ax = plt.subplots(figsize=(8, 4))
    ax.axis("off")
    df_metrics = pd.DataFrame(correlations)
    tbl = ax.table(
        cellText=df_metrics.values.tolist(),
        colLabels=df_metrics.columns.tolist(),
        loc="center",
        cellLoc="center",
    )
    tbl.auto_set_font_size(False)
    tbl.set_fontsize(10)
    tbl.scale(1.2, 2)
    ax.set_title("PERSONAGE: Correlation & MAE per OCEAN trait")
    plt.tight_layout()
    plt.savefig(out_dir / "personage_metrics.png", dpi=150)
    plt.close()
    print(f"Saved: {out_dir / 'personage_metrics.png'}")

    # 3. Export summary CSV
    records = []
    for r in rows:
        rec = {"id": r.get("id", ""), "input_len": len(r.get("input", ""))}
        for k in OCEAN_ORDER:
            rec[f"gt_{k}"] = r.get("ground_truth_ocean", {}).get(k)
            rec[f"det_{k}"] = r.get("detected_ocean", {}).get(k)
        records.append(rec)
    csv_path = out_dir / "personage_summary.csv"
    pd.DataFrame(records).to_csv(csv_path, index=False)
    print(f"Saved: {csv_path}")


def load_demo(input_path: Path) -> List[dict]:
    """Generate synthetic detected OCEAN from ground truth (for demo when Big5Loop not running)."""
    rows = []
    with open(input_path) as f:
        for line in f:
            r = json.loads(line)
            gt = r.get("ground_truth_ocean") or {}
            if not gt:
                continue
            det = {k: round(gt.get(k, 0.5) + random.gauss(0, 0.15), 3) for k in OCEAN_ORDER}
            det = {k: max(-1, min(1, v)) for k, v in det.items()}
            rows.append({**r, "detected_ocean": det})
    return rows


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--input", default=str(PERSONAGE_PROCESSED / "personage_eval_results.jsonl"))
    p.add_argument("--demo", action="store_true", help="Use synthetic detected OCEAN from personage_eval.jsonl")
    p.add_argument("-o", "--output-dir", default=str(PERSONAGE_PROCESSED))
    args = p.parse_args()

    if args.demo:
        path = PERSONAGE_PROCESSED / "personage_eval.jsonl"
        if not path.exists():
            raise SystemExit(f"Missing: {path}. Run preprocess_personage.py first.")
        print("Using demo (synthetic) detected OCEAN...")
        rows = load_demo(path)
    else:
        path = Path(args.input)
        if not path.exists():
            raise SystemExit(f"Missing: {path}. Run run_personage_eval.py first.")
        rows = load_results(path)
    if not rows:
        raise SystemExit("No rows with detected_ocean and ground_truth_ocean.")

    print(f"Loaded {len(rows)} samples with full OCEAN")
    plot_full_ocean(rows, Path(args.output_dir))


if __name__ == "__main__":
    main()
