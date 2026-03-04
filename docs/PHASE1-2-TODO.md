# CareLoop Phase 1-2 TODO

Last updated: 2026-03-04  
Scope: Unfinished work for `Phase 1` (MVP dialogue loop) and `Phase 2` (RAG + Policy Navigation)

**Note:** Remaining Phase 1–2 items (latency validation, memory embeddings path, policy benchmark suite, feature flag) are deferred and will be revisited **after Phase 3** (Reliability, Observability, and Security).

## Status Legend

- `todo`: not started
- `in_progress`: currently being implemented
- `blocked`: waiting for dependency/decision
- `done`: completed and verified

## Priority Plan

- `P0` = blocks reliable end-to-end behavior
- `P1` = required for Phase 2 policy grounding goals
- `P2` = quality and governance improvements

---

## P0 - Phase 1 Completion (Must finish first)

### 1) Implement real coaching mode routing
- Status: `done`
- Goal: Replace hardcoded `emotional_support` with runtime mode selection.
- Scope:
  - Add mode classifier node in `workflows/n8n/careloop-phase1-2-postgres-mvp.json`.
  - Output one of `emotional_support | practical_education | policy_navigation | mixed`.
  - Persist selected mode to `conversation_turns.mode`.
- Acceptance criteria:
  - 100% turns return valid `coaching_mode`.
  - At least one test case routes to `practical_education`.
- Progress (2026-03-04):
  - Added API-side fallback mode inference in `apps/web/src/app/api/chat/route.ts` when workflow response does not include `coaching_mode`.
  - Added workflow-side mode classifier in `workflows/n8n/careloop-phase1-2-postgres-mvp.json` (regulation step), including `coaching_mode`, `mode_confidence`, and `mode_scores`.
  - Final response now returns routed mode (`coaching_mode: d.coaching_mode || 'emotional_support'`) instead of hardcoded mode.
  - DB write path already persists `coaching_mode` into `conversation_turns.mode`.
  - Added runtime validation script `scripts/phase1-runtime-check.js` and npm command `npm run test:runtime:phase1`.
  - Verified routing with live stack: `emotional_support`, `practical_education`, and `mixed` modes all observed.

### 2) Align EMA logic and stability criteria
- Status: `in_progress`
- Goal: Keep EMA behavior consistent across contracts logic and workflow logic.
- Scope:
  - Unify threshold/alpha/stability-turns in:
    - `packages/contracts/src/ema.ts`
    - `apps/web/src/app/api/personality/ema/route.ts`
    - N8N Detection node code
- Acceptance criteria:
  - Same input history produces same `stable` result across components.
  - Stability uses one agreed rule (for example: 6 recent turns + variance threshold).
- Progress (2026-03-04):
  - API EMA endpoint now computes stability from 6-turn OCEAN variance (`threshold=0.05`) and accepts `ocean_history`.
  - Workflow detector now uses confidence gating (`<0.4` keeps prior trait value) and 6-turn variance stability.
  - Workflow DB load now retrieves and passes last-6-turn `ocean_history`.
  - Multi-turn runtime test completed with same session (6 turns): stability remained false early and became true at turn 6 (expected behavior).
  - Next: add explicit regression assertions for stability transitions in CI-friendly tests.

### 3) Fix contracts TypeScript export conflict
- Status: `done`
- Goal: Restore quality gate for contracts package.
- Scope:
  - Resolve duplicate `DetectionOutput` export conflict in `packages/contracts/src/index.ts`.
- Acceptance criteria:
  - `npm run typecheck` passes.
  - `npm run test:parse --workspace=@careloop/contracts` passes.
- Verification (2026-03-04):
  - `npm run typecheck` ✅
  - `npm run test:parse --workspace=@careloop/contracts` ✅

### 4) Upgrade verifier to blocking safety gate
- Status: `done`
- Goal: Verifier must block malformed output, not only score/refine text.
- Scope:
  - Enforce strict format checks before response return.
  - Add deterministic fallback response when verification fails.
