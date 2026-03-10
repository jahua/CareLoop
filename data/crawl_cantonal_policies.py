#!/usr/bin/env python3
"""Crawl configured cantonal websites and export discovered pages/PDFs to CSV."""

import argparse
import csv
import json
from collections import deque
from dataclasses import dataclass
from pathlib import Path
from typing import Deque, Dict, List, Set, Tuple
from urllib.parse import urljoin, urlsplit, urlunsplit

import requests
from bs4 import BeautifulSoup


@dataclass
class Source:
    source_id: str
    url: str
    canton: str
    title: str = ""


def normalize_url(url: str, keep_query: bool = False) -> str:
    parts = urlsplit(url.strip())
    if not parts.scheme:
        return url.strip()

    path = parts.path or "/"
    query = parts.query if keep_query else ""
    normalized = urlunsplit((parts.scheme.lower(), parts.netloc.lower(), path, query, ""))
    if normalized.endswith("/") and path != "/":
        normalized = normalized.rstrip("/")
    return normalized


def is_pdf(url: str) -> bool:
    return urlsplit(url).path.lower().endswith(".pdf")


def same_host(url: str, host: str) -> bool:
    return urlsplit(url).netloc.lower() == host.lower()


def should_skip_href(href: str) -> bool:
    lowered = href.lower()
    return (
        not href
        or href.startswith("#")
        or lowered.startswith("javascript:")
        or lowered.startswith("mailto:")
        or lowered.startswith("tel:")
    )


def load_sources(config_path: Path) -> List[Source]:
    with config_path.open("r", encoding="utf-8") as f:
        raw = json.load(f)

    sources: List[Source] = []
    for entry in raw.get("sources", []):
        source_id = entry.get("source_id", "").strip()
        url = normalize_url(entry.get("url", ""))
        canton = entry.get("canton", "").strip()
        title = entry.get("title", "").strip()
        if not source_id or not url or not canton:
            continue
        sources.append(Source(source_id=source_id, url=url, canton=canton, title=title))

    return sources


def crawl_source(
    source: Source,
    max_depth: int,
    max_pages_per_source: int,
    timeout_seconds: int,
    user_agent: str,
    keep_query_params: bool,
    verbose: bool,
) -> List[Dict[str, str]]:
    session = requests.Session()
    session.headers.update({"User-Agent": user_agent})

    start_host = urlsplit(source.url).netloc.lower()
    queue: Deque[Tuple[str, int, str]] = deque([(source.url, 0, "")])
    queued: Set[str] = {source.url}
    visited: Set[str] = set()
    emitted: Set[Tuple[str, str]] = set()
    records: List[Dict[str, str]] = []

    if verbose:
        print(f"[{source.source_id}] crawl start: {source.url}")

    while queue and len(visited) < max_pages_per_source:
        url, depth, parent_url = queue.popleft()
        url = normalize_url(url, keep_query=keep_query_params)

        if depth > max_depth or url in visited:
            continue

        visited.add(url)

        try:
            response = session.get(url, timeout=timeout_seconds)
            response.raise_for_status()
        except requests.RequestException:
            if verbose:
                print(f"[{source.source_id}] request failed: {url}")
            continue

        content_type = response.headers.get("content-type", "").lower()
        if "html" not in content_type:
            continue

        soup = BeautifulSoup(response.text, "html.parser")
        title = soup.title.string.strip() if soup.title and soup.title.string else source.title

        page_key = ("page", url)
        if page_key not in emitted:
            emitted.add(page_key)
            records.append(
                {
                    "canton": source.canton,
                    "source": source.source_id,
                    "url": url,
                    "title": title,
                    "type": "page",
                    "depth": str(depth),
                    "parent_url": parent_url,
                }
            )

        for link in soup.find_all("a", href=True):
            href = link["href"].strip()
            if should_skip_href(href):
                continue

            full = normalize_url(urljoin(url, href), keep_query=keep_query_params)
            if not same_host(full, start_host):
                continue

            if is_pdf(full):
                pdf_key = ("pdf", full)
                if pdf_key in emitted:
                    continue
                emitted.add(pdf_key)
                records.append(
                    {
                        "canton": source.canton,
                        "source": source.source_id,
                        "url": full,
                        "title": link.get_text(strip=True) or "PDF",
                        "type": "pdf",
                        "depth": str(depth + 1),
                        "parent_url": url,
                    }
                )
                continue

            if full not in visited and full not in queued:
                queue.append((full, depth + 1, url))
                queued.add(full)

        if verbose and len(visited) % 20 == 0:
            print(f"[{source.source_id}] visited={len(visited)} queue={len(queue)} records={len(records)}")

    if verbose:
        print(f"[{source.source_id}] crawl done: visited={len(visited)} records={len(records)}")

    return records


def write_csv(records: List[Dict[str, str]], output_path: Path) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    columns = ["canton", "source", "url", "title", "type", "depth", "parent_url"]

    with output_path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=columns)
        writer.writeheader()
        writer.writerows(records)


def parse_args() -> argparse.Namespace:
    script_dir = Path(__file__).resolve().parent
    default_config = script_dir / "sources" / "cantonal" / "sources.config.json"
    default_output = script_dir / "documents" / "cantonal" / "swiss_social_insurance_docs.csv"

    parser = argparse.ArgumentParser(description="Crawl cantonal policy sites and collect page/PDF URLs.")
    parser.add_argument("--config", type=Path, default=default_config, help="Path to sources.config.json")
    parser.add_argument("--output", type=Path, default=default_output, help="Output CSV file path")
    parser.add_argument("--max-depth", type=int, default=2, help="Maximum link depth per source")
    parser.add_argument("--max-pages-per-source", type=int, default=200, help="Max HTML pages per source")
    parser.add_argument("--timeout-seconds", type=int, default=10, help="HTTP timeout in seconds")
    parser.add_argument(
        "--keep-query-params",
        action="store_true",
        help="Keep query parameters in normalized URLs (off by default to reduce duplicates).",
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Print progress logs while crawling.",
    )
    parser.add_argument(
        "--user-agent",
        type=str,
        default="Big5LoopPolicyCrawler/1.0 (+https://github.com/jahua/Big5Loop)",
        help="HTTP User-Agent string",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    sources = load_sources(args.config)
    if not sources:
        print(f"No valid sources found in: {args.config}")
        return

    all_records: List[Dict[str, str]] = []
    for source in sources:
        all_records.extend(
            crawl_source(
                source=source,
                max_depth=args.max_depth,
                max_pages_per_source=args.max_pages_per_source,
                timeout_seconds=args.timeout_seconds,
                user_agent=args.user_agent,
                keep_query_params=args.keep_query_params,
                verbose=args.verbose,
            )
        )

    write_csv(all_records, args.output)
    print(f"Collected {len(all_records)} records into {args.output}")


if __name__ == "__main__":
    main()
