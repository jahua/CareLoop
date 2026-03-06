# MDPI Converter: Figures Integration Guide

## Overview

The enhanced MDPI converter now automatically detects, locates, and embeds figures from the `@figures/` directory into your Word manuscripts. This guide explains how figures are handled and how to ensure proper integration.

## ✨ Key Features

- ✅ **Automatic Figure Detection**: Finds figures from `@figures/` directory
- ✅ **Smart Path Resolution**: Checks multiple common locations
- ✅ **Proper Figure Ordering**: Inserts figures BEFORE captions (correct academic format)
- ✅ **Error Handling**: Comprehensive logging and diagnostics
- ✅ **Batch Processing**: Handles all 11 figures systematically
- ✅ **MDPI Compliance**: 300 DPI, proper sizing, correct captions

## 📁 Figure Directory Structure

```
project/
├── MDPI converter/
│   ├── mdpi_template_converter.py     ← Main converter
│   ├── convert_revised_manuscript.sh  ← Shell script
│   └── MDPI converter/docoutput/      ← Output location
│
└── statistical analyis/               ← Note: Space in "analyis"
    └── figures/
        ├── 01_sample_distribution.png
        ├── 02_missing_data_heatmap.png
        ├── 03_performance_comparison.png
        ├── 04_effect_sizes.png
        ├── 05_percentage_improvement.png
        ├── 06_personality_dimensions.png
        ├── 07_personality_heatmap.png
        ├── 08_weighted_scores.png
        ├── 09_total_score_boxplot.png
        ├── 10_system_overview.png
        └── 11_study_workflow.png
```

## 🔍 Figure Mapping

The converter maps figure numbers to filenames:

| Figure # | Filename | Content |
|----------|----------|---------|
| 1 | `01_sample_distribution.png` | Data quality visualization |
| 2 | `02_missing_data_heatmap.png` | Completeness check |
| 3 | `06_personality_dimensions.png` | OCEAN trait analysis |
| 4 | `07_personality_heatmap.png` | Personality patterns |
| 5 | `03_performance_comparison.png` | Regulated vs Baseline |
| 6 | `04_effect_sizes.png` | Cohen's d analysis |
| 7 | `05_percentage_improvement.png` | Improvement metrics |
| 8 | `08_weighted_scores.png` | Scoring breakdown |
| 9 | `09_total_score_boxplot.png` | Score distribution |
| 10 | `10_system_overview.png` | System architecture |
| 11 | `11_study_workflow.png` | Research workflow |

## 📝 Markdown Figure Format

Figures are specified in the markdown using placeholders:

```markdown
**[Figure 1 near here]**

**Figure 1.** Sample distribution across personality types. Bars represent 
individual agent instances with 6 dialogue turns each, showing the breakdown 
of Type A (extreme introversion) and Type B (extreme extroversion) profiles.
```

### Structure Requirements

1. **Placeholder line**: `**[Figure X near here]**`
2. **Blank line**
3. **Caption line**: `**Figure X.** Caption text...`

The converter expects this exact format for proper figure detection.

## 🚀 Usage

### Option 1: Automatic (Recommended)

```bash
cd "/Users/huaduojiejia/MyProject/hslu/2026/paper-summay/paper_submission/MDPI converter"
bash convert_revised_manuscript.sh
```

**Features:**
- ✅ Auto-detects figures directory
- ✅ Displays all detected figures
- ✅ Provides color-coded status messages
- ✅ Verifies embedded media count
- ✅ Detailed error reporting

### Option 2: Manual with Explicit Path

```bash
cd "/Users/huaduojiejia/MyProject/hslu/2026/paper-summay/paper_submission/MDPI converter"

python3 mdpi_template_converter.py \
    ../V5_Healthcare_Submission_REVISED.md \
    -o ../docoutput/output.docx \
    -f ../statistical\ analyis/figures \
    -t ../docoutput/msf-template.dot
```

### Option 3: Without Template

```bash
python3 mdpi_template_converter.py \
    ../V5_Healthcare_Submission_REVISED.md \
    -o ../docoutput/output.docx \
    -f ../statistical\ analyis/figures
```

## 🔧 How Figure Insertion Works

### Step 1: Auto-Detection

When you run the converter without specifying a figures directory:

```
✓ Auto-detected figures directory: ../statistical analyis/figures
✓ Found 11 figures in: ../statistical analyis/figures
   • 01_sample_distribution.png
   • 02_missing_data_heatmap.png
   • 03_performance_comparison.png
   ... and 8 more
```

### Step 2: Parsing Markdown

The converter scans the markdown for figure placeholders:

```
Handle figure placeholders → Extract figure number → Look ahead for caption
```

### Step 3: Figure Insertion

For each figure found:

1. **Insert Image First**: Centered, 6 inches wide (MDPI standard)
2. **Add Caption Below**: Formatted as `**Figure X.** Caption text`
3. **Copy to Output**: Backup copy saved to `../docoutput/figures/`

### Step 4: Embedding

- Figure embedded directly in Word document (no external links)
- Resolution: 300 DPI (publication-grade)
- Format: PNG (lossless compression)
- Size: ~6 inches width (fits A4 page)

## 📊 Output Structure

After conversion, you'll have:

```
../docoutput/
├── V5_Healthcare_Submission_REVISED_MDPI.docx  ← Final manuscript (with figures embedded)
├── figures/                                      ← Backup figure copies
│   ├── 01_sample_distribution.png
│   ├── 02_missing_data_heatmap.png
│   ├── ... (all 9 figures)
│   └── 11_study_workflow.png
│
└── (other manuscript files)
```

