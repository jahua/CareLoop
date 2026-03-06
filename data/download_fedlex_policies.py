#!/usr/bin/env python3
"""
Download actual Swiss social insurance policy law texts from Fedlex.

Sources: fedlex.admin.ch — verified direct PDF-A filestore URLs (current as of 2026-03).

Usage:
  python download_fedlex_policies.py [--output-dir PATH] [--verbose]
"""

import argparse
import time
from pathlib import Path
from typing import List, NamedTuple

import requests


class PolicyDoc(NamedTuple):
    sr: str        # SR number
    name: str      # human-readable name
    category: str  # domain tag
    url_de: str    # verified direct PDF-A URL (German)
    url_fr: str = ""  # French version (optional)


# ---------------------------------------------------------------------------
# Curated list of actual Swiss social insurance LAWS — verified URLs from Fedlex
# (obtained by browsing fedlex.admin.ch and extracting PDF-A links)
# ---------------------------------------------------------------------------
POLICIES: List[PolicyDoc] = [
    # ── IV (Invalidenversicherung) ──────────────────────────────────────────
    PolicyDoc(
        sr="831.20",
        name="IVG – Bundesgesetz über die Invalidenversicherung",
        category="IV",
        url_de="https://www.fedlex.admin.ch/filestore/fedlex.data.admin.ch/eli/cc/1959/827_857_845/20240101/de/pdf-a/fedlex-data-admin-ch-eli-cc-1959-827_857_845-20240101-de-pdf-a-10.pdf",
        url_fr="https://www.fedlex.admin.ch/filestore/fedlex.data.admin.ch/eli/cc/1959/827_857_845/20240101/fr/pdf-a/fedlex-data-admin-ch-eli-cc-1959-827_857_845-20240101-fr-pdf-a-10.pdf",
    ),
    PolicyDoc(
        sr="831.201",
        name="IVV – Verordnung über die Invalidenversicherung",
        category="IV",
        url_de="https://www.fedlex.admin.ch/filestore/fedlex.data.admin.ch/eli/cc/1961/29_29_29/20250601/de/pdf-a/fedlex-data-admin-ch-eli-cc-1961-29_29_29-20250601-de-pdf-a.pdf",
    ),
    # ── AHV (Alters- und Hinterlassenenversicherung) ────────────────────────
    PolicyDoc(
        sr="831.10",
        name="AHVG – Bundesgesetz über die Alters- und Hinterlassenenversicherung",
        category="AHV",
        url_de="https://www.fedlex.admin.ch/filestore/fedlex.data.admin.ch/eli/cc/63/837_843_843/20260101/de/pdf-a/fedlex-data-admin-ch-eli-cc-63-837_843_843-20260101-de-pdf-a.pdf",
        url_fr="https://www.fedlex.admin.ch/filestore/fedlex.data.admin.ch/eli/cc/63/837_843_843/20260101/fr/pdf-a/fedlex-data-admin-ch-eli-cc-63-837_843_843-20260101-fr-pdf-a.pdf",
    ),
    # ── ATSG (Allgemeiner Teil Sozialversicherungsrecht) ────────────────────
    PolicyDoc(
        sr="830.1",
        name="ATSG – Bundesgesetz über den Allgemeinen Teil des Sozialversicherungsrechts",
        category="General",
        url_de="https://www.fedlex.admin.ch/filestore/fedlex.data.admin.ch/eli/cc/2002/510/20240101/de/pdf-a/fedlex-data-admin-ch-eli-cc-2002-510-20240101-de-pdf-a-1.pdf",
        url_fr="https://www.fedlex.admin.ch/filestore/fedlex.data.admin.ch/eli/cc/2002/510/20240101/fr/pdf-a/fedlex-data-admin-ch-eli-cc-2002-510-20240101-fr-pdf-a-1.pdf",
    ),
    # ── EL (Ergänzungsleistungen) ───────────────────────────────────────────
    PolicyDoc(
        sr="831.30",
        name="ELG – Bundesgesetz über Ergänzungsleistungen zur AHV und IV",
        category="EL",
        url_de="https://www.fedlex.admin.ch/filestore/fedlex.data.admin.ch/eli/cc/2007/804/20260101/de/pdf-a/fedlex-data-admin-ch-eli-cc-2007-804-20260101-de-pdf-a.pdf",
        url_fr="https://www.fedlex.admin.ch/filestore/fedlex.data.admin.ch/eli/cc/2007/804/20260101/fr/pdf-a/fedlex-data-admin-ch-eli-cc-2007-804-20260101-fr-pdf-a.pdf",
    ),
    PolicyDoc(
        sr="831.301",
        name="ELV – Verordnung über die Ergänzungsleistungen zur AHV und IV",
        category="EL",
        url_de="https://www.fedlex.admin.ch/filestore/fedlex.data.admin.ch/eli/cc/2007/805/20230101/de/pdf-a/fedlex-data-admin-ch-eli-cc-2007-805-20230101-de-pdf-a.pdf",
    ),
    # ── Hilflosenentschädigung / Hilfsmittel ────────────────────────────────
    PolicyDoc(
        sr="831.232.21",
        name="HVI – Verordnung über die Abgabe von Hilfsmitteln durch die IV",
        category="HE",
        url_de="https://www.fedlex.admin.ch/filestore/fedlex.data.admin.ch/eli/cc/1976/2664_2664_2664/20240101/de/pdf-a/fedlex-data-admin-ch-eli-cc-1976-2664_2664_2664-20240101-de-pdf-a.pdf",
    ),
    # ── Familienzulagen ─────────────────────────────────────────────────────
    PolicyDoc(
        sr="836.1",
        name="FamZG – Bundesgesetz über die Familienzulagen",
        category="FamZ",
        url_de="https://www.fedlex.admin.ch/filestore/fedlex.data.admin.ch/eli/cc/2008/51/20260101/de/pdf-a/fedlex-data-admin-ch-eli-cc-2008-51-20260101-de-pdf-a.pdf",
        url_fr="https://www.fedlex.admin.ch/filestore/fedlex.data.admin.ch/eli/cc/2008/51/20260101/fr/pdf-a/fedlex-data-admin-ch-eli-cc-2008-51-20260101-fr-pdf-a.pdf",
    ),
    # ── Erwerbsersatz ───────────────────────────────────────────────────────
    PolicyDoc(
        sr="834.1",
        name="EOG – Bundesgesetz über die Erwerbsersatzordnung",
        category="EO",
        url_de="https://www.fedlex.admin.ch/filestore/fedlex.data.admin.ch/eli/cc/1952/1021_1046_1050/20250128/de/pdf-a/fedlex-data-admin-ch-eli-cc-1952-1021_1046_1050-20250128-de-pdf-a-1.pdf",
    ),
]


