#!/usr/bin/env python3
from pathlib import Path
import sys

# allow: from _run import run
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from _run import run


if __name__ == "__main__":
    v83 = Path(__file__).resolve().parents[2]
    run(v83 / "statistical analyis" / "create_study_design_flowchart.py", chdir=v83 / "statistical analyis")