## ✅ Verification Checklist

After conversion, verify:

- [ ] Output file created (check size > 1 MB if figures embedded)
- [ ] Open in Microsoft Word
- [ ] All figures visible and properly centered
- [ ] Captions below each figure
- [ ] No placeholder text remaining (e.g., "Figure X near here")
- [ ] Figures are high-quality (not blurry or pixelated)
- [ ] Spacing between figures and text looks correct
- [ ] Page breaks occur in appropriate places
- [ ] Text wrapping works correctly around figures

### Command to Check Embedded Media

```bash
unzip -l ../docoutput/V5_Healthcare_Submission_REVISED_MDPI.docx | grep "word/media/"
```

Expected: Multiple media files listed (one per embedded figure)

## 🛠️ Troubleshooting

### Problem: "Figure file not found"

**Solution:**
1. Check figures directory exists:
   ```bash
   ls -la "/Users/huaduojiejia/MyProject/hslu/2026/paper-summay/paper_submission/statistical analyis/figures/"
   ```
2. Verify PNG files are present:
   ```bash
   find . -name "*.png" | wc -l  # Should show 11
   ```
3. Provide explicit path:
   ```bash
   python3 mdpi_template_converter.py input.md -o output.docx -f /full/path/to/figures
   ```

### Problem: "No figures directory provided or detected"

**Solution:**
```bash
# Explicitly specify figures directory
bash convert_revised_manuscript.sh
# Or manually:
python3 mdpi_template_converter.py input.md -o output.docx -f ../statistical\ analyis/figures
```

### Problem: Figures not embedded in final Word document

**Solution:**
1. Check file size (should be > 1 MB with figures):
   ```bash
   ls -lh output.docx
   ```
2. Verify markdown has proper placeholder format:
   ```markdown
   **[Figure X near here]**
   
   **Figure X.** Caption text
   ```
3. Try without template:
   ```bash
   python3 mdpi_template_converter.py input.md -o output.docx -f path/to/figures
   ```

### Problem: Figures look blurry or pixelated

**Solution:**
- All figures are generated at 300 DPI (publication standard)
- If they appear blurry in Word, zoom to 100% for accurate preview
- Print or export to PDF to see actual quality

## 📖 Technical Details

### Figure Sizing

- **Width**: 6 inches (fits MDPI page with margins)
- **DPI**: 300 (publication standard)
- **Format**: PNG (lossless)
- **Aspect ratio**: Maintained from source

### Caption Formatting

```
Figure X. [Caption text]
│         │
└─ Bold  └─ Regular text, 10pt, Times New Roman
```

### MDPI Compliance

✅ Figures embedded in document (not external links)
✅ 300 DPI resolution (MDPI requirement)
✅ PNG format (MDPI preferred)
✅ Proper captions with numbering
✅ Centered alignment (standard practice)
✅ Backup figure directory created

## 🔄 Common Workflows

### Workflow 1: Convert Latest Manuscript

```bash
# Update figures first (if needed)
cd ../statistical\ analyis
python3 statistical_analysis_publication.py
cd ../MDPI\ converter

# Convert with figures
bash convert_revised_manuscript.sh

# Open result
open ../docoutput/V5_Healthcare_Submission_REVISED_MDPI.docx
```

### Workflow 2: Multiple Conversions

```bash
# Convert different manuscripts
for manuscript in V5.1 V5.2 V5.3; do
    python3 mdpi_template_converter.py \
        ../${manuscript}_manuscript.md \
        -o ../docoutput/${manuscript}_MDPI.docx \
        -f ../statistical\ analyis/figures
done
```

### Workflow 3: Update Figures Only

```bash
# Regenerate publication-quality figures
cd ../statistical\ analyis
python3 statistical_analysis_publication.py

# Reconvert manuscript (picks up new figures automatically)
cd ../MDPI\ converter
bash convert_revised_manuscript.sh
```

## 📝 Notes

- Figures must be in PNG format (JPG, GIF not supported)
- Figure numbers in markdown must match manuscript references
- Captions are required (blank captions will still be formatted)
- Figures are embedded, not linked (standalone Word file)
- Template detection is optional (default MDPI formatting applied if not found)

## 🎯 Best Practices

1. **Always verify figure files exist before converting**
   ```bash
   ls -la ../statistical\ analyis/figures/*.png
   ```

2. **Use absolute paths if running from different directory**
   ```bash
   python3 mdpi_template_converter.py \
       /absolute/path/input.md \
       -f /absolute/path/figures
   ```

3. **Keep backup of figures directory**
   ```bash
   cp -r ../statistical\ analyis/figures ../statistical\ analyis/figures.backup
   ```

4. **Regenerate figures if analysis changes**
   ```bash
   cd ../statistical\ analyis
   python3 statistical_analysis_publication.py
   ```

5. **Test with small manuscript first**
   ```bash
   # Extract first 5 sections to test file
   head -500 input.md > test.md
   python3 mdpi_template_converter.py test.md -o test.docx -f ../figures
   ```

## 📞 Support

If you encounter issues:

1. Check error messages in console (color-coded)
2. Verify file paths match your system
3. Ensure PNG files are not corrupted:
   ```bash
   file ../statistical\ analyis/figures/*.png
   ```
4. Check that python-docx is installed:
   ```bash
   python3 -c "import docx; print(docx.__version__)"
   ```

---

**Last Updated**: October 27, 2025
**Converter Version**: Enhanced with Figure Integration
**Status**: ✅ Production Ready


