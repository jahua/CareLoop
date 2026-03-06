# CareLoop Phase 3 TODO

Last updated: 2026-03-05  
Scope: **Phase 3 – Reliability, Observability, and Security** (Weeks 11–13)  
Aligned with: `ROADMAP.md` §6, `Technical-Specification-RAG-Policy-Navigation.md` §11–12, §15.1, §17.4–17.6

## Status Legend

- `todo`: not started
- `in_progress`: currently being implemented
- `blocked`: waiting for dependency/decision
- `done`: completed and verified

## Priority Plan

- `P0` = blocks production readiness / safety
- `P1` = required for Phase 3 DoD
- `P2` = recommended (gateway, model-tier routing, background jobs)

---

## P0 – Failure Handling & Structured Responses

### 1) Implement all Spec §12 failure paths
- Status: `done`
- Goal: Every failure path returns structured responses; no raw stack traces to clients.
- Scope:
  - **Detector failure:** keep prior stable traits, move to neutral style.
  - **RAG failure:** non-policy emotional support + clarification prompt; set `retrieval=degraded`.
  - **Verifier failure:** safe fallback response with minimal claims.
  - **Upstream timeout:** controlled fallback JSON only (no plain-text error).
  - **EMA divergence:** freeze updates, revert to last stable state; emit `ema_divergence` alert.
  - **Mixed-mode token overflow:** prioritize policy segment facts/citations, compress support segment.
  - **Language fallback failure:** return in best detected language (or English) with explicit notice.
- Acceptance criteria:
  - All failure paths return structured envelopes with stable `error_code`.
  - No raw stack traces or unhandled exceptions exposed to clients.
- Progress (2026-03-04):
  - **Chat API:** All failure paths now return `ErrorResponseEnvelope`. When N8N returns 200 with `success: false` and `error: { error_code, message }`, API maps to envelope and returns 503. When response is malformed (no data, missing `session_id` or `message.content`), API returns `verifier_fallback` or `internal_error` envelope instead of passing through. No raw upstream body is ever returned to the client.
  - **N8N workflow:** All Code nodes (Merge, Detection, Regulation, Merge Retrieval, Generation, Grounding, Verification, Format Response) pass through when `success === false && error`; Format Response also emits `verifier_fallback` envelope when `session_id` or reply content is missing. Error envelope flows to Return API Response; API normalizes to 503.
- Reference: Spec §12.

### 2) Add structured error envelopes and error_code
- Status: `done`
- Goal: Clients and logs see consistent, parseable error shapes.
- Scope:
  - Define error contract (e.g. in `packages/contracts`) with `error_code`, `message`, `stage`, `retryable`.
  - Use in workflow fallback nodes and API response layer.
- Acceptance criteria:
  - Every error response validates against shared error schema.
  - Logs use same codes for correlation.
- Progress (2026-03-04):
  - Added `packages/contracts/src/errors.ts`: `ERROR_CODES`, `StructuredErrorSchema`, `ErrorResponseEnvelopeSchema`, parse/safeParse helpers. Exported from `packages/contracts`.
  - Wired API layer: `apps/web/src/app/api/chat/route.ts` and `apps/web/src/app/api/personality/ema/route.ts` return `ErrorResponseEnvelope` on all error paths (timeout_fallback, internal_error, validation_failed); frontend `page.tsx` reads `error.message` from envelope.
  - **API normalization:** Chat route now treats N8N 200+error envelope or malformed 200 as failure and returns our envelope (P0-1). **N8N error branch:** See `docs/WORKFLOW-ERROR-ENVELOPE.md` for the exact response shape when adding an error path in the workflow (success: false, error: { error_code, message, stage }, request_id, etc.).
  - Workflow now passes through error envelope in all Code nodes; Format Response returns it or emits verifier_fallback when required fields missing (see WORKFLOW-ERROR-ENVELOPE.md).

---

## P1 – Audit, Correlation IDs, and Redaction

### 3) Audit JSONL per turn
- Status: `done`
- Goal: Full observability and audit trail for every turn.
- Scope:
  - Emit JSONL per turn with: input hash, detected traits/confidence, retrieval IDs, citation list, verifier decision, final status.
  - Correlation IDs across frontend, orchestrator, and DB writes.
