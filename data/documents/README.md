# Data documents

This directory holds **data document** format and examples: JSON arrays of document objects used as input for chunk-and-load (`scripts/chunk-and-load-policy.js`).

- **Format:** Array of `{ source_id, title, url?, content, metadata? }`. See `data/sources/cantonal/DATA-FORMAT.md` for full schema and standards.
- **Example:** `example.json` – generic template. Copy and fill for your pipeline.
- **Cantonal:** Source config and cantonal example live under `data/sources/cantonal/`. Generated document output can be written here (e.g. `data/documents/cantonal/documents.json`) or under that sources subdirectory, per your script.

Place generated document files (e.g. after download) in this directory or in subdirs (e.g. `documents/cantonal/`) so all data documents stay under `data/`.
