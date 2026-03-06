#!/usr/bin/env python3
"""
Merge regulated conversation data from all conversation CSV files.
Creates a merged CSV with modified MSG. NO. format (e.g., A-1-1, A-1-2, etc.)
"""

import pandas as pd
import os
import glob

def merge_regulated_data(data_dir="data", output_dir="merged"):
    """
    Merge regulated columns from all conversation CSV files.
    
    Args:
        data_dir (str): Directory containing the CSV files
        output_dir (str): Directory to save the merged file
    """
    # Columns to extract (REGULATED columns only)
    regulated_columns = [
        'MSG. NO.',
        'ASSISTANT START',
        'USER REPLY',
        'DETECTED PERSONALITY (O,C,E,A,N)',
        'REGULATION PROMPT APPLIED',
        'ASSISTANT REPLY (REG)',
        'DETECTION ACCURATE',
        'REGULATION EFFECTIVE',
        'EMOTIONAL TONE APPROPRIATE',
        'RELEVANCE & COHERENCE',
        'PERSONALITY NEEDS ADDRESSED',
        'EVALUATORS NOTES (REGULATED)'
    ]
    
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    
    # Find all conversation CSV files (A-1 through A-5, B-1 through B-5)
    pattern = os.path.join(data_dir, '[AB]-[0-9].csv')
    csv_files = sorted(glob.glob(pattern))
    
    if not csv_files:
        print(f"No conversation CSV files found in {data_dir}")
        return False
    
    print(f"Found {len(csv_files)} conversation files:")
    for f in csv_files:
        print(f"  - {os.path.basename(f)}")
    print()
    
    # List to store all dataframes
    all_dfs = []
    
    # Process each CSV file
    for csv_file in csv_files:
        filename = os.path.basename(csv_file).replace('.csv', '')
        print(f"Processing {filename}...")
        
        try:
            # Read the CSV file
            df = pd.read_csv(csv_file)
            
            # Select only the regulated columns
            df_regulated = df[regulated_columns].copy()
            
            # Create new MSG. NO. with format: filename-message_number
            # Handle NaN values in MSG. NO.
            df_regulated['MSG. NO.'] = df_regulated['MSG. NO.'].apply(
                lambda x: f"{filename}-{int(x)}" if pd.notna(x) else None
            )
            
            # Remove rows where MSG. NO. is None (empty rows)
            df_regulated = df_regulated.dropna(subset=['MSG. NO.'])
            
            print(f"  Added {len(df_regulated)} rows from {filename}")
            
            # Append to the list
            all_dfs.append(df_regulated)
            
        except Exception as e:
            print(f"  Error processing {filename}: {str(e)}")
            continue
    
    if not all_dfs:
        print("No data to merge!")
        return False
    
    # Concatenate all dataframes
    print("\nMerging all data...")
    merged_df = pd.concat(all_dfs, ignore_index=True)
    
    # Save to CSV
    output_file = os.path.join(output_dir, "regulated.csv")
    import csv
    merged_df.to_csv(output_file, index=False, encoding='utf-8-sig',
                    quoting=csv.QUOTE_NONNUMERIC, doublequote=True, lineterminator='\n')
    
    print(f"\n✓ Successfully merged {len(merged_df)} rows from {len(csv_files)} files")
    print(f"✓ Output saved to: {output_file}")
    print(f"\nMerged file info:")
    print(f"  Shape: {merged_df.shape} (rows, columns)")
    print(f"  Columns: {len(merged_df.columns)}")
    print(f"\nSample MSG. NO. values:")
    print(f"  {merged_df['MSG. NO.'].head(10).tolist()}")
    
    return True

if __name__ == "__main__":
    success = merge_regulated_data()
    exit(0 if success else 1)



