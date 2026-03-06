# Statistical Analysis Guide
## Personality-Adaptive Chatbot Performance Evaluation

This guide explains all the generated files and how to use them for your thesis.

---

## 📁 Directory Structure

```
statistical analysis/
├── data/                              # Individual CSV files from Excel tabs
│   ├── A-1.csv to A-5.csv            # Type A personality conversations
│   ├── B-1.csv to B-5.csv            # Type B personality conversations
│   ├── TEMPLATE.csv                   # Template sheet
│   └── RESULTS.csv                    # Summary results
│
├── merged/                            # Merged datasets
│   ├── regulated.csv                  # All regulated data (59 messages)
│   └── baseline.csv                   # All baseline data (60 messages)
│
├── figures/                           # Generated visualizations
│   ├── 01_sample_distribution.png     # Sample size and distribution
│   ├── 02_missing_data_heatmap.png    # Data quality heatmap
│   ├── 03_performance_comparison.png  # Regulated vs Baseline comparison
│   ├── 04_effect_sizes.png            # Cohen's d effect sizes
│   └── 05_percentage_improvement.png  # Percentage point improvements
│
├── Scripts:
│   ├── convert_excel_to_csv.py        # Converts Excel to CSV
│   ├── merge_regulated.py             # Merges regulated data
│   ├── merge_baseline.py              # Merges baseline data
│   └── statistical_analysis.py        # Main analysis script
│
└── Results:
    ├── analysis_report.txt            # Comprehensive text report
    ├── analysis_results_descriptive.csv   # Descriptive statistics table
    ├── analysis_results_effect_sizes.csv  # Effect sizes table
    └── analysis_results_inferential.csv   # Inferential test results
```

---

## 📊 Key Results Summary

### Sample Information
- **Total Conversations:** 10 (5 Type A, 5 Type B)
- **Regulated Messages:** 59
- **Baseline Messages:** 60
- **Personality Types:** 
  - Type A (OCEAN: 1,1,1,1,1)
  - Type B (OCEAN: -1,-1,-1,-1,-1)

### Main Findings

#### 1. **PERSONALITY NEEDS ADDRESSED** 🎯
- **Cohen's d:** 4.584 (LARGE effect)
- **Regulated:** 100.0% success rate
- **Baseline:** 8.6% success rate
- **Improvement:** +91.4 percentage points
- **Interpretation:** The regulated condition dramatically outperforms baseline in addressing individual personality needs

#### 2. **RELEVANCE & COHERENCE**
- **Cohen's d:** 0.182 (Negligible effect)
- **Regulated:** 100.0%
- **Baseline:** 98.3%
- **Improvement:** +1.7 percentage points
- **Interpretation:** Both conditions perform well, with slight advantage to regulated

#### 3. **EMOTIONAL TONE APPROPRIATE**
- **Cohen's d:** 0.000 (Negligible effect)
- **Regulated:** 100.0%
- **Baseline:** 100.0%
- **Improvement:** 0.0 percentage points
- **Interpretation:** Both conditions equally effective

#### 4. **DETECTION ACCURATE** (Regulated Only)
- **Success Rate:** 100.0% (58/58 valid responses)
- **Interpretation:** Near-perfect personality detection accuracy

#### 5. **REGULATION EFFECTIVE** (Regulated Only)
- **Success Rate:** 100.0% (59/59 responses)
- **Interpretation:** Perfect regulation effectiveness

---

## 🔬 Statistical Methods Used

### 1. Descriptive Statistics
- **Mean (M):** Average score (0-1 scale, or 0-100%)
- **Standard Deviation (SD):** Measure of variability
- **95% Confidence Intervals:** Range of plausible values
- **Sample Size (N):** Number of observations

### 2. Effect Size (Cohen's d)
Formula: `d = (M_regulated - M_baseline) / pooled_SD`

**Interpretation (Cohen, 1988):**
- |d| < 0.2: Negligible effect
- 0.2 ≤ |d| < 0.5: Small effect
- 0.5 ≤ |d| < 0.8: Medium effect
- |d| ≥ 0.8: Large effect

### 3. Inferential Statistics (Illustrative)
- **Independent samples t-tests**
- **Note:** These are for illustration only, given the deterministic simulation
- Should NOT be interpreted as evidence of generalizable hypothesis testing
- Useful for contextualizing effect sizes and facilitating comparisons with empirical studies

---

## 📝 How to Use These Results in Your Thesis

### For Methods Section

```
Statistical Analysis: Descriptive statistics (means, standard deviations, 
and 95% confidence intervals) were calculated for each evaluation metric. 
Effect sizes (Cohen's d) were computed to estimate the magnitude of 
differences between regulated and baseline conditions. The study employed 
10 conversations (5 per personality type) with 6 dialogue turns each, 
generating approximately 120 total dialogue turns for analysis.
```

