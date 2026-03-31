#!/usr/bin/env python3
"""
Optional post-hoc linear calibration for PERSONAGE results.

Trains per-trait affine calibration (gt ≈ a*pred + b) on dev,
applies to test, reports raw vs calibrated Pearson r + MAE.

Usage:
    python calibration.py --train results/harness_X.jsonl --apply results/benchmark_Y.jsonl
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np
from scipy import stats

TRAITS = ["O", "C", "E", "A", "N"]


def load_results(path: Path) -> list[dict]:
    rows = []
    with open(path, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                rows.append(json.loads(line))
    return rows


def extract_paired(rows: list[dict]) -> dict[str, tuple[np.ndarray, np.ndarray]]:
    data = {t: ([], []) for t in TRAITS}
    for row in rows:
        gt = row.get("ground_truth_ocean")
        det = row.get("detected_ocean")
        if not gt or not det:
            continue
        for t in TRAITS:
            if t in gt and t in det:
                data[t][0].append(float(det[t]))
                data[t][1].append(float(gt[t]))
    return {t: (np.array(p), np.array(g)) for t, (p, g) in data.items()}


def train_calibration(paired: dict) -> dict[str, tuple[float, float]]:
    cal = {}
    for t in TRAITS:
        pred, gt = paired[t]
        if len(pred) < 5 or np.std(pred) < 1e-6:
            cal[t] = (1.0, 0.0)
            continue
        slope, intercept, _, _, _ = stats.linregress(pred, gt)
        cal[t] = (float(slope), float(intercept))
    return cal


def apply_calibration(pred: float, a: float, b: float) -> float:
    return max(-1.0, min(1.0, a * pred + b))


def metrics(pred: np.ndarray, gt: np.ndarray) -> tuple[float, float]:
    if len(pred) < 3 or np.std(pred) < 1e-8:
        return 0.0, float(np.mean(np.abs(pred - gt)))
    r, _ = stats.pearsonr(pred, gt)
    mae = float(np.mean(np.abs(pred - gt)))
    return float(r), mae


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--train", required=True, help="JSONL for calibration training")
    parser.add_argument("--apply", default=None, help="JSONL to apply calibration to (optional)")
    args = parser.parse_args()

    train_rows = load_results(Path(args.train))
    train_paired = extract_paired(train_rows)
    cal = train_calibration(train_paired)

    print("Calibration coefficients (a, b):")
    for t in TRAITS:
        print(f"  {t}: a={cal[t][0]:.4f}  b={cal[t][1]:.4f}")

    print("\n--- Train set metrics ---")
    print(f"{'Trait':<6} {'Raw r':>8} {'Raw MAE':>8} {'Cal r':>8} {'Cal MAE':>8}")
    for t in TRAITS:
        pred, gt = train_paired[t]
        r_raw, mae_raw = metrics(pred, gt)
        cal_pred = np.array([apply_calibration(p, *cal[t]) for p in pred])
        r_cal, mae_cal = metrics(cal_pred, gt)
        print(f"  {t:<4} {r_raw:>8.3f} {mae_raw:>8.3f} {r_cal:>8.3f} {mae_cal:>8.3f}")

    raw_rs = [metrics(train_paired[t][0], train_paired[t][1])[0] for t in TRAITS]
    cal_rs = [
        metrics(
            np.array([apply_calibration(p, *cal[t]) for p in train_paired[t][0]]),
            train_paired[t][1],
        )[0]
        for t in TRAITS
    ]
    print(f"\n  Macro r: raw={np.mean(raw_rs):.3f}  cal={np.mean(cal_rs):.3f}")

    if args.apply:
        apply_rows = load_results(Path(args.apply))
        apply_paired = extract_paired(apply_rows)
        print(f"\n--- Apply set metrics ({args.apply}) ---")
        print(f"{'Trait':<6} {'Raw r':>8} {'Raw MAE':>8} {'Cal r':>8} {'Cal MAE':>8}")
        for t in TRAITS:
            pred, gt = apply_paired[t]
            r_raw, mae_raw = metrics(pred, gt)
            cal_pred = np.array([apply_calibration(p, *cal[t]) for p in pred])
            r_cal, mae_cal = metrics(cal_pred, gt)
            print(f"  {t:<4} {r_raw:>8.3f} {mae_raw:>8.3f} {r_cal:>8.3f} {mae_cal:>8.3f}")


if __name__ == "__main__":
    main()
