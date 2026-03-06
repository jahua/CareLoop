#!/usr/bin/env python3
"""
Figure Renumbering and Styling Unification
Renumbers all figures sequentially and applies uniform publication style

Author: Unified Pipeline
Date: 2026
Version: 1.0
"""

import os
import shutil
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import sys

# Figure Renumbering Scheme - Proper Sequential Order
FIGURE_RENUMBERING = {
    # System Architecture & Study Design (Figures 1-2)
    '10_system_architecture.png': ('Figure_01_System_Architecture.png', 'System Architecture Overview'),
    '11_study_design_flowchart.png': ('Figure_02_Study_Design.png', 'Study Design and Methodology'),
    
    # Theoretical Framework & Pipelines (Figures 3-7)
    '16_trait_to_zurich_mapping.png': ('Figure_03_Theoretical_Framework.png', 'Big Five to Zurich Model Mapping'),
    '13_data_flow_pipeline.png': ('Figure_04_Data_Flow.png', 'Data Processing Pipeline'),
    '14_detection_pipeline.png': ('Figure_05_Detection_Process.png', 'Personality Detection Process'),
    '15_regulation_prompt_assembly.png': ('Figure_06_Regulation_System.png', 'Regulation and Prompt Assembly'),
    '12_evaluation_framework.png': ('Figure_07_Evaluation_Framework.png', 'Evaluation Methodology'),
    
    # Statistical Results (Figures 8-13)
    '01_sample_distribution.png': ('Figure_08_Sample_Distribution.png', 'Sample Characteristics'),
    '03_performance_comparison.png': ('Figure_09_Performance_Comparison.png', 'Regulated vs Baseline Performance'),
    '04_effect_sizes.png': ('Figure_10_Effect_Sizes.png', 'Effect Sizes (Cohen\'s d)'),
    '06_personality_dimensions.png': ('Figure_11_Personality_Dimensions.png', 'OCEAN Personality Dimensions'),
    '07_personality_heatmap.png': ('Figure_12_Personality_Heatmap.png', 'Personality Vector Heatmap'),
    '08_weighted_scores.png': ('Figure_13_Weighted_Scores.png', 'Weighted Scoring Analysis'),
    
    # Remove these duplicates/redundant figures
    '10_system_overview.png': None,  # Use detailed version instead
    '11_study_workflow.png': None,   # Use detailed version instead
    '02_missing_data_heatmap.png': None,  # Redundant
    '05_percentage_improvement.png': None,  # Redundant with effect sizes
    '09_total_score_boxplot.png': None,  # Redundant
}

# Publication Style Configuration
STYLE_CONFIG = {
    'dpi': 300,
    'max_width': 2400,  # 8 inches at 300 DPI
    'max_height': 1800,  # 6 inches at 300 DPI
    'border_width': 3,
    'border_color': (220, 220, 220),  # Light gray
    'background': (255, 255, 255),  # White
    'quality': 95
}


def apply_uniform_style(input_path, output_path, config=STYLE_CONFIG):
    """
    Apply uniform publication-quality styling to figure.
    
    - Ensures 300 DPI
    - Resizes to fit publication standards
    - Adds subtle professional border
    - Optimizes for print quality
    - Ensures white background
    """
    try:
        img = Image.open(input_path)
        
        # Convert to RGB with white background
        if img.mode == 'RGBA':
            background = Image.new('RGB', img.size, config['background'])
            background.paste(img, mask=img.split()[3])
            img = background
        elif img.mode != 'RGB':
            img = img.convert('RGB')
        
        # Resize if exceeds maximum dimensions (maintain aspect ratio)
        width, height = img.size
        if width > config['max_width'] or height > config['max_height']:
            ratio = min(config['max_width'] / width, config['max_height'] / height)
            new_width = int(width * ratio)
            new_height = int(height * ratio)
            img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
            print(f"      Resized: {width}x{height} -> {new_width}x{new_height}")
        
        # Add professional border
        draw = ImageDraw.Draw(img)
        w, h = img.size
        
        # Draw border
        for i in range(config['border_width']):
            draw.rectangle(
                [i, i, w-1-i, h-1-i],
                outline=config['border_color'],
                width=1
            )
        
        # Save with publication quality
        img.save(
            output_path,
            'PNG',
            dpi=(config['dpi'], config['dpi']),
            optimize=True,
            quality=config['quality']
        )
        
        size_kb = output_path.stat().st_size / 1024
        return True, size_kb
        
    except Exception as e:
        print(f"      Error: {e}")
        return False, 0