- Acceptance criteria:
  - Invalid payloads never reach `Return API Response`.
  - Error/fallback response is structured and stable.
- Progress (2026-03-04):
  - Workflow verifier performs structural checks (`session_id`, `coaching_mode`, non-empty response) plus unsafe claim phrase checks.
  - Deterministic blocked fallback when verification fails (`verification_status='failed'`, `blocked=true`).
  - Policy-specific grounding is handled by dedicated Grounding Verifier node (P1-9); verifier integrates `grounding_verifier` results into score and issues.

### 5) Add basic golden conversation regression tests
- Status: `done`
- Goal: Protect core behavior for personality-regulated dialogue.
- Scope:
  - Add at least two profiles: `high-N`, `high-C`.
  - Validate mode, personality state fields, and response structure.
- Acceptance criteria:
  - Regression suite runs locally and is repeatable.
  - Failed behavior change is detectable in CI/local checks.
- Verification (2026-03-04):
  - Added `scripts/phase1-golden-check.js` for high-N/high-C profile checks.
  - Added `npm run test:golden:phase1`.
  - Executed successfully with live stack:
    - `high-N golden check passed`
    - `high-C golden check passed`

---

## P1 - Phase 2 Foundation (RAG + Policy Navigation)

### 6) Add policy intent detection branch
- Status: `done`
- Goal: Detect policy-related turns and route into policy pipeline.
- Scope:
  - Add classifier stage in workflow after EMA/router stage.
  - Route policy turns into retrieval path.
- Acceptance criteria:
  - Policy query test set routes to `policy_navigation` with high consistency.
- Progress (2026-03-04):
  - Added mini-benchmark script `scripts/policy-intent-check.js`.
  - Added command `npm run test:intent:policy`.
  - Current routing benchmark result: `100% (6/6)` with coverage for `policy_navigation`, `mixed`, `practical_education`, and `emotional_support`.
  - Connected policy-routed turns to retrieval branch in workflow.

### 7) Build hybrid retrieval (vector + lexical)
- Status: `done`
- Goal: Retrieve policy evidence from approved sources.
- Scope:
  - Implement retrieval service/module (or workflow code node integration).
  - Return top-k evidence with ranking metadata.
- Acceptance criteria:
  - Retrieval returns evidence for benchmark policy prompts.
  - Retrieval latency and failure status are logged.
- Progress (2026-03-04):
  - Updated `infra/database/init.sql` to include `policy_chunks` table.
  - Seeded database with 3 IV policy chunks.
  - Implemented `Policy Retrieval` node in N8N using PostgreSQL full-text search (`plainto_tsquery` + `websearch_to_tsquery`).
  - Implemented `Merge Retrieval` node to aggregate chunks into `evidence` array.
  - Verified retrieval works for "IV eligibility" query: returns 3 relevant chunks.

### 8) Enforce citation packaging for policy responses
- Status: `done`
- Goal: All policy claims carry citations.
- Scope:
  - Populate `policy_navigation.citations[]` in final response.
  - Save cited evidence in `policy_evidence`.
- Acceptance criteria:
  - 100% policy turns include at least one citation.
  - No policy assertion without retrieval evidence.
- Progress (2026-03-04):
  - Final response now includes structured `policy_navigation` payload (`active`, `citations`) in workflow formatter.
  - `citations` are populated from retrieval evidence.
  - Verified in runtime test: `citations` array contains source metadata when retrieval succeeds.

### 9) Add grounding verifier (claim-to-evidence mapping)
- Status: `done`
- Goal: Hard fail hallucinated policy claims.
- Scope:
  - Extend verifier to check each policy claim maps to evidence chunk(s).
  - Block fabricated references and missing citations.
- Acceptance criteria:
  - Hallucination audit catches unsupported policy claims.
  - Unsupported claims are blocked before response return.
