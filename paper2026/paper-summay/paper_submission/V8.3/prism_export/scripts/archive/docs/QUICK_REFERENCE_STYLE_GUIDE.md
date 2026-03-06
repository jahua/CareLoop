# Quick Reference: FIGURE_STYLE_GUIDE.md Compliance

**Quick lookup for figure generation with style guide compliance**

---

## ⚡ Quick Start

```python
from visualization_config import configure_matplotlib, save_figure_multi_format, PUBLICATION_CONFIG as C

# 1. Apply style guide
configure_matplotlib(apply_style_guide=True)

# 2. Create figure (use MDPI column widths)
fig, ax = plt.subplots(figsize=(C.FIGURE_WIDTH_SINGLE, 4.0))  # 1-column
# OR
fig, ax = plt.subplots(figsize=(C.FIGURE_WIDTH_DOUBLE, 5.0))  # 2-column

# 3. Plot with correct settings
ax.plot(x, y, linewidth=C.LINE_WIDTH, color=C.COLOR_REGULATED)
ax.set_xlabel('Label', fontsize=C.FONT_SIZE_AXIS_LABELS)
ax.tick_params(labelsize=C.FONT_SIZE_TICK_LABELS)
ax.legend(fontsize=C.FONT_SIZE_LEGEND)

# 4. Save (both PNG and PDF)
save_figure_multi_format(fig, 'figure_name', high_res=True)  # 600 DPI for line art
```

---

## 📊 Style Guide Requirements at a Glance

| Requirement | Value | Config Variable |
|-------------|-------|-----------------|
| **Format** | PDF + PNG | `formats=['png', 'pdf']` |
| **DPI (standard)** | 300 | `C.DPI` |
| **DPI (line art)** | 600 | `C.DPI_LINE_ART` |
| **1-col width** | 85mm = 3.35" | `C.FIGURE_WIDTH_SINGLE` |
| **2-col width** | 170mm = 6.69" | `C.FIGURE_WIDTH_DOUBLE` |
| **Min px (1-col)** | ≥2000 px | @ 600 DPI = 2010 px ✓ |
| **Min px (2-col)** | ≥4000 px | @ 600 DPI = 4014 px ✓ |
| **Axis labels** | 8-9 pt | `C.FONT_SIZE_AXIS_LABELS = 9` |
| **Tick labels** | 8-9 pt | `C.FONT_SIZE_TICK_LABELS = 8` |
| **Legend** | 9-10 pt | `C.FONT_SIZE_LEGEND = 9` |
| **Line width** | 1.0-1.5 pt | `C.LINE_WIDTH = 1.25` |
| **Axes width** | 1.0 pt | `C.LINE_WIDTH_AXES = 1.0` |
| **Grid width** | 0.5 pt | `C.LINE_WIDTH_GRID = 0.5` |

---

## 🎨 Color Palette (Okabe-Ito)

```python
C.COLOR_REGULATED  = '#0072B2'  # Blue
C.COLOR_BASELINE   = '#E69F00'  # Orange
C.COLOR_POSITIVE   = '#009E73'  # Green
C.COLOR_NEGATIVE   = '#D55E00'  # Red
C.COLOR_NEUTRAL    = '#666666'  # Gray
```

---

## 📏 Figure Sizes

```python
# Single column (85mm)
fig, ax = plt.subplots(figsize=(3.35, 4.0))

# Double column (170mm)
fig, ax = plt.subplots(figsize=(6.69, 5.0))

# Or use templates
from visualization_config import FigureTemplates
fig, ax = FigureTemplates.create_single_panel('medium')
fig, axes = FigureTemplates.create_double_panel('tall')
```

---

## 💾 Saving Figures

```python
# Standard resolution (300 DPI)
save_figure_multi_format(fig, 'my_figure')

# High resolution for line art/text (600 DPI)
save_figure_multi_format(fig, 'diagram', high_res=True)

# Custom formats
save_figure_multi_format(fig, 'plot', formats=['png', 'pdf', 'svg'])
```

---

## ✅ Verify Resolution

```python
from visualization_config import verify_figure_resolution

result = verify_figure_resolution(fig, target_width_px=2000, dpi=600)
print(f"Width: {result['width_px']} px")
print(f"Meets requirement: {result['meets_requirement']}")
```

