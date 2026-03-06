# Complete Workflow: Markdown to MDPI Word Document

**Version:** 1.0  
**Date:** January 16, 2026  
**Status:** Production Ready

---

## Quick Start (2 Steps)

### Step 1: Generate Figures

```bash
cd "paper-summay/paper_submission/V8.3/statistical analyis"
python3 master_analysis.py
python3 create_diagrams.py
```

**Time:** ~20 seconds  
**Output:** 7 figures in `./figures/` directory

### Step 2: Convert to Word

```bash
cd "../MDPI converter"
python3 convert_clean.py ../V8.2.3.md ../V8.2.3_MDPI.docx
```

**Time:** ~3 seconds  
**Output:** `V8.2.3_MDPI.docx` with MDPI formatting

---

## Complete Workflow

### Prerequisites

```bash
# Check Python version
python3 --version  # Requires 3.7+

# Install dependencies
cd "statistical analyis"
pip install pandas numpy matplotlib seaborn scipy

cd "../MDPI converter"
pip install python-docx PyYAML
```

### Step-by-Step Process

#### 1. Generate Statistical Figures

```bash
# Navigate to statistical analysis directory
cd "paper-summay/paper_submission/V8.3/statistical analyis"

# Generate core analysis figures (4 figures)
python3 master_analysis.py
```

**Generates:**
- `figures/01_performance_comparison.png`
- `figures/02_effect_sizes.png`
- `figures/03_personality_needs.png`
- `figures/04_sample_quality.png`

```bash
# Generate system diagrams (2 figures)
python3 create_diagrams.py
```

**Generates:**
- `figures/06_system_architecture.png`
- `figures/07_study_workflow.png`

```bash
# Optional: Generate personality profiles
python3 personality_analysis.py
```

**Generates:**
- `figures/05_personality_profiles.png`

#### 2. Verify Figures Generated

```bash
ls -lh figures/
```

**Expected output:**
```
01_performance_comparison.png  ~110 KB
02_effect_sizes.png           ~125 KB
03_personality_needs.png       ~85 KB
04_sample_quality.png         ~115 KB
05_personality_profiles.png   ~295 KB (optional)
06_system_architecture.png    ~215 KB
07_study_workflow.png         ~235 KB
```

#### 3. Convert Markdown to Word

```bash
# Navigate to MDPI converter
cd "../MDPI converter"

# Run conversion
python3 convert_clean.py ../V8.2.3.md ../V8.2.3_MDPI.docx "../statistical analyis/figures"
```

**Alternative (auto-detect figures):**
```bash
python3 convert_clean.py ../V8.2.3.md
```

#### 4. Verify Output

```bash
# Check file created
ls -lh ../V8.2.3_MDPI.docx

# Expected: ~5-10 MB with embedded figures
```

---

## Conversion Script Features

### MDPI Formatting Applied

? **Page Setup**
- A4 paper size (21.0 � 29.7 cm)
- Margins: Top 1.5cm, Bottom 3.5cm, Left/Right 1.75cm

? **Typography**
- Font: Times New Roman
- Size: 12pt body, 16-18pt title
- Line spacing: 1.5
- Alignment: Justified

? **Structure**
- Title page from YAML front matter
- Automatic heading hierarchy (H1, H2, H3)
- Figure insertion at references
- List formatting (bullet and numbered)

? **Figures**
- Automatic detection from `[Figure N]` references
- Centered alignment
- 6-inch width (publication standard)
- Maintains aspect ratio

---

## Figure Numbering

The converter uses the reorganized figure numbering:

| Figure # | Filename | Description |
|----------|----------|-------------|
| 1 | `01_performance_comparison.png` | Main results |
| 2 | `02_effect_sizes.png` | Cohen's d |
| 3 | `03_personality_needs.png` | Primary outcome |
| 4 | `04_sample_quality.png` | Sample info |
| 5 | `05_personality_profiles.png` | OCEAN (optional) |
| 6 | `06_system_architecture.png` | System pipeline |
| 7 | `07_study_workflow.png` | Study design |

**Note:** Figures 8-16 from old versions are deprecated. Update your manuscript to use figures 1-7.

---

## Troubleshooting

### Problem: Figures Not Found

**Symptom:**
```
? Warning: Figure not found: ../statistical analyis/figures/01_performance_comparison.png
```

**Solution:**
```bash
# Generate figures first
cd "../statistical analyis"
python3 master_analysis.py
python3 create_diagrams.py
cd "../MDPI converter"

# Then convert
python3 convert_clean.py ../V8.2.3.md
```

