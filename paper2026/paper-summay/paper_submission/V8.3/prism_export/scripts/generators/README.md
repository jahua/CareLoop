# Generator Scripts

**Organized**: 2026-02-03  
**Location**: `prism_export/scripts/generators/`  
**Status**: ✅ Production-ready

---

## 📁 Directory Structure

```
generators/
├── README.md                    # This file
├── _run.py                      # Legacy main runner
├── analysis/                    # Statistical analysis generators
│   ├── create_diagrams.py
│   ├── create_system_diagrams.py
│   ├── enhanced_figures.py
│   ├── enhanced_statistical_analysis.py
│   ├── master_analysis.py
│   └── statistical_analysis_publication.py
├── diagrams/                    # System diagram generators
│   ├── create_study_design_flowchart.py
│   └── create_submission_diagrams.py
├── submission/                  # Submission preparation tools
│   ├── add_all_figures_to_manuscript.py
│   ├── add_safe_padding.py
│   ├── convert_all_figures.py
│   ├── convert_final.py
│   ├── crop_whitespace.py
│   ├── restyle_to_workflow_theme.py
│   └── retheme_pngs.py
├── maintenance/                 # Maintenance utilities
│   ├── consolidate_figures.py
│   ├── renumber_and_style_figures.py
│   └── update_figure_numbers.py
└── utils/                       # Shared utilities (empty for now)
```

---

## 🎯 Purpose

This directory contains **legacy and specialized generator scripts** for:

1. **Analysis**: Statistical analysis and plot generation
2. **Diagrams**: System architecture and workflow diagrams
3. **Submission**: Document conversion and figure preparation
4. **Maintenance**: Figure renumbering and consolidation

---

## ⚠️ Important Notes

### Main Generator Script

**For most use cases, use the main generator script instead**:

```bash
cd ..  # Go to scripts/
python3 generate_all_figures.py
```

This is the **recommended** entry point that:
- ✅ Uses Cliff's delta (NOT Cohen's d)
- ✅ Generates all publication figures
- ✅ Includes dialogue illustrations
- ✅ Well-documented and tested

### Legacy Scripts

The scripts in this `generators/` subdirectory are:
- Legacy code from earlier development
- May contain redundant functionality
- Some may still use Cohen's d (needs verification)
- Kept for reference and backward compatibility

---

## 📊 Script Categories

### 1. Analysis Scripts (`analysis/`)

Generate statistical analysis and plots:

| Script | Purpose | Status |
|--------|---------|--------|
| `master_analysis.py` | Main analysis orchestrator | ⚠️ Legacy |
| `statistical_analysis_publication.py` | Publication-ready analysis | ⚠️ Check effect sizes |
| `enhanced_statistical_analysis.py` | Enhanced analysis | ⚠️ May duplicate parent |
| `create_diagrams.py` | Generate analysis diagrams | 📋 Review |
| `create_system_diagrams.py` | System architecture diagrams | 📋 Review |
| `enhanced_figures.py` | Enhanced figure generation | 📋 Review |

**Recommendation**: Use `../generate_all_figures.py` instead for new work.

### 2. Diagram Scripts (`diagrams/`)

Generate system architecture and workflow diagrams:

| Script | Purpose | Notes |
|--------|---------|-------|
| `create_study_design_flowchart.py` | Figure 1 (study design) | Manual diagram preferred |
| `create_submission_diagrams.py` | Multiple system diagrams | May be outdated |

**Note**: System diagrams are typically created manually with draw.io for better quality.

### 3. Submission Scripts (`submission/`)

Prepare figures and documents for journal submission:

| Script | Purpose | Use Case |
|--------|---------|----------|
| `convert_all_figures.py` | Convert figures to submission format | Pre-submission |
| `convert_final.py` | Final conversion before submission | Final check |
| `add_all_figures_to_manuscript.py` | Embed figures in Word doc | DOCX workflow |
| `retheme_pngs.py` | Apply consistent theme to PNGs | Styling |
| `crop_whitespace.py` | Remove whitespace from figures | Optimization |
| `add_safe_padding.py` | Add padding for print safety | Print prep |
| `restyle_to_workflow_theme.py` | Apply workflow theme | Consistency |

### 4. Maintenance Scripts (`maintenance/`)

Figure management and renumbering:

| Script | Purpose | When to Use |
|--------|---------|-------------|
| `consolidate_figures.py` | Consolidate figures from multiple sources | After reorganization |
| `renumber_and_style_figures.py` | Renumber figures sequentially | Figure order changes |
| `update_figure_numbers.py` | Update figure references in text | After renumbering |

---

## 🚀 Usage

### Recommended Workflow

**For new analysis**:
```bash
cd /path/to/prism_export/scripts
python3 generate_all_figures.py
```

**For legacy scripts**:
```bash
cd /path/to/prism_export/scripts/generators

# Analysis
python3 analysis/master_analysis.py

# Diagrams
python3 diagrams/create_study_design_flowchart.py

# Submission prep
python3 submission/convert_all_figures.py

# Maintenance
python3 maintenance/consolidate_figures.py
```

---

## ⚠️ Cohen's d vs Cliff's Delta

**CRITICAL**: Some legacy scripts may still use Cohen's d.

