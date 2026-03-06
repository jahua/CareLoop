#!/usr/bin/env python3
"""
Translate Swiss social insurance policy PDFs from Fedlex to English using Gemini 2.0.

Because these PDFs are large (often >100 pages), this script chunks them into 
smaller pieces, sends them to the Gemini API, and concatenates the results 
into Markdown files.

Usage:
  export GEMINI_API_KEY="your-key"
  python translate_fedlex_gemini.py
"""

import os
import sys
import glob
import time
import base64
import argparse
from pathlib import Path
import json
import urllib.request
import urllib.error

# We will need PyPDF2 to chunk the PDFs.
try:
    import PyPDF2
except ImportError:
    print("Error: PyPDF2 is required. Please install it using:")
    print("pip install PyPDF2")
    sys.exit(1)


API_KEY = os.environ.get("GEMINI_API_KEY")
MODEL = os.environ.get("GEMINI_MODEL", "gemini-2.0-flash")

# Adjust these paths based on script location vs data folder
SCRIPT_DIR = Path(__file__).resolve().parent
INPUT_DIR = SCRIPT_DIR / "documents" / "cantonal" / "pdf_policy"
OUTPUT_DIR = SCRIPT_DIR / "documents" / "translated_fedlex"

SYSTEM_PROMPT = """You are a professional translator specializing in Swiss social insurance and disability policy.

TASK: Translate the provided pages of the Swiss legal document to English. 

RULES — follow these strictly:
1. Output in clean Markdown formatting (headings, lists, bold, etc., according to the visible structure).
2. Keep Swiss-specific legal/insurance terms in parentheses after the English term.
   Examples:
   - "disability insurance (Invalidenversicherung / IV)"
   - "supplementary benefits (Ergänzungsleistungen / EL)"
   - "helplessness allowance (Hilflosenentschädigung / HE)"
   - "assistance contribution (Assistenzbeitrag)"
   - "vocational rehabilitation (berufliche Eingliederung)"
   - "daily allowance (Taggeld)"
   - "pension (Rente)"
   - "degree of disability (Invaliditätsgrad)"
   For French equivalents use the same pattern:
   - "disability insurance (assurance-invalidité / AI)"
3. Do NOT translate proper nouns (e.g., SVA Zürich, OCAS, IV-Stelle), URLs, form numbers, addresses.
4. Translate accurately — do not add, remove, or summarize information. Maintain the legal tone.
5. Use clear, accessible English suitable for caregivers and patients navigating the Swiss system.
6. Return ONLY the translated Markdown text, no preamble, explanation, or conversational filler.
"""

def split_pdf(pdf_path: Path, max_pages: int = 15):
    """Splits a PDF into chunks and saves them in a temporary folder. 
    Returns list of paths to the temporary chunk PDFs."""
    reader = PyPDF2.PdfReader(str(pdf_path))
    total_pages = len(reader.pages)
    
    tmp_dir = pdf_path.parent / "tmp_chunks"
    tmp_dir.mkdir(exist_ok=True)
    
    chunk_paths = []
    
    for i in range(0, total_pages, max_pages):
        writer = PyPDF2.PdfWriter()
        end_page = min(i + max_pages, total_pages)
        
        for j in range(i, end_page):
            writer.add_page(reader.pages[j])
            
        chunk_filename = tmp_dir / f"{pdf_path.stem}_chunk_{i+1}_to_{end_page}.pdf"
        with open(chunk_filename, "wb") as out_pdf:
            writer.write(out_pdf)
            
        chunk_paths.append(str(chunk_filename))
        
    return chunk_paths


