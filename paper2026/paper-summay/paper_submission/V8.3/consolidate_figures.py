#!/usr/bin/env python3
"""
Figure Consolidation and Standardization Script
Consolidates all figures into one directory with uniform styling

Features:
- Identifies and removes duplicate figures
- Applies consistent styling (borders, DPI, dimensions)
- Creates a unified figures directory
- Generates figure index

Author: Unified Pipeline
Date: 2026
Version: 1.0
"""

import os
import shutil
from pathlib import Path
from PIL import Image, ImageDraw
import hashlib

# Configuration
SOURCE_DIRS = [
    "statistical analyis/figures",
    "figures",
    "V8.3/figures"
]

OUTPUT_DIR = "unified_figures"
TARGET_DPI = 300
MAX_WIDTH = 2400  # pixels at 300 DPI = 8 inches
BORDER_COLOR = (200, 200, 200)  # Light gray
BORDER_WIDTH = 2


def get_file_hash(filepath):
    """Calculate MD5 hash of file to detect duplicates."""
    hash_md5 = hashlib.md5()
    with open(filepath, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()


def standardize_figure(input_path, output_path):
    """
    Apply uniform styling to figure:
    - Ensure 300 DPI
    - Resize if too large
    - Add subtle border
    - Optimize for publication
    """
    try:
        img = Image.open(input_path)
        
        # Convert RGBA to RGB if needed
        if img.mode == 'RGBA':
            background = Image.new('RGB', img.size, (255, 255, 255))
            background.paste(img, mask=img.split()[3] if len(img.split()) == 4 else None)
            img = background
        elif img.mode != 'RGB':
            img = img.convert('RGB')
        
        # Resize if too large (maintain aspect ratio)
        if img.width > MAX_WIDTH:
            ratio = MAX_WIDTH / img.width
            new_height = int(img.height * ratio)
            img = img.resize((MAX_WIDTH, new_height), Image.Resampling.LANCZOS)
        
        # Add subtle border
        draw = ImageDraw.Draw(img)
        width, height = img.size
        for i in range(BORDER_WIDTH):
            draw.rectangle(
                [i, i, width-1-i, height-1-i],
                outline=BORDER_COLOR,
                width=1
            )
        
        # Save with high quality and DPI metadata
        img.save(
            output_path,
            'PNG',
            dpi=(TARGET_DPI, TARGET_DPI),
            optimize=True,
            quality=95
        )
        
        return True
    except Exception as e:
        print(f"  Error processing {input_path.name}: {e}")
        return False


def consolidate_figures():
    """Main consolidation process."""
    print("\n" + "="*70)
    print("FIGURE CONSOLIDATION AND STANDARDIZATION")
    print("="*70)
    
    # Create output directory
    output_dir = Path(OUTPUT_DIR)
    output_dir.mkdir(exist_ok=True)
    print(f"\nOutput directory: {OUTPUT_DIR}/")
    
    # Track figures by hash to detect duplicates
    figure_hashes = {}
    figure_inventory = {}
    duplicates = []
    
    # Scan all source directories
    print("\nScanning source directories:")
    for source_dir in SOURCE_DIRS:
        source_path = Path(source_dir)
        if not source_path.exists():
            continue
        
        png_files = list(source_path.glob("*.png"))
        print(f"  {source_dir}: {len(png_files)} figures")
        
        for fig_file in png_files:
            # Calculate hash
            file_hash = get_file_hash(fig_file)
            
            # Check for duplicates
            if file_hash in figure_hashes:
                duplicates.append({
                    'original': figure_hashes[file_hash],
                    'duplicate': str(fig_file)
                })
                continue
            
            # Store unique figure
            figure_hashes[file_hash] = str(fig_file)
            
            # Extract figure number from filename
            filename = fig_file.name
            if filename[0:2].isdigit():
                fig_num = filename[0:2]
            else:
                fig_num = filename.split('_')[0] if '_' in filename else filename
            
            figure_inventory[filename] = {
                'source': str(fig_file),
                'number': fig_num,
                'size': fig_file.stat().st_size
            }
    
    print(f"\n? Found {len(figure_inventory)} unique figures")
    if duplicates:
        print(f"? Identified {len(duplicates)} duplicates (will skip)")
    
    # Process and copy unique figures
    print("\nProcessing figures:")
    processed = 0
    failed = 0
    
    for filename, info in sorted(figure_inventory.items()):
        source = Path(info['source'])
        output = output_dir / filename
        
        # Apply standardization
        if standardize_figure(source, output):
            size_kb = output.stat().st_size / 1024
            print(f"  ? {filename} ({size_kb:.1f} KB)")
            processed += 1
        else:
            failed += 1
    
    # Generate index
    print("\nGenerating figure index...")
    index_path = output_dir / "FIGURE_INDEX.md"
    
    with open(index_path, 'w') as f:
        f.write("# Unified Figures Directory\n\n")
        f.write(f"**Total Figures:** {processed}\n")
        f.write(f"**Standard:** 300 DPI, Publication-ready\n\n")
        f.write("---\n\n")
        f.write("## Figure Inventory\n\n")
        f.write("| # | Filename | Size | Source |\n")
        f.write("|---|----------|------|--------|\n")
        
        for filename, info in sorted(figure_inventory.items()):
            output = output_dir / filename
            if output.exists():
                size_kb = output.stat().st_size / 1024
                f.write(f"| {info['number']} | {filename} | {size_kb:.1f} KB | {Path(info['source']).parent.name} |\n")
        
        if duplicates:
            f.write("\n---\n\n## Duplicates Removed\n\n")
            for dup in duplicates:
                f.write(f"- {dup['duplicate']} (duplicate of {dup['original']})\n")
    
    # Summary
    print("\n" + "="*70)
    print("? CONSOLIDATION COMPLETE")
    print("="*70)
    print(f"\n?? Summary:")
    print(f"  � Unique figures: {processed}")
    print(f"  � Duplicates removed: {len(duplicates)}")
    print(f"  � Failed: {failed}")
    print(f"  � Output: {OUTPUT_DIR}/")
    print(f"\n?? Files:")
    print(f"  � Figures: {processed} PNG files")
    print(f"  � Index: FIGURE_INDEX.md")
    print(f"\n? All figures standardized:")
    print(f"  � Resolution: 300 DPI")
    print(f"  � Max width: {MAX_WIDTH}px (8 inches)")
    print(f"  � Border: Subtle gray frame")
    print(f"  � Format: Optimized PNG")
    print("\n" + "="*70)
    
    return processed, len(duplicates)


if __name__ == "__main__":
    try:
        consolidate_figures()
    except Exception as e:
        print(f"\n? Error: {e}")
        import traceback
        traceback.print_exc()
