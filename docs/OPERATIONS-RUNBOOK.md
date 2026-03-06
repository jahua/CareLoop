# CareLoop Operations Runbook

Short reference for running and operating the CareLoop stack. See `.env.example` and the linked docs for full configuration.

---

## 1. Environment and startup

- **Copy env:** `cp .env.example .env` and set values (never commit `.env`). See [SECRETS-AND-CREDENTIALS.md](SECRETS-AND-CREDENTIALS.md).
- **Stack:** Start PostgreSQL, N8N, and (optionally) LLM endpoint. Next.js app uses `N8N_WEBHOOK_URL` to proxy chat to the workflow.
- **Workflow:** Import and activate `workflows/n8n/careloop-phase1-2-postgres-mvp.json` in N8N; webhook path is `careloop-turn`.
- **DB schema:** Run `infra/database/init.sql` once (e.g. on first deploy or via migration). Policy seed: `npm run seed:policy` if `policy_chunks` is empty.

---

## 2. Health and availability

- **Probe:** `GET /api/health` → `{ ok: true, service: "careloop-web", timestamp }`. Use for load balancer or uptime checks.
- **If health fails:** Check that the Next.js app is running; if chat fails, verify N8N is up and the workflow is active, and that PostgreSQL is reachable from N8N.

---

## 3. Audit and feedback logs

- **Audit (file):** Set `AUDIT_LOG_PATH` (e.g. `./logs/audit.jsonl`). One JSONL line per successful turn; includes `request_id`, `session_id`, `turn_index`, `coaching_mode`, `pipeline_status`, `turn_latency_ms`, etc. No user message content.
- **Audit (DB):** Set `AUDIT_DB_WRITE=true` and `AUDIT_DATABASE_URL` (or `DATABASE_URL`). Same payload is written to `audit_log` table. Ensure `audit_log` exists (from `init.sql`).
- **Feedback:** Set `FEEDBACK_LOG_PATH`; `POST /api/feedback` appends one JSONL line per submission.
- **Retention:** Define retention for audit and feedback files/DB per [DATA-EXPORT-AND-DELETION.md](DATA-EXPORT-AND-DELETION.md) and your compliance policy.

---

## 4. Data export and deletion (P1-11)

- **Export:** `GET /api/data/export?session_id=<uuid>`. Returns session, turns, personality_states, policy_evidence. Requires `DATABASE_URL` (or `AUDIT_DATABASE_URL`). If `DATA_API_KEY` is set, send `x-api-key` or `Authorization: Bearer <key>`.
- **Delete:** `POST /api/data/delete` with body `{ "session_id": "<uuid>" }`. Deletes all data for that session in the correct order (policy_evidence → personality_states → performance_metrics → conversation_turns → audit_log → chat_sessions). Same env and optional auth as export.
- **Production:** Set `DATA_API_KEY` and restrict who can call these endpoints; consider rate limits and audit logging of delete requests.

---

## 5. Monitoring and alerts

- **SLO and thresholds:** See [SLO-AND-MONITORING.md](SLO-AND-MONITORING.md) (health, turn latency p95/p99, error rate, retrieval/verification timeouts).
- **Alert routing/severity:** See [monitoring/ALERT-RULES.md](monitoring/ALERT-RULES.md) for warning/critical rules, query mappings, and notification policy.
- **Turn latency:** Use `turn_latency_ms` from audit file or `audit_log` for dashboards and alerts (e.g. p95 &gt; 2s warning).
- **Correlation:** Use `request_id` and `session_id` from audit and error responses for tracing.

---

## 6. Incidents and rollback

- **Chat returns 503 or error envelope:** Check N8N workflow is active and DB/LLM are reachable; inspect workflow execution logs and API logs for `request_id`.
- **Rollback:** Revert app/workflow deploy; DB schema is backward-compatible for the current Phase. If a new workflow version is incompatible, re-import the previous workflow JSON and reactivate.

---

## 7. Phase 3 → Phase 4 / P2

- **Phase 3 DoD 1–3** are met (error envelope, audit, feedback, export/delete, security docs). **DoD 4** applies only when a gateway is introduced: shadow → canary → GA and success gate (no critical hallucination increase).
- **P2 Gateway (shadow):** `POST /api/gateway/chat` accepts the gateway envelope (`request_id`, `session_id`, `user_id?`, `message`, `context?`, `routing_hints?`), optionally logs it when `GATEWAY_SHADOW_LOG` is set, then forwards to `/api/chat`. See [GATEWAY-SHADOW-DESIGN.md](GATEWAY-SHADOW-DESIGN.md). To use the gateway as the chat entry point, point the frontend to `/api/gateway/chat` instead of `/api/chat`.
- **Gateway env (optional):** `GATEWAY_SHADOW_LOG` (path for envelope JSONL); `GATEWAY_API_KEY` (require x-api-key or Bearer); `GATEWAY_RATE_LIMIT_PER_MINUTE` (per user_id or IP, 0 = off); `NEXT_PUBLIC_APP_URL` (base URL for internal forward to `/api/chat`).
- **Baseline capture:** `npm run job:gateway-baseline-capture` against `/api/chat` (without gateway path) to derive `BASELINE_P95_MS` and `BASELINE_5XX_RATE`.
- **Canary gate check:** `npm run job:gateway-canary-check` (requires `GATEWAY_SHADOW_LOG`, `BASELINE_P95_MS`, `BASELINE_5XX_RATE`; optional audit coverage paths). Script exits non-zero when canary gates fail.
- **Traffic-slice rollout checklist (10% -> 50% -> 100%):**
  1. Capture baseline on direct path (`/api/chat`): `BASELINE_REQUESTS=100 BASELINE_CONCURRENCY=10 npm run job:gateway-baseline-capture`.
  2. Route 10% traffic through gateway, then run gate check on the same window log (`MIN_REQUESTS>=20`).
  3. Route 50% traffic through gateway, then rerun gate check (`MIN_REQUESTS>=50`).
  4. Before 100%, run citation-coverage diff gate with both audit logs:
     - `BASELINE_AUDIT_LOG_PATH=<...> CANARY_AUDIT_LOG_PATH=<...> MAX_POLICY_CITATION_DROP=0.05 npm run job:gateway-canary-check`
  5. Promote to 100% only when all checks remain `status=ok`.
