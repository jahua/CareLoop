# Clean MDPI Converter

**Version:** 1.0  
**Status:** Production Ready

---

## Overview

Streamlined Python script to convert academic markdown manuscripts to MDPI-formatted Word documents.

**Key Features:**
- ? YAML front matter extraction
- ? Automatic figure insertion
- ? MDPI-compliant formatting (Times New Roman, 1.5 spacing, A4)
- ? Clean, maintainable code (~400 lines)
- ? Compatible with reorganized figure pipeline (V2.0)

---

## Quick Start

### Install Dependencies

```bash
pip install python-docx PyYAML
```

### Convert Document

```bash
python3 convert_clean.py input.md output.docx
```

**Example:**
```bash
python3 convert_clean.py ../V8.2.3.md ../V8.2.3_MDPI.docx
```

---

## Usage

### Basic

```bash
python3 convert_clean.py input.md
```

Output: `input.docx` (same name as input)

### Specify Output Name

```bash
python3 convert_clean.py input.md custom_output.docx
```

### Custom Figures Directory

```bash
python3 convert_clean.py input.md output.docx /path/to/figures
```

**Auto-detection:** If not specified, looks for figures in:
1. `../statistical analyis/figures/` (reorganized pipeline)
2. `../figures/` (fallback)

---

## Figure Mapping

Uses reorganized figure numbering (V2.0):

| Ref | Filename |
|-----|----------|
| `[Figure 1]` | `01_performance_comparison.png` |
| `[Figure 2]` | `02_effect_sizes.png` |
| `[Figure 3]` | `03_personality_needs.png` |
| `[Figure 4]` | `04_sample_quality.png` |
| `[Figure 5]` | `05_personality_profiles.png` |
| `[Figure 6]` | `06_system_architecture.png` |
| `[Figure 7]` | `07_study_workflow.png` |

---

## MDPI Formatting

Applied automatically:

**Page Setup:**
- Paper: A4 (21.0 � 29.7 cm)
- Margins: 1.5cm (top), 3.5cm (bottom), 1.75cm (left/right)

**Typography:**
- Font: Times New Roman
- Size: 12pt (body), 14-18pt (headings)
- Spacing: 1.5 lines
- Alignment: Justified

**Figures:**
- Width: 6 inches
- Alignment: Centered
- High resolution maintained

---

## Complete Workflow

### 1. Generate Figures

```bash
cd "../statistical analyis"
python3 master_analysis.py
python3 create_diagrams.py
```

### 2. Convert to Word

```bash
cd "../MDPI converter"
python3 convert_clean.py ../V8.2.3.md
```

### 3. Done!

```bash
open ../V8.2.3_MDPI.docx
```

**Total time:** ~25 seconds

---

## File Structure

```
MDPI converter/
??? convert_clean.py          ? Use this (clean script)
??? README_CLEAN.md           Documentation
??? requirements.txt          Dependencies
?
??? Legacy scripts (for reference):
?   ??? mdpi_converter_fixed.py
?   ??? mdpi_enhanced_converter.py
?   ??? ... (other old scripts)
?
??? templates/
    ??? academic_template.docx
```

---

## Advantages Over Old Scripts

| Feature | Old Scripts | convert_clean.py |
|---------|-------------|------------------|
| **Lines of code** | 500+ each | ~400 total |
| **Figure mapping** | Hardcoded, outdated | Updated for V2.0 |
| **Dependencies** | Many (markdown, bs4, etc.) | Minimal (docx, yaml) |
| **Maintenance** | Multiple files | Single file |
| **Documentation** | Scattered | Complete inline |
| **Figure detection** | Manual path | Auto-detection |

---

## Supported Markdown Features

? Headings (`#`, `##`, `###`, `####`)  
? Bold text (`**bold**`)  
? Italic text (`*italic*`)  
? Bullet lists (`- item`)  
? Numbered lists (`1. item`)  
? Figure references (`[Figure N]`)  
? YAML front matter  
? Paragraphs with justification  

---

## Requirements

**Python:** 3.7+

**Packages:**
```
python-docx>=0.8.11
PyYAML>=5.0
```

**Install:**
```bash
pip install python-docx PyYAML
```

Or use requirements.txt:
```bash
pip install -r requirements.txt
```

---

## Troubleshooting

### Figures Not Embedded

**Problem:** Warning messages about missing figures

**Solution:**
1. Generate figures first:
   ```bash
   cd "../statistical analyis"
   python3 master_analysis.py
   python3 create_diagrams.py
   ```
2. Then convert

### Module Not Found

**Problem:** `ModuleNotFoundError: No module named 'docx'`

**Solution:**
```bash
pip install python-docx PyYAML
```

### Wrong Figure Numbers

**Problem:** "Unknown figure number: 10"

**Solution:** Update manuscript to use new numbering (1-7, not 8-16)

---

## Comparison with Legacy Scripts

### Old System (Deprecated)

Multiple overlapping scripts:
- `mdpi_converter_fixed.py` - Basic conversion
- `mdpi_enhanced_converter.py` - Enhanced features
- `mdpi_template_converter.py` - Template-based
- `thesis_md2docx.py` - Thesis format
- `academic_md2word.py` - Academic format

**Problems:**
- Redundant code
- Inconsistent figure numbering
- Outdated mappings
- Hard to maintain

### New System (convert_clean.py)

Single unified script:
- All features in one place
- Updated for reorganized figures
- Clear, documented code
- Easy to maintain

---

## Migration from Old Scripts

If you were using old scripts:

**Before:**
```bash
python3 mdpi_converter_fixed.py input.md
# or
python3 mdpi_enhanced_converter.py input.md
```

**After:**
```bash
python3 convert_clean.py input.md
```

**Changes:**
1. Figure numbering updated (1-7 instead of 1-16)
2. Auto-detects figures directory
3. Simplified command line
4. Better error messages

---

## Code Structure

```python
# Main components:

1. extract_yaml_frontmatter()     # Parse YAML header
2. setup_mdpi_styles()            # Apply formatting
3. add_title_page()               # Create title
4. process_markdown_content()     # Convert content
5. insert_figure()                # Embed figures
6. convert_markdown_to_docx()     # Main conversion
7. main()                         # CLI interface
```

**Total:** ~400 lines, well-documented

---

## Example Output

**Input:** `V8.2.3.md` (markdown with YAML)  
**Output:** `V8.2.3_MDPI.docx` (formatted Word document)

**Features:**
- Title from YAML
- MDPI formatting applied
- Figures embedded at references
- Clean, professional layout
- Ready for submission

---

## Future Enhancements

Possible additions (not in V1.0):

- [ ] Table conversion from markdown
- [ ] Citation linking
- [ ] Equation formatting
- [ ] Supplementary materials handling
- [ ] Batch conversion mode

---

## Support

**Documentation:**
- This file: Script-specific info
- `../CONVERT_TO_WORD_GUIDE.md`: Complete workflow
- Inline comments: Implementation details

**For issues:**
1. Check error messages
2. Verify dependencies installed
3. Ensure figures generated
4. Review this README

---

## License

See `LICENSE` file in this directory.

---

## Version History

### Version 1.0 (Current)
- Initial release
- Clean, unified script
- Updated for figure reorganization
- Auto-detection features
- Comprehensive documentation

---

**Last Updated:** January 16, 2026  
**Script:** `convert_clean.py`  
**Status:** ? Production Ready
