# MDPI Enhanced Converter - Complete Guide

## Overview

The MDPI Enhanced Converter transforms your Markdown manuscript into a fully-formatted Microsoft Word document that adheres to MDPI (Multidisciplinary Digital Publishing Institute) submission guidelines.

### Key Features

✅ **MDPI-Compliant Formatting**
- 12pt Times New Roman font throughout
- 1.5 line spacing for body text
- A4 paper size with correct margins (Top: 1.5cm, Bottom: 3.5cm, Left/Right: 1.75cm)
- Proper heading hierarchy

✅ **Automatic Figure Management**
- Inserts all 9 figures from statistical analysis
- Exports high-resolution copies to `docoutput/figures/`
- Formats figure captions per MDPI standards

✅ **Professional Table Formatting**
- MDPI-compliant table styles
- Proper table captions
- Auto-fitted columns

✅ **Abstract Handling**
- Single paragraph format (MDPI requirement)
- Removes internal headings while preserving structure

✅ **Reference Formatting**
- Ensures [1] citations appear before punctuation (MDPI style)

✅ **Complete Output Package**
- Main manuscript in DOCX format
- All figures exported separately
- Supplementary materials directory ready

---

## Quick Start

### 1. Run the Conversion

```bash
cd "/Users/huaduojiejia/MyProject/hslu/2026/paper-summay/paper_submission/MDPI converter"
./convert_to_mdpi.sh
```

### 2. Check Output

The converter creates:
```
docoutput/
├── V4_Healthcare_Submission_MDPI.docx  # Main manuscript
├── figures/                             # All 9 figures
│   ├── 01_sample_distribution.png
│   ├── 02_missing_data_heatmap.png
│   ├── 03_performance_comparison.png
│   ├── 04_effect_sizes.png
│   ├── 05_percentage_improvement.png
│   ├── 06_personality_dimensions.png
│   ├── 07_personality_heatmap.png
│   ├── 08_weighted_scores.png
│   └── 09_total_score_boxplot.png
└── supplementary/                       # Ready for supplementary materials
```

---

## MDPI Formatting Requirements Implemented

### Document Structure

✅ **Front Matter**
- Title (formatted as Heading 0)
- Abstract (single paragraph, no internal headings)
- Keywords

✅ **Main Sections**
1. Introduction (Heading 1)
2. Materials and Methods (Heading 1)
3. Results (Heading 1)
4. Discussion (Heading 1)
5. Conclusions (Heading 1)

✅ **Back Matter**
- Author Contributions
- Funding
- Institutional Review Board Statement
- Informed Consent Statement
- Data Availability Statement
- Acknowledgments
- Conflicts of Interest
- References

### Typography

| Element | Font | Size | Spacing |
|---------|------|------|---------|
| Body Text | Times New Roman | 12pt | 1.5 line spacing |
| Headings 1 | Times New Roman Bold | 16pt | 12pt before, 6pt after |
| Headings 2 | Times New Roman Bold | 14pt | 12pt before, 6pt after |
| Headings 3 | Times New Roman Bold | 12pt | 12pt before, 6pt after |
| Tables | Times New Roman | 9pt | Single spacing |
| Table Captions | Times New Roman Bold | 10pt | 6pt before, 3pt after |
| Figure Captions | Times New Roman | 10pt | 3pt before, 12pt after |

### Figures

Each figure includes:
- Centered placement
- Width: 6 inches (standard for MDPI)
- Bold figure number: "**Figure 1.**"
- Descriptive caption text
- Proper spacing before/after

### Tables

Tables are formatted with:
- Light Grid Accent 1 style
- Bold header row
- 9pt font throughout
- Centered alignment
- Table caption above table

### References

Citations follow MDPI style:
- Format: `[1]` or `[1,2,3]`
- Placement: **Before** punctuation (e.g., "text [1].")
- Superscript: No (use regular brackets)

---

## Figure Mapping

The converter automatically maps figure placeholders to actual PNG files:

| Placeholder | PNG File | Description |
|-------------|----------|-------------|
| Figure 1 | `01_sample_distribution.png` | Sample distribution across conditions |
| Figure 2 | `02_missing_data_heatmap.png` | Missing data assessment |
| Figure 3 | `06_personality_dimensions.png` | OCEAN trait distributions |
| Figure 4 | `07_personality_heatmap.png` | Personality trait heatmap |
| Figure 5 | `03_performance_comparison.png` | Performance comparison bars |
| Figure 6 | `04_effect_sizes.png` | Cohen's d effect sizes |
| Figure 7 | `05_percentage_improvement.png` | Percentage improvements |
| Figure 8 | `08_weighted_scores.png` | Weighted score distributions |
| Figure 9 | `09_total_score_boxplot.png` | Total quality score boxplots |

All figures are:
- ≥300 DPI resolution
- PNG format
- Publication-ready quality

---

## Post-Conversion Checklist

After conversion, open the Word document and verify:

### 1. Front Matter
- [ ] Title is properly formatted (large, bold, centered)
- [ ] Abstract is **single paragraph** (no line breaks between sections)
- [ ] Keywords are listed (3-10 keywords)

### 2. Figures
- [ ] All 9 figures are inserted
- [ ] Figures are centered
- [ ] Figure captions have bold numbers ("**Figure 1.**")
- [ ] Captions are descriptive and complete

### 3. Tables
- [ ] All 4 tables are present
- [ ] Table captions appear **above** tables
- [ ] Table numbers are bold ("**Table 1.**")
- [ ] Header rows are bold
- [ ] Content is readable (not too small)

### 4. References
- [ ] Citations appear as [1], [2], etc.
- [ ] Citations are **before** punctuation
- [ ] Reference list is properly formatted
- [ ] All citations in text match reference list

### 5. Formatting
- [ ] Font is Times New Roman throughout
- [ ] Body text is 12pt with 1.5 spacing
- [ ] Headings are properly hierarchical
- [ ] No orphaned headings (heading without following text)

### 6. Author Information (Manual Addition Required)
- [ ] Author names and affiliations added
- [ ] Corresponding author designated with email
- [ ] ORCID IDs added (if available)
- [ ] Author contributions statement completed

### 7. Ethics & Declarations (Manual Verification Required)
- [ ] IRB statement correct
- [ ] Conflicts of interest declared
- [ ] Funding sources listed
- [ ] Data availability statement complete

---

## Advanced Usage

### Convert with Custom Options

```bash
# Custom output directory
python3 mdpi_enhanced_converter.py input.md -o custom_output/

# Custom figures directory
python3 mdpi_enhanced_converter.py input.md -f path/to/figures/

# Custom output filename
python3 mdpi_enhanced_converter.py input.md -n my_manuscript.docx

# All options combined
python3 mdpi_enhanced_converter.py input.md \
    -o custom_output/ \
    -f path/to/figures/ \
    -n my_manuscript.docx
```

### Batch Processing

```bash
# Convert multiple manuscripts
for md in *.md; do
    python3 mdpi_enhanced_converter.py "$md" -o "output_${md%.md}/"
done
```

---

## Troubleshooting

### Issue: Figures Not Inserted

**Symptoms**: Manuscript converts but figures are missing

**Solution**:
1. Verify figures directory exists:
   ```bash
   ls -la "statistical analyis/figures/"
   ```

2. Check figure files are present (all 9 PNG files)

3. Ensure figure placeholders in markdown match format:
   ```markdown
   **[Figure 1 near here]**
   
   **Figure 1.** Caption text here.
   ```

### Issue: Tables Not Formatting Correctly

**Symptoms**: Tables appear but formatting is wrong

**Solution**:
1. Verify markdown table syntax:
   ```markdown
   **Table 1.** Caption text here.
   
   | Header 1 | Header 2 |
   |----------|----------|
   | Cell 1   | Cell 2   |
   ```

2. Ensure separator line has hyphens (not other characters)

3. Check all rows have same number of columns

### Issue: Abstract Has Multiple Paragraphs

**Symptoms**: Abstract breaks into multiple paragraphs in Word

**Solution**:
1. In the markdown, ensure abstract content is continuous
2. Remove any empty lines within the abstract section
3. Re-run conversion

### Issue: References Not Formatted Correctly

**Symptoms**: Citations appear after punctuation or in wrong format

**Solution**:
1. Ensure markdown uses square brackets: `[1]` not `(1)` or `^1^`
2. Place citations before punctuation: `text [1].` not `text. [1]`
3. For multiple citations: `[1,2,3]` not `[1] [2] [3]`

