# Update Summary: Integration of Best-Practice Plan into Main Document

**Date:** October 22, 2025  
**Document Updated:** Preliminary-Study-V2.7.1.md  
**Scope:** Full integration of OPTION A (Real Caregiver Cohort), APPROACH 2 (Human Expert Evaluation), OPTION B (Formalized Crisis Protocol), plus all Tier 2-4 best-practice suggestions

---

## MAJOR UPDATES MADE

### 1. ABSTRACT (Lines 26-32)
**Change:** Expanded to clearly articulate three-phase validation approach
- **Phase 1:** Expert pilot (Weeks 3-5, n=5-8)
- **Phase 2:** Synthetic evaluation (Weeks 11-14, N≥250)
- **Phase 3:** Real caregiver validation (Weeks 11-14, n=20-30)

**New Elements:**
- Real caregiver cohort with BFI-44 & PSS-10 validation (r≥0.60, r≥0.50 targets)
- Human experts trained as evaluators (κ≥0.70 required)
- 100% of real caregiver responses scored by humans (not LLM)
- Formalized crisis protocol with IRB approval & automated Swiss crisis line contacts (143, 112)
- Separated clinical outcome measurement to future phases

**Impact:** Abstract now accurately represents gold-standard methodology with real participant validation

---

### 2. RESEARCH QUESTIONS (RQ1-RQ5, Lines 243-258)
**Change:** Upgraded all RQs to include real caregiver ground-truth validation and human expert response scoring

**RQ1 - EMA Stability:**
- Added: Real caregiver validation against BFI-44 (r ≥ 0.60 target)
- Added: Synthetic + real comparison (N≥250 synthetic, n=20-30 real)

**RQ2 - Coaching Effectiveness:**
- Added: Human expert engagement/stress rating thresholds (≥1.2/2.0)
- Added: Real caregiver data alongside synthetic

**RQ3 - Policy Accuracy:**
- Changed: "100% accuracy" → "≥95% accuracy, <5% critical hallucinations"
- Added: Systematic audit of 250 policy claims (Weeks 15-16)
- Added: Tiered hallucination classification (Critical vs. Minor)

**RQ4 - Expert Usability & Response Quality:**
- Expanded from single criterion to **four validation streams:**
  - (a) Expert Pilot: SUS ≥70, appropriateness ≥4.0/5.0, tone-fit ≥80%
  - (b) Human Expert Response Scoring: 30% synthetic + 100% real, 5 criteria, κ≥0.70 certification
  - (c) Real Caregiver Ground-Truth: r≥0.60 personality, r≥0.50 stress, ≥60% mitigation
  - (d) Crisis Protocol: IRB approval, automated contacts, team training, zero violations

**RQ5 - Study Scope:**
- Now explicitly includes: expert + real caregiver + synthetic (not expert-only)
- Clarifies non-clinical scope while establishing validated methodology

**Impact:** RQs now reflect rigorous validation across three data sources (expert, real caregiver, synthetic)

---

### 3. SUCCESS CRITERIA (Lines 260-276)
**Change:** Completely restructured with new gold-standard criteria

**Old Structure:** Generic targets (SUS, reliability, effectiveness)
**New Structure:** Seven specific validation targets:

1. **Expert Pilot Usability:** SUS ≥70, appropriateness ≥4.0/5.0, tone ≥80%, accuracy 100%
2. **Human Expert Response Scoring:** κ≥0.70 certification, 30% synthetic + 100% real, mean scores ≥1.4/2.0
3. **Real Caregiver Ground-Truth:** r≥0.60 personality, r≥0.50 stress, ≥60% mitigation, ≥80% retention
4. **Crisis Protocol:** IRB approval, automated contacts, 100% team training, ≥80% quiz scores
5. **Policy Accuracy:** ≥95% correct, <5% critical hallucinations, systematic audit of 250 claims
6. **Effectiveness vs. Baselines:** ≥20% improvement (Cohen's d≥0.3) on 5 criteria, baselines scored by humans
7. **Observability:** JSONL traces, expert rubrics archived, audit trail preserved

**Impact:** Success criteria now gate on human expert judgment (κ≥0.70-0.75), real caregiver validation, and crisis protocol compliance

---

### 4. DATA MANAGEMENT: PRIMARY DATA SOURCES (Lines 623-649)
**Change:** Restructured from 2 sources to 4 distinct sources with detailed schemas

**New Section (3): Real Caregiver Validation (Weeks 11-14, n=20-30)**
- **Session 1:** BFI-44 (personality self-report) + informed consent
- **Session 2:** Interactive coaching + system logs (engagement, stress, directives)
- **Session 3:** PSS-10 (stress self-report) + usability feedback
- **Ground-truth validation:**
  - Inferred OCEAN vs. BFI-44 (target r≥0.60)
  - System stress levels vs. PSS-10 (target r≥0.50)
  - Engagement pattern consistency (t-test, p>0.05)
  - Stress mitigation rate (target ≥60%)
- **Storage:** PostgreSQL + JSONL (encrypted, pseudonymized)

**New Section (4): Human Expert Response Scoring & Crisis Monitoring (Weeks 11-14)**
- **Expert pool:** 2-3 domain specialists from pilot (trained in Week 10)
- **Rubric:** 15-page guide, 30 examples per criterion, 3-hour certification
- **Scoring:** 30% synthetic (n≥75) + 100% real (60-90 turns), blinded double-rating
- **5 criteria:** tone appropriateness, engagement, stress reduction, relevance, factual accuracy (each 0-2)
- **Quality gates:**
  - Fleiss' κ≥0.75 team agreement
  - Inter-rater calibration after every 20-30 responses
  - Consensus scoring if >0.5-point disagreement
- **Crisis monitoring:** Level 4 detections logged, automated contact verified, researcher actions documented

**Impact:** Data sources now include human expert judgment at scale + real caregiver ground-truth + crisis documentation

---

### 5. UPDATED POSTGRESQL SCHEMA (Lines 660-666)
**New Tables Added:**
- `engagement_metrics`: message length, latency, follow-up questions, directive acceptance (per turn)
- `stress_metrics`: stress level (0-4), lexical markers, emotional intensity, escalation flags, drivers
- `engagement_stress_interaction`: correlation, mitigation rate, scenario consistency

**Plus caregiver_validation table** for BFI-44/PSS-10 scores and participant demographics

**Impact:** Schema now captures both operational metrics (logs) and ground-truth instruments (BFI-44, PSS-10)

---

### 6. TWENTY-WEEK TIMELINE (Lines 1000-1013)
**Change:** Restructured from 8 phases to 8 integrated phases with explicit research quality gates

**Key Additions:**

**Phase 1: Foundation (Weeks 1-2)**
- Added: **IRB submissions (Main study + Crisis protocol)**
- Success: IRB approvals pending

**Phase 2: Expert Pilot (Weeks 3-5)**
- Added: **Train 2-3 experts as evaluators (3-hour certification)**
- Added: Develop 15-page rubric with 30 examples per criterion
- Success: κ≥0.70 evaluator certification required

**Phase 2.5: Caregiver Recruitment & Prep (NEW, Weeks 8-9)**
- Recruit n=20-30 Swiss caregivers (>5h/week)
- Partner with Spitex + support groups
- Prepare informed consent + session scheduling
- Success: 80%+ consent, n=20-30 recruited

**Phase 4: Implementation (Weeks 7-10)**
- Added: **EMA sensitivity analysis (Week 10)** → convergence curves, variance table
- Added: **Stress driver validation (Week 9)** → confusion matrix, κ per driver
- Added: **Engagement formula (Week 10)** → data-driven weights, AUC≥0.75
- Added: **Stress level calibration (Week 10)** → 0-4 scale validation, κ≥0.70

**Phase 5: Evaluation & Validation (NEW STRUCTURE, Weeks 11-14)**
- Multi-stream validation:
  - (a) Real caregiver sessions (3 per participant)
  - (b) Synthetic evaluation (N≥250 with 3 baselines)
  - (c) Human expert scoring (2-3 raters, blind double-scoring)
  - (d) Crisis protocol monitoring (Level 4 tracking)
  - (e) Baseline comparisons (adaptive vs. 3 alternatives)
- Success: r≥0.60 personality, r≥0.50 stress, d≥0.30 baselines, κ≥0.75 team

**Phase 6: Advanced Validation & Analysis (Weeks 15-16)**
- Real vs. Synthetic comparison tables
- Statistical summary (correlations, effect sizes, κ)
- Temporal dynamics (VAR analysis)
- Policy audit (250 claims, <5% hallucinations)

**Phase 8: Finalization (Week 20)**
- Added: **Update abstract/title to reflect real caregiver validation + human expert scoring**
- Success: External validity clearly bounded

**Impact:** Timeline now explicitly gates on IRB approvals, human expert certification (κ≥0.70), real caregiver recruitment, and comprehensive multi-stream validation

---

### 7. LIMITATIONS VS. FUTURE WORK (Lines 1040-1049)
**Change:** Comprehensive update showing all improvements addressed in THIS study

**Before:** Generic future improvements listed
**After:** Checkmark (✓) system showing what IS done in this study

**Now Included (✓ THIS STUDY):**
- ✓ EMA sensitivity analysis (α ∈ {0.1-0.5}) with convergence curves
- ✓ Real caregiver ground-truth validation (BFI-44 r≥0.60, PSS-10 r≥0.50)
- ✓ Stress level calibration (100 examples, human-LLM confusion matrix, κ≥0.70)
- ✓ Stress driver reduction + validation (3 drivers, κ≥0.70)
- ✓ Engagement formula derivation (logistic regression, AUC≥0.75)
- ✓ Human expert evaluation (30% synthetic + 100% real, κ≥0.75)
- ✓ Baseline comparisons (3 baselines, matched scoring, Cohen's d)
- ✓ Formalized crisis protocol (IRB approved, automated contacts, training)
- ✓ Expanded human audit (30% vs. 10-15%, Fleiss' κ≥0.75)
- ✓ Policy accuracy audit (250 claims, <5% hallucinations, tiered classification)

**Deferred to Thesis/Future Phases:**
- Clinical outcome measurement (n=150+, CBI, PSS-10)
- Full 26-canton RAG coverage
- Multimodal inputs (voice, facial expression)
- Cross-cultural adaptation (French, Italian variants)

**Impact:** Document now clearly distinguishes between validated methodology (THIS study) and clinical trials (future phases)

---

## INTEGRATED PLAN ALIGNMENT

### Three Core Selections Implemented:
✅ **OPTION A: Real Caregiver Cohort (n=20-30)**
- Weeks 11-14 data collection
- 2-3 brief sessions (non-clinical, non-longitudinal)
- BFI-44 & PSS-10 ground-truth validation
- Feasibility within 20-week timeline
- CHF 50-100 compensation, ethical approvals

✅ **APPROACH 2: Human Expert Evaluation (Gold Standard)**
- 2-3 domain specialists trained (κ≥0.70 certification)
- 30% of synthetic (n≥75) + 100% of real caregivers scored
- 15-page rubric with 30 examples per criterion
- Blinded double-rating, consensus scoring
- Inter-rater reliability gated (κ≥0.75)

✅ **OPTION B: Formalized Crisis Protocol**
- Separate IRB approval (Weeks 1-4)
- Level 4 triggers automatic TeleFon 143 + 112 emergency contacts
- Researcher notification protocol (documentation, not clinical care)
- 2-hour team training (≥80% certification required)
- Secure crisis incident log maintained

### Tier 2-4 Best Suggestions Implemented:
✅ EMA Sensitivity Analysis (α ∈ {0.1-0.5}, Week 10)
✅ Stress Driver Validation (3 drivers, κ≥0.70, Week 9)
✅ Engagement Formula (Data-driven logistic regression, AUC≥0.75, Week 10)
✅ Stress Level Calibration (100 examples, κ≥0.70, Week 10)
✅ Temporal Dynamics (Vector autoregression, Granger causality, Weeks 15-16)
✅ Baseline Comparisons (3 baselines, matched A/B scoring, human evaluation)
✅ Expanded Human Audit (30% not 10-15%, Fleiss' κ≥0.75 ongoing)
✅ Realistic Accuracy Target (≥95% correct, <5% critical hallucinations, tiered classification)
✅ External Validity Framing (Study rename, explicit limitations, research roadmap)

---

## NEW SECTION: VALIDATION ARCHITECTURE

Document now explicitly frames study as:

**NOT:**
- "Caregiver outcome study" (clinical claims)
- "Expert-only validation" (excludes real participants)
- "Purely synthetic" (ignores ground-truth)

**YES:**
- "Expert + Synthetic + Real Caregiver Validation" (three-phase proof-of-concept)
- "Validated methodology for clinical research" (foundation for future trials)
- "Best-practice evaluation framework" (rubrics, metrics, protocols replicable)

---

## KEY METRICS & SUCCESS GATES

### IRB & Ethics:
- ✓ Main study IRB approval (Weeks 1-4)
- ✓ Crisis protocol IRB approval (Weeks 1-4, parallel)
- ✓ Caregiver study IRB approval (Weeks 8-9)
- ✓ Team crisis training certification (≥80% quiz)
- ✓ Informed consent documented (all participants)

### Expert Validation:
- ✓ SUS ≥ 70 (expert pilot)
- ✓ Appropriateness ≥ 4.0/5.0 (tone, engagement, guidance)
- ✓ Evaluator certification: κ ≥ 0.70 (minimum), κ ≥ 0.75 (team ongoing)
- ✓ Policy accuracy: 100% verified by experts (Weeks 3-5)

### Real Caregiver Validation:
- ✓ Personality detection: r ≥ 0.60 vs. BFI-44
- ✓ Stress detection: r ≥ 0.50 vs. PSS-10
- ✓ Engagement consistency: No significant divergence from synthetic (t-test, p>0.05)
- ✓ Stress mitigation: ≥ 60% of high-stress turns followed by lower stress
- ✓ Retention: ≥ 80% session completion
- ✓ Usability: ≥ 4.0/5.0 system rating

### Synthetic Evaluation:
- ✓ Human-LLM agreement: κ ≥ 0.70 (gate for LLM scaling to 70%)
- ✓ Baseline effect: Cohen's d ≥ 0.30 vs. non-adaptive
- ✓ EMA convergence: 6-8 turns with variance < 0.15
- ✓ Policy accuracy: ≥ 95% correct, < 5% critical hallucinations
- ✓ Inter-run consistency: ≥ 0.85

### Human Expert Scoring:
- ✓ Rubric coverage: 30 examples per criterion (5 criteria × 0-2 scale)
- ✓ Sample size: 30% synthetic (n ≥ 75) + 100% real (60-90 turns)
- ✓ Blinded scoring: Independent raters, two-rater consensus
- ✓ Team calibration: κ ≥ 0.75, recalibration after every 20-30 responses
- ✓ Mean scores: ≥ 1.4/2.0 across all criteria

### Crisis Protocol:
- ✓ IRB approval obtained
- ✓ Automated contact system implemented (143, 112 triggers)
- ✓ Researcher notification protocol functional
- ✓ Team training completed (100% participation, ≥80% quiz)
- ✓ Secure crisis log maintained
- ✓ Zero protocol violations

---

## DOCUMENT IMPROVEMENTS SUMMARY

| Section | Before | After | Impact |
|---------|--------|-------|--------|
| **Abstract** | Expert + synthetic only | Expert + synthetic + real caregiver + crisis protocol | Establishes rigorous 3-phase validation |
| **RQs** | 5 generic research questions | 5 expanded RQs with ground-truth targets (r≥0.60, κ≥0.70) | Clear empirical thresholds for all research directions |
| **Success Criteria** | 5 generic targets | 7 specific validation streams with human expert gates | Success now depends on κ≥0.70-0.75 human agreement |
| **Data Sources** | 2 sources (expert logs, synthetic) | 4 sources (expert, synthetic, real caregiver, human expert scoring) | Comprehensive multi-source validation |
| **Timeline** | 8 phases, 20 weeks | 8 integrated phases with IRB gates + real caregiver recruitment | Realistic sequencing with parallel ethical approvals |
| **Limitations Table** | Future-only improvements | Mix of ✓THIS STUDY and deferred items | Clear distinction between validated (now) and clinical (future) |

---

## NEXT STEPS FOR USER

1. **Review updated document:** Scan Abstract through Success Criteria to verify alignment with intent
2. **Socialize with supervisor:** Present updated RQs, timeline, real caregiver component
3. **Initiate IRB submissions:** Use Phase 1 (Weeks 1-2) to prepare main study + crisis protocols
4. **Begin expert recruitment:** Identify 5-8 domain specialists + 2-3 for evaluator training
5. **Recruit caregivers early:** Start Weeks 8-9 to enable Weeks 11-14 data collection
6. **Prepare rubric & training:** Finalize 15-page rubric during Phase 3 (Weeks 6-8)
7. **Implement validation studies:** Week 10 runs sensitivity analyses, driver validation, engagement formula

---

## FILE LOCATION & VERSION
- **File:** `/Users/huaduojiejia/MyProject/hslu/2026/preliminary-studies/FINAL_CASE- Caregiver research roadmap/PMT/Preliminary-Study-V2.7.1.md`
- **Version:** 2.7.1 (Updated with Integrated Implementation Plan)
- **Last Updated:** October 22, 2025
- **Changes:** 50+ edits across Abstract, RQs, Success Criteria, Data Management, Timeline, Limitations

