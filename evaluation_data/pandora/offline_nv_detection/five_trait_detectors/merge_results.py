#!/usr/bin/env python3
"""Merge five-trait detector JSONL runs by sample_id and compute correlation / MAE metrics."""

from __future__ import annotations

import argparse
import json
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

TRAITS = ["O", "C", "E", "A", "N"]


def record_priority(rec: dict[str, Any]) -> tuple[int, int, str]:
    """Higher tuple sorts last (we keep best). Prefer live API, then trait success count, then timestamp."""
    method = str(rec.get("method") or "")
    tier = 0 if "dry_run" in method else 1
    ad = rec.get("agent_details") or {}
    n_ok = sum(1 for t in TRAITS if isinstance(ad.get(t), dict) and ad[t].get("success"))
    ts = str(rec.get("timestamp") or "")
    return (tier, n_ok, ts)


def pearson(xs: list[float], ys: list[float]) -> float:
    n = len(xs)
    if n < 2:
        return 0.0
    mx, my = sum(xs) / n, sum(ys) / n
    num = sum((xs[i] - mx) * (ys[i] - my) for i in range(n))
    dx = sum((x - mx) ** 2 for x in xs)
    dy = sum((y - my) ** 2 for y in ys)
    if dx <= 0 or dy <= 0:
        return 0.0
    return num / (dx**0.5 * dy**0.5)


def mae(xs: list[float], ys: list[float]) -> float:
    if not xs:
        return 0.0
    return sum(abs(xs[i] - ys[i]) for i in range(len(xs))) / len(xs)


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument(
        "--inputs",
        nargs="*",
        default=None,
        help="JSONL files to merge (default: all five_trait_ocean_*.jsonl in results/)",
    )
    ap.add_argument(
        "--out-dir",
        type=Path,
        default=None,
        help="Output directory (default: same as first input's parent)",
    )
    args = ap.parse_args()

    root = Path(__file__).resolve().parent
    results_dir = root / "results"
    if args.inputs:
        paths = [Path(p) for p in args.inputs]
    else:
        paths = sorted(results_dir.glob("five_trait_ocean_*.jsonl"))

    if not paths:
        raise SystemExit("No input files found.")

    out_dir = args.out_dir or paths[0].parent
    out_dir.mkdir(parents=True, exist_ok=True)

    by_id: dict[str, dict[str, Any]] = {}
    provenance: dict[str, list[str]] = defaultdict(list)

    for path in paths:
        if not path.is_file():
            continue
        with open(path, encoding="utf-8") as f:
            for line_no, line in enumerate(f, 1):
                line = line.strip()
                if not line:
                    continue
                try:
                    rec = json.loads(line)
                except json.JSONDecodeError:
                    continue
                sid = str(rec.get("sample_id") or "")
                if not sid:
                    continue
                provenance[sid].append(f"{path.name}:{line_no}")
                cur = by_id.get(sid)
                if cur is None or record_priority(rec) > record_priority(cur):
                    rec["_merge_source_file"] = path.name
                    by_id[sid] = rec

    run_tag = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    merged_path = out_dir / f"merged_five_trait_ocean_{run_tag}.jsonl"
    with open(merged_path, "w", encoding="utf-8") as f:
        for sid in sorted(by_id.keys(), key=lambda x: (len(x), x)):
            f.write(json.dumps(by_id[sid], ensure_ascii=False) + "\n")

    # Metrics: only rows with ground_truth and non-dry-run preferred for "live" subset
    def eval_rows(*, live_only: bool) -> list[dict[str, Any]]:
        rows = []
        for rec in by_id.values():
            if live_only and "dry_run" in str(rec.get("method") or ""):
                continue
            gt = rec.get("ground_truth_ocean")
            pr = rec.get("predicted_ocean")
            if not isinstance(gt, dict) or not isinstance(pr, dict):
                continue
            rows.append(rec)
        return rows

    def metrics_for(rows: list[dict[str, Any]]) -> dict[str, Any]:
        per_trait: dict[str, dict[str, float]] = {}
        macro_r: list[float] = []
        macro_m: list[float] = []
        for t in TRAITS:
            xs: list[float] = []
            ys: list[float] = []
            for r in rows:
                gt = r.get("ground_truth_ocean") or {}
                pr = r.get("predicted_ocean") or {}
                if t not in gt or t not in pr:
                    continue
                xs.append(float(gt[t]))
                ys.append(float(pr[t]))
            r_val = pearson(xs, ys) if len(xs) >= 2 else 0.0
            m_val = mae(xs, ys) if xs else 0.0
            per_trait[t] = {"n": len(xs), "pearson": r_val, "mae": m_val}
            if len(xs) >= 2:
                macro_r.append(r_val)
                macro_m.append(m_val)
        return {
            "n_samples": len(rows),
            "macro_pearson": sum(macro_r) / len(macro_r) if macro_r else 0.0,
            "macro_mae": sum(macro_m) / len(macro_m) if macro_m else 0.0,
            "per_trait": per_trait,
        }

    all_rows = eval_rows(live_only=False)
    live_rows = eval_rows(live_only=True)

    n_dup = sum(1 for sid, srcs in provenance.items() if len(srcs) > 1)
    analysis = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "input_files": [str(p.name) for p in paths],
        "unique_sample_ids": len(by_id),
        "sample_ids_with_duplicate_inputs": n_dup,
        "merged_path": str(merged_path),
        "all_merged_including_dry_run": metrics_for(all_rows),
        "live_api_only": metrics_for(live_rows),
        "success_counts": {
            "full_success": sum(1 for r in by_id.values() if r.get("success")),
            "any_trait_fail": sum(
                1
                for r in by_id.values()
                if not r.get("success")
                or any(
                    not (r.get("agent_details") or {}).get(t, {}).get("success", True)
                    for t in TRAITS
                )
            ),
        },
        "method_breakdown": {},
    }
    methods: dict[str, int] = defaultdict(int)
    for r in by_id.values():
        methods[str(r.get("method") or "?")] += 1
    analysis["method_breakdown"] = dict(sorted(methods.items(), key=lambda x: -x[1]))

    analysis_path = out_dir / f"merged_five_trait_analysis_{run_tag}.json"
    with open(analysis_path, "w", encoding="utf-8") as f:
        json.dump(analysis, f, indent=2, ensure_ascii=False)

    csv_path = out_dir / f"merged_five_trait_metrics_{run_tag}.csv"
    with open(csv_path, "w", encoding="utf-8") as f:
        f.write("subset,trait,n,pearson,mae\n")
        for subset_name, rows in [("all", all_rows), ("live_only", live_rows)]:
            m = metrics_for(rows)
            for t in TRAITS:
                pt = m["per_trait"][t]
                f.write(
                    f"{subset_name},{t},{int(pt['n'])},{pt['pearson']:.6f},{pt['mae']:.6f}\n"
                )
            f.write(
                f"{subset_name},MACRO,{m['n_samples']},{m['macro_pearson']:.6f},{m['macro_mae']:.6f}\n"
            )

    print(f"Merged {len(by_id)} unique samples -> {merged_path}")
    print(f"Analysis -> {analysis_path}")
    print(f"CSV -> {csv_path}")
    print(json.dumps(analysis, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
