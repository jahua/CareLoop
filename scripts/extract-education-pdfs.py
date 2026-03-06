#!/usr/bin/env python3
"""
Extract education PDF documents to markdown for embedding.

Usage:
    pip install pymupdf4llm
    python3 scripts/extract-education-pdfs.py

Input:  data/documents/home_care_education/*.pdf
Output: data/documents/home_care_education/extracted/*.md
"""

import os
import sys

try:
    import pymupdf4llm
except ImportError:
    print("ERROR: pymupdf4llm not installed.")
    print("Run:  pip install pymupdf4llm")
    sys.exit(1)

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(SCRIPT_DIR)
INPUT_DIR = os.path.join(PROJECT_ROOT, "data", "documents", "home_care_education")
OUTPUT_DIR = os.path.join(INPUT_DIR, "extracted")

# Map PDF filenames to clean source IDs
PDF_MAP = {
    "1_Caregiver_Training_Manual_-_Basic_Care_of_People_with_Disabilities_in_Institution___at_Home_compressed.pdf":
        "edu_caregiver_training_manual",
    "AARP-PrepareToCare-Guide.pdf":
        "edu_aarp_prepare_to_care",
    "Caregiving-for-Seniors-A-Practical-Guide-2nd-Edition_CWA-Complete-Version.pdf":
        "edu_caregiving_seniors_guide",
    "Family_Caregiver_Guide.pdf":
        "edu_family_caregiver_guide",
}

def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    pdf_files = [f for f in os.listdir(INPUT_DIR) if f.endswith(".pdf")]
    if not pdf_files:
        print(f"No PDF files found in {INPUT_DIR}")
        sys.exit(1)

    print(f"Found {len(pdf_files)} PDF files in {INPUT_DIR}\n")

    for pdf_file in sorted(pdf_files):
        source_id = PDF_MAP.get(pdf_file)
        if not source_id:
            stem = os.path.splitext(pdf_file)[0]
            source_id = "edu_" + stem.lower().replace(" ", "_").replace("-", "_")[:50]

        input_path = os.path.join(INPUT_DIR, pdf_file)
        output_path = os.path.join(OUTPUT_DIR, f"{source_id}.md")

        print(f"Processing: {pdf_file}")
        print(f"  → {source_id}.md")

        try:
            text = pymupdf4llm.to_markdown(input_path)
            with open(output_path, "w", encoding="utf-8") as f:
                f.write(text)

            word_count = len(text.split())
            char_count = len(text)
            print(f"  ✓ {word_count:,} words, {char_count:,} chars\n")

        except Exception as e:
            print(f"  ✗ Error: {e}\n")
            continue

    print(f"Done! Extracted files in: {OUTPUT_DIR}")
    print(f"\nNext step:")
    print(f"  NVIDIA_API_KEY=<key> node scripts/embed-education-docs.js")

if __name__ == "__main__":
    main()
