# Figures Quick Reference Guide

## Essential Figures for Manuscript Submission (7 total)

| # | Filename | Size | Use In Manuscript |
|---|----------|------|-------------------|
| **10** | `10_system_overview.png` | 108 KB | Section 3.2 - System Architecture |
| **11** | `11_study_design_flowchart.png` | 474 KB | Section 3.4 - Experimental Materials |
| **12** | `12_evaluation_framework.png` | 136 KB | Section 3.5 - Evaluation Procedure |
| **13** | `13_data_flow_pipeline.png` | 255 KB | Section 3.2.2 - Data Flow Pipeline |
| **14** | `14_detection_pipeline_layered.png` | 322 KB | Section 3.3.1 - Detection Pipeline ? |
| **15** | `15_regulation_prompt_assembly.png` | 181 KB | Section 3.3.2 - Regulation |
| **16** | `16_trait_to_zurich_mapping.png` | 423 KB | Section 3.3.2 - Trait Mapping |

? = Newly improved with layered architecture

## Key Improvements Made

### Figure 10 - System Overview
**Before**: 5-layer detailed architecture  
**After**: Simple 4-box flow + Quality Assurance layer  
**Benefit**: Matches manuscript Section 3.2 description perfectly

### Figure 14 - Detection Pipeline ? NEW
**Before**: Linear chain (User ? Detection ? Parsing ? Update)  
**After**: 3-layer architecture with 5 parallel OCEAN detectors  
**Benefit**: Shows modularity, parallelization, clear interfaces

**Layers**:
1. **Input Layer**: User message + dialogue context
2. **Inference Layer**: 5 parallel trait detectors (O, C, E, A, N)
3. **State & Interface**: Cumulative evidence + regulation interface

**Why better**: Reviewers immediately see:
- ? Modular architecture
- ? Parallel processing  
- ? Separation of concerns
- ? Clear interfaces between components

## Alternative Versions (Keep for Reference)

These are kept but NOT recommended for the manuscript:

- `10_system_architecture.png` (331 KB) - Detailed 5-layer version
- `11_study_workflow.png` (341 KB) - Simplified study flow
- `12_evaluation_framework_alt.png` (430 KB) - Alternative evaluation view
- `14_detection_pipeline.png` (128 KB) - Linear flow version

## Quick Actions

### Regenerate All Essential Figures
```bash
cd figures/src
python generate_all.py
```
Generates: Figures 10, 11, 12, 13, 14 (layered)

### Regenerate Specific Figure
```bash
cd figures/src
python create_system_overview.py           # Figure 10
python create_study_design_flowchart.py    # Figure 11
python create_submission_diagrams.py       # Figures 12, 13
python create_detection_architecture.py    # Figure 14 (layered)
```

### View Documentation
```bash
cat figures/src/README.md                       # Technical docs
cat figures/DETECTION_PIPELINE_IMPROVEMENT.md   # Figure 14 comparison
cat figures/FIGURE_GENERATION_SUMMARY.txt       # Complete summary
```

## Manuscript Figure References

When citing in your manuscript:

```latex
**Figure 10.** System architecture overview showing...
**Figure 11.** Experimental workflow and study design...
**Figure 12.** Evaluation framework with scoring criteria...
**Figure 13.** End-to-end data processing pipeline...
**Figure 14.** Personality detection pipeline with parallel OCEAN trait inference...
**Figure 15.** Regulation prompt assembly workflow...
**Figure 16.** Mapping from Big Five traits to Zurich Model motivational domains...
```

## File Locations

```
V8.3/
??? figures/
?   ??? 10_system_overview.png                  ? Use this
?   ??? 11_study_design_flowchart.png           ? Use this
?   ??? 12_evaluation_framework.png             ? Use this
?   ??? 13_data_flow_pipeline.png               ? Use this
?   ??? 14_detection_pipeline_layered.png       ? Use this ?
?   ??? 15_regulation_prompt_assembly.png       ? Use this
?   ??? 16_trait_to_zurich_mapping.png          ? Use this
?   ?
?   ??? src/                                    ? All generation scripts
?   ??? QUICK_REFERENCE.md                      ? This file
?   ??? DETECTION_PIPELINE_IMPROVEMENT.md       ? Figure 14 details
?   ??? FIGURE_GENERATION_SUMMARY.txt           ? Complete summary
?
??? V8.2.5.md                                   ? Main manuscript
```

## Dependencies

**Required**: Python 3.9+, matplotlib >= 3.5.0  
**Optional**: Graphviz (only for regenerating Figures 15-16 from .dot source)

Install:
```bash
pip install matplotlib
```

## Status

? All 7 essential figures generated and verified  
? Figure 10 redesigned to match manuscript  
? Figure 14 improved with layered architecture  
? All scripts self-contained and documented  
? Ready for manuscript submission  

## Support

For questions or regeneration issues:
1. Check `src/README.md` for detailed documentation
2. Check `DETECTION_PIPELINE_IMPROVEMENT.md` for Figure 14 details
3. Check `FIGURE_GENERATION_SUMMARY.txt` for complete overview
