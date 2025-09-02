#!/bin/bash

# Convert Markdown to Word script that always saves to docoutput directory
# Usage: ./convert_to_docx.sh filename.md [template.docx] [--edit-original] [--compact]

# Set the directory containing this script
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PARENT_DIR="$(dirname "$SCRIPT_DIR")"
DOCOUTPUT_DIR="$PARENT_DIR/docoutput"

# Check if at least one argument is provided
if [ $# -lt 1 ]; then
    echo "Usage: $0 <input_markdown_file> [template_docx_file] [--edit-original] [--compact]"
    echo "  --edit-original    Edit the original markdown file to fix numbering"
    echo "  --compact          Use space-saving compact formatting (11pt Arial, 1.15 spacing, 2cm margins)"
    exit 1
fi

# Get the input markdown file
INPUT_FILE="$1"
INPUT_FILENAME=$(basename "$INPUT_FILE")
INPUT_NAME="${INPUT_FILENAME%.*}"

# Check if template is provided
TEMPLATE_ARG=""
EDIT_ORIGINAL=""
COMPACT_MODE=""

# Parse arguments
shift  # Remove the input file argument
while [ $# -gt 0 ]; do
    case "$1" in
        --edit-original)
            EDIT_ORIGINAL="--edit-original"
            shift
            ;;
        --compact)
            COMPACT_MODE="--compact"
            shift
            ;;
        *)
            # Assume this is a template file
            TEMPLATE_ARG="--template $1"
            shift
            ;;
    esac
done

# Create the docoutput directory if it doesn't exist
mkdir -p "$DOCOUTPUT_DIR"

# Run the conversion script
echo "Converting $INPUT_FILE to $DOCOUTPUT_DIR/$INPUT_NAME.docx"
python "$SCRIPT_DIR/academic_md2word.py" "$INPUT_FILE" "$DOCOUTPUT_DIR/$INPUT_NAME.docx" $TEMPLATE_ARG $EDIT_ORIGINAL $COMPACT_MODE

# Check the result
if [ $? -eq 0 ]; then
    echo "Conversion successful! Output saved to $DOCOUTPUT_DIR/$INPUT_NAME.docx"
    
    # Print formatting information
    if [ -n "$COMPACT_MODE" ]; then
        echo "Used compact formatting: 11pt Arial, 1.15 spacing, 2cm margins"
    else
        echo "Used standard academic formatting: 12pt Times New Roman, 1.5 spacing, 2.5cm margins"
    fi
    
else
    echo "Conversion failed!"
    exit 1
fi 