### For Results Section

```
The analysis revealed substantial improvements in the regulated condition 
compared to baseline. Most notably, the regulated assistant demonstrated 
a large effect size (Cohen's d = 4.584) for addressing personality needs, 
with 100% success rate compared to 8.6% in the baseline condition 
(+91.4 percentage points). Both conditions performed equally well in 
maintaining appropriate emotional tone (100% each), while the regulated 
condition showed perfect coherence (100%) compared to 98.3% in baseline 
(Cohen's d = 0.182).
```

### For Tables

**Table 1: Descriptive Statistics and Effect Sizes**

| Metric | Condition | N | Mean | SD | 95% CI | Cohen's d |
|--------|-----------|---|------|----|----|-----------|
| Emotional Tone | Regulated | 59 | 1.000 | 0.000 | [—, —] | 0.000 |
| | Baseline | 60 | 1.000 | 0.000 | [—, —] | |
| Relevance & Coherence | Regulated | 59 | 1.000 | 0.000 | [—, —] | 0.182 |
| | Baseline | 60 | 0.983 | 0.129 | [0.950, 1.017] | |
| Personality Needs | Regulated | 59 | 1.000 | 0.000 | [—, —] | **4.584** |
| | Baseline | 58 | 0.086 | 0.283 | [0.012, 0.161] | |

Note: Cohen's d > 0.8 indicates large effect (shown in bold)

### For Figures

1. **Figure 1 (01_sample_distribution.png):** Sample distribution showing balanced representation of personality types and consistent conversation lengths

2. **Figure 2 (03_performance_comparison.png):** Performance comparison between regulated and baseline conditions across all metrics

3. **Figure 3 (04_effect_sizes.png):** Effect sizes visualization showing the dramatic advantage of regulation for personality needs

4. **Figure 4 (05_percentage_improvement.png):** Percentage point improvements, highlighting the 91.4% advantage in addressing personality needs

---

## 🔄 Reproducing the Analysis

### Step 1: Convert Excel to CSV
```bash
python3 convert_excel_to_csv.py
```
Creates individual CSV files in `data/` directory.

### Step 2: Merge Data
```bash
python3 merge_regulated.py
python3 merge_baseline.py
```
Creates `merged/regulated.csv` and `merged/baseline.csv`.

### Step 3: Run Statistical Analysis
```bash
python3 statistical_analysis.py
```
Generates all figures, tables, and reports.

---

## 📚 For Jupyter Notebook

To convert the analysis to a Jupyter notebook for interactive exploration:

1. Create cells for each analysis step from `statistical_analysis.py`
2. The script is already modular with clear sections
3. Each section can be a separate notebook cell
4. Add markdown cells between code cells for narrative

Key sections:
- Data loading and preparation
- Data quality assessment
- Descriptive statistics
- Effect size calculations
- Visualizations
- Inferential tests (illustrative)

---

## ⚠️ Important Notes

### Ethics Statement
No human subjects were involved. All conversations were simulated interactions between predefined personality profiles (Type A and Type B) and the chatbot. No formal ethics approval required for synthetic data.

### Statistical Limitations
- **Deterministic Simulation:** Results from simulated conversations, not real users
- **Inferential Statistics:** Included for illustration only, not for generalization
- **Sample Size:** 10 conversations sufficient for proof-of-concept
- **Future Work:** Real-user trials would require different statistical approach

### Data Quality
- Missing data primarily in "ASSISTANT START" fields (expected for some message types)
- All evaluation metrics have high completion rates (>98%)
- No systematic missing data patterns detected

---

## 📖 References for Statistical Methods

1. **Cohen's d:**
   - Cohen, J. (1988). Statistical power analysis for the behavioral sciences (2nd ed.). Erlbaum.

2. **Confidence Intervals:**
   - Cumming, G. (2014). The new statistics: Why and how. Psychological Science, 25(1), 7-29.

3. **Effect Sizes in Psychology:**
   - Lakens, D. (2013). Calculating and reporting effect sizes to facilitate cumulative science. Frontiers in Psychology, 4, 863.

---

## 🎯 Key Takeaway for Thesis

**The personality-adaptive regulation system demonstrates LARGE and practically meaningful improvements in addressing individual personality needs (Cohen's d = 4.584, 91.4 percentage point improvement), while maintaining consistently high performance across all other evaluation dimensions. This provides strong evidence for the effectiveness of the proposed approach in simulation-based testing.**

---

## Questions?

For issues or questions about the analysis:
1. Check the `analysis_report.txt` for detailed results
2. Review figures in `figures/` directory
3. Examine CSV files in `analysis_results_*.csv` for raw numbers
4. Re-run `statistical_analysis.py` if data changes

Generated: October 2025



