# Phase 3 -> Phase 4: Next Week Execution Plan

Execution window: 7 working days  
Goal: close remaining Phase 3 production-readiness gaps and start Phase 4 validation with auditable evidence.

---

## 0) Exit Criteria for This Week

- [ ] Gateway rollout evidence recorded for real traffic slices (`10% -> 50% -> 100%`) with gate checks passing at each stage.
- [ ] Monitoring queries and alert rules are wired in the monitoring platform and at least one warning + one critical test notification are verified.
- [ ] Phase 4 matrix kickoff completed with first 40 cases (`policy_navigation`) and no critical grounding failures.
- [ ] Updated status reflected in:
  - `docs/PHASE3-TODO.md`
  - `docs/PHASE4-PILOT-CHECKLIST.md`
  - `ROADMAP.md` (if DoD status changes)

---

## 1) Day-by-Day Plan

## Day 1 - Baseline + Environment Lock

### Tasks
- Freeze release candidate (code + workflow version) for this execution window.
- Ensure active workflows are only:
  - `careloop-turn`
  - `careloop-turn-simple`
- Capture fresh direct-path baseline (without gateway as active path).

### Commands (run from `CareLoop/`)
```bash
BASELINE_REQUESTS=100 BASELINE_CONCURRENCY=10 npm run job:gateway-baseline-capture
```

### Pass/Fail
- Pass: baseline output includes `BASELINE_P95_MS` and `BASELINE_5XX_RATE`.
- Fail: baseline capture fails, or sample volume is insufficient (<100).

### Evidence to save
- Baseline command output in release notes / ops log.
- Baseline values copied into rollout worksheet:
  - `BASELINE_P95_MS=<value>`
  - `BASELINE_5XX_RATE=<value>`

---

## Day 2 - 10% Real Canary

### Tasks
- Route 10% real traffic to gateway.
- Run canary gate checks for the same observation window.

### Commands
```bash
GATEWAY_SHADOW_LOG=./logs/gateway-shadow.jsonl \
BASELINE_P95_MS=<from-day1> \
BASELINE_5XX_RATE=<from-day1> \
MIN_REQUESTS=20 \
npm run job:gateway-canary-check
```

### Pass/Fail
- Pass:
  - `status=ok`
  - `5xx=0` (or not worse than defined gate)
  - no invalid envelopes
  - no increase in error-envelope rate beyond gate threshold
- Fail: any gate failure or `status!=ok`.

### Evidence to save
- Gate output JSON/result.
- One Production Rollout Record entry (`10%`) in `docs/OPERATIONS-RUNBOOK.md` template section.

---

## Day 3 - 50% Rollout + Citation Coverage Guard

### Tasks
- Increase gateway traffic share to 50%.
- Run canary gate check with higher sample requirement.
- Run policy citation coverage diff (baseline vs canary audit).

### Commands
```bash
GATEWAY_SHADOW_LOG=./logs/gateway-shadow.jsonl \
BASELINE_P95_MS=<from-day1> \
BASELINE_5XX_RATE=<from-day1> \
MIN_REQUESTS=50 \
BASELINE_AUDIT_LOG_PATH=./logs/audit.baseline.policy.40.jsonl \
CANARY_AUDIT_LOG_PATH=./logs/audit.canary.policy.40.jsonl \
MAX_POLICY_CITATION_DROP=0.05 \
npm run job:gateway-canary-check
```

### Pass/Fail
- Pass:
  - gate `status=ok`
  - policy citation coverage drop <= `0.05`
- Fail: gate failure or citation coverage breach.

### Evidence to save
- Gate output for 50% stage.
- Citation coverage comparison output.
- Rollout Record entry (`50%`).

---

## Day 4 - 100% Gateway Cutover Decision

### Tasks
- If Day 2 and Day 3 are clean, promote to 100% through gateway.
- Re-run gate check on production traffic window.
- Confirm rollback decision path and on-call ownership.

### Commands
```bash
GATEWAY_SHADOW_LOG=./logs/gateway-shadow.jsonl \
BASELINE_P95_MS=<from-day1> \
BASELINE_5XX_RATE=<from-day1> \
MIN_REQUESTS=50 \
npm run job:gateway-canary-check
```

### Pass/Fail
- Pass: all gate metrics remain green at 100%.
- Fail: hold or rollback to previous stable share.

