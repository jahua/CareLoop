#!/usr/bin/env python3
"""
Seaborn-first publication plots for the enhanced analysis notebook.

This module keeps the same dataset + scoring pipeline, but renders key figures
using Seaborn APIs (barplot, histplot, heatmap, catplot) with a consistent,
publication-friendly theme.
"""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from visualization_config import configure_matplotlib, PUBLICATION_CONFIG as C


def configure_seaborn() -> None:
    """Apply a consistent Seaborn theme on top of matplotlib rcParams."""
    configure_matplotlib()
    sns.set_theme(
        style="whitegrid",
        context="paper",
        font="sans-serif",
        rc={
            "axes.titlesize": C.FONT_SIZE_LARGE,
            "axes.labelsize": C.FONT_SIZE_MEDIUM,
            "legend.fontsize": C.FONT_SIZE_BASE,
            "xtick.labelsize": C.FONT_SIZE_BASE,
            "ytick.labelsize": C.FONT_SIZE_BASE,
        },
    )
    sns.set_palette([C.COLOR_REGULATED, C.COLOR_BASELINE, C.COLOR_POSITIVE, C.COLOR_ACCENT])


def _ensure_dir(output_dir: str) -> Path:
    out = Path(output_dir)
    out.mkdir(parents=True, exist_ok=True)
    return out


def plot_sample_distribution(df_regulated: pd.DataFrame, *, output_dir: str) -> Path:
    """Seaborn version of sample distribution (counts + turns histogram)."""
    out = _ensure_dir(output_dir)
    fig, axes = plt.subplots(1, 2, figsize=(C.FIGURE_WIDTH_DOUBLE, C.FIGURE_HEIGHT_SHORT), dpi=150)

    # Conversations per personality type
    reg_counts = df_regulated.groupby("Personality_Type")["Conversation_ID"].nunique().reset_index()
    reg_counts.columns = ["Personality_Type", "Conversations"]
    sns.barplot(
        data=reg_counts,
        x="Personality_Type",
        y="Conversations",
        ax=axes[0],
        color=C.COLOR_REGULATED,
        edgecolor=C.COLOR_GRAY,
    )
    axes[0].set_title("Conversations per Personality Type", fontweight="bold")
    axes[0].set_xlabel("Personality type")
    axes[0].set_ylabel("Conversations")
    axes[0].spines["top"].set_visible(False)
    axes[0].spines["right"].set_visible(False)

    # Turns per conversation
    msg_counts = df_regulated.groupby("Conversation_ID").size().rename("Turns").reset_index()
    sns.histplot(
        data=msg_counts,
        x="Turns",
        bins=range(int(msg_counts["Turns"].min()), int(msg_counts["Turns"].max()) + 2),
        ax=axes[1],
        color=C.COLOR_BASELINE,
        edgecolor=C.COLOR_GRAY,
    )
    axes[1].set_title("Turns per Conversation", fontweight="bold")
    axes[1].set_xlabel("Turns")
    axes[1].set_ylabel("Conversations")
    axes[1].spines["top"].set_visible(False)
    axes[1].spines["right"].set_visible(False)

    fig.tight_layout()
    path = out / "01_sample_distribution.png"
    fig.savefig(path, dpi=C.DPI, bbox_inches=C.BBOX_INCHES, facecolor=C.FACECOLOR)
    plt.close(fig)
    return path


def plot_missingness(df_regulated: pd.DataFrame, df_baseline: pd.DataFrame, *, output_dir: str) -> Path:
    """Binary missingness heatmap (Seaborn heatmap)."""
    out = _ensure_dir(output_dir)
    fig, axes = plt.subplots(1, 2, figsize=(C.FIGURE_WIDTH_DOUBLE, C.FIGURE_HEIGHT_MEDIUM), dpi=150)

    cmap = sns.color_palette([C.FACECOLOR, C.FILL_RED], as_cmap=True)  # 0=present, 1=missing

    miss_reg = df_regulated.isnull().astype(int)
    sns.heatmap(
        miss_reg.T,
        cmap=cmap,
        ax=axes[0],
        cbar=True,
        xticklabels=False,
        yticklabels=df_regulated.columns,
        linewidths=0.2,
        linecolor="#EFEFEF",
    )
    axes[0].set_title("Missingness (Regulated)", fontweight="bold")
    axes[0].set_xlabel("Row index")

    miss_base = df_baseline.isnull().astype(int)
    sns.heatmap(
        miss_base.T,
        cmap=cmap,
        ax=axes[1],
        cbar=True,
        xticklabels=False,
        yticklabels=df_baseline.columns,
        linewidths=0.2,
        linecolor="#EFEFEF",
    )
    axes[1].set_title("Missingness (Baseline)", fontweight="bold")
    axes[1].set_xlabel("Row index")

    fig.tight_layout()
    path = out / "02_missing_data_heatmap.png"
    fig.savefig(path, dpi=C.DPI, bbox_inches=C.BBOX_INCHES, facecolor=C.FACECOLOR)
    plt.close(fig)
    return path


