# Phase 3: Reliability, Observability, and Security (Implementation Report)

**CareLoop Development Report**  
**Version:** 1.0  
**Status:** In progress (core DoD met)  
**Scope:** Weeks 11–13 per ROADMAP §6

---

## 1. Introduction

Phase 3 strengthens the CareLoop system with structured failure handling, observability, and privacy-aware logging. All client-facing failure paths now return a consistent error envelope; audit and correlation IDs support tracing; optional feedback and health checks support quality and availability monitoring; and redaction and security documentation align with the technical specification and Swiss FADP considerations.

---

## 2. Implemented Deliverables

### 2.1 Structured Error Envelope (P0-1, P0-2)

- **Contracts:** `packages/contracts/src/errors.ts` defines `ERROR_CODES`, `StructuredErrorSchema`, `ErrorResponseEnvelopeSchema`, and parse helpers. All failure responses use a stable `error_code`, `message`, optional `stage`, `retryable`, and `request_id`/`session_id`.
- **API:** Chat and EMA routes return `ErrorResponseEnvelope` on every error path (timeout, upstream error, validation failure). No raw stack traces or upstream bodies are exposed to clients.
- **Normalization:** When N8N returns 200 with `success: false` and an `error` object, or when the response is malformed (missing `session_id` or `message.content`), the chat API converts to the shared envelope and returns 503 or appropriate status.
- **N8N workflow:** All Code nodes (Merge, Detection, Regulation, Merge Retrieval, Generation, Grounding, Verification, Format Response) pass through when `success === false && error`; Format Response also emits a `verifier_fallback` envelope when required fields are missing. See `docs/WORKFLOW-ERROR-ENVELOPE.md`.
- **Frontend:** Error display reads `error.message` from the envelope (supports both legacy `{ error: string }` and new shape).

### 2.2 Correlation IDs and Audit (P1-3)

- **request_id:** Generated or accepted (body or `x-request-id`) in the chat API, passed to the N8N workflow, carried through Ingest and Format Response, and included in error responses. Enables tracing frontend → API → workflow → response.
- **Audit JSONL:** When `AUDIT_LOG_PATH` is set, one JSONL line is appended per successful turn. Each line includes `request_id`, `session_id`, `turn_index`, `coaching_mode`, `pipeline_status`, personality summary, `retrieval_ids`/`citation_count`, `verifier_status`, `timestamp`, optional `input_hash` (SHA-256 truncated, no PII), and `turn_latency_ms` (API-side). No user message content is logged (`apps/web/src/lib/audit.ts`).
- **Audit DB (optional):** When `AUDIT_DB_WRITE=true` and `AUDIT_DATABASE_URL` (or `DATABASE_URL`) is set, each turn is also written to the `audit_log` table via `apps/web/src/lib/audit-db.ts` (fire-and-forget). Table and schema are in `infra/database/init.sql`; see `docs/AUDIT-LOG-PERSISTENCE.md`.

### 2.3 Optional Feedback (P1-5, DoD 3)

- **POST /api/feedback:** Accepts `session_id`, optional `turn_index`/`request_id`, and at least one of `thumbs_up_down` ('up'|'down') or `helpfulness_score` (0–5). Appends one JSONL line when `FEEDBACK_LOG_PATH` is set; returns 202 Accepted.
- **UI:** Chat page shows thumbs up/down per assistant message (when `turn_index`/`request_id` are present). Submitting feedback disables the buttons and highlights the selection; duplicate submissions are avoided.

### 2.4 Redaction and Pseudonymization (P1-4)

- **Policy:** Audit and feedback logs use only pseudonymous identifiers; no user message or other PII in persistent logs.
- **Helper:** `apps/web/src/lib/redact.ts` provides `redactForLog(text)` to redact email and phone patterns before any future free-text logging.
- **Docs:** `docs/PRIVACY-AND-REDACTION.md` documents the logging policy and use of the redaction helper.

### 2.5 Health and SLO Documentation (P1-10)

- **GET /api/health:** Returns `{ ok: true, service: "careloop-web", timestamp }` for availability checks (load balancer, uptime monitoring).
- **Turn latency:** Each audit line (file or `audit_log`) includes `turn_latency_ms` for p95/p99 and SLO (e.g. end-to-end ≤ 2s).
- **Docs:** `docs/SLO-AND-MONITORING.md` lists target SLOs, where metrics come from (health, audit/audit_log), and recommended alert thresholds (health down, latency p95/p99, error rate, retrieval/verification timeouts). Stage-level instrumentation in the workflow and wiring to `performance_metrics` remain optional.

### 2.6 Security and Privacy Documentation (P1-11)

