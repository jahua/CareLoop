#!/usr/bin/env python3
"""
Update manuscript figure references to sequential numbering
Converts old figure numbers (10-16) to new sequential (1-13)
"""

import re
from pathlib import Path

# Figure renumbering mapping
RENUMBERING_MAP = {
    # Old manuscript numbers -> New sequential numbers
    'Figure 11': 'Figure 1',  # Study Design
    'Figure 10': 'Figure 2',  # System Architecture
    'Figure 13': 'Figure 3',  # Data Flow
    'Figure 14': 'Figure 4',  # Detection
    'Figure 16': 'Figure 5',  # Trait Mapping
    'Figure 15': 'Figure 6',  # Regulation
    'Figure 12': 'Figure 7',  # Evaluation
    # Results section (currently text-only)
    'Figure 1': 'Figure 8',   # Sample
    'Figure 2': 'Figure 9',   # Missing data
    'Figure 3': 'Figure 10',  # Performance
    'Figure 4': 'Figure 11',  # Effect sizes
    'Figure 5': 'Figure 12',  # Personality dims
    'Figure 6': 'Figure 13',  # Personality heatmap
    'Figure 7': 'Figure 14',  # Weighted scores
    'Figure 8': 'Figure 15',  # Box plots
    'Figure 9': 'Figure 16',  # Total scores
}

# Filename mapping for markdown images
# Match actual filenames in final_figures/
FILENAME_RENUMBERING = {
    '11_study_design_flowchart.png': 'Figure_02_Study_Design.png',  # Fix: Figure 2 not 1
    '10_system_architecture.png': 'Figure_01_System_Architecture.png',  # Fix: Figure 1 not 2
    '13_data_flow_pipeline.png': 'Figure_04_Data_Flow.png',
    '14_detection_pipeline.png': 'Figure_05_Detection_Process.png',
    '16_trait_to_zurich_mapping.png': 'Figure_03_Theoretical_Framework.png',
    '15_regulation_prompt_assembly.png': 'Figure_06_Regulation_System.png',
    '12_evaluation_framework.png': 'Figure_07_Evaluation_Framework.png',
}


def renumber_figures_in_manuscript(input_file, output_file):
    """Update figure references to sequential numbering."""
    
    with open(input_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    print(f"Processing: {input_file}")
    print("="*70)
    
    # Replace figure references in text
    replacements_made = {}
    for old_ref, new_ref in RENUMBERING_MAP.items():
        # Count occurrences
        count = content.count(old_ref)
        if count > 0:
            content = content.replace(old_ref, new_ref)
            replacements_made[old_ref] = (new_ref, count)
            print(f"  {old_ref} -> {new_ref} ({count} instances)")
    
    # Replace filenames in markdown image syntax
    for old_file, new_file in FILENAME_RENUMBERING.items():
        if old_file in content:
            content = content.replace(f'figures/{old_file}', f'final_figures/{new_file}')
            print(f"  Image: {old_file} -> {new_file}")
    
    # Write updated manuscript
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("="*70)
    print(f"? Updated manuscript saved: {output_file}")
    print(f"? Total replacements: {sum(c for _, c in replacements_made.values())}")
    
    return True


if __name__ == "__main__":
    input_file = "V8.2.3.md"
    output_file = "V8.2.3_renumbered.md"
    
    print("\nFigure Renumbering Script")
    print("="*70)
    
    renumber_figures_in_manuscript(input_file, output_file)
    
    print("\n" + "="*70)
    print("? COMPLETE")
    print("="*70)
    print(f"\nUpdated manuscript: {output_file}")
    print("\nNext step: Convert with MDPI converter")
    print(f"  python3 'MDPI converter/convert_final.py' {output_file}")
    print()
