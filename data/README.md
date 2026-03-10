# Data directory

Big5Loop policy and document data: formats, configs, and generated outputs.

| Path | Purpose |
|------|--------|
| **`documents/`** | Data document format and examples. Generated document arrays (for chunk/load) go here or in subdirs (e.g. `documents/cantonal/`). |
| **`documents/example.json`** | Generic document-array example (input shape for chunk script). |
| **`sources/cantonal/`** | Cantonal data source scope: config, format, and standards. See `sources/cantonal/README.md` and `DATA-FORMAT.md`. |
| **`crawl_cantonal_policies.py`** | Optional crawler that reads `sources/cantonal/sources.config.json` and exports discovered pages/PDF links to `documents/cantonal/swiss_social_insurance_docs.csv`. |

Scripts that produce document JSON should write under `data/documents/` (or a subdirectory) so all data documents live in `data/`.
