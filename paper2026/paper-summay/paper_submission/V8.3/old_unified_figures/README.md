# Unified Figures Directory

**Created:** January 16, 2026  
**Total Figures:** 18  
**Standard:** 300 DPI, Publication-ready

---

## Overview

This directory contains all figures consolidated from multiple sources with uniform formatting and organization.

---

## Figure Categories

### Statistical Analysis Figures (01-09)

| # | Filename | Size | Purpose |
|---|----------|------|---------|
| 01 | `01_sample_distribution.png` | 112 KB | Sample characteristics |
| 02 | `02_missing_data_heatmap.png` | 270 KB | Data quality |
| 03 | `03_performance_comparison.png` | 121 KB | Main results |
| 04 | `04_effect_sizes.png` | 135 KB | Cohen's d |
| 05 | `05_percentage_improvement.png` | 91 KB | Improvement metrics |
| 06 | `06_personality_dimensions.png` | 289 KB | OCEAN dimensions |
| 07 | `07_personality_heatmap.png` | 94 KB | Personality patterns |
| 08 | `08_weighted_scores.png` | 150 KB | Weighted analysis |
| 09 | `09_total_score_boxplot.png` | 111 KB | Score distribution |

### System Architecture Figures (10-11)

| # | Filename | Size | Purpose |
|---|----------|------|---------|
| 10 | `10_system_overview.png` | 238 KB | System pipeline (simple) |
| 10 | `10_system_architecture.png` | 344 KB | System architecture (detailed) |
| 11 | `11_study_workflow.png` | 259 KB | Study workflow (simple) |
| 11 | `11_study_design_flowchart.png` | 444 KB | Study design (detailed) |

### Detailed Process Figures (12-16)

| # | Filename | Size | Purpose |
|---|----------|------|---------|
| 12 | `12_evaluation_framework.png` | 440 KB | Evaluation methodology |
| 13 | `13_data_flow_pipeline.png` | 246 KB | Data processing flow |
| 14 | `14_detection_pipeline.png` | 128 KB | Personality detection |
| 15 | `15_regulation_prompt_assembly.png` | 181 KB | Regulation system |
| 16 | `16_trait_to_zurich_mapping.png` | 423 KB | Trait mapping |

**Total Size:** ~3.5 MB

---

## Recommendations for Manuscript

### Essential Figures (7 core)

Use these in the main manuscript:

1. **Figure 1**: `03_performance_comparison.png` - Main results
2. **Figure 2**: `04_effect_sizes.png` - Effect sizes
3. **Figure 3**: `01_sample_distribution.png` - Sample info
4. **Figure 4**: `10_system_overview.png` - System overview (simpler version)
5. **Figure 5**: `11_study_workflow.png` - Study design (simpler version)
6. **Figure 6**: `14_detection_pipeline.png` - Detection process
7. **Figure 7**: `16_trait_to_zurich_mapping.png` - Theoretical framework

### Supplementary Figures

Move to supplementary materials:
- `02_missing_data_heatmap.png`
- `05_percentage_improvement.png` (redundant with Figure 2)
- `06_personality_dimensions.png`
- `07_personality_heatmap.png`
- `08_weighted_scores.png`
- `09_total_score_boxplot.png`
- `12_evaluation_framework.png`
- `13_data_flow_pipeline.png`
- `15_regulation_prompt_assembly.png`

### Note on Duplicates

Two versions exist for Figures 10 and 11:
- **Simple versions** (`10_system_overview.png`, `11_study_workflow.png`): Use in main text
- **Detailed versions** (`10_system_architecture.png`, `11_study_design_flowchart.png`): Use if more detail needed

---

## Quality Standards

All figures meet:
- Resolution: 300 DPI minimum
- Format: PNG with transparency support
- Width: 6-8 inches for publication
- Style: Consistent colors and fonts
- Accessibility: Colorblind-friendly palettes

---

## Usage in Converter

The MDPI converter (`convert_clean.py`) automatically searches this directory:

```bash
cd "MDPI converter"
python3 convert_clean.py ../V8.2.3.md
```

Figures are embedded automatically when referenced as `[Figure N]`.

---

## Regenerating Figures

If you need to regenerate statistical figures:

```bash
cd "../statistical analyis"
python3 statistical_analysis_publication.py
python3 create_system_diagrams.py

# Then copy to unified directory
cp figures/*.png ../unified_figures/
```

---

## Source Directories

Figures consolidated from:
1. `statistical analyis/figures/` - Generated plots
2. `figures/` - Architectural diagrams
3. Duplicates removed automatically

---

## Figure Numbering System

- **01-09**: Statistical analysis and results
- **10-11**: System overview and study design
- **12-16**: Detailed architectural diagrams

All figures numbered consistently for easy reference.

---

## File Naming Convention

Format: `##_descriptive_name.png`

Examples:
- `01_sample_distribution.png`
- `14_detection_pipeline.png`

Clear, descriptive names make figures easy to identify and reference.

---

## Next Steps

1. Review all figures in this directory
2. Select 7 essential figures for main manuscript
3. Move remaining figures to supplementary
4. Update manuscript figure references
5. Reconvert document with unified figures

---

**Status:** Ready for use in document conversion and publication

**Location:** `V8.3/unified_figures/`

**Total:** 18 figures, publication-ready
