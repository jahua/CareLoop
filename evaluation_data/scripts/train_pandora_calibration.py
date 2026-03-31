#!/usr/bin/env python3
"""
Fit per-trait linear calibration for PANDORA OCEAN: gt ≈ a * pred + b.

Use a held-out fraction so reported metrics are not optimistically biased.
Saves JSON consumed by pandora_metrics.py --calibration.

Example:
  python scripts/train_pandora_calibration.py \\
    --input pandora/processed/pandora_eval_results_sample100.jsonl \\
    --output pandora/processed/pandora_ocean_calibration.json \\
    --holdout 0.25
"""

import argparse
import json
import random
from pathlib import Path
from typing import Dict, List, Tuple

TRAITS = ["O", "C", "E", "A", "N"]
EPS = 1e-8


def load_rows(path: Path) -> List[dict]:
    rows = []
    with open(path, encoding="utf-8") as f:
        for line in f:
            if not line.strip():
                continue
            r = json.loads(line)
            pred = r.get("detected_ocean") or r.get("predicted_ocean")
            if pred and r.get("ground_truth_ocean"):
                r = dict(r)
                r["detected_ocean"] = pred
                rows.append(r)
    return rows


def fit_linear(x: List[float], y: List[float]) -> Tuple[float, float]:
    n = len(x)
    if n < 3:
        return 1.0, 0.0
    mx = sum(x) / n
    my = sum(y) / n
    vx = sum((xi - mx) ** 2 for xi in x) / n
    if vx < EPS:
        return 1.0, float(my - mx)
    cov = sum((xi - mx) * (yi - my) for xi, yi in zip(x, y)) / n
    a = cov / vx
    b = my - a * mx
    return float(a), float(b)


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--input", required=True, help="Eval JSONL with detected_ocean + ground_truth_ocean")
    p.add_argument("--output", required=True, help="Calibration JSON path")
    p.add_argument("--holdout", type=float, default=0.25, help="Fraction held out for reporting (0=all fit)")
    p.add_argument("--seed", type=int, default=42)
    args = p.parse_args()

    in_path = Path(args.input)
    rows = load_rows(in_path)
    if len(rows) < 5:
        raise SystemExit(f"Need at least 5 labeled rows, got {len(rows)}")

    rng = random.Random(args.seed)
    idx = list(range(len(rows)))
    rng.shuffle(idx)
    h = max(1, int(len(rows) * args.holdout)) if args.holdout > 0 else 0
    train_idx = set(idx[h:]) if h else set(idx)
    test_idx = set(idx[:h]) if h else set()

    coef: Dict = {
        "traits": {},
        "meta": {
            "source": str(in_path),
            "n_total": len(rows),
            "n_train": len(train_idx),
            "n_holdout": len(test_idx),
            "seed": args.seed,
        },
    }

    for t in TRAITS:
        x_tr = [float((rows[i]["detected_ocean"] or {}).get(t, 0.0)) for i in train_idx]
        y_tr = [float((rows[i]["ground_truth_ocean"] or {}).get(t, 0.0)) for i in train_idx]
        a, b = fit_linear(x_tr, y_tr)
        coef["traits"][t] = {"a": a, "b": b}

    out = Path(args.output)
    out.parent.mkdir(parents=True, exist_ok=True)
    with open(out, "w", encoding="utf-8") as f:
        json.dump(coef, f, indent=2, ensure_ascii=False)
    print(f"Saved: {out}")
    print(json.dumps(coef["traits"], indent=2))

    if test_idx:
        import pandas as pd

        def clip(v: float, lo: float = -1.0, hi: float = 1.0) -> float:
            return max(lo, min(hi, v))

        pears = []
        for t in TRAITS:
            cfg = coef["traits"][t]
            a, b = cfg["a"], cfg["b"]
            xs = [float((rows[i]["detected_ocean"] or {}).get(t, 0.0)) for i in test_idx]
            ys = [float((rows[i]["ground_truth_ocean"] or {}).get(t, 0.0)) for i in test_idx]
            adj = [clip(a * x + b) for x in xs]
            gts = pd.Series(ys)
            prs = pd.Series(adj)
            r = float(gts.corr(prs, method="pearson")) if gts.std() > 0 and prs.std() > 0 else 0.0
            pears.append(r)
        print("\nHoldout Pearson (after calibration, honest):")
        print("  per-trait:", dict(zip(TRAITS, [round(x, 4) for x in pears])))
        print("  macro avg:", round(sum(pears) / len(pears), 4))


if __name__ == "__main__":
    main()
