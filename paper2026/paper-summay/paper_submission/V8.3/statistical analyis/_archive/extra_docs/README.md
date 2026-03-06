# Statistical Analysis and Visualization Pipeline

**Version 2.0** - Unified, Publication-Ready System

---

## ?? Overview

This directory contains a **completely reorganized and streamlined** statistical analysis pipeline for the Personality-Adaptive Conversational AI study. All visualizations follow publication standards (MDPI, IEEE, Nature) with unified styling, colorblind-friendly palettes, and 300 DPI resolution.

### Key Improvements in V2.0

? **Unified Configuration** - Single source of truth for all visual styling  
? **Reduced Redundancy** - Eliminated overlapping plots (11 ? 7 essential figures)  
? **Modular Design** - Core analysis + optional extensions  
? **Publication Standards** - MDPI/IEEE/Nature compliant  
? **Consistent Styling** - Unified color schemes and typography

---

## ?? Directory Structure

```
statistical analyis/
??? Core Scripts (NEW - Use These!)
?   ??? visualization_config.py       ? Unified publication standards
?   ??? master_analysis.py            ? Main analysis pipeline
?   ??? create_diagrams.py            ? System architecture figures
?   ??? personality_analysis.py       ? Optional: OCEAN analysis
?
??? Data Files
?   ??? data/                          Individual CSV files (A-1 to B-5)
?   ??? merged/
?   ?   ??? regulated.csv              Merged regulated data
?   ?   ??? baseline.csv               Merged baseline data
?   ??? *.csv                          Analysis results
?
??? Generated Figures
?   ??? figures/                       Publication-ready visualizations
?       ??? 01_performance_comparison.png
?       ??? 02_effect_sizes.png
?       ??? 03_personality_needs.png
?       ??? 04_sample_quality.png
?       ??? 05_personality_profiles.png   (optional)
?       ??? 06_system_architecture.png
?       ??? 07_study_workflow.png
?
??? Legacy Scripts (Keep for Reference)
?   ??? statistical_analysis.py        Original version
?   ??? statistical_analysis_publication.py
?   ??? enhanced_statistical_analysis.py
?   ??? create_system_diagrams.py
?
??? Documentation
    ??? README.md                      ? This file
    ??? REORGANIZATION_SUMMARY.md      Change documentation
    ??? ANALYSIS_GUIDE.md              Original guide
```

---

## ?? Quick Start

### Prerequisites

```bash
pip install pandas numpy matplotlib seaborn scipy
```

### Basic Usage

Run the complete analysis pipeline:

```bash
# Navigate to directory
cd "statistical analyis"

# 1. Core statistical analysis (REQUIRED)
python3 master_analysis.py

# 2. System diagrams (REQUIRED)
python3 create_diagrams.py

# 3. Optional: Extended personality analysis
python3 personality_analysis.py
```

This generates **7 publication-ready figures** in `./figures/`.

---

## ?? Generated Figures

### Core Figures (Required for Paper)

| Figure | File | Description | Priority |
|--------|------|-------------|----------|
| **1** | `01_performance_comparison.png` | Regulated vs Baseline across all metrics | HIGH |
| **2** | `02_effect_sizes.png` | Cohen's d with interpretation guidelines | HIGH |
| **3** | `03_personality_needs.png` | Primary outcome (focused visualization) | HIGH |
| **4** | `04_sample_quality.png` | Sample distribution and completeness | MEDIUM |
| **6** | `06_system_architecture.png` | System pipeline diagram | HIGH |
| **7** | `07_study_workflow.png` | Research methodology flowchart | HIGH |

### Optional Figure (Supplementary)

| Figure | File | Description | Priority |
|--------|------|-------------|----------|
| **5** | `05_personality_profiles.png` | OCEAN dimension distributions | LOW |

### Removed as Redundant

- ? `02_missing_data_heatmap.png` - Covered in sample quality
- ? `05_percentage_improvement.png` - Redundant with effect sizes
- ? `06-09_extended_analysis.png` - Consolidated into optional module
- ? `10-11_system_diagrams.png` - Renumbered to 06-07

---

## ?? Publication Standards

All figures comply with:

### Resolution & Format
- **DPI:** 300 (publication standard)
- **Format:** PNG with lossless compression
- **Dimensions:** A4-optimized (7-10 inches width)

### Typography
- **Font:** Arial/Helvetica (sans-serif)
- **Sizes:** 8-12pt (readable when embedded)
- **Weight:** Bold for titles, labels

### Colors (Colorblind-Friendly)
- **Regulated:** `#0173B2` (Blue)
- **Baseline:** `#DE8F05` (Orange)
- **Positive:** `#029E73` (Green)
- **Negative:** `#D55E00` (Red)

All colors tested with:
- Deuteranopia simulation
- Protanopia simulation
- Grayscale conversion

### Grid & Style
- White background with light gray grid
- Spine removal (top/right)
- Consistent error bar styling

---

## ?? Statistical Methods

### Descriptive Statistics
- Mean, SD, 95% confidence intervals
- Sample size reporting