### Problem: Unknown Figure Number

**Symptom:**
```
? Warning: Unknown figure number: 10
```

**Solution:**
This means your markdown references old figure numbers. Update your manuscript:
- Change `[Figure 10]` ? `[Figure 6]` (system architecture)
- Change `[Figure 11]` ? `[Figure 7]` (study workflow)

See figure mapping table above for complete conversions.

### Problem: python-docx Not Installed

**Symptom:**
```
Error: python-docx not installed
```

**Solution:**
```bash
pip install python-docx PyYAML
```

### Problem: Module Import Error

**Symptom:**
```
ModuleNotFoundError: No module named 'visualization_config'
```

**Solution:**
Make sure you're in the correct directory:
```bash
cd "statistical analyis"
python3 master_analysis.py
```

---

## Advanced Usage

### Custom Figure Directory

```bash
python3 convert_clean.py input.md output.docx /path/to/figures
```

### Different Output Name

```bash
python3 convert_clean.py V8.2.3.md V8.2.3_Submission.docx
```

### Process Different Markdown File

```bash
python3 convert_clean.py ../V8.md ../V8_MDPI.docx
```

---

## Workflow Automation

Create a shell script for the complete workflow:

```bash
#!/bin/bash
# File: convert_complete.sh

echo "=== Complete Markdown to Word Workflow ==="

# Step 1: Generate figures
echo "Step 1: Generating figures..."
cd "../statistical analyis"
python3 master_analysis.py
python3 create_diagrams.py

# Step 2: Convert to Word
echo "Step 2: Converting to Word..."
cd "../MDPI converter"
python3 convert_clean.py ../V8.2.3.md ../V8.2.3_MDPI.docx

echo "=== Complete! ==="
echo "Output: V8.2.3_MDPI.docx"
```

Make executable and run:
```bash
chmod +x convert_complete.sh
./convert_complete.sh
```

---

## Quality Checklist

After conversion, verify:

- [ ] Document opens in Word without errors
- [ ] Title displays correctly
- [ ] All headings properly formatted
- [ ] Figures appear in correct locations
- [ ] Figures are high quality (not pixelated)
- [ ] Citations formatted correctly
- [ ] Page margins correct (1.5/3.5/1.75/1.75 cm)
- [ ] Font is Times New Roman, 12pt
- [ ] Line spacing is 1.5
- [ ] Text is justified
- [ ] No placeholder figure references

---

## File Structure

```
V8.3/
??? V8.2.3.md                          (Input markdown)
??? V8.2.3_MDPI.docx                   (Output Word doc)
?
??? statistical analyis/
?   ??? master_analysis.py             (Generate analysis figures)
?   ??? create_diagrams.py             (Generate system diagrams)
?   ??? personality_analysis.py        (Optional)
?   ??? figures/
?       ??? 01_performance_comparison.png
?       ??? 02_effect_sizes.png
?       ??? 03_personality_needs.png
?       ??? 04_sample_quality.png
?       ??? 05_personality_profiles.png
?       ??? 06_system_architecture.png
?       ??? 07_study_workflow.png
?
??? MDPI converter/
    ??? convert_clean.py               (Clean converter script)
    ??? requirements.txt               (Dependencies)
```

---

## Next Steps After Conversion

### 1. Review in Word

1. Open `V8.2.3_MDPI.docx`
2. Check formatting
3. Verify figures
4. Review for MDPI compliance

### 2. Final Adjustments

- Add author information
- Insert keywords
- Add acknowledgments section
- Check references formatting
- Verify supplementary materials

### 3. Export to PDF

```
File ? Save As ? PDF
```

### 4. Submit to MDPI

1. Create submission package
2. Include Word document
3. Include original figures (separate files)
4. Add cover letter

---

## Summary

**Complete workflow:**

```bash
# 1. Generate figures (~20s)
cd "statistical analyis"
python3 master_analysis.py && python3 create_diagrams.py

# 2. Convert to Word (~3s)
cd "../MDPI converter"
python3 convert_clean.py ../V8.2.3.md

# 3. Done!
open ../V8.2.3_MDPI.docx
```

**Total time:** ~25 seconds  
**Output:** Publication-ready Word document with MDPI formatting

---

## Support

For issues:
1. Check this guide
2. Review error messages
3. Verify all dependencies installed
4. Ensure figures generated before conversion

---

**Last Updated:** January 16, 2026  
**Script Version:** 1.0  
**Status:** Production Ready
