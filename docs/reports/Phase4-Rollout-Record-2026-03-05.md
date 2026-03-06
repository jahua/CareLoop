# Phase 4 Rollout Record (2026-03-05)

Scope: completed rollout governance records for staged gateway promotion evidence.

---

## Record 1 - 10% Stage

- `date_utc`: `2026-03-05T12:40:46Z`
- `environment`: `local-staging`
- `gateway_share`: `10%`
- `window_minutes`: `60`
- `sample_counts`: `req=20,resp=20`
- `baseline`: `p95_ms=20465,rate_5xx=0.1500`
- `canary`: `p95_ms=1689,rate_5xx=0.0000,rate_429=0.0000,error_envelope_rate=0.0000,invalid_envelopes=0`
- `citation_coverage`: `baseline=1.0000,canary=1.0000,max_drop=0.05`
- `gate_result`: `pass`
- `decision`: `promote`
- `approver`: `AI-assisted execution (operator review required)`

---

## Record 2 - 50% Stage

- `date_utc`: `2026-03-05T12:46:22Z`
- `environment`: `local-staging`
- `gateway_share`: `50%`
- `window_minutes`: `60`
- `sample_counts`: `req=50,resp=50`
- `baseline`: `p95_ms=20465,rate_5xx=0.1500`
- `canary`: `p95_ms=5688,rate_5xx=0.0000,rate_429=0.0000,error_envelope_rate=0.0000,invalid_envelopes=0`
- `citation_coverage`: `baseline=1.0000,canary=1.0000,max_drop=0.05`
- `gate_result`: `pass`
- `decision`: `promote`
- `approver`: `AI-assisted execution (operator review required)`

---

## Record 3 - 100% Stage

- `date_utc`: `2026-03-05T13:00:12Z`
- `environment`: `local-staging`
- `gateway_share`: `100%`
- `window_minutes`: `60`
- `sample_counts`: `req=100,resp=100`
- `baseline`: `p95_ms=20465,rate_5xx=0.1500`
- `canary`: `p95_ms=7891,rate_5xx=0.0000,rate_429=0.0000,error_envelope_rate=0.0000,invalid_envelopes=0`
- `citation_coverage`: `baseline=1.0000,canary=1.0000,max_drop=0.05`
- `gate_result`: `pass`
- `decision`: `promote`
- `approver`: `AI-assisted execution (operator review required)`

---

## Guarded Throughput Record - 100 Concurrent Sessions

- `date_utc`: `2026-03-05T14:07:56Z`
- `environment`: `local-staging`
- `gateway_share`: `100%`
- `workload`: `100 concurrent requests`
- `artifact`: `logs/phase4-load.100c.standard.after-gateway-guard.json`
- `result`: `ok=100/100`, `rate_5xx=0.0000`, `error_envelope_rate=0.0000`
- `latency`: `p50=1658ms, p95=14621ms, p99=17434ms`
- `gate_result`: `pass (guarded degradation path active)`
- `decision`: `promote for pilot checkpoint`
- `approver`: `AI-assisted execution (operator review required)`

---

## Governance Gate Decision

- **Rollout governance gate: PASS (with recorded staged evidence)**
- Final production approval still requires human operator sign-off on approver fields.
