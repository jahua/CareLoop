#!/usr/bin/env python3
"""
Generate manuscript diagrams.

Runs all generator scripts to create Figures 10-13:
- create_submission_diagrams.py -> Figures 10, 12, 13
- create_study_design_flowchart.py -> Figure 11

Figures 14-16 are maintained separately (see README.md).

Usage:
    cd figures/src
    python generate_all.py
"""

from pathlib import Path
import subprocess
import sys


def main():
    src_dir = Path(__file__).parent
    
    print("=" * 60)
    print("Generating manuscript diagrams...")
    print("=" * 60)
    print()
    
    scripts = [
        ("create_system_overview.py", "Figure 10 (system overview)"),
        ("create_submission_diagrams.py", "Figures 12, 13"),
        ("create_study_design_flowchart.py", "Figure 11"),
        ("create_detection_architecture.py", "Figure 14 (detection pipeline - layered)"),
        ("create_mdpi_architecture.py", "MDPI system architecture (PDF + PNG)"),
        ("create_mdpi_study_design.py", "MDPI study design flowchart (PDF + PNG)"),
    ]
    
    for script, desc in scripts:
        print(f"Running {script} ({desc})...")
        result = subprocess.run(
            [sys.executable, script],
            cwd=src_dir,
            capture_output=True,
            text=True
        )
        
        if result.returncode != 0:
            print(f"  ✗ ERROR")
            print(result.stderr)
            sys.exit(1)
        else:
            print(f"  ✓ Success")
            if result.stdout.strip():
                for line in result.stdout.strip().split('\n'):
                    print(f"    {line}")
        print()
    
    print("=" * 60)
    print("✓ All diagrams generated successfully")
    print(f"  Output: {src_dir.parent}/")
    print("=" * 60)


if __name__ == "__main__":
    main()
