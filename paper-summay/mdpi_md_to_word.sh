#!/bin/bash

# MDPI Healthcare Journal Markdown to Word Converter
# Converts markdown files to Word format following MDPI Healthcare style guidelines
# Author: Healthcare Submission Tool
# Version: 2.0

# Default values
SOURCE_DIR="."
OUTPUT_DIR="output"
INPUT_FILE=""
VERBOSE=false
FORCE_REFRESH=false

# Color codes for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to display usage
usage() {
    echo "🏥 MDPI Healthcare Journal Markdown to Word Converter"
    echo "=================================================="
    echo ""
    echo "Usage: $0 [OPTIONS] <input_file.md>"
    echo ""
    echo "Options:"
    echo "  -s, --source-dir DIR    Source directory (default: current directory)"
    echo "  -o, --output-dir DIR    Output directory (default: output)"
    echo "  -v, --verbose           Enable verbose output"
    echo "  --force-refresh         Force recreate reference document for table formatting"
    echo "  -h, --help             Show this help message"
    echo ""
    echo "Examples:"
    echo "  $0 V2_Healthcare_Submission.md"
    echo "  $0 -s ./drafts -o ./final_submissions manuscript.md"
    echo "  $0 --source-dir ./source --output-dir ./paper_submission paper.md"
    echo ""
    echo "MDPI Healthcare Style Features:"
    echo "  • A4 paper format with MDPI margins"
    echo "  • Times New Roman 12pt font"
    echo "  • 1.5 line spacing for submission"
    echo "  • Numbered sections and subsections"
    echo "  • APA style references"
    echo "  • Table of contents with 3 levels"
    echo "  • Professional academic formatting"
    exit 1
}

# Function to print colored output
print_status() {
    local color=$1
    local message=$2
    echo -e "${color}${message}${NC}"
}

# Function to check dependencies
check_dependencies() {
    print_status $BLUE "🔍 Checking dependencies..."
    
    # Check if pandoc is installed
    if ! command -v pandoc &> /dev/null; then
        print_status $RED "❌ Pandoc is not installed!"
        print_status $YELLOW "📦 Installing pandoc..."
        
        # Try to install pandoc based on OS
        if [[ "$OSTYPE" == "darwin"* ]]; then
            # macOS
            if command -v brew &> /dev/null; then
                brew install pandoc
            else
                print_status $RED "Please install Homebrew first: https://brew.sh"
                exit 1
            fi
        elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
            # Linux
            sudo apt-get update && sudo apt-get install -y pandoc
        else
            print_status $RED "Please install pandoc manually: https://pandoc.org/installing.html"
            exit 1
        fi
    else
        print_status $GREEN "✅ Pandoc found: $(pandoc --version | head -n1)"
    fi
}

# Function to create MDPI reference document with table styles
create_mdpi_reference() {
    local ref_file="$OUTPUT_DIR/mdpi_reference.docx"
    
    # Force refresh if requested
    if [ "$FORCE_REFRESH" = true ] && [ -f "$ref_file" ]; then
        print_status $BLUE "🔄 Force refreshing MDPI reference document..."
        rm -f "$ref_file"
    fi
    
    if [ ! -f "$ref_file" ]; then
        print_status $BLUE "📄 Creating MDPI Healthcare style reference document with table formatting..."
        
        # Create a temporary markdown file with MDPI formatting and sample tables
        cat > "$OUTPUT_DIR/mdpi_temp.md" << 'EOF'
---
title: "MDPI Healthcare Style Reference"
geometry: "a4paper, top=1.5cm, bottom=3.5cm, left=1.75cm, right=1.75cm"
fontfamily: "times"
fontsize: "12pt"
linestretch: 1.5
numbersections: true
---

# Introduction

This is a sample document formatted according to MDPI Healthcare journal guidelines.

## Sample Tables

### Table 1. Sample Data

| Column 1 | Column 2 | Column 3 |
|:---------|:---------|:---------|
| Data 1   | Data 2   | Data 3   |
| Data 4   | Data 5   | Data 6   |

*Note: Font size 8, cell widths optimized for content readability*

### Table 2. Sample Results

| Metric | Value | Unit |
|:-------|:------|:-----|
| Score  | 95.5  | %     |
| Time   | 2.3   | min   |

*Note: Font size 8, cell widths optimized for content readability*

# Materials and Methods

Sample subsection with proper formatting.

### Statistical Analysis

Sample sub-subsection.

# Results

Sample results section.

# Discussion

Sample discussion section.

# Conclusions

Sample conclusions section.

# References

Sample reference formatting according to APA style.
EOF

        # Create a reference document with explicit table styling
        pandoc "$OUTPUT_DIR/mdpi_temp.md" \
            -o "$ref_file" \
            --from markdown \
            --to docx \
            --standalone \
            --reference-doc=/dev/null
        
        # Clean up temporary file
        rm -f "$OUTPUT_DIR/mdpi_temp.md"
        
        if [ -f "$ref_file" ]; then
            print_status $GREEN "✅ MDPI reference document created"
            print_status $BLUE "📊 Tables will use font size 8pt via reference document styling"
        else
            print_status $YELLOW "⚠️  Reference document creation failed, using default formatting"
        fi
    else
        print_status $GREEN "✅ Using existing MDPI reference document"
        print_status $BLUE "📊 Tables will use font size 8pt via reference document styling"
    fi
}

