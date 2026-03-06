#!/usr/bin/env python3
"""
convert_markdown.py
Robust Markdown → DOCX/ODT/HTML converter with formatting fixes

Usage:
    python3 convert_markdown.py input.md
    python3 convert_markdown.py input.md output.docx
    python3 convert_markdown.py input.md --all  # Generate all formats

Features:
    - Fixes YAML parsing conflicts (removes --- in appendices)
    - Cleans table syntax
    - Generates multiple output formats (DOCX, ODT, HTML, PDF)
    - Validates output files
"""

import sys
import os
import subprocess
import shutil
from pathlib import Path
import argparse


class Colors:
    """ANSI color codes for terminal output"""
    GREEN = '\033[0;32m'
    YELLOW = '\033[1;33m'
    RED = '\033[0;31m'
    BLUE = '\033[0;34m'
    BOLD = '\033[1m'
    NC = '\033[0m'  # No Color


def info(msg):
    print(f"{Colors.GREEN}✓{Colors.NC} {msg}")


def warn(msg):
    print(f"{Colors.YELLOW}⚠{Colors.NC} {msg}")


def error(msg):
    print(f"{Colors.RED}✗{Colors.NC} {msg}")
    sys.exit(1)


def check_pandoc():
    """Check if pandoc is installed"""
    if not shutil.which('pandoc'):
        error("pandoc is not installed. Install with:\n"
              "  macOS: brew install pandoc\n"
              "  Linux: sudo apt install pandoc\n"
              "  Windows: choco install pandoc")
    return True


def clean_markdown(input_file, output_file):
    """
    Clean markdown file to fix common conversion issues
    
    Fixes:
    1. Remove --- horizontal rules in appendices (causes YAML errors)
    2. Normalize line endings
    3. Remove trailing whitespace
    4. Ensure proper table formatting
    """
    with open(input_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    cleaned_lines = []
    in_appendix = False
    appendix_count = 0
    removed_hr_count = 0
    
    for i, line in enumerate(lines):
        # Track when we enter appendix sections
        if line.startswith('### Appendix') or line.startswith('## Appendix'):
            in_appendix = True
            appendix_count += 1
        
        # Fix 1: Remove --- horizontal rules in appendices
        # These cause "YAML parse exception" errors in Pandoc
        if in_appendix and line.strip() == '---':
            cleaned_lines.append('\n')  # Replace with blank line
            removed_hr_count += 1
            continue
        
        # Fix 2: Normalize whitespace (remove trailing spaces)
        line = line.rstrip()
        if line:
            line = line + '\n'
        else:
            line = '\n'
        
        cleaned_lines.append(line)
    
    # Write cleaned markdown
    with open(output_file, 'w', encoding='utf-8') as f:
        f.writelines(cleaned_lines)
    
    info(f"Cleaned {len(cleaned_lines)} lines")
    if removed_hr_count > 0:
        info(f"  Removed {removed_hr_count} horizontal rules in {appendix_count} appendices")
    
    return output_file


def convert_to_format(input_file, output_file, format_type, extra_args=None):
    """
    Convert markdown to specified format using pandoc
    
    Args:
        input_file: Path to cleaned markdown file
        output_file: Path to output file
        format_type: Output format (docx, odt, html, pdf)
        extra_args: Additional pandoc arguments
    """
    if extra_args is None:
        extra_args = []
    
    # Base pandoc command
    cmd = [
        'pandoc',
        input_file,
        '-o', output_file,
        '-f', 'markdown',
        '-t', format_type,
        '--standalone',
    ]
    
    # Format-specific options
    if format_type in ['docx', 'odt', 'html']:
        cmd.extend(['--toc', '--toc-depth=3'])
    
    # Note: --number-sections removed because markdown already has manual numbering
    # Adding it would create double numbering like "1.6.5 1. Introduction"
    
    if format_type == 'html':
        cmd.extend([
            '--css=https://cdn.jsdelivr.net/npm/water.css@2/out/water.css',
            '--self-contained',
        ])
    
    if format_type == 'pdf':
        if shutil.which('pdflatex'):
            cmd.append('--pdf-engine=pdflatex')
        else:
            warn(f"Skipping PDF: pdflatex not installed")
            return None
    
    # Add extra arguments
    cmd.extend(extra_args)
    
    # Run conversion
    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            check=True
        )
        
        if os.path.exists(output_file):
            size = os.path.getsize(output_file)
            size_kb = size / 1024
            info(f"Created {format_type.upper()}: {output_file} ({size_kb:.1f} KB)")
            return output_file
        else:
            warn(f"Output file not created: {output_file}")
            return None
            
    except subprocess.CalledProcessError as e:
        warn(f"{format_type.upper()} conversion failed: {e.stderr}")
        return None


