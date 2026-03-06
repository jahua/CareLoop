#!/usr/bin/env python3
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from _run import run


if __name__ == "__main__":
    v83 = Path(__file__).resolve().parents[2]
    run(v83 / "consolidate_figures.py", chdir=v83)

