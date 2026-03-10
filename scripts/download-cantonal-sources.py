#!/usr/bin/env python3
from __future__ import annotations
"""
download-cantonal-sources.py
----------------------------
Reads data/sources/cantonal/sources.config.json, fetches each URL,
strips HTML to plain text, and writes a documents.json array to
data/documents/cantonal/documents.json (or --output <path>).

The output is compatible with:
  npm run chunk:policy -- data/documents/cantonal/documents.json

Usage (from the Big5Loop repo root):
  python scripts/download-cantonal-sources.py
  python scripts/download-cantonal-sources.py --config data/sources/cantonal/sources.config.json
  python scripts/download-cantonal-sources.py --output data/documents/cantonal/documents.json
  python scripts/download-cantonal-sources.py --dry-run

Requires: Python 3.7+, no third-party packages.
"""

import argparse
import json
import os
import re
import sys
import time
from datetime import datetime, timezone
from html.parser import HTMLParser
from urllib import request, error
from urllib.parse import urljoin, urlparse

# ---------------------------------------------------------------------------
# Config / defaults
# ---------------------------------------------------------------------------

DEFAULT_CONFIG = os.path.join("data", "sources", "cantonal", "sources.config.json")
DEFAULT_OUTPUT = os.path.join("data", "documents", "cantonal", "documents.json")

# Canton code → language (ISO 639-1)
CANTON_LANG = {
    "ZH": "de", "BE": "de", "LU": "de", "UR": "de", "SZ": "de",
    "OW": "de", "NW": "de", "GL": "de", "ZG": "de", "SO": "de",
    "BS": "de", "BL": "de", "SH": "de", "AR": "de", "AI": "de",
    "SG": "de", "GR": "de", "AG": "de", "TG": "de", "VS": "de",
    "GE": "fr", "VD": "fr", "NE": "fr", "JU": "fr", "FR": "fr",
    "TI": "it",
}

REQUEST_TIMEOUT = 15      # seconds per request
DELAY_BETWEEN = 1.0       # polite delay (seconds) between fetches


# ---------------------------------------------------------------------------
# HTML → plain text
# ---------------------------------------------------------------------------

# Tags whose content we skip entirely
SKIP_TAGS = {"script", "style", "noscript", "head", "nav", "footer",
             "header", "aside", "form", "button", "iframe", "svg", "figure"}

# Tags that act as block separators → emit a newline
BLOCK_TAGS = {"p", "div", "section", "article", "li", "tr", "td", "th",
              "h1", "h2", "h3", "h4", "h5", "h6", "br", "dt", "dd"}


class _TextExtractor(HTMLParser):
    """Minimal HTML → plain text extractor using stdlib only."""

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self._skip_depth = 0
        self._parts: list[str] = []

    def handle_starttag(self, tag, attrs):
        tag = tag.lower()
        if tag in SKIP_TAGS:
            self._skip_depth += 1
        elif tag in BLOCK_TAGS and not self._skip_depth:
            self._parts.append("\n")

    def handle_endtag(self, tag):
        tag = tag.lower()
        if tag in SKIP_TAGS:
            self._skip_depth = max(0, self._skip_depth - 1)
        elif tag in BLOCK_TAGS and not self._skip_depth:
            self._parts.append("\n")

    def handle_data(self, data):
        if not self._skip_depth:
            self._parts.append(data)

    def get_text(self) -> str:
        raw = "".join(self._parts)
        # Collapse runs of whitespace / blank lines
        raw = re.sub(r"[ \t]+", " ", raw)
        raw = re.sub(r"\n{3,}", "\n\n", raw)
        return raw.strip()


def html_to_text(html: str) -> str:
    parser = _TextExtractor()
    parser.feed(html)
    return parser.get_text()


# ---------------------------------------------------------------------------
# HTTP fetch
# ---------------------------------------------------------------------------

HEADERS = {
    "User-Agent": (
        "Big5Loop-DataBot/1.0 "
        "(thesis research crawler; +https://github.com/big5loop)"
    ),
    "Accept": "text/html,application/xhtml+xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "de,fr,it,en;q=0.5",
}


def fetch_url(url: str, timeout: int = REQUEST_TIMEOUT) -> "tuple[str, str, str]":
    """
    Returns (text_content, raw_html, final_url).
    Raises urllib.error.URLError / ValueError on failure.
    """
    req = request.Request(url, headers=HEADERS)
    with request.urlopen(req, timeout=timeout) as resp:
        charset = "utf-8"
        content_type = resp.headers.get_content_charset()
        if content_type:
            charset = content_type
        raw_bytes = resp.read()
        final_url = resp.url
    html = raw_bytes.decode(charset, errors="replace")
    text = html_to_text(html)
    return text, html, final_url


# ---------------------------------------------------------------------------
# Main logic
# ---------------------------------------------------------------------------

def load_config(config_path: str) -> list[dict]:
    with open(config_path, encoding="utf-8") as f:
        cfg = json.load(f)
    sources = cfg.get("sources", [])
    if not isinstance(sources, list) or not sources:
        raise ValueError("sources.config.json must have a non-empty 'sources' array.")
    return sources


