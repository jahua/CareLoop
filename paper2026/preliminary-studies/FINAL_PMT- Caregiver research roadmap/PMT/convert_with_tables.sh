#!/bin/bash
# Enhanced conversion script that properly handles Markdown tables

INPUT_FILE="$1"
OUTPUT_DIR="${2:-.}"

if [ -z "$INPUT_FILE" ]; then
    echo "Usage: $0 <markdown_file> [output_dir]"
    exit 1
fi

# Get filename without extension
BASENAME=$(basename "$INPUT_FILE" .md)
OUTPUT_FILE="$OUTPUT_DIR/${BASENAME}_thesis.docx"

echo "Converting Markdown to DOCX with proper table handling..."
echo "Input:  $INPUT_FILE"
echo "Output: $OUTPUT_FILE"
echo ""

# Use python converter instead of direct pandoc
python3 /Users/huaduojiejia/MyProject/hslu/2026/md2doc/thesis_md2docx.py "$INPUT_FILE" "$OUTPUT_DIR"

echo ""
echo "✓ Conversion complete!"
ls -lh "$OUTPUT_FILE" 2>/dev/null && echo "✓ File created successfully"

