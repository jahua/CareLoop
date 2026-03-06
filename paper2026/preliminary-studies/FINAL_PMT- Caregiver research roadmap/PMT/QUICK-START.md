# 🚀 Quick Start: Convert Markdown to DOCX

## One-Line Command

```bash
# Convert your markdown file to DOCX + ODT + HTML
python3 convert_markdown.py YourFile.md --all
```

That's it! You'll get:
- ✅ `YourFile.docx` — Microsoft Word format
- ✅ `YourFile.odt` — OpenDocument (opens in Word, Google Docs, LibreOffice)
- ✅ `YourFile.html` — Web format (perfect rendering)

---

## Why Use These Scripts?

❌ **Without the script:**
```bash
pandoc file.md -o file.docx
# Error: YAML parse exception at line 1331
# Result: Vertical text, broken tables, formatting issues
```

✅ **With the script:**
```bash
python3 convert_markdown.py file.md --all
# ✓ Fixes YAML conflicts automatically
# ✓ Cleans table formatting
# ✓ Generates backup formats
# ✓ Validates output
```

---

## Common Usage

### 1. Just DOCX (default)
```bash
python3 convert_markdown.py Preliminary-Study-V2.7.4.md
```

### 2. All formats (recommended)
```bash
python3 convert_markdown.py Preliminary-Study-V2.7.4.md --all
```

### 3. HTML only (for web viewing)
```bash
python3 convert_markdown.py Preliminary-Study-V2.7.4.md --format html
# Then open in browser: open Preliminary-Study-V2.7.4.html
```

### 4. Custom output name
```bash
python3 convert_markdown.py input.md my-thesis.docx
```

---

## If DOCX Has Formatting Issues

### Option 1: Use the ODT file (recommended)
```bash
# The script already created it
open Preliminary-Study-V2.7.4.odt  # macOS
# or
xdg-open Preliminary-Study-V2.7.4.odt  # Linux
```

Open in Word → Save As DOCX → Done! ✅

### Option 2: Use the HTML file
```bash
open Preliminary-Study-V2.7.4.html
# Perfect rendering, no issues
# Print to PDF if needed
```

---

## Installation (First Time Only)

### 1. Install Pandoc
```bash
# macOS
brew install pandoc

# Linux
sudo apt install pandoc

# Windows
choco install pandoc
```

### 2. Verify Installation
```bash
pandoc --version
# Should show: pandoc 3.x or higher
```

---

## Full Documentation

See [CONVERSION-README.md](./CONVERSION-README.md) for:
- Detailed troubleshooting
- Advanced options
- What the scripts fix
- Best practices

---

## File Locations

After conversion, your files will be in the same directory:

```
📁 Your Project/
├── Preliminary-Study-V2.7.4.md        ← Original
├── Preliminary-Study-V2.7.4.docx      ← Word document
├── Preliminary-Study-V2.7.4.odt       ← OpenDocument (backup)
└── Preliminary-Study-V2.7.4.html      ← Web version (perfect rendering)
```

---

## Need Help?

```bash
# Show help message
python3 convert_markdown.py --help

# Example output shows you all options
```

**Still stuck?** Check [CONVERSION-README.md](./CONVERSION-README.md) for troubleshooting.

---

**Created:** 2025-10-22  
**Last Updated:** 2025-10-22