def renumber_and_style_figures(source_dir='unified_figures', output_dir='final_figures'):
    """Main renumbering and styling process."""
    
    print("\n" + "="*70)
    print("FIGURE RENUMBERING AND STYLE UNIFICATION")
    print("="*70)
    
    source_path = Path(source_dir)
    output_path = Path(output_dir)
    
    if not source_path.exists():
        print(f"\nError: Source directory not found: {source_dir}")
        return False
    
    # Create output directory
    output_path.mkdir(exist_ok=True)
    print(f"\nSource: {source_dir}/")
    print(f"Output: {output_dir}/")
    
    # Process figures
    print("\nProcessing and renumbering figures:")
    print("-" * 70)
    
    processed = []
    skipped = []
    
    for old_name, mapping in FIGURE_RENUMBERING.items():
        source_file = source_path / old_name
        
        if not source_file.exists():
            print(f"\n  Warning: {old_name} not found (skipping)")
            continue
        
        # Skip if marked for removal
        if mapping is None:
            skipped.append(old_name)
            print(f"\n  SKIP: {old_name}")
            print(f"        (Redundant/duplicate - removed)")
            continue
        
        new_name, caption = mapping
        output_file = output_path / new_name
        
        print(f"\n  {old_name}")
        print(f"    -> {new_name}")
        print(f"    Caption: {caption}")
        
        # Apply styling
        success, size_kb = apply_uniform_style(source_file, output_file)
        
        if success:
            print(f"    Size: {size_kb:.1f} KB")
            print(f"    Status: OK")
            processed.append({
                'old': old_name,
                'new': new_name,
                'caption': caption,
                'size': size_kb
            })
        else:
            print(f"    Status: FAILED")
    
    # Generate figure index
    index_file = output_path / 'FIGURE_INDEX.md'
    with open(index_file, 'w', encoding='utf-8') as f:
        f.write("# Final Figures - Complete Index\n\n")
        f.write(f"**Total Figures:** {len(processed)}\n")
        f.write(f"**Removed:** {len(skipped)} redundant figures\n")
        f.write(f"**Quality:** 300 DPI, Publication-ready\n\n")
        f.write("---\n\n")
        f.write("## Figure List\n\n")
        f.write("| # | Filename | Caption | Size |\n")
        f.write("|---|----------|---------|------|\n")
        
        for fig in processed:
            fig_num = fig['new'].split('_')[1]  # Extract number
            f.write(f"| {fig_num} | {fig['new']} | {fig['caption']} | {fig['size']:.1f} KB |\n")
        
        f.write("\n---\n\n")
        f.write("## Removed Figures (Redundant)\n\n")
        for skipped_fig in skipped:
            f.write(f"- {skipped_fig}\n")
        
        f.write("\n---\n\n")
        f.write("## Usage in Manuscript\n\n")
        f.write("Reference figures sequentially:\n\n")
        for fig in processed:
            fig_num = fig['new'].split('_')[1]
            f.write(f"- Figure {fig_num}: {fig['caption']}\n")
        
        f.write("\n---\n\n")
        f.write("**All figures ready for publication**\n")
    
    # Summary
    print("\n" + "="*70)
    print("RENUMBERING COMPLETE")
    print("="*70)
    print(f"\nProcessed: {len(processed)} figures")
    print(f"Removed: {len(skipped)} redundant figures")
    print(f"Output: {output_dir}/")
    print(f"\nAll figures:")
    print("  - Renumbered sequentially (01-13)")
    print("  - Uniform style applied (300 DPI, borders)")
    print("  - Optimized for publication")
    print("  - Indexed in FIGURE_INDEX.md")
    print("\n" + "="*70)
    
    return True


if __name__ == "__main__":
    success = renumber_and_style_figures()
    sys.exit(0 if success else 1)
