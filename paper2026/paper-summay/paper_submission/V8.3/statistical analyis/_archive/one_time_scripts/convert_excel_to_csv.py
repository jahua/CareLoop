#!/usr/bin/env python3
"""
Convert Excel file tabs to individual CSV files.
Each sheet in the Excel file will be saved as a separate CSV file in the 'data' directory.
"""

import pandas as pd
import os
import sys
import csv

def convert_excel_to_csv(excel_file, output_dir="data"):
    """
    Convert each sheet in an Excel file to a separate CSV file.
    
    Args:
        excel_file (str): Path to the Excel file
        output_dir (str): Directory to save CSV files (default: 'data')
    """
    try:
        # Read the Excel file
        print(f"Reading Excel file: {excel_file}")
        xls = pd.ExcelFile(excel_file)
        
        # Create output directory if it doesn't exist
        os.makedirs(output_dir, exist_ok=True)
        print(f"Output directory: {output_dir}")
        print()
        
        # Convert each sheet to CSV
        for sheet_name in xls.sheet_names:
            # RESULTS sheet has a different structure (header in row 0)
            # All other sheets have metadata in rows 0-3, header in row 4
            if sheet_name == 'RESULTS' or sheet_name == 'TEMPLATE':
                # Check if first row looks like a proper header
                df_check = pd.read_excel(xls, sheet_name=sheet_name, nrows=1, header=None)
                first_cell = str(df_check.iloc[0, 0]) if pd.notna(df_check.iloc[0, 0]) else ""
                
                if first_cell and not first_cell.startswith('http') and first_cell != 'UUID':
                    # Header is in row 0
                    df = pd.read_excel(xls, sheet_name=sheet_name)
                else:
                    # Skip first 4 rows for TEMPLATE
                    df = pd.read_excel(xls, sheet_name=sheet_name, skiprows=[0, 1, 2, 3])
            else:
                # For A-1, A-2, etc., B-1, B-2, etc., always skip first 4 rows
                df = pd.read_excel(xls, sheet_name=sheet_name, skiprows=[0, 1, 2, 3])
            
            # Clean the sheet name for use as filename (replace special characters)
            clean_name = (sheet_name
                         .replace("/", "_")
                         .replace("\\", "_")
                         .replace(":", "_")
                         .replace("*", "_")
                         .replace("?", "_")
                         .replace('"', "_")
                         .replace("<", "_")
                         .replace(">", "_")
                         .replace("|", "_"))
            
            csv_filename = os.path.join(output_dir, f"{clean_name}.csv")
            # Use proper CSV settings for multi-line cells and special characters
            # quoting=csv.QUOTE_NONNUMERIC ensures text fields are properly quoted
            df.to_csv(csv_filename, index=False, encoding='utf-8-sig', 
                     quoting=csv.QUOTE_NONNUMERIC, doublequote=True, lineterminator='\n')
            print(f"✓ Converted '{sheet_name}' to '{csv_filename}' ({len(df)} rows, {len(df.columns)} columns)")
        
        print()
        print(f"Successfully converted {len(xls.sheet_names)} sheets to CSV files.")
        return True
        
    except FileNotFoundError:
        print(f"Error: File '{excel_file}' not found.")
        return False
    except Exception as e:
        print(f"Error: {str(e)}")
        return False

if __name__ == "__main__":
    # Default Excel file
    excel_file = "1-Evaluation-Simulated-Conversations.xlsx"
    
    # Allow command line argument for different Excel file
    if len(sys.argv) > 1:
        excel_file = sys.argv[1]
    
    # Run conversion
    success = convert_excel_to_csv(excel_file)
    sys.exit(0 if success else 1)

