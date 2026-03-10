#!/usr/bin/env python3
"""
Visualize agreement between Big5Loop detected OCEAN traits and BIG5-CHAT annotations.

Reads from: eval_results.jsonl (from run_big5_eval.py) OR database (personality_states + eval_session_metadata)
Output: processed/agreement_*.png, detected_vs_ground_truth_*.png, eval_summary.csv
"""
import argparse
import json
import os
from pathlib import Path
from typing import List, Optional

EVAL_DIR = Path(__file__).resolve().parent.parent
PROCESSED_DIR = EVAL_DIR / "processed"

TRAIT_TO_OCEAN = {"openness": "O", "conscientiousness": "C", "extraversion": "E", "agreeableness": "A", "neuroticism": "N"}
OCEAN_LABELS = {"O": "Openness", "C": "Conscientiousness", "E": "Extraversion", "A": "Agreeableness", "N": "Neuroticism"}
OCEAN_ORDER = ["O", "C", "E", "A", "N"]


def load_from_file(path: Path) -> List[dict]:
    rows = []
    with open(path) as f:
        for line in f:
            r = json.loads(line)
            if r.get("detected_ocean"):
                rows.append(r)
    return rows


def load_from_db() -> List[dict]:
    try:
        import psycopg2
        import json as _json
    except ImportError:
        return []

    url = os.environ.get("DATABASE_URL") or os.environ.get("AUDIT_DATABASE_URL") or ""
    if not url:
        return []

    conn = psycopg2.connect(url)
    cur = conn.cursor()
    cur.execute("""
        SELECT ps.session_id, ps.turn_index, ps.ocean_json,
               esm.ground_truth, t.user_msg, t.assistant_msg
        FROM personality_states ps
        JOIN eval_session_metadata esm ON esm.session_id = ps.session_id
        JOIN conversation_turns t ON t.session_id = ps.session_id AND t.turn_index = ps.turn_index
    """)
    rows = []
    for r in cur.fetchall():
        session_id, turn_index, ocean_json, ground_truth, user_msg, assistant_msg = r
        gt = ground_truth if isinstance(ground_truth, dict) else _json.loads(ground_truth or "{}")
        ocean = ocean_json if isinstance(ocean_json, dict) else _json.loads(ocean_json or "{}")
        rows.append({
            "session_id": str(session_id),
            "input": user_msg,
            "expected_output": gt.get("expected_output"),
            "trait": gt.get("trait"),
            "level": gt.get("level"),
            "ground_truth": gt.get("ground_truth"),
            "detected_ocean": ocean,
            "response": assistant_msg,
        })
    cur.close()
    conn.close()
    return rows


def compute_agreement(rows: List[dict]) -> dict:
    """For each sample: ground truth trait+level vs detected OCEAN. Agreement = sign matches."""
    trait_stats = {t: {"agree": 0, "disagree": 0, "detected": [], "expected": []} for t in TRAIT_TO_OCEAN}

    for r in rows:
        trait = r.get("trait")
        level = r.get("level")
        ocean = r.get("detected_ocean") or {}
        if not trait or not level or trait not in TRAIT_TO_OCEAN:
            continue

        key = TRAIT_TO_OCEAN[trait]
        detected = float(ocean.get(key, 0))
        expected_sign = 1 if level == "high" else -1
        detected_sign = 1 if detected > 0 else (-1 if detected < 0 else 0)

        trait_stats[trait]["detected"].append(detected)
        trait_stats[trait]["expected"].append(expected_sign)

        if detected_sign == expected_sign:
            trait_stats[trait]["agree"] += 1
        elif detected_sign != 0:
            trait_stats[trait]["disagree"] += 1

    return trait_stats


def build_analysis_data(rows: List[dict]) -> "pd.DataFrame":
    """Build DataFrame: detected OCEAN + ground truth encoded for each sample."""
    import pandas as pd

    records = []
    for r in rows:
        trait = r.get("trait")
        level = r.get("level")
        ocean = r.get("detected_ocean") or {}
        if not trait or not level or trait not in TRAIT_TO_OCEAN:
            continue

        rec = {
            "sample_idx": len(records),
            "trait": trait,
            "level": level,
            "ground_truth": r.get("ground_truth", ""),
            "expected_sign": 1 if level == "high" else -1,
        }
        for k in OCEAN_ORDER:
            rec[f"detected_{k}"] = float(ocean.get(k, 0))
        key = TRAIT_TO_OCEAN[trait]
        rec["detected_target"] = float(ocean.get(key, 0))
        rec["agreement"] = (1 if rec["detected_target"] > 0 else (-1 if rec["detected_target"] < 0 else 0)) == rec["expected_sign"]
        records.append(rec)

    return pd.DataFrame(records)


