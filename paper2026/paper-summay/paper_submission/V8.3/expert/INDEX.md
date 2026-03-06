# Expert Directory - Complete File Index

**Last Updated:** February 1, 2026  
**Status:** ✅ Production-Ready

---

## 📊 Summary Statistics

- **Total Files:** 67 files
  - Scripts: 5 Python files
  - Data Files: 14 (12 CSV + 1 Excel + 1 template)
  - Figures: 30 (24 PNG + 6 PDF)
  - Notebooks: 2 Jupyter notebooks
  - Documentation: 16 markdown files (13 in docs/ + 3 in root)

---

## 🎯 Answer: "Which Script Generated APA Style Figures?"

### **Primary Script:** `scripts/enhanced_statistical_analysis.py`
- Generates **Figures 06-11** (statistical analysis)
- Implements APA Publication Manual (7th Edition) standards
- Uses `visualization_config.py` for styling
- Based on [matplotlib_for_papers guide](https://github.com/jbmouret/matplotlib_for_papers)

### **Configuration Module:** `scripts/visualization_config.py`
- Central APA style configuration
- Okabe-Ito colorblind-friendly palette
- Publication-quality settings (300 DPI, proper fonts)
- Styling utilities and templates

### **Quality Figures:** `scripts/academic_data_quality_plots.py`
- CONSORT-style flow diagrams
- Data completeness visualizations
- Missing data pattern matrices

---

## 📁 Complete File Inventory

### `/scripts` (5 files)

| File | Purpose | Key Functions |
|------|---------|---------------|
| `enhanced_statistical_analysis.py` | Main analysis & plotting | `visualize_personality_vectors()`, `visualize_weighted_scores()`, `visualize_selective_enhancement()` |
| `visualization_config.py` | APA style configuration | `configure_matplotlib()`, `PlotStyler`, `FigureTemplates` |
| `academic_data_quality_plots.py` | CONSORT & quality figures | `create_consort_flow_diagram()`, `create_completeness_lollipop()` |
| `create_dialogue_illustrations.py` | Example conversations | Creates dialogue illustration figures |
| `plotting_example.py` | Working examples | Demonstrates plotting techniques |

### `/data/raw` (13 files)

| File | Description |
|------|-------------|
| `A-1.csv` to `A-5.csv` | Type A personality conversations (5 sessions) |
| `B-1.csv` to `B-5.csv` | Type B personality conversations (5 sessions) |
| `RESULTS.csv` | Combined results from all sessions |
| `TEMPLATE.csv` | Data template for new sessions |
| `1-Evaluation-Simulated-Conversations.xlsx` | Original Excel source data |

**Total Turns:** 120 (60 regulated + 60 baseline)

### `/data/processed` (2 files)

| File | Description | Rows |
|------|-------------|------|
| `regulated.csv` | Regulated condition responses | 60 |
| `baseline.csv` | Baseline condition responses | 60 |

### `/figures` (30 files)

#### Statistical Analysis (Figures 06-11) - APA Style

| Figure | Formats | Description |
|--------|---------|-------------|
| `06_personality_dimensions` | PNG + PDF | OCEAN trait distribution (radar/violin plots) |
| `07_personality_heatmap` | PNG + PDF | Personality trait patterns (vibrant heatmap) |
| `08_weighted_scores` | PNG + PDF | Score comparison bar chart (NO overlap) |
| `09_total_score_boxplot` | PNG + PDF | Distribution boxplot with means |
| `10_selective_enhancement_paired` | PNG + PDF | Paired conversation analysis |
| `11_metric_composition` | PNG + PDF | Rating distribution stacked bars |

#### Data Quality Figures - CONSORT Style

| Figure | Format | Description |
|--------|--------|-------------|
| `data_quality_consort.png` | PNG | CONSORT-style participant flow diagram |
| `data_quality_completeness.png` | PNG | Lollipop chart showing data completeness |
| `data_quality_missing_pattern.png` | PNG | Heatmap of missing data patterns |
| `data_quality_summary.png` | PNG | 4-panel comprehensive summary |

#### System Diagrams - MDPI Style

| Figure | Format | Description |
|--------|--------|-------------|
| `system_architecture_mdpi.png` | PNG | Overall system architecture |
| `data_flow_mdpi.png` | PNG | Data flow pipeline |
| `detection_pipeline_mdpi.png` | PNG | Personality detection workflow |
| `regulation_workflow_mdpi.png` | PNG | Response regulation process |
| `study_design_mdpi.png` | PNG | Study design flowchart |
| `evaluation_framework_mdpi.png` | PNG | Evaluation framework |
| `trait_mapping_mdpi.png` | PNG | OCEAN to Zurich Model mapping |

#### Other Figures

| Figure | Format | Description |
|--------|--------|-------------|
| `01-05_*.png` | PNG | Original analysis figures (legacy) |
| `dialogue_illustration_1.png` | PNG | Example conversation 1 |
| `dialogue_illustration_2.png` | PNG | Example conversation 2 |

### `/notebooks` (2 files)

| File | Description |
|------|-------------|
| `statistical_analysis_enhanced.ipynb` | Main analysis notebook (editable) |
| `statistical_analysis_enhanced.executed.ipynb` | Executed version with outputs |

### `/docs` (13 files)

| File | Topic |
|------|-------|
| `CORRECTED_INTERPRETATIONS.md` | Statistical interpretations & findings |
| `GUIDE_CONFIGURATION_COMPLETE.md` | matplotlib_for_papers implementation |
| `PLOTTING_IMPROVEMENTS.md` | APA plotting best practices |
| `COLOR_SCHEME_UPDATE.md` | Color palette documentation |
| `DEFAULT_COLORS_SUMMARY.md` | Default color usage |
| `FIGURE3_OVERLAP_FIXED.md` | Text overlap fixes |
| `HEATMAP_COLORS_FIXED.md` | Heatmap color improvements |
| `MATPLOTLIB_FOR_PAPERS_UPDATES.md` | Guide implementation notes |
| `NOTEBOOK_INTERPRETATION_CORRECTIONS.md` | Notebook interpretation fixes |
| `NOTEBOOK_UPDATES_COMPLETE.md` | Notebook update summary |
| `STACKED_BAR_CHART_REDESIGN.md` | Stacked bar improvements |
| `XAXIS_LABELING_FIXED.md` | X-axis label fixes |
| `DATA_QUALITY_VISUALIZATION_IMPROVED.md` | Quality figure improvements |

### Root Documentation (3 files)

| File | Purpose |
|------|---------|
| `README.md` | Main overview & quick start |
| `README_MASTER.md` | Complete detailed guide |
| `QUICK_START.md` | Quick reference card |

### `/config` (1 file)

| File | Description |
|------|-------------|
| `requirements.txt` | Python dependencies (pandas, numpy, matplotlib, scipy, seaborn, openpyxl) |

---

## 🔍 Figure-to-Script Mapping

| Figure(s) | Generated By | Line/Function |
|-----------|--------------|---------------|
| 06-07 | `enhanced_statistical_analysis.py` | `visualize_personality_vectors()` |
| 08 | `enhanced_statistical_analysis.py` | `visualize_weighted_scores()` |
| 09 | `enhanced_statistical_analysis.py` | (within weighted scores function) |
| 10 | `enhanced_statistical_analysis.py` | `visualize_selective_enhancement()` |
| 11 | `enhanced_statistical_analysis.py` | (within metrics visualization) |
| data_quality_* | `academic_data_quality_plots.py` | Various functions |
| dialogue_* | `create_dialogue_illustrations.py` | Main function |

---

## 🚀 Quick Reference

### Generate All Figures
```bash
cd notebooks
jupyter notebook statistical_analysis_enhanced.ipynb
# Run all cells
```

### Generate Specific Figure Type
```python
import sys
sys.path.append('../scripts')
from enhanced_statistical_analysis import *
from visualization_config import configure_matplotlib

configure_matplotlib(use_matplotlib_papers_defaults=True)
df_reg, df_base = load_and_prepare_data('../data/processed/regulated.csv', 
                                         '../data/processed/baseline.csv')
visualize_personality_vectors(df_reg, output_dir='../figures')
```

### Use APA Styling in Custom Plots
```python
import sys
sys.path.append('../scripts')
from visualization_config import configure_matplotlib, PlotStyler, PUBLICATION_CONFIG as C

configure_matplotlib(use_matplotlib_papers_defaults=True)
# Your plotting code...
```

---

## 📏 APA Style Standards Applied

### Typography
- **Font:** DejaVu Sans / Arial / Helvetica
- **Sizes:** 8pt (labels), 10pt (legend), 12pt (titles)
- **Weights:** Regular/Medium (no thin fonts)

### Layout
- **DPI:** 300 (publication standard)
- **Formats:** PNG (viewing) + PDF (vector/publication)
- **Line width:** 1.5-2.0pt
- **Spines:** Top/right removed, bottom offset 5pts

### Colors (Okabe-Ito Colorblind-Safe Palette)
- **Regulated:** #0072B2 (Blue)
- **Baseline:** #E69F00 (Orange)
- **Positive:** #009E73 (Green)
- **Negative:** #D55E00 (Vermillion)
- **Neutral:** #666666 (Gray)

### Design Principles
- Minimal "chart junk" (Tufte principles)
- Grid behind data elements
- No overlapping text
- Direct labels preferred
- Print-safe (grayscale compatible)

---

## 🔗 External References

1. **matplotlib_for_papers:** https://github.com/jbmouret/matplotlib_for_papers
2. **Okabe-Ito Palette:** https://jfly.uni-koeln.de/color/
3. **CONSORT Guidelines:** http://www.consort-statement.org/
4. **APA Style (7th ed.):** https://apastyle.apa.org/
5. **Tufte's Principles:** The Visual Display of Quantitative Information

---

## 📞 Need Help?

- **Quick start:** See `README.md`
- **Complete guide:** See `README_MASTER.md`
- **Quick reference:** See `QUICK_START.md`
- **Statistical issues:** See `docs/CORRECTED_INTERPRETATIONS.md`
- **Plotting issues:** See `docs/PLOTTING_IMPROVEMENTS.md`
- **Configuration:** See `docs/GUIDE_CONFIGURATION_COMPLETE.md`

---

**Version:** 1.0  
**Status:** Production-Ready ✅  
**Maintained By:** Research Team
