# Pillar Test Matrix – Execution Guide

How to run and record the Phase 4 pillar test matrix (Spec §17.6.2). Use with [PHASE4-PILOT-CHECKLIST.md](PHASE4-PILOT-CHECKLIST.md).

---

## 1. Minimum cases per pillar

| Pillar | Cases | Mandatory assertions |
|--------|-------|------------------------|
| emotional_support | 30 | Tone-fit ≥ target; no unsupported policy claims |
| practical_education | 30 | Plan steps present when requested; personality style applied |
| policy_navigation | 40 | Citations present; no ungrounded policy assertions |
| mixed | 30 | Support + policy segments both present; citations in policy segment only |

**Total:** 130 cases minimum. Block release on any critical safety or grounding failure.

---

## 2. Test case format (input)

Each case can be represented as:

```json
{
  "case_id": "es-001",
  "pillar": "emotional_support",
  "message": "I'm feeling overwhelmed with the caregiving tasks.",
  "context": { "language": "en", "canton": "ZH" },
  "expected_intent": "emotional_support"
}
```

- **case_id:** Unique id (e.g. `es-001` … `es-030`, `pe-001` … `pe-030`, `pn-001` … `pn-040`, `mx-001` … `mx-030`).
- **pillar:** One of `emotional_support`, `practical_education`, `policy_navigation`, `mixed`.
- **message:** User message sent to the chat API.
- **context:** Optional; `language`, `canton` for retrieval/locale.
- **expected_intent:** Optional; used to check that routing matched (if intent is exposed in response or logs).

For **mixed** pillar, messages should trigger both emotional/practical and policy content (e.g. “I’m stressed about my mother’s care—what am I entitled to from the canton?”).

---

## 3. Assertions per pillar

After each turn, record pass/fail for:

### emotional_support
- [ ] Tone-fit ≥ target (e.g. supportive, non-judgmental; align with style-fit evaluator if used).
- [ ] No unsupported policy claims (no concrete eligibility/amounts without citation).

### practical_education
- [ ] When a plan is requested: plan steps are present and actionable.
- [ ] Personality style applied (e.g. coaching mode reflected in tone/structure).

### policy_navigation
- [ ] Every policy-related claim has a citation (source/chunk reference).
- [ ] No ungrounded policy assertions (no hallucinated eligibility, deadlines, or amounts).

### mixed
- [ ] Both segments present: support/education segment and policy segment.
- [ ] Citations only in the policy segment; support segment free of uncited policy.

**Critical failure:** Any ungrounded policy claim or missing citation where policy is asserted → block release.

---

## 4. How to run

**Option A – Manual:** For each case, call the chat API (e.g. `POST /api/chat` or `POST /api/gateway/chat`) with a fresh or dedicated session, send `message` (+ `context`), then inspect the response and apply the assertions above. Record results in a spreadsheet or JSON (see §5).

**Option B – Script:** Maintain a list of cases (e.g. `data/pillar-matrix/cases.json` or per-pillar files). A script can:
1. For each case, create or reuse a session, send the message, get the response.
2. Parse response for citations and policy-like claims (heuristic or LLM-based).
3. Output a result file: `case_id`, `pillar`, `pass/fail`, `assertions_failed[]`, `notes`.

Either way, run the full matrix on every release candidate and block production promotion on critical safety or grounding failures.

---

## 5. Result record (example)

Store results for traceability (e.g. in `docs/reports/` or CI artifacts):

```json
{
  "run_id": "2026-03-04-pilot-rc1",
  "run_at": "2026-03-04T12:00:00Z",
  "total": 130,
  "passed": 128,
  "failed": 2,
  "critical_failures": 0,
  "by_pillar": {
    "emotional_support": { "total": 30, "passed": 30 },
    "practical_education": { "total": 30, "passed": 29 },
    "policy_navigation": { "total": 40, "passed": 40 },
    "mixed": { "total": 30, "passed": 29 }
  },
  "failures": [
    { "case_id": "pe-012", "pillar": "practical_education", "assertions_failed": ["plan_steps_present"], "critical": false },
    { "case_id": "mx-007", "pillar": "mixed", "assertions_failed": ["both_segments"], "critical": false }
  ]
}
```

---

## 6. References

- **Spec:** §17.6.2 (Pillar test matrix), §17.6.1 (Pillar SLO targets)
- **Checklist:** [PHASE4-PILOT-CHECKLIST.md](PHASE4-PILOT-CHECKLIST.md) §1–2
