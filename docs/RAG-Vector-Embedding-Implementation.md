# RAG Vector Embedding Implementation

> CareLoop policy retrieval pipeline — technical reference.
> Built: 6 March 2026

---

## 1. Overview

CareLoop uses Retrieval-Augmented Generation (RAG) to ground chatbot responses in Swiss social insurance policy. The pipeline translates German/French source documents to English, chunks them, generates 1024-dimensional vector embeddings via the NVIDIA API, and stores everything in PostgreSQL with pgvector for fast cosine-similarity retrieval.

### Architecture at a glance

```
Source documents (DE/FR)
        │
        ▼
  Translation layer
  ├── Cantonal: Gemini / manual  →  translated_policies.json
  └── Fedlex:   Kimi API (PDF→MD) →  translated_fedlex/*.md
        │
        ▼
  Chunking  (~300 tokens, 15 % overlap)
        │
        ▼
  Embedding  (NVIDIA nv-embedqa-e5-v5, 1024-dim)
        │
        ▼
  PostgreSQL  (pgvector, HNSW index)
        │
        ▼
  Retrieval   (cosine similarity  +  FTS fallback)
        │
        ▼
  LLM Generation  (grounding verifier → cited response)
```

---

## 2. Document corpus

### 2.1 Corpus summary

| Category | Sources | Chunks | Content size | Original languages |
|---|---|---|---|---|
| Cantonal policies | 22 | 60 | 61.3 KB | 15 German, 7 French |
| Federal laws (Fedlex) | 9 | 310 | 358.5 KB | 9 German |
| Legacy (seed data) | 2 | 3 | 1.0 KB | English |
| **Total** | **33** | **373** | **420.8 KB** | — |

### 2.2 Cantonal documents (22 sources, 3 cantons)

These are plain-text policy pages scraped from cantonal IV/SVA/OCAS websites and translated to English.

| Canton | # Docs | Topics covered |
|---|---|---|
| Zürich (ZH) | 7 | IV pension, helplessness allowance, supplementary benefits, assistance contribution, assistive devices, medical measures, contact |
| Bern (BE) | 8 | IV registration, cash benefits, disability entitlement, rehabilitation, assistance contribution, assistive devices, medical measures, contact |
| Genève (GE) | 7 | AI pension & vocational rehab, helplessness allowance, supplementary benefits, assistance contribution, assistive devices, medical measures, contact |

**Source file:** `data/documents/translated/translated_policies.json`
**Format:** JSON array; each entry contains `source_id`, `title`, `title_en`, `content_en`, `url`, and `metadata`.

### 2.3 Federal laws — Fedlex (9 sources)

Full legal texts extracted from Fedlex PDFs and translated to English Markdown.

| SR Number | Short name | Full title | Chunks |
|---|---|---|---|
| SR 830.1 | ATSG | General Part of Social Insurance Law | 28 |
| SR 831.10 | IVG | Federal Act on Disability Insurance | 73 |
| SR 831.20 | IVV | Disability Insurance Ordinance | 64 |
| SR 831.201 | IVV Annexes | Disability Insurance Ordinance Details | 71 |
| SR 831.232.21 | HVI | Assistive Devices Ordinance | 12 |
| SR 831.30 | ELG | Federal Act on Supplementary Benefits | 23 |
| SR 831.301 | ELV | Supplementary Benefits Ordinance | 4 |
| SR 834.1 | EOG | Earnings Compensation Act | 23 |
| SR 836.1 | FamZG | Federal Act on Family Allowances | 12 |

**Source directory:** `data/documents/translated_fedlex/*.md`
**Format:** Markdown files, one per law.

---

## 3. Translation pipeline

### 3.1 Cantonal documents

1. **Source:** 22 `.txt` files in `data/documents/cantonal/`
2. **Translation:** Manually translated (German → English, French → English) using LLM assistance
3. **Output:** `data/documents/translated/translated_policies.json` (128 KB)
4. **Automation script:** `scripts/translate-policies-gemini.js` (Gemini API, available for future batches)

Translation rules applied:
- Swiss legal terms preserved in parentheses: e.g., "disability insurance (Invalidenversicherung, IV)"
- URLs and reference numbers kept verbatim
- Markdown structure preserved

### 3.2 Federal laws (Fedlex)

1. **Source:** 9 PDF files from `data/documents/cantonal/pdf_policy/`
2. **Extraction + Translation:** `data/translate_fedlex_kimi.py` using Moonshot Kimi API
   - PDF → Markdown extraction via Kimi file upload
   - Markdown → English translation via Kimi chat completions
   - Chunked by headings during extraction
3. **Output:** 9 `.md` files in `data/documents/translated_fedlex/` (total ~316 KB)

---

## 4. Chunking strategy

| Parameter | Value | Rationale |
|---|---|---|
| Target chunk size | 300 tokens (~1,200 chars) | Balances retrieval precision with context window |
| Overlap ratio | 15 % (~180 chars) | Prevents information loss at chunk boundaries |
| Chars-per-token estimate | 4 | Conservative estimate for English legal text |
| Boundary alignment | Word boundary (last space before target) | Avoids splitting words mid-token |

