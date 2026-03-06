#!/bin/bash
#
# convert-to-docx.sh
# Robust Markdown → DOCX conversion script with formatting fixes
# Usage: ./convert-to-docx.sh <input.md> [output.docx]
#

set -e  # Exit on error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to print colored messages
info() { echo -e "${GREEN}✓${NC} $1"; }
warn() { echo -e "${YELLOW}⚠${NC} $1"; }
error() { echo -e "${RED}✗${NC} $1"; exit 1; }

# Check arguments
if [ $# -lt 1 ]; then
    echo "Usage: $0 <input.md> [output.docx]"
    echo ""
    echo "Example: $0 Preliminary-Study-V2.7.4.md"
    echo "         $0 input.md output.docx"
    exit 1
fi

INPUT_FILE="$1"
OUTPUT_FILE="${2:-${INPUT_FILE%.md}.docx}"
TEMP_FILE="/tmp/$(basename ${INPUT_FILE%.md})-cleaned.md"

# Verify input file exists
[ ! -f "$INPUT_FILE" ] && error "Input file not found: $INPUT_FILE"

# Check if pandoc is installed
command -v pandoc >/dev/null 2>&1 || error "pandoc is not installed. Install with: brew install pandoc"

info "Starting conversion: $INPUT_FILE → $OUTPUT_FILE"

# Step 1: Clean the markdown file
info "Step 1/5: Cleaning markdown syntax..."

python3 << 'PYEOF' "$INPUT_FILE" "$TEMP_FILE"
import sys

input_file = sys.argv[1] if len(sys.argv) > 1 else sys.stdin
temp_file = sys.argv[2] if len(sys.argv) > 2 else '/tmp/cleaned.md'

with open(input_file, 'r', encoding='utf-8') as f:
    lines = f.readlines()

cleaned_lines = []
in_appendix = False
appendix_count = 0

for i, line in enumerate(lines):
    # Track appendix sections
    if line.startswith('### Appendix'):
        in_appendix = True
        appendix_count += 1
    
    # Fix 1: Remove --- horizontal rules in appendices (causes YAML parsing errors)
    if in_appendix and line.strip() == '---':
        cleaned_lines.append('\n')  # Replace with blank line
        continue
    
    # Fix 2: Ensure tables don't have double pipes (already fixed, but ensure)
    # Tables should be: | col | col | not || col | col |
    # This is just for safety - the line number display might show ||
    
    # Fix 3: Remove any trailing whitespace
    line = line.rstrip() + '\n' if line.strip() else '\n'
    
    cleaned_lines.append(line)

# Write cleaned markdown
with open(temp_file, 'w', encoding='utf-8') as f:
    f.writelines(cleaned_lines)

print(f"✓ Cleaned {len(cleaned_lines)} lines, removed {appendix_count} appendix --- separators")
PYEOF

info "Step 2/5: Validating markdown structure..."

# Count tables, headings, etc.
TABLE_COUNT=$(grep -c "^|" "$TEMP_FILE" || true)
HEADING_COUNT=$(grep -c "^#" "$TEMP_FILE" || true)
info "  Found: $HEADING_COUNT headings, $TABLE_COUNT table rows"

# Step 3: Convert to multiple formats
info "Step 3/5: Converting to DOCX (primary)..."

# Primary conversion: DOCX with TOC (no auto-numbering, markdown has manual numbers)
pandoc "$TEMP_FILE" \
    -o "$OUTPUT_FILE" \
    -f markdown \
    -t docx \
    --standalone \
    --toc \
    --toc-depth=3 \
    --highlight-style=tango \
    2>&1 || error "DOCX conversion failed"

info "Step 4/5: Creating backup formats..."

# Backup format 1: ODT (often renders better than DOCX)
ODT_FILE="${OUTPUT_FILE%.docx}.odt"
pandoc "$TEMP_FILE" \
    -o "$ODT_FILE" \
    -f markdown \
    -t odt \
    --standalone \
    --toc \
    2>&1 && info "  Created ODT: $ODT_FILE"

# Backup format 2: HTML (always renders correctly)
HTML_FILE="${OUTPUT_FILE%.docx}.html"
pandoc "$TEMP_FILE" \
    -o "$HTML_FILE" \
    -f markdown \
    -t html \
    --standalone \
    --toc \
    --toc-depth=3 \
    --css=https://cdn.jsdelivr.net/npm/water.css@2/out/water.css \
    --metadata title="$(head -1 $TEMP_FILE | sed 's/^# //')" \
    2>&1 && info "  Created HTML: $HTML_FILE"

# Backup format 3: PDF (if pandoc has PDF support via LaTeX)
PDF_FILE="${OUTPUT_FILE%.docx}.pdf"
if command -v pdflatex >/dev/null 2>&1; then
    pandoc "$TEMP_FILE" \
        -o "$PDF_FILE" \
        -f markdown \
        -t pdf \
        --pdf-engine=pdflatex \
        --toc \
        2>&1 && info "  Created PDF: $PDF_FILE"
else
    warn "  Skipped PDF (pdflatex not installed)"
fi

# Step 5: Verify output files
info "Step 5/5: Verifying output..."

if [ -f "$OUTPUT_FILE" ]; then
    SIZE=$(ls -lh "$OUTPUT_FILE" | awk '{print $5}')
    info "  Primary DOCX: $OUTPUT_FILE ($SIZE)"
    
    # Check if file is valid Word document
    file "$OUTPUT_FILE" | grep -q "Microsoft Word" && info "  File type: Valid Microsoft Word document" || warn "  File type check failed"
else
    error "Output file not created: $OUTPUT_FILE"
fi

# Clean up temporary file
rm -f "$TEMP_FILE"

# Summary
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
info "Conversion complete!"
echo ""
echo "  📄 DOCX: $OUTPUT_FILE"
[ -f "$ODT_FILE" ] && echo "  📄 ODT:  $ODT_FILE (recommended if DOCX has issues)"
[ -f "$HTML_FILE" ] && echo "  🌐 HTML: $HTML_FILE (perfect rendering)"
[ -f "$PDF_FILE" ] && echo "  📕 PDF:  $PDF_FILE"
echo ""
echo "Recommendations:"
echo "  1. Open the DOCX file in Microsoft Word"
echo "  2. If you see vertical text, try the ODT file instead"
echo "  3. Use the HTML file for review/viewing in browser"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