### Effect Sizes
- Cohen's d (standardized mean difference)
- Interpretation: |d| < 0.2 (negligible), 0.2-0.5 (small), 0.5-0.8 (medium), ?0.8 (large)

### Inferential Tests
- Independent samples t-tests
- **Note:** For context only; results from simulated data

---

## ?? Customization

### Modifying Visual Style

Edit `visualization_config.py`:

```python
# Change colors
PUBLICATION_CONFIG.COLOR_REGULATED = '#YOUR_COLOR'

# Adjust DPI
PUBLICATION_CONFIG.DPI = 600  # For higher resolution

# Modify font sizes
PUBLICATION_CONFIG.FONT_SIZE_BASE = 10
```

### Adding New Figures

Use provided templates:

```python
from visualization_config import FigureTemplates, save_figure

# Create figure
fig, ax = FigureTemplates.create_single_panel()

# ... your plotting code ...

# Save with standards
save_figure(fig, 'my_new_figure', 'figures')
```

---

## ?? Key Results Summary

### Primary Outcome
- **Metric:** Personality Needs Addressed
- **Regulated:** 100.0% (59/59)
- **Baseline:** 8.6% (5/58)
- **Effect Size:** Cohen's d = 4.58 (Very Large)
- **Improvement:** +91.4 percentage points

### Secondary Outcomes
- **Emotional Tone:** No difference (both 100%)
- **Relevance:** Negligible difference (d = 0.18)
- **Detection Accuracy:** 100% (58/58 valid)
- **Regulation Effectiveness:** 100% (59/59)

---

## ?? Migration from Old Scripts

If you were using the old scripts:

| Old Script | New Equivalent | Action |
|------------|----------------|--------|
| `statistical_analysis.py` | `master_analysis.py` | Replace |
| `statistical_analysis_publication.py` | `master_analysis.py` | Replace |
| `enhanced_statistical_analysis.py` | `personality_analysis.py` | Optional |
| `create_system_diagrams.py` | `create_diagrams.py` | Replace |

**Migration steps:**
1. Backup your `figures/` directory
2. Run `master_analysis.py` to regenerate core figures
3. Run `create_diagrams.py` for architecture diagrams
4. Compare outputs with backups
5. Update manuscript figure references

---

## ?? For Manuscript Integration

### Methods Section

```markdown
Statistical Analysis: Descriptive statistics (means, standard deviations, 
95% confidence intervals) were calculated for all evaluation metrics. 
Effect sizes (Cohen's d) quantified the magnitude of differences between 
regulated and baseline conditions. All visualizations adhere to journal 
standards (300 DPI, colorblind-friendly palettes).
```

### Results Section

```markdown
Personality-adaptive regulation produced a very large effect on addressing 
personality-specific needs (Cohen's d = 4.58, 95% CI: [see Figure 2]), 
with the regulated condition achieving 100% success compared to 8.6% in 
baseline (Figure 3). Both conditions maintained equivalent performance on 
general conversational quality metrics (emotional tone, relevance).
```

### Figure Captions

See `FIGURE_CAPTIONS.md` for publication-ready captions.

---

## ?? Troubleshooting

### Import Errors
```bash
# If you get "ModuleNotFoundError: No module named 'visualization_config'"
# Make sure you're running scripts from the 'statistical analyis' directory
cd "statistical analyis"
python3 master_analysis.py
```

### Missing Data Files
```bash
# If CSV files are missing, regenerate from Excel:
python3 convert_excel_to_csv.py
python3 merge_regulated.py
python3 merge_baseline.py
```

### Figure Not Generating
- Check `figures/` directory exists (created automatically)
- Verify data files in `merged/` directory
- Check console for error messages

---

## ?? Support

For questions or issues:
1. Check this README
2. Review `REORGANIZATION_SUMMARY.md` for detailed changes
3. Examine inline documentation in scripts

---

## ?? Design Philosophy

This reorganization follows these principles:

1. **Single Source of Truth:** All styling in `visualization_config.py`
2. **DRY (Don't Repeat Yourself):** No duplicate plotting code
3. **Modularity:** Core vs. optional analyses separated
4. **Standards Compliance:** Publication-ready by default
5. **Clarity:** Each script has a single, clear purpose

---

## ?? Version History

### Version 2.0 (Current) - January 2026
- Complete reorganization
- Unified configuration system
- Reduced figures from 11 to 7 core
- Publication standards applied throughout
- Modular architecture

### Version 1.x (Legacy)
- Multiple overlapping scripts
- Inconsistent styling
- 11 figures with redundancies

---

## ? Checklist for Publication

- [ ] Run `master_analysis.py` successfully
- [ ] Run `create_diagrams.py` successfully
- [ ] Verify all 7 figures generated (check `figures/` directory)
- [ ] Review figures in manuscript draft
- [ ] Check figure resolution (should be 300 DPI)
- [ ] Verify colorblind accessibility (use online simulator)
- [ ] Update figure captions
- [ ] Reference figures correctly in text
- [ ] Include statistical results in tables
- [ ] Add data availability statement

---

**Last Updated:** January 16, 2026  
**Pipeline Version:** 2.0  
**Status:** ? Production Ready
