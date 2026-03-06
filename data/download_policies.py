#!/usr/bin/env python3
"""Download actual PDF files listed in the crawler CSV to disk."""

import argparse
import csv
import hashlib
import re
import time
from pathlib import Path
from urllib.parse import unquote, urlsplit

from typing import Optional

import requests


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def safe_filename(url: str, title: str, canton: str, index: int) -> str:
    """Build a readable, filesystem-safe filename from a PDF URL."""
    path = urlsplit(url).path
    original = Path(unquote(path)).name  # e.g. "merkblatt_foo.pdf"

    # Strip non-ASCII and problematic chars, keep extension
    stem = re.sub(r"[^\w\-.]", "_", original.rsplit(".", 1)[0])[:80]
    stem = stem.strip("_")

    # Prefix with canton + sequential index so names are always unique
    filename = f"{canton.lower()}_{index:04d}_{stem}.pdf"
    return filename


def sha256_of_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


# ---------------------------------------------------------------------------
# Main download logic
# ---------------------------------------------------------------------------

def download_pdfs(
    csv_path: Path,
    output_dir: Path,
    timeout: int,
    delay: float,
    user_agent: str,
    verbose: bool,
    canton_filter: Optional[str],
) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)

    session = requests.Session()
    session.headers.update({"User-Agent": user_agent})

    # Read CSV
    with csv_path.open("r", encoding="utf-8", newline="") as f:
        rows = list(csv.DictReader(f))

    pdf_rows = [r for r in rows if r.get("type", "").strip().lower() == "pdf"]

    if canton_filter:
        cf = canton_filter.upper()
        pdf_rows = [r for r in pdf_rows if r.get("canton", "").upper() == cf]

    total = len(pdf_rows)
    print(f"Found {total} PDF entries to download (from {csv_path.name})")

    downloaded = skipped = failed = 0

    for idx, row in enumerate(pdf_rows, start=1):
        url = row["url"].strip()
        canton = row.get("canton", "XX").strip()
        title = row.get("title", "").strip()

        filename = safe_filename(url, title, canton, idx)
        dest = output_dir / filename

        if dest.exists():
            if verbose:
                print(f"[{idx}/{total}] SKIP (exists) {filename}")
            skipped += 1
            continue

        if verbose:
            print(f"[{idx}/{total}] GET  {url}")

        try:
            resp = session.get(url, timeout=timeout, stream=True)
            resp.raise_for_status()
        except requests.RequestException as exc:
            print(f"[{idx}/{total}] FAIL {url} — {exc}")
            failed += 1
            continue

        # Write to disk
        dest_tmp = dest.with_suffix(".tmp")
        try:
            with dest_tmp.open("wb") as f:
                for chunk in resp.iter_content(chunk_size=65536):
                    if chunk:
                        f.write(chunk)
            dest_tmp.rename(dest)
            size_kb = dest.stat().st_size // 1024
            if verbose:
                print(f"[{idx}/{total}] DONE {filename} ({size_kb} KB)")
            downloaded += 1
        except OSError as exc:
            print(f"[{idx}/{total}] IO ERROR {dest} — {exc}")
            dest_tmp.unlink(missing_ok=True)
            failed += 1
            continue

        if delay > 0:
            time.sleep(delay)

    print(
        f"\nFinished: {downloaded} downloaded, {skipped} skipped (already exist), "
        f"{failed} failed — files in {output_dir}"
    )


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def parse_args() -> argparse.Namespace:
    script_dir = Path(__file__).resolve().parent
    default_csv = script_dir / "documents" / "cantonal" / "swiss_social_insurance_docs.csv"
    default_out = script_dir / "documents" / "cantonal" / "pdf_raw"

    p = argparse.ArgumentParser(
        description="Download PDF policy files listed in the crawler CSV."
    )
    p.add_argument("--csv", type=Path, default=default_csv,
                   help="Input CSV produced by crawl_cantonal_policies.py")
    p.add_argument("--output-dir", type=Path, default=default_out,
                   help="Directory where PDFs will be saved")
    p.add_argument("--canton", type=str, default=None,
                   help="Only download PDFs for a specific canton (e.g. ZH, BE, GE)")
    p.add_argument("--timeout", type=int, default=30,
                   help="HTTP request timeout in seconds (default: 30)")
    p.add_argument("--delay", type=float, default=0.5,
                   help="Seconds to wait between requests (default: 0.5)")
    p.add_argument("--user-agent", type=str,
                   default="CareLoopPolicyCrawler/1.0 (+https://github.com/jahua/CareLoop)",
                   help="HTTP User-Agent string")
    p.add_argument("--verbose", action="store_true",
                   help="Print per-file progress")
    return p.parse_args()


def main() -> None:
    args = parse_args()
    download_pdfs(
        csv_path=args.csv,
        output_dir=args.output_dir,
        timeout=args.timeout,
        delay=args.delay,
        user_agent=args.user_agent,
        verbose=args.verbose,
        canton_filter=args.canton,
    )


if __name__ == "__main__":
    main()
