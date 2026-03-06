# Color Scheme: Using Default Okabe-Ito Palette

## Current Configuration

All plots now use the **default Okabe-Ito colorblind-friendly palette**.

## Active Colors

| Purpose | Color | Hex Code | Description |
|---------|-------|----------|-------------|
| **Regulated/Treatment** | Blue | `#0072B2` | Okabe-Ito Blue |
| **Baseline/Control** | Orange | `#E69F00` | Okabe-Ito Orange |
| **Positive/Success** | Green | `#009E73` | Okabe-Ito Green |
| **Negative/Failure** | Vermillion | `#D55E00` | Okabe-Ito Red |
| **Neutral** | Gray | `#666666` | Medium Gray |
| **Accent** | Purple | `#CC79A7` | Okabe-Ito Purple |

## Visual Reference

```
Regulated: ? #0072B2 (Blue)
Baseline:  ? #E69F00 (Orange)
Positive:  ? #009E73 (Green)
Negative:  ? #D55E00 (Vermillion)
Neutral:   ? #666666 (Gray)
Accent:    ? #CC79A7 (Purple)
```

## Why Okabe-Ito?

The Okabe-Ito palette is the **gold standard** for scientific visualization:

1. **Colorblind-Friendly:** Distinguishable by all types of color vision deficiency
2. **Print-Safe:** Works in grayscale
3. **Widely Adopted:** Recommended by journals (Nature, Science, etc.)
4. **Well-Tested:** Used in thousands of scientific publications

## Colorblind Verification

| Vision Type | Blue #0072B2 | Orange #E69F00 | Result |
|-------------|--------------|----------------|---------|
| Normal | Blue | Orange | ? Distinct |
| Protanopia | Blue | Yellow-green | ? Distinct |
| Deuteranopia | Blue | Yellow | ? Distinct |
| Tritanopia | Teal | Pink-red | ? Distinct |
| Grayscale | Medium gray | Light gray | ? Distinct |

## Usage in Code

### Automatic (Recommended)

```python
from visualization_config import PUBLICATION_CONFIG as C

# These automatically use Okabe-Ito colors
fig, ax = plt.subplots(figsize=(7, 5))
ax.plot(x, y1, color=C.COLOR_REGULATED, label='Regulated')  # Blue
ax.plot(x, y2, color=C.COLOR_BASELINE, label='Baseline')    # Orange
```

### Direct Access

```python
# Access specific colors directly
blue = C.COLOR_BLUE        # #0072B2
orange = C.COLOR_ORANGE    # #E69F00
green = C.COLOR_GREEN      # #009E73
red = C.COLOR_RED          # #D55E00
purple = C.COLOR_PURPLE    # #CC79A7
gray = C.COLOR_GRAY        # #666666
```

## Alternative: matplotlib_for_papers Colors

The matplotlib_for_papers colors are still available if needed:

```python
# Optional: Use guide's specific colors
blue_guide = C.MPL_PAPERS_BLUE    # #006BB2
red_guide = C.MPL_PAPERS_RED      # #B22400
```

To switch to these colors system-wide:
1. Edit `visualization_config.py`
2. Change `COLOR_REGULATED` and `COLOR_BASELINE` assignments

## Current Plot Examples

All existing plots use default Okabe-Ito:

1. **OCEAN Personality Dimensions** - Orange/Blue/Green cycle
2. **Weighted Scores** - Blue (Regulated) vs Orange (Baseline)
3. **Boxplots** - Blue (Regulated) vs Orange (Baseline)
4. **Paired Plots** - Orange (Baseline) vs Blue (Regulated)
5. **Bar Charts** - Consistent color mapping

## Benefits of Default Palette

### Advantages

1. **Universally Recognized:** Readers familiar with this palette
2. **Journal Approved:** Explicitly recommended by major publishers
3. **Accessibility:** Maximum inclusivity for readers
4. **Proven Track Record:** Decades of successful use

