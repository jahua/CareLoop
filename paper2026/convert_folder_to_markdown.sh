#!/bin/bash

# 📁 Folder Document to Markdown Converter
# =========================================
# Converts all documents in a specified folder to markdown format

# Usage: ./convert_folder_to_markdown.sh [input_folder] [output_folder]
# Example: ./convert_folder_to_markdown.sh "Samuel_paper/3-System-Prompts" "markdown_output"

# Default values
INPUT_FOLDER="${1:-.}"  # Current directory if not specified
OUTPUT_FOLDER="${2:-markdown_output}"  # Default output folder

echo "📁 FOLDER DOCUMENT CONVERTER"
echo "============================="
echo "📂 Input folder: $INPUT_FOLDER"
echo "📁 Output folder: $OUTPUT_FOLDER"
echo ""

# Create output directory
mkdir -p "$OUTPUT_FOLDER"

# Check if input folder exists
if [ ! -d "$INPUT_FOLDER" ]; then
    echo "❌ Error: Input folder '$INPUT_FOLDER' does not exist"
    exit 1
fi

# Check for required tools
echo "🔧 Checking conversion tools..."
PANDOC_AVAILABLE=false
PDFTOTEXT_AVAILABLE=false

if command -v pandoc >/dev/null 2>&1; then
    echo "✅ pandoc: Available"
    PANDOC_AVAILABLE=true
else
    echo "❌ pandoc: Not available (install with: brew install pandoc)"
fi

if command -v pdftotext >/dev/null 2>&1; then
    echo "✅ pdftotext: Available"
    PDFTOTEXT_AVAILABLE=true
else
    echo "❌ pdftotext: Not available (install with: brew install poppler)"
fi

echo ""

# Counters
converted_count=0
failed_count=0

# Function to convert DOCX to markdown
convert_docx_to_md() {
    local input_file="$1"
    local base_name=$(basename "$input_file" .docx)
    local output_file="$OUTPUT_FOLDER/${base_name}.md"
    
    echo "📝 Converting: $input_file"
    
    if [ "$PANDOC_AVAILABLE" = true ]; then
        if pandoc "$input_file" -o "$output_file" 2>/dev/null; then
            echo "✅ Success: $output_file"
            ((converted_count++))
        else
            echo "❌ Failed: $input_file"
            ((failed_count++))
        fi
    else
        echo "❌ Cannot convert DOCX: pandoc not available"
        ((failed_count++))
    fi
}

# Function to convert PDF to markdown (with fallback to text)
convert_pdf_to_md() {
    local input_file="$1"
    local base_name=$(basename "$input_file" .pdf)
    local output_file="$OUTPUT_FOLDER/${base_name}.md"
    
    echo "📄 Converting: $input_file"
    
    # Try pandoc first (better formatting)
    if [ "$PANDOC_AVAILABLE" = true ]; then
        if pandoc "$input_file" -o "$output_file" 2>/dev/null; then
            echo "✅ Success (pandoc): $output_file"
            ((converted_count++))
            return 0
        fi
    fi
    
    # Fallback to pdftotext + manual markdown formatting
    if [ "$PDFTOTEXT_AVAILABLE" = true ]; then
        local temp_txt="${output_file%.md}.txt"
        if pdftotext "$input_file" "$temp_txt" 2>/dev/null; then
            # Convert plain text to basic markdown
            {
                echo "# $(basename "$input_file" .pdf)"
                echo ""
                echo "**Source:** $input_file"
                echo "**Converted:** $(date)"
                echo ""
                echo "---"
                echo ""
                cat "$temp_txt"
            } > "$output_file"
            rm -f "$temp_txt"
            echo "✅ Success (pdftotext): $output_file"
            ((converted_count++))
        else
            echo "❌ Failed: $input_file"
            ((failed_count++))
        fi
    else
        echo "❌ Cannot convert PDF: no conversion tools available"
        ((failed_count++))
    fi
}

# Function to convert DOC to markdown (if possible)
convert_doc_to_md() {
    local input_file="$1"
    local base_name=$(basename "$input_file" .doc)
    local output_file="$OUTPUT_FOLDER/${base_name}.md"
    
    echo "📄 Converting: $input_file"
    
    if [ "$PANDOC_AVAILABLE" = true ]; then
        if pandoc "$input_file" -o "$output_file" 2>/dev/null; then
            echo "✅ Success: $output_file"
            ((converted_count++))
        else
            echo "❌ Failed: $input_file"
            ((failed_count++))
        fi
    else
        echo "❌ Cannot convert DOC: pandoc not available"
        ((failed_count++))
    fi
}

# Process files
echo "🔍 Processing files in '$INPUT_FOLDER'..."
echo ""

# Find and convert DOCX files
while IFS= read -r -d '' file; do
    convert_docx_to_md "$file"
done < <(find "$INPUT_FOLDER" -maxdepth 1 -name "*.docx" -not -name "~$*" -print0 2>/dev/null)

# Find and convert PDF files
while IFS= read -r -d '' file; do
    convert_pdf_to_md "$file"
done < <(find "$INPUT_FOLDER" -maxdepth 1 -name "*.pdf" -print0 2>/dev/null)

# Find and convert DOC files
while IFS= read -r -d '' file; do
    convert_doc_to_md "$file"
done < <(find "$INPUT_FOLDER" -maxdepth 1 -name "*.doc" -not -name "~$*" -print0 2>/dev/null)

echo ""
echo "🎉 CONVERSION COMPLETE!"
echo "======================"
echo "✅ Converted: $converted_count files"
echo "❌ Failed: $failed_count files"
echo "📁 Output location: $OUTPUT_FOLDER"
echo ""

if [ $converted_count -gt 0 ]; then
    echo "📋 Converted files:"
    ls -la "$OUTPUT_FOLDER"/*.md 2>/dev/null | head -10
    echo ""
    echo "💡 USAGE TIPS:"
    echo "   • Open .md files directly in Cursor"
    echo "   • Files are now searchable and AI-accessible"
    echo "   • Reference with @$OUTPUT_FOLDER/filename.md"
fi

if [ $failed_count -gt 0 ]; then
    echo ""
    echo "⚠️ Some conversions failed. Make sure you have:"
    echo "   brew install pandoc      # For DOCX and PDF conversion"
    echo "   brew install poppler     # For PDF text extraction"
fi


















































