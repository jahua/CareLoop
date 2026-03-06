#!/bin/bash
#
# Enhanced MDPI Manuscript Converter
# -----------------------------------
# Converts V4_Healthcare_Submission_processed.md to MDPI-compliant Word format
# with all figures, tables, and supplementary materials exported
#

# Set paths
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
MANUSCRIPT="$PROJECT_ROOT/V4_Healthcare_Submission_processed.md"
OUTPUT_DIR="$PROJECT_ROOT/docoutput"
FIGURES_DIR="$PROJECT_ROOT/statistical analyis/figures"
OUTPUT_NAME="V4_Healthcare_Submission_MDPI.docx"

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo ""
echo "======================================================================"
echo "          MDPI Enhanced Manuscript Converter"
echo "======================================================================"
echo ""

# Check if manuscript exists
if [ ! -f "$MANUSCRIPT" ]; then
    echo -e "${RED}ERROR: Manuscript not found at:${NC}"
    echo "  $MANUSCRIPT"
    exit 1
fi

echo -e "${BLUE}Input manuscript:${NC} $MANUSCRIPT"
echo -e "${BLUE}Output directory:${NC} $OUTPUT_DIR"
echo -e "${BLUE}Figures directory:${NC} $FIGURES_DIR"
echo ""

# Check if figures directory exists
if [ ! -d "$FIGURES_DIR" ]; then
    echo -e "${YELLOW}WARNING: Figures directory not found. Figures will not be inserted.${NC}"
    echo "  Expected: $FIGURES_DIR"
    FIGURES_ARG=""
else
    echo -e "${GREEN}✓ Found figures directory${NC}"
    FIGURES_ARG="-f \"$FIGURES_DIR\""
fi

# Check if Python script exists
CONVERTER="$SCRIPT_DIR/mdpi_enhanced_converter.py"
if [ ! -f "$CONVERTER" ]; then
    echo -e "${RED}ERROR: Converter script not found at:${NC}"
    echo "  $CONVERTER"
    exit 1
fi

# Check Python dependencies
echo ""
echo "Checking Python dependencies..."
if ! python3 -c "import docx" 2>/dev/null; then
    echo -e "${YELLOW}Installing python-docx...${NC}"
    pip3 install python-docx
fi

# Run conversion
echo ""
echo "Starting conversion..."
echo "----------------------------------------------------------------------"

if [ -z "$FIGURES_ARG" ]; then
    python3 "$CONVERTER" "$MANUSCRIPT" -o "$OUTPUT_DIR" -n "$OUTPUT_NAME"
else
    python3 "$CONVERTER" "$MANUSCRIPT" -o "$OUTPUT_DIR" -f "$FIGURES_DIR" -n "$OUTPUT_NAME"
fi

RESULT=$?

echo "----------------------------------------------------------------------"
echo ""

# Check result
if [ $RESULT -eq 0 ]; then
    echo -e "${GREEN}✓ CONVERSION SUCCESSFUL!${NC}"
    echo ""
    echo "Output files:"
    echo "  • Main manuscript: $OUTPUT_DIR/$OUTPUT_NAME"
    echo "  • Figures: $OUTPUT_DIR/figures/"
    echo "  • Supplementary: $OUTPUT_DIR/supplementary/"
    echo ""
    echo "Next steps:"
    echo "  1. Open $OUTPUT_NAME in Microsoft Word"
    echo "  2. Review figure placements and captions"
    echo "  3. Check table formatting"
    echo "  4. Verify abstract is single paragraph"
    echo "  5. Confirm all references are formatted [1] before punctuation"
    echo "  6. Add author information in front matter"
    echo "  7. Submit to MDPI"
    echo ""
else
    echo -e "${RED}✗ CONVERSION FAILED${NC}"
    echo "Check error messages above for details."
    echo ""
    exit 1
fi

echo "======================================================================"
echo ""



