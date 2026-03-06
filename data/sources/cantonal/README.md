# Cantonal policy data source (side project)

**Scope:** Data source – **cantonal** policy content for CareLoop RAG.  
**Purpose:** Define data formats, document standards, and scope for the cantonal policy download task. Download/ingest scripts are implemented separately; this directory holds only format, config, and standards.

---

## What cantonal data we need

See **`CANTONAL-DATA-REQUIREMENTS.md`** for the definitive list:

- **Topics:** IV (cantonal offices, procedure, forms), supplementary benefits (EL), Hilflosenentschädigung, general cantonal social services.
- **Content types per canton:** Eligibility/procedure, required documents, office/contact/routing, forms and links.
- **Which cantons:** At least ZH, BE, GE for pilot; extend as needed.
- **Languages:** de, fr, it, en where available.

Use that doc to select and prioritize sources in `sources.config.json`.

---

## Layout

| File | Purpose |
|------|--------|
| `CANTONAL-DATA-REQUIREMENTS.md` | **What we need:** topics, content types, cantons, languages. |
| `DATA-FORMAT.md` | Data format, scope, and document standards (schemas, field definitions). |
| `sources.config.json` | **Scope object:** list of cantonal sources (input to your download process). |
| `documents.example.json` | **Output standard:** example shape of downloaded documents for chunking/load. |
| `.gitignore` | Ignore generated output (e.g. `documents.json`) if desired. |

**Output location:** Write generated document arrays under the data directory, e.g. `data/documents/cantonal/documents.json` or keep here as `data/sources/cantonal/documents.json`. See `data/README.md`.

No download or fetch scripts live here; you script the download separately and conform to the formats below.
