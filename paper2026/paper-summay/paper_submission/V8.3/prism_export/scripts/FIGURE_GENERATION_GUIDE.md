# Figure Generation Guide

**Date**: 2026-02-03  
**Status**: Updated to use **Cliff's delta** (NOT Cohen's d)

---

## 📊 Overview

This document explains how to generate all figures used in the manuscript.

**IMPORTANT**: All statistical figures use **Cliff's delta** for effect sizes, NOT Cohen's d. Cohen's d is inappropriate for bounded ordinal data with ceiling effects.

---

## 🎯 Figure Types

### 1. Statistical Analysis Figures (Auto-generated)

These figures are generated from the analysis scripts:

| Figure | File | Script | Effect Size |
|--------|------|--------|-------------|
| Figure 3 | `03_performance_comparison.png` | `generate_all_figures.py` | Cliff's δ ✅ |
| Figure 4 | `04_effect_sizes.png` | `generate_all_figures.py` | Cliff's δ ✅ |
| Figure 8 | `data_quality_summary.png` | `enhanced_statistical_analysis.py` | N/A |
| Figure 9 | `06_personality_dimensions.png` | `enhanced_statistical_analysis.py` | N/A |
| Figure 10 | `07_personality_heatmap.png` | `enhanced_statistical_analysis.py` | N/A |
| Figure 11 | `08_weighted_scores.png` | `generate_all_figures.py` | Cliff's δ ✅ |
| Figure 12 | `09_total_score_boxplot.png` | `generate_all_figures.py` | Cliff's δ ✅ |
| Figure 13 | `10_selective_enhancement_paired.png` | `enhanced_statistical_analysis.py` | N/A |
| Figure 14 | `11_metric_composition.png` | `enhanced_statistical_analysis.py` | N/A |

### 2. Dialogue Illustrations (Auto-generated)

| Figure | File | Script | Data Source |
|--------|------|--------|-------------|
| Figure 15 | `dialogue_illustration_1.png` | `generate_all_figures.py` | MSG B-4-1 |
| Figure 16 | `dialogue_illustration_2.png` | `generate_all_figures.py` | MSG A-5-3 |

### 3. System Architecture Diagrams (Manual)

These are created with diagram tools (draw.io, Figma, etc.):

| Figure | File | Tool | Notes |
|--------|------|------|-------|
| Figure 1 | `mdpi/study_design_mdpi.png` | draw.io | Study workflow |
| Figure 2 | `mdpi/system_architecture_mdpi.png` | draw.io | System components |
| Figure 3 | `mdpi/data_flow_mdpi.png` | draw.io | Pipeline flow |
| Figure 4 | `mdpi/detection_pipeline_mdpi.png` | draw.io | Detection module |
| Figure 5 | `mdpi/trait_mapping_mdpi.png` | draw.io | Trait to behavior |
| Figure 6 | `mdpi/regulation_workflow_mdpi.png` | draw.io | Regulation logic |
| Figure 7 | `mdpi/evaluation_framework_mdpi.png` | draw.io | Evaluation criteria |

---

## 🚀 Quick Start

### Generate All Figures

```bash
cd scripts
python3 generate_all_figures.py
```

This will:
1. ✅ Load data from `data/merged/` directory
2. ✅ Calculate statistics using **Cliff's delta** (NOT Cohen's d)
3. ✅ Generate all statistical figures (Figures 3, 4, 8-14)
4. ✅ Generate dialogue illustrations (Figures 15-16)
5. ✅ Save to `figures/` directory

---

## 📁 Directory Structure

```
scripts/
├── generate_all_figures.py          # Main generation script ✅ Cliff's delta
├── enhanced_statistical_analysis.py # Core analysis functions ✅ Cliff's delta
├── visualization_config.py          # Plot styling configuration
├── statistical_analysis_enhanced.ipynb # Interactive analysis notebook
├── data/
│   └── merged/
│       ├── regulated.csv            # Regulated condition data
│       └── baseline.csv             # Baseline condition data
└── figures/
    ├── 03_performance_comparison.png
    ├── 04_effect_sizes.png          # ✅ Shows Cliff's delta
    ├── 08_weighted_scores.png
    ├── 09_total_score_boxplot.png
    ├── dialogue_illustration_1.png
    ├── dialogue_illustration_2.png
    └── mdpi/
        ├── study_design_mdpi.png    # Manual diagram
        ├── system_architecture_mdpi.png
        └── ...
```

