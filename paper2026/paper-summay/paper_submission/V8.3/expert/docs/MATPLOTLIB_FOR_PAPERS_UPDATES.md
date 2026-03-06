# matplotlib_for_papers Specific Improvements

## Overview

Additional refinements applied based on specific techniques from [matplotlib_for_papers](https://github.com/jbmouret/matplotlib_for_papers) guide by Jean-Baptiste Mouret.

## Key Updates

### 1. Spine Offsetting ?

**From matplotlib_for_papers guide:**
```python
# Offset spines outward for cleaner appearance
for spine in ax.spines.values():
    spine.set_position(('outward', 5))
```

**Implementation:**
- Added `offset_spines` parameter to `style_publication_axes()`
- Spines are now offset 5 points outward
- Creates more breathing room between data and frame

**Visual Impact:** Frame doesn't compete with data points near edges.

### 2. Grid Styling (Exact Match)

**From guide:**
```python
ax.grid(axis='y', color="0.9", linestyle='-', linewidth=1)
ax.set_axisbelow(True)
```

**Changed:**
- Grid color: `'0.92'` ? `'0.9'` (matches guide exactly)
- Grid linewidth: `0.8` ? `1` (matches guide)

### 3. Tick Direction

**From guide:**
```python
ax.get_xaxis().tick_bottom()
ax.get_yaxis().tick_left()
ax.tick_params(axis='x', direction='out')
ax.tick_params(axis='y', length=0)
```

**Implementation:**
- X-axis ticks point outward (length=3)
- Y-axis ticks removed (length=0)  
- More explicit tick positioning

### 4. Statistical Significance Bars

**From guide's boxplot example:**
```python
ax.annotate("", xy=(x1, y), xycoords='data',
           xytext=(x2, y), textcoords='data',
           arrowprops=dict(arrowstyle="-", ec='#aaaaaa',
                         connectionstyle="bar,fraction=0.2"))
```

**Implementation:**
- Replaced manual line drawing with `annotate()` method
- Uses `connectionstyle="bar,fraction=0.2"` for proper bar shape
- Stars displayed as: `*`, `**`, `***`, `****`, or `-` (not 'ns')

### 5. Color Scheme

**Added matplotlib_for_papers colors:**
```python
COLORS_MATPLOTLIB_PAPERS = {
    "blue": "#006BB2",      # From guide examples
    "red": "#B22400",       # From guide examples
    "green": "#009E73",     # Colorblind-safe
    "orange": "#E69F00",    # Colorblind-safe
}
```

These match the exact colors used in the guide's examples.

### 6. Minimalist Line Plots

**New function:** `style_line_plot_minimalist()`

Based on guide's "Minimizing ink" section:
```python
# Option 1: Remove frame entirely (frameon=0 style)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['left'].set_visible(False)
ax.spines['bottom'].set_visible(False)
```

**Use case:** Time series, evolution plots where frame is unnecessary.

### 7. Connecting Lines in Paired Plots

**From guide's variance plots:**
- Individual lines: subtle, thin (`linewidth=0.5`, `alpha=0.3`)
- Mean line: bold, prominent (`linewidth=2`, `color='black'`)
- Points: simpler (no white edge), slightly transparent

**Before:**
```python
ax.plot([0, 1], [y1, y2], color='0.7', alpha=0.4, linewidth=0.8)
ax.scatter(x, y, edgecolors='white', linewidths=1)
```

**After (matplotlib_for_papers style):**
```python
ax.plot([0, 1], [y1, y2], color='0.75', alpha=0.3, linewidth=0.5)
ax.scatter(x, y, s=40, alpha=0.6)  # No edge
```

## Function Updates

### Updated: `style_publication_axes()`

**New parameters:**
- `offset_spines=True` - Offset spines outward (guide technique)

**Behavior changes:**
- Grid matches guide exactly (color='0.9', linewidth=1)
- Explicit tick positioning with `get_xaxis().tick_bottom()`
- X-axis ticks visible but short (length=3)
- Spine offsetting for cleaner appearance

### Updated: `add_significance_bar()`

**Changes:**
- Uses `annotate()` method (guide approach)
- Proper bar connection style
- Stars: `-` for non-significant (not 'ns')

### New: `style_line_plot_minimalist()`

**Purpose:** Minimalist styling for time series/evolution plots

**Parameters:**
- `remove_frame=True` - Remove all spines (frameon=0 style)

**Use when:** Frame adds no information to the plot.

## Visual Comparison

### Spine Offset Effect

**Before (no offset):**
```
???????????????
? •  •  •  •  ?  <- Data touches frame
? •  •  •  •  ?
???????????????
```

**After (5pt offset):**
```
   •  •  •  •     <- Data has breathing room
   •  •  •  •
?????????????     <- Frame offset outward
```

### Grid Comparison

**Before:** 0.92 gray, 0.8pt line  
**After:** 0.9 gray, 1pt line (slightly more visible, matches guide)

### Significance Bar Comparison

**Before (manual lines):**
```python
ax.plot([x1, x2], [y, y], ...)  # Horizontal
ax.plot([x1, x1], [y1, y2], ...)  # Vertical left
ax.plot([x2, x2], [y1, y2], ...)  # Vertical right
```

**After (annotate):**
```python
ax.annotate("", xy=(x1, y), xytext=(x2, y),
           arrowprops=dict(..., connectionstyle="bar,fraction=0.2"))
```

More elegant, handles curve automatically.

## Usage Examples

### Example 1: Publication-quality line plot

```python
fig, ax = plt.subplots(figsize=(7, 5), dpi=150)

# Your data
ax.plot(x, y, linewidth=2, color=COLORS_MATPLOTLIB_PAPERS['blue'])

# Apply guide-style formatting
style_publication_axes(ax, grid_axis='y', offset_spines=True)

# Labels
ax.set_xlabel('Time', fontweight='bold')
ax.set_ylabel('Fitness', fontweight='bold')

# Save
save_figure_multi_format(fig, 'evolution_plot')
```

### Example 2: Minimalist time series

```python
fig, ax = plt.subplots(figsize=(7, 4), dpi=150)

# Multiple time series
for series in data:
    ax.plot(x, series, linewidth=1.5, alpha=0.7)

# Minimalist style (no frame)
style_line_plot_minimalist(ax, remove_frame=True)

# Minimal labels
ax.set_xlabel('Generation')
ax.set_ylabel('Fitness')

save_figure_multi_format(fig, 'time_series')
```

### Example 3: Boxplot with significance

```python
from scipy.stats import mannwhitneyu

fig, ax = plt.subplots(figsize=(6, 6), dpi=150)

# Data
bp = create_enhanced_boxplot(ax, [control, treatment], [1, 2],
                             ['Control', 'Treatment'],
                             [COLORS_MATPLOTLIB_PAPERS['red'],
                              COLORS_MATPLOTLIB_PAPERS['blue']])

# Style with offset spines
style_publication_axes(ax, grid_axis='y', offset_spines=True)

# Statistical test (Mann-Whitney U, as recommended in guide)
_, p_value = mannwhitneyu(control, treatment)
p_value = p_value * 2  # Two-tailed test

# Add significance bar (guide style)
y_max = max(control.max(), treatment.max())
add_significance_bar(ax, 1, 2, y_max + 0.8, p_value)

save_figure_multi_format(fig, 'comparison')
```

## Best Practices from Guide

### 1. Use Median, Not Mean (for algorithms)

From guide:
> "Using the mean + standard deviation assumes that your data are normally distributed. 
> This assumption is usually wrong in evolutionary computation."

**Recommendation:** Use median + quartiles (25th/75th percentiles)

### 2. Mann-Whitney U Test (not t-test)

From guide:
> "A good non-parametric alternative to the t-test is the Mann-Whitney U-test"

**Implementation:**
```python
from scipy.stats import mannwhitneyu
z, p = mannwhitneyu(data1, data2)
p_value = p * 2  # Two-tailed test
```

### 3. Minimize Ink (Tufte)

From guide:
> "Maximize the data/ink ratio. In other words, minimize the visual clutter, 
> or remove everything that is not useful to understand the data."

**Applied:**
- Removed top/right spines
- Light grid (0.9 gray)
- Minimal tick marks
- Offset spines

### 4. Vector Formats

From guide:
> "pdf (vector format, useful for LaTeX papers compiled with pdflatex: 
> no problem of resolution)"