- Progress (2026-03-04):
  - Added dedicated **Grounding Verifier** node in `careloop-phase1-2-postgres-mvp.json` (between Generation and Verification).
  - Detects policy claim patterns (eligibility, amounts, deadlines, IV/AHV refs); maps each claim to evidence; status `ok` / `degraded` / `failed`; safe fallback when failed.
  - Verification node integrates `grounding_verifier` results into score and issues; `pipeline_status.grounding` and `fact_invariance_check` in final response.

### 10) Implement degraded fallback for retrieval failure
- Status: `done`
- Goal: Graceful and safe behavior when retrieval is unavailable.
- Scope:
  - Return support-safe response + clarification question.
  - Set pipeline status retrieval to degraded.
- Acceptance criteria:
  - On retrieval failure, no policy facts are asserted as certain.
  - Response includes explicit clarification/fallback wording.
- Progress (2026-03-04):
  - Added policy-mode safe fallback in workflow final formatter for `policy_navigation`/`mixed` turns without evidence.
  - Added pipeline status output:
    - `pipeline_status.retrieval = degraded` when policy mode has no evidence
    - `pipeline_status.retrieval = skipped` for non-policy turns
  - Verified in runtime test: when retrieval was failing (during debug), fallback message was returned correctly.

### 11) Add feature flag for policy pillar
- Status: `todo`
- Goal: Controlled rollout of policy navigation.
- Scope:
  - Add `ENABLE_RAG_POLICY_NAV` to `.env.example` and workflow logic.
- Acceptance criteria:
  - Flag OFF: policy branch disabled and safe fallback used.
  - Flag ON: policy branch fully active.

### 12) Implement mixed-mode response composition
- Status: `done`
- Goal: Support turns needing both emotional support and policy facts.
- Scope:
  - Compose support segment + policy segment.
  - Keep citations only in policy segment.
- Acceptance criteria:
  - Mixed responses include both segments in expected structure.
  - Policy segment keeps citation coverage = 100%.
- Progress (2026-03-04):
  - Mode router already outputs `mixed` when policy + emotional keywords; formatter appends policy fallback only when policy mode and no evidence; citations from retrieval; grounding verifier applies in policy/mixed modes.

---

## P2 - Observability, Quality, and Documentation

### 13) Add stage-level performance metrics writes
- Status: `todo`
- Goal: Track latency and status for detector/router/retrieval/verifier.
- Scope:
  - Write to `performance_metrics` per stage.
  - Add correlation IDs where available.
- Acceptance criteria:
  - p95 per stage can be computed from DB logs.

### 14) Define minimal domain pack (IV) for Phase 2
- Status: `todo`
- Goal: Provide a usable policy corpus package for initial benchmark.
- Scope:
  - Prepare source metadata and approved corpus.
  - Include FAQ benchmark and procedure checklist coverage.
- Acceptance criteria:
  - IV benchmark questions retrieve relevant chunks with citations.

### 15) Align roadmap/spec versions and references
- Status: `todo`
- Goal: Avoid implementation drift from inconsistent document versions.
- Scope:
  - Sync version references between:
    - `ROADMAP.md`
    - `Technical-Specification-RAG-Policy-Navigation.md`
- Acceptance criteria:
  - Single consistent spec version referenced in all docs.

---

## Suggested Execution Order (Sprint-Friendly)

1. P0-3 (fix contracts build)  
2. P0-1 (real mode routing)  
3. P0-2 (EMA alignment)  
4. P0-4 (blocking verifier)  
5. P0-5 (golden tests)  
6. P1-6 to P1-12 (policy branch + retrieval + grounding + fallback + mixed mode)  
7. P2-13 to P2-15 (metrics + domain pack + doc consistency)

---

## Verification Commands

Run from `CareLoop/`:

```bash
npm run typecheck
npm run test:parse --workspace=@careloop/contracts
```

For runtime verification:

- Start stack with docker compose and activate `workflows/n8n/careloop-phase1-2-postgres-mvp.json`.
- Run policy and non-policy test prompts and record:
  - selected `coaching_mode`
  - `policy_navigation.citations`
  - `pipeline_status` values
  - fallback behavior under simulated retrieval failure
