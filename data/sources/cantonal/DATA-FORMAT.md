# Cantonal data format, scope, and document standards

Standards for the cantonal policy data source (side project). Your download process should consume the **sources config** and produce **documents** that match these formats.

---

## 1. Scope

- **In scope:** Cantonal (Swiss canton) policy and guidance content intended for RAG retrieval in Big5Loop (policy_navigation pillar). **What** cantonal data we need (topics, content types, cantons, languages) is defined in **`CANTONAL-DATA-REQUIREMENTS.md`**.
- **Content types:** Official canton pages, IV/EL/Hilflosenentschädigung procedure and contact, required documents, office/contact routing. Federal content belongs in a separate data source (e.g. `data/sources/federal/`) if needed.
- **Out of scope:** User data, non‑policy content, content from outside the defined source list. Download tooling and scheduling are out of scope for this directory (script separately).

---

## 2. Sources config (input to download)

**File:** `sources.config.json` in this directory.

**Root shape:**

```json
{
  "description": "Optional string.",
  "sources": [ { ... } ]
}
```

**Source object (each entry in `sources`):**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `source_id` | string | yes | Unique id for this source (e.g. `zh_social_services`). Used as prefix for chunk IDs. |
| `title` | string | yes | Human-readable title for the document/source. |
| `url` | string | yes | Canonical URL of the page or resource to fetch. |
| `canton` | string | yes | Two-letter canton code (e.g. `ZH`, `BE`, `GE`). ISO 3166-2 CH. |
| `notes` | string | no | Optional note (e.g. "PDF", "German only"). |

Your download process reads `sources.config.json` and fetches each `url`; it then produces a **documents** file that conforms to §3.

---

## 3. Documents (output of download, input to chunk/load)

**File:** Typically `documents.json` in this directory (or another path your pipeline chooses). Name and path are not mandated; the **structure** is.

**Root:** JSON array of document objects.

**Document object:**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `source_id` | string | yes | Same as in sources config; identifies the source. |
| `title` | string | yes | Title of the document (e.g. from config or extracted from page). |
| `url` | string | no | Canonical URL of the fetched resource. |
| `content` | string | yes | Plain text body used for chunking. No HTML; normalize whitespace as needed. |
| `metadata` | object | no | Key-value metadata for RAG/governance. |

**Recommended `metadata` fields (optional but standard):**

| Key | Type | Description |
|-----|------|-------------|
| `authority_tier` | number | 1–5; canton-level often 2. |
| `jurisdiction` | string | e.g. `"Canton"` or canton name. |
| `canton` | string | Two-letter canton code. |
| `language` | string | e.g. `de`, `fr`, `en`, `it` if known. |
| `fetched_at` | string | ISO-8601 timestamp of fetch. |

**Example document:**

```json
{
  "source_id": "zh_social_services",
  "title": "Zurich supplementary benefits",
  "url": "https://www.svazurich.ch/el",
  "content": "Full plain text of the page…",
  "metadata": { "authority_tier": 2, "jurisdiction": "Canton", "canton": "ZH", "language": "de" }
}
```

This format is compatible with the repo’s chunk-and-load script (`scripts/chunk-and-load-policy.js`), which expects an array of objects with `source_id`, `title`, `url`, `content`, and optional `metadata`.

---

## 4. Document standards

- **Encoding:** UTF-8 for all JSON and text content.
- **IDs:** `source_id` – lowercase, underscores allowed; no spaces. Stable across runs for the same source.
- **Canton codes:** Two letters, uppercase (e.g. ZH, BE, GE). Use standard Swiss canton abbreviations.
- **Content:** Plain text only in `content`; strip HTML/PDF markup before writing documents. Preserve section structure (e.g. newlines or headings) if useful for chunking.
- **Optional governance:** If you add fields like `validation_status` or `expires_at`, document them in this file and align with Spec §7.1 (e.g. `validation_status=approved` for production retrieval).