def plot_detected_vs_ground_truth(rows: List[dict], out_dir: Path) -> None:
    """Data-scientist visualizations: scatter, heatmap, distributions, metrics."""
    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
        import numpy as np
        import pandas as pd
    except ImportError as e:
        print(f"Install dependencies: pip install matplotlib pandas. {e}")
        return

    df = build_analysis_data(rows)
    if df.empty:
        print("No data for detected vs ground truth plots.")
        return

    out_dir.mkdir(parents=True, exist_ok=True)

    # 1. Scatter: Detected vs Ground Truth (target trait only), with regression line and correlation
    traits_with_data = df["trait"].unique().tolist()
    n_traits = len(traits_with_data)
    if n_traits == 0:
        return

    fig, axes = plt.subplots(2, 3, figsize=(12, 8))
    axes = axes.flatten()

    for idx, trait in enumerate(traits_with_data):
        ax = axes[idx]
        sub = df[df["trait"] == trait]
        x = sub["expected_sign"].values
        y = sub["detected_target"].values

        ax.scatter(x, y, alpha=0.6, s=40, c="steelblue", edgecolors="white", linewidth=0.5)
        ax.axhline(0, color="gray", linestyle="--", alpha=0.7)
        ax.axvline(0, color="gray", linestyle="--", alpha=0.7)

        if len(x) >= 3 and np.std(x) > 1e-6:
            z = np.polyfit(x, y, 1)
            p = np.poly1d(z)
            x_line = np.linspace(x.min(), x.max(), 50)
            ax.plot(x_line, p(x_line), "r-", linewidth=2, label="Linear fit")
        r = np.corrcoef(x, y)[0, 1] if len(x) >= 2 and np.std(x) > 1e-6 and np.std(y) > 1e-6 else np.nan
        r_str = f"r = {r:.3f}" if not np.isnan(r) else "r = N/A (constant GT)"
        ax.set_title(f"{OCEAN_LABELS[TRAIT_TO_OCEAN[trait]]}\n{r_str}, n = {len(sub)}")
        ax.set_xlabel("Ground truth (high=1, low=-1)")
        ax.set_ylabel("Detected value")
        ax.set_xlim(-1.5, 1.5)

    for j in range(idx + 1, len(axes)):
        axes[j].axis("off")

    plt.suptitle("Detected OCEAN vs Ground Truth (Target Trait)", fontsize=12)
    plt.tight_layout()
    plt.savefig(out_dir / "detected_vs_ground_truth_scatter.png", dpi=150)
    plt.close()
    print(f"Saved: {out_dir / 'detected_vs_ground_truth_scatter.png'}")

    # 2. Heatmap: All OCEAN detected values across samples (top N samples)
    n_show = min(50, len(df))
    df_show = df.head(n_show)
    ocean_cols = [f"detected_{k}" for k in OCEAN_ORDER]
    mat = df_show[ocean_cols].values
    col_labels = [OCEAN_LABELS[k] for k in OCEAN_ORDER]

    fig, ax = plt.subplots(figsize=(8, max(6, n_show * 0.15)))
    im = ax.imshow(mat, aspect="auto", cmap="RdYlGn", vmin=-1, vmax=1)
    ax.set_xticks(range(len(col_labels)))
    ax.set_xticklabels(col_labels)
    ax.set_ylabel("Sample index")
    ax.set_title(f"Detected OCEAN Values (first {n_show} samples)")
    plt.colorbar(im, ax=ax, label="Detected value")
    plt.tight_layout()
    plt.savefig(out_dir / "detected_ocean_heatmap.png", dpi=150)
    plt.close()
    print(f"Saved: {out_dir / 'detected_ocean_heatmap.png'}")

    # 3. Distribution: Detected target trait by ground truth level (box + violin)
    fig, axes = plt.subplots(1, min(n_traits, 5), figsize=(4 * n_traits, 5))
    if n_traits == 1:
        axes = [axes]
    for idx, trait in enumerate(traits_with_data[:5]):
        ax = axes[idx]
        sub = df[df["trait"] == trait]
        levels = sub["level"].unique()
        data_by_level = [sub[sub["level"] == lv]["detected_target"].values for lv in sorted(levels, reverse=True)]
        labels = sorted(levels, reverse=True)
        bp = ax.boxplot(data_by_level, labels=labels, patch_artist=True)
        for patch in bp["boxes"]:
            patch.set_facecolor("lightsteelblue")
        ax.axhline(0, color="gray", linestyle="--", alpha=0.7)
        ax.set_ylabel("Detected value")
        ax.set_xlabel("Ground truth level")
        ax.set_title(OCEAN_LABELS[TRAIT_TO_OCEAN[trait]])
    plt.suptitle("Distribution of Detected Values by Ground Truth Level", fontsize=12)
    plt.tight_layout()
    plt.savefig(out_dir / "detected_distribution_by_ground_truth.png", dpi=150)
    plt.close()
    print(f"Saved: {out_dir / 'detected_distribution_by_ground_truth.png'}")

    # 4. Metrics summary panel
    metrics = []
    for trait in traits_with_data:
        sub = df[df["trait"] == trait]
        x = sub["expected_sign"].values
        y = sub["detected_target"].values
        agree = sub["agreement"].sum()
        total = len(sub)
        pearson = np.corrcoef(x, y)[0, 1] if len(x) >= 2 and np.std(x) > 0 and np.std(y) > 0 else np.nan
        mae = np.mean(np.abs(y - x)) if len(y) > 0 else np.nan
        metrics.append({
            "trait": OCEAN_LABELS[TRAIT_TO_OCEAN[trait]],
            "n": total,
            "agreement_rate": agree / total * 100 if total > 0 else 0,
            "pearson_r": pearson,
            "MAE": mae,
        })

    fig, ax = plt.subplots(figsize=(10, 4))
    ax.axis("off")
    tbl = ax.table(
        cellText=[[m["trait"], m["n"], f"{m['agreement_rate']:.1f}%", f"{m['pearson_r']:.3f}" if not np.isnan(m["pearson_r"]) else "—", f"{m['MAE']:.3f}" if not np.isnan(m["MAE"]) else "—"]
        for m in metrics
        ],
        colLabels=["Trait", "n", "Agreement %", "Pearson r", "MAE"],
        loc="center",
        cellLoc="center",
    )
    tbl.auto_set_font_size(False)
    tbl.set_fontsize(10)
    tbl.scale(1.2, 2)
    ax.set_title("Evaluation Metrics: Detected vs Ground Truth")
    plt.tight_layout()
    plt.savefig(out_dir / "eval_metrics_summary.png", dpi=150)
    plt.close()
    print(f"Saved: {out_dir / 'eval_metrics_summary.png'}")

    # 5. Export CSV: detected vs ground truth per sample
    csv_path = out_dir / "eval_summary.csv"
    df.to_csv(csv_path, index=False)
    print(f"Saved: {csv_path}")


