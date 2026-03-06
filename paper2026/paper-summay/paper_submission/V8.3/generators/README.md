## Generators Hub (V8.3)

This folder is the **single entrypoint** for all reproducible generators:

- **analysis**: run statistical analysis + regenerate plots
- **figures**: regenerate system/workflow diagrams
- **submission**: rebuild `.docx`, retheme/crop/pad figures
- **maintenance**: renumbering / consolidation utilities

### Usage

From `paper-summay/paper_submission/V8.3/`:

```bash
# regenerate Figure 01 (study workflow diagram)
python3 "generators/figures/create_study_design_flowchart.py"

# rebuild the Word document with embedded figures
python3 "generators/submission/convert_all_figures.py"
```

### Notes

- The underlying �real� scripts remain in their original locations (e.g. `statistical analyis/`, `complete_submission/`) for compatibility.
- Any older `*/generators/*` folders now forward to this hub.

## Generators Hub (V8.3)

This folder centralizes **all generator entrypoints** (figures + docx + maintenance) in one place.

It uses thin wrapper scripts that delegate to the original implementations so existing paths/docs keep working.

### Figure / analysis generators
- `analysis/master_analysis.py`
- `analysis/statistical_analysis_publication.py`
- `analysis/create_diagrams.py`
- `analysis/create_system_diagrams.py`
- `analysis/personality_analysis.py`
- `analysis/merge_regulated.py`
- `analysis/merge_baseline.py`
- `analysis/convert_excel_to_csv.py`
- `analysis/statistical_analysis.py`

### Submission / docx generators
- `submission/convert_all_figures.py`
- `submission/convert_final.py`
- `submission/update_figure_numbers.py`
- `submission/add_all_figures_to_manuscript.py`
- `submission/retheme_pngs.py`
- `submission/crop_whitespace.py`

### Maintenance generators
- `maintenance/renumber_and_style_figures.py`
- `maintenance/consolidate_figures.py`
- `maintenance/update_figure_numbers_root.py`

### Usage
From `V8.3/`:

```bash
python3 generators/analysis/master_analysis.py
python3 generators/submission/convert_all_figures.py
```

