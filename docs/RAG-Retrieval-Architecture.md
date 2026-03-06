# RAG Retrieval Architecture: API-Side Vector Search

> CareLoop retrieval pipeline — design decision and implementation reference.
> Implemented: 6 March 2026

---

## 1. Design Decision: Why Retrieval Moved Out of N8N

### Problem

The original CareLoop pipeline ran the entire RAG flow inside N8N, including policy retrieval. This created several issues:

1. **No vector search capability.** N8N's Postgres node runs plain SQL. To use vector similarity search, the workflow would need a Code node to call an external embedding API, capture the 1024-dimensional vector, then pass it into a second Postgres query. N8N Code nodes have runtime limitations (e.g., `fetch` may not be available depending on configuration), making this fragile.

2. **Poor retrieval quality.** The N8N query relied on PostgreSQL full-text search (FTS) with a broad `ILIKE '%IV%'` fallback, which matched any chunk containing the string "IV" regardless of relevance. This returned only 3 legacy seed-data rows for most queries.

3. **Hard to test and iterate.** N8N workflows are stored as JSON. Testing retrieval changes required importing new workflow versions, restarting N8N, and verifying through end-to-end calls. There was no way to unit-test retrieval logic.

4. **Tight coupling.** Retrieval, personality detection, generation, and verification were all in a single workflow. A retrieval change could break unrelated nodes.

### Decision

Move policy retrieval from N8N into the **Next.js API route** (`apps/web/src/app/api/chat/route.ts`). The API route already handled intent classification fallback, mode normalization, and auditing — adding retrieval aligns with the existing responsibility pattern.

N8N continues to handle what it does well: personality detection (Zurich model), LLM generation, grounding verification, and response formatting — the orchestration logic that benefits from visual workflow editing.

### Trade-offs

| Factor | API-side retrieval | N8N retrieval |
|---|---|---|
| Vector search | Full support (NVIDIA API + pgvector) | Requires fragile Code node workaround |
| Testability | Standard TypeScript, unit testable | JSON workflow, end-to-end only |
| Latency | ~3s added before N8N call | ~0s (simple FTS) |
| Debugging | `console.log`, breakpoints, stack traces | N8N execution log (limited) |
| Separation of concerns | Clean: retrieval in API, orchestration in N8N | Monolithic: everything in one workflow |
| Deployment | Rebuild web container | Re-import workflow JSON |

---

## 2. Architecture Overview

### Request flow

```
┌────────────┐
│  Frontend   │
│  (Next.js)  │
└─────┬──────┘
      │ POST /api/chat
      ▼
┌────────────────────────────────────────────┐
│  API Route (apps/web/src/app/api/chat)     │
│                                            │
│  1. Parse request, classify intent         │
│  2. If policy/mixed intent:                │
│     ├── Embed query (NVIDIA API)           │
│     ├── Vector search (pgvector)           │
│     └── FTS fallback (if needed)           │
│  3. Forward to N8N with evidence attached  │
│  4. Post-process N8N response:             │
│     └── Overlay vector citations           │
└─────┬──────────────────────────────────────┘
      │ POST /webhook/careloop-turn
      ▼
┌────────────────────────────────────────────┐
│  N8N Workflow                              │
│                                            │
│  1. Ingest + sanitize input                │
│  2. Load personality state (Postgres)      │
│  3. Zurich model personality detection     │
│  4. Personality regulation (directives)    │
│  5. (Legacy FTS query — results ignored    │
│      when prefetched_evidence present)     │
│  6. LLM generation (NVIDIA Gemma)          │
│  7. Grounding verifier                     │
│  8. Verification & refinement              │
│  9. Format response + save to DB           │
└────────────────────────────────────────────┘
```

### Data flow for retrieval

```
API route                           N8N workflow
─────────                           ────────────

userMessage
    │
    ├──► NVIDIA embed API
    │    input_type: "query"
    │    model: nv-embedqa-e5-v5
    │         │
    │         ▼
    │    1024-dim vector
    │         │
    │         ▼
    ├──► PostgreSQL: SELECT ... ORDER BY embedding <=> vector
    │         │
    │         ▼
    │    PolicyEvidence[] (top 5, sim > 0.30)
    │         │
    │    (if < 2 results)───► PostgreSQL FTS fallback
    │         │                      │
    │         ◄──────────────────────┘
    │         │
    ▼         ▼
n8nPayload = {
  ...body,                          ──► Ingest ──► Detection
  prefetched_evidence: [...],            ──► Regulation
  retrieval_meta: {                      ──► Merge Retrieval
    method, timing...                         (uses prefetched_evidence
  }                                            if available)
}                                        ──► Generation
                                         ──► Grounding
N8N response                             ──► Format
    │
    ▼
API post-processing:
  overlay citations from
  vector results onto
  policy_navigation.citations
    │
    ▼
Final response to frontend
```

