# Phase 3 Alert Rules (P1-10)

Operational alert mappings for the current CareLoop stack, based on `audit_log` and `performance_metrics`.

Use together with:

- `docs/monitoring/PHASE3-MONITORING-QUERIES.sql`
- `docs/SLO-AND-MONITORING.md`
- `docs/OPERATIONS-RUNBOOK.md` (incidents/rollback)

---

## 1. Severity model

- `warning`: degraded performance or elevated risk; investigate in business hours.
- `critical`: user-visible impact or likely SLO breach; page on-call immediately.

---

## 2. Core alert rules

| Alert ID | Metric | Window | Trigger | Severity | First response |
|---|---|---|---|---|---|
| `health_down` | `/api/health` success | 2 checks | 2 consecutive failures | critical | Check web process, then N8N and DB reachability. |
| `turn_latency_p95_high` | `audit_log.turn_latency_ms` p95 | 5 min | `> 2000ms` | warning | Inspect N8N execution times and DB slow queries. |
| `turn_latency_p99_high` | `audit_log.turn_latency_ms` p99 | 5 min | `> 5000ms` | critical | Check queue/backlog, upstream timeouts, and fallback rate. |
| `retrieval_timeout_breach` | `performance_metrics` retrieval breach rate | 15 min | `duration_ms > 2000ms` in `>= 5%` samples | warning | Validate retrieval stage status/errors; inspect `policy_chunks` and query load. |
| `verification_timeout_breach` | `performance_metrics` verification breach rate | 15 min | `duration_ms > 1500ms` in `>= 5%` samples | warning | Inspect verifier stage status/errors and model latency. |
| `stage_fail_rate_high` | `performance_metrics` stage hard-fail rate | 15 min | hard-fail rate `>= 2%` | warning | Check top `error_code` and affected stage. |
| `stage_fail_rate_critical` | `performance_metrics` stage hard-fail rate | 15 min | hard-fail rate `>= 5%` | critical | Trigger incident, consider rollback if sustained. |
| `stage_fallback_rate_high` | `performance_metrics` stage fallback rate | 15 min | fallback rate `>= 50%` | warning | Validate detector/generator upstream health and fallback root cause. |
| `citation_coverage_drop` | policy citation coverage | 30 min | `< 98%` for policy turns | warning | Inspect retrieval evidence count and routing mode distribution. |
| `citation_coverage_critical` | policy citation coverage | 30 min | `< 95%` for policy turns | critical | Stop promotion/canary; investigate corpus and routing immediately. |

---

## 3. Query-to-alert mapping

- `turn_latency_p95_high` / `turn_latency_p99_high`
  - Use query **#1** from `PHASE3-MONITORING-QUERIES.sql`.
- `stage_fail_rate_high` / `stage_fail_rate_critical`
  - Use query **#3** and optionally **#7** for diagnosis.
- `stage_fallback_rate_high`
  - Use query **#3b**.
- `retrieval_timeout_breach`
  - Use query **#4**.
- `verification_timeout_breach`
  - Use query **#5**.
- `citation_coverage_drop` / `citation_coverage_critical`
  - Use query **#6**.

---

## 4. Notification routing (recommended)

- `warning`:
  - Slack/Teams ops channel
  - ticket auto-created if alert lasts > 30 min
- `critical`:
  - Pager/on-call phone + Slack/Teams incident channel
  - incident owner assigned within 10 minutes

---

## 5. Promotion gates (gateway rollout)

For canary promotion (`10% -> 50% -> 100%`), require all below:

- No `critical` alerts in previous 60 minutes.
- `turn_latency_p95_high` not firing continuously for > 30 minutes.
- `citation_coverage_drop` not firing.
- Gateway canary check remains `status=ok`.

If any `critical` fires during canary window:

1. Hold promotion immediately.
2. Execute rollback/hold decision in rollout record.
3. Re-run gate checks after mitigation.

---

## 6. Notes for current stack

- In current local/staging workflow, `detection` and `generation` may legitimately report `status='fallback'`.
- `fallback` is treated as degradation, not hard failure, in alert logic.
- Track fallback trend with `stage_fallback_rate_high`; use hard-fail alerts for true breakages.
