# Phase 4 Pillar Matrix Report: Practical Education (30 Cases)

Date: 2026-03-05  
Scope: Phase 4 matrix batch for `practical_education` pillar (Spec §17.6.2)  
Execution path: `POST /api/gateway/chat`  
Environment: local/staging-like runtime

---

## 1) Final Run Summary

- Total cases: `30`
- Passed: `30`
- Failed: `0`
- Critical failures: `0`
- Practical mode routing: `100%`
- Unexpected policy citations: `0%`

---

## 2) Initial Failure and Mitigation

Initial practical run showed routing instability:

- Initial result: `15/30` pass
- First mitigation rerun: `20/30` pass
- Final rerun: `30/30` pass

Root causes:

- Some practical prompts were routed to `emotional_support`.
- Education keyword coverage was too narrow for cases such as `checklist`, `method`, `prioritize`, `actionable`.

Mitigations (implemented in `apps/web/src/app/api/chat/route.ts`):

- Added `normalizePracticalFalseNegative(...)` safeguard:
  - when mode is `emotional_support`, no policy cues are present, and education intent dominates, normalize to `practical_education`.
- Expanded education keyword coverage:
  - added `step-by-step`, `checklist`, `method`, `prioritize`, `actionable`, `next steps`.

Final rerun outcome:

- `30/30` pass
- `0` critical failures

---

## 3) Assertions Used

- [x] `coaching_mode = practical_education`
- [x] actionable plan structure present in response
- [x] no policy citations for practical-only prompts
- [x] no critical safety/grounding failure in this batch

---

## 4) Conclusion

`practical_education` pillar currently passes required 30-case matrix checks in this environment after routing normalization and keyword expansion.
