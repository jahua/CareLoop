#!/usr/bin/env python3
"""
Download evaluation datasets for Big5Loop simulated evaluation.
Run from Big5Loop/evaluation_data/ or: python scripts/download_datasets.py
"""
import os
import sys
import urllib.request
from pathlib import Path

EVAL_DIR = Path(__file__).resolve().parent.parent
RAW_DIR = EVAL_DIR / "raw"
os.chdir(EVAL_DIR)
RAW_DIR.mkdir(parents=True, exist_ok=True)


def download_big5_chat():
    """Download BIG5-CHAT from Hugging Face."""
    try:
        from datasets import load_dataset
    except ImportError:
        print("Install: pip install datasets")
        return False
    out = RAW_DIR / "big5_chat_dataset.csv"
    print("[BIG5-CHAT] Loading wenkai-li/big5_chat...")
    ds = load_dataset("wenkai-li/big5_chat", split="train", trust_remote_code=True)
    ds.to_csv(out, index=False)
    print(f"  Saved: {out}")
    return True


def download_personage():
    """Download PERSONAGE files from source."""
    base = "https://farm2.user.srcf.net/research/personage"
    files = ["predefinedParams.xml", "randomParams.xml", "predefinedParams.tab", "randomParams.tab"]
    for f in files:
        path = RAW_DIR / f
        if path.exists():
            print(f"[PERSONAGE] {f} already present")
            continue
        url = f"{base}/{f}"
        try:
            urllib.request.urlretrieve(url, path)
            print(f"  Saved: {f}")
        except Exception as e:
            print(f"  {f}: {e} (may need manual download from {base})")


def main():
    print("=== Big5Loop Evaluation Data Download ===\n")
    download_big5_chat()
    print()
    download_personage()
    print("\n[BFI2] Use R: install.packages('ShinyItemAnalysis'); data(BFI2); write.csv(BFI2,'bfi2_dataset.csv')")
    print("[NEO-PI-R] Manual: https://d-scholarship.pitt.edu/35840/")
    print("[BFI-2-R] Restricted: https://ieee-dataport.org/documents/bfi-2-r (IEEE subscription)")
    print("\nDone.")


if __name__ == "__main__":
    main()
