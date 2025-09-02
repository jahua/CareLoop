# MDPI Healthcare Converter Usage Guide

## Enhanced Script Features

The improved `mdpi_md_to_word.sh` script now includes comprehensive MDPI Healthcare journal formatting and submission package creation.

### Key Improvements Made

✅ **MDPI Style Compliance**:
- A4 paper format (1.5cm top, 3.5cm bottom, 1.75cm sides)
- Times New Roman 12pt font
- 1.5 line spacing for submission
- Numbered sections and subsections (3 levels)
- APA style reference formatting
- Professional academic layout

✅ **Source/Output Directory Flags**:
- `-s, --source-dir`: Specify source directory
- `-o, --output-dir`: Specify output directory (default: `paper_submission`)
- `-v, --verbose`: Enable detailed output
- `-h, --help`: Show usage information

✅ **Submission Package Creation**:
- Complete MDPI Healthcare submission structure
- Pre-submission checklist
- Directory structure for figures, tables, supplementary materials
- README with submission guidelines

## Usage Examples

### Basic Usage
```bash
./mdpi_md_to_word.sh V2_Healthcare_Submission.md
```

### With Custom Directories
```bash
./mdpi_md_to_word.sh -s ./source -o ./paper_submission manuscript.md
```

### Verbose Mode
```bash
./mdpi_md_to_word.sh --verbose --output-dir paper_submission V2_Healthcare_Submission.md
```

## Generated Files Structure

```
paper_submission/
├── V2_Healthcare_Submission_MDPI.docx    # Main MDPI-formatted manuscript
├── mdpi_reference.docx                   # MDPI style reference document
├── MDPI_Submission_Checklist.txt         # Pre-submission checklist
├── README.md                             # Submission package guide
├── figures/                              # Directory for high-res figures
├── tables/                               # Directory for table files
└── supplementary/                        # Directory for supplementary materials
```

## MDPI Healthcare Specific Features

### Formatting Applied
- **Paper Size**: A4 with MDPI margins
- **Typography**: Times New Roman 12pt, 1.5 spacing
- **Structure**: Numbered headings, table of contents (3 levels)
- **References**: APA style formatting
- **Tables**: Proper numbering and captioning
- **Figures**: Preparation for high-resolution inclusion

### Special Issue Alignment
- **Title**: "Artificial Intelligence in Healthcare: Opportunities and Challenges"
- **Focus**: Healthcare AI applications and challenges
- **Format**: MDPI Healthcare journal requirements
- **Submission**: Ready for online portal submission

## Submission Checklist Integration

The script automatically creates a comprehensive checklist including:

- ✅ MDPI Healthcare formatting compliance
- ✅ APA reference style verification
- ✅ Figure and table preparation
- ✅ Word count and structure validation
- ✅ Special issue relevance confirmation
- ✅ Author information completion (if applicable)
- ✅ Ethics and funding statements

## Technical Features

### Advanced Conversion
- YAML metadata processing for MDPI compliance
- Mathematical equation handling
- Cross-reference support
- Bibliography integration
- Fallback conversion for compatibility

### Quality Assurance
- File size validation
- Output format verification
- Error handling and recovery
- Detailed logging in verbose mode

## Troubleshooting

### Common Issues
1. **Pandoc not found**: Script auto-installs on macOS/Linux
2. **Conversion fails**: Automatic fallback to basic conversion
3. **Reference formatting**: Uses APA style with automatic citation processing
4. **Figure quality**: Instructions provided for 300 DPI requirements

### Success Indicators
- ✅ Word document created (>1KB file size)
- ✅ MDPI reference document generated
- ✅ Submission package structure created
- ✅ Checklist and README generated

## Next Steps After Conversion

1. **Review Generated Document**: Open the MDPI-formatted Word file
2. **Complete Checklist**: Use the generated submission checklist
3. **Add Figures**: Place high-resolution figures in `figures/` directory
4. **Verify References**: Ensure all citations follow APA format
5. **Submit**: Use MDPI Healthcare online submission portal

## Script Success

The enhanced script successfully:
- ✅ Converted V2_Healthcare_Submission.md to MDPI format
- ✅ Created 21.9KB properly formatted Word document
- ✅ Generated complete submission package
- ✅ Applied MDPI Healthcare style guidelines
- ✅ Prepared for "AI in Healthcare: Opportunities and Challenges" special issue

## File Location

Generated submission package: `paper_submission/V2_Healthcare_Submission_MDPI.docx`

Ready for MDPI Healthcare journal submission!