def source_to_document(source: dict, dry_run: bool, raw_dir: str) -> "dict | None":
    """Fetch a source URL and return a document dict, or None on error."""
    source_id = source.get("source_id", "").strip()
    title     = source.get("title", source_id).strip()
    url       = source.get("url", "").strip()
    canton    = source.get("canton", "").upper().strip()
    notes     = source.get("notes", "")

    if not url:
        print(f"  [SKIP] {source_id}: no URL defined.", file=sys.stderr)
        return None

    print(f"  Fetching [{canton}] {source_id} → {url}")

    if dry_run:
        content = f"[DRY RUN] Content would be fetched from {url}"
        final_url = url
    else:
        try:
            content, raw_html, final_url = fetch_url(url)
            
            # Save raw HTML
            raw_path = os.path.join(raw_dir, f"{source_id}.html")
            with open(raw_path, "w", encoding="utf-8") as f:
                f.write(raw_html)
            print(f"  [SAVED RAW] {raw_path}")
                
        except Exception as exc:
            print(f"  [ERROR] {source_id}: {exc}", file=sys.stderr)
            return None

    if not content:
        print(f"  [WARN] {source_id}: fetched empty content.", file=sys.stderr)

    language = CANTON_LANG.get(canton, "de")  # default to German

    metadata = {
        "authority_tier": 2,       # canton level
        "jurisdiction": "Canton",
        "canton": canton,
        "language": language,
        "fetched_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
    }
    if notes:
        metadata["notes"] = notes

    doc = {
        "source_id": source_id,
        "title": title,
        "url": final_url,
        "content": content,
        "metadata": metadata,
    }
    return doc


def main():
    parser = argparse.ArgumentParser(
        description="Fetch cantonal policy sources and write documents.json for RAG."
    )
    parser.add_argument(
        "--config",
        default=DEFAULT_CONFIG,
        help=f"Path to sources.config.json (default: {DEFAULT_CONFIG})",
    )
    parser.add_argument(
        "--output",
        default=DEFAULT_OUTPUT,
        help=f"Output path for documents.json (default: {DEFAULT_OUTPUT})",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Skip actual HTTP fetches; write placeholder content.",
    )
    parser.add_argument(
        "--delay",
        type=float,
        default=DELAY_BETWEEN,
        help=f"Seconds to wait between requests (default: {DELAY_BETWEEN})",
    )
    parser.add_argument(
        "--source-id",
        metavar="ID",
        help="Only download the source with this source_id (for targeted refresh).",
    )
    args = parser.parse_args()

    # --- Resolve paths relative to repo root (one level up from scripts/) ---
    script_dir = os.path.dirname(os.path.abspath(__file__))
    repo_root  = os.path.dirname(script_dir)

    config_path = (
        args.config if os.path.isabs(args.config)
        else os.path.join(repo_root, args.config)
    )
    output_path = (
        args.output if os.path.isabs(args.output)
        else os.path.join(repo_root, args.output)
    )

    # --- Load config ---
    print(f"Loading config: {config_path}")
    try:
        sources = load_config(config_path)
    except (FileNotFoundError, ValueError, json.JSONDecodeError) as e:
        print(f"[ERROR] Cannot load config: {e}", file=sys.stderr)
        sys.exit(1)

    # Filter by --source-id if given
    if args.source_id:
        sources = [s for s in sources if s.get("source_id") == args.source_id]
        if not sources:
            print(f"[ERROR] No source with source_id='{args.source_id}' found.", file=sys.stderr)
            sys.exit(1)

    print(f"Processing {len(sources)} source(s)…\n")

    # --- Merge with existing output (so we don't overwrite already-fetched docs) ---
    existing_docs: dict[str, dict] = {}
    if os.path.exists(output_path):
        try:
            with open(output_path, encoding="utf-8") as f:
                for doc in json.load(f):
                    existing_docs[doc["source_id"]] = doc
            print(f"Found {len(existing_docs)} existing document(s) at {output_path}. "
                  "Will update fetched sources, keep others.\n")
        except Exception:
            pass  # If anything goes wrong, start fresh

    # --- Download ---
    documents = dict(existing_docs)  # start from existing
    success, skipped, errors = 0, 0, 0

    # Create raw directory
    raw_dir = os.path.join(os.path.dirname(output_path), "raw")
    os.makedirs(raw_dir, exist_ok=True)

    for i, source in enumerate(sources):
        doc = source_to_document(source, dry_run=args.dry_run, raw_dir=raw_dir)
        if doc is None:
            errors += 1
        else:
            documents[doc["source_id"]] = doc
            success += 1

        # Polite delay between requests (skip after last one)
        if not args.dry_run and i < len(sources) - 1:
            time.sleep(args.delay)

    # --- Write output ---
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    output_list = list(documents.values())
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(output_list, f, ensure_ascii=False, indent=2)
        f.write("\n")

    # --- Summary ---
    print(f"\n{'='*60}")
    print(f"Done. {success} fetched, {errors} error(s).")
    print(f"Output: {output_path}  ({len(output_list)} total document(s))")
    print(f"\nNext step — chunk and load into policy_chunks:")
    print(f"  npm run chunk:policy -- data/documents/cantonal/documents.json")
    print('='*60)

    sys.exit(0 if errors == 0 else 1)


if __name__ == "__main__":
    main()