---

## 🔬 Statistical Methods

### Effect Size: Cliff's Delta (δ)

**Why Cliff's delta and NOT Cohen's d?**

Our data violates Cohen's d assumptions:
- ❌ **Not continuous**: Discrete ordinal values (0, 0.5, 1)
- ❌ **Not normally distributed**: Bounded, skewed distribution
- ❌ **Ceiling effects**: Near-zero variance in regulated condition
- ❌ **Result**: Cohen's d = 4.651 was meaningless (artifact of SD ≈ 0)

**Solution**: Cliff's delta (δ)
- ✅ **Non-parametric**: No distribution assumptions
- ✅ **Ordinal-appropriate**: Designed for ranked/ordered data
- ✅ **Robust**: Handles ceiling effects correctly
- ✅ **Interpretable**: δ = 0.917 = "91.7% ordinal dominance"

### Thresholds (Romano et al., 2006)

| |δ| | Interpretation |
|-----|----------------|
| < 0.147 | Negligible |
| < 0.33 | Small |
| < 0.474 | Medium |
| ≥ 0.474 | **Large** |

### Implementation

```python
from enhanced_statistical_analysis import calculate_effect_sizes

# Calculates Cliff's delta (NOT Cohen's d)
df_effects = calculate_effect_sizes(df_regulated, df_baseline)

# Results:
# - Cliffs_delta: The effect size value
# - Cliffs_delta_Interpretation: Text interpretation
# - Risk_Difference: YES-rate difference (Δp)
# - Odds_Ratio: OR with 95% CI
# - Cohens_h: Proportion difference standardized
```

---

## 🎨 Dialogue Illustrations

### Data Source

Dialogue illustrations pull actual conversation excerpts from the merged dataset:

- **Figure 15 (Type B)**: Message `B-4-1`
  - Personality: Low OCEAN (vulnerable profile)
  - Shows security-focused, low-pressure approach
  
- **Figure 16 (Type A)**: Message `A-5-3`
  - Personality: High OCEAN (high-functioning profile)
  - Shows growth-oriented, affirming approach

### Visual Design

Each figure shows:
1. **User message** (top)
2. **Regulated response** (left column)
   - Includes detected personality traits
   - Shows regulation prompt applied
3. **Baseline response** (right column)
   - Generic supportive response

### Customization

To use different conversation examples, edit `generate_all_figures.py`:

```python
# Change message IDs here:
rr_b, rb_b = get_row("B-4-1")  # Type B example
rr_a, rb_a = get_row("A-5-3")  # Type A example
```

Available messages: Any `MSG. NO.` from `data/merged/regulated.csv`

---

## 📊 Regenerating Specific Figures

### Statistical Figures Only

```python
from enhanced_statistical_analysis import (
    load_and_prepare_data,
    convert_to_numeric,
    calculate_effect_sizes,  # Uses Cliff's delta
    visualize_results,
)

# Load data
df_reg, df_base = load_and_prepare_data('data/merged/regulated.csv', 
                                        'data/merged/baseline.csv')

# Calculate statistics (Cliff's delta, NOT Cohen's d)
df_reg_num, df_base_num = convert_to_numeric(df_reg, df_base)
df_stats = calculate_descriptive_statistics(df_reg_num, df_base_num)
df_effects = calculate_effect_sizes(df_reg_num, df_base_num)

# Generate figures
visualize_results(df_stats, df_effects, output_dir='figures')
```

### Dialogue Illustrations Only

```bash
cd scripts
python3 -c "from generate_all_figures import generate_dialogue_illustrations; generate_dialogue_illustrations()"
```

---

## ⚠️ Important Notes

### 1. Cohen's d is REMOVED

The old approach used Cohen's d:
```python
# ❌ OLD (inappropriate for our data)
d = (mean_reg - mean_base) / pooled_sd  # d = 4.651 (meaningless!)
```

The new approach uses Cliff's delta:
```python
# ✅ NEW (appropriate for ordinal bounded data)
delta = cliffs_delta(regulated_vals, baseline_vals)  # δ = 0.917 ✅
```