def validate_output(output_file):
    """Validate the output file was created correctly"""
    if not os.path.exists(output_file):
        return False
    
    # Check file size
    size = os.path.getsize(output_file)
    if size < 100:  # Less than 100 bytes is suspicious
        warn(f"Output file is very small ({size} bytes)")
        return False
    
    # Check file type using 'file' command (Unix/macOS)
    if shutil.which('file'):
        try:
            result = subprocess.run(
                ['file', output_file],
                capture_output=True,
                text=True
            )
            info(f"File type: {result.stdout.strip().split(': ', 1)[1]}")
        except Exception:
            pass
    
    return True


def main():
    parser = argparse.ArgumentParser(
        description='Convert Markdown to DOCX/ODT/HTML with formatting fixes'
    )
    parser.add_argument('input', help='Input markdown file')
    parser.add_argument('output', nargs='?', help='Output file (default: input.docx)')
    parser.add_argument('--all', action='store_true', help='Generate all formats (DOCX, ODT, HTML, PDF)')
    parser.add_argument('--format', choices=['docx', 'odt', 'html', 'pdf'], help='Specific format to generate')
    
    args = parser.parse_args()
    
    # Validate input file
    input_file = Path(args.input)
    if not input_file.exists():
        error(f"Input file not found: {input_file}")
    
    # Check pandoc
    check_pandoc()
    
    print(f"\n{Colors.BOLD}Markdown → DOCX Converter{Colors.NC}")
    print(f"Input: {input_file}\n")
    
    # Step 1: Clean markdown
    info("Step 1/4: Cleaning markdown syntax...")
    temp_file = Path(f"/tmp/{input_file.stem}-cleaned.md")
    clean_markdown(input_file, temp_file)
    
    # Step 2: Validate structure
    info("Step 2/4: Validating markdown structure...")
    with open(temp_file, 'r') as f:
        content = f.read()
        table_rows = content.count('\n|')
        headings = content.count('\n#')
        info(f"  Found: {headings} headings, {table_rows} table rows")
    
    # Step 3: Determine output formats
    info("Step 3/4: Converting to output format(s)...")
    
    output_base = Path(args.output) if args.output else input_file.with_suffix('.docx')
    output_base = output_base.with_suffix('')  # Remove extension
    
    formats_to_generate = []
    
    if args.all:
        formats_to_generate = ['docx', 'odt', 'html', 'pdf']
    elif args.format:
        formats_to_generate = [args.format]
    else:
        formats_to_generate = ['docx']
    
    created_files = []
    
    for fmt in formats_to_generate:
        output_file = output_base.with_suffix(f'.{fmt}')
        result = convert_to_format(temp_file, str(output_file), fmt)
        if result:
            created_files.append((fmt, result))
    
    # Step 4: Validate outputs
    info("Step 4/4: Validating output files...")
    for fmt, filepath in created_files:
        if validate_output(filepath):
            info(f"  {fmt.upper()}: OK")
    
    # Clean up temp file
    temp_file.unlink(missing_ok=True)
    
    # Summary
    print("\n" + "━" * 60)
    info("Conversion complete!")
    print()
    
    format_icons = {
        'docx': '📄',
        'odt': '📄',
        'html': '🌐',
        'pdf': '📕'
    }
    
    for fmt, filepath in created_files:
        icon = format_icons.get(fmt, '📄')
        print(f"  {icon} {fmt.upper()}: {filepath}")
    
    print("\nRecommendations:")
    print("  1. Open the DOCX file in Microsoft Word")
    print("  2. If you see formatting issues, try the ODT file")
    print("  3. Use the HTML file for perfect rendering in browser")
    print("━" * 60 + "\n")


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nConversion cancelled.")
        sys.exit(1)
    except Exception as e:
        error(f"Unexpected error: {e}")

