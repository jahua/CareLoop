#!/bin/bash

# MDPI-Specific Markdown to Word Converter
# Usage: ./convert_to_mdpi_docx.sh filename.md

# Set the directory containing this script
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PARENT_DIR="$(dirname "$SCRIPT_DIR")"
DOCOUTPUT_DIR="$PARENT_DIR/docoutput"

# Check if at least one argument is provided
if [ $# -lt 1 ]; then
    echo "Usage: $0 <input_markdown_file>"
    echo ""
    echo "MDPI Converter - Formats documents according to MDPI guidelines:"
    echo "  - 12pt Times New Roman font"
    echo "  - 1.5 line spacing"
    echo "  - A4 paper with standard margins"
    echo "  - Numbered references"
    echo "  - IMRaD structure preservation"
    exit 1
fi

# Get the input markdown file
INPUT_FILE="$1"
INPUT_FILENAME=$(basename "$INPUT_FILE")
INPUT_NAME="${INPUT_FILENAME%.*}"

# Create the docoutput directory if it doesn't exist
mkdir -p "$DOCOUTPUT_DIR"

echo "=========================================="
echo "MDPI Document Converter"
echo "=========================================="
echo "Input: $INPUT_FILE"
echo "Output: $DOCOUTPUT_DIR/$INPUT_NAME.docx"
echo ""

# Run the MDPI-specific conversion
echo "Converting to MDPI format..."
python3 "$SCRIPT_DIR/mdpi_md2word.py" "$INPUT_FILE" "$DOCOUTPUT_DIR/$INPUT_NAME.docx"

# Check the result
if [ $? -eq 0 ]; then
    echo ""
    echo "✓ Conversion successful!"
    echo ""
    echo "MDPI Formatting Applied:"
    echo "  • Font: 12pt Times New Roman"
    echo "  • Line spacing: 1.5"
    echo "  • Paper: A4"
    echo "  • Margins: Top/Bottom 1.5cm, Left/Right 1.75cm"
    echo "  • References: Numbered [1], [2], etc."
    echo ""
    echo "Output saved to: $DOCOUTPUT_DIR/$INPUT_NAME.docx"
    echo ""
    
    # Verify document structure
    python3 - "$DOCOUTPUT_DIR/$INPUT_NAME.docx" << 'PY'
import sys
from docx import Document
try:
    doc = Document(sys.argv[1])
    print(f"Document Statistics:")
    print(f"  • Total paragraphs: {len(doc.paragraphs)}")
    print(f"  • Total tables: {len(doc.tables)}")
    print(f"  • Total sections: {len(doc.sections)}")
except Exception as e:
    print(f"Could not verify document: {e}")
PY
    
    echo ""
    echo "Ready for MDPI submission!"
    echo "=========================================="
else
    echo ""
    echo "✗ Conversion failed!"
    echo "=========================================="
    exit 1
fi




