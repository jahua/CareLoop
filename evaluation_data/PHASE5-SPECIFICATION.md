# Phase 5 — PANDORA Evaluation: File Layout, Data Transforms, Workflow, Testing, Versioning

**Document version:** 1.0.2  
**Aligned with:** `ROADMAP.md` v1.6.0 (Phase 5)  
**Last updated:** 2026-03-26  

This specification is the **single source of truth** for where Phase 5 artifacts live, how datasets are organized and transformed, how the N8N evaluation workflow is named and versioned, and how tests are layered.

---

## 1. Purpose

Phase 5 benchmarks Big5Loop **OCEAN detection** (and optionally full turns) against **PANDORA**-family data: Reddit text with Big Five labels, using Hugging Face datasets and the dedicated **PANDORA evaluation** N8N export (v4).

---

## 2. Versioning policy

| Layer | What to version | How |
|--------|-----------------|-----|
| **This spec** | `PHASE5-SPECIFICATION.md` | Header `Document version` (semver: major = breaking layout/contract, minor = new fields/scripts, patch = clarifications). |
| **Roadmap** | Phase scope | `ROADMAP.md` product version (e.g. 1.6.0) — update when Phase 5 DoD or scope changes. |
| **Hugging Face data** | Reproducible eval | Record **`revision`** (commit SHA) or dataset snapshot **date** in `pandora/raw/manifest.json` (see §4). Every thesis table should cite that pin. |
| **N8N workflow export** | Workflow behavior | **Filename + webhook path** use a single integer generation: **`v4`** = current PANDORA eval fork from parallel v3. Next breaking change → **`big5loop-pandora-eval-v5.json`** + path `big5loop-pandora-eval-v5`. |
| **Preprocess / eval scripts** | Code behavior | Track in git commits; optional `evaluation_data/pandora/processed/run_meta.json` with script git SHA and timestamp. |

**Naming rule:** `big5loop-pandora-eval-v{N}.json` and webhook `big5loop-pandora-eval-v{N}` stay **in lockstep** (same N).

---

## 3. Directory layout (Phase 5)

All paths are relative to the Big5Loop repo root unless noted.

```
evaluation_data/
├── PHASE5-SPECIFICATION.md     # This document (canonical)
├── PHASE5-PANDORA.md           # Short overview + quick links
├── DATASOURCE-DESCRIPTION.md   # §7 PANDORA + citations
├── README.md                   # Dataset index (includes Phase 5 row)
├── scripts/
│   ├── download_pandora.py     # HF → pandora/raw/*.csv
│   ├── preprocess_pandora.py   # raw/pandora_big5_test.csv → processed eval artifacts
│   ├── run_pandora_eval.py     # batch POST to /api/chat (sample/full)
│   └── pandora_metrics.py      # per-trait Pearson/Spearman/MAE + macro averages
└── pandora/
    ├── raw/                    # Gitignored — large CSVs from HF
    │   ├── pandora_big5_<split>.csv
    │   ├── app_<split>.csv     # Optional: Automated-Personality-Prediction
    │   └── manifest.json       # Recommended: revisions, dates (§4)
    └── processed/              # Smaller artifacts; results committed selectively
        ├── .gitkeep
        ├── pandora_eval.jsonl          # Model input: text + ground_truth_ocean + sample_id
        ├── pandora_eval_results.jsonl    # Detector outputs + optional errors
        └── metrics.json                # Aggregated Pearson/Spearman/MAE per trait
```

```
workflows/n8n/
├── big5loop-phase1-2-parallel-v3.json   # Lineage parent (production-style parallel pipeline)
└── big5loop-pandora-eval-v4.json       # Phase 5 fork: dedicated webhook + PANDORA ingest flags
```

**Do not** store multi-gigabyte raw dumps inside `packages/` or `apps/` — keep them under `evaluation_data/pandora/raw/` (ignored) or an external `DATA_ROOT`.

---

## 4. Dataset organization

### 4.1 Primary: `jingjietan/pandora-big5`

| Item | Convention |
|------|------------|
| Role | Primary benchmark: Reddit-aligned text + Big Five targets. |
| Download | `python scripts/download_pandora.py` → `pandora/raw/pandora_big5_<split>.csv` |
| Schema | Follow the dataset card on Hugging Face; column names may differ from `O,C,E,A,N` — **do not** assume keys until inspected. |

### 4.2 Secondary: `Fatima0923/Automated-Personality-Prediction`

| Item | Convention |
|------|------------|
| Role | Optional cross-check / personality-prediction benchmark. |
| Download | Same script (best effort); `pandora/raw/app_<split>.csv` |

### 4.3 Manifest (`pandora/raw/manifest.json`)

After any download, write (manually or extend `download_pandora.py`) a small manifest for reproducibility:

```json
{
  "created_at": "2026-03-26T12:00:00Z",
  "datasets": {
    "jingjietan/pandora-big5": {
      "revision": "<hf-git-commit-sha-or-tag>",
      "files": ["pandora_big5_train.csv"]
    }
  }
}
```

---

## 5. Data transformation pipeline

Transforms are **offline** (Python) before N8N/API calls. The N8N workflow does **not** replace preprocessing; it consumes **already normalized** payloads.

### 5.1 Stages

| Stage | Input | Output | Responsibility |
|-------|--------|--------|----------------|
| **D1 — Download** | Hugging Face Hub | `pandora/raw/*.csv` | `download_pandora.py` |
| **D2 — Inspect** | Raw CSV | Column mapping doc in code or README | Human / one-time notebook |
| **D3 — Preprocess** | Raw CSV | `processed/pandora_eval_test.jsonl` | `preprocess_pandora.py` |
| **D4 — Evaluate** | JSONL + N8N or `/api/chat` | `pandora_eval_results_*.jsonl`, `metrics_*.json` | `run_pandora_eval.py` + `pandora_metrics.py` |