- Acceptance criteria:
  - Audit JSONL and correlation IDs available for every turn.
  - Can reconstruct turn flow from logs for debugging and compliance.
- Progress (2026-03-04):
  - **Correlation ID:** `request_id` added. Chat API generates or accepts `request_id` (body or `x-request-id`), passes to N8N; workflow Ingest and Format Response pass through; error envelope includes `request_id`. Enables tracing frontend → API → workflow → response.
  - **Audit JSONL:** `apps/web/src/lib/audit.ts` appends one JSONL line per successful turn when `AUDIT_LOG_PATH` is set. Each line includes: `request_id`, `session_id`, `turn_index`, `coaching_mode`, `pipeline_status`, personality summary, `retrieval_ids`/`citation_count`, `verifier_status`, `timestamp`. No raw user message (privacy). Fire-and-forget append; optional env var.
  - **Input hash:** Optional `input_hash` (SHA-256 truncated) of user message added to audit line via `hashForAudit()`; no PII stored. **Turn latency:** `turn_latency_ms` (API-side) added to each audit line for SLO visibility.
  - **DB persistence (optional):** `infra/database/init.sql` creates `audit_log` table. When `AUDIT_DB_WRITE=true` and `AUDIT_DATABASE_URL` (or `DATABASE_URL`) is set, `apps/web/src/lib/audit-db.ts` writes each turn to `audit_log` (fire-and-forget). Chat route calls `writeAuditToDb(auditPayload)` after `auditTurn(payload)`. See `docs/AUDIT-LOG-PERSISTENCE.md`.
- Reference: Spec §11.

### 4) Redaction and pseudonymization in logs
- Status: `done`
- Goal: No raw sensitive content in analytics; pseudonymized IDs in logs.
- Scope:
  - Apply redaction rules for personal names and contact details before persistent logs.
  - Use pseudonymous identifiers for user/session in observability.
- Acceptance criteria:
  - No raw sensitive personal content in analytics exports.
  - Compliant with Spec §5, §17.4.
- Progress (2026-03-04):
  - **Policy:** Audit and feedback payloads do not include user message content; only pseudonymous IDs (`session_id`, `request_id`). See `docs/PRIVACY-AND-REDACTION.md`.
  - **Helper:** `apps/web/src/lib/redact.ts` exports `redactForLog(text)` to redact email and phone patterns before any future free-text logging. Linked from `docs/SECRETS-AND-CREDENTIALS.md`.

---

## P1 – Optional Feedback and Quality Signals

### 5) Capture optional feedback signals
- Status: `done`
- Goal: Enable quality monitoring and product iteration.
- Scope:
  - Capture optional post-turn feedback: e.g. `thumbs_up_down`, `helpfulness_score`.
  - Persist to DB or analytics pipeline; do not block response path.
- Acceptance criteria:
  - Optional feedback signals captured when provided; available for quality dashboards.
- Progress (2026-03-04):
  - **POST /api/feedback:** Accepts `session_id` (required), `turn_index?`, `request_id?`, `thumbs_up_down?` ('up'|'down'), `helpfulness_score?` (0–5). At least one of thumbs_up_down or helpfulness_score required. Appends one JSONL line to file when `FEEDBACK_LOG_PATH` is set; returns 202 Accepted. `apps/web/src/lib/feedback.ts` + `apps/web/src/app/api/feedback/route.ts`. Frontend can call after displaying a turn to submit thumbs or score.
- Reference: Spec §11, ROADMAP §6.3 DoD.

---

## P2 – Gateway (Shadow Then Active)

### 6) Gateway control plane (shadow mode first)
- Status: `in_progress`
- Goal: Centralize session lifecycle, auth, routing, and correlation.
- Scope:
  - Add Gateway service: session lifecycle, correlation IDs, authN/authZ, rate limits, routing (Spec §15.1.A).
  - Deploy in **shadow mode** (observe only); no traffic routed through gateway initially.
  - Minimum gateway request envelope: `request_id`, `session_id`, `user_id` (pseudonymous), `message`, `context`, `routing_hints`.
- Acceptance criteria:
  - Gateway runs in shadow mode; request/response logged for validation.
  - Rollout plan: shadow → canary → GA (Spec §15.1.G).