---

## 🎯 Common Scenarios

### Scenario 1: Statistical Plot (1-column)
```python
configure_matplotlib(apply_style_guide=True)
fig, ax = plt.subplots(figsize=(C.FIGURE_WIDTH_SINGLE, 4.0))
ax.plot(x, y, linewidth=C.LINE_WIDTH)
save_figure_multi_format(fig, '06_personality_dimensions')
```

### Scenario 2: Text-Heavy Diagram (2-column)
```python
configure_matplotlib(apply_style_guide=True)
fig, ax = plt.subplots(figsize=(C.FIGURE_WIDTH_DOUBLE, 6.0))
# ... create diagram ...
save_figure_multi_format(fig, 'system_architecture', high_res=True)  # 600 DPI
```

### Scenario 3: Multi-Panel Figure
```python
configure_matplotlib(apply_style_guide=True)
fig, axes = plt.subplots(2, 2, figsize=(C.FIGURE_WIDTH_DOUBLE, 8.0))
# ... create panels ...
save_figure_multi_format(fig, 'multi_panel', high_res=True)
```

---

## 🔍 Priority Figures to Re-export

Based on FIGURE_STYLE_GUIDE.md "Quick triage":

**Low file size = may need higher resolution:**

1. `07_personality_heatmap.png` (94 KB) - Re-export at 600 DPI
2. `08_weighted_scores.png` (149 KB)
3. `09_total_score_boxplot.png` (111 KB)
4. `10_selective_enhancement_paired.png` (150 KB)
5. `11_metric_composition.png` (121 KB)

**Action:**
```python
save_figure_multi_format(fig, basename, high_res=True)
```

---

## 📋 Checklist

Before saving any figure, verify:

- [ ] Using `configure_matplotlib(apply_style_guide=True)`
- [ ] Figure width: 3.35" (1-col) or 6.69" (2-col)
- [ ] Font sizes: 8-9 pt labels, 9-10 pt legend
- [ ] Line widths: 1.0-1.5 pt
- [ ] Colors from colorblind-safe palette
- [ ] Saving both PNG and PDF
- [ ] Using `high_res=True` for text-heavy plots
- [ ] Tight cropping enabled (automatic)

---

## 🚀 Complete Example

```python
#!/usr/bin/env python3
import matplotlib.pyplot as plt
import numpy as np
from visualization_config import (
    configure_matplotlib, 
    save_figure_multi_format,
    verify_figure_resolution,
    PUBLICATION_CONFIG as C
)

# 1. Configure matplotlib
configure_matplotlib(apply_style_guide=True)

# 2. Create data
x = np.linspace(0, 10, 100)
y1 = np.sin(x)
y2 = np.cos(x)

# 3. Create figure (MDPI single column)
fig, ax = plt.subplots(figsize=(C.FIGURE_WIDTH_SINGLE, 4.0))

# 4. Plot with correct settings
ax.plot(x, y1, linewidth=C.LINE_WIDTH, color=C.COLOR_REGULATED, label='Regulated')
ax.plot(x, y2, linewidth=C.LINE_WIDTH, color=C.COLOR_BASELINE, label='Baseline')

# 5. Format
ax.set_xlabel('Time (s)', fontsize=C.FONT_SIZE_AXIS_LABELS)
ax.set_ylabel('Amplitude', fontsize=C.FONT_SIZE_AXIS_LABELS)
ax.tick_params(labelsize=C.FONT_SIZE_TICK_LABELS)
ax.legend(fontsize=C.FONT_SIZE_LEGEND, frameon=True)
ax.grid(True, alpha=0.3, linewidth=C.LINE_WIDTH_GRID)

# 6. Verify resolution (optional)
result = verify_figure_resolution(fig, target_width_px=2000, dpi=600)
print(f"Resolution: {result['width_px']} × {result['height_px']} px")

# 7. Save (both PNG at 600 DPI and PDF vector)
save_figure_multi_format(fig, 'example_plot', high_res=True, verbose=True)

print("✓ Figure saved successfully!")
```

---

**Quick Reference Version:** 1.0  
**Last Updated:** February 1, 2026  
**See also:** STYLE_GUIDE_APPLIED.md (detailed documentation)
