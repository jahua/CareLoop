#!/bin/bash

# Script to convert Samuel-Devdas_Master-Thesis.pdf to markdown

echo "PDF to Markdown Converter"
echo "========================="

# Check if Python is available
if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 is not installed or not in PATH"
    exit 1
fi

# Install required dependencies if not present
echo "Checking dependencies..."
python3 -c "import PyPDF2" 2>/dev/null || python3 -c "import pypdf" 2>/dev/null || {
    echo "Installing PyPDF2..."
    pip3 install PyPDF2
}

# Convert the PDF
PDF_FILE="/Users/huaduojiejia/MyProject/hslu/2026/Samuel-Devdas_Master-Thesis.pdf"
OUTPUT_FILE="/Users/huaduojiejia/MyProject/hslu/2026/Samuel-Devdas_Master-Thesis.md"

echo "Converting PDF to Markdown..."
python3 pdf_to_markdown.py "$PDF_FILE" "$OUTPUT_FILE"

echo "Conversion complete!"
echo "Output file: $OUTPUT_FILE"
echo ""
echo "Preview of the converted file:"
echo "=============================="
head -n 20 "$OUTPUT_FILE"