### 2. Data Requirements

Required CSV files with columns:
- `MSG. NO.`: Message identifier (e.g., "A-1-1", "B-2-3")
- Evaluation metrics:
  - `EMOTIONAL TONE APPROPRIATE`
  - `RELEVANCE & COHERENCE`
  - `PERSONALITY NEEDS ADDRESSED`
- Regulated-only:
  - `DETECTED PERSONALITY (O,C,E,A,N)`
  - `REGULATION PROMPT APPLIED`
  - `ASSISTANT REPLY (REG)`

### 3. Output Formats

All figures are saved in:
- **PNG** (300 DPI) - For viewing and inclusion in Word docs
- **PDF** (vector) - For LaTeX and print-quality publishing

### 4. System Diagrams

Architecture diagrams (Figures 1-7) are NOT auto-generated. They are:
- Created manually with diagram tools (draw.io recommended)
- Exported as PNG at 300 DPI
- Saved in `figures/mdpi/` directory
- Follow MDPI publication standards (colorblind-safe palette, minimal design)

---

## 🔍 Verification

### Check Effect Sizes

After generation, verify that Cliff's delta is used:

```bash
cd scripts
python3 -c "
import pandas as pd
df = pd.read_csv('analysis_results_summary.csv')
if 'Cliffs_delta' in df.columns:
    print('✓ Using Cliff's delta')
    print(df[['Metric', 'Cliffs_delta']])
else:
    print('⚠️  WARNING: Cliff's delta not found!')
"
```

Expected output:
```
✓ Using Cliff's delta
                        Metric  Cliffs_delta
0   EMOTIONAL TONE APPROPRIATE      0.000000
1        RELEVANCE & COHERENCE      0.016667
2  PERSONALITY NEEDS ADDRESSED      0.916667
```

### Check Figure Files

```bash
ls -lh figures/*.png | grep -E "(04_effect|08_weighted|dialogue)"
```

Expected:
- `04_effect_sizes.png` - Shows Cliff's delta values
- `08_weighted_scores.png` - Bar chart comparison
- `dialogue_illustration_1.png` - Type B example
- `dialogue_illustration_2.png` - Type A example

---

## 🐛 Troubleshooting

### "Data files not found"

**Problem**: Script can't find CSV files

**Solution**: Ensure data files exist:
```bash
ls data/merged/regulated.csv
ls data/merged/baseline.csv
```

### "Message ID not found"

**Problem**: Dialogue illustration can't find specified message

**Solution**: Check available messages:
```bash
cd scripts
python3 -c "
import pandas as pd
df = pd.read_csv('data/merged/regulated.csv')
print(df['MSG. NO.'].unique())
"
```

### "Module not found"

**Problem**: Can't import analysis functions

**Solution**: Ensure you're in the scripts directory:
```bash
cd scripts
python3 generate_all_figures.py
```

### "Cliff's delta not in results"

**Problem**: Old version of analysis script

**Solution**: Verify script version:
```bash
grep "Cliffs_delta" enhanced_statistical_analysis.py
```

Should return multiple matches. If not, update the script.

---

## 📚 References

### Cliff's Delta
- Cliff, N. (1993). Dominance statistics: Ordinal analyses to answer ordinal questions. *Psychological Bulletin*, 114(3), 494-509.

### Thresholds
- Romano, J., et al. (2006). Appropriate statistics for ordinal level data. *Annual Meeting of the Florida Association of Institutional Research*.

### Visualization Standards
- Tufte, E. R. (2001). *The Visual Display of Quantitative Information*
- [matplotlib_for_papers](https://github.com/jbmouret/matplotlib_for_papers)

---

## ✅ Summary

**Quick Generation**:
```bash
cd scripts
python3 generate_all_figures.py
```

**Key Points**:
1. ✅ Uses **Cliff's delta** (NOT Cohen's d)
2. ✅ Generates statistical figures + dialogue illustrations
3. ✅ System diagrams are created manually (draw.io)
4. ✅ Output: PNG (300 DPI) + PDF (vector)
5. ✅ Publication-ready quality

**Result**: All figures ready for manuscript submission! 🎓✨

---

**Last Updated**: 2026-02-03  
**Script**: `generate_all_figures.py`  
**Status**: ✅ Production-ready