### Before Running Any Script

Check for Cohen's d usage:
```bash
grep -i "cohen" script_name.py
```

If Cohen's d is found:
1. ⚠️ Do NOT use for publication
2. ✅ Use `../generate_all_figures.py` instead
3. Or update script to use Cliff's delta

### Why This Matters

Our data:
- ❌ Bounded [0, 1]
- ❌ Ordinal discrete values
- ❌ Ceiling effects
- ❌ Near-zero variance

**Cohen's d produces meaningless values** (e.g., d = 4.651 artifact)  
**Cliff's delta provides interpretable results** (e.g., δ = 0.917 = 91.7% dominance)

---

## 📚 Documentation

### Main Documentation

- **Generation Guide**: `../FIGURE_GENERATION_GUIDE.md`
- **Script Summary**: `../../SCRIPT_GENERATION_SUMMARY.md`
- **Effect Size Updates**: `../../EFFECT_SIZE_UPDATE_SUMMARY.md`

### Legacy Documentation

- **Original README**: `README.md` (this file, from original generators/)
- **Legacy structure**: Preserved for backward compatibility

---

## 🔧 Migration Status

### Migrated to Parent Directory

These functionalities are now in `../`:

| Legacy Location | New Location | Status |
|----------------|--------------|--------|
| `analysis/enhanced_statistical_analysis.py` | `../enhanced_statistical_analysis.py` | ✅ Migrated |
| Various analysis functions | `../generate_all_figures.py` | ✅ Consolidated |
| Visualization config | `../visualization_config.py` | ✅ Migrated |
| Dialogue illustrations | `../generate_all_figures.py` | ✅ Integrated |

### Remaining in generators/

Legacy scripts kept for:
- Backward compatibility
- Specialized tools (DOCX conversion, renumbering)
- Reference implementation

---

## 🗂️ File Organization

### Parent Directory (`scripts/`)

**Active scripts** (use these):
```
scripts/
├── generate_all_figures.py          ⭐ Main generator (Cliff's delta)
├── enhanced_statistical_analysis.py  ⭐ Core analysis functions
├── visualization_config.py           ⭐ Plot configuration
├── statistical_analysis_enhanced.ipynb ⭐ Interactive notebook
├── FIGURE_GENERATION_GUIDE.md       📚 Complete guide
└── README.md                        📚 Project overview
```

### This Directory (`scripts/generators/`)

**Legacy scripts** (reference only):
```
generators/
├── analysis/          # Statistical analysis (legacy)
├── diagrams/          # System diagrams (manual preferred)
├── submission/        # DOCX/figure conversion tools
├── maintenance/       # Figure management utilities
└── README.md          # This file
```

---

## ✅ Best Practices

### Do's ✅

1. ✅ Use `../generate_all_figures.py` for new work
2. ✅ Verify Cliff's delta usage before running legacy scripts
3. ✅ Check output against main generator for consistency
4. ✅ Document any updates to legacy scripts
5. ✅ Keep this README updated

### Don'ts ❌

1. ❌ Don't use scripts with Cohen's d for publication
2. ❌ Don't assume legacy scripts are up-to-date
3. ❌ Don't modify without checking dependencies
4. ❌ Don't bypass the main generator without good reason
5. ❌ Don't delete without verifying no active usage

---

## 🐛 Troubleshooting

### "Script uses Cohen's d"

**Problem**: Legacy script contains Cohen's d calculations

**Solution**: Use main generator instead:
```bash
cd ..
python3 generate_all_figures.py
```

### "Module not found"

**Problem**: Script can't find dependencies

**Solution**: Run from correct directory:
```bash
# For main generator
cd /path/to/prism_export/scripts
python3 generate_all_figures.py

# For legacy scripts
cd /path/to/prism_export/scripts/generators
python3 analysis/script_name.py
```

### "Figure numbers don't match"

**Problem**: Inconsistent figure numbering

**Solution**: Use maintenance script:
```bash
python3 maintenance/renumber_and_style_figures.py
```

---

## 📝 Maintenance Log

### 2026-02-03: Initial Organization

- ✅ Moved all generator scripts from `V8.3/generators/`
- ✅ Created organized subdirectory structure
- ✅ Created comprehensive README
- ✅ Verified Cliff's delta in main generator
- ✅ Documented migration status

### Future Maintenance

- 🔄 Audit legacy scripts for Cohen's d usage
- 🔄 Update or deprecate outdated scripts
- 🔄 Consolidate redundant functionality
- 🔄 Add automated tests for critical generators

---

## 🎯 Summary

**Quick Reference**:

| Task | Command |
|------|---------|
| **Generate all figures** | `cd .. && python3 generate_all_figures.py` |
| **Statistical analysis** | Use main generator or notebook |
| **System diagrams** | Create manually with draw.io |
| **Submission prep** | `python3 submission/convert_all_figures.py` |
| **Renumber figures** | `python3 maintenance/renumber_and_style_figures.py` |

**Remember**: ⭐ Use `../generate_all_figures.py` for most tasks (uses Cliff's delta ✅)

---

**Location**: `prism_export/scripts/generators/`  
**Last Updated**: 2026-02-03  
**Status**: ✅ Organized and documented
