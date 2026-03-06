# SLO and Monitoring (Phase 3 P1-10)

Aligned with Technical Specification §15.1.F, §17.6.

## Health check

- **GET /api/health** – Returns `{ ok: true, service: "careloop-web", timestamp }`. Use for:
  - Load balancer or gateway availability checks.
  - Uptime monitoring (target: gateway availability ≥ 99.9% when gateway is in front).

## Target SLOs (from Spec)

| SLO | Target | Notes |
|-----|--------|--------|
| Gateway availability | ≥ 99.9% | When gateway is deployed; health endpoint supports probing. |
| Routing decision latency | p95 ≤ 50ms | From gateway/router; not yet instrumented in current stack. |
| Retrieval timeout | ≤ 2.0s | Enforce in workflow/retrieval node; log to `performance_metrics` when available. |
| Verification timeout | ≤ 1.5s | Enforce in workflow verifier; log to `performance_metrics`. |
| Citation coverage (policy mode) | 100% | Already enforced; audit log and pipeline_status carry this. |

## Where metrics come from

- **Availability:** GET /api/health (and, when present, gateway health).
- **End-to-end turn latency:** Each audit line (file or `audit_log` when AUDIT_DB_WRITE is set) includes `turn_latency_ms`. Use for p95 dashboards and SLO (e.g. target end-to-end ≤ 2s). Parsing audit JSONL or querying `SELECT turn_latency_ms FROM audit_log WHERE created_at > now() - interval '1 hour'` gives a basis for alerts.
- **Stage latency (routing/retrieval/verification):** The chat API persists stage timings when the N8N workflow returns a **stage_timings** array in the response. Each item: `{ stage: string, status: string, duration_ms?: number, error_code?: string }`. The API writes them to `performance_metrics(session_id, turn_index, stage, status, duration_ms, error_code)` (fire-and-forget). Current workflow emits per-stage durations for `detection`, `routing`, `retrieval`, `generation`, `grounding`, `verification`, plus `end_to_end`. Table and FK in `infra/database/init.sql`. Next step: connect dashboards and alert rules to these DB metrics. See Phase3 report §6.
- **Dashboard query pack:** Use `docs/monitoring/PHASE3-MONITORING-QUERIES.sql` as a starter set for dashboards/alerts (p95/p99 latency, stage failure rates, retrieval/verification timeout breaches, citation coverage, top error codes).
- **Alert rule catalog:** Use `docs/monitoring/ALERT-RULES.md` for warning/critical thresholds, query mappings, and notification routing.

## Alert thresholds (recommended)

| Condition | Threshold | Action |
|-----------|------------|--------|
| Health check down | 2 consecutive failures | Page / notify; check N8N and DB. |
| Turn latency p95 | > 2000 ms (2s) | Warning; investigate N8N/LLM/DB. |
| Turn latency p99 | > 5000 ms | Critical; possible timeout or backlog. |
| Error rate (5xx or envelope) | > 1% over 5 min | Warning; check workflow and API logs. |
| Retrieval timeout | > 2.0s (Spec §15.1.F) | Log and optionally emit `rag_fallback`. |
| Verification timeout | > 1.5s (Spec §15.1.F) | Log and optionally emit `verifier_fallback`. |

Configure these in your monitoring stack (e.g. Prometheus + Alertmanager, or cloud alerts on health and log-based metrics). Use `request_id` and `session_id` from audit/error responses for correlation.
