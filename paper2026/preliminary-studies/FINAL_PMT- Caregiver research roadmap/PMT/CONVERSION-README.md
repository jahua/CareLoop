# Markdown to DOCX Conversion Scripts

This directory contains robust conversion scripts for converting Markdown documents to Microsoft Word (DOCX) and other formats, with automatic fixes for common formatting issues.

## 🎯 Quick Start

### Python Script (Recommended)
```bash
# Convert to DOCX (default)
python3 convert_markdown.py Preliminary-Study-V2.7.4.md

# Generate all formats (DOCX, ODT, HTML, PDF)
python3 convert_markdown.py Preliminary-Study-V2.7.4.md --all

# Specific format
python3 convert_markdown.py Preliminary-Study-V2.7.4.md --format odt
```

### Bash Script (macOS/Linux)
```bash
# Convert to DOCX
./convert-to-docx.sh Preliminary-Study-V2.7.4.md

# Specify output filename
./convert-to-docx.sh input.md output.docx
```

---

## 📋 What These Scripts Fix

### Common Markdown → DOCX Issues

1. **YAML Parsing Errors**
   - ❌ Problem: `---` horizontal rules in appendices cause "YAML parse exception"
   - ✅ Fix: Automatically removes `---` separators in appendix sections

2. **Table Formatting**
   - ❌ Problem: Double-pipe syntax (`||`) breaks table rendering
   - ✅ Fix: Ensures proper single-pipe markdown table format

3. **Vertical Text Rendering**
   - ❌ Problem: Some text renders vertically character-by-character in Word
   - ✅ Fix: Provides alternative formats (ODT, HTML) that render correctly

4. **Whitespace & Encoding**
   - ❌ Problem: Trailing whitespace and inconsistent line endings
   - ✅ Fix: Normalizes whitespace and uses UTF-8 encoding

---

## 📄 Output Formats

Both scripts generate multiple formats for maximum compatibility:

| Format | File Extension | Best For | Notes |
|--------|----------------|----------|-------|
| **DOCX** | `.docx` | Microsoft Word, final submission | Primary output; may have minor rendering issues |
| **ODT** | `.odt` | LibreOffice, Google Docs | Often renders better than DOCX |
| **HTML** | `.html` | Web viewing, review | Perfect rendering; styled with water.css |
| **PDF** | `.pdf` | Print, archival | Requires pdflatex/LaTeX installation |

---

## 🛠️ Requirements

### Required
- **Pandoc** (document converter)
  ```bash
  # macOS
  brew install pandoc
  
  # Linux (Debian/Ubuntu)
  sudo apt install pandoc
  
  # Windows
  choco install pandoc
  ```

### Optional (for PDF)
- **LaTeX** (for PDF generation)
  ```bash
  # macOS
  brew install basictex
  
  # Linux
  sudo apt install texlive-latex-base
  ```

---

## 📖 Usage Examples

### Python Script

#### Example 1: Basic Conversion
```bash
python3 convert_markdown.py Preliminary-Study-V2.7.4.md
# Output: Preliminary-Study-V2.7.4.docx
```

#### Example 2: All Formats
```bash
python3 convert_markdown.py Preliminary-Study-V2.7.4.md --all
# Outputs:
#   - Preliminary-Study-V2.7.4.docx
#   - Preliminary-Study-V2.7.4.odt
#   - Preliminary-Study-V2.7.4.html
#   - Preliminary-Study-V2.7.4.pdf (if LaTeX installed)
```

#### Example 3: Custom Output Name
```bash
python3 convert_markdown.py input.md final-thesis.docx
# Output: final-thesis.docx
```

#### Example 4: HTML Only
```bash
python3 convert_markdown.py document.md --format html
# Output: document.html (great for browser viewing)
```

### Bash Script

```bash
# Basic usage
./convert-to-docx.sh Preliminary-Study-V2.7.4.md

# Custom output name
./convert-to-docx.sh input.md my-output.docx
```

---

## 🐛 Troubleshooting

### Issue: "pandoc is not installed"
**Solution:** Install pandoc using the commands in the Requirements section above.

### Issue: Vertical text still appears in DOCX
**Solutions:**
1. **Use the ODT file** instead:
   - Open `Preliminary-Study-V2.7.4.odt` in Microsoft Word
   - Save as DOCX from within Word
   