**Algorithm:** Fixed-size sliding window with word-boundary snapping. Each document's content is whitespace-normalized, then sliced into overlapping windows. The first chunk inherits the document title; subsequent chunks append "(part N)".

**Result statistics:**

| Metric | Value |
|---|---|
| Total chunks | 373 |
| Average chunk size | 1,155 chars |
| Minimum chunk size | 248 chars |
| Maximum chunk size | 1,200 chars |
| Chunks with embeddings | 370 (99.2 %) |

---

## 5. Embedding model

| Property | Value |
|---|---|
| Provider | NVIDIA API |
| Model | `nvidia/nv-embedqa-e5-v5` |
| Dimensions | 1024 |
| API endpoint | `https://integrate.api.nvidia.com/v1/embeddings` |
| Input type | `passage` (for indexing), `query` (for search) |
| Max input tokens | 2,048 characters per chunk (truncated) |
| Batch size | 5 texts per API call |
| Rate limiting | 500 ms delay between batches |

**Why this model:**
- Matches the pre-existing `VECTOR(1024)` column in the database schema (no migration needed)
- Optimized for Q&A retrieval tasks (E5 architecture)
- Available via NVIDIA API with the project's existing API key
- Good performance on domain-specific English text

---

## 6. Database storage

### 6.1 Table schema

```sql
CREATE TABLE policy_chunks (
    id            SERIAL PRIMARY KEY,
    source_id     TEXT NOT NULL,
    chunk_id      TEXT NOT NULL,
    title         TEXT,
    content       TEXT NOT NULL,
    url           TEXT,
    metadata      JSONB DEFAULT '{}',
    embedding     VECTOR(1024),
    created_at    TIMESTAMPTZ DEFAULT now(),
    UNIQUE (source_id, chunk_id)
);
```

### 6.2 Indexes

| Index | Type | Purpose |
|---|---|---|
| `policy_chunks_pkey` | B-tree (id) | Primary key |
| `policy_chunks_source_id_chunk_id_key` | B-tree (source_id, chunk_id) | Upsert deduplication |
| `idx_policy_chunks_content_trgm` | GIN (tsvector) | Full-text search fallback |
| `idx_policy_chunks_embedding_hnsw` | HNSW (cosine) | Vector similarity search |

### 6.3 HNSW index parameters

| Parameter | Value | Description |
|---|---|---|
| `m` | 16 | Max bi-directional links per node |
| `ef_construction` | 64 | Size of dynamic candidate list during build |
| Distance metric | Cosine (`vector_cosine_ops`) | Normalized similarity; 1.0 = identical |

### 6.4 Storage sizes

| Component | Size |
|---|---|
| Table data | 720 KB |
| Indexes (all) | 3,648 KB |
| **Total relation** | **6,440 KB (~6.3 MB)** |

### 6.5 Metadata structure

Each chunk stores a JSONB `metadata` field:

```json
{
  "language": "en",
  "language_original": "de",
  "source_type": "cantonal | fedlex",
  "canton": "ZH | BE | GE | Federal",
  "jurisdiction": "Cantonal | Federal",
  "authority_tier": 1,
  "sr_number": "831.10",
  "original_source_id": "zh_iv_rente",
  "translated_at": "2026-03-06T..."
}
```

---

## 7. Retrieval mechanism

### 7.1 Architecture: API-side retrieval

Retrieval runs in the **Next.js API route** (`apps/web/src/app/api/chat/route.ts`), not inside N8N. This separates concerns: the API handles retrieval and the N8N workflow handles personality detection, generation, grounding, and formatting.

```
User query → API route
               │
               ├── 1. Intent check (policy_navigation or mixed?)
               ├── 2. Embed query  (NVIDIA API, input_type: "query")
               ├── 3. Vector search (pgvector cosine similarity, top 5)
               ├── 4. FTS fallback  (if vector results < 2 hits)
               │
               └── Forward to N8N (with evidence attached)
                     ├── Personality detection
                     ├── LLM generation (uses evidence for grounding)
                     └── Response formatting (citations from vector results)
```

**Retrieval service:** `apps/web/src/lib/retrieval.ts`

### 7.2 Vector similarity search (primary)

```sql
SELECT source_id, chunk_id, title, content, url,
       1 - (embedding <=> $1::vector) AS similarity
FROM policy_chunks
WHERE embedding IS NOT NULL
ORDER BY embedding <=> $1::vector
LIMIT 5;
```

The query text is embedded at search time using the same NVIDIA model with `input_type: "query"` (asymmetric retrieval). Results below 30% cosine similarity are filtered out.

### 7.3 Full-text search (fallback)

```sql
SELECT source_id, chunk_id, title, content, url,
       ts_rank(to_tsvector('english', content || ' ' || title),
               websearch_to_tsquery('english', $1)) AS rank
FROM policy_chunks
WHERE to_tsvector('english', content || ' ' || title)
      @@ websearch_to_tsquery('english', $1)
ORDER BY rank DESC
LIMIT 5;
```