- **Docs:** `docs/SECURITY-AND-PRIVACY.md` summarizes Spec §17.4: secrets in env only, least privilege, no raw errors to clients, redaction/pseudonymization (with links to PRIVACY-AND-REDACTION and SECRETS-AND-CREDENTIALS), retention/deletion, consent for personality profiling, and data export/delete. It includes an "Access paths (deployed services)" table (Next.js, N8N, DB, future gateway).
- **Export/delete and retention:** `docs/DATA-EXPORT-AND-DELETION.md` defines retention defaults, export and deletion contracts, consent for profiling, and deletion order. GET /api/data/export and POST /api/data/delete are implemented: when DATABASE_URL (or AUDIT_DATABASE_URL) is set, they export session data or delete by session_id in the correct order. Optional auth via DATA_API_KEY (x-api-key or Authorization header).

### 2.7 P2 Gateway (shadow, auth, rate limit, model_tier)

- **Design:** `docs/GATEWAY-SHADOW-DESIGN.md` – gateway envelope, shadow/canary/GA rollout, success gate, canary checklist.
- **Route:** `POST /api/gateway/chat` accepts the gateway envelope (`request_id`, `session_id`, `user_id?`, `message`, `context?`, `routing_hints?`), optionally logs to `GATEWAY_SHADOW_LOG`, then forwards to `/api/chat`. Optional auth: `GATEWAY_API_KEY` (x-api-key or Bearer). Optional rate limit: `GATEWAY_RATE_LIMIT_PER_MINUTE` (per user_id or IP); 429 + Retry-After when exceeded; `X-RateLimit-Remaining` on success. Implementation: `apps/web/src/lib/gateway-shadow.ts`, `apps/web/src/lib/gateway-rate-limit.ts`, `apps/web/src/app/api/gateway/chat/route.ts`.
- **Model tier:** `routing_hints.model_tier` (`light`|`medium`|`heavy`) is passed through; gateway sets `context.model_tier` (default `medium`) on the body forwarded to `/api/chat`, so N8N can consume it for params when implemented.
- **Canary automation:** Added `scripts/gateway-canary-check.js` (`npm run job:gateway-canary-check`) to enforce canary gates from shadow logs (5xx drift, p95 drift, 429, error-envelope rate, envelope validity, optional policy citation coverage diff).
- **Baseline automation:** Added `scripts/gateway-baseline-capture.js` (`npm run job:gateway-baseline-capture`) to derive `BASELINE_P95_MS` and `BASELINE_5XX_RATE` from direct `/api/chat` traffic before canary.
- **Validation run (2026-03-05):** Baseline capture with 100 direct requests produced `BASELINE_P95_MS=4609`, `BASELINE_5XX_RATE=0`. Canary run with 30 gateway requests passed gate checks (`status=ok`): request/response volume met (`req=30`, `resp=30`), `error_rate_5xx=0`, `p95=330ms`, `rate_429=0`, `error_envelope_rate=0`, and `invalid_envelopes=0`.
- **High-sample gate run (2026-03-05):** Additional canary with 100 gateway requests also passed (`status=ok`) under stricter sample threshold (`MIN_REQUESTS=50`): `req=100`, `resp=100`, `p95=327ms`, `error_rate_5xx=0`, `rate_429=0`, `error_envelope_rate=0`, `invalid_envelopes=0`.
- **Citation coverage diff (2026-03-05):** Full gate check with audit comparison also passed using policy-intent samples (`baseline_audit=40`, `canary_audit=40`): `policy_citation_coverage baseline=1.0000, canary=1.0000, max_drop=0.05`.
- **Workflow cleanup (2026-03-05):** Cleaned the active N8N set and ensured only the two intended webhook workflows remain operational for mode routing: full pipeline (`careloop-turn`) and simple mode (`careloop-turn-simple`).
- **50/50 split drill (2026-03-05):** Simulated a traffic-slice rollout window with 100 direct requests and 100 gateway requests. Gateway half passed with strict gate threshold (`MIN_REQUESTS=50`): `req=100`, `resp=100`, `p95=837ms`, `error_rate_5xx=0`, `rate_429=0`, `error_envelope_rate=0`, `invalid_envelopes=0`; citation coverage guard remained stable (`baseline=1.0000`, `canary=1.0000`).
- **10% stage drill (2026-03-05):** Simulated `10%` canary stage with 180 direct requests and 20 gateway requests. Using a fresh baseline (`BASELINE_P95_MS=5838`, `BASELINE_5XX_RATE=0`), gateway gate check passed (`MIN_REQUESTS=20`): `req=20`, `resp=20`, `p95=4473ms`, `error_rate_5xx=0`, `rate_429=0`, `error_envelope_rate=0`, `invalid_envelopes=0`; citation coverage guard remained stable (`baseline=1.0000`, `canary=1.0000`).

### 2.8 P2 Model-tier router (implementation in progress)

