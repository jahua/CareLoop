#!/bin/bash
# Helper script to run statistical analysis with virtual environment

# Get the directory of this script
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Path to virtual environment (3 levels up from this directory)
VENV_PATH="$SCRIPT_DIR/../../../.venv"

echo "============================================"
echo "Running Statistical Analysis"
echo "============================================"
echo ""
echo "Activating virtual environment..."
source "$VENV_PATH/bin/activate"

echo "Virtual environment activated."
echo "Python version: $(python --version)"
echo ""

cd "$SCRIPT_DIR"

echo "Running analysis..."
echo ""

python statistical_analysis.py

echo ""
echo "============================================"
echo "Analysis Complete!"
echo "============================================"



