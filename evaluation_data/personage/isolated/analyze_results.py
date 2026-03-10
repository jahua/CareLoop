#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import math
from pathlib import Path


TRAITS = ["O", "C", "E", "A", "N"]


def load_jsonl(path: Path) -> list[dict]:
    rows: list[dict] = []
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                rows.append(json.loads(line))
    return rows


def corr(xs: list[float], ys: list[float]) -> float:
    n = len(xs)
    mx = sum(xs) / n
    my = sum(ys) / n
    vx = sum((x - mx) ** 2 for x in xs)
    vy = sum((y - my) ** 2 for y in ys)
    if vx <= 1e-12 or vy <= 1e-12:
        return float("nan")
    cov = sum((x - mx) * (y - my) for x, y in zip(xs, ys))
    return cov / math.sqrt(vx * vy)


def main() -> None:
    parser = argparse.ArgumentParser(description="Analyze isolated PERSONAGE benchmark results")
    parser.add_argument("input", help="Path to results jsonl")
    args = parser.parse_args()

    rows = [
        row for row in load_jsonl(Path(args.input))
        if row.get("ground_truth_ocean") and row.get("detected_ocean")
    ]
    if not rows:
        raise SystemExit("No valid rows with both ground truth and detected_ocean.")

    mean_r = 0.0
    print("trait\tr\tmae")
    for trait in TRAITS:
        gt = [float(row["ground_truth_ocean"][trait]) for row in rows]
        det = [float(row["detected_ocean"][trait]) for row in rows]
        r = corr(gt, det)
        mae = sum(abs(a - b) for a, b in zip(gt, det)) / len(gt)
        mean_r += r
        print(f"{trait}\t{r:.3f}\t{mae:.3f}")
    print(f"mean_r\t{mean_r / len(TRAITS):.3f}")


if __name__ == "__main__":
    main()