FTS activates in two scenarios:
1. **Hybrid mode:** When vector search returns fewer than 2 results, FTS results are merged and deduplicated
2. **Pure FTS fallback:** When the NVIDIA embedding API is unavailable

### 7.4 Retrieval modes

| Mode | Trigger | Description |
|---|---|---|
| `vector` | Vector returns >= 2 results above threshold | Pure semantic similarity |
| `hybrid` | Vector returns < 2 results | Vector + FTS merged, deduplicated |
| `fts` | Embedding API unavailable | PostgreSQL full-text search only |
| `none` | No results from any method | No evidence passed to generator |

### 7.5 Test query results (live system)

**Query:** "What IV benefits are available in Zurich?"

| Rank | Similarity | Method | Source | Title |
|---|---|---|---|---|
| 1 | 52.8 % | vector | zh_iv_rente_en | IV Pension — SVA Zurich |
| 2 | 52.3 % | vector | be_iv_invaliditaet_en | Disability & Entitlement — Bern |
| 3 | 52.0 % | vector | zh_iv_hilfsmittel_en | Auxiliary means IV — SVA Zurich |
| 4 | 51.9 % | vector | zh_el_zusatzleistungen_en | Supplementary benefits — SVA Zurich |
| 5 | 51.8 % | vector | zh_iv_medizinische_massnahmen_en | Medical measures — SVA Zurich |

**Performance:** Embedding 2.8s, vector search 52ms, total 3.0s.

---

## 8. Scripts reference

### 8.1 Embed and load: `scripts/embed-and-load-policies.js`

The main ingestion script that chunks, embeds, and loads all translated documents.

```bash
# Full run (requires NVIDIA_API_KEY and running PostgreSQL)
NVIDIA_API_KEY=nvapi-... node scripts/embed-and-load-policies.js

# Preview without API calls or DB writes
node scripts/embed-and-load-policies.js --dry-run

# Load without embeddings (FTS only)
node scripts/embed-and-load-policies.js --skip-embed

# Process specific source types
node scripts/embed-and-load-policies.js --cantonal-only
node scripts/embed-and-load-policies.js --fedlex-only

# Process a single document
node scripts/embed-and-load-policies.js --single fedlex_831.10_en
```

**Runtime:** ~3.5 minutes for 370 chunks (dominated by NVIDIA API calls at 500 ms intervals).

### 8.2 Translation scripts

| Script | Purpose | API |
|---|---|---|
| `scripts/translate-policies-gemini.js` | Translate cantonal JSON docs | Google Gemini |
| `data/translate_fedlex_kimi.py` | Extract + translate Fedlex PDFs | Moonshot Kimi |

---

## 9. Infrastructure dependencies

| Component | Version / Image | Purpose |
|---|---|---|
| PostgreSQL | `pgvector/pgvector:pg16` | Storage + vector search |
| pgvector extension | Bundled with image | `VECTOR` type + HNSW index |
| Node.js | 22.x | Ingestion scripts |
| Docker Compose | — | Container orchestration |
| NVIDIA API | `nv-embedqa-e5-v5` | Embedding generation |

**Docker Compose file:** `infra/docker/docker-compose.yml`

---

## 10. Adding new documents

To add new policy documents to the corpus:

1. **Translate** the document to English and place it in:
   - Cantonal: Add to `data/documents/translated/translated_policies.json`
   - Federal: Save as `.md` in `data/documents/translated_fedlex/`

2. **Register** the source (Fedlex only): Add an entry to `FEDLEX_SR_MAP` in the embed script if it's a new SR number.

3. **Run** the embed+load script:
   ```bash
   NVIDIA_API_KEY=nvapi-... node scripts/embed-and-load-policies.js
   ```
   The script uses `ON CONFLICT ... DO UPDATE`, so re-running is safe and idempotent.

4. **Verify** in the database:
   ```sql
   SELECT source_id, count(*) AS chunks, count(embedding) AS embedded
   FROM policy_chunks
   GROUP BY source_id
   ORDER BY source_id;
   ```

---

## 11. Known limitations and future improvements

| Limitation | Impact | Planned improvement |
|---|---|---|
| Fixed-size chunking | May split mid-paragraph or mid-article | Semantic chunking by heading/article boundaries |
| Single embedding model | No fallback if NVIDIA API is down | Add local model option (e.g., `multilingual-e5-base`) |
| English-only embeddings | Requires pre-translation of all sources | Multilingual embedding model for direct DE/FR retrieval |
| No re-ranking | Top-K results may include marginally relevant chunks | Add cross-encoder re-ranker (e.g., `ms-marco-MiniLM`) |
| 3 legacy chunks without embeddings | Not reachable via vector search | Re-embed or remove legacy seed data |
| Embedding latency (~3s) | Adds latency to policy queries | Cache frequent query embeddings or use local model |
