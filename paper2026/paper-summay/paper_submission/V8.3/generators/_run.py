from __future__ import annotations

from pathlib import Path
import os
import runpy
import sys


def run(script: Path, *, chdir: Path | None = None) -> None:
    """Run a python script as __main__, optionally from a working directory."""
    if chdir is not None:
        os.chdir(str(chdir))
        sys.path.insert(0, str(chdir))
    else:
        sys.path.insert(0, str(script.parent))
    runpy.run_path(str(script), run_name="__main__")
