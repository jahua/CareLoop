# MDPI Markdown to Word Converter

A streamlined converter specifically designed to format Markdown documents according to **MDPI (Multidisciplinary Digital Publishing Institute)** journal submission guidelines.

## MDPI Formatting Standards

This converter implements the following MDPI requirements:

### Document Formatting
- **Font**: 12pt Times New Roman
- **Line Spacing**: 1.5
- **Paper Size**: A4
- **Margins**: 
  - Top: 1.5 cm (~0.59 inches)
  - Bottom: 3.5 cm (~1.38 inches)
  - Left: 1.75 cm (~0.69 inches)
  - Right: 1.75 cm (~0.69 inches)

### Structure Requirements
- **IMRaD Format**: Introduction, Methods, Results, and Discussion
- **Mandatory Sections**:
  - Abstract (150-250 words)
  - Keywords (8-10 keywords)
  - Author Contributions
  - Funding
  - Institutional Review Board Statement
  - Informed Consent Statement
  - Data Availability Statement
  - Acknowledgments
  - Conflicts of Interest
  - References (numbered style: [1], [2], etc.)

### Content Guidelines
- **Word Count**: Typically 5,000-8,000 words (journal-specific)
- **References**: Numbered citation style [1]
- **Tables/Figures**: High resolution (≥300 dpi), numbered sequentially
- **File Size**: Total ≤120 MB

## Installation

### Prerequisites

```bash
# Python 3.7+ required
python3 --version

# Install required Python packages
pip3 install python-docx
```

### Setup

The converter is ready to use once the repository is cloned. No additional installation needed.

## Usage

### Basic Conversion

```bash
./convert_to_mdpi_docx.sh input_file.md
```

### Example

```bash
cd "/Users/yourname/path/to/MDPI converter"
./convert_to_mdpi_docx.sh ../V4_Healthcare_Submission_processed.md
```

### Output

The converted DOCX file will be saved to:
```
../docoutput/input_file.docx
```

## Features

### ✅ Automatic MDPI Formatting
- Times New Roman 12pt font throughout
- 1.5 line spacing for body text
- Proper heading hierarchy (H1-H3)
- Justified text alignment for body paragraphs

### ✅ Markdown Support
- **Bold text**: `**text**`
- *Italic text*: `*text*`
- `Inline code`: `` `code` ``
- Code blocks: ` ```code``` `
- Links: `[text](url)`
- Tables (GitHub Flavored Markdown)
- Headings: `# H1`, `## H2`, `### H3`

### ✅ Table Formatting
- Converts Markdown tables to Word tables
- Auto-fit columns
- Bold headers
- Professional table styling

### ✅ Reference Handling
- Preserves numbered references [1], [2], etc.
- Maintains bibliography formatting

### ✅ Section Structure
- Automatically preserves IMRaD structure
- Maintains all mandatory MDPI sections
- Proper heading levels and spacing

## Markdown Guidelines for MDPI

### Document Structure

```markdown
---
title: "Your Paper Title"
---

## Abstract

**Background**: ...
**Objective**: ...
**Methods**: ...
**Results**: ...
**Conclusions**: ...

**Keywords:** keyword1; keyword2; keyword3; ...

# Introduction

## Background and Motivation
...

# Materials and Methods
...

# Results
...

# Discussion
...

# Conclusions
...

# Data Availability Statement
...

# Author Contributions
...

# Funding
...

# Institutional Review Board Statement
...

# Informed Consent Statement
...

# Acknowledgments
...

# Conflicts of Interest
...

# References

1. Author, A.; Author, B. Title. *Journal* **Year**, *Volume*, Pages.
2. ...
```

### Tables

```markdown
| Header 1 | Header 2 | Header 3 |
|----------|----------|----------|
| Data 1   | Data 2   | Data 3   |
| Data 4   | Data 5   | Data 6   |
```

### Emphasis

- **Bold**: `**text**` for strong emphasis
- *Italic*: `*text*` for emphasis
- Both: `***text***`

### Code

Inline: `` `code` ``

Block:
```
```python
def function():
    pass
```
```

## Verification

After conversion, the script automatically verifies:
- Total paragraph count
- Total table count
- Total section count

## Troubleshooting

### Common Issues

**Issue**: "Permission denied" error
```bash
chmod +x convert_to_mdpi_docx.sh
```

**Issue**: "python3: command not found"
- Install Python 3.7+
- Ensure python3 is in your PATH

**Issue**: "No module named 'docx'"
```bash
pip3 install python-docx
```

**Issue**: Tables not converting properly
- Ensure table has proper Markdown syntax
- Check that all rows have the same number of columns
- Verify separator line uses `|---|---|` format

**Issue**: Formatting looks incorrect
- Open the DOCX in Microsoft Word (not preview)
- Check that original Markdown follows GitHub Flavored Markdown syntax

## MDPI Submission Checklist

After conversion, verify your document includes:

- [ ] Title (concise, ≤20 words)
- [ ] Abstract (structured, 150-250 words)
- [ ] Keywords (8-10 keywords)
- [ ] Introduction with clear objectives
- [ ] Methods section with sufficient detail for reproducibility
- [ ] Results with tables/figures
- [ ] Discussion with limitations
- [ ] Conclusions
- [ ] Data Availability Statement
- [ ] Author Contributions (CRediT format)
- [ ] Funding statement (even if "none")
- [ ] IRB Statement (even if "N/A")
- [ ] Informed Consent Statement (even if "N/A")
- [ ] Acknowledgments (if applicable)
- [ ] Conflicts of Interest declaration
- [ ] References (numbered style, with DOIs where possible)

## Official MDPI Resources

- **MDPI Instructions for Authors**: https://www.mdpi.com/authors
- **LaTeX Template**: https://www.mdpi.com/authors/latex
- **Word Template**: https://www.mdpi.com/authors/word-templates
- **Style Guide PDF**: https://mdpi-res.com/data/mdpi-author-layout-style-guide.pdf

## Comparison with Generic Converters

| Feature | MDPI Converter | Generic Converter |
|---------|----------------|-------------------|
| MDPI-specific margins | ✅ | ❌ |
| 12pt Times New Roman | ✅ | ⚠️ Variable |
| 1.5 line spacing | ✅ | ⚠️ Variable |
| IMRaD structure preservation | ✅ | ❌ |
| Numbered references | ✅ | ⚠️ May vary |
| Mandatory sections checked | ✅ | ❌ |
| MDPI table styling | ✅ | ❌ |

## Example Workflow

### 1. Write in Markdown
Write your paper in Markdown following MDPI structure:
```bash
nano manuscript.md
```

### 2. Convert to DOCX
```bash
./convert_to_mdpi_docx.sh manuscript.md
```

### 3. Review Output
```bash
open ../docoutput/manuscript.docx
```

### 4. Final Checks
- Verify all mandatory sections present
- Check table/figure quality (≥300 dpi)
- Ensure references are properly numbered
- Confirm word count (typically 5,000-8,000 words)

### 5. Submit to MDPI
- Upload via MDPI SuSy platform
- Attach supplementary materials if any
- Complete submission form

## Support

For issues specific to:
- **MDPI formatting**: Check official MDPI guidelines
- **Converter bugs**: Review error messages and verify input format
- **Markdown syntax**: Refer to GitHub Flavored Markdown guide

## License

This converter is provided as-is for academic and research purposes.

## Version

**Version**: 1.0  
**Last Updated**: October 2025  
**Compatible with**: MDPI 2025 guidelines