### Evidence to save
- Rollout Record entry (`100%`) with `decision=promote|hold|rollback`.
- Incident note if rollback/hold happens.

---

## Day 5 - Monitoring and Alert Wiring Validation

### Tasks
- Wire dashboard queries from `docs/monitoring/PHASE3-MONITORING-QUERIES.sql`.
- Implement rules from `docs/monitoring/ALERT-RULES.md`.
- Trigger at least one warning and one critical alert in non-prod (or controlled prod window).

### Verification checklist
- [ ] Dashboard panel for end-to-end p95/p99 latency.
- [ ] Dashboard panel for stage p95 (`retrieval`, `verification`, `routing` when available).
- [ ] Alert: health check down condition verified.
- [ ] Alert: latency or error-rate condition verified.
- [ ] Notification channel delivery confirmed.

### Pass/Fail
- Pass: both warning and critical alerts are observed end-to-end.
- Fail: rules exist but no validated notification path.

### Evidence to save
- Screenshot/export of dashboard panels.
- Alert test logs with timestamps and delivery proof.

---

## Day 6 - Phase 4 Kickoff: Policy Navigation Matrix (40 cases)

### Tasks
- Execute first mandatory pillar batch:
  - `policy_navigation` 40 cases
- Record assertions per `docs/PILLAR-TEST-MATRIX-EXECUTION.md`.

### Recommended run mode
- Start with manual + script-assisted hybrid:
  - scripted invocation
  - manual audit on failed/suspicious cases

### Pass/Fail
- Pass:
  - 40/40 executed
  - no critical grounding failure
  - citation coverage remains 100% for policy claims
- Fail: any critical ungrounded policy assertion.

### Evidence to save
- Result artifact under `docs/reports/` (JSON or markdown).
- Failure triage notes (if any).

---

## Day 7 - Consolidation + Status Sync

### Tasks
- Consolidate week evidence and outcomes.
- Update official progress docs:
  - `docs/PHASE3-TODO.md`
  - `docs/PHASE4-PILOT-CHECKLIST.md`
  - `ROADMAP.md` (only if DoD state changed)
- Decide next sprint focus:
  - remaining pillar matrix (`emotional_support`, `practical_education`, `mixed`)
  - load test (`>=100` concurrent)
  - benchmark audit finalization

### Pass/Fail
- Pass: documents reflect actual verified state and next actions are explicit.
- Fail: implementation moved but status docs remain stale.

---

## 2) Operational Guardrails (Do Not Skip)

- Never promote rollout stage without completing the previous stage gate.
- Treat any critical grounding failure as release-blocking.
- Keep canary window logs immutable for traceability.
- Use `request_id` and `session_id` for incident reconstruction.
- If uncertain, prefer `hold` over `promote`.

---

## 3) Quick Command Pack

Run from `CareLoop/`:

```bash
# Day 1 baseline
BASELINE_REQUESTS=100 BASELINE_CONCURRENCY=10 npm run job:gateway-baseline-capture

# Canary gate check (parameterized)
GATEWAY_SHADOW_LOG=./logs/gateway-shadow.jsonl \
BASELINE_P95_MS=<value> \
BASELINE_5XX_RATE=<value> \
MIN_REQUESTS=50 \
npm run job:gateway-canary-check

# Canary gate with citation coverage diff
GATEWAY_SHADOW_LOG=./logs/gateway-shadow.jsonl \
BASELINE_P95_MS=<value> \
BASELINE_5XX_RATE=<value> \
MIN_REQUESTS=50 \
BASELINE_AUDIT_LOG_PATH=./logs/audit.baseline.policy.40.jsonl \
CANARY_AUDIT_LOG_PATH=./logs/audit.canary.policy.40.jsonl \
MAX_POLICY_CITATION_DROP=0.05 \
npm run job:gateway-canary-check
```

---

## 4) References

- `docs/OPERATIONS-RUNBOOK.md`
- `docs/PHASE3-TODO.md`
- `docs/PHASE4-PILOT-CHECKLIST.md`
- `docs/PILLAR-TEST-MATRIX-EXECUTION.md`
- `docs/SLO-AND-MONITORING.md`
- `docs/monitoring/PHASE3-MONITORING-QUERIES.sql`
- `docs/monitoring/ALERT-RULES.md`
- `ROADMAP.md`