- Progress:
  - **Design:** `docs/GATEWAY-SHADOW-DESIGN.md` (envelope, shadow/canary/GA, success gate).
  - **Stub:** `POST /api/gateway/chat` accepts gateway envelope, logs to `GATEWAY_SHADOW_LOG` when set, forwards to `/api/chat`. `apps/web/src/lib/gateway-shadow.ts`, `apps/web/src/app/api/gateway/chat/route.ts`.
  - **Optional auth:** `GATEWAY_API_KEY` → require x-api-key or Authorization: Bearer; else 401.
  - **Optional rate limit:** `GATEWAY_RATE_LIMIT_PER_MINUTE` → in-memory limit per user_id or IP; 429 + Retry-After when exceeded; `X-RateLimit-Remaining` on success. See `apps/web/src/lib/gateway-rate-limit.ts`.
  - Remaining: auth/rate-limit when enabling; canary then GA with success gate.
- Reference: Spec §15.1.A, §15.1.G.

### 7) Gateway rollout and success gate
- Status: `in_progress`
- Goal: Safe promotion to active gateway when enabled.
- Scope:
  - Follow rollout: shadow → canary → general availability.
  - Success gate: no critical hallucination increase; stable or better benchmark scores (Spec §15.1.G).
- Acceptance criteria:
  - If gateway is enabled: rollout plan followed; success gate met before full traffic.
