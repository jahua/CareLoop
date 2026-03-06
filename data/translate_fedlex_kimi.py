#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Translate Swiss social insurance policy PDFs from Fedlex to English using Moonshot Kimi API.

This script leverages Kimi's native file extraction API to convert PDFs to high-quality
Markdown, and then uses Kimi's Chat Completions to translate the Markdown into English
in chunks, thereby preserving legal vocabulary and formatting.

Usage:
  export KIMI_API_KEY="your-moonshot-api-key"
  python translate_fedlex_kimi.py
"""

import os
import sys
import time
import argparse
from pathlib import Path
import json

try:
    import requests
except ImportError:
    print("Error: 'requests' library is required. Install via: pip install requests")
    sys.exit(1)


API_KEY = os.environ.get("KIMI_API_KEY")
MODEL = os.environ.get("KIMI_MODEL", "moonshot-v1-32k")

SCRIPT_DIR = Path(__file__).resolve().parent
INPUT_DIR = SCRIPT_DIR / "documents" / "cantonal" / "pdf_policy"
OUTPUT_DIR = SCRIPT_DIR / "documents" / "translated_fedlex"

SYSTEM_PROMPT = """You are a professional translator specializing in Swiss social insurance and disability policy.

TASK: Translate the provided markdown text from Swiss legal documents to English.

RULES — follow these strictly:
1. Preserve all markdown formatting (headings, lists, bold, etc.).
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
4. Translate accurately — do not add, remove, or summarize information. Maintain the legal/administrative tone.
5. Use clear, accessible English.
6. Return ONLY the translated Markdown text, no preamble, explanation, or conversational filler.
"""

def extract_pdf_with_kimi(pdf_path: Path) -> str:
    """Uploads the PDF to Kimi, extracts it as Markdown, and returns the Markdown string."""
    print("    Uploading to Kimi File API for extraction...")
    headers = {"Authorization": f"Bearer {API_KEY}"}
    
    with open(pdf_path, "rb") as f:
        files = {"file": (pdf_path.name, f, "application/pdf")}
        data = {"purpose": "file-extract"}
        resp = requests.post("https://api.moonshot.cn/v1/files", headers=headers, files=files, data=data)
        
    resp.raise_for_status()
    file_id = resp.json()["id"]
    
    print(f"    File uploaded (ID: {file_id}). Fetching extracted content...")
    time.sleep(2) # brief wait for processing
    
    content_resp = requests.get(f"https://api.moonshot.cn/v1/files/{file_id}/content", headers=headers)
    content_resp.raise_for_status()
    
    # The API returns a JSON with "content" field
    return content_resp.json()["content"]

def chunk_markdown(text: str, max_chars: int = 12000):
    """Splits markdown texts into manageable chunks without breaking words/lines where possible."""
    chunks = []
    lines = text.splitlines(keepends=True)
    current_chunk = ""
    
    for line in lines:
        if len(current_chunk) + len(line) > max_chars:
            if current_chunk:
                chunks.append(current_chunk.strip())
            current_chunk = line
        else:
            current_chunk += line
            
    if current_chunk:
        chunks.append(current_chunk.strip())
        
    return chunks

def call_kimi_chat(text_chunk: str) -> str:
    """Calls Moonshot's Chat Completion API to translate a text chunk."""
    url = "https://api.moonshot.cn/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": MODEL,
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": text_chunk}
        ],
        "temperature": 0.1,
    }
    
    resp = requests.post(url, headers=headers, json=payload)
    if resp.status_code != 200:
        raise Exception(f"Kimi API Error: {resp.status_code} - {resp.text}")
        
    resp_json = resp.json()
    return resp_json["choices"][0]["message"]["content"].strip()


def main():
    parser = argparse.ArgumentParser(description="Translate Fedlex PDFs using Kimi.")
    parser.add_argument("--dry-run", action="store_true", help="Chunk files but don't call translations")
    parser.add_argument("--doc", type=str, help="Process only documents matching this string")
    parser.add_argument("--delay", type=float, default=2.0, help="Delay in seconds between API calls")
    args = parser.parse_args()

    if not args.dry_run and not API_KEY:
        print("ERROR: KIMI_API_KEY environment variable is required.")
        print("Set it via: export KIMI_API_KEY='your-key'")
        sys.exit(1)

    if not INPUT_DIR.exists():
        print(f"Input directory not found: {INPUT_DIR}")
        sys.exit(1)
        
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    
    pdf_files = list(INPUT_DIR.glob("*.pdf"))
    if args.doc:
        pdf_files = [f for f in pdf_files if args.doc in f.name]
        
    print(f"Found {len(pdf_files)} PDF(s) to process via Kimi ({MODEL}).\n")
    
    for pdf_path in pdf_files:
        out_md_path = OUTPUT_DIR / f"{pdf_path.stem}.md"
        
        if out_md_path.exists() and not args.dry_run:
            print(f"[{pdf_path.name}] Output {out_md_path.name} already exists. Skipping.")
            continue
            
        print(f"Processing: {pdf_path.name}")
        
        if args.dry_run:
            print("  (Dry-run) would extract text and chunk here.")
            continue
            
        # 1. Extract PDF to Markdown using Kimi
        try:
            markdown_content = extract_pdf_with_kimi(pdf_path)
        except Exception as e:
            print(f"  Error extracting PDF text: {e}")
            continue
            
        # 2. Chunk Markdown
        chunks = chunk_markdown(markdown_content, max_chars=12000)
        print(f"  Extracted {len(markdown_content)} characters. Split into {len(chunks)} chunks.")
        
        # 3. Translate Chunks
        translated_chunks = []
        for idx, chunk in enumerate(chunks, 1):
            print(f"  Translating chunk {idx}/{len(chunks)}...")
            
            retries = 3
            while retries > 0:
                try:
                    translated_text = call_kimi_chat(chunk)
                    translated_chunks.append(translated_text)
                    print(f"    ✓ Done ({len(translated_text)} chars)")
                    break
                except Exception as e:
                    retries -= 1
                    error_str = str(e)
                    if "429" in error_str or "rate limit" in error_str.lower():
                        print("    Rate limit hit. Waiting 10s...")
                        time.sleep(10)
                    elif retries > 0:
                        print(f"    Error: {e}. Retrying in 5s...")
                        time.sleep(5)
                    else:
                        print(f"    Failed after retries.")
                        translated_chunks.append(f"\n> [!ERROR] Failed to translate chunk {idx}\n")
                        
            time.sleep(args.delay)
            
        # 4. Save to Disk
        with open(out_md_path, "w", encoding="utf-8") as f:
            f.write(f"# Translation of {pdf_path.name}\n\n")
            f.write("\n\n---\n\n".join(translated_chunks))
            
        print(f"  Saved translated document to: {out_md_path.name}\n")
        
    print("All done!")

if __name__ == "__main__":
    main()
