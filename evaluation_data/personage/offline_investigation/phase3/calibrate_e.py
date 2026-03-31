#!/usr/bin/env python3
"""
Post-hoc Extraversion calibration.

Fits a linear correction on dev predictions to reduce E positive bias,
then applies it to test predictions.

Usage:
    python calibrate_e.py --dev-results results/phase3_v2_dev_*.jsonl \
                          --test-results results/phase3_v2_test_*.jsonl
"""
from __future__ import annotations

import argparse
import json
import numpy as np
from pathlib import Path
from scipy import stats


def load_predictions(path: Path) -> list[dict]:
    rows = []
    for line in open(path):
        r = json.loads(line.strip())
        if r.get("detected_ocean") and "E" in r.get("ground_truth_ocean", {}):
            rows.append(r)
    return rows


def fit_calibration(rows):
    """Fit linear calibration: calibrated_E = a * predicted_E + b"""
    pred = np.array([r["detected_ocean"]["E"] for r in rows])
    gt = np.array([r["ground_truth_ocean"]["E"] for r in rows])

    slope, intercept, r_before, _, _ = stats.linregress(pred, gt)
    calibrated = slope * pred + intercept
    r_after, _ = stats.pearsonr(calibrated, gt)
    mae_before = np.mean(np.abs(pred - gt))
    mae_after = np.mean(np.abs(calibrated - gt))
    bias_before = np.mean(pred - gt)
    bias_after = np.mean(calibrated - gt)

    print(f"Calibration fit (n={len(rows)}):")
    print(f"  calibrated_E = {slope:.4f} * predicted_E + ({intercept:+.4f})")
    print(f"  Before: r={r_before:.3f}  MAE={mae_before:.3f}  bias={bias_before:+.3f}")
    print(f"  After:  r={r_after:.3f}  MAE={mae_after:.3f}  bias={bias_after:+.3f}")

    return slope, intercept


def apply_calibration(rows, slope, intercept):
    """Apply calibration and report metrics."""
    pred_raw = np.array([r["detected_ocean"]["E"] for r in rows])
    gt = np.array([r["ground_truth_ocean"]["E"] for r in rows])
    calibrated = np.clip(slope * pred_raw + intercept, -1, 1)

    r_before, _ = stats.pearsonr(pred_raw, gt)
    r_after, _ = stats.pearsonr(calibrated, gt)
    mae_before = np.mean(np.abs(pred_raw - gt))
    mae_after = np.mean(np.abs(calibrated - gt))
    bias_before = np.mean(pred_raw - gt)
    bias_after = np.mean(calibrated - gt)

    print(f"\nTest set results (n={len(rows)}):")
    print(f"  Before calibration: r={r_before:.3f}  MAE={mae_before:.3f}  bias={bias_before:+.3f}")
    print(f"  After calibration:  r={r_after:.3f}  MAE={mae_after:.3f}  bias={bias_after:+.3f}")

    return calibrated


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--dev-results", required=True)
    parser.add_argument("--test-results", default=None)
    args = parser.parse_args()

    dev_rows = load_predictions(Path(args.dev_results))
    slope, intercept = fit_calibration(dev_rows)

    if args.test_results:
        test_rows = load_predictions(Path(args.test_results))
        apply_calibration(test_rows, slope, intercept)


if __name__ == "__main__":
    main()