def plot_agreement(trait_stats: dict, out_dir: Path) -> None:
    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
        import numpy as np
    except ImportError:
        print("Install matplotlib: pip install matplotlib")
        return

    out_dir.mkdir(parents=True, exist_ok=True)

    # 1. Agreement rate per trait (bar chart)
    fig, ax = plt.subplots(figsize=(8, 5))
    traits = list(TRAIT_TO_OCEAN.keys())
    agrees = [trait_stats[t]["agree"] for t in traits]
    disagrees = [trait_stats[t]["disagree"] for t in traits]
    totals = [a + d for a, d in zip(agrees, disagrees)]
    rates = [a / t * 100 if t > 0 else 0 for a, t in zip(agrees, totals)]

    x = np.arange(len(traits))
    width = 0.35
    ax.bar(x - width/2, agrees, width, label="Agree", color="steelblue")
    ax.bar(x + width/2, disagrees, width, label="Disagree", color="coral")
    ax.set_xticks(x)
    ax.set_xticklabels([OCEAN_LABELS[TRAIT_TO_OCEAN[t]] for t in traits])
    ax.set_ylabel("Count")
    ax.set_title("Detected vs Annotated Trait Agreement (high=+, low=-)")
    ax.legend()
    for i, (r, t) in enumerate(zip(rates, totals)):
        if t > 0:
            ax.annotate(f"{r:.0f}%", (i, agrees[i] + 0.5), ha="center", fontsize=9)
    plt.tight_layout()
    plt.savefig(out_dir / "agreement_by_trait.png", dpi=150)
    plt.close()
    print(f"Saved: {out_dir / 'agreement_by_trait.png'}")

    # 2. Detected vs expected (scatter, one subplot per trait)
    fig, axes = plt.subplots(2, 3, figsize=(12, 8))
    axes = axes.flatten()
    for idx, trait in enumerate(traits):
        ax = axes[idx]
        stats = trait_stats[trait]
        det = stats["detected"]
        exp = stats["expected"]
        if not det:
            ax.text(0.5, 0.5, "No data", ha="center", va="center")
            ax.set_title(OCEAN_LABELS[TRAIT_TO_OCEAN[trait]])
            continue
        ax.scatter(exp, det, alpha=0.6, s=30)
        ax.axhline(0, color="gray", linestyle="--")
        ax.axvline(0, color="gray", linestyle="--")
        ax.set_xlabel("Annotated (high=1, low=-1)")
        ax.set_ylabel("Detected OCEAN")
        ax.set_title(OCEAN_LABELS[TRAIT_TO_OCEAN[trait]])
    axes[-1].axis("off")
    plt.suptitle("Detected OCEAN vs Dataset Annotation", fontsize=12)
    plt.tight_layout()
    plt.savefig(out_dir / "detected_vs_annotated.png", dpi=150)
    plt.close()
    print(f"Saved: {out_dir / 'detected_vs_annotated.png'}")

    # 3. Overall confusion-style: predicted high/low vs actual
    fig, ax = plt.subplots(figsize=(6, 5))
    all_agree = sum(trait_stats[t]["agree"] for t in traits)
    all_disagree = sum(trait_stats[t]["disagree"] for t in traits)
    total = all_agree + all_disagree
    rate = all_agree / total * 100 if total > 0 else 0
    ax.bar(["Agree", "Disagree"], [all_agree, all_disagree], color=["steelblue", "coral"])
    ax.set_ylabel("Count")
    ax.set_title(f"Overall Agreement: {rate:.1f}% ({all_agree}/{total})")
    plt.tight_layout()
    plt.savefig(out_dir / "agreement_overall.png", dpi=150)
    plt.close()
    print(f"Saved: {out_dir / 'agreement_overall.png'}")


