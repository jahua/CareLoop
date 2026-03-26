#!/usr/bin/env python3
"""
Download PANDORA-related Hugging Face datasets for Phase 5 evaluation.

Usage (from Big5Loop/evaluation_data):
  python scripts/download_pandora.py

Requires: pip install datasets  (see requirements-eval.txt)
"""
from __future__ import annotations

import os
import sys
from pathlib import Path

EVAL_DIR = Path(__file__).resolve().parent.parent
OUT_DIR = EVAL_DIR / "pandora" / "raw"
OUT_DIR.mkdir(parents=True, exist_ok=True)


def _save_split(ds, name: str) -> Path:
    """Write a HF Dataset split to CSV (portable; add pyarrow for Parquet if needed)."""
    path = OUT_DIR / f"{name}.csv"
    ds.to_csv(str(path))
    return path


def download_pandora_big5() -> bool:
    """jingjietan/pandora-big5 — primary Reddit + Big Five targets."""
    try:
        from datasets import load_dataset
    except ImportError:
        print("Install: pip install datasets pyarrow")
        return False
    print("[PANDORA-Big5] Loading jingjietan/pandora-big5 ...")
    ds = load_dataset("jingjietan/pandora-big5", trust_remote_code=True)
    saved = []
    if hasattr(ds, "keys"):
        for split in ds.keys():
            p = _save_split(ds[split], f"pandora_big5_{split}")
            saved.append(p)
            print(f"  Saved: {p}")
    else:
        p = _save_split(ds, "pandora_big5_all")
        saved.append(p)
        print(f"  Saved: {p}")
    return bool(saved)


def download_automated_personality_subset() -> bool:
    """Fatima0923/Automated-Personality-Prediction — benchmark / cross-check."""
    try:
        from datasets import load_dataset
    except ImportError:
        return False
    print("[APP] Loading Fatima0923/Automated-Personality-Prediction ...")
    try:
        ds = load_dataset("Fatima0923/Automated-Personality-Prediction", trust_remote_code=True)
    except Exception as e:
        print(f"  Skip or manual import: {e}")
        return False
    saved = []
    if hasattr(ds, "keys"):
        for split in list(ds.keys())[:4]:
            p = _save_split(ds[split], f"app_{split}")
            saved.append(p)
            print(f"  Saved: {p}")
    return bool(saved)


def main() -> None:
    os.chdir(EVAL_DIR)
    print("=== Phase 5 PANDORA downloads →", OUT_DIR, "\n")
    ok1 = download_pandora_big5()
    print()
    ok2 = download_automated_personality_subset()
    if not ok1 and not ok2:
        sys.exit(1)
    print("\nDone. Map labels to O,C,E,A,N in preprocess; see PHASE5-PANDORA.md")


if __name__ == "__main__":
    main()