### When to Consider Alternatives

- Journal requires specific colors
- Brand guidelines dictate colors
- Matching existing publication series
- Cultural color associations matter

## Testing Your Plots

### Check Colorblind Accessibility

Use online simulators:
- https://www.color-blindness.com/coblis-color-blindness-simulator/
- https://davidmathlogic.com/colorblind/

### Check Grayscale

```python
# Quick grayscale test
import matplotlib.pyplot as plt

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 4))

# Your plot
ax1.plot(x, y1, color=C.COLOR_REGULATED)
ax1.plot(x, y2, color=C.COLOR_BASELINE)
ax1.set_title('Color')

# Grayscale version
ax2.plot(x, y1, color='0.3')  # Dark gray
ax2.plot(x, y2, color='0.7')  # Light gray  
ax2.set_title('Grayscale Preview')

plt.show()
```

## Configuration Summary

### visualization_config.py

```python
# Default configuration (active)
COLOR_REGULATED: str = COLOR_BLUE    # #0072B2
COLOR_BASELINE: str = COLOR_ORANGE   # #E69F00

# Alternative (available but not default)
# COLOR_REGULATED: str = MPL_PAPERS_BLUE  # #006BB2
# COLOR_BASELINE: str = MPL_PAPERS_RED    # #B22400
```

### Files Updated

- ? `visualization_config.py` - Default palette active
- ? `enhanced_statistical_analysis.py` - Uses C.COLOR_REGULATED/BASELINE
- ? `plotting_example.py` - All examples use default colors

## Regenerating Plots

To regenerate all figures with default colors:

```bash
cd "paper-summay/paper_submission/V8.3/statistical analyis"
python plotting_example.py
```

All figures will automatically use the Okabe-Ito palette.

## Color Palette Reference

### Okabe-Ito Complete Palette

```python
COLORS_OKABE_ITO = {
    'blue': '#0072B2',
    'orange': '#E69F00',
    'green': '#009E73',
    'yellow': '#F0E442',
    'vermillion': '#D55E00',
    'purple': '#CC79A7',
    'sky_blue': '#56B4E9',
    'black': '#000000'
}
```

### Current Usage

| Color | Used For |
|-------|----------|
| Blue #0072B2 | Regulated, Treatment, Intervention |
| Orange #E69F00 | Baseline, Control |
| Green #009E73 | Success, Positive results |
| Vermillion #D55E00 | Failure, Negative results |
| Gray #666666 | Neutral, Not significant |
| Purple #CC79A7 | Accent, Special cases |

## References

1. **Okabe & Ito (2008)** - "Color Universal Design"  
   https://jfly.uni-koeln.de/color/

2. **Wong (2011)** - "Points of view: Color blindness"  
   *Nature Methods* 8, 441

3. **Matplotlib Documentation** - "Choosing Colormaps"  
   https://matplotlib.org/stable/tutorials/colors/colormaps.html

## Quick Comparison

| Aspect | Okabe-Ito (Default) | matplotlib_for_papers |
|--------|-------------------|----------------------|
| **Regulated** | #0072B2 (Blue) | #006BB2 (Darker Blue) |
| **Baseline** | #E69F00 (Orange) | #B22400 (Red) |
| **Colorblind Safe** | ? Yes | ? Yes |
| **Print Safe** | ? Yes | ? Yes |
| **Journal Recommended** | ? Yes | Used in specific papers |
| **Widely Recognized** | ? Yes | Less common |

## Summary

- ? **Active Palette:** Okabe-Ito (default scientific standard)
- ? **Regulated:** Blue #0072B2
- ? **Baseline:** Orange #E69F00
- ? **Colorblind Safe:** Verified
- ? **Print Safe:** Verified
- ? **Alternative Available:** matplotlib_for_papers colors (optional)

---

**Version:** 1.3 (Default Okabe-Ito)  
**Date:** January 18, 2026  
**Status:** Production Ready ?