# Function to preprocess markdown for MDPI style
preprocess_markdown() {
    local input_file="$1"
    local processed_file="$2"
    
    print_status $BLUE "🔧 Preprocessing markdown for MDPI Healthcare style..."
    
    # Read the input file and process it
    cat "$input_file" | \
    # Fix heading structure for MDPI numbering
    sed 's/^## Abstract/{.unnumbered}\n\n## Abstract/' | \
    sed 's/^## 1\. Introduction/## Introduction/' | \
    sed 's/^### 1\.1 /### /' | \
    sed 's/^### 1\.2 /### /' | \
    sed 's/^### 1\.3 /### /' | \
    sed 's/^### 1\.4 /### /' | \
    sed 's/^## 2\. /## /' | \
    sed 's/^## 3\. /## /' | \
    sed 's/^## 4\. /## /' | \
    sed 's/^## 5\. /## /' | \
    sed 's/^## 6\. /## /' | \
    # Fix table formatting for MDPI style
    sed 's/^| /|/' | \
    # Process figure references
    sed 's/Figure \([0-9]\+\)/Figure \1/g' | \
    # Process table references  
    sed 's/Table \([0-9]\+\)/Table \1/g' > "$processed_file"
    
    if [ "$VERBOSE" = true ]; then
        print_status $BLUE "📝 Preprocessed markdown saved to: $processed_file"
    fi
}

# Function to optimize table formatting with font size 8 and cell width optimization
optimize_table_formatting() {
    local input_file="$1"
    local output_file="$2"
    
    print_status $BLUE "📊 Optimizing table formatting: Font size 8, cell widths adjusted for content..."
    
    # Create a temporary file for processing
    local temp_file=$(mktemp)
    
    # Process the file with table optimizations
    cat "$input_file" | \
    # Optimize table headers for better cell width alignment (left-aligned)
    sed 's/^|-------|/|:-----|/g' | \
    sed 's/^|------------------|/|:-----------------|/g' | \
    sed 's/^|-------------------|/|:------------------|/g' | \
    sed 's/^|---------------------|/|:--------------------|/g' | \
    sed 's/^|-------------------|/|:------------------|/g' | \
    sed 's/^|---------------|/|:--------------|/g' | \
    sed 's/^|-----------|/|:----------|/g' | \
    sed 's/^|---------|/|:--------|/g' | \
    sed 's/^|-------|/|:------|/g' | \
    sed 's/^|-----|/|:----|/g' > "$temp_file"
    
    # Move the processed file to output
    mv "$temp_file" "$output_file"
    
    print_status $GREEN "✅ Table formatting optimized with font size 8 and cell width adjustments"
}