def plot_personality_dimensions(df_personality: pd.DataFrame, *, output_dir: str) -> Path:
    """Count distributions for O/C/E/A/N values (-1/0/1) across turns."""
    out = _ensure_dir(output_dir)
    dims = ["O", "C", "E", "A", "N"]
    if not all(d in df_personality.columns for d in dims):
        raise KeyError("Expected O/C/E/A/N columns in df_personality.")

    long = df_personality[dims].melt(var_name="Dimension", value_name="Value")
    # Ensure consistent ordering
    long["Value"] = long["Value"].astype(int)
    value_order = [-1, 0, 1]

    fig, axes = plt.subplots(2, 3, figsize=(C.FIGURE_WIDTH_DOUBLE, C.FIGURE_HEIGHT_TALL), dpi=150)
    axes = axes.flatten()

    for i, dim in enumerate(dims):
        ax = axes[i]
        sub = long[long["Dimension"] == dim]
        sns.countplot(
            data=sub,
            x="Value",
            order=value_order,
            ax=ax,
            color=C.COLOR_REGULATED,
            edgecolor=C.COLOR_GRAY,
        )
        ax.set_title(dim, fontweight="bold")
        ax.set_xlabel("Trait value")
        ax.set_ylabel("Count")
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)

    axes[5].axis("off")
    fig.suptitle("OCEAN Dimension Distributions", y=1.02, fontweight="bold")
    fig.tight_layout()

    path = out / "06_personality_dimensions.png"
    fig.savefig(path, dpi=C.DPI, bbox_inches=C.BBOX_INCHES, facecolor=C.FACECOLOR)
    plt.close(fig)
    return path


def plot_personality_heatmap(df_personality: pd.DataFrame, *, output_dir: str) -> Path:
    """Seaborn heatmap of OCEAN values (messages x dimensions)."""
    out = _ensure_dir(output_dir)

    dims = ["O", "C", "E", "A", "N"]
    if not all(d in df_personality.columns for d in dims):
        raise KeyError("Expected O/C/E/A/N columns in df_personality.")

    df_sorted = df_personality.sort_values(["Conversation_ID", "Turn_Number"])
    mat = df_sorted[dims].T

    fig, ax = plt.subplots(figsize=(C.FIGURE_WIDTH_DOUBLE, C.FIGURE_HEIGHT_SHORT), dpi=150)
    cmap = sns.diverging_palette(25, 240, as_cmap=True)
    sns.heatmap(mat, ax=ax, cmap=cmap, vmin=-1, vmax=1, cbar_kws={"label": "Trait value"})
    ax.set_title("Personality Vector Heatmap (OCEAN)", fontweight="bold")
    ax.set_xlabel("Message index")
    ax.set_ylabel("Dimension")
    fig.tight_layout()

    path = out / "07_personality_heatmap.png"
    fig.savefig(path, dpi=C.DPI, bbox_inches=C.BBOX_INCHES, facecolor=C.FACECOLOR)
    plt.close(fig)
    return path


def plot_weighted_scores(df_reg_scored: pd.DataFrame, df_base_scored: pd.DataFrame, *, output_dir: str) -> Path:
    """Seaborn grouped barplot for the 0-2 weighted scores."""
    out = _ensure_dir(output_dir)

    metrics = [
        ("Emotional_Tone_Score", "Emotional Tone"),
        ("Relevance_Coherence_Score", "Relevance & Coherence"),
        ("Personality_Needs_Score", "Personality Needs"),
    ]

    rows = []
    for col, label in metrics:
        rows.append({"Condition": "Regulated", "Metric": label, "Score": df_reg_scored[col].astype(float).values})
        rows.append({"Condition": "Baseline", "Metric": label, "Score": df_base_scored[col].astype(float).values})

    long = pd.concat([pd.DataFrame(r).explode("Score") for r in rows], ignore_index=True)
    long["Score"] = long["Score"].astype(float)

    fig, ax = plt.subplots(figsize=(C.FIGURE_WIDTH_SINGLE, C.FIGURE_HEIGHT_MEDIUM), dpi=150)
    sns.barplot(
        data=long,
        x="Metric",
        y="Score",
        hue="Condition",
        ax=ax,
        errorbar="sd",
        palette={"Regulated": C.COLOR_REGULATED, "Baseline": C.COLOR_BASELINE},
        edgecolor=C.COLOR_GRAY,
    )
    ax.set_title("Weighted Scores (0-2)", fontweight="bold")
    ax.set_xlabel("")
    ax.set_ylabel("Score")
    ax.set_ylim(0, 2.2)
    ax.legend(frameon=True, title="")
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    fig.tight_layout()

    path = out / "08_weighted_scores.png"
    fig.savefig(path, dpi=C.DPI, bbox_inches=C.BBOX_INCHES, facecolor=C.FACECOLOR)
    plt.close(fig)
    return path


