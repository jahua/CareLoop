#!/usr/bin/env python3
"""Compute PANDORA metrics from eval results JSONL."""

import argparse
import json
from pathlib import Path

import pandas as pd

EVAL_DIR = Path(__file__).resolve().parent.parent
PROCESSED = EVAL_DIR / "pandora" / "processed"
TRAITS = ["O", "C", "E", "A", "N"]


def clamp(v: float, lo: float = -1.0, hi: float = 1.0) -> float:
    return max(lo, min(hi, v))


def load_calibration(path: Path | None) -> dict | None:
    if not path:
        return None
    with open(path, encoding="utf-8") as f:
        data = json.load(f)
    traits = data.get("traits") or {}
    return traits


def apply_calibration(pred: dict, cal: dict | None) -> dict:
    if not cal:
        return dict(pred)
    out = {}
    for t in TRAITS:
        x = float(pred.get(t, 0.0))
        cfg = cal.get(t)
        if cfg and "a" in cfg and "b" in cfg:
            a = float(cfg["a"])
            b = float(cfg["b"])
            out[t] = clamp(a * x + b)
        else:
            out[t] = x
    return out


def load_rows(path: Path):
    rows = []
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            r = json.loads(line)
            pred = r.get("detected_ocean") or r.get("predicted_ocean")
            if pred and r.get("ground_truth_ocean"):
                r = dict(r)
                r["detected_ocean"] = pred
                rows.append(r)
    return rows


def spearman(a: pd.Series, b: pd.Series) -> float:
    return a.rank().corr(b.rank(), method="pearson")


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--input", required=True)
    p.add_argument("--json-out", default=None)
    p.add_argument("--csv-out", default=None)
    p.add_argument(
        "--calibration",
        default=None,
        help="Optional JSON from train_pandora_calibration.py (applies linear map per trait before metrics)",
    )
    args = p.parse_args()

    in_path = Path(args.input)
    rows = load_rows(in_path)
    if not rows:
        raise SystemExit("No valid rows with both ground_truth_ocean and detected_ocean/predicted_ocean")

    cal = load_calibration(Path(args.calibration)) if args.calibration else None

    recs = []
    for r in rows:
        rec = {"sample_id": r.get("sample_id")}
        raw_pred = r["detected_ocean"] or {}
        adj = apply_calibration(raw_pred, cal)
        for t in TRAITS:
            rec[f"gt_{t}"] = float((r["ground_truth_ocean"] or {}).get(t, 0.0))
            rec[f"pred_{t}"] = float(adj.get(t, 0.0))
        recs.append(rec)

    df = pd.DataFrame(recs)
    metrics = {"n": len(df), "calibration_applied": bool(cal), "traits": {}}
    summary_rows = []

    for t in TRAITS:
        gt = df[f"gt_{t}"]
        pred = df[f"pred_{t}"]
        pearson = float(gt.corr(pred, method="pearson")) if gt.std() > 0 and pred.std() > 0 else 0.0
        spear = float(spearman(gt, pred)) if gt.std() > 0 and pred.std() > 0 else 0.0
        mae = float((pred - gt).abs().mean())
        metrics["traits"][t] = {"pearson": pearson, "spearman": spear, "mae": mae}
        summary_rows.append({"trait": t, "pearson": pearson, "spearman": spear, "mae": mae, "n": len(df)})

    metrics["macro_avg"] = {
        "pearson": float(pd.Series([metrics["traits"][t]["pearson"] for t in TRAITS]).mean()),
        "spearman": float(pd.Series([metrics["traits"][t]["spearman"] for t in TRAITS]).mean()),
        "mae": float(pd.Series([metrics["traits"][t]["mae"] for t in TRAITS]).mean()),
    }

    json_out = Path(args.json_out) if args.json_out else PROCESSED / (in_path.stem.replace("results", "metrics") + ".json")
    csv_out = Path(args.csv_out) if args.csv_out else PROCESSED / (in_path.stem.replace("results", "metrics") + ".csv")

    with open(json_out, "w", encoding="utf-8") as f:
        json.dump(metrics, f, ensure_ascii=False, indent=2)

    pd.DataFrame(summary_rows).to_csv(csv_out, index=False)
    print(f"Saved: {json_out}")
    print(f"Saved: {csv_out}")
    print(json.dumps(metrics["macro_avg"], indent=2))


if __name__ == "__main__":
    main()
