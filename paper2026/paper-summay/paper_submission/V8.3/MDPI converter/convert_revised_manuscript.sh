#!/bin/bash

# MDPI Manuscript Conversion Script for Revised Version
# Converts V5_Healthcare_Submission_REVISED.md to Word using MDPI template
# Enhanced: Automatic figure detection and embedding

echo ""
echo "======================================================================"
echo "          MDPI Manuscript Converter with Figure Integration"
echo "======================================================================"
echo ""

# Configuration
INPUT_MD="../V5_Healthcare_Submission_REVISED.md"
OUTPUT_DIR="../docoutput"
OUTPUT_FILE="V5_Healthcare_Submission_REVISED_MDPI.docx"
FIGURES_DIR="../statistical analyis/figures"
TEMPLATE_FILE="../docoutput/msf-template.dot"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Helper function to print with color
print_status() {
    echo -e "${BLUE}➜${NC} $1"
}

print_success() {
    echo -e "${GREEN}✓${NC} $1"
}

print_error() {
    echo -e "${RED}✗${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}⚠${NC} $1"
}

# Check input file
print_status "Checking input files..."
if [ ! -f "$INPUT_MD" ]; then
    print_error "Input file not found: $INPUT_MD"
    exit 1
fi
print_success "Found input: $INPUT_MD"

# Check and log figures directory
print_status "Checking figures directory..."
if [ ! -d "$FIGURES_DIR" ]; then
    print_error "Figures directory not found: $FIGURES_DIR"
    print_status "Creating placeholder..."
    mkdir -p "$FIGURES_DIR"
    print_warning "Figures directory created but is empty"
    FIGURES_ARG=""
else
    FIG_COUNT=$(find "$FIGURES_DIR" -name "*.png" | wc -l)
    if [ $FIG_COUNT -gt 0 ]; then
        print_success "Found figures directory with $FIG_COUNT PNG files"
        echo "   Figures found:"
        ls -1 "$FIGURES_DIR"/*.png 2>/dev/null | head -5 | sed 's/^/     • /'
        if [ $FIG_COUNT -gt 5 ]; then
            echo "     ... and $((FIG_COUNT - 5)) more"
        fi
        FIGURES_ARG="-f $FIGURES_DIR"
    else
        print_error "Figures directory exists but contains no PNG files"
        FIGURES_ARG=""
    fi
fi

# Check template
print_status "Checking MDPI template..."
if [ ! -f "$TEMPLATE_FILE" ]; then
    print_warning "MDPI template not found: $TEMPLATE_FILE"
    print_status "Will use default MDPI formatting instead"
    TEMPLATE_ARG=""
else
    print_success "Found MDPI template: $TEMPLATE_FILE"
    TEMPLATE_ARG="-t $TEMPLATE_FILE"
fi

# Create output directories
print_status "Setting up output directories..."
mkdir -p "$OUTPUT_DIR"
mkdir -p "$OUTPUT_DIR/figures"
print_success "Output directory ready: $OUTPUT_DIR"

echo ""
echo "======================================================================"
echo "          CONVERSION PARAMETERS"
echo "======================================================================"
echo ""
echo "Input:        $INPUT_MD"
echo "Output:       $OUTPUT_DIR/$OUTPUT_FILE"
echo "Figures:      $FIGURES_DIR"
echo "Template:     ${TEMPLATE_FILE:-'(using default formatting)'}"
echo ""

# Run converter with enhanced error handling
print_status "Starting conversion..."
echo ""

python3 mdpi_template_converter.py "$INPUT_MD" \
    -o "$OUTPUT_DIR/$OUTPUT_FILE" \
    $FIGURES_ARG \
    $TEMPLATE_ARG

CONVERSION_RESULT=$?

echo ""
echo "======================================================================"

if [ $CONVERSION_RESULT -eq 0 ]; then
    print_success "Conversion completed successfully!"
    echo ""
    
    # Verify output file
    if [ -f "$OUTPUT_DIR/$OUTPUT_FILE" ]; then
        FILE_SIZE=$(ls -lh "$OUTPUT_DIR/$OUTPUT_FILE" | awk '{print $5}')
        print_success "Output file created: $FILE_SIZE"
        
        # Check for embedded figures
        EMBEDDED_FIGS=$(unzip -l "$OUTPUT_DIR/$OUTPUT_FILE" 2>/dev/null | grep -c "word/media/" || echo "0")
        print_success "Embedded media objects: $EMBEDDED_FIGS"
    fi
    
    echo ""
    echo "======================================================================"
    echo "                    ✓ MANUSCRIPT READY"
    echo "======================================================================"
    echo ""
    echo "Output files:"
    echo "  • Main: $OUTPUT_DIR/$OUTPUT_FILE"
    echo "  • Figs: $OUTPUT_DIR/figures/ (backup copies)"
    echo ""
    echo "Next Steps:"
    echo "  1. Open $OUTPUT_DIR/$OUTPUT_FILE in Microsoft Word"
    echo "  2. Verify all figures are embedded correctly"
    echo "  3. Check formatting and spacing"
    echo "  4. Add author names and affiliations"
    echo "  5. Review abstract and front matter"
    echo ""
    echo "======================================================================"
    echo ""
else
    print_error "Conversion failed with exit code $CONVERSION_RESULT"
    echo ""
    echo "Troubleshooting:"
    echo "  1. Check that Python 3 and required packages are installed:"
    echo "     pip install python-docx pyyaml"
    echo "  2. Verify all input files exist and are readable"
    echo "  3. Ensure figures directory contains PNG files"
    echo "  4. Check console output above for specific errors"
    echo ""
    echo "======================================================================"
    exit 1
fi