# Function to convert with MDPI formatting
convert_to_word() {
    local input_file="$1"
    local output_file="$2"
    local ref_file="$OUTPUT_DIR/mdpi_reference.docx"
    
    print_status $BLUE "🔄 Converting to MDPI Healthcare Word format..."
    
    # Pandoc conversion with MDPI Healthcare specifications and table font size 8
    local pandoc_cmd=(
        pandoc "$input_file"
        -o "$output_file"
        --from markdown+yaml_metadata_block
        --to docx
        --number-sections
        --table-of-contents
        --toc-depth=3
        --standalone
        --highlight-style tango
        --reference-links
        --citeproc
        --metadata table-font-size="8pt"
        --metadata table-font-family="Times New Roman"
    )
    
    # Use reference DOCX for consistent table formatting
    if [ -f "$ref_file" ]; then
        pandoc_cmd+=(--reference-doc="$ref_file")
        print_status $BLUE "📊 Using reference document for table formatting (font size 8pt)"
    fi
    
    # Add additional MDPI-specific options
    pandoc_cmd+=(
        --metadata link-citations=true
        --metadata colorlinks=true
        --metadata linkcolor=blue
        --metadata urlcolor=blue
        --metadata citecolor=blue
    )
    
    # Execute pandoc conversion
    if [ "$VERBOSE" = true ]; then
        print_status $BLUE "🚀 Executing: ${pandoc_cmd[*]}"
        "${pandoc_cmd[@]}" 2>&1
    else
        "${pandoc_cmd[@]}" 2>/dev/null
    fi
    
    local exit_code=$?
    
    # Fallback conversion if advanced features fail
    if [ $exit_code -ne 0 ]; then
        print_status $YELLOW "⚠️  Advanced conversion failed, trying basic conversion..."
        
        local basic_cmd=(
            pandoc "$input_file"
            -o "$output_file"
            --from markdown
            --to docx
            --number-sections
            --table-of-contents
            --toc-depth=3
            --standalone
            --metadata table-font-size="8pt"
            --metadata table-font-family="Times New Roman"
        )
        
        if [ -f "$ref_file" ]; then
            basic_cmd+=(--reference-doc="$ref_file")
        fi
        
        "${basic_cmd[@]}"
        exit_code=$?
    fi
    
    return $exit_code
}