def plot_total_scores(df_reg_scored: pd.DataFrame, df_base_scored: pd.DataFrame, *, output_dir: str) -> Path:
    """Seaborn box + strip for total score (0-6)."""
    out = _ensure_dir(output_dir)

    reg = df_reg_scored["Total_Regulated_Score"].astype(float)
    base = df_base_scored["Total_Baseline_Score"].astype(float)
    df = pd.DataFrame(
        {
            "Condition": ["Regulated"] * len(reg) + ["Baseline"] * len(base),
            "Total": np.concatenate([reg.values, base.values]),
        }
    )

    fig, ax = plt.subplots(figsize=(C.FIGURE_WIDTH_SINGLE, C.FIGURE_HEIGHT_MEDIUM), dpi=150)
    sns.boxplot(
        data=df,
        x="Condition",
        y="Total",
        ax=ax,
        palette={"Regulated": C.FILL_BLUE, "Baseline": C.FILL_ORANGE},
        width=0.55,
        showfliers=False,
    )
    sns.stripplot(
        data=df,
        x="Condition",
        y="Total",
        ax=ax,
        palette={"Regulated": C.COLOR_REGULATED, "Baseline": C.COLOR_BASELINE},
        size=3.2,
        alpha=0.6,
        jitter=0.15,
    )
    ax.set_title("Total Score (0-6)", fontweight="bold")
    ax.set_xlabel("")
    ax.set_ylabel("Total")
    ax.set_ylim(0, 6.8)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    fig.tight_layout()

    path = out / "09_total_score_boxplot.png"
    fig.savefig(path, dpi=C.DPI, bbox_inches=C.BBOX_INCHES, facecolor=C.FACECOLOR)
    plt.close(fig)
    return path


def plot_performance_comparison(df_stats: pd.DataFrame, *, output_dir: str) -> Path:
    """
    Seaborn barplot for 0-1 means by condition, with manual 95% CI error bars from df_stats.
    Expects columns: Metric, Condition, Mean, CI_Lower, CI_Upper.
    """
    out = _ensure_dir(output_dir)

    common = df_stats[df_stats["Condition"].isin(["Regulated", "Baseline"])].copy()
    # Only metrics with both conditions
    metric_counts = common.groupby("Metric")["Condition"].count()
    valid_metrics = metric_counts[metric_counts == 2].index.tolist()
    common = common[common["Metric"].isin(valid_metrics)]

    fig, ax = plt.subplots(figsize=(C.FIGURE_WIDTH_SINGLE, C.FIGURE_HEIGHT_MEDIUM), dpi=150)
    sns.barplot(
        data=common,
        x="Metric",
        y="Mean",
        hue="Condition",
        ax=ax,
        palette={"Regulated": C.COLOR_REGULATED, "Baseline": C.COLOR_BASELINE},
        edgecolor=C.COLOR_GRAY,
        errorbar=None,
    )

    # Manual CI error bars
    # Determine bar centers in drawing order: seaborn draws grouped bars per x category.
    for container, (cond, color) in zip(
        ax.containers,
        [("Regulated", C.COLOR_REGULATED), ("Baseline", C.COLOR_BASELINE)],
    ):
        rows = common[common["Condition"] == cond].set_index("Metric").reindex(valid_metrics)
        ci_low = rows["CI_Lower"].values.astype(float)
        ci_high = rows["CI_Upper"].values.astype(float)
        means = rows["Mean"].values.astype(float)
        for rect, lo, hi, m in zip(container, ci_low, ci_high, means):
            x = rect.get_x() + rect.get_width() / 2
            if np.isfinite(lo) and np.isfinite(hi):
                ax.plot([x, x], [lo, hi], color=C.COLOR_GRAY, linewidth=1.2, zorder=3)
                ax.plot([x - 0.03, x + 0.03], [lo, lo], color=C.COLOR_GRAY, linewidth=1.2, zorder=3)
                ax.plot([x - 0.03, x + 0.03], [hi, hi], color=C.COLOR_GRAY, linewidth=1.2, zorder=3)

    ax.set_title("Performance Comparison (0-1)", fontweight="bold")
    ax.set_xlabel("")
    ax.set_ylabel("Mean")
    ax.set_ylim(0, 1.08)
    ax.legend(frameon=True, title="")
    ax.tick_params(axis="x", rotation=0)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.grid(axis="y", alpha=C.GRID_ALPHA, linestyle=C.GRID_LINESTYLE)
    fig.tight_layout()

    path = out / "03_performance_comparison.png"
    fig.savefig(path, dpi=C.DPI, bbox_inches=C.BBOX_INCHES, facecolor=C.FACECOLOR)
    plt.close(fig)
    return path