- **Design:** `docs/MODEL-TIER-ROUTER-DESIGN.md` – tier definitions (light/medium/heavy), selection from routing_hints or intent, pass-through to pipeline, safety rule (no skip of grounding/verification for policy-relevant turns), observability.
- **Workflow consumption implemented:** `workflows/n8n/careloop-phase1-2-postgres-mvp.json` now consumes `context.model_tier`:
  - Ingest validates tier and defaults to `medium`.
  - Regulation applies safety escalation (`policy_navigation`/`mixed` + `light` ⇒ `medium`) and emits `model_tier_requested`, `model_tier_effective`, `retrieval_top_k`.
  - Retrieval query uses dynamic top-k (`LIMIT {{ $json.retrieval_top_k || 3 }}`).
  - Generation applies tier-aware `max_tokens`/`temperature` and records the applied tier in `generation_config`.
- **Remaining:** benchmark-driven tuning of tier thresholds and heavy-tier triggers for ambiguous policy turns.

### 2.10 Routing, Intent, and Mode Design

- **Design:** `docs/ROUTING-AND-INTENT-DESIGN.md` — canonical reference for which layer owns which routing decision:
  - **Intent / pillar mode** (`coaching_mode`): authoritative in the **N8N workflow** (after detection + EMA). Now upgraded toward Spec §8.4.F with normalized thresholds, tie-break rules, and low-confidence clarification metadata.
  - **Model tier** (`light`/`medium`/`heavy`): owned by the **Gateway**, derived from `routing_hints.model_tier`; workflow may escalate for safety.
  - **Workflow selection** (simple vs full): owned by the **Gateway**, derived from tier or explicit `routing_hints.workflow`.
  - **API fallback**: `inferCoachingModeFallback()` in `apps/web/src/app/api/chat/route.ts` — fires only when workflow omits `coaching_mode`.
- **Code:** Renamed `inferCoachingMode` → `inferCoachingModeFallback` with explicit docstring marking it as non-authoritative.
- **Workflow implementation update:** `workflows/n8n/careloop-phase1-2-postgres-mvp.json` (`Enhanced Regulation`) now emits `mode_scores_raw`, normalized `mode_scores`, `needs_clarifying_question`, `clarifying_question`, and `mode_routing_reason`.
- **Cross-references:** Updated `GATEWAY-SHADOW-DESIGN.md`, `MODEL-TIER-ROUTER-DESIGN.md`, `TWO-WORKFLOWS-AND-MODE-SWITCH.md` to reference the canonical doc.

### 2.9 P2 Background jobs (design + corpus freshness)

- **Design:** `docs/BACKGROUND-JOBS-DESIGN.md` – job types (corpus freshness, recrawl/re-embedding, stale citation detector, retrieval regression), telemetry shape (JSONL with stage=background_job), scheduling.
- **Corpus freshness:** `scripts/corpus-freshness-check.js`; run with `npm run job:corpus-freshness`. Connects to DB, counts `policy_chunks`, optional `MIN(created_at)`; writes one JSONL line to `BACKGROUND_JOB_LOG_PATH` or stdout. Env: `DATABASE_URL`, `BACKGROUND_JOB_LOG_PATH`, `CORPUS_FAIL_ON_EMPTY`. Exit 0 on success, 1 on DB error or empty corpus (when `CORPUS_FAIL_ON_EMPTY` is not disabled).
- **Source recrawl / re-embedding baseline:** `scripts/source-recrawl-reembed.js`; run with `npm run job:source-recrawl`. Compares source content hashes from fetched documents against DB metadata, reports changed sources in dry-run (default), and in apply mode (`SOURCE_RECRAWL_DRY_RUN=0`) replaces chunks for changed sources.
- **Stale citation detector:** `scripts/stale-citation-detector.js`; run with `npm run job:stale-citation`. Checks distinct `policy_chunks.url` with HEAD and optional GET fallback, emits `checked_count`, `stale_count`, `stale_ratio`, and `stale_samples` telemetry. Supports tuning via `STALE_CITATION_MAX_URLS`, `STALE_CITATION_TIMEOUT_MS`, `STALE_CITATION_FAIL_THRESHOLD`, `STALE_CITATION_ALLOW_GET_FALLBACK`.
- **Regression hardening update (2026-03-05):** `scripts/retrieval-regression-runner.js` now supports case-level routing assertions (`require_policy_mode`, `expected_coaching_mode`, `min_citations`) to catch policy-intent misrouting. New fixture cases were added in `scripts/fixtures/retrieval-cases.json`.
- **Router + runner follow-up (2026-03-05):** The `Enhanced Regulation` node in `workflows/n8n/careloop-phase1-2-postgres-mvp.json` was tuned to strengthen explicit policy-intent routing (expanded policy cues and adjusted policy/mixed thresholds). Regression citation parsing was fixed to include `policy_navigation.citations`. Result: `npm run job:retrieval-regression -- scripts/fixtures/retrieval-cases.json` passed `5/5` (`status=ok`).