### 5.2 Canonical JSONL record (`processed/pandora_eval_test.jsonl`)

One JSON object per line:

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `sample_id` | string | yes | Stable ID (HF row id or hash). |
| `input` | string | yes | User/Reddit text passed as `message` to the workflow. |
| `ground_truth_ocean` | object | yes | Keys **`O`,`C`,`E`,`A`,`N`**, floats in **[-1, 1]** after normalization (§5.3). |
| `meta` | object | no | Subreddit, demographics, original columns (for analysis only). |

### 5.3 Normalizing labels to [-1, 1]

Big5Loop’s detector emits **approximately** [-1, 1] per trait. Dataset scales differ (e.g. 1–5, z-scores). For each source:

1. Document the **source scale** in `DATASOURCE-DESCRIPTION.md` once known.
2. Apply a deterministic map, e.g. z-score using published norms, or linear map from `[min,max] → [-1,1]`.
3. Store the **formula** in the preprocess script or a one-line comment in `manifest.json`.

**Rule:** Never mix scales across rows without documenting the transform.

### 5.4 Reported metrics (outputs)

After **D4 — Evaluate**, write at least:

| Artifact | Content |
|----------|---------|
| `processed/pandora_eval_results.jsonl` | Per-row: `sample_id`, detector OCEAN, `ground_truth_ocean`, optional latency/error. |
| `processed/metrics.json` | Per-trait **Pearson** and **Spearman** correlation, **MAE** (and counts *n*); overall summary. |

Align computation with PERSONAGE/BIG5-CHAT evaluation scripts where possible so thesis tables are comparable across benchmarks.

---

## 6. N8N workflow — names and contracts

### 6.1 Current release (v4)

| Property | Value |
|----------|--------|
| **Export file** | `workflows/n8n/big5loop-pandora-eval-v4.json` |
| **Workflow display name (inside JSON)** | `Big5Loop Phase 5 PANDORA Evaluation v4` |
| **Webhook HTTP method** | `POST` |
| **Webhook path** | `big5loop-pandora-eval-v4` |
| **Full URL (local)** | `http://localhost:5678/webhook/big5loop-pandora-eval-v4` |
| **Lineage** | Fork of `big5loop-phase1-2-parallel-v3.json` with PANDORA ingest fields |

### 6.2 Ingest flags (Code node: “Enhanced Ingest”)

Set on every request processed by this workflow:

- `pandora_evaluation: true`
- Optional: `ground_truth_ocean`, `pandora_sample_id` (passed through for logging/metrics downstream).

### 6.3 Request body (minimum)

```json
{
  "session_id": "<uuid>",
  "turn_index": 1,
  "message": "<text from JSONL text field>",
  "evaluation_mode": true,
  "ground_truth_ocean": { "O": 0.0, "C": 0.0, "E": 0.0, "A": 0.0, "N": 0.0 },
  "pandora_sample_id": "<sample_id>"
}
```

### 6.4 Bumping workflow version (v5, v6, …)

1. Duplicate the previous export JSON.
2. Increment **both** filename and webhook path: `…-v5.json`, path `big5loop-pandora-eval-v5`.
3. Update **workflow `name`** field inside JSON.
4. Register the change in `ROADMAP.md` changelog and in this document’s version table (add a row below).

| Export | Webhook path | Status |
|--------|----------------|--------|
| `big5loop-pandora-eval-v4.json` | `big5loop-pandora-eval-v4` | Current Phase 5 |
| `big5loop-pandora-eval-v5.json` | `big5loop-pandora-eval-v5` | Reserved for next breaking change |

---

## 7. Testing strategy

| Level | Goal | How |
|-------|------|-----|
| **T0 — Script sanity** | Download/preprocess code runs | `python -m py_compile scripts/download_pandora.py`; run download on a machine with HF access. |
| **T1 — Webhook smoke** | N8N accepts payload and returns 200 | `curl -X POST http://localhost:5678/webhook/big5loop-pandora-eval-v4 -H "Content-Type: application/json" -d '{"message":"test","evaluation_mode":true}'` |
| **T2 — Golden mini-batch** | 10–50 rows from `pandora_eval.jsonl` | Batch script posts each row; assert JSON shape and non-empty detector output. |
| **T3 — Full eval** | Metrics match thesis tables | Full JSONL + `metrics.json`; compare to prior run when changing preprocess version. |

**Regression:** When upgrading workflow v4 → v5, re-run **T2** on the same `pandora_eval.jsonl` slice and compare correlation deltas (document in changelog).

---

## 8. Cross-references

- `docs/phase5/README.md` — Phase 5 index under `docs/` (GitHub-friendly; links to this spec)  
- `ROADMAP.md` §8 — Phase 5 goals and DoD  
- `DATASOURCE-DESCRIPTION.md` §7 — PANDORA provenance and bibtex  
- `workflows/n8n/README.md` — Import steps for v4  
- `Technical-Specification-RAG-Policy-Navigation.md` — OCEAN contracts (system-wide)  

---

## 9. Specification changelog

| Spec version | Date | Changes |
|--------------|------|---------|
| 1.0.2 | 2026-03-26 | Cross-referenced `docs/phase5/README.md` (tracked docs index). |
| 1.0.1 | 2026-03-26 | Added §5.4 reported metrics (`metrics.json` / results JSONL). |
| 1.0.0 | 2026-03-26 | Initial: layout, transforms, workflow naming, testing, versioning. |
