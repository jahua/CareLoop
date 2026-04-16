#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Standalone Effect Sizes figure generator.
Produces 04_effect_sizes.png in the same directory.
Values are taken directly from the paper's statistical results.
"""

from pathlib import Path
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

OUT = Path(__file__).resolve().parent

# ── Data (from paper Table 4) ──────────────────────────────────────────────
# Listed bottom-to-top so primary outcome (Personality Needs) appears at top
metrics = ["Emotional Tone", "Relevance &\nCoherence", "Personality Needs\n(Primary)"]
values  = [0.000, 0.183, 4.42]
colors  = ["#aec7e8", "#aec7e8", "#2ca02c"]   # blue for secondary, green for primary

# Cohen's d interpretation thresholds
thresholds = [(0.2, "small"), (0.5, "medium"), (0.8, "large")]

DPI = 300

plt.rcParams.update({
    "font.family": "DejaVu Sans",
    "font.size":   10,
    "axes.linewidth": 0.8,
})

fig, ax = plt.subplots(figsize=(10, 4.2))
fig.suptitle("Effect Sizes: Cohen's d  (Regulated vs Baseline)",
             fontsize=12, fontweight="bold", y=0.98)

y_pos = np.arange(len(metrics))
bars = ax.barh(y_pos, values, color=colors, alpha=0.85,
               edgecolor="gray", linewidth=0.8)

# Zero line
ax.axvline(x=0, color="black", linestyle="-", linewidth=1.0)

# Threshold reference lines with non-overlapping labels at top
ax_top = ax.get_ylim()[1]
for thr, label in thresholds:
    ax.axvline(x=thr,  color="gray", linestyle="--", alpha=0.4, linewidth=0.8)
    ax.axvline(x=-thr, color="gray", linestyle="--", alpha=0.4, linewidth=0.8)
    # Label above the plot area (using ax.text with clip_on=False)
    ax.text(thr, ax_top + 0.08, label,
            ha="center", va="bottom", fontsize=7.5,
            color="#777777", clip_on=False)

# Value labels on bars
for i, val in enumerate(values):
    offset = 0.08 if val >= 0 else -0.08
    ha = "left" if val >= 0 else "right"
    ax.text(val + offset, i, f"{val:.3f}",
            va="center", ha=ha, fontweight="bold", fontsize=10)

ax.set_yticks(y_pos)
ax.set_yticklabels(metrics, fontsize=10)
ax.set_xlabel("Cohen's d", fontweight="bold")
ax.set_xlim(-0.5, 5.0)

# Clean style
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
ax.grid(axis="x", alpha=0.3, linestyle="--")
ax.set_axisbelow(True)

plt.tight_layout()

out_path = OUT / "04_effect_sizes.png"
fig.savefig(str(out_path), dpi=DPI, bbox_inches="tight",
            facecolor="white", edgecolor="none")
plt.close(fig)
print(f"Saved: {out_path}")
