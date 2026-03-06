#!/usr/bin/env python3
from __future__ import annotations
"""
download-cantonal-pdfs.py
-------------------------
Downloads cantonal policy web pages as PDF files using headless Chrome (Selenium).
Requires: selenium, webdriver-manager

Usage:
  source venv/bin/activate
  python scripts/download-cantonal-pdfs.py
"""

import argparse
import base64
import json
import os
import sys
import time

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

DEFAULT_CONFIG = os.path.join("data", "sources", "cantonal", "sources.config.json")
DEFAULT_OUTPUT_DIR = os.path.join("data", "documents", "cantonal", "pdf_raw")

def load_config(config_path: str) -> list[dict]:
    with open(config_path, encoding="utf-8") as f:
        cfg = json.load(f)
    return cfg.get("sources", [])

def setup_driver() -> webdriver.Chrome:
    from selenium.webdriver.common.print_page_options import PrintOptions
    chrome_options = Options()
    chrome_options.add_argument("--headless=new")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    # Request English language specifically
    chrome_options.add_argument("--lang=en-US,en;q=0.9")
    chrome_options.add_argument("--accept-lang=en-US,en")
    
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    driver.set_page_load_timeout(30)
    return driver

def save_page_as_pdf(driver: webdriver.Chrome, url: str, output_path: str):
    from selenium.webdriver.common.print_page_options import PrintOptions
    print(f"  Loading: {url}")
    try:
        driver.get(url)
    except Exception as e:
        print(f"  Got timeout or error loading {url}: {e}. Proceeding to print anyway if partial load...")
        
    time.sleep(4)
    print(f"  Generating PDF...")
    
    print_options = PrintOptions()
    print_options.background = True
    
    pdf_base64 = driver.print_page(print_options)
    
    with open(output_path, "wb") as f:
        f.write(base64.b64decode(pdf_base64))
    
    print(f"  Saved: {output_path}")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", default=DEFAULT_CONFIG)
    parser.add_argument("--output-dir", default=DEFAULT_OUTPUT_DIR)
    args = parser.parse_args()

    script_dir = os.path.dirname(os.path.abspath(__file__))
    repo_root  = os.path.dirname(script_dir)
    
    config_path = args.config if os.path.isabs(args.config) else os.path.join(repo_root, args.config)
    output_dir = args.output_dir if os.path.isabs(args.output_dir) else os.path.join(repo_root, args.output_dir)
    
    try:
        sources = load_config(config_path)
    except Exception as e:
        print(f"Failed to load config {config_path}: {e}")
        sys.exit(1)

    os.makedirs(output_dir, exist_ok=True)
    
    print("Setting up Chrome driver...")
    driver = setup_driver()
    
    success_count = 0
    error_count = 0

    try:
        for source in sources:
            source_id = source.get("source_id", "unknown")
            url = source.get("url")
            
            if not url:
                print(f"Skipping {source_id}: No URL")
                continue
                
            output_path = os.path.join(output_dir, f"{source_id}.pdf")
            
            try:
                save_page_as_pdf(driver, url, output_path)
                success_count += 1
            except Exception as e:
                print(f"  [ERROR] Failed to save {source_id}: {e}")
                error_count += 1
                
    finally:
        driver.quit()
        
    print(f"\nDone. {success_count} PDFs generated. {error_count} errors.")
    print(f"Output directory: {output_dir}")

if __name__ == "__main__":
    main()