def call_gemini_with_pdf(pdf_path: str) -> str:
    """Calls the Gemini API with the given PDF chunk."""
    with open(pdf_path, "rb") as f:
        pdf_data = f.read()
    
    base64_pdf = base64.b64encode(pdf_data).decode("utf-8")

    url = f"https://generativelanguage.googleapis.com/v1beta/models/{MODEL}:generateContent?key={API_KEY}"
    
    payload = {
        "contents": [
            {
                "role": "user",
                "parts": [
                    {"text": SYSTEM_PROMPT},
                    {
                        "inline_data": {
                            "mime_type": "application/pdf",
                            "data": base64_pdf
                        }
                    }
                ]
            }
        ],
        "generationConfig": {
            "temperature": 0.1,
            "maxOutputTokens": 8192
        }
    }
    
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(url, data=data, headers={"Content-Type": "application/json"}, method="POST")
    
    try:
        with urllib.request.urlopen(req) as response:
            resp_body = response.read().decode("utf-8")
            resp_json = json.loads(resp_body)
            try:
               text = resp_json["candidates"][0]["content"]["parts"][0]["text"]
               return text.strip()
            except (KeyError, IndexError):
                print(f"Error parsing response: {resp_json}")
                return ""
    except urllib.error.HTTPError as e:
        err_msg = e.read().decode("utf-8")
        print(f"API Error ({e.code}): {err_msg}")
        raise
    except Exception as e:
         print(f"Request failed: {e}")
         raise


def main():
    parser = argparse.ArgumentParser(description="Translate Fedlex PDFs.")
    parser.add_argument("--dry-run", action="store_true", help="Chunk PDFs but don't call the API")
    parser.add_argument("--doc", type=str, help="Process only documents matching this string (e.g., '831.20')")
    parser.add_argument("--delay", type=float, default=2.0, help="Delay in seconds between API calls")
    args = parser.parse_args()

    if not args.dry_run and not API_KEY:
        print("ERROR: GEMINI_API_KEY environment variable is required.")
        print("Get a free key at: https://aistudio.google.com/apikey")
        sys.exit(1)

    if not INPUT_DIR.exists():
        print(f"Input directory not found: {INPUT_DIR}")
        sys.exit(1)
        
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    
    pdf_files = list(INPUT_DIR.glob("*.pdf"))
    if args.doc:
        pdf_files = [f for f in pdf_files if args.doc in f.name]
        
    print(f"Found {len(pdf_files)} PDF(s) to process.")
    
    for pdf_path in pdf_files:
        out_md_path = OUTPUT_DIR / f"{pdf_path.stem}.md"
        
        # Check if already fully translated (simple check based on file existence)
        if out_md_path.exists() and not args.dry_run:
            print(f"[{pdf_path.name}] Output {out_md_path.name} already exists. Skipping.")
            continue
            
        print(f"\nProcessing: {pdf_path.name}")
        try:
            chunk_paths = split_pdf(pdf_path, max_pages=15)
        except Exception as e:
            print(f"  Error splitting PDF: {e}")
            continue
            
        print(f"  Split into {len(chunk_paths)} chunks.")
        
        if args.dry_run:
            continue
            
        translated_chunks = []
        for idx, chunk_path in enumerate(chunk_paths, 1):
            print(f"  Translating chunk {idx}/{len(chunk_paths)}...")
            
            # Simple retry loop for 429 Resource Exhausted / rate limits
            retries = 3
            while retries > 0:
                try:
                    text = call_gemini_with_pdf(chunk_path)
                    translated_chunks.append(text)
                    print(f"    ✓ Done ({len(text)} chars)")
                    break
                except Exception as e:
                    retries -= 1
                    if "429" in str(e):
                        print("    Rate limit hit. Waiting 10s...")
                        time.sleep(10)
                    elif retries > 0:
                        print(f"    Error: {e}. Retrying in 5s...")
                        time.sleep(5)
                    else:
                        print(f"    Failed after retries.")
                        translated_chunks.append(f"\n> [!ERROR] Failed to translate chunk '{Path(chunk_path).name}'\n")
            
            time.sleep(args.delay)
            
        # Combine and write to file
        with open(out_md_path, "w", encoding="utf-8") as f:
            f.write(f"# Translation of {pdf_path.name}\n\n")
            f.write("\n\n---\n\n".join(translated_chunks))
            
        print(f"  Saved translated document to: {out_md_path.name}")
        
    print("\nAll done!")


if __name__ == "__main__":
    main()
