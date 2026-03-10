# Scraping and Chunking Open Resources for Policy Chunks

How to get content from **open resources** (official sites, PDFs, open data) and load it into `policy_chunks` for RAG. The repo has no built-in scraper; you fetch content externally, then use the chunking script below to produce DB-ready chunks.

---

## 1. Chunking rules (from Spec §7.1)

- **Size:** 200–400 tokens per chunk (or ~800–1600 characters as a rough proxy).
- **Overlap:** 15–20% overlap between consecutive chunks to keep context.
- **Context:** Preserve section headers in chunks so legal/procedural context is clear.
- **Schema:** Each chunk needs `source_id`, `chunk_id`, `title`, `content`, `url`, and optional `metadata` (e.g. `authority_tier`, `jurisdiction`, `validation_status`).

---

## 2. Ways to get source content (open resources)

| Approach | Use when | Tools / notes |
|----------|----------|----------------|
| **Manual copy** | Few pages; official PDFs or web pages | Paste into a JSON/CSV or markdown; run chunk script. |
| **HTTP fetch** | Public HTML pages, APIs | `curl`, `node-fetch`, or a small Node script; parse HTML (e.g. `cheerio`) to extract text. |
| **PDF** | Official PDFs (leaflets, guides) | `pdf-parse` (Node) or `pdftotext`; extract text then chunk. |
| **Open data / APIs** | Cantonal or federal open data | Fetch JSON/CSV, convert to text per record, then chunk. |
| **Crawler** | Many pages from one site | Respect `robots.txt` and rate limits; use Puppeteer/Playwright or a crawler; export text per URL. |

Always respect terms of use and copyright; prefer official or licensed sources for policy content.

---

## 3. Script: chunk and load from a JSON of documents

Use the script **`scripts/chunk-and-load-policy.js`** (see below). It:

1. Reads a **JSON file** of documents: each has `source_id`, `title`, `url`, `content` (full text), and optional `metadata`.
2. **Chunks** each document (target ~300 tokens, ~15% overlap; preserves paragraph boundaries where possible).
3. **Inserts** into `policy_chunks` (creates table if missing). Uses `source_id` + chunk index as `chunk_id`.

**Input JSON shape** (e.g. `data/documents/example.json` or `data/documents/cantonal/documents.json`):

```json
[
  {
    "source_id": "iv_guideline_2025",
    "title": "IV Eligibility Overview",
    "url": "https://www.ahv-iv.ch/en/...",
    "content": "Full text of the page or PDF here. You can paste scraped or manually copied content. It will be split into chunks of about 200-400 tokens with overlap.",
    "metadata": { "authority_tier": 1, "jurisdiction": "Federal", "canton": "Federal" }
  }
]
```

**Run:**

```bash
cd Big5Loop
export DATABASE_URL="postgresql://big5loop:PASSWORD@localhost:5432/big5loop"
npm run chunk:policy -- data/documents/cantonal/documents.json
```

Or use `data/documents/example.json` as a template; copy to e.g. `data/documents/my-documents.json` and fill in your content. All data documents live under `data/documents/` (see `data/README.md`).

You can prepare the document JSON by:

- Scraping: fetch HTML/PDF → extract text → save one object per page/document.
- Manual: copy text from open resources (e.g. admin.ch, ahv-iv.ch) into `content`, set `source_id`, `title`, `url`.

---

## 4. Workflow summary

1. **Obtain** text from open resources (scrape, PDF, or manual).
2. **Normalize** to one “document” per source (e.g. one row per page or PDF).
3. **Save** as JSON array under `data/documents/` (e.g. `data/documents/cantonal/documents.json`) with `source_id`, `title`, `url`, `content`, `metadata`.
4. **Run** `npm run chunk:policy -- data/documents/cantonal/documents.json` to chunk and insert into `policy_chunks`.
5. **Optional:** Regenerate embeddings later if you use vector search (current retrieval uses full-text search; embeddings can be added in a separate step).

---

## 5. Embeddings (optional)

`policy_chunks` has an `embedding` column (vector). The current N8N retrieval uses **full-text search** only. If you add vector search later:

- Run an embedding model over each chunk’s `content` (e.g. via your chosen embedding API or local model).
- Update `policy_chunks.embedding` for each row.  
Phase 3 background jobs (P2-9) can later handle “re-embedding” when the corpus is refreshed.
