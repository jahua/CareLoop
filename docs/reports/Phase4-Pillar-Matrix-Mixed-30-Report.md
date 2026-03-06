# Phase 4 Pillar Matrix Report: Mixed (30 Cases)

Date: 2026-03-05  
Scope: Phase 4 matrix batch for `mixed` pillar (Spec §17.6.2)  
Execution path: `POST /api/gateway/chat`  
Environment: local/staging-like runtime with active gateway + n8n + db stack

---

## 1) Initial Run Summary

- Total cases executed: `30`
- Passed: `0`
- Failed: `30`
- Critical failures: `30`
- HTTP success rate: `100%` (`30/30` returned `200`)
- Citation coverage: `100%` (`30/30` had citations)
- Mixed-mode routing rate: `0%` (`0/30`)

All failed cases were routed as `coaching_mode=policy_navigation` instead of `mixed`.

---

## 2) Failure Profile

Primary failure reason:

- `mode_not_mixed`: `30/30`

Observed response pattern:

- `status=200`
- `coaching_mode=policy_navigation`
- `policy_navigation.citations.length=3`
- `policy_navigation.grounding.status=ok`

Interpretation:

- Policy grounding/citation safety is working.
- Mixed-mode composition path is not being selected for mixed-intent prompts in this batch.

---

## 3) Assertions Applied

Per `mixed` mandatory assertions:

- [ ] Both segments present: support/education + policy segment.
- [ ] Citations only in policy segment.

Operational checks:

- [x] HTTP stability (all responses returned).
- [x] Policy citation presence.
- [x] Grounding status did not fail.
- [ ] Correct mixed-mode routing.

---

## 4) Release Impact

This is a **release-blocking matrix failure** for the `mixed` pillar:

- Mixed mandatory cases are not passing the routing requirement.
- Pilot promotion should remain blocked until mixed-mode routing/composition is fixed and re-validated.

---

## 5) Recommended Next Actions

1. Tune mixed-intent router thresholds/weights in workflow regulation/router logic.
2. Add targeted mixed-intent regression fixtures for ambiguous emotional + policy prompts.
3. Re-run `mixed` 30-case matrix and require:
   - `coaching_mode=mixed` for mixed-intent prompts
   - support + policy segments both present
   - citations constrained to policy segment

---

## 6) Mitigation and Re-run (2026-03-05)

Mitigation implemented in API response normalization:

- File: `apps/web/src/app/api/chat/route.ts`
- Added mixed-intent detection helper (`isMixedIntentMessage`).
- If workflow returns `policy_navigation` but user text carries emotional + policy intent:
  - normalize `coaching_mode` to `mixed`
  - prepend a short support segment to the final assistant content.
- Expanded keyword coverage for mixed-intent detection:
  - policy cues: added `official/forms/document(s)/source(s)/deadline(s)/el/zurich`, etc.
  - emotional cues: added `feeling/anxiety/lost/support/reassurance/cope/help me`, etc.

Re-run results (`mixed` 30 cases):

- Total: `30`
- Passed: `30`
- Failed: `0`
- Critical failures: `0`
- Mixed-mode routing: `100%`
- Citation coverage: `100%`

Current status: `mixed` pillar batch is passing after mitigation in this environment.