- Progress: Canary checklist in [GATEWAY-SHADOW-DESIGN.md](GATEWAY-SHADOW-DESIGN.md) §6 (baseline metrics, 10%→50%→100% gateway share, success gate). Added executable scripts: baseline capture `scripts/gateway-baseline-capture.js` (`npm run job:gateway-baseline-capture`) and gate checker `scripts/gateway-canary-check.js` (`npm run job:gateway-canary-check`) to evaluate sample volume, envelope validity, 5xx/p95 drift vs baseline, 429 rate, and error-envelope rate from `GATEWAY_SHADOW_LOG`.
  - 2026-03-05 canary validation run:
    - Baseline (direct `/api/chat`): 100 requests, p95=4609ms, 5xx=0.
    - Canary (gateway `/api/gateway/chat`): 30 requests, p95=330ms, 5xx=0, 429=0, error-envelope rate=0, invalid envelope=0.
    - Gate result: `status=ok` with default minimum sample threshold (`MIN_REQUESTS=20`).
  - 2026-03-05 high-sample canary gate run:
    - Canary (gateway `/api/gateway/chat`): 100 requests, p95=327ms, 5xx=0, 429=0, error-envelope rate=0, invalid envelope=0.
    - Gate result: `status=ok` with stricter minimum sample threshold (`MIN_REQUESTS=50`).
  - 2026-03-05 citation coverage diff run:
    - Baseline audit sample: `logs/audit.baseline.policy.40.jsonl` (40 policy-intent turns).
    - Canary audit sample: `logs/audit.canary.policy.40.jsonl` (40 policy-intent turns via gateway).
    - Gate check result: `policy_citation_coverage` passed (`baseline=1.0000`, `canary=1.0000`, `max_drop=0.05`).
  - 2026-03-05 N8N workflow hygiene:
    - Imported and activated `CareLoop Simple (Quick) Mode` (`careloop-turn-simple`) in the active n8n instance.
    - Removed duplicate legacy workflow entries; active set is now the intended pair (`careloop-turn`, `careloop-turn-simple`).
  - 2026-03-05 split-rollout drill (50/50 simulation):
    - Simulated 50% split by running 100 direct requests (`/api/chat`) and 100 gateway requests (`/api/gateway/chat`) with the same policy-intent prompt profile.
    - Canary gate (gateway half) passed with `MIN_REQUESTS=50`: `req=100`, `resp=100`, `p95=837ms`, `5xx=0`, `429=0`, `error-envelope rate=0`, `invalid_envelopes=0`.
    - Citation coverage guard also passed: `baseline=1.0000`, `canary=1.0000`, `max_drop=0.05`.
  - 2026-03-05 10% rollout stage drill:
    - Simulated stage window with 180 direct requests + 20 gateway requests (10% canary share).
    - Fresh baseline capture: `BASELINE_P95_MS=5838`, `BASELINE_5XX_RATE=0`.
    - Gateway gate result (`MIN_REQUESTS=20`): `status=ok` with `req=20`, `resp=20`, `p95=4473ms`, `5xx=0`, `429=0`, `error-envelope rate=0`, `invalid_envelopes=0`.
    - Citation coverage guard passed: `baseline=1.0000`, `canary=1.0000`, `max_drop=0.05`.
  - 2026-03-05 local Day-2 execution run (fresh sample):
    - Gateway shadow log was reset and recollected from active `web` container to `logs/gateway-shadow.day2.10pct.20.jsonl`.
    - Sent 20 requests through `/api/gateway/chat` (all `200`).
    - Canary gate result (`MIN_REQUESTS=20`, `CANARY_WINDOW_MINUTES=60`): `status=ok` with `req=20`, `resp=20`, `p95=1689ms`, `5xx=0`, `429=0`, `error-envelope rate=0`, `invalid_envelopes=0`.
    - Baseline inputs used for this local run: `BASELINE_P95_MS=20465`, `BASELINE_5XX_RATE=0.15` (captured from local baseline job under constrained dev resources).
  - 2026-03-05 local Day-3 execution run (50% stage simulation):
    - Built fresh baseline policy audit sample: 40 direct `/api/chat` turns (all `200`) -> `logs/audit.baseline.policy.40.local.jsonl`.
    - Built fresh canary sample: 50 gateway `/api/gateway/chat` turns (all `200`) -> `logs/gateway-shadow.day3.50pct.50.jsonl` and `logs/audit.canary.policy.50.local.jsonl`.
    - Canary gate result (`MIN_REQUESTS=50`, `CANARY_WINDOW_MINUTES=60`): `status=ok` with `req=50`, `resp=50`, `p95=5688ms`, `5xx=0`, `429=0`, `error-envelope rate=0`, `invalid_envelopes=0`.
    - Citation coverage diff gate: `policy_citation_coverage` passed (`baseline=1.0000`, `canary=1.0000`, `max_drop=0.05`).
  - 2026-03-05 local Day-4 execution run (100% cutover simulation):
    - Built fresh canary sample: 100 gateway `/api/gateway/chat` turns (all `200`) -> `logs/gateway-shadow.day4.100pct.100.jsonl` and `logs/audit.canary.policy.100.local.jsonl`.
    - Canary gate result (`MIN_REQUESTS=50`, `CANARY_WINDOW_MINUTES=60`): `status=ok` with `req=100`, `resp=100`, `p95=7891ms`, `5xx=0`, `429=0`, `error-envelope rate=0`, `invalid_envelopes=0`.
    - Citation coverage diff gate: `policy_citation_coverage` passed (`baseline=1.0000`, `canary=1.0000`, `max_drop=0.05`) using `logs/audit.baseline.policy.40.local.jsonl` vs `logs/audit.canary.policy.100.local.jsonl`.
    - Local cutover decision for simulation window: `promote` (all gates green in this controlled environment).
  - Remaining: execute real deployment traffic-slice rollout (10% -> 50% -> 100%) and keep gate checks green before GA cutover; record each stage using the template in `docs/OPERATIONS-RUNBOOK.md` ("Production Rollout Record").

---

## P2 – Model-Tier Router

### 8) Model-tier router (light / medium / heavy)
- Status: `in_progress`
- Goal: Cost-quality tradeoff without skipping grounding/verification.
- Scope:
  - Implement dual router: Intent Router (pillar mode) + Model Tier Router (`light` | `medium` | `heavy`).
  - `light`: short non-policy turns, low reasoning depth.
  - `medium`: standard coaching + moderate policy complexity.
  - `heavy`: ambiguous eligibility/procedural edge-cases, verification retries, complex multi-step reasoning.
  - Safety: cannot skip grounding/verification steps (Spec §15.1.B).
- Acceptance criteria:
  - Tier selection is observable; grounding and verification always run for policy-relevant turns.
