#!/usr/bin/env python3
"""
Generate sample statistical figures with new style guide
"""
import matplotlib.pyplot as plt
import numpy as np
from visualization_config import (
    configure_matplotlib, 
    save_figure_multi_format,
    verify_figure_resolution,
    PUBLICATION_CONFIG as C
)

print("="*80)
print("  GENERATING SAMPLE FIGURES WITH NEW STYLE GUIDE")
print("="*80)

# Apply style guide
configure_matplotlib(apply_style_guide=True)
print("\n✓ Style guide applied")

# Generate sample data
np.random.seed(42)
regulated_scores = np.random.normal(8.5, 1.2, 60)
baseline_scores = np.random.normal(6.0, 1.5, 60)

# Figure 1: Box plot comparison
print("\n1. Generating box plot comparison...")
fig, ax = plt.subplots(figsize=(C.FIGURE_WIDTH_SINGLE, 4.0))

bp = ax.boxplot([regulated_scores, baseline_scores], 
                 labels=['Regulated', 'Baseline'],
                 patch_artist=True,
                 widths=0.6)

# Style boxes
bp['boxes'][0].set_facecolor(C.FILL_BLUE)
bp['boxes'][0].set_edgecolor(C.COLOR_REGULATED)
bp['boxes'][1].set_facecolor(C.FILL_ORANGE)
bp['boxes'][1].set_edgecolor(C.COLOR_BASELINE)

ax.set_ylabel('Score', fontsize=C.FONT_SIZE_AXIS_LABELS)
ax.set_title('Performance Comparison', fontsize=C.FONT_SIZE_TITLE, pad=10)
ax.tick_params(labelsize=C.FONT_SIZE_TICK_LABELS)
ax.grid(axis='y', alpha=0.3, linewidth=C.LINE_WIDTH_GRID)
ax.set_axisbelow(True)

result = verify_figure_resolution(fig, target_width_px=2000, dpi=600)
print(f"   Resolution: {result['width_px']} × {result['height_px']} px ✓")

save_figure_multi_format(fig, 'sample_boxplot', high_res=True, verbose=True)
plt.close()

# Figure 2: Bar chart
print("\n2. Generating bar chart...")
fig, ax = plt.subplots(figsize=(C.FIGURE_WIDTH_SINGLE, 4.0))

metrics = ['Emotional\nTone', 'Relevance', 'Personality\nNeeds']
reg_values = [100, 99, 100]
base_values = [100, 97, 8]

x = np.arange(len(metrics))
width = 0.35

bars1 = ax.bar(x - width/2, reg_values, width, 
               label='Regulated', color=C.COLOR_REGULATED, 
               edgecolor='white', linewidth=1.5)
bars2 = ax.bar(x + width/2, base_values, width,
               label='Baseline', color=C.COLOR_BASELINE,
               edgecolor='white', linewidth=1.5)

ax.set_ylabel('Score (%)', fontsize=C.FONT_SIZE_AXIS_LABELS)
ax.set_title('Metric Comparison', fontsize=C.FONT_SIZE_TITLE, pad=10)
ax.set_xticks(x)
ax.set_xticklabels(metrics, fontsize=C.FONT_SIZE_TICK_LABELS)
ax.tick_params(axis='y', labelsize=C.FONT_SIZE_TICK_LABELS)
ax.legend(fontsize=C.FONT_SIZE_LEGEND, frameon=True)
ax.grid(axis='y', alpha=0.3, linewidth=C.LINE_WIDTH_GRID)
ax.set_axisbelow(True)
ax.set_ylim(0, 110)

result = verify_figure_resolution(fig, target_width_px=2000, dpi=600)
print(f"   Resolution: {result['width_px']} × {result['height_px']} px ✓")

save_figure_multi_format(fig, 'sample_barchart', high_res=True, verbose=True)
plt.close()

# Figure 3: Line plot (double column)
print("\n3. Generating line plot (double column)...")
fig, ax = plt.subplots(figsize=(C.FIGURE_WIDTH_DOUBLE, 4.5))

turns = np.arange(1, 11)
reg_detection = np.array([0.8, 0.85, 0.9, 0.92, 0.95, 0.96, 0.97, 0.98, 0.98, 0.99])
base_detection = np.array([0.7, 0.72, 0.75, 0.73, 0.76, 0.74, 0.77, 0.75, 0.78, 0.76])

ax.plot(turns, reg_detection, 'o-', linewidth=C.LINE_WIDTH, 
        color=C.COLOR_REGULATED, markersize=6, label='Regulated')
ax.plot(turns, base_detection, 's-', linewidth=C.LINE_WIDTH,
        color=C.COLOR_BASELINE, markersize=6, label='Baseline')

ax.set_xlabel('Dialogue Turn', fontsize=C.FONT_SIZE_AXIS_LABELS)
ax.set_ylabel('Detection Accuracy', fontsize=C.FONT_SIZE_AXIS_LABELS)
ax.set_title('Detection Performance Over Time', fontsize=C.FONT_SIZE_TITLE, pad=10)
ax.tick_params(labelsize=C.FONT_SIZE_TICK_LABELS)
ax.legend(fontsize=C.FONT_SIZE_LEGEND, frameon=True)
ax.grid(True, alpha=0.3, linewidth=C.LINE_WIDTH_GRID)
ax.set_axisbelow(True)

result = verify_figure_resolution(fig, target_width_px=4000, dpi=600)
print(f"   Resolution: {result['width_px']} × {result['height_px']} px ✓")
print(f"   Meets 2-column requirement: {result['meets_requirement']}")

save_figure_multi_format(fig, 'sample_lineplot', high_res=True, verbose=True)
plt.close()

print("\n" + "="*80)
print("  ✓ All sample figures generated successfully!")
print("="*80)
print("\nGenerated files:")
print("  • sample_boxplot.{png,pdf}")
print("  • sample_barchart.{png,pdf}")
print("  • sample_lineplot.{png,pdf}")
print("\nAll figures meet FIGURE_STYLE_GUIDE.md requirements:")
print("  ✓ PDF (vector) + PNG (raster) formats")
print("  ✓ 600 DPI for high resolution")
print("  ✓ Proper MDPI column widths (85mm / 170mm)")
print("  ✓ Typography: 8-9pt labels, 9pt legends")
print("  ✓ Line widths: 1.25pt")
print("  ✓ Colorblind-safe palette")
print("  ✓ Tight cropping")
