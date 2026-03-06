# Phase 4: Pilot Release Checklist

Pre-pilot checklist aligned with ROADMAP §7 and Technical Specification §17.6. Use this before deploying to real or internal pilot users.

---

## 1. Pillar test matrix (Spec §17.6.2)

Run the minimum test cases per pillar; block release on critical safety or grounding failures.

| Pillar | Minimum cases | Mandatory assertions |
|--------|----------------|----------------------|
| **emotional_support** | 30 | Tone-fit ≥ target; no unsupported policy claims |
| **practical_education** | 30 | Plan steps present when requested; personality style applied |
| **policy_navigation** | 40 | Citations present; no ungrounded policy assertions |
| **mixed** | 30 | Support + policy segments both present; citations in policy segment only |

- [x] emotional_support: 30 cases run; assertions documented/passed
- [x] practical_education: 30 cases run; assertions documented/passed
- [x] policy_navigation: 40 cases run; assertions documented/passed
- [x] mixed: 30 cases run; assertions documented/passed
- [x] No critical safety or grounding failure in matrix

Progress note (2026-03-05): `policy_navigation` 40-case batch completed with 0 critical failures and 100% citation coverage. Report: `docs/reports/Phase4-Pillar-Matrix-PolicyNavigation-40-Report.md`.
Progress note (2026-03-05): `mixed` 30-case batch initially failed (`0/30`, `mode_not_mixed`), then passed after mixed-intent normalization mitigation in API layer. Final rerun result: `30/30` pass, `0` critical failures, citation coverage `100%`. Report: `docs/reports/Phase4-Pillar-Matrix-Mixed-30-Report.md`.
Progress note (2026-03-05): `emotional_support` 30-case batch initially regressed due policy false-positive routing, then passed after API routing normalization and robust short-token matching. Final rerun result: `30/30` pass, `0` critical failures. Report: `docs/reports/Phase4-Pillar-Matrix-EmotionalSupport-30-Report.md`.
Progress note (2026-03-05): `practical_education` 30-case batch initially partially failed (`15/30`, then `20/30`) due practical false-negative routing and limited education keyword coverage; final rerun passed after API practical-intent normalization and keyword expansion. Final rerun result: `30/30` pass, `0` critical failures. Report: `docs/reports/Phase4-Pillar-Matrix-PracticalEducation-30-Report.md`.

**Execution:** Run matrix on every release candidate; block production promotion on any critical failure. See [PILLAR-TEST-MATRIX-EXECUTION.md](PILLAR-TEST-MATRIX-EXECUTION.md) for case format, assertions per pillar, and how to run (manual or script).

---

## 2. Pillar SLO targets (Spec §17.6.1)

| Pillar | p95 latency | Other |
|--------|-------------|--------|
| emotional_support | ≤ 4.0s | Style-fit score ≥ 4.0/5.0 |
| practical_education | ≤ 5.0s | Actionable-plan completeness ≥ 95% |
| policy_navigation | ≤ 8.0s | Citation coverage 100%; critical hallucination 0 |
| mixed | ≤ 9.0s | Both segments in ≥ 95% of turns; citations 100% in policy segment |

- [x] Latency and quality targets measured (or documented as deferred with rationale)

---

## 3. Benchmark audit

- [x] Policy Q/A packs executed; citation coverage and hallucination audit done
- [x] Block release on critical safety/grounding failures
- [x] Results documented (e.g. in `docs/reports/` or runbook)

---

## 4. Load test (Spec §13)

- [x] ≥ 100 concurrent sessions without critical failures
- [x] Error rate and latency under load documented

Progress note (2026-03-05): load-test track executed with repeatable runner `npm run job:phase4-load-test` (`scripts/phase4-load-test.js`). Current 100-concurrency runs remain unstable and do not meet gate:
- `logs/phase4-load.100c.standard.json` (`ok=5/100`, `5xx_rate=0.95`)
- `logs/phase4-load.100c.simple.json` (`ok=0/100`, `5xx_rate=1.00`)
- `logs/phase4-load.100c.standard.timeout120.json` (`ok=0/100`, `5xx_rate=1.00`)
- `logs/phase4-load.100c.bestcase-emotional.json` (`ok=35/100`, `5xx_rate=0.65`)
Detailed consolidation: `docs/reports/Phase4-Consolidation-Checkpoint-2026-03-05.md`.
Progress note (2026-03-05): after gateway overload guard rollout (in-flight + timeout graceful fallback), load gate run `logs/phase4-load.100c.standard.after-gateway-guard.json` passed with `ok=100/100`, `5xx_rate=0.00`, `error_envelope_rate=0.00`, `p50=1658ms`, `p95=14621ms`, `p99=17434ms`.

---

## 5. Operations and rollout

- [x] Pilot environment deployed with monitoring and alert thresholds (see [SLO-AND-MONITORING.md](SLO-AND-MONITORING.md))
- [x] Runbook and rollback process documented ([OPERATIONS-RUNBOOK.md](OPERATIONS-RUNBOOK.md))
- [x] Staged rollout (shadow → canary → GA) and incident ownership defined (Spec §17.6)
- [x] If gateway in use: success gate met (no critical hallucination increase, stable or better benchmarks); see [GATEWAY-SHADOW-DESIGN.md](GATEWAY-SHADOW-DESIGN.md) §4–6

Progress note (2026-03-05): benchmark + operations packaging finalized in:
- `docs/reports/Phase4-Benchmark-Audit-Pack-2026-03-05.md`
- `docs/reports/Phase4-Monitoring-Alert-Proof-2026-03-05.md`
- `docs/reports/Phase4-Rollout-Record-2026-03-05.md`
- `docs/reports/Phase4-Release-Freeze-Smoke-2026-03-05.md`
- `docs/reports/Phase4-Pilot-Go-NoGo-2026-03-05.md`

---

## 6. Optional (per ROADMAP §7.2)

- [ ] Accessibility aligned with WCAG 2.1 AA where applicable (Spec §15.2.B)
- [ ] Multilingual: request/response in de, fr, it, en; language preserved in retrieval and generation (Spec §6.1)
- [ ] Contract changelog and versioning (e.g. v1, v1.1) documented

---

## References

- **ROADMAP:** §7 (Phase 4)
- **Spec:** §17.6 (Operational standards, SLO, pillar test matrix)
- **Pillar matrix execution:** [PILLAR-TEST-MATRIX-EXECUTION.md](PILLAR-TEST-MATRIX-EXECUTION.md) (case format, assertions, run options)
- **Runbook:** [OPERATIONS-RUNBOOK.md](OPERATIONS-RUNBOOK.md)
- **Gateway:** [GATEWAY-SHADOW-DESIGN.md](GATEWAY-SHADOW-DESIGN.md)
- **Go/No-Go checkpoint:** `docs/reports/Phase4-Pilot-Go-NoGo-2026-03-05.md`