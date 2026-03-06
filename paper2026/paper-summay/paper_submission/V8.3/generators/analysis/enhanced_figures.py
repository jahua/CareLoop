#!/usr/bin/env python3
"""
Convenience entrypoint to regenerate the enhanced analysis figures.

Currently this forwards to:
  statistical analyis/enhanced_statistical_analysis.py
"""

from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from _run import run


if __name__ == "__main__":
    v83 = Path(__file__).resolve().parents[2]
    run(v83 / "statistical analyis" / "enhanced_statistical_analysis.py", chdir=v83 / "statistical analyis")

