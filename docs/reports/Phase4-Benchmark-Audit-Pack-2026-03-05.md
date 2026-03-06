# Phase 4 Benchmark Audit Pack (2026-03-05)

Scope: consolidated benchmark evidence for policy quality, citation coverage, and grounding safety.

---

## 1) Policy Benchmark Regression

Command:

```bash
npm run job:retrieval-regression -- scripts/fixtures/retrieval-cases.json
```

Result:

- status: `ok`
- total: `5`
- pass: `5`
- fail: `0`
- duration: `40573ms`

Evidence source: command output from `scripts/retrieval-regression-runner.js`.

---

## 2) Pillar Matrix Audit Coverage

Final pillar reports:

- `policy_navigation` 40 cases: pass, critical failures `0`, citation coverage `100%`
- `mixed` 30 cases: pass (after rerun/fix), critical failures `0`, citation coverage `100%`
- `emotional_support` 30 cases: pass, critical failures `0`
- `practical_education` 30 cases: pass, critical failures `0`

References:

- `docs/reports/Phase4-Pillar-Matrix-PolicyNavigation-40-Report.md`
- `docs/reports/Phase4-Pillar-Matrix-Mixed-30-Report.md`
- `docs/reports/Phase4-Pillar-Matrix-EmotionalSupport-30-Report.md`
- `docs/reports/Phase4-Pillar-Matrix-PracticalEducation-30-Report.md`

---

## 3) Citation Coverage Gate Evidence

Canary citation-diff checks executed during rollout simulation:

- `baseline=1.0000`
- `canary=1.0000`
- `max_drop=0.05`
- gate result: `pass`

Supporting logs/checks are recorded in:

- `docs/PHASE3-TODO.md` (gateway rollout section)
- `logs/audit.baseline.policy.40.local.jsonl`
- `logs/audit.canary.policy.50.local.jsonl`
- `logs/audit.canary.policy.100.local.jsonl`

---

## 4) Hallucination / Grounding Safety Summary

Grounding-critical failures in final matrix reruns:

- `0`

Policy responses in benchmark and matrix runs include citations and pass grounding checks in final reruns.

---

## 5) Benchmark Gate Decision

- **Benchmark audit gate: PASS**
- Recommendation: include this pack as the benchmark appendix in pilot sign-off.
