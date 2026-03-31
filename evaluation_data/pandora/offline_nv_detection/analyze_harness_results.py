#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Harness Engineering — Results Analysis & Interpretation
========================================================
Loads all harness JSONL results, computes metrics, and produces
publication-ready visualizations + thesis-ready interpretation.

Run:
    python3 analyze_harness_results.py

Or import into Jupyter/IPython:
    %run analyze_harness_results.py
"""

import json
import glob
import warnings
from pathlib import Path
from collections import defaultdict

import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")  # non-interactive backend
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker

warnings.filterwarnings("ignore", category=FutureWarning)

# ── Config ─────────────────────────────────────────────────────────────────────

RESULTS_DIR = Path(__file__).resolve().parent / "results"
TRAITS = ["O", "C", "E", "A", "N"]
TRAIT_LABELS = {
    "O": "Openness",
    "C": "Conscientiousness",
    "E": "Extraversion",
    "A": "Agreeableness",
    "N": "Neuroticism",
}
COLORS = {
    "O": "#FF6B6B",
    "C": "#4ECDC4",
    "E": "#45B7D1",
    "A": "#96CEB4",
    "N": "#FFEAA7",
}
BOOTSTRAP_N = 1000
BOOTSTRAP_SEED = 42

# ── Load Data ──────────────────────────────────────────────────────────────────


def load_all_harness_results() -> pd.DataFrame:
    """Load all harness JSONL files into a single DataFrame."""
    files = sorted(RESULTS_DIR.glob("harness_*.jsonl"))
    if not files:
        raise FileNotFoundError(f"No harness_*.jsonl files in {RESULTS_DIR}")

    rows = []
    for f in files:
        run_id = f.stem.replace("harness_", "")
        with open(f, encoding="utf-8") as fh:
            for line in fh:
                r = json.loads(line)
                r["run_id"] = run_id
                r["file"] = f.name
                rows.append(r)

    df = pd.DataFrame(rows)
    print(f"✓ Loaded {len(df)} evaluations from {len(files)} files")
    print(f"  Models: {df['model'].nunique()} unique")
    print(f"  Prompt sets: {df['prompt_set'].nunique()} unique")
    print(f"  Samples: {df['sample_id'].nunique()} unique")
    return df


def extract_traits(df: pd.DataFrame) -> pd.DataFrame:
    """Expand predicted/ground-truth OCEAN into separate columns."""
    for t in TRAITS:
        df[f"gt_{t}"] = df["ground_truth_ocean"].apply(
            lambda x: float((x or {}).get(t, np.nan))
        )
        df[f"pr_{t}"] = df["predicted_ocean"].apply(
            lambda x: float((x or {}).get(t, np.nan)) if x else np.nan
        )
    df["has_prediction"] = df["predicted_ocean"].apply(lambda x: x is not None)
    return df


# ── Metrics ────────────────────────────────────────────────────────────────────


def compute_group_metrics(group: pd.DataFrame) -> dict:
    """Compute metrics for a group of evaluations."""
    ok = group[group["has_prediction"]]
    n = len(ok)
    total = len(group)

    if n < 3:
        return {
            "n": n, "total": total, "coverage": n / total if total else 0,
            "macro_pearson": np.nan, "macro_spearman": np.nan,
            "macro_mae": np.nan, "macro_bias": np.nan,
            "per_trait": {}, "ci_lo": np.nan, "ci_hi": np.nan,
        }

    trait_metrics = {}
    pears, maes, biases = [], [], []
    for t in TRAITS:
        gt = ok[f"gt_{t}"].values
        pr = ok[f"pr_{t}"].values
        mask = ~(np.isnan(gt) | np.isnan(pr))
        if mask.sum() < 3:
            continue
        gt_clean, pr_clean = gt[mask], pr[mask]
        pearson = np.corrcoef(gt_clean, pr_clean)[0, 1] if np.std(gt_clean) > 0 and np.std(pr_clean) > 0 else 0.0
        mae = np.mean(np.abs(pr_clean - gt_clean))
        bias = np.mean(pr_clean - gt_clean)

        # Spearman
        from scipy.stats import spearmanr
        rho, _ = spearmanr(gt_clean, pr_clean)

        trait_metrics[t] = {
            "pearson": float(pearson), "spearman": float(rho) if not np.isnan(rho) else 0.0,
            "mae": float(mae), "bias": float(bias),
            "gt_mean": float(np.mean(gt_clean)), "gt_std": float(np.std(gt_clean)),
            "pr_mean": float(np.mean(pr_clean)), "pr_std": float(np.std(pr_clean)),
            "n": int(mask.sum()),
        }
        pears.append(float(pearson))
        maes.append(float(mae))
        biases.append(float(bias))

    macro_r = np.mean(pears) if pears else np.nan
    macro_mae = np.mean(maes) if maes else np.nan
    macro_bias = np.mean(biases) if biases else np.nan

    # Bootstrap CI
    ci_lo, ci_hi = bootstrap_ci(ok, BOOTSTRAP_N, BOOTSTRAP_SEED)

    return {
        "n": n, "total": total, "coverage": n / total if total else 0,
        "macro_pearson": macro_r,
        "macro_spearman": np.mean([tm.get("spearman", 0) for tm in trait_metrics.values()]) if trait_metrics else np.nan,
        "macro_mae": macro_mae, "macro_bias": macro_bias,
        "per_trait": trait_metrics,
        "ci_lo": ci_lo, "ci_hi": ci_hi,
    }


def bootstrap_ci(ok: pd.DataFrame, n_boot: int = 1000, seed: int = 42):
    if len(ok) < 5:
        return np.nan, np.nan
    rng = np.random.RandomState(seed)
    boot_rs = []
    for _ in range(n_boot):
        idx = rng.choice(len(ok), size=len(ok), replace=True)
        sample = ok.iloc[idx]
        rs = []
        for t in TRAITS:
            gt = sample[f"gt_{t}"].values
            pr = sample[f"pr_{t}"].values
            mask = ~(np.isnan(gt) | np.isnan(pr))
            if mask.sum() < 3:
                rs.append(0.0)
                continue
            r = np.corrcoef(gt[mask], pr[mask])[0, 1] if np.std(gt[mask]) > 0 and np.std(pr[mask]) > 0 else 0.0
            rs.append(r)
        boot_rs.append(np.mean(rs))
    return float(np.percentile(boot_rs, 2.5)), float(np.percentile(boot_rs, 97.5))


def composite_score(m: dict) -> float:
    r = m["macro_pearson"] if not np.isnan(m.get("macro_pearson", np.nan)) else 0.0
    c = m.get("coverage", 0.0)
    mae = m["macro_mae"] if not np.isnan(m.get("macro_mae", np.nan)) else 1.0
    return 0.5 * r + 0.3 * c + 0.2 * (1.0 - mae)


# ── Visualization ──────────────────────────────────────────────────────────────


def plot_model_comparison(metrics_by_config: dict, save_path: Path):
    """Bar chart comparing models by composite score."""
    model_scores = defaultdict(list)
    for key, m in metrics_by_config.items():
        if m["n"] < 3:
            continue
        model = key[0]
        model_scores[model].append(composite_score(m))

    if not model_scores:
        print("⚠ No data for model comparison plot")
        return

    models = sorted(model_scores, key=lambda x: np.mean(model_scores[x]), reverse=True)
    means = [np.mean(model_scores[m]) for m in models]
    bests = [max(model_scores[m]) for m in models]
    short_names = [m.split("/")[-1] for m in models]

    fig, ax = plt.subplots(1, 1, figsize=(10, 5))
    x = np.arange(len(models))
    w = 0.35
    ax.bar(x - w / 2, means, w, label="Avg Composite", color="#45B7D1", alpha=0.85)
    ax.bar(x + w / 2, bests, w, label="Best Composite", color="#FF6B6B", alpha=0.85)
    ax.set_xticks(x)
    ax.set_xticklabels(short_names, rotation=30, ha="right", fontsize=9)
    ax.set_ylabel("Composite Score")
    ax.set_title("Model Comparison: Avg vs Best Composite Score")
    ax.legend()
    ax.grid(axis="y", alpha=0.3)
    fig.tight_layout()
    fig.savefig(save_path, dpi=150, bbox_inches="tight")
    plt.close(fig)
    print(f"  📊 Saved: {save_path.name}")


def plot_prompt_comparison(metrics_by_config: dict, save_path: Path):
    """Bar chart comparing prompt sets."""
    ps_scores = defaultdict(list)
    for key, m in metrics_by_config.items():
        if m["n"] < 3:
            continue
        ps = key[1]
        ps_scores[ps].append(composite_score(m))

    if not ps_scores:
        print("⚠ No data for prompt comparison plot")
        return

    ps_list = sorted(ps_scores, key=lambda x: np.mean(ps_scores[x]), reverse=True)
    means = [np.mean(ps_scores[p]) for p in ps_list]
    bests = [max(ps_scores[p]) for p in ps_list]

    fig, ax = plt.subplots(1, 1, figsize=(10, 5))
    x = np.arange(len(ps_list))
    w = 0.35
    ax.bar(x - w / 2, means, w, label="Avg Composite", color="#4ECDC4", alpha=0.85)
    ax.bar(x + w / 2, bests, w, label="Best Composite", color="#96CEB4", alpha=0.85)
    ax.set_xticks(x)
    ax.set_xticklabels(ps_list, rotation=35, ha="right", fontsize=8)
    ax.set_ylabel("Composite Score")
    ax.set_title("Prompt Set Comparison: Avg vs Best Composite Score")
    ax.legend()
    ax.grid(axis="y", alpha=0.3)
    fig.tight_layout()
    fig.savefig(save_path, dpi=150, bbox_inches="tight")
    plt.close(fig)
    print(f"  📊 Saved: {save_path.name}")


def plot_fewshot_ablation(metrics_by_config: dict, save_path: Path):
    """Line chart for few-shot ablation."""
    fs_data = defaultdict(lambda: {"pearson": [], "coverage": [], "composite": []})
    for key, m in metrics_by_config.items():
        if m["n"] < 3:
            continue
        ns = key[2]
        fs_data[ns]["pearson"].append(m["macro_pearson"])
        fs_data[ns]["coverage"].append(m["coverage"])
        fs_data[ns]["composite"].append(composite_score(m))

    if not fs_data:
        print("⚠ No data for few-shot ablation plot")
        return

    shots = sorted(fs_data.keys())
    avg_r = [np.mean(fs_data[s]["pearson"]) for s in shots]
    avg_cov = [np.mean(fs_data[s]["coverage"]) for s in shots]
    avg_comp = [np.mean(fs_data[s]["composite"]) for s in shots]

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))

    ax1.plot(shots, avg_r, "o-", color="#FF6B6B", linewidth=2, markersize=8, label="Macro Pearson r")
    ax1.plot(shots, avg_comp, "s-", color="#45B7D1", linewidth=2, markersize=8, label="Composite")
    ax1.set_xlabel("# Few-Shot Examples")
    ax1.set_ylabel("Score")
    ax1.set_title("Few-Shot Ablation: Correlation & Composite")
    ax1.legend()
    ax1.grid(alpha=0.3)
    ax1.set_xticks(shots)

    ax2.plot(shots, avg_cov, "D-", color="#4ECDC4", linewidth=2, markersize=8)
    ax2.set_xlabel("# Few-Shot Examples")
    ax2.set_ylabel("Coverage")
    ax2.set_title("Few-Shot Ablation: Coverage")
    ax2.yaxis.set_major_formatter(mticker.PercentFormatter(1.0))
    ax2.grid(alpha=0.3)
    ax2.set_xticks(shots)

    fig.tight_layout()
    fig.savefig(save_path, dpi=150, bbox_inches="tight")
    plt.close(fig)
    print(f"  📊 Saved: {save_path.name}")


def plot_per_trait_heatmap(metrics_by_config: dict, save_path: Path):
    """Heatmap of per-trait Pearson for top 10 configs."""
    ranked = sorted(
        [(k, m) for k, m in metrics_by_config.items() if m["n"] >= 3],
        key=lambda x: composite_score(x[1]),
        reverse=True,
    )[:10]

    if not ranked:
        print("⚠ No data for per-trait heatmap")
        return

    labels = []
    data = []
    for key, m in ranked:
        model_short = key[0].split("/")[-1][:12]
        ps_short = key[1][:15]
        labels.append(f"{model_short} / {ps_short} / {key[2]}s")
        row = [m["per_trait"].get(t, {}).get("pearson", np.nan) for t in TRAITS]
        data.append(row)

    data_arr = np.array(data)

    fig, ax = plt.subplots(1, 1, figsize=(8, max(4, len(labels) * 0.5)))
    im = ax.imshow(data_arr, cmap="RdYlGn", aspect="auto", vmin=-0.3, vmax=0.6)

    ax.set_xticks(range(len(TRAITS)))
    ax.set_xticklabels([f"{t}\n({TRAIT_LABELS[t][:4]})" for t in TRAITS], fontsize=9)
    ax.set_yticks(range(len(labels)))
    ax.set_yticklabels(labels, fontsize=8)

    for i in range(len(labels)):
        for j in range(len(TRAITS)):
            val = data_arr[i, j]
            if not np.isnan(val):
                color = "white" if abs(val) > 0.3 else "black"
                ax.text(j, i, f"{val:.2f}", ha="center", va="center", fontsize=8, color=color)

    fig.colorbar(im, ax=ax, label="Pearson r", shrink=0.8)
    ax.set_title("Per-Trait Pearson Correlation (Top 10 Configs)")
    fig.tight_layout()
    fig.savefig(save_path, dpi=150, bbox_inches="tight")
    plt.close(fig)
    print(f"  📊 Saved: {save_path.name}")


def plot_coverage_vs_correlation(metrics_by_config: dict, save_path: Path):
    """Scatter plot of coverage vs macro Pearson, colored by model."""
    fig, ax = plt.subplots(1, 1, figsize=(10, 6))
    model_colors = {}
    cmap = plt.cm.Set2
    i = 0

    for key, m in metrics_by_config.items():
        if m["n"] < 2:
            continue
        model = key[0]
        if model not in model_colors:
            model_colors[model] = cmap(i % 8)
            i += 1

        ax.scatter(
            m["coverage"], m["macro_pearson"],
            c=[model_colors[model]], s=80, alpha=0.7,
            edgecolors="white", linewidth=0.5,
        )

    # Legend
    for model, color in model_colors.items():
        ax.scatter([], [], c=[color], s=80, label=model.split("/")[-1])
    ax.legend(loc="upper left", fontsize=8)
    ax.set_xlabel("Coverage (% samples with valid predictions)")
    ax.set_ylabel("Macro Pearson r")
    ax.set_title("Coverage vs Correlation Trade-off")
    ax.axhline(0, color="gray", linestyle="--", alpha=0.3)
    ax.grid(alpha=0.3)
    ax.xaxis.set_major_formatter(mticker.PercentFormatter(1.0))
    fig.tight_layout()
    fig.savefig(save_path, dpi=150, bbox_inches="tight")
    plt.close(fig)
    print(f"  📊 Saved: {save_path.name}")


def plot_bias_by_trait(metrics_by_config: dict, save_path: Path):
    """Box plot of prediction bias per trait across all configs."""
    bias_data = {t: [] for t in TRAITS}
    for key, m in metrics_by_config.items():
        if m["n"] < 3:
            continue
        for t in TRAITS:
            b = m["per_trait"].get(t, {}).get("bias")
            if b is not None:
                bias_data[t].append(b)

    if not any(bias_data.values()):
        print("⚠ No data for bias plot")
        return

    fig, ax = plt.subplots(1, 1, figsize=(8, 5))
    positions = range(len(TRAITS))
    bp = ax.boxplot(
        [bias_data[t] for t in TRAITS],
        positions=positions,
        patch_artist=True,
        labels=[f"{t}\n({TRAIT_LABELS[t][:5]})" for t in TRAITS],
    )
    for patch, t in zip(bp["boxes"], TRAITS):
        patch.set_facecolor(COLORS[t])
        patch.set_alpha(0.7)
    ax.axhline(0, color="red", linestyle="--", alpha=0.5)
    ax.set_ylabel("Mean Signed Error (Prediction - Ground Truth)")
    ax.set_title("Prediction Bias by Trait (across all configs)")
    ax.grid(axis="y", alpha=0.3)
    fig.tight_layout()
    fig.savefig(save_path, dpi=150, bbox_inches="tight")
    plt.close(fig)
    print(f"  📊 Saved: {save_path.name}")


# ── Interpretation ─────────────────────────────────────────────────────────────


def generate_interpretation(metrics_by_config: dict, df: pd.DataFrame) -> str:
    """Generate a thesis-ready interpretation of the results."""
    ranked = sorted(
        [(k, m) for k, m in metrics_by_config.items() if m["n"] >= 3],
        key=lambda x: composite_score(x[1]),
        reverse=True,
    )

    lines = []
    lines.append("=" * 70)
    lines.append("  HARNESS ENGINEERING — RESULTS INTERPRETATION")
    lines.append("=" * 70)
    lines.append("")

    # ── Overview ──
    total_evals = len(df)
    total_valid = df["has_prediction"].sum()
    n_models = df["model"].nunique()
    n_prompts = df["prompt_set"].nunique()
    n_configs = len(metrics_by_config)
    lines.append(f"  Total evaluations: {total_evals}")
    lines.append(f"  Valid predictions: {total_valid} ({total_valid/total_evals:.0%})")
    lines.append(f"  Models tested: {n_models}")
    lines.append(f"  Prompt sets tested: {n_prompts}")
    lines.append(f"  Configurations evaluated: {n_configs}")
    lines.append("")

    # ── Winner Analysis ──
    if ranked:
        wk, wm = ranked[0]
        lines.append("─" * 70)
        lines.append("  🏆 BEST CONFIGURATION")
        lines.append("─" * 70)
        lines.append(f"  Model:       {wk[0]}")
        lines.append(f"  Prompt set:  {wk[1]}")
        lines.append(f"  Few-shots:   {wk[2]}")
        lines.append(f"  Coverage:    {wm['coverage']:.0%}")
        lines.append(f"  Macro r:     {wm['macro_pearson']:.4f} (95% CI: [{wm['ci_lo']:.3f}, {wm['ci_hi']:.3f}])")
        lines.append(f"  Macro MAE:   {wm['macro_mae']:.4f}")
        lines.append(f"  Macro Bias:  {wm['macro_bias']:+.4f}")
        lines.append(f"  Composite:   {composite_score(wm):.4f}")
        lines.append("")

        # Per-trait for winner
        lines.append("  Per-trait breakdown:")
        lines.append(f"  {'Trait':<18} {'Pearson':>8} {'MAE':>8} {'Bias':>8}")
        lines.append(f"  {'─'*18} {'─'*8} {'─'*8} {'─'*8}")
        for t in TRAITS:
            tm = wm["per_trait"].get(t, {})
            if tm:
                lines.append(
                    f"  {TRAIT_LABELS[t]:<18} {tm['pearson']:>8.4f} {tm['mae']:>8.4f} {tm['bias']:>+8.4f}"
                )
        lines.append("")

    # ── Key Findings ──
    lines.append("─" * 70)
    lines.append("  📋 KEY FINDINGS")
    lines.append("─" * 70)

    # 1. Model reliability
    model_coverage = defaultdict(list)
    for key, m in metrics_by_config.items():
        model_coverage[key[0]].append(m["coverage"])

    lines.append("")
    lines.append("  1. MODEL RELIABILITY (API Coverage)")
    for model in sorted(model_coverage, key=lambda x: np.mean(model_coverage[x]), reverse=True):
        avg_cov = np.mean(model_coverage[model])
        lines.append(f"     {model.split('/')[-1]:>30}: {avg_cov:.0%} avg coverage")
    lines.append("")

    # 2. Prompt strategy effectiveness
    ps_pearson = defaultdict(list)
    for key, m in metrics_by_config.items():
        if m["n"] >= 3:
            ps_pearson[key[1]].append(m["macro_pearson"])

    lines.append("  2. PROMPT STRATEGY EFFECTIVENESS (Avg Macro Pearson)")
    for ps in sorted(ps_pearson, key=lambda x: np.mean(ps_pearson[x]), reverse=True):
        avg_r = np.mean(ps_pearson[ps])
        lines.append(f"     {ps:>30}: r = {avg_r:.4f}")
    lines.append("")

    # 3. Few-shot impact
    fs_pearson = defaultdict(list)
    for key, m in metrics_by_config.items():
        if m["n"] >= 3:
            fs_pearson[key[2]].append(m["macro_pearson"])

    lines.append("  3. FEW-SHOT IMPACT")
    for ns in sorted(fs_pearson):
        avg_r = np.mean(fs_pearson[ns])
        lines.append(f"     {ns:>3}-shot: avg r = {avg_r:.4f}")
    lines.append("")

    # 4. Trait difficulty
    trait_pearson = defaultdict(list)
    for key, m in metrics_by_config.items():
        if m["n"] >= 3:
            for t in TRAITS:
                if t in m["per_trait"]:
                    trait_pearson[t].append(m["per_trait"][t]["pearson"])

    lines.append("  4. TRAIT DIFFICULTY RANKING (easiest → hardest)")
    for t in sorted(trait_pearson, key=lambda x: np.mean(trait_pearson[x]), reverse=True):
        avg_r = np.mean(trait_pearson[t])
        lines.append(f"     {TRAIT_LABELS[t]:<20} ({t}): avg r = {avg_r:.4f}")
    lines.append("")

    # 5. Systematic biases
    trait_bias = defaultdict(list)
    for key, m in metrics_by_config.items():
        if m["n"] >= 3:
            for t in TRAITS:
                if t in m["per_trait"]:
                    trait_bias[t].append(m["per_trait"][t]["bias"])

    lines.append("  5. SYSTEMATIC BIASES")
    for t in TRAITS:
        if trait_bias[t]:
            avg_bias = np.mean(trait_bias[t])
            direction = "over-predicts" if avg_bias > 0.05 else "under-predicts" if avg_bias < -0.05 else "well-calibrated"
            lines.append(f"     {TRAIT_LABELS[t]:<20}: bias = {avg_bias:+.3f} ({direction})")
    lines.append("")

    # ── Thesis Recommendations ──
    lines.append("─" * 70)
    lines.append("  📝 THESIS RECOMMENDATIONS")
    lines.append("─" * 70)
    lines.append("")

    if ranked:
        wk, wm = ranked[0]
        lines.append(f"  • DEPLOY: {wk[0]} with {wk[1]} ({wk[2]}-shot)")
        lines.append(f"    Justification: highest composite ({composite_score(wm):.4f})")
        lines.append(f"    with {wm['coverage']:.0%} coverage and r = {wm['macro_pearson']:.4f}")
        lines.append("")

        if wm["macro_pearson"] < 0.2:
            lines.append("  ⚠ CAVEAT: Macro Pearson < 0.20 indicates weak correlation.")
            lines.append("    This means zero-shot Big Five detection from single messages")
            lines.append("    has limited individual-level accuracy — expected for this task.")
            lines.append("    In the thesis, frame this as a task-level insight:")
            lines.append("    '...single-message OCEAN detection achieves r ≈ 0.15,")
            lines.append("     consistent with known psychometric limits of short-text")
            lines.append("     personality assessment (Schwartz et al., 2013).'")
        elif wm["macro_pearson"] < 0.3:
            lines.append("  ℹ Macro Pearson 0.20–0.30: moderate for single-message detection.")
            lines.append("    Comparable to published baselines on PANDORA (Gjurković et al.).")
        else:
            lines.append("  ✓ Macro Pearson > 0.30: competitive with SOTA for this task.")

    lines.append("")
    lines.append("=" * 70)
    return "\n".join(lines)


# ── Main ───────────────────────────────────────────────────────────────────────


def main():
    print("\n🔬 Harness Engineering — Results Analysis\n")

    # Load data
    df = load_all_harness_results()
    df = extract_traits(df)

    # Group by (model, prompt_set, n_shots)
    metrics_by_config: dict[tuple, dict] = {}
    for (model, ps, ns), group in df.groupby(["model", "prompt_set", "n_shots"]):
        metrics_by_config[(model, ps, ns)] = compute_group_metrics(group)

    print(f"\n  Configs with ≥3 valid predictions: "
          f"{sum(1 for m in metrics_by_config.values() if m['n'] >= 3)}/{len(metrics_by_config)}")

    # ── Generate plots ──
    print("\n📊 Generating visualizations...")
    plot_dir = RESULTS_DIR / "plots"
    plot_dir.mkdir(exist_ok=True)

    plot_model_comparison(metrics_by_config, plot_dir / "model_comparison.png")
    plot_prompt_comparison(metrics_by_config, plot_dir / "prompt_comparison.png")
    plot_fewshot_ablation(metrics_by_config, plot_dir / "fewshot_ablation.png")
    plot_per_trait_heatmap(metrics_by_config, plot_dir / "per_trait_heatmap.png")
    plot_coverage_vs_correlation(metrics_by_config, plot_dir / "coverage_vs_correlation.png")
    plot_bias_by_trait(metrics_by_config, plot_dir / "bias_by_trait.png")

    # ── Generate interpretation ──
    print("\n📝 Generating interpretation...")
    interpretation = generate_interpretation(metrics_by_config, df)
    print(interpretation)

    # Save interpretation
    interp_path = RESULTS_DIR / "INTERPRETATION_LATEST.txt"
    interp_path.write_text(interpretation, encoding="utf-8")
    print(f"\n✓ Saved: {interp_path}")

    # ── Save summary CSV ──
    summary_rows = []
    for key, m in metrics_by_config.items():
        summary_rows.append({
            "model": key[0],
            "prompt_set": key[1],
            "n_shots": key[2],
            "n": m["n"],
            "coverage": m["coverage"],
            "macro_pearson": m["macro_pearson"],
            "macro_spearman": m.get("macro_spearman", np.nan),
            "macro_mae": m["macro_mae"],
            "macro_bias": m["macro_bias"],
            "ci_lo": m.get("ci_lo", np.nan),
            "ci_hi": m.get("ci_hi", np.nan),
            "composite": composite_score(m),
        })
    summary_df = pd.DataFrame(summary_rows).sort_values("composite", ascending=False)
    summary_path = RESULTS_DIR / "harness_summary_latest.csv"
    summary_df.to_csv(summary_path, index=False)
    print(f"✓ Saved: {summary_path}")

    print(f"\n✓ All outputs in: {plot_dir}/")
    print("  Run '%run analyze_harness_results.py' in IPython to re-analyze.")


if __name__ == "__main__":
    main()
