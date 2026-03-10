# Translation Inventory — Big5Loop Policy Documents

Status of all policy documents that need English translation for RAG retrieval.

---

## Summary

| Language | Canton | Documents | Status |
|----------|--------|-----------|--------|
| **German (de)** | ZH | 7 | Needs translation |
| **German (de)** | BE | 7 | Needs translation |
| **French (fr)** | GE | 7 | Needs translation |
| **Total** | | **21** | |

---

## German documents — Zurich (ZH)

| # | source_id | Title | Topic |
|---|-----------|-------|-------|
| 1 | `zh_iv_rente` | IV-Rente (SVA Zürich) | IV pension, disability degree, registration |
| 2 | `zh_iv_hilflosenentschaedigung` | Hilflosenentschädigung IV | Helplessness allowance, eligibility, forms |
| 3 | `zh_el_zusatzleistungen` | Ergänzungsleistungen / Zusatzleistungen | Supplementary benefits (EL) |
| 4 | `zh_sva_kontakt` | SVA Zürich Kontakt & Adressen | Contact, address, office hours |
| 5 | `zh_iv_assistenzbeitrag` | Assistenzbeitrag IV | Assistance contribution, home care |
| 6 | `zh_iv_hilfsmittel` | Hilfsmittel IV | Assistive devices, aids |
| 7 | `zh_iv_medizinische_massnahmen` | Medizinische Massnahmen | Medical measures, minors |

## German documents — Bern (BE)

| # | source_id | Title | Topic |
|---|-----------|-------|-------|
| 8 | `be_iv_anmeldung` | IV Anmeldung & Verfahren | Registration, procedure, appeal |
| 9 | `be_iv_geldleistungen` | Geld- & Sachleistungen | Pension, HE, EL, assistance contribution |
| 10 | `be_iv_kontakt` | IV-Stelle Kontakt & Adressen | Contact, address, office hours |
| 11 | `be_iv_invaliditaet` | Invalidität & Anspruch | Disability, eligibility, disability degree |
| 12 | `be_iv_eingliederung` | Früherfassung & Eingliederung | Early detection, vocational rehab |
| 13 | `be_iv_assistenzbeitrag` | Assistenzbeitrag | Assistance contribution |
| 14 | `be_iv_hilfsmittel` | Hilfsmittel | Assistive devices |
| 15 | `be_iv_medizinische_massnahmen` | Medizinische Massnahmen | Medical measures, minors |

## French documents — Geneva (GE)

| # | source_id | Title | Topic |
|---|-----------|-------|-------|
| 16 | `ge_ai_rente_readaptation` | Rente AI & Réadaptation professionnelle | AI pension, vocational rehab |
| 17 | `ge_ai_allocation_impotent` | Allocation pour impotent AI | Helplessness allowance |
| 18 | `ge_pc_el` | Prestations complémentaires AVS/AI | Supplementary benefits (PC/EL) |
| 19 | `ge_ocas_kontakt` | Contact OCAS & SPC | Contact, address, forms |
| 20 | `ge_ai_contribution_assistance` | Contribution d'assistance AI | Assistance contribution |
| 21 | `ge_ai_moyens_auxiliaires` | Moyens auxiliaires AI | Assistive devices |
| 22 | `ge_ai_mesures_medicales` | Mesures médicales (Mineurs) | Medical measures, minors |

---

## Translation rules

1. **Keep Swiss-specific terms** in parentheses: "disability insurance (Invalidenversicherung / IV)", "supplementary benefits (Ergänzungsleistungen / EL)"
2. **Do NOT translate** proper nouns: SVA Zürich, OCAS, IV-Stelle Kanton Bern
3. **Do NOT translate** URLs, form numbers, addresses, phone numbers
4. **Preserve** markdown structure (headings, lists, links)
5. **Preserve** all metadata headers (source, canton, language, date)
6. **Add** `language_original` and `language_translated` to metadata

---

## File locations

| What | Path |
|------|------|
| Source documents (parsed) | `data/documents/cantonal/parsed_cantonal_policies.json` |
| Individual text files | `data/documents/cantonal/*.txt` |
| Translation output | `data/documents/translated/` |
| Translation script | `scripts/translate-policies-gemini.js` |