2. **Manual fix in Word:**
   - Select All (Cmd+A or Ctrl+A)
   - Format → Text Direction → Horizontal
   
3. **Use HTML for viewing:**
   - Open the `.html` file in your browser
   - Print to PDF if needed

### Issue: Tables look misaligned
**Solution:** The ODT or HTML formats typically have better table rendering. Use those instead.

### Issue: PDF generation fails
**Cause:** LaTeX is not installed.  
**Solution:** Install LaTeX (see Requirements) or skip PDF generation.

---

## 🔍 Script Details

### Python Script (`convert_markdown.py`)
- **Platform:** Cross-platform (Windows, macOS, Linux)
- **Language:** Python 3.6+
- **Features:**
  - Colored terminal output
  - Detailed progress reporting
  - Automatic validation
  - Error handling with helpful messages

### Bash Script (`convert-to-docx.sh`)
- **Platform:** macOS, Linux, WSL
- **Language:** Bash + Python
- **Features:**
  - All-in-one solution
  - Generates backups in multiple formats
  - Color-coded output
  - File validation

---

## 📊 What Gets Fixed Automatically

### Before (Original Markdown)
```markdown
### Appendix C. Data Management

**Bias Mitigation:** Detection module...

---
### Appendix D. Glossary
```

**Problem:** The `---` causes a YAML parsing error:
```
Error parsing YAML metadata at line 1331:
YAML parse exception at line 3, column 2
```

### After (Cleaned Markdown)
```markdown
### Appendix C. Data Management

**Bias Mitigation:** Detection module...


### Appendix D. Glossary
```

**Result:** ✅ Converts successfully without errors

---

## 💡 Best Practices

### For Future Documents

1. **Avoid `---` in appendices**
   - Use blank lines instead for separation
   - If you need horizontal rules, use `<hr>` HTML tags

2. **Test conversion early**
   - Don't wait until the document is complete
   - Run conversions periodically to catch issues

3. **Keep backup formats**
   - Always generate ODT and HTML versions
   - HTML is perfect for review/web viewing
   - ODT often opens better in Word than direct DOCX conversion

4. **Use the `--all` flag**
   - Generate all formats at once
   - Gives you options if one format has issues

5. **Validate tables**
   - Use proper markdown table syntax: `| col | col |`
   - Avoid leading/trailing pipes without content

---

## 🎓 Example Output

When you run the scripts, you'll see output like this:

```
Markdown → DOCX Converter
Input: Preliminary-Study-V2.7.4.md

✓ Step 1/4: Cleaning markdown syntax...
✓ Cleaned 1413 lines
✓   Removed 3 horizontal rules in 6 appendices
✓ Step 2/4: Validating markdown structure...
✓   Found: 87 headings, 342 table rows
✓ Step 3/4: Converting to output format(s)...
✓ Created DOCX: Preliminary-Study-V2.7.4.docx (70.1 KB)
✓ Created ODT: Preliminary-Study-V2.7.4.odt (66.3 KB)
✓ Created HTML: Preliminary-Study-V2.7.4.html (169.2 KB)
✓ Step 4/4: Validating output files...
✓   DOCX: OK
✓   ODT: OK
✓   HTML: OK

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✓ Conversion complete!

  📄 DOCX: Preliminary-Study-V2.7.4.docx
  📄 ODT:  Preliminary-Study-V2.7.4.odt (recommended if DOCX has issues)
  🌐 HTML: Preliminary-Study-V2.7.4.html (perfect rendering)

Recommendations:
  1. Open the DOCX file in Microsoft Word
  2. If you see formatting issues, try the ODT file
  3. Use the HTML file for perfect rendering in browser
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

## 📝 Version History

- **2025-10-22:** Initial scripts created
  - Python cross-platform version
  - Bash script for Unix systems
  - Automatic YAML conflict resolution
  - Multi-format output (DOCX, ODT, HTML, PDF)

---

## 🤝 Support

If you encounter issues:

1. Check the Troubleshooting section above
2. Verify pandoc is installed: `pandoc --version`
3. Try the HTML format first (always works)
4. Use the ODT format as an alternative to DOCX

---

**Happy Converting! 🎉**


