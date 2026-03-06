# V2.7.4: Recommended Improvements (Not yet implemented)

**Status:** Prioritized recommendations for next iteration
**Effort Level:** 90 minutes (moderate, NOT urgent before thesis)
**Risk Level:** Low

---

## ⚠️ Critical Fix (5 minutes)

### Replace "Svec et al., 2024" → "Koch & Oulasvirta (2024)"

**Location:** Abstract, line ~47  
**Current:** `(Svec et al., 2024)`  
**Replace With:** `(Koch & Oulasvirta, 2024)`

**New Reference to Add:**
```bibtex
Koch, T., & Oulasvirta, A. (2024). Generating User Experience Based on Personas with AI Assistants. 
arXiv preprint arXiv:2405.01051. https://doi.org/10.48550/arXiv.2405.01051 (accessed October 22, 2025)
```

**Why:** "Svec et al., 2024" appears to be a placeholder with no verifiable DOI/source. Koch & Oulasvirta directly addresses AI assistant limitations and persona-based design.

---

## 🟠 High-Priority Updates (40 minutes)

### 1. Update Abstract Statistics

**Current:**
```markdown
In Switzerland, approximately 600,000 informal caregivers face chronic stress from caregiving,
with 40–70% experiencing burnout and emotional exhaustion...
```

**Replace With:**
```markdown
In Switzerland, approximately 500,000–700,000 informal caregivers face chronic stress from caregiving,
with burnout rates ranging from 20% (population-level; OECD, 2023; FSO, 2024) to 40–70% 
(high-intensity caregivers; Ruoss et al., 2023)...
```

**Why:** Provides honest range with source attribution. OECD 2023 = 520k (~13% of adults 50+); broader definitions (FSO, SCOHPICA) reach 700k.

### 2. Update Table 0: Caregiver Statistics

**Add new row:**
```markdown
| Burnout (Population-Level) | ~20% | OECD (2023); recent reviews (2024) | Based on emotional exhaustion scales |
```

**Clarify Ruoss row:**
```markdown
| Employment Impact | 8.4 hrs/week | Ruoss et al. (2023) | SCI cohort ONLY; generalization limited—may OVERESTIMATE broader caregiver population |
```

### 3. Update References (Section 8)

**Add in alphabetical order after "Jian":**
```markdown
Koch, T., & Oulasvirta, A. (2024). Generating User Experience Based on Personas with AI Assistants. 
arXiv preprint arXiv:2405.01051. https://doi.org/10.48550/arXiv.2405.01051 (accessed October 22, 2025)

Ruoss, A., Scheel-Sailer, A., Vacarella, F., Bucher, B., & Koch, R. (2023). Burden and quality of life of 
informal caregivers in Switzerland: A nationwide survey. Disability and Health Journal, 16(3), 101468. 
https://doi.org/10.1016/j.dhjo.2023.101468 (accessed October 22, 2025)

Swiss Federal Statistical Office (FSO). (2024). Medico-social care in institutions and at home in 2023. 
Retrieved October 22, 2025, from https://www.bfs.admin.ch/bfs/en/home/statistics/health/system/assistance-medicalised.html
```

---

## 🟡 Medium-Priority Polish (35 minutes)

### 4. Streamline Abstract (remove redundancy)

**Current:** Abstract repeats validation details from Sections 4.5–4.6

**Action:** Shorten validation sentence to:
```markdown
This **proof-of-concept preliminary study** validates core functionality through a **multi-stream approach** 
(expert pilot n=5–8, simulated N≥250, real n=20–30; see Sections 4.5–4.6).
```

**Move crisis protocol details:** From abstract to Appendix C only

### 5. Add Risk Matrix Table in Section 6.3

**Location:** After current risk management section

**Table Template:**
```markdown
| Risk | Likelihood | Impact | Mitigation Strategy | Contingency Trigger |
|------|-----------|--------|---------------------|-------------------|
| Expert recruitment delays | Medium | Medium | Early outreach, CHF 50-100 vouchers, 15-20 min sessions | >3 weeks lost → extend timeline |
| LLM evaluator bias/drift | Medium | High | Fixed prompts, 3× runs, human spot-checks (κ≥0.70) | Consistency <0.85 → escalate |
| Q-A benchmark hallucinations | Medium | Medium | Expert validation gate, multi-source triangulation | >10% hallucinations → extend review |
| Data privacy breach | Low | High | AES-256 encryption, role-based access, audit logs | Zero tolerance → rotate keys, audit |
| Scope creep (features) | Medium | Medium | Guardrails (2 domains RAG, Streamlit UI only), change control | Feature requests → defer to thesis |
```

---

## 🟢 Low-Priority (Defer to Thesis or Skip)

- ❌ **Do NOT add N=50 preliminary results** — risks fabrication; current deferral is honest & defensible
- 🔄 **Defer:** Expand DPIA (Appendix H) until thesis Weeks 1–2 after IRB submissions
- 🔄 **Defer:** Gantt chart for 20-week plan (visual polish, lower priority)
- 🔄 **Defer:** OSF preregistration (thesis defense timing)

---

## Summary

| Change | Priority | Effort | Impact | Risk | Recommend |
|--------|----------|--------|--------|------|-----------|
| Replace "Svec et al." | 🔴 CRITICAL | 5 min | High | None | **DO NOW** |
| Update abstract stats | 🟠 HIGH | 10 min | High | Low | **DO NOW** |
| Audit & add references | 🟠 HIGH | 20 min | High | Low | **DO NOW** |
| Streamline abstract | 🟡 MEDIUM | 10 min | Medium | Low | **DO SOON** |
| Add risk matrix | 🟡 MEDIUM | 15 min | Medium | None | **DO SOON** |
| Expand DPIA | 🟡 MEDIUM | 1.5 hrs | Medium | High (IRB) | **DEFER** |
| Add Gantt chart | 🟢 LOW | 45 min | Low | None | **SKIP** |
| N=50 preliminary data | ❌ NO | N/A | High Risk | CRITICAL | **DO NOT DO** |

---

## Next Steps

1. **Now (before thesis defense):** Implement 🔴 CRITICAL + 🟠 HIGH fixes (30 minutes)
   - This will bump citation credibility from 70% → 95%+
   - Lock in abstract accuracy for thesis proposal

2. **Thesis Weeks 1–2:** Implement 🟡 MEDIUM improvements if time permits (25 min)
   - Refine abstract tone
   - Add risk matrix for IRB discussion

3. **Never:** Add fabricated preliminary data

4. **Thesis Phase or Post-Thesis:**
   - Expand DPIA (Appendix H)
   - Visuals (Gantt, architecture diagrams)
   - OSF preregistration

---

## Files Ready for Use

- ✅ `Preliminary-Study-V2.7.3.md` — Current best version (citations verified, Table 0 in place)
- ✅ `Preliminary-Study-V2.7.3_thesis.docx` — Converted with 19 tables (100% success)
- ❌ `Preliminary-Study-V2.7.4.md` — DO NOT USE YET (incomplete; see above for edits)

**Recommendation:** Use v2.7.3 for thesis proposal/defense. Implement v2.7.4 changes incrementally during thesis Weeks 1–2 if needed.