def plot_effect_sizes(df_effects: pd.DataFrame, *, output_dir: str) -> Path:
    """Seaborn horizontal barplot for effect sizes (Cohen's d)."""
    out = _ensure_dir(output_dir)
    df = df_effects.copy()
    df["Direction"] = np.where(df["Cohens_d"] >= 0, "Regulated > Baseline", "Baseline > Regulated")

    fig, ax = plt.subplots(figsize=(C.FIGURE_WIDTH_SINGLE, C.FIGURE_HEIGHT_MEDIUM), dpi=150)
    sns.barplot(
        data=df,
        y="Metric",
        x="Cohens_d",
        ax=ax,
        palette=[C.COLOR_POSITIVE if v >= 0 else C.COLOR_NEGATIVE for v in df["Cohens_d"].values],
        edgecolor=C.COLOR_GRAY,
        orient="h",
        errorbar=None,
    )
    ax.axvline(0, color=C.COLOR_GRAY, linewidth=1.0)
    for v in (0.2, 0.5, 0.8):
        ax.axvline(v, color=C.COLOR_GRAY, linestyle="--", alpha=0.35, linewidth=0.8)
        ax.axvline(-v, color=C.COLOR_GRAY, linestyle="--", alpha=0.35, linewidth=0.8)
    ax.set_title("Effect Sizes (Cohen's d)", fontweight="bold")
    ax.set_xlabel("Cohen's d")
    ax.set_ylabel("")
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.grid(axis="x", alpha=C.GRID_ALPHA, linestyle=C.GRID_LINESTYLE)
    fig.tight_layout()

    path = out / "04_effect_sizes.png"
    fig.savefig(path, dpi=C.DPI, bbox_inches=C.BBOX_INCHES, facecolor=C.FACECOLOR)
    plt.close(fig)
    return path


def plot_percentage_improvement(df_effects: pd.DataFrame, *, output_dir: str) -> Path:
    """Seaborn horizontal barplot of percentage-point differences."""
    out = _ensure_dir(output_dir)
    df = df_effects.copy()
    df["pp"] = df["Difference"].astype(float) * 100.0

    fig, ax = plt.subplots(figsize=(C.FIGURE_WIDTH_SINGLE, C.FIGURE_HEIGHT_MEDIUM), dpi=150)
    sns.barplot(
        data=df,
        y="Metric",
        x="pp",
        ax=ax,
        palette=[C.COLOR_POSITIVE if v >= 0 else C.COLOR_NEGATIVE for v in df["pp"].values],
        edgecolor=C.COLOR_GRAY,
        orient="h",
        errorbar=None,
    )
    ax.axvline(0, color=C.COLOR_GRAY, linewidth=1.0)
    ax.set_title("Percentage-point Differences", fontweight="bold")
    ax.set_xlabel("Regulated - Baseline (pp)")
    ax.set_ylabel("")
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.grid(axis="x", alpha=C.GRID_ALPHA, linestyle=C.GRID_LINESTYLE)
    fig.tight_layout()

    path = out / "05_percentage_improvement.png"
    fig.savefig(path, dpi=C.DPI, bbox_inches=C.BBOX_INCHES, facecolor=C.FACECOLOR)
    plt.close(fig)
    return path