---

## 3. Phase 3 Definition of Done (Current Status)

| DoD | Status | Notes |
|-----|--------|--------|
| DoD 1: All failure paths return structured responses | Done | ErrorResponseEnvelope in chat/EMA; N8N error/malformed responses normalized. |
| DoD 2: Audit JSONL and correlation IDs | Done | request_id end-to-end; AUDIT_LOG_PATH JSONL per turn. |
| DoD 3: Optional feedback captured | Done | POST /api/feedback + thumbs UI; FEEDBACK_LOG_PATH. |
| DoD 4: Gateway rollout (if enabled) | In progress | Gateway stub + shadow log, optional auth and rate limit, model_tier pass-through; baseline + 30-sample + 100-sample canary gates passed on 2026-03-05, and policy citation coverage diff gate passed. Remaining work is production traffic-slice rollout execution (10% -> 50% -> 100%) before GA. |

---

## 4. Remaining Work (from PHASE3-TODO)

- **P0 (optional):** EMA divergence detection and explicit `ema_divergence` handling in workflow; mixed-mode token overflow and language fallback handling.
- **P1-10:** Workflow now emits `stage_timings` with per-stage durations (`detection`, `routing`, `retrieval`, `generation`, `grounding`, `verification`) plus `end_to_end`, and API persists them to `performance_metrics`. Remaining: connect monitoring stack dashboards/alerts to these metrics. See §6 below and `docs/SLO-AND-MONITORING.md`.
- **P2-8:** N8N consumption of `context.model_tier` for params (e.g. max_tokens); design is in MODEL-TIER-ROUTER-DESIGN.md.
- **P2-9:** Retrieval regression script, stale citation detector, optional re-embedding job; design and corpus-freshness script done.

## 5. Transition to Phase 4

- **Operations runbook:** `docs/OPERATIONS-RUNBOOK.md` covers env, health, audit, feedback, export/delete, gateway env, monitoring, incidents, and Phase 3 → 4 / P2 notes.
- **When introducing a gateway (P2):** Deploy in shadow mode first; use canary checklist in GATEWAY-SHADOW-DESIGN §6; then canary and GA with success gate (no critical hallucination increase, stable or better benchmarks) per Spec §15.1.G.
- **Phase 4 pilot:** `docs/PHASE4-PILOT-CHECKLIST.md` and `docs/PILLAR-TEST-MATRIX-EXECUTION.md` for pillar test matrix, SLO, benchmark audit, load test, rollout.

## 6. Stage latency and performance_metrics (P1-10 follow-up)

- **Current:** End-to-end turn latency is recorded as `turn_latency_ms` in each audit line (file and optional `audit_log` table). This is the primary latency signal for SLO (e.g. p95 ≤ 2s).
- **Future:** To get per-stage latency (routing, retrieval, verification), the N8N workflow can emit one row per stage into `performance_metrics` per turn. Table schema: `(session_id, turn_index, stage, status, duration_ms, error_code, created_at)` with FK to `conversation_turns`. Workflow would need to record timestamps at each stage and either (a) call a small HTTP endpoint that inserts into `performance_metrics`, or (b) include stage timings in the final webhook response so the API can write them. Until then, alerts rely on `turn_latency_ms` and health checks; see `docs/SLO-AND-MONITORING.md`.

---

## 7. References

- **ROADMAP:** `CareLoop/ROADMAP.md` §6 (Phase 3), §7 (Phase 4).
- **TODO:** `CareLoop/docs/PHASE3-TODO.md`.
- **Runbook:** `CareLoop/docs/OPERATIONS-RUNBOOK.md`.
- **Gateway:** `CareLoop/docs/GATEWAY-SHADOW-DESIGN.md`.
- **Model-tier:** `CareLoop/docs/MODEL-TIER-ROUTER-DESIGN.md`.
- **Background jobs:** `CareLoop/docs/BACKGROUND-JOBS-DESIGN.md`.
- **Routing and intent:** `CareLoop/docs/ROUTING-AND-INTENT-DESIGN.md`.
- **Two workflows:** `CareLoop/docs/TWO-WORKFLOWS-AND-MODE-SWITCH.md`.
- **Phase 4:** `CareLoop/docs/PHASE4-PILOT-CHECKLIST.md`, `CareLoop/docs/PILLAR-TEST-MATRIX-EXECUTION.md`.
- **Spec:** `CareLoop/Technical-Specification-RAG-Policy-Navigation.md` §11–12, §15.1, §17.4, §17.6.

---

**Document Control**  
Last Updated: 2026-03-05
