#!/usr/bin/env python3
"""
Generate publication-quality data completeness figure for paper.
"""

import matplotlib.pyplot as plt
import numpy as np

# Publication-quality settings
plt.rcParams.update({
    'font.family': 'sans-serif',
    'font.sans-serif': ['Arial', 'Helvetica', 'DejaVu Sans'],
    'font.size': 10,
    'axes.labelsize': 11,
    'axes.titlesize': 12,
    'xtick.labelsize': 10,
    'ytick.labelsize': 10,
    'legend.fontsize': 9,
    'figure.dpi': 300,
    'savefig.dpi': 300,
    'savefig.bbox': 'tight',
    'axes.spines.top': False,
    'axes.spines.right': False,
})

# Data from analysis
metrics = [
    'Emotional Tone',
    'Relevance & Coherence', 
    'Personality Needs',
    'Detection Accurate',
    'Regulation Effective'
]

# Completeness data (n observed / n expected)
regulated_complete = [59/59, 59/59, 59/59, 58/59, 59/59]  # percentages
baseline_complete = [60/60, 60/60, 58/60, np.nan, np.nan]  # NaN for N/A metrics

regulated_pct = [x * 100 for x in regulated_complete]
baseline_pct = [x * 100 if not np.isnan(x) else 0 for x in baseline_complete]

# Create figure
fig, ax = plt.subplots(figsize=(8, 4.5))

y_pos = np.arange(len(metrics))
height = 0.35

# Plot bars
bars1 = ax.barh(y_pos + height/2, regulated_pct, height, 
                label='Regulated (n=59)', color='#0173B2', alpha=0.9)
bars2 = ax.barh(y_pos - height/2, baseline_pct, height,
                label='Baseline (n=60)', color='#DE8F05', alpha=0.9)

# Add percentage labels on bars
for i, (bar, pct) in enumerate(zip(bars1, regulated_pct)):
    ax.text(bar.get_width() - 3, bar.get_y() + bar.get_height()/2, 
            f'{pct:.1f}%', ha='right', va='center', color='white', fontweight='bold', fontsize=9)

for i, (bar, pct, orig) in enumerate(zip(bars2, baseline_pct, baseline_complete)):
    if np.isnan(orig):
        ax.text(5, bar.get_y() + bar.get_height()/2, 
                'N/A', ha='left', va='center', color='#666666', fontsize=9, style='italic')
    else:
        ax.text(bar.get_width() - 3, bar.get_y() + bar.get_height()/2,
                f'{pct:.1f}%', ha='right', va='center', color='white', fontweight='bold', fontsize=9)

# Add vertical line at 95% threshold
ax.axvline(x=95, color='#CC78BC', linestyle='--', linewidth=1.5, alpha=0.7, label='95% threshold')

# Customize axes
ax.set_xlim(0, 105)
ax.set_ylim(-0.5, len(metrics) - 0.5)
ax.set_xlabel('Data Completeness (%)')
ax.set_yticks(y_pos)
ax.set_yticklabels(metrics)
ax.invert_yaxis()  # Top metric first

# Add gridlines
ax.xaxis.grid(True, linestyle='-', alpha=0.3)
ax.set_axisbelow(True)

# Legend
ax.legend(loc='lower right', framealpha=0.95)

# Title
ax.set_title('Data Completeness by Evaluation Metric', fontweight='bold', pad=10)

# Add sample size annotation
ax.text(0.98, 0.02, 'Total: 10 conversations\n(5 Type A, 5 Type B)', 
        transform=ax.transAxes, ha='right', va='bottom',
        fontsize=8, color='#666666',
        bbox=dict(boxstyle='round,pad=0.3', facecolor='white', edgecolor='#cccccc', alpha=0.9))

plt.tight_layout()

# Save figure
output_path = 'figures/12_data_completeness.png'
plt.savefig(output_path, dpi=300, bbox_inches='tight', facecolor='white')
print(f"Figure saved to: {output_path}")

plt.close()
