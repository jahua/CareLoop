# Enhanced Statistical Analysis Notebook Guide

## 📓 Overview

The **`statistical_analysis_enhanced.ipynb`** notebook provides a comprehensive, publication-ready statistical analysis for your thesis, meeting **MDPI academic standards**. It includes all requested features:

✅ **Personality Vector Analysis** (OCEAN dimensions)  
✅ **Weighted Scoring System** (SUMPRODUCT-like: YES=2, NOT SURE=1, NO=0)  
✅ **Advanced Statistical Tests** (t-test, Mann-Whitney U, Effect Sizes)  
✅ **Reliability Analysis** (Cronbach's Alpha)  
✅ **Publication-Ready Visualizations**

---

## 🚀 Quick Start

### 1. Activate Virtual Environment

```bash
source /Users/huaduojiejia/MyProject/hslu/2026/.venv/bin/activate
```

### 2. Navigate to Analysis Directory

```bash
cd "/Users/huaduojiejia/MyProject/hslu/2026/paper-summay/paper_submission/statistical analyis"
```

### 3. Launch Jupyter Notebook

```bash
jupyter notebook statistical_analysis_enhanced.ipynb
```

### 4. Run the Analysis

**Option A: Run All Cells**
- Menu: `Kernel` → `Restart & Run All`

**Option B: Run Cell-by-Cell**
- Click each cell and press `Shift+Enter`

---

## 📊 Notebook Structure

### **Section 1: Setup (Cells 1-3)**
- Import libraries
- Load analysis functions
- Configure visualization settings

### **Section 2: Data Loading (Cells 4-5)**
- Load regulated and baseline datasets
- Extract conversation IDs
- Preview data

### **Section 3: Data Quality (Cell 6-7)**
- Assess missing data
- Visualize sample distribution
- Check data completeness

### **Section 4: Personality Vector Analysis (Cells 8-9)** ⭐ **NEW**
- Parse OCEAN personality vectors: `(O, C, E, A, N)`
- Each dimension: `-1` (low), `0` (neutral), `1` (high)
- Analyze personality trait distributions
- Visualize:
  - Individual OCEAN dimension frequencies
  - Personality heatmap across messages

**Key Outputs:**
- `06_personality_dimensions.png` - Bar charts for each OCEAN trait
- `07_personality_heatmap.png` - Heatmap showing personality patterns

### **Section 5: Weighted Scoring System (Cells 10-12)** ⭐ **NEW**

**Scoring Formula (SUMPRODUCT-like):**
- **YES** = 2 points
- **NOT SURE** = 1 point
- **NO** = 0 points

**Regulated Metrics:**
1. **Detection Accuracy Score** (max=2)
2. **Regulation Effectiveness Score** (max=2)
3. **Emotional Tone Score** (max=2)
4. **Relevance & Coherence Score** (max=2)
5. **Personality Needs Score** (max=2)
6. **Total (Regulated)** (max=6) = Emotional Tone + Relevance + Personality Needs

**Baseline Metrics:**
1. **Emotional Tone Score** (max=2)
2. **Relevance & Coherence Score** (max=2)
3. **Personality Needs Score** (max=2)
4. **Total (Baseline)** (max=6) = Sum of above

**Key Outputs:**
- `08_weighted_scores.png` - Bar chart comparison with error bars
- `09_total_score_boxplot.png` - Box plot of total scores

### **Section 6: Numeric Conversion (Cell 13-14)**
- Convert categorical to 0-1 scale for traditional analysis
- YES → 1.0, NOT SURE → 0.5, NO → 0.0

### **Section 7: Descriptive Statistics (Cell 15)**
- Mean ± Standard Deviation
- 95% Confidence Intervals
- Sample sizes

### **Section 8: Effect Size Analysis (Cell 16-17)**
- **Cohen's d** effect sizes
- Interpretation: Small (0.2), Medium (0.5), Large (0.8)
- Percentage point improvements

**Key Outputs:**
- `03_performance_comparison.png` - Mean comparison with CIs
- `04_effect_sizes.png` - Cohen's d visualization
- `05_percentage_improvement.png` - Percentage differences

### **Section 9: Advanced Statistical Tests (Cell 18-19)** ⭐ **NEW**

**Tests Performed:**
1. **Independent t-test**: Compare means (parametric)
2. **Mann-Whitney U test**: Non-parametric alternative
3. **Levene's test**: Check equality of variances
4. **Shapiro-Wilk test**: Check normality assumptions
5. **95% Confidence Intervals**: For mean differences

**Output Table Includes:**
- Test statistics (t, U)
- p-values (with significance stars: ***, **, *, ns)
- Cohen's d effect sizes
- Assumption check results

### **Section 10: Reliability Analysis (Cell 20-21)** ⭐ **NEW**

- **Cronbach's Alpha** for internal consistency
- Inter-item correlation matrix

**Interpretation:**
- α ≥ 0.9: Excellent
- α ≥ 0.8: Good
- α ≥ 0.7: Acceptable
- α ≥ 0.6: Questionable
- α < 0.6: Poor

### **Section 11: Comprehensive Summary (Cell 22-23)**

Creates final summary table with:
- Mean and SD for each metric
- Mean differences
- Cohen's d
- Percentage improvements
- Overall total scores

### **Section 12: Export Results (Cell 24)**

Exports:
- `analysis_results_summary.csv` - Main summary table
- `analysis_results_advanced_tests.csv` - All statistical tests
- `regulated_with_scores.csv` - Full regulated data with scores
- `baseline_with_scores.csv` - Full baseline data with scores
- `regulated_with_personality.csv` - Regulated data with parsed OCEAN vectors

---

## 📈 Generated Visualizations

All figures are saved in `figures/` directory:

| File | Description |
|------|-------------|
| `01_sample_distribution.png` | Sample size by conversation |
| `02_missing_data_heatmap.png` | Missing data patterns |
| `03_performance_comparison.png` | Mean scores with 95% CIs |
| `04_effect_sizes.png` | Cohen's d effect sizes |
| `05_percentage_improvement.png` | Percentage point differences |
| `06_personality_dimensions.png` | ⭐ OCEAN trait distributions |
| `07_personality_heatmap.png` | ⭐ Personality patterns across messages |
| `08_weighted_scores.png` | ⭐ Weighted score comparison |
| `09_total_score_boxplot.png` | ⭐ Total score distributions |

---

## 🎓 MDPI Academic Rigor Features

### ✅ Comprehensive Statistical Testing
- Parametric (t-test) and non-parametric (Mann-Whitney) tests
- Assumption checks (normality, equal variance)
- Multiple effect size measures

### ✅ Transparent Methodology
- Clear documentation of scoring methods
- Explicit statement of limitations (simulation data)
- Step-by-step reproducible workflow

### ✅ Robust Reporting
- Confidence intervals for all estimates
- Standard deviations alongside means
- Significance testing with appropriate caveats

### ✅ Reliability Assessment
- Internal consistency analysis (Cronbach's Alpha)
- Inter-item correlations

### ✅ Publication-Quality Figures
- High DPI (300 dpi)
- Professional color schemes
- Clear labels and legends
- Error bars with confidence intervals

---

## 💡 Usage Tips

### Customizing Visualizations

To modify plots, edit the functions in `enhanced_statistical_analysis.py`:

```python
# Change figure size
fig, ax = plt.subplots(figsize=(12, 8))  # Increase from default

# Change color scheme
colors = ['#yourcolor1', '#yourcolor2']

# Adjust DPI
plt.savefig('output.png', dpi=600)  # Higher resolution
```

### Re-running Specific Sections

You can re-run any section independently:
1. Click the cell
2. Press `Shift+Enter`
3. Subsequent cells will use updated results

### Exporting Individual Cells

To export a specific visualization or table:

```python
# Save specific figure
import matplotlib.pyplot as plt
plt.savefig('my_custom_figure.png', dpi=300, bbox_inches='tight')

# Export specific table
df_summary.to_csv('my_custom_table.csv', index=False)
df_summary.to_latex('my_custom_table.tex', index=False)  # For LaTeX
```

---

## 🔧 Troubleshooting

### Issue: Visualizations not displaying

**Solution:**
```python
%matplotlib inline
import matplotlib.pyplot as plt
plt.show()
```

### Issue: "No module named X"

**Solution:**
```bash
source /Users/huaduojiejia/MyProject/hslu/2026/.venv/bin/activate
pip install -r requirements.txt
```

### Issue: Personality vectors not parsing

**Check:**
- Column name is exactly: `DETECTED PERSONALITY (O,C,E,A,N)`
- Format is: `(0, 0, 1, 1, 1)` with parentheses and commas
- No missing or malformed entries

**Debug:**
```python
# Check unique values
print(df_regulated['DETECTED PERSONALITY (O,C,E,A,N)'].unique())

# Check parsing results
df_regulated['test_parse'] = df_regulated['DETECTED PERSONALITY (O,C,E,A,N)'].apply(parse_personality_vector)
print(df_regulated[['DETECTED PERSONALITY (O,C,E,A,N)', 'test_parse']].head(10))
```

### Issue: Statistical tests show warnings

**Common warnings:**
- Small sample size: Normal for simulation studies
- Non-normal distribution: Use Mann-Whitney U instead of t-test
- Equal variance violated: Results still valid with large effect sizes

---

## 📝 Integrating Results into Thesis

### For Methods Section

```markdown
Statistical analyses were conducted using Python 3.9 with pandas, NumPy, 
SciPy, and matplotlib. Personality traits were encoded using the OCEAN model 
(Openness, Conscientiousness, Extraversion, Agreeableness, Neuroticism) with 
values of -1 (low), 0 (neutral), and 1 (high).

Evaluation responses were scored using a weighted system: YES = 2 points, 
NOT SURE = 1 point, NO = 0 points. This approach, analogous to Excel's 
SUMPRODUCT function, provides a continuous quantitative measure while 
preserving information about evaluator certainty.

Descriptive statistics (M ± SD), 95% confidence intervals, and effect sizes 
(Cohen's d) were computed for all metrics. Both parametric (independent 
t-test) and non-parametric (Mann-Whitney U) tests were applied, with 
assumption checks (Shapiro-Wilk for normality, Levene's for variance 
homogeneity). Internal consistency was assessed using Cronbach's Alpha. 
Statistical significance was set at α = 0.05, though results are interpreted 
cautiously given the simulation-based study design.
```

### For Results Section

Use the summary tables and figures directly:
- Table: `analysis_results_summary.csv`
- Figures: All PNG files in `figures/`

Example:
```markdown
Regulated assistants achieved higher weighted scores across all metrics 
(Figure 8). The total score (max=6) was M=4.52 ± 0.68 for regulated vs 
M=3.81 ± 0.72 for baseline, representing a difference of 0.71 points 
(95% CI: [0.45, 0.97], d=1.01, p<.001).

Personality detection accuracy was high (M=1.82 ± 0.31, 91% YES responses), 
and regulation effectiveness was consistently rated positively 
(M=1.76 ± 0.38, 88% YES responses).

Cronbach's Alpha indicated good internal consistency (α=0.83) across the 
five evaluation metrics.
```

### For Discussion Section

```markdown
The large effect sizes (d > 0.8) observed across metrics suggest meaningful 
practical differences between regulated and baseline assistants. However, 
as these results derive from deterministic simulations with predefined 
personality profiles, they should be interpreted as proof-of-concept rather 
than generalizable findings. Future work with real users is needed to 
validate these patterns in naturalistic settings.
```

---

## 🎯 Key Takeaways

1. **Comprehensive Analysis**: All requested features implemented (personality vectors, weighted scoring, advanced tests)

2. **Academic Standards**: Meets MDPI requirements with transparent methods, robust statistics, and clear limitations

3. **Publication-Ready**: High-quality visualizations and exportable tables

4. **Reproducible**: Complete step-by-step workflow in notebook format

5. **Flexible**: Easy to modify, extend, and customize

6. **Well-Documented**: Clear explanations throughout

---

## 📧 Next Steps

1. ✅ Run the complete notebook
2. ✅ Review all visualizations
3. ✅ Examine summary tables
4. ✅ Integrate findings into thesis manuscript
5. ✅ Share with advisor for feedback
6. ✅ Refine analyses as needed

---

## 🏁 You're Ready!

All analysis tools are complete and tested. The enhanced notebook provides everything you need for a rigorous, publication-quality statistical analysis section in your thesis.

**Good luck with your thesis! 🎓**



