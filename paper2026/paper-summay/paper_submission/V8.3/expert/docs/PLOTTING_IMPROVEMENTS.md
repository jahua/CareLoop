# Publication-Quality Plotting Improvements

## Overview

The statistical analysis plotting system has been enhanced with best practices from leading matplotlib resources:
- [Publication-Quality Plots with Matplotlib](https://www.fschuch.com/en/blog/2025/07/05/publication-quality-plots-in-python-with-matplotlib/)
- [Matplotlib for Papers](https://github.com/jbmouret/matplotlib_for_papers)
- Tufte, E. R. (2001). *The Visual Display of Quantitative Information*

## Key Improvements

### 1. Minimize Ink (Tufte's Principle)

**Before:**
- Full plot borders with all four spines
- Heavy grid lines competing with data
- Prominent tick marks

**After:**
```python
# Top and right spines removed
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

# Lighter, cleaner remaining spines
ax.spines['left'].set_linewidth(0.8)
ax.spines['bottom'].set_linewidth(0.8)

# Remove tick marks, keep labels
ax.tick_params(axis='both', which='both', length=0, pad=6)
```

**Result:** Cleaner, more professional appearance that focuses attention on the data.

### 2. Vector Format Support

**Implementation:**
```python
# Save in both PNG (viewing) and PDF (publication)
save_figure_multi_format(fig, "figure_name", output_dir="figures", 
                        formats=['png', 'pdf'])
```

**Benefits:**
- PNG for quick viewing, presentations, and web display
- PDF for high-quality print and LaTeX inclusion
- Scalable graphics that maintain quality at any size
- No pixelation when zooming or printing

**File Output:**
```
figures/
??? 06_personality_dimensions.png  # For viewing
??? 06_personality_dimensions.pdf  # For publication
??? 07_personality_heatmap.png
??? 07_personality_heatmap.pdf
??? ...
```

### 3. Enhanced Boxplots

**New Features:**
```python
bp = create_enhanced_boxplot(
    ax,
    data=[data1, data2],
    positions=[1, 2],
    labels=['Baseline', 'Regulated'],
    colors=['#E69F00', '#0072B2'],
    show_means=True,      # Diamond markers for means
    show_outliers=True     # Subtle outlier styling
)
```

**Improvements:**
- ? Filled boxes with consistent colors
- ? Mean markers (white diamonds) in addition to medians
- ? Cleaner whiskers with appropriate line widths
- ? Subtle outlier points (semi-transparent)
- ? Statistical significance bars when applicable

### 4. Grid Styling

**Implementation:**
```python
# Grid always behind data
ax.grid(axis='y', color='0.92', linestyle='-', 
       linewidth=0.8, alpha=1.0, zorder=0)
ax.set_axisbelow(True)
```

**Key Points:**
- Grid color: `'0.92'` (very light gray) instead of default
- Positioned behind data using `zorder=0`
- Only on relevant axis (usually y-axis for bar charts)
- Consistent line width (0.8 pt)

### 5. Color Palette

**Current Implementation:**
Using the Okabe-Ito colorblind-friendly palette:

```python
COLOR_REGULATED = '#0072B2'  # Blue
COLOR_BASELINE = '#E69F00'   # Orange
COLOR_POSITIVE = '#009E73'   # Green
COLOR_NEGATIVE = '#D55E00'   # Red/Vermillion
COLOR_NEUTRAL = '#666666'    # Gray
```

**Why Okabe-Ito?**
- ? Distinguishable by people with color vision deficiency
- ? Print-safe (works in grayscale)
- ? Aesthetically pleasing
- ? Recommended by Nature, Science, and other journals

**Alternative Palettes Available:**
```python
colors = PlotStyler.create_color_palette(n_colors=5, palette_name='okabe_ito')
# Also available: 'wong', 'tol', 'paul_tol'
```

### 6. Typography

**Font Hierarchy:**
```python
FONT_SIZE_SMALL = 9     # Annotations, secondary labels
FONT_SIZE_BASE = 10     # Axis tick labels, legend
FONT_SIZE_MEDIUM = 11   # Axis labels
FONT_SIZE_LARGE = 12    # Subplot titles
FONT_SIZE_TITLE = 14    # Main figure title
```

**Fonts:**
- Primary: DejaVu Sans (always available)
- Fallbacks: Arial, Helvetica
- Sans-serif for all plots (cleaner, more modern)

### 7. Figure Dimensions

**Journal-Specific Sizing:**
```python
# Get appropriate size for target journal
figsize = get_figure_size_for_journal(
    journal='mdpi',  # or 'nature', 'science', 'plos', etc.
    columns=1,       # single column
    aspect=0.7       # height/width ratio
)

fig, ax = plt.subplots(figsize=figsize)
```

**Common Journal Widths:**
| Journal  | Single Column | Double Column |
|----------|--------------|---------------|
| Nature   | 89 mm        | 183 mm        |
| Science  | 56 mm        | 120 mm        |
| PLOS     | 83 mm        | 174 mm        |
| MDPI     | 85 mm        | 178 mm        |
| IEEE     | 88 mm        | 181 mm        |

### 8. Enhanced Legends

**Implementation:**
```python
legend = ax.legend(
    fontsize=C.FONT_SIZE_BASE,
    frameon=True,              # Frame visible but subtle
    edgecolor='0.85',          # Light gray border
    framealpha=0.95,           # Semi-transparent
    loc='upper left'
)
legend.get_frame().set_linewidth(1)
```

**Features:**
- Lighter frame that doesn't compete with data
- Semi-transparent background (0.95 alpha)
- Consistent with overall plot styling
- Positioned to avoid data occlusion

## New Utility Functions

### `style_publication_axes(ax, grid_axis='y', remove_spines=True)`
Apply all publication styling at once:
```python
style_publication_axes(ax, grid_axis='y', remove_spines=True)
```

### `add_significance_bar(ax, x1, x2, y, p_value, height=0.02)`
Add statistical significance indicators:
```python
add_significance_bar(ax, 1, 2, y_max + 0.5, p_value=0.023)
# Automatically displays: *, **, ***, ****, or 'ns'
```

### `save_figure_multi_format(fig, basename, output_dir, formats=['png', 'pdf'])`
Save in multiple formats efficiently:
```python
save_figure_multi_format(fig, "results", formats=['png', 'pdf', 'svg'])
```

### `create_enhanced_boxplot(...)`
Publication-quality boxplots in one call:
```python
bp = create_enhanced_boxplot(
    ax, data, positions, labels, colors,
    show_means=True, show_outliers=True
)
```

## Usage Examples

### Example 1: Simple Bar Chart

```python
fig, ax = plt.subplots(figsize=(7, 5), dpi=150)

# Your data
categories = ['A', 'B', 'C']
values = [23, 45, 32]

# Plot
bars = ax.bar(categories, values, color='#0072B2', 
             alpha=0.85, edgecolor='0.3', linewidth=1.5)

# Apply publication styling
style_publication_axes(ax, grid_axis='y')

# Labels
ax.set_ylabel('Response Count', fontweight='bold')
ax.set_title('Category Comparison', fontweight='bold', pad=15)

# Save
save_figure_multi_format(fig, "bar_chart_example")
```

### Example 2: Boxplot Comparison

```python
fig, ax = plt.subplots(figsize=(6, 5), dpi=150)

# Your data
data1 = np.random.normal(5, 1, 50)
data2 = np.random.normal(6, 1, 50)

# Create enhanced boxplot
bp = create_enhanced_boxplot(
    ax,
    data=[data1, data2],
    positions=[1, 2],
    labels=['Control', 'Treatment'],
    colors=['#E69F00', '#0072B2'],
    show_means=True
)

# Styling
style_publication_axes(ax, grid_axis='y')

# Add significance
from scipy.stats import ttest_ind
_, p_val = ttest_ind(data1, data2)
add_significance_bar(ax, 1, 2, max(data1.max(), data2.max()) + 0.5, p_val)

# Labels
ax.set_ylabel('Score', fontweight='bold')
ax.set_title('Treatment Effect', fontweight='bold', pad=15)

# Save
save_figure_multi_format(fig, "boxplot_example")
```

### Example 3: Multi-Panel Figure

```python
fig, axes = plt.subplots(1, 3, figsize=(12, 4), dpi=150)

for ax in axes:
    # Your plotting code
    ax.plot(x, y)
    
    # Apply consistent styling
    style_publication_axes(ax, grid_axis='both')
    
    # Labels
    ax.set_xlabel('Time', fontweight='bold')
    ax.set_ylabel('Value', fontweight='bold')

plt.tight_layout()
save_figure_multi_format(fig, "multi_panel_example")
```

## Before/After Comparison

### Before (Default Matplotlib):
- ? Heavy black borders on all four sides
- ? Dark, distracting grid lines
- ? Large tick marks
- ? Generic colors
- ? Only PNG output
- ? Inconsistent styling

### After (Publication Quality):
- ? Clean, minimal borders (left & bottom only)
- ? Light grid behind data
- ? No tick marks (labels only)
- ? Colorblind-friendly palette
- ? Vector format support (PDF, SVG)
- ? Consistent, professional styling

## Best Practices Summary

1. **Always use vector formats** (PDF/SVG) for publications
2. **Remove chartjunk** - only include elements that convey information
3. **Use colorblind-friendly palettes** - accessible to all readers
4. **Grid behind data** - data should be the focus
5. **Consistent styling** - use the same configuration across all figures
6. **Appropriate figure sizes** - match your target journal's requirements
7. **Clear labels** - bold, readable, appropriately sized
8. **Statistical rigor** - show medians, quartiles, and significance
9. **Transparency** - use alpha for overlapping elements
10. **Test in grayscale** - ensure figures work without color

## Checklist for Publication Figures

- [ ] Figure saved in vector format (PDF or SVG)
- [ ] Also saved in PNG for presentations/web
- [ ] Top and right spines removed
- [ ] Grid is light and behind data
- [ ] Using colorblind-friendly colors
- [ ] Font sizes appropriate for journal
- [ ] All text is legible
- [ ] Legend doesn't obscure data
- [ ] Statistical significance clearly marked
- [ ] Figure caption prepared (separate from plot)
- [ ] Tested appearance in grayscale
- [ ] File size reasonable (< 5 MB for raster)

## File Structure

```
statistical analyis/
??? enhanced_statistical_analysis.py  # Main analysis with improved plots
??? visualization_config.py          # Enhanced configuration
??? PLOTTING_IMPROVEMENTS.md         # This document
??? figures/
    ??? *.png                        # Raster versions (viewing)
    ??? *.pdf                        # Vector versions (publication)
```

## Resources

### References
1. Schuch, F. N. (2025). "Publication-Quality Plots in Python with Matplotlib"  
   https://www.fschuch.com/en/blog/2025/07/05/publication-quality-plots-in-python-with-matplotlib/

2. Mouret, J-B. "Creating publication-quality figures with matplotlib"  
   https://github.com/jbmouret/matplotlib_for_papers

3. Tufte, E. R. (2001). *The Visual Display of Quantitative Information* (2nd ed.)  
   Graphics Press.

4. Okabe, M., & Ito, K. (2008). "Color Universal Design"  
   https://jfly.uni-koeln.de/color/

### Additional Reading
- Rougier, N. P., et al. (2014). "Ten Simple Rules for Better Figures"  
  *PLOS Computational Biology*. https://doi.org/10.1371/journal.pcbi.1003833

- Crameri, F., et al. (2020). "The misuse of colour in science communication"  
  *Nature Communications*. https://doi.org/10.1038/s41467-020-19160-7

## Support

For questions or issues with the plotting improvements:
1. Check this documentation
2. Review the example code in `enhanced_statistical_analysis.py`
3. Consult the matplotlib documentation: https://matplotlib.org/
4. Review the source materials linked in References

---

**Last Updated:** January 2026  
**Version:** 1.0  
**Compatibility:** Python 3.7+, Matplotlib 3.3+