- Progress:
  - Design in [MODEL-TIER-ROUTER-DESIGN.md](MODEL-TIER-ROUTER-DESIGN.md) (tiers, selection from routing_hints/intent, pass-through to pipeline, observability, implementation order).
  - Intent-router decision logic in `workflows/n8n/careloop-phase1-2-postgres-mvp.json` was upgraded toward Spec §8.4.F: normalized score thresholds, tie-break rules, and low-confidence clarification flag (`needs_clarifying_question`, `clarifying_question`, `mode_routing_reason`).
  - `context.model_tier` is now consumed in N8N:
    - Ingest validates and stores tier (`light`/`medium`/`heavy`, default `medium`).
    - Regulation applies safety escalation (`policy_navigation`/`mixed` + `light` ⇒ `medium`) and emits `model_tier_requested`, `model_tier_effective`, `retrieval_top_k`.
    - Retrieval uses dynamic `LIMIT {{ $json.retrieval_top_k || 3 }}`.
    - Generation uses tier-aware params (`max_tokens`, `temperature`) and records effective tier in `generator.generation_config`.
  - Remaining: calibrate tier heuristics with benchmark cases and tune heavy-tier triggers for ambiguous policy turns.

---

## P2 – Background Jobs and Corpus Hygiene

### 9) Background jobs for corpus and retrieval quality
- Status: `in_progress`
- Goal: Corpus freshness, citation validity, and regression coverage.
- Scope:
  - Policy corpus freshness checks (daily).
  - Source recrawl and re-embedding (scheduled/incremental).
  - Stale citation detector (link validity + version hash mismatch).
  - Retrieval quality regression suite on benchmark questions.
  - Emit structured job telemetry into `performance_metrics` with `stage=background_job` (Spec §15.1.E).
- Acceptance criteria:
  - At least one scheduled job runs (e.g. corpus freshness); telemetry written.
  - Regression suite can be run on demand or on schedule.
- Progress: Design in [BACKGROUND-JOBS-DESIGN.md](BACKGROUND-JOBS-DESIGN.md). Corpus freshness: `scripts/corpus-freshness-check.js` → `npm run job:corpus-freshness`. Source recrawl/re-embedding baseline: `scripts/source-recrawl-reembed.js` → `npm run job:source-recrawl` (content-hash change detection, dry-run by default, apply mode replaces changed source chunks). Stale citation detector: `scripts/stale-citation-detector.js` → `npm run job:stale-citation` (checks distinct `policy_chunks.url` with timeout, emits stale ratio + samples). Retrieval smoke: `scripts/retrieval-regression-smoke.js` → `npm run job:retrieval-smoke` (one policy question, assert content + citations; env: `BASE_URL` or `CARELOOP_BASE_URL`). Multi-case runner now supports explicit policy-intent assertions (`require_policy_mode` / `expected_coaching_mode`) via `scripts/retrieval-regression-runner.js` + `scripts/fixtures/retrieval-cases.json`. Telemetry to `BACKGROUND_JOB_LOG_PATH` or stdout.
  - 2026-03-05 regression hardening result:
    - Router thresholds and policy cues were tightened in `workflows/n8n/careloop-phase1-2-postgres-mvp.json` so explicit policy requests route to `policy_navigation` more reliably.
    - Regression runner citation parsing was corrected to include `policy_navigation.citations`.
    - `npm run job:retrieval-regression -- scripts/fixtures/retrieval-cases.json` now passes `5/5` (`status=ok`).

---

## P1 – SLO Monitoring

### 10) SLO monitoring and alerting
- Status: `in_progress`
- Goal: Operational visibility and alert thresholds.
- Scope:
  - Gateway availability ≥ 99.9%.
  - Routing decision latency p95 ≤ 50ms.
  - Retrieval timeout ≤ 2.0s.
  - Verification timeout ≤ 1.5s (Spec §15.1.F, §17.6).
  - Define alert thresholds and dashboards for critical failures.
- Acceptance criteria:
  - SLO metrics collectable (from gateway/logs/DB); alerts fire on breach.