# ---------------------------------------------------------------------------
# Downloader
# ---------------------------------------------------------------------------

def download_all(
    output_dir: Path,
    lang: str,
    timeout: int,
    delay: float,
    user_agent: str,
    verbose: bool,
) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)

    session = requests.Session()
    session.headers.update({"User-Agent": user_agent})

    total = len(POLICIES)
    downloaded = skipped = failed = 0

    for idx, doc in enumerate(POLICIES, start=1):
        url = doc.url_fr if (lang == "fr" and doc.url_fr) else doc.url_de
        if lang == "fr" and not doc.url_fr:
            print(f"[{idx}/{total}] INFO  No FR version for {doc.sr}, falling back to DE")

        # Filename: sr_number + lang + basename from URL
        sr_safe = doc.sr.replace(".", "_")
        url_basename = url.split("/")[-1]
        filename = f"policy_{sr_safe}_{url_basename}"
        dest = output_dir / filename

        if dest.exists() and dest.stat().st_size > 10_000:
            if verbose:
                print(f"[{idx}/{total}] SKIP  {filename}")
            skipped += 1
            continue

        if verbose:
            print(f"[{idx}/{total}] GET   {doc.sr} — {doc.name}")

        try:
            resp = session.get(url, timeout=timeout, stream=True)
            resp.raise_for_status()
        except requests.RequestException as exc:
            print(f"[{idx}/{total}] FAIL  {url}\n       {exc}")
            failed += 1
            continue

        content_type = resp.headers.get("content-type", "")
        if "pdf" not in content_type.lower() and "octet" not in content_type.lower():
            # Peek first bytes to check
            first_bytes = b""
            for chunk in resp.iter_content(chunk_size=16):
                first_bytes = chunk
                break
            if b"%PDF" not in first_bytes:
                print(f"[{idx}/{total}] FAIL  Not a PDF (content-type: {content_type}) — {url}")
                failed += 1
                continue
            # re-open (can't rewind stream easily — retry)
            try:
                resp = session.get(url, timeout=timeout, stream=True)
                resp.raise_for_status()
            except requests.RequestException as exc:
                print(f"[{idx}/{total}] FAIL  retry: {exc}")
                failed += 1
                continue

        dest_tmp = dest.with_suffix(".tmp")
        try:
            with dest_tmp.open("wb") as f:
                for chunk in resp.iter_content(chunk_size=65536):
                    if chunk:
                        f.write(chunk)
            size_kb = dest_tmp.stat().st_size // 1024
            if size_kb < 10:
                print(f"[{idx}/{total}] FAIL  File too small ({size_kb} KB) — probably HTML: {url}")
                dest_tmp.unlink(missing_ok=True)
                failed += 1
                continue
            dest_tmp.rename(dest)
            print(f"[{idx}/{total}] DONE  {filename} ({size_kb} KB)  [{doc.category}]")
            downloaded += 1
        except OSError as exc:
            print(f"[{idx}/{total}] IO ERR {dest} — {exc}")
            dest_tmp.unlink(missing_ok=True)
            failed += 1

        if delay > 0:
            time.sleep(delay)

    print(
        f"\nDone: {downloaded} downloaded, {skipped} already existed, "
        f"{failed} failed  →  {output_dir}"
    )


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def parse_args() -> argparse.Namespace:
    script_dir = Path(__file__).resolve().parent
    default_out = script_dir / "documents" / "cantonal" / "pdf_policy"

    p = argparse.ArgumentParser(
        description="Download Swiss social insurance policy law PDFs from Fedlex."
    )
    p.add_argument("--output-dir", type=Path, default=default_out)
    p.add_argument("--lang", choices=["de", "fr"], default="de",
                   help="Language (de or fr). Falls back to de if no FR version.")
    p.add_argument("--timeout", type=int, default=30)
    p.add_argument("--delay", type=float, default=0.5)
    p.add_argument("--user-agent", type=str,
                   default="CareLoopPolicyCrawler/1.0 (+https://github.com/jahua/CareLoop)")
    p.add_argument("--verbose", action="store_true")
    return p.parse_args()


def main() -> None:
    args = parse_args()
    # Clean out any bad HTML files from previous run
    out = args.output_dir
    if out.exists():
        for f in out.glob("*.pdf"):
            if f.stat().st_size < 10_000:
                print(f"Removing bad file: {f.name} ({f.stat().st_size} bytes)")
                f.unlink()
    download_all(
        output_dir=out,
        lang=args.lang,
        timeout=args.timeout,
        delay=args.delay,
        user_agent=args.user_agent,
        verbose=args.verbose,
    )


if __name__ == "__main__":
    main()