def load_demo(path: Path) -> List[dict]:
    """Generate synthetic detected OCEAN for demo (when no eval run yet)."""
    rows = []
    with open(path) as f:
        for line in f:
            r = json.loads(line)
            trait, level = r.get("trait"), r.get("level")
            if trait not in TRAIT_TO_OCEAN:
                continue
            import random
            base = 0.5 if level == "high" else -0.5
            ocean = {k: round(base + random.gauss(0, 0.3), 2) for k in "OCEAN"}
            ocean[TRAIT_TO_OCEAN[trait]] = round(base + random.gauss(0, 0.2), 2)
            rows.append({**r, "detected_ocean": ocean})
    return rows


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--input", default=str(PROCESSED_DIR / "eval_results.jsonl"))
    p.add_argument("--sessions", default=str(PROCESSED_DIR / "big5_eval_sessions.jsonl"), help="For --demo")
    p.add_argument("--db", action="store_true", help="Load from database instead of file")
    p.add_argument("--demo", action="store_true", help="Use synthetic OCEAN from sessions (no eval run needed)")
    p.add_argument("-o", "--output-dir", default=str(PROCESSED_DIR))
    args = p.parse_args()

    if args.demo:
        path = Path(args.sessions)
        if not path.exists():
            raise SystemExit(f"Missing: {path}. Run create_eval_sessions.py first.")
        print("Using demo (synthetic) detected OCEAN...")
        rows = load_demo(path)
    elif args.db:
        print("Loading from database...")
        rows = load_from_db()
    else:
        path = Path(args.input)
        if not path.exists():
            raise SystemExit(f"Missing: {path}. Run run_big5_eval.py first, or use --db or --demo")
        rows = load_from_file(path)

    if not rows:
        raise SystemExit("No rows with detected OCEAN. Run run_big5_eval.py or ensure DB has data.")

    print(f"Loaded {len(rows)} samples with detected OCEAN")
    trait_stats = compute_agreement(rows)
    out_dir = Path(args.output_dir)
    plot_agreement(trait_stats, out_dir)
    plot_detected_vs_ground_truth(rows, out_dir)


if __name__ == "__main__":
    main()