---

## MDPI Submission Process

### Before Submission

1. **Review Manuscript in Word**
   - Open `V4_Healthcare_Submission_MDPI.docx`
   - Make any necessary manual edits
   - Add author information
   - Verify all required sections are present

2. **Prepare Figures Package**
   - Zip the `figures/` directory
   - Ensure all figures are ≥300 DPI
   - Name figures clearly: `figure1.png`, `figure2.png`, etc.

3. **Create Cover Letter**
   - Explain study significance
   - Suggest reviewers (if required)
   - Declare any potential conflicts

4. **Gather Supplementary Materials**
   - Code repositories
   - Additional datasets
   - Extended methods
   - Place in `supplementary/` directory

### During Submission

1. **Go to MDPI Submission Portal**
   - Select target journal (e.g., Healthcare, Sensors, etc.)
   - Create account if needed

2. **Upload Main Manuscript**
   - Upload `V4_Healthcare_Submission_MDPI.docx`
   - Or export to PDF if preferred

3. **Upload Figures**
   - Upload each figure from `figures/` directory
   - Verify figure numbers match manuscript

4. **Add Metadata**
   - Title, authors, affiliations
   - Keywords (3-10)
   - Abstract (can copy from manuscript)

5. **Complete Declarations**
   - Ethics statements
   - Conflicts of interest
   - Funding sources
   - Author contributions

### After Submission

- MDPI will send confirmation email
- Track manuscript status in submission portal
- Respond promptly to reviewer comments
- Use the Word document for revisions

---

## Tips for Best Results

### 1. Keep Markdown Clean
- Use standard markdown syntax
- Avoid HTML tags unless necessary
- Consistent heading levels (# for H1, ## for H2, etc.)

### 2. Test Figure Placeholders
- Use exact format: `**[Figure X near here]**`
- Follow immediately with caption: `**Figure X.** Caption text.`
- Number figures sequentially (1, 2, 3...)

### 3. Table Formatting
- Use markdown tables (pipe `|` delimiter)
- Include separator line with hyphens
- Keep tables simple (complex tables may need manual adjustment)

### 4. Reference Management
- Use consistent citation format throughout
- Place citations before punctuation
- Group multiple citations: [1,2,3]

### 5. Abstract Formatting
- Write abstract as continuous text in markdown
- Use inline markers for structure (Background:, Methods:, Results:, Conclusions:)
- Do NOT use markdown headings within abstract

---

## File Locations

### Input Files
```
paper-summay/paper_submission/
├── V4_Healthcare_Submission_processed.md     # Source manuscript
└── statistical analyis/figures/               # Figures directory
    ├── 01_sample_distribution.png
    ├── 02_missing_data_heatmap.png
    └── ... (7 more figures)
```

### Output Files
```
paper-summay/paper_submission/docoutput/
├── V4_Healthcare_Submission_MDPI.docx        # Main output
├── figures/                                   # Exported figures
│   └── (all 9 PNG files)
└── supplementary/                             # Supplementary materials
```

### Converter Files
```
MDPI converter/
├── mdpi_enhanced_converter.py    # Main Python script
├── convert_to_mdpi.sh             # Convenience shell script
├── MDPI_CONVERSION_GUIDE.md       # This guide
└── requirements.txt               # Python dependencies
```

---

## Python Dependencies

The converter requires:
- `python-docx` >= 1.2.0
- `lxml` >= 6.0.0

These are installed automatically when running `convert_to_mdpi.sh`

Manual installation:
```bash
pip install python-docx
```

---

## Contact & Support

If you encounter issues:
1. Check this guide's Troubleshooting section
2. Verify MDPI guidelines haven't changed: https://www.mdpi.com/authors
3. Review the converter code for customization options

---

## Version History

### v1.0 (October 2025)
- Initial enhanced converter
- Automatic figure insertion (9 figures)
- MDPI-compliant table formatting
- Single-paragraph abstract handling
- Reference style formatting
- Complete manuscript structure support

---

## License

This converter is provided for academic research purposes.
Ensure compliance with MDPI's submission guidelines and your institution's policies.

---

**Ready to submit to MDPI! 🎓**