- **N8N workflow hygiene:** Keep only intended workflows active in N8N:
  - `CareLoop Phase1-2 PostgreSQL (Imported from MVP)` (`careloop-turn`)
  - `CareLoop Simple (Quick) Mode` (`careloop-turn-simple`)
  Remove stale duplicates before canary windows to avoid webhook ambiguity.
- **Production Rollout Record (sign-off template):**
  - Use one record per stage (`10%`, `50%`, `100%`) and keep it with release artifacts.
  - Required fields:
    - `date_utc`:
    - `environment`:
    - `gateway_share`:
    - `window_minutes`:
    - `sample_counts`: `req=<...>`, `resp=<...>`
    - `baseline`: `p95_ms=<...>`, `rate_5xx=<...>`
    - `canary`: `p95_ms=<...>`, `rate_5xx=<...>`, `rate_429=<...>`, `error_envelope_rate=<...>`, `invalid_envelopes=<...>`
    - `citation_coverage`: `baseline=<...>`, `canary=<...>`, `max_drop=<...>` (required at least for 50% and 100%)
    - `gate_result`: `pass|fail`
    - `decision`: `promote|hold|rollback`
    - `approver`:
  - Example (copy/paste):
    - `date_utc=2026-03-05T03:00:00Z`
    - `environment=staging`
    - `gateway_share=50%`
    - `window_minutes=60`
    - `sample_counts=req=1200,resp=1198`
    - `baseline=p95_ms=4609,rate_5xx=0.0000`
    - `canary=p95_ms=910,rate_5xx=0.0000,rate_429=0.0000,error_envelope_rate=0.0000,invalid_envelopes=0`
    - `citation_coverage=baseline=1.0000,canary=0.9900,max_drop=0.05`
    - `gate_result=pass`
    - `decision=promote`
    - `approver=<name>`
- **P2 (optional):** Model-tier router ([MODEL-TIER-ROUTER-DESIGN.md](MODEL-TIER-ROUTER-DESIGN.md)), background jobs ([BACKGROUND-JOBS-DESIGN.md](BACKGROUND-JOBS-DESIGN.md)): corpus freshness (`npm run job:corpus-freshness`), source recrawl (`npm run job:source-recrawl`, dry-run by default), stale citation detector (`npm run job:stale-citation`), retrieval smoke (`npm run job:retrieval-smoke`), retrieval regression (`npm run job:retrieval-regression` or with cases file; set `BASE_URL` if needed). Set `BACKGROUND_JOB_LOG_PATH` for job telemetry JSONL. See [PHASE3-TODO.md](PHASE3-TODO.md) and ROADMAP §6–7.
- **Phase 4:** Pilot release, pillar test matrix, load test, rollout and runbook. See ROADMAP §7 and [PHASE4-PILOT-CHECKLIST.md](PHASE4-PILOT-CHECKLIST.md).
- **Next-week execution plan:** Use [PHASE3-4-NEXT-WEEK-EXECUTION-PLAN.md](PHASE3-4-NEXT-WEEK-EXECUTION-PLAN.md) for day-by-day commands, gates, and evidence capture.

---

## References

- [SECRETS-AND-CREDENTIALS.md](SECRETS-AND-CREDENTIALS.md) – Env and credentials
- [SLO-AND-MONITORING.md](SLO-AND-MONITORING.md) – SLOs and alert thresholds
- [monitoring/PHASE3-MONITORING-QUERIES.sql](monitoring/PHASE3-MONITORING-QUERIES.sql) – Dashboard SQL baseline
- [monitoring/ALERT-RULES.md](monitoring/ALERT-RULES.md) – Alert severity and routing
- [DATA-EXPORT-AND-DELETION.md](DATA-EXPORT-AND-DELETION.md) – Export/delete and retention
- [PHASE3-TODO.md](PHASE3-TODO.md) – Phase 3 checklist and P2 items
- [ROUTING-AND-INTENT-DESIGN.md](ROUTING-AND-INTENT-DESIGN.md) – Routing, intent, and mode separation
- [ROADMAP.md](../ROADMAP.md) – Phases and DoD