- Progress (2026-03-04):
  - **Health check:** GET /api/health returns `{ ok, service, timestamp }` for availability probing (load balancer, uptime). See `docs/SLO-AND-MONITORING.md` for target SLOs and where metrics will come from.
  - **API turn latency:** Each successful turn audit line includes `turn_latency_ms`; usable for p95 dashboards and SLO (e.g. end-to-end ≤ 2s). Chat route records `startedAt` and passes `latencyMs` to `buildAuditPayload`.
  - **Alert thresholds:** `docs/SLO-AND-MONITORING.md` now defines recommended alert thresholds (health down, turn latency p95/p99, error rate, retrieval/verification timeouts) and where to get metrics (health endpoint, audit JSONL / `audit_log.turn_latency_ms`).
  - **Stage timings:** Chat API persists `stage_timings` from workflow response to `performance_metrics` when N8N includes that array in the success payload. Workflow now emits per-stage timing entries (`detection`, `routing`, `retrieval`, `generation`, `grounding`, `verification`) with `duration_ms`, plus `end_to_end` duration in `Format Response` (`workflows/n8n/careloop-phase1-2-postgres-mvp.json`). See `apps/web/src/lib/performance-metrics.ts`, `docs/SLO-AND-MONITORING.md`, `docs/WORKFLOW-ERROR-ENVELOPE.md` (Stage timings).
  - **Monitoring baseline pack (2026-03-05):** Added executable SQL dashboard/alert queries in `docs/monitoring/PHASE3-MONITORING-QUERIES.sql` covering end-to-end p50/p95/p99, stage p95, stage failure rate, retrieval/verification timeout breaches, citation coverage, and top error codes.
  - **Alert rules pack (2026-03-05):** Added `docs/monitoring/ALERT-RULES.md` with warning/critical thresholds, query mappings, notification routing, and rollout promotion gates.
  - **Monitoring calibration (2026-03-05):** Stage status `fallback` is now treated as degradation (not hard failure) in `docs/monitoring/PHASE3-MONITORING-QUERIES.sql` query #3; added query #3b for `fallback_rate_pct` trend. `docs/monitoring/ALERT-RULES.md` now distinguishes hard-fail alerts from fallback-rate warning alerts. Local DB validation run confirms `hard-fail rate=0%` while fallback remains visible for detector/generator trend monitoring.
  - Remaining: wire query panels and alert rules into the monitoring platform (Grafana/Alertmanager or equivalent) and validate live notifications.

---

## P1 – Security and Privacy

### 11) Security and privacy standards
- Status: `done`
- Goal: Align with Spec §17.4 and Swiss FADP where applicable.
- Scope:
  - Secrets in env only; least privilege for service accounts and data access.
  - Retention and deletion policies aligned with Swiss FADP.
  - Explicit user consent required before enabling personality profiling.
  - Data export/delete controls for profile-related records.
- Acceptance criteria:
  - No hardcoded credentials; access paths documented; consent and data controls documented or implemented.
- Progress (2026-03-04):
  - **Documentation:** `docs/SECURITY-AND-PRIVACY.md` summarizes Spec §17.4: secrets, least privilege, no raw errors to clients, redaction/pseudonymization (links to PRIVACY-AND-REDACTION), retention/deletion, consent for profiling, export/delete. Links from SECRETS and PRIVACY docs.
  - **Access paths:** Same doc now includes "Access paths (deployed services)" table: Next.js (N8N + optional file logs, no DB); N8N (PostgreSQL, LLM); DB (receives N8N); future gateway. Production note: restrict DB credentials and avoid exposing webhook/LLM env to frontend.
  - **Export/delete and retention:** `docs/DATA-EXPORT-AND-DELETION.md` defines retention defaults, export (GET /api/data/export) and deletion (POST /api/data/delete) contracts, consent for profiling, and deletion order. Linked from SECURITY-AND-PRIVACY.
  - **Stub routes:** GET /api/data/export and POST /api/data/delete validate session_id (UUID). When DATABASE_URL or AUDIT_DATABASE_URL is set, they perform export (session, turns, personality_states, policy_evidence) and deletion (policy_evidence → personality_states → performance_metrics → conversation_turns → audit_log → chat_sessions). Optional: set DATA_API_KEY and send x-api-key or Authorization: Bearer. See `apps/web/src/lib/db.ts`, `data-export.ts`, `data-delete.ts`.
  - Remaining: runbook for production; consider rate limits and audit log for delete.

---

## Phase 3 Definition of Done (Checklist)

From ROADMAP §6.3:

