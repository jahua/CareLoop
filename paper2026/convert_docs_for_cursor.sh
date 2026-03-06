#!/bin/bash

# 📚 Document Conversion Script for Cursor
# ========================================
# This script converts various document formats to markdown/text for better Cursor compatibility

echo "🔄 Converting documents for Cursor compatibility..."
echo "=================================================="

# Create docs output directory
mkdir -p ./docs_converted

# Function to convert PDF to text
convert_pdf() {
    local pdf_file="$1"
    local base_name=$(basename "$pdf_file" .pdf)
    
    echo "📄 Converting: $pdf_file"
    
    # Try pandoc first (better formatting)
    if command -v pandoc >/dev/null 2>&1; then
        pandoc "$pdf_file" -o "./docs_converted/${base_name}.md" 2>/dev/null
        if [ $? -eq 0 ]; then
            echo "✅ Converted to markdown: ./docs_converted/${base_name}.md"
            return 0
        fi
    fi
    
    # Fallback to pdftotext
    if command -v pdftotext >/dev/null 2>&1; then
        pdftotext "$pdf_file" "./docs_converted/${base_name}.txt"
        if [ $? -eq 0 ]; then
            echo "✅ Converted to text: ./docs_converted/${base_name}.txt"
            return 0
        fi
    fi
    
    echo "❌ Failed to convert: $pdf_file"
    echo "   Install: brew install pandoc poppler"
}

# Function to convert DOCX to markdown
convert_docx() {
    local docx_file="$1"
    local base_name=$(basename "$docx_file" .docx)
    
    echo "📄 Converting: $docx_file"
    
    if command -v pandoc >/dev/null 2>&1; then
        pandoc "$docx_file" -o "./docs_converted/${base_name}.md"
        if [ $? -eq 0 ]; then
            echo "✅ Converted to markdown: ./docs_converted/${base_name}.md"
        else
            echo "❌ Failed to convert: $docx_file"
        fi
    else
        echo "❌ pandoc not found. Install with: brew install pandoc"
    fi
}

# Find and convert PDF files
echo ""
echo "🔍 Looking for PDF files..."
find . -name "*.pdf" -not -path "./docs_converted/*" | while read pdf_file; do
    convert_pdf "$pdf_file"
done

# Find and convert DOCX files  
echo ""
echo "🔍 Looking for DOCX files..."
find . -name "*.docx" -not -path "./docs_converted/*" | while read docx_file; do
    convert_docx "$docx_file"
done

echo ""
echo "🎉 Conversion complete!"
echo "📁 Converted files are in: ./docs_converted/"
echo ""
echo "💡 CURSOR TIPS:"
echo "   • Open converted .md files directly in Cursor"
echo "   • These files will be automatically indexed for AI context"
echo "   • Add ./docs_converted/ to your project workspace"
echo ""
echo "🔧 To make these conversions permanent:"
echo "   1. Review the converted files"
echo "   2. Move important ones to your main docs/ folder"
echo "   3. Add originals to .cursorignore if desired"


















































