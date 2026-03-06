# Quick Start: Publication-Quality Plots

## Instant Usage

### Run Examples
```bash
cd "paper-summay/paper_submission/V8.3/statistical analyis"
python plotting_example.py
```

This generates 5 example figures demonstrating all improvements.

### Use in Your Code

#### 1. Simple Setup
```python
from visualization_config import configure_matplotlib
from enhanced_statistical_analysis import (
    style_publication_axes,
    save_figure_multi_format
)

# Configure once at the start
configure_matplotlib()
```

#### 2. Create Any Plot
```python
import matplotlib.pyplot as plt

# Your normal plotting code
fig, ax = plt.subplots(figsize=(7, 5), dpi=150)
ax.bar(['A', 'B', 'C'], [23, 45, 32])

# Apply publication styling (one line!)
style_publication_axes(ax, grid_axis='y')

# Save in both PNG and PDF
save_figure_multi_format(fig, "my_figure")
```

## Key Functions

### `style_publication_axes(ax)`
Instantly makes any plot publication-ready:
- Removes top/right spines
- Adds light grid behind data
- Cleans up tick marks

### `create_enhanced_boxplot(ax, data, positions, labels, colors)`
Beautiful boxplots with:
- Filled boxes
- Mean markers
- Clean styling

### `save_figure_multi_format(fig, name)`
Saves both PNG (viewing) and PDF (publication) automatically.

### `add_significance_bar(ax, x1, x2, y, p_value)`
Adds significance indicators (* / ** / *** / ns) between groups.

## What Changed?

### Before
```python
# Default matplotlib
fig, ax = plt.subplots()
ax.plot(x, y)
plt.savefig('figure.png')
```
Result: Basic plot with heavy borders, distracting grid

### After
```python
# Publication quality
fig, ax = plt.subplots(figsize=(7, 5), dpi=150)
ax.plot(x, y, linewidth=2, color='#0072B2')
style_publication_axes(ax, grid_axis='y')
ax.set_ylabel('Value', fontweight='bold')
save_figure_multi_format(fig, 'figure')
```
Result: Professional plot saved as both PNG and PDF

## Color Palette

Use these pre-defined colorblind-friendly colors:

```python
from visualization_config import PUBLICATION_CONFIG as C

C.COLOR_REGULATED  # '#0072B2' Blue
C.COLOR_BASELINE   # '#E69F00' Orange  
C.COLOR_POSITIVE   # '#009E73' Green
C.COLOR_NEGATIVE   # '#D55E00' Red
C.COLOR_NEUTRAL    # '#666666' Gray
```

## Checklist

When creating a publication figure:

```python
# ✓ High DPI
fig, ax = plt.subplots(figsize=(7, 5), dpi=150)

# ✓ Your plot
ax.plot(...) or ax.bar(...) or ax.boxplot(...)

# ✓ Clean styling
style_publication_axes(ax, grid_axis='y')

# ✓ Bold labels
ax.set_xlabel('...', fontweight='bold')
ax.set_ylabel('...', fontweight='bold')
ax.set_title('...', fontweight='bold', pad=15)

# ✓ Save both formats
save_figure_multi_format(fig, 'figure_name')
```

## Common Patterns

### Bar Chart
```python
fig, ax = plt.subplots(figsize=(7, 5), dpi=150)
ax.bar(categories, values, color='#0072B2', alpha=0.85, 
      edgecolor='0.3', linewidth=1.5)
style_publication_axes(ax, grid_axis='y')
ax.set_ylabel('Count', fontweight='bold')
save_figure_multi_format(fig, 'bar_chart')
```

### Boxplot
```python
from enhanced_statistical_analysis import create_enhanced_boxplot

fig, ax = plt.subplots(figsize=(6, 6), dpi=150)
bp = create_enhanced_boxplot(ax, [data1, data2], [1, 2],
                             ['Control', 'Treatment'],
                             ['#E69F00', '#0072B2'])
style_publication_axes(ax, grid_axis='y')
save_figure_multi_format(fig, 'boxplot')
```

### Line Plot
```python
fig, ax = plt.subplots(figsize=(7, 5), dpi=150)
ax.plot(x, y, linewidth=2, color='#0072B2', label='Data')
style_publication_axes(ax, grid_axis='both')
ax.legend(frameon=True, edgecolor='0.85')
save_figure_multi_format(fig, 'line_plot')
```

## File Sizes

Typical output sizes:
- PNG: ~100-300 KB (depends on complexity)
- PDF: ~50-150 KB (vector format)

PDFs stay sharp at any zoom level!

## Integration

### In Jupyter Notebooks
```python
%matplotlib inline
from visualization_config import configure_matplotlib
configure_matplotlib()

# Then use normally
fig, ax = plt.subplots(figsize=(7, 5), dpi=150)
# ... your plots ...
```

### In LaTeX Documents
```latex
\begin{figure}[htbp]
  \centering
  \includegraphics[width=0.8\textwidth]{figures/my_figure.pdf}
  \caption{My publication-quality figure}
  \label{fig:my_figure}
\end{figure}
```

Note: Use the PDF version in LaTeX for best quality!

## Help

- **Full documentation**: See `PLOTTING_IMPROVEMENTS.md`
- **Examples**: Run `python plotting_example.py`
- **Source code**: Check `enhanced_statistical_analysis.py`
- **Configuration**: See `visualization_config.py`

## Tips

1. **Always use high DPI**: `dpi=150` for screen, automatic 300 DPI for PDFs
2. **Bold labels**: Makes text readable at any size
3. **Colorblind safe**: Use the pre-defined palette
4. **Vector formats**: PDFs for publication, PNGs for presentations
5. **Consistent styling**: Use `style_publication_axes()` on every plot
6. **Test grayscale**: Print your figure in B&W to check clarity

---

**Quick Reference Card**

| Task | Code |
|------|------|
| Configure | `configure_matplotlib()` |
| Clean plot | `style_publication_axes(ax)` |
| Save dual format | `save_figure_multi_format(fig, 'name')` |
| Boxplot | `create_enhanced_boxplot(ax, data, ...)` |
| Significance | `add_significance_bar(ax, x1, x2, y, p)` |
| Colors | `C.COLOR_REGULATED`, `C.COLOR_BASELINE`, etc. |

**One-liner for any plot:**
```python
style_publication_axes(ax); save_figure_multi_format(fig, 'name')
```