def plot_selective_enhancement(df_regulated: pd.DataFrame, df_baseline: pd.DataFrame, *, output_dir: str) -> Path:
    """
    Seaborn faceted barplots of YES-rate (conversation-level) per metric, by condition.
    """
    out = _ensure_dir(output_dir)
    common_metrics = ["EMOTIONAL TONE APPROPRIATE", "RELEVANCE & COHERENCE", "PERSONALITY NEEDS ADDRESSED"]

    def yes_rate_by_conv(df: pd.DataFrame, metric: str) -> pd.Series:
        s = df[metric].astype(str).str.upper()
        is_yes = (s == "YES").astype(float)
        return is_yes.groupby(df["Conversation_ID"]).mean()

    rows = []
    for m in common_metrics:
        r = yes_rate_by_conv(df_regulated, m)
        b = yes_rate_by_conv(df_baseline, m)
        convs = sorted(set(r.index).intersection(set(b.index)))
        for c in convs:
            rows.append({"Metric": m.title(), "Conversation_ID": c, "Condition": "Baseline", "YES_rate": float(b.loc[c])})
            rows.append({"Metric": m.title(), "Conversation_ID": c, "Condition": "Regulated", "YES_rate": float(r.loc[c])})

    long = pd.DataFrame(rows)
    g = sns.catplot(
        data=long,
        x="Condition",
        y="YES_rate",
        col="Metric",
        kind="point",
        errorbar=None,
        order=["Baseline", "Regulated"],
        height=3.0,
        aspect=1.15,
        palette={"Regulated": C.COLOR_REGULATED, "Baseline": C.COLOR_BASELINE},
    )
    g.set(ylim=(-0.02, 1.02))
    g.set_axis_labels("", "YES-rate (per conversation)")
    g.set_titles("{col_name}")
    for ax in g.axes.flat:
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)
        ax.grid(axis="y", alpha=C.GRID_ALPHA, linestyle=C.GRID_LINESTYLE)

    path = out / "10_selective_enhancement_paired.png"
    g.fig.suptitle("Selective Enhancement (Paired Scenario YES-rates)", y=1.08, fontweight="bold")
    g.fig.tight_layout()
    g.fig.savefig(path, dpi=C.DPI, bbox_inches=C.BBOX_INCHES, facecolor=C.FACECOLOR)
    plt.close(g.fig)
    return path


def plot_rating_composition(df_regulated: pd.DataFrame, df_baseline: pd.DataFrame, *, output_dir: str) -> Path:
    """
    Seaborn grouped composition plot: proportion of YES/NOT SURE/NO by metric, faceted by condition.
    (Seaborn doesn't do stacked bars cleanly; this is the publication-friendly alternative.)
    """
    out = _ensure_dir(output_dir)
    metrics = ["EMOTIONAL TONE APPROPRIATE", "RELEVANCE & COHERENCE", "PERSONALITY NEEDS ADDRESSED"]
    ratings = ["YES", "NOT SURE", "NO"]

    def _props(df: pd.DataFrame, metric: str) -> dict[str, float]:
        s = df[metric].astype(str).str.upper()
        total = float(len(s))
        return {r: float((s == r).sum()) / total for r in ratings}

    rows = []
    for cond, df in [("Baseline", df_baseline), ("Regulated", df_regulated)]:
        for m in metrics:
            if m not in df.columns:
                continue
            props = _props(df, m)
            for r in ratings:
                rows.append({"Condition": cond, "Metric": m.title(), "Rating": r, "Proportion": props[r]})

    long = pd.DataFrame(rows)
    g = sns.catplot(
        data=long,
        kind="bar",
        x="Metric",
        y="Proportion",
        hue="Rating",
        col="Condition",
        height=3.6,
        aspect=1.2,
        palette={"YES": C.COLOR_POSITIVE, "NOT SURE": C.COLOR_NEUTRAL, "NO": C.COLOR_NEGATIVE},
        edgecolor=C.COLOR_GRAY,
        legend=True,
    )
    g.set_titles("{col_name}")
    g.set_axis_labels("", "Proportion")
    g.set(ylim=(0, 1.0))
    for ax in g.axes.flat:
        ax.tick_params(axis="x", rotation=0)
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)
        ax.grid(axis="y", alpha=C.GRID_ALPHA, linestyle=C.GRID_LINESTYLE)

    path = out / "11_metric_composition.png"
    g.fig.suptitle("Rating Composition by Metric (Proportions)", y=1.08, fontweight="bold")
    g.fig.tight_layout()
    g.fig.savefig(path, dpi=C.DPI, bbox_inches=C.BBOX_INCHES, facecolor=C.FACECOLOR)
    plt.close(g.fig)
    return path