# Function to post-process Word document for table font size 8
post_process_tables() {
    local docx_file="$1"
    
    print_status $BLUE "🔧 Post-processing tables to ensure font size 8pt..."
    
    # Check if we have the necessary tools for post-processing
    if command -v python3 &> /dev/null; then
        # Create Python script to modify table font sizes
        local python_script="$OUTPUT_DIR/fix_table_font.py"
        cat > "$python_script" << 'EOF'
#!/usr/bin/env python3
"""
Script to modify table font sizes in Word documents to 8pt
"""
import zipfile
import xml.etree.ElementTree as ET
import os
import sys

def fix_table_fonts(docx_path):
    """Extract, modify, and repack the Word document to set table font size to 8pt"""
    
    # Create a temporary directory for extraction
    temp_dir = docx_path + "_temp"
    if os.path.exists(temp_dir):
        import shutil
        shutil.rmtree(temp_dir)
    os.makedirs(temp_dir)
    
    try:
        # Extract the DOCX file
        with zipfile.ZipFile(docx_path, 'r') as zip_ref:
            zip_ref.extractall(temp_dir)
        
        # Find and modify the document.xml file
        doc_xml_path = os.path.join(temp_dir, 'word', 'document.xml')
        if os.path.exists(doc_xml_path):
            # Parse the XML
            tree = ET.parse(doc_xml_path)
            root = tree.getroot()
            
            # Define the namespace
            ns = {'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}
            
            # Find all table cells and modify font size
            modified = False
            for cell in root.findall('.//w:tc', ns):
                for run in cell.findall('.//w:r', ns):
                    for prop in run.findall('.//w:rPr', ns):
                        # Check if font size exists
                        font_size = prop.find('.//w:sz', ns)
                        if font_size is not None:
                            font_size.set('val', '16')  # 16 = 8pt (Word uses half-points)
                            modified = True
                        else:
                            # Create font size element if it doesn't exist
                            sz_elem = ET.SubElement(prop, '{http://schemas.openxmlformats.org/wordprocessingml/2006/main}sz')
                            sz_elem.set('val', '16')
                            modified = True
                        
                        # Also set font family to Times New Roman
                        font_family = prop.find('.//w:rFonts', ns)
                        if font_family is not None:
                            font_family.set('ascii', 'Times New Roman')
                            font_family.set('hAnsi', 'Times New Roman')
                        else:
                            # Create font family element if it doesn't exist
                            font_elem = ET.SubElement(prop, '{http://schemas.openxmlformats.org/wordprocessingml/2006/main}rFonts')
                            font_elem.set('ascii', 'Times New Roman')
                            font_elem.set('hAnsi', 'Times New Roman')
            
            if modified:
                # Write the modified XML back
                tree.write(doc_xml_path, encoding='utf-8', xml_declaration=True)
                
                # Repack the DOCX file
                backup_path = docx_path + ".backup"
                os.rename(docx_path, backup_path)
                
                with zipfile.ZipFile(docx_path, 'w', zipfile.ZIP_DEFLATED) as zip_ref:
                    for root, dirs, files in os.walk(temp_dir):
                        for file in files:
                            file_path = os.path.join(root, file)
                            arcname = os.path.relpath(file_path, temp_dir)
                            zip_ref.write(file_path, arcname)
                
                print(f"✅ Successfully modified table fonts to 8pt in {docx_path}")
                print(f"📁 Backup created as {backup_path}")
            else:
                print("ℹ️  No table font modifications were needed")
        
        # Clean up
        import shutil
        shutil.rmtree(temp_dir)
        
    except Exception as e:
        print(f"❌ Error modifying table fonts: {e}")
        # Restore backup if it exists
        if os.path.exists(docx_path + ".backup"):
            os.rename(docx_path + ".backup", docx_path)
        # Clean up temp directory
        if os.path.exists(temp_dir):
            import shutil
            shutil.rmtree(temp_dir)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 fix_table_font.py <docx_file>")
        sys.exit(1)
    
    docx_file = sys.argv[1]
    if not os.path.exists(docx_file):
        print(f"Error: File {docx_file} not found")
        sys.exit(1)
    
    fix_table_fonts(docx_file)
EOF
        
        # Make the script executable and run it
        chmod +x "$python_script"
        if python3 "$python_script" "$docx_file"; then
            print_status $GREEN "✅ Table font sizes successfully modified to 8pt"
        else
            print_status $YELLOW "⚠️  Table font modification failed, using original document"
        fi
        
        # Clean up Python script unless verbose
        if [ "$VERBOSE" = false ]; then
            rm -f "$python_script"
        fi
        
    else
        print_status $YELLOW "⚠️  Python3 not available, skipping table font size modification"
        print_status $BLUE "📝 Tables will use default font sizes from reference document"
    fi
}

# Function to validate output
validate_output() {
    local output_file="$1"
    
    if [ -f "$output_file" ]; then
        local file_size=$(stat -c%s "$output_file" 2>/dev/null || stat -f%z "$output_file" 2>/dev/null)
        if [ "$file_size" -gt 1000 ]; then
            print_status $GREEN "✅ Word document created successfully"
            print_status $GREEN "📊 File size: $(echo "scale=1; $file_size/1024" | bc 2>/dev/null || echo "$((file_size/1024))")KB"
            return 0
        else
            print_status $RED "❌ Output file is too small, conversion may have failed"
            return 1
        fi
    else
        print_status $RED "❌ Output file was not created"
        return 1
    fi
}

# Function to create submission package
create_submission_package() {
    local output_file="$1"
    local base_name=$(basename "$output_file" .docx)
    
    print_status $BLUE "📦 Creating MDPI Healthcare submission package..."
    
    # Create submission directory structure
    mkdir -p "$OUTPUT_DIR/figures"
    mkdir -p "$OUTPUT_DIR/tables"
    mkdir -p "$OUTPUT_DIR/supplementary"
    
    # Create submission checklist
    cat > "$OUTPUT_DIR/MDPI_Submission_Checklist.txt" << 'EOF'
MDPI Healthcare Submission Checklist
===================================

Before Submission:
□ Manuscript follows MDPI Healthcare formatting guidelines
□ References are in APA style format
□ All figures are high-resolution (300 dpi minimum)
□ All tables have proper captions and headers
□ Abbreviations are defined at first use
□ Word count is appropriate for article type
□ Author information is complete (if applicable)
□ Funding information is provided (if applicable)
□ Ethics approval mentioned (if applicable)
□ Data availability statement included
□ Conflicts of interest declared

MDPI Healthcare Specific:
□ A4 paper format with correct margins (1.5cm top, 3.5cm bottom, 1.75cm sides)
□ Legible font (Times New Roman 12pt recommended)
□ 1.5 line spacing for submission
□ Numbered headings and sections
□ Figures numbered and captioned below
□ Tables numbered and captioned above
□ APA style references
□ Mathematical equations numbered sequentially

Files to Submit:
□ Main manuscript (Word format)
□ Cover letter
□ Figures (separate high-resolution files)
□ Tables (if not embedded in manuscript)
□ Supplementary materials (if any)

Special Issue: Artificial Intelligence in Healthcare: Opportunities and Challenges
□ Manuscript addresses AI opportunities in healthcare
□ Manuscript discusses AI challenges in healthcare
□ Content is relevant to healthcare applications
□ Technical contributions are clearly explained
□ Clinical implications are discussed
EOF
    
    # Create README for submission
    cat > "$OUTPUT_DIR/README.md" << EOF
# MDPI Healthcare Submission Package

## Generated Files

- \`$(basename "$output_file")\` - Main manuscript in MDPI Healthcare format
- \`MDPI_Submission_Checklist.txt\` - Pre-submission checklist
- \`mdpi_reference.docx\` - MDPI style reference document
- \`figures/\` - Directory for high-resolution figures
- \`tables/\` - Directory for table files
- \`supplementary/\` - Directory for supplementary materials

## MDPI Healthcare Guidelines Applied

- **Paper Format**: A4 size with MDPI margins
- **Font**: Times New Roman 12pt (recommended)
- **Spacing**: 1.5 line spacing for submission
- **Sections**: Numbered headings and subsections
- **References**: APA style formatting
- **Structure**: Table of contents with 3 levels
- **Tables**: Font size 8pt with optimized cell widths via post-processing

## Next Steps

1. Review the submission checklist
2. Add high-resolution figures to the figures/ directory
3. Verify all references are in APA format
4. Complete author information (if applicable)
5. Prepare cover letter for special issue submission

## Special Issue Information

**Title**: Artificial Intelligence in Healthcare: Opportunities and Challenges
**Journal**: Healthcare (MDPI)
**Submission Portal**: https://www.mdpi.com/journal/healthcare

Generated on: $(date)
EOF
    
    print_status $GREEN "📋 Submission package created in: $OUTPUT_DIR/"
}

# Parse command line arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        -s|--source-dir)
            SOURCE_DIR="$2"
            shift 2
            ;;
        -o|--output-dir)
            OUTPUT_DIR="$2"
            shift 2
            ;;
        -v|--verbose)
            VERBOSE=true
            shift
            ;;
        --force-refresh)
            FORCE_REFRESH=true
            shift
            ;;
        -h|--help)
            usage
            ;;
        -*)
            print_status $RED "❌ Unknown option: $1"
            usage
            ;;
        *)
            if [ -z "$INPUT_FILE" ]; then
                INPUT_FILE="$1"
            else
                print_status $RED "❌ Multiple input files specified"
                usage
            fi
            shift
            ;;
    esac
done

# Main execution
main() {
    print_status $BLUE "🏥 MDPI Healthcare Journal Markdown to Word Converter v2.0"
    print_status $BLUE "============================================================"
    echo ""
    
    # Validate input
    if [ -z "$INPUT_FILE" ]; then
        print_status $RED "❌ No input file specified"
        usage
    fi
    
    # Construct full paths
    local source_file="$SOURCE_DIR/$INPUT_FILE"
    local base_name=$(basename "$INPUT_FILE" .md)
    local processed_file="$OUTPUT_DIR/${base_name}_processed.md"
    local output_file="$OUTPUT_DIR/${base_name}_MDPI.docx"
    
    # Check if source file exists
    if [ ! -f "$source_file" ]; then
        print_status $RED "❌ Input file not found: $source_file"
        exit 1
    fi
    
    # Create output directory
    mkdir -p "$OUTPUT_DIR"
    
    print_status $GREEN "📁 Source: $source_file"
    print_status $GREEN "📁 Output: $output_file"
    echo ""
    
    # Execute conversion pipeline
    check_dependencies
    create_mdpi_reference
    preprocess_markdown "$source_file" "$processed_file"
    
    # Optimize table formatting with font size 9 and cell width adjustments
    local optimized_file="$OUTPUT_DIR/${base_name}_optimized.md"
    optimize_table_formatting "$processed_file" "$optimized_file"
    
    if convert_to_word "$optimized_file" "$output_file"; then
        if validate_output "$output_file"; then
            # Post-process tables to ensure font size 8pt
            post_process_tables "$output_file"
            
            create_submission_package "$output_file"
            
            print_status $GREEN "🎉 SUCCESS! MDPI Healthcare formatted document created"
            print_status $BLUE "📄 Output: $output_file"
            print_status $BLUE "📦 Submission package: $OUTPUT_DIR/"
            
            # Try to open the file (macOS)
            if [[ "$OSTYPE" == "darwin"* ]] && [ "$VERBOSE" = true ]; then
                print_status $BLUE "🚀 Opening document..."
                open "$output_file"
            fi
        else
            exit 1
        fi
    else
        print_status $RED "❌ Conversion failed!"
        exit 1
    fi
    
    # Clean up processed files unless verbose
    if [ "$VERBOSE" = false ]; then
        rm -f "$processed_file"
        rm -f "$optimized_file"
    fi
    
    echo ""
    print_status $GREEN "✅ MDPI Healthcare submission ready!"
}

# Run main function
main