---

## 3. Implementation Details

### 3.1 Retrieval service

**File:** `apps/web/src/lib/retrieval.ts`

The retrieval service exports a single function:

```typescript
export async function retrievePolicyEvidence(
  userMessage: string
): Promise<RetrievalResult>
```

**Configuration (environment variables):**

| Variable | Default | Description |
|---|---|---|
| `NVIDIA_API_KEY` | (required) | API key for embedding |
| `NVIDIA_EMBED_MODEL` | `nvidia/nv-embedqa-e5-v5` | Embedding model |
| `DATABASE_URL` | (required) | PostgreSQL connection string |

**Constants:**

| Constant | Value | Purpose |
|---|---|---|
| `VECTOR_TOP_K` | 5 | Max vector search results |
| `FTS_TOP_K` | 5 | Max FTS fallback results |
| `SIMILARITY_THRESHOLD` | 0.30 | Min cosine similarity to include |

**Retrieval flow:**

```
retrievePolicyEvidence(userMessage)
    │
    ├── NVIDIA_API_KEY available?
    │   ├── YES: embedQuery(userMessage) → 1024-dim vector
    │   │        vectorSearch(vector, top 5)
    │   │        ├── >= 2 results above threshold → return (method: "vector")
    │   │        └── < 2 results → ftsSearch() → merge + dedup → return (method: "hybrid")
    │   │
    │   └── NO or embed fails: ftsSearch(userMessage, top 5) → return (method: "fts")
    │
    └── No DATABASE_URL → return empty (method: "none")
```

### 3.2 Asymmetric embedding

The NVIDIA `nv-embedqa-e5-v5` model uses **asymmetric retrieval**: documents are embedded with `input_type: "passage"` during ingestion, and queries are embedded with `input_type: "query"` at search time. This optimizes for the natural mismatch between short questions and long document passages.

```typescript
// At ingestion time (embed-and-load-policies.js)
{ input: texts, model: "nvidia/nv-embedqa-e5-v5", input_type: "passage" }

// At search time (retrieval.ts)
{ input: [query], model: "nvidia/nv-embedqa-e5-v5", input_type: "query" }
```

### 3.3 Vector search SQL

```sql
SELECT source_id, chunk_id, title, content, url,
       1 - (embedding <=> $1::vector) AS similarity
FROM policy_chunks
WHERE embedding IS NOT NULL
ORDER BY embedding <=> $1::vector
LIMIT $2
```

- `<=>` is the pgvector cosine distance operator
- `1 - distance` converts to similarity (1.0 = identical, 0.0 = orthogonal)
- The HNSW index (`idx_policy_chunks_embedding_hnsw`) accelerates the search

### 3.4 FTS fallback SQL

```sql
SELECT source_id, chunk_id, title, content, url,
       ts_rank(to_tsvector('english', content || ' ' || title),
               websearch_to_tsquery('english', $1)) AS rank
FROM policy_chunks
WHERE to_tsvector('english', content || ' ' || title)
      @@ websearch_to_tsquery('english', $1)
ORDER BY rank DESC
LIMIT $2
```

FTS uses PostgreSQL's built-in English stemmer. It handles exact keyword queries well (e.g., "Art. 42 IVG") where vector search may not match the specific article number.

### 3.5 Hybrid deduplication

When both vector and FTS results are combined (hybrid mode), duplicates are removed by `source_id::chunk_id` key, with vector results taking priority (they appear first in the merged array).

### 3.6 API route integration

**Intent gating:** Retrieval only runs for `policy_navigation` and `mixed` intents. The intent is determined by keyword scoring in `inferCoachingModeFallback()` before the N8N call.

**Payload forwarding:** Evidence is attached to the N8N payload as `prefetched_evidence` and `retrieval_meta`. The N8N workflow's Merge Retrieval node checks for these fields and uses them when present, falling back to its own FTS query otherwise.

**Response overlay:** After N8N returns, the API route replaces `policy_navigation.citations` with the vector search results. This ensures the frontend always sees the best available evidence, regardless of which N8N workflow version is active.

```typescript
if (retrieval && retrieval.evidence.length > 0) {
  const pn = (data.policy_navigation ?? {}) as Record<string, unknown>;
  pn.citations = retrieval.evidence.map((e) => ({
    source_id: e.source_id,
    title: e.title,
    url: e.url,
    similarity: e.similarity,
    retrieval_method: e.retrieval_method,
  }));
  data.policy_navigation = pn;
}
```

---

## 4. Response Format

### Citation object (in `policy_navigation.citations`)

```json
{
  "source_id": "zh_iv_rente_en",
  "title": "IV Pension — SVA Zürich",
  "url": "https://www.svazurich.ch/iv-rente",
  "similarity": 0.528,
  "retrieval_method": "vector"
}
```

### Retrieval timing (in `retrieval_timing`)

```json
{
  "method": "vector",
  "query_embedding_ms": 2817,
  "search_ms": 52,
  "total_ms": 2953,
  "evidence_count": 5
}
```

### Pipeline status fields

```json
{
  "pipeline_status": {
    "retrieval": "ok",
    "retrieval_method": "vector"
  }
}
```

---

## 5. Retrieval Modes

| Mode | Condition | Evidence sources |
|---|---|---|
| `vector` | NVIDIA API available, >= 2 results above 30% similarity | pgvector cosine search only |
| `hybrid` | NVIDIA API available, < 2 vector results | Vector + FTS merged, deduplicated |
| `fts` | NVIDIA API unavailable or embed fails | PostgreSQL full-text search only |
| `none` | No DATABASE_URL, or no results from any method | No evidence; N8N generates without grounding |

---

## 6. Performance

Measured on live system (6 March 2026):

| Stage | Duration | Notes |
|---|---|---|
| Query embedding | ~2,800 ms | NVIDIA API call (network-bound) |
| Vector search (pgvector) | ~50 ms | HNSW index, 370 chunks |
| DB connection | ~100 ms | New connection per request |
| **Total retrieval** | **~3,000 ms** | Added before N8N pipeline |
| N8N pipeline | ~3,500 ms | Detection + generation + verification |
| **End-to-end** | **~8,500 ms** | User message to response |

### Optimization opportunities

| Optimization | Expected improvement | Complexity |
|---|---|---|
| Connection pooling (pg Pool) | -100 ms per request | Low |
| Embedding cache (LRU by query hash) | -2,800 ms for repeat queries | Medium |
| Local embedding model | -2,500 ms (eliminates API call) | High |
| Batch embedding for multi-turn | Amortize over conversation | Medium |

---

## 7. Error Handling and Resilience

The retrieval service is designed to never block the main pipeline:

```
Retrieval fails → catch(err) → continue without evidence → N8N generates ungrounded response
```

**Failure scenarios:**

| Failure | Fallback behavior |
|---|---|
| NVIDIA API down | FTS fallback (method: "fts") |
| NVIDIA API timeout | FTS fallback |
| PostgreSQL down | Empty evidence (method: "none"); N8N still runs |
| Invalid embedding response | FTS fallback |
| All methods fail | N8N generates response without policy grounding |

The API route wraps the entire retrieval call in `try/catch`:

```typescript
try {
  retrieval = await retrievePolicyEvidence(userMessage);
} catch (err) {
  console.error("[chat] Retrieval error (continuing without evidence):", err);
}
```

---

## 8. Files Changed

| File | Change |
|---|---|
| `apps/web/src/lib/retrieval.ts` | **New.** Retrieval service module |
| `apps/web/src/app/api/chat/route.ts` | Added retrieval call before N8N, citation overlay after |
| `infra/docker/docker-compose.yml` | Added `NVIDIA_API_KEY` and `NVIDIA_EMBED_MODEL` to web container |
| `workflows/n8n/careloop-phase1-2-postgres-mvp.json` | Merge Retrieval node updated to accept `prefetched_evidence`; Ingest node passes through retrieval fields |

---

## 9. Testing

### Manual test

```bash
curl -s -X POST http://localhost:3003/api/chat \
  -H "Content-Type: application/json" \
  -d '{
    "session_id": "test-001",
    "turn_index": 1,
    "message": "What IV benefits are available in Zurich?"
  }' | python3 -m json.tool
```

**Expected:** `policy_navigation.citations` contains vector search results with `similarity` scores and `retrieval_method: "vector"`.

### Verified results

Query: "What IV benefits are available in Zurich?"

| # | Similarity | Source | Title |
|---|---|---|---|
| 1 | 52.8% | zh_iv_rente_en | IV Pension — SVA Zurich |
| 2 | 52.3% | be_iv_invaliditaet_en | Disability & Entitlement — Bern |
| 3 | 52.0% | zh_iv_hilfsmittel_en | Auxiliary means IV — SVA Zurich |
| 4 | 51.9% | zh_el_zusatzleistungen_en | Supplementary benefits — SVA Zurich |
| 5 | 51.8% | zh_iv_medizinische_massnahmen_en | Medical measures — SVA Zurich |

vs. previous FTS results (3 legacy seed chunks, no similarity scores, no Zurich-specific content).

---

## 10. Relationship to Other Documents

- **[RAG-Vector-Embedding-Implementation.md](./RAG-Vector-Embedding-Implementation.md)** — Covers the document corpus, chunking, embedding model, database schema, and ingestion pipeline. This document covers the runtime retrieval architecture.
- **[ROUTING-AND-INTENT-DESIGN.md](./ROUTING-AND-INTENT-DESIGN.md)** — Defines the four intent categories (`policy_navigation`, `mixed`, `practical_education`, `emotional_support`) that determine whether retrieval runs.