**Implementation:** All figures save as both PNG and PDF.

### 5. Color Choice

From guide examples:
- Avoid pure red/blue (#FF0000, #0000FF)
- Use specific hex codes: #B22400, #006BB2
- Consider colorblind accessibility

**Implementation:** Added COLORS_MATPLOTLIB_PAPERS dictionary.

## Key Differences from Standard Matplotlib

| Aspect | Standard | matplotlib_for_papers | Our Implementation |
|--------|----------|----------------------|-------------------|
| Spines | All 4 visible | Top/right removed, left/bottom offset | ? Implemented |
| Grid | Dark (0.15), in front | Light (0.9), behind | ? Implemented |
| Ticks | All sides, 4pt | Bottom/left only, variable | ? Implemented |
| Colors | Default cycle | Specific hex codes | ? Provided |
| Frame | Always on | Sometimes off (frameon=0) | ? Function available |
| Significance | Manual | annotate() method | ? Implemented |

## Files Updated

1. **enhanced_statistical_analysis.py**
   - Updated `style_publication_axes()` with spine offsetting
   - Updated `add_significance_bar()` with annotate method
   - Added `style_line_plot_minimalist()` function
   - Added `COLORS_MATPLOTLIB_PAPERS` dictionary
   - Updated paired plot styling (thinner connecting lines)

2. **This document**
   - Documents specific matplotlib_for_papers techniques
   - Provides guide-aligned examples
   - Explains rationale for each change

## Testing

To verify the improvements match the guide:

```bash
cd "paper-summay/paper_submission/V8.3/statistical analyis"
python plotting_example.py
```

Check generated figures for:
1. ? Offset spines (5pt outward)
2. ? Light grid (0.9 gray)
3. ? Minimal tick marks
4. ? Clean significance bars
5. ? Subtle connecting lines

## References

1. **Primary source:**  
   Mouret, J-B. "Creating publication-quality figures with Matplotlib"  
   https://github.com/jbmouret/matplotlib_for_papers

2. **Key papers using this style:**
   - Clune et al. (2013). "The evolutionary origins of modularity." *Proc. Royal Society B*
   - Tonelli & Mouret (2013). "On the relationships between generative encodings..." *PLOS ONE*

3. **Design principles:**
   - Tufte, E. R. (2001). *The Visual Display of Quantitative Information*

## Summary

These updates ensure our plots match the **exact style** used in the matplotlib_for_papers guide, incorporating:

- ? Spine offsetting technique
- ? Exact grid styling (color='0.9', linewidth=1)
- ? Proper tick configuration
- ? annotate() for significance bars
- ? Guide's specific hex colors
- ? Minimalist option for frameless plots
- ? Subtle styling for connecting lines

All improvements maintain backward compatibility while providing guide-aligned alternatives.

---

**Version:** 1.1 (matplotlib_for_papers aligned)  
**Date:** January 18, 2026  
**Status:** Production ready ?