- [x] **DoD 1:** All failure paths return structured responses; no raw stack traces to clients (ErrorResponseEnvelope in chat/EMA APIs; N8N 200+error/malformed normalized to envelope).
- [x] **DoD 2:** Audit JSONL and correlation IDs available for every turn (request_id end-to-end; AUDIT_LOG_PATH JSONL per turn).
- [x] **DoD 3:** Optional feedback signals (e.g. thumbs up/down) captured for quality monitoring (POST /api/feedback + FEEDBACK_LOG_PATH).
- [ ] **DoD 4:** If gateway is enabled: rollout plan followed (shadow → canary); success gate: no critical hallucination increase, stable or better benchmark scores (Spec §15.1.G).

---

## Suggested Execution Order (Sprint-Friendly)

1. P0-1, P0-2 (failure handling + error envelopes).
2. P1-3, P1-4 (audit JSONL + redaction).
3. P1-5 (feedback signals).
4. P1-10, P1-11 (SLO monitoring + security/privacy).
5. P2-6, P2-7 (gateway shadow + rollout).
6. P2-8 (model-tier router).
7. P2-9 (background jobs).

---

## Verification Commands (When Implemented)

Run from `CareLoop/`:

```bash
npm run typecheck
npm run test:parse --workspace=@careloop/contracts
# Add when available:
# npm run test:audit
# npm run test:slo
```

Manual checks:

- Trigger each failure path (detector fail, RAG fail, verifier fail, timeout) and confirm structured response.
- Inspect audit JSONL for a sample of turns; verify correlation IDs end-to-end.
- If gateway is used: run shadow mode and compare metrics to baseline before canary.

---

## References

- **Phase 3 report:** `CareLoop/docs/reports/Phase3-Reliability-Observability-Report.md` (implementation summary).
- **ROADMAP:** `CareLoop/ROADMAP.md` §6 (Phase 3).
- **Spec:** `CareLoop/Technical-Specification-RAG-Policy-Navigation.md` §11 (Observability), §12 (Failure Handling), §15.1 (OpenClaw-Inspired), §17.4 (Security/Privacy), §17.6 (Operational SLO).
- **Workflow error envelope:** `CareLoop/docs/WORKFLOW-ERROR-ENVELOPE.md` (N8N error branch response shape for P0-2).
- **Audit DB persistence:** `CareLoop/docs/AUDIT-LOG-PERSISTENCE.md` (audit_log table and optional DB write for P1-3).
- **Data export/delete:** `CareLoop/docs/DATA-EXPORT-AND-DELETION.md` (retention, export, deletion, consent for P1-11).
- **Operations runbook:** `CareLoop/docs/OPERATIONS-RUNBOOK.md` (env, health, audit, feedback, export/delete, monitoring, Phase 3→4).
- **Gateway shadow:** `CareLoop/docs/GATEWAY-SHADOW-DESIGN.md` (P2 gateway envelope, shadow/canary/GA, canary checklist).
- **Phase 4 pilot:** `CareLoop/docs/PHASE4-PILOT-CHECKLIST.md` (pillar test matrix, SLO, benchmark, load test, rollout).
- **Pillar matrix execution:** `CareLoop/docs/PILLAR-TEST-MATRIX-EXECUTION.md` (case format, assertions per pillar, manual/script run).
- **Model-tier router:** `CareLoop/docs/MODEL-TIER-ROUTER-DESIGN.md` (P2-8 design: tiers, selection, pass-through, safety).
- **Background jobs:** `CareLoop/docs/BACKGROUND-JOBS-DESIGN.md` (P2-9); `scripts/corpus-freshness-check.js`, `scripts/retrieval-regression-smoke.js`, `scripts/retrieval-regression-runner.js`, `scripts/fixtures/retrieval-cases.json`; `npm run job:corpus-freshness`, `npm run job:retrieval-smoke`, `npm run job:retrieval-regression`.
- **Routing and intent:** `CareLoop/docs/ROUTING-AND-INTENT-DESIGN.md` (decision layers: intent in workflow, model tier in gateway, fallback in API; improvement path for intent router).
- **Two workflows:** `CareLoop/docs/TWO-WORKFLOWS-AND-MODE-SWITCH.md` (simple + full pipeline, frontend mode switch, gateway-handled modes).