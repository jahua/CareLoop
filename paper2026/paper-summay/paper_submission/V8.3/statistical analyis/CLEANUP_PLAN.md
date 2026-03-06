# Directory Cleanup and Organization Plan

## Current Status: 67 items (too many!)

## Target Structure

```
statistical_analyis/
??? ?? NOTEBOOKS (Main Analysis)
?   ??? statistical_analysis_enhanced.ipynb          ? KEEP (main notebook)
?
??? ?? CORE SCRIPTS (Essential)
?   ??? enhanced_statistical_analysis.py             ? KEEP (main functions)
?   ??? visualization_config.py                      ? KEEP (configuration)
?   ??? plotting_example.py                          ? KEEP (examples)
?
??? ?? DATA (Input)
?   ??? 1-Evaluation-Simulated-Conversations.xlsx    ? KEEP (source)
?   ??? data/                                        ? KEEP (CSV files)
?   ??? merged/                                      ? KEEP (processed)
?
??? ?? FIGURES (Output)
?   ??? figures/                                     ? KEEP (all figures)
?
??? ?? DOCUMENTATION (Essential Only)
?   ??? README_MASTER.md                             ? KEEP (main guide)
?   ??? QUICK_START.md                               ? KEEP (quick ref)
?   ??? ALL_IMPROVEMENTS_FINAL.md                    ? KEEP (complete list)
?   ??? requirements.txt                             ? KEEP (dependencies)
?
??? ??? ARCHIVE (Moved, not deleted)
    ??? old_versions/                                ? Old scripts/notebooks
    ??? one_time_scripts/                            ? Build/conversion scripts
    ??? intermediate_results/                        ? CSV results
    ??? extra_docs/                                  ? Redundant documentation
```

## Files to Archive/Delete

### Old Versions ? _archive/old_versions/
- statistical_analysis_enhanced.executed.ipynb (old execution)
- statistical_analysis.ipynb (old version)
- statistical_analysis_publication.py (old script)
- master_analysis.py (old script)
- seaborn_visualizations.py (superseded)
- personality_analysis.py (superseded)

### One-Time Scripts ? _archive/one_time_scripts/
- convert_excel_to_csv.py
- merge_baseline.py
- merge_regulated.py
- create_enhanced_notebook.py
- create_improved_notebook.py
- create_diagrams.py
- create_study_design_flowchart.py
- create_submission_diagrams.py
- create_system_diagrams.py
- diagram_theme.py
- run_analysis.sh

### Intermediate Results ? _archive/intermediate_results/
- analysis_results_advanced_tests.csv
- analysis_results_descriptive.csv
- analysis_results_effect_sizes.csv
- analysis_results_inferential.csv
- analysis_results_summary.csv
- analysis_report.txt
- regulated_with_scores.csv
- baseline_with_scores.csv
- regulated_with_personality.csv

### Redundant Documentation ? _archive/extra_docs/
- README.md (superseded by README_MASTER.md)
- README_IMPROVEMENTS.md (superseded)
- NOTEBOOK_GUIDE.md (superseded)
- INDEX.md (superseded)
- ANALYSIS_GUIDE.md (superseded)
- ENHANCED_NOTEBOOK_GUIDE.md (superseded)
- PUBLICATION_READY_ANALYSIS_SUMMARY.md (superseded)
- SETUP_COMPLETE.md (no longer relevant)
- REORGANIZATION_COMPLETE.md (no longer relevant)
- REORGANIZATION_SUMMARY.md (no longer relevant)
- IMPROVEMENTS_SUMMARY.txt (superseded by markdown version)
- FIGURE_CAPTIONS.md (redundant with main docs)

### Python Cache ? DELETE
- __pycache__/ (Python cache, regenerates automatically)

### Keep as Reference (Detailed Docs)
- GUIDE_CONFIGURATION_COMPLETE.md (guide implementation details)
- MATPLOTLIB_FOR_PAPERS_UPDATES.md (specific techniques)
- PLOTTING_IMPROVEMENTS.md (theory)
- DATA_QUALITY_VISUALIZATION_IMPROVED.md (data quality specifics)
- CORRECTED_INTERPRETATIONS.md (interpretation guide)
- NOTEBOOK_INTERPRETATION_CORRECTIONS.md (corrections)
- NOTEBOOK_UPDATES_COMPLETE.md (notebook changes)
- HEATMAP_COLORS_FIXED.md (color explanation)
- DEFAULT_COLORS_SUMMARY.md (color reference)
- COLOR_SCHEME_UPDATE.md (color details)
- STACKED_BAR_CHART_REDESIGN.md (chart redesign)
- XAXIS_LABELING_FIXED.md (labeling fixes)
- FIGURE3_OVERLAP_FIXED.md (overlap fixes)

## Execution Plan

1. Create archive directories
2. Move old versions to archive
3. Move one-time scripts to archive
4. Move intermediate results to archive
5. Move redundant docs to archive
6. Delete Python cache
7. Organize remaining documentation
8. Create final README

## Final Clean Structure (Target: ~25-30 items)

**Core files:** 3 Python scripts + 1 notebook = 4  
**Data:** 3 locations = 3  
**Figures:** 1 directory = 1  
**Documentation:** ~10 essential docs = 10  
**Archive:** 1 directory = 1  
**Total:** ~19 items in root (clean!)
