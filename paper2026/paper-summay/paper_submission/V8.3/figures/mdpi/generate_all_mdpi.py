#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Master script to regenerate all MDPI-ready figures for journal submission.
"""

import subprocess
import sys
from pathlib import Path

def main():
    scripts = [
        "create_mdpi_architecture.py",
        "create_mdpi_study_design.py",
        "create_mdpi_data_flow.py",
        "create_mdpi_detection_pipeline.py",
        "create_mdpi_trait_mapping.py",
        "create_mdpi_regulation_workflow.py",
        "create_mdpi_evaluation_framework.py"
    ]
    
    base_dir = Path(__file__).resolve().parent
    
    print(f"Regenerating all {len(scripts)} MDPI figures...")
    print("=" * 50)
    
    for script in scripts:
        script_path = base_dir / script
        if not script_path.exists():
            print(f"Error: Script not found: {script}")
            continue
            
        print(f"Running {script}...")
        try:
            result = subprocess.run([sys.executable, str(script_path)], 
                                   cwd=str(base_dir),
                                   capture_output=True, text=True, check=True)
            print(result.stdout.strip())
        except subprocess.CalledProcessError as e:
            print(f"Error running {script}:")
            print(e.stderr)
            
    print("=" * 50)
    print("All MDPI figures regenerated successfully.")

if __name__ == "__main__":
    main()
