# What cantonal (Kantonal) data we need

Clear definition of the cantonal data required for Big5Loop policy navigation (RAG). Use this to select sources and prioritize downloads.

---

## 1. Why cantonal data

Big5Loop answers policy questions about **IV (Invalidenversicherung)**, **Hilflosenentschädigung**, and related benefits. Federal rules apply nationwide, but **procedures, forms, and contacts are canton-specific**. Users need: “Where do I apply in my canton?” “Which office?” “Which forms?” “What are the cantonal steps?” So we need **cantonal** content in addition to federal.

---

## 2. Topics we need (by policy domain)

| Domain | What we need at cantonal level |
|--------|---------------------------------|
| **IV (Invalidenversicherung)** | Cantonal IV office contacts and addresses; cantonal procedure (how to register, where to submit); cantonal forms or links; where to get the “Anmeldung” form in the canton. |
| **Supplementary benefits (Ergänzungsleistungen / EL)** | Who is responsible in the canton (e.g. SVA Zurich for ZH); eligibility and calculation at cantonal/municipal level; application procedure and required documents; contact and office details. |
| **Hilflosenentschädigung** | Cantonal implementation and contact; how and where to apply; required documents and procedure. |
| **General social services (Sozialhilfe, etc.)** | Where to turn in the canton for social support; first-contact offices; links to cantonal info. |

Federal content (e.g. IV eligibility criteria, federal forms) belongs in a **federal** data source; this list is **cantonal** only.

---

## 3. Content types we need (per canton)

For each canton you support, we need at least:

| Content type | Description | Example |
|--------------|-------------|--------|
| **Eligibility / conditions** | Canton-specific conditions or how federal rules are applied locally (if published). | “In canton ZH you must …” |
| **Procedure / steps** | Step-by-step: how to apply, register, or request in this canton. | “1. Contact your municipal office … 2. Submit form X …” |
| **Required documents** | Checklist of documents and forms for applications in the canton. | “ID, medical report, form Anmeldung …” |
| **Office / contact / routing** | Official office name, address, phone, web, e-mail; when to go to municipality vs canton. | “SVA Zurich, …” or “Your Gemeinde …” |
| **Forms and links** | Links to cantonal forms or PDFs; where to download. | Links to canton form pages. |

Optional but useful: short FAQ (e.g. “Who pays EL in my canton?”), deadlines, appeal steps.

---

## 4. Which cantons

- **Minimum (pilot):** A small set (e.g. **ZH, BE, GE**) so we have at least one German-, one French-speaking canton and a clear “what we need” set.
- **Extended:** Add more cantons (e.g. AG, SG, VD, TI) as needed.
- **Full:** All 26 cantons if the product targets all of Switzerland.

Define the target list in `sources.config.json` and keep it in sync with this document.

---

## 5. Languages

Big5Loop supports **de, fr, it, en** (Spec §6.1). Prefer:

- **de** for German-speaking cantons (ZH, BE, AG, etc.),
- **fr** for French-speaking (GE, VD, VS, etc.),
- **it** for Ticino and Italian-speaking areas,
- **en** where officially available (or mark `language` in metadata so we know what we have).

---

## 6. Summary checklist (per canton)

When adding a canton, ensure we have documents that cover:

- [ ] IV: cantonal office/contact and procedure (and forms/links if possible).
- [ ] Supplementary benefits (EL): responsible body, procedure, documents, contact.
- [ ] Hilflosenentschädigung: where/how to apply in the canton (if applicable).
- [ ] At least one of: eligibility, procedure, documents, or contact for each of the above.

Sources can be official canton sites (e.g. svazurich.ch, ge.ch, be.ch), SVA/cantonal social insurance pages, or official guidance linked from there. Prefer authoritative, up-to-date pages; note `url` and optional `fetched_at` in metadata.
