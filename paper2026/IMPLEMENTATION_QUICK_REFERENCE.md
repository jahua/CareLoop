# Quick Reference: 20-Week Implementation Guide

**Study Name:** Expert + Synthetic + Real Caregiver Validation of Personality-Adaptive Coaching  
**Timeline:** Weeks 1-20 (Oct 22, 2025 → ~March 2026)  
**Key Dates:** See calendar below

---

## PHASE-BY-PHASE SUMMARY

### PHASE 1: FOUNDATION (Weeks 1-2)
**What:** Literature review, IRB prep, environment setup
**Key Actions:**
- [ ] Submit main study IRB (personality detection + synthetic evaluation + real caregiver validation)
- [ ] Submit crisis protocol IRB (separate, parallel track)
- [ ] Review 30+ papers on personality, motivation, caregiver support
- [ ] Setup N8N + Docker development environment
- [ ] Develop FADP compliance checklist
**Success Gate:** Both IRBs submitted; ≥30 papers reviewed; dev environment working

---

### PHASE 2: EXPERT PILOT (Weeks 3-5)
**What:** Recruit n=5-8 domain experts; conduct think-aloud sessions; train evaluators
**Key Actions:**
- [ ] Recruit 5-8 domain experts (Spitex coordinators, geriatricians, home care nurses)
- [ ] Conduct 3 think-aloud sessions per expert (policy query, caregiving skill, tone-fit)
- [ ] Measure: SUS scores (target ≥70), appropriateness ratings (≥4.0/5.0), tone-fit (≥80%)
- [ ] **Select 2-3 experts for evaluator training**
- [ ] Develop 15-page evaluation rubric with 30 examples per criterion
- [ ] Train evaluators: 3 hours (rubric walk-through, practice scoring, calibration)
- [ ] Certification check: Practice κ ≥ 0.70 with trainer
**Success Gate:** n=5-8 experts, SUS ≥70, evaluators certified κ≥0.70

---

### PHASE 2.5: CAREGIVER RECRUITMENT (Weeks 8-9)
**What:** Recruit n=20-30 Swiss caregivers; prepare consent & scheduling
**Key Actions:**
- [ ] Partner with Spitex organizations + caregiver support groups (3-5 partners)
- [ ] Finalize informed consent forms (ethical template)
- [ ] Create recruitment flyer (Swiss German, plain language)
- [ ] Recruit n=20-30 caregivers (inclusion: >5h/week, ≥18y, Swiss German fluent)
- [ ] **Request caregiver study IRB approval** (Weeks 8-9, follow-up to main study approval)
- [ ] Schedule Sessions 1-3 for Weeks 11-14
- [ ] Prepare compensation process (CHF 50-100 per participant)
**Success Gate:** n=20-30 recruited, 80%+ consent rate, caregiver IRB approved, sessions scheduled

---

### PHASE 3: RAG & BENCHMARKING (Weeks 6-8)
**What:** Build Swiss policy RAG; curate Q-A benchmark
**Key Actions:**
- [ ] Gather policy documents (IV guidelines, Hilflosenentschädigung, BAG, cantonal Spitex)
- [ ] Generate 20-30 Q-A-chunk pairs (manual + LLM-assisted)
- [ ] Expert validation: Expert review of Q-A pairs (κ≥0.70 threshold)
- [ ] Implement minimal RAG retrieval system (vector embedding + similarity)
- [ ] Test: Recall@3 ≥0.7, groundedness ≥1.5/2.0
**Success Gate:** 20-30 validated Q-A pairs, Recall@3 ≥0.7, zero hallucinations

---

### PHASE 4: IMPLEMENTATION (Weeks 7-10)
**What:** Build detection, regulation, generation; validation studies
**Key Actions:**
- [ ] Week 7-8: Detection module (OCEAN + confidence), regulation logic, generation pipeline
- [ ] Week 8-9: EMA integration, Streamlit UI, Flask backend, integration tests
- [ ] **Week 9: Stress Driver Validation** (100 synthetic examples, human-LLM, κ≥0.70)
- [ ] **Week 10: EMA Sensitivity Analysis** (α ∈ {0.1-0.5}, convergence curves, table)
- [ ] **Week 10: Engagement Formula** (logistic regression on 50 examples, AUC≥0.75)
- [ ] **Week 10: Stress Level Calibration** (100 examples, κ≥0.70, confusion matrix)
**Success Gate:** Detection ≥70% accuracy, EMA α=0.3 empirically justified, formula AUC≥0.75, drivers κ≥0.70

---

### PHASE 5: EVALUATION & VALIDATION (Weeks 11-14)
**Multi-Stream Validation:** (a) Real caregiver, (b) Synthetic, (c) Human expert scoring, (d) Crisis monitoring, (e) Baselines
**Key Actions:**

**Stream (a): Real Caregiver Sessions**
- [ ] Week 11: Session 1 (BFI-44 personality survey + informed consent)
- [ ] Week 12: Session 2 (Interactive coaching 15-20 min + system logs)
- [ ] Week 13-14: Session 3 (PSS-10 stress survey + usability feedback)
- [ ] Collect: Engagement scores, stress levels, directives, personality evolution

**Stream (b): Synthetic Evaluation**
- [ ] Weeks 11-14: Run N≥250 synthetic conversations (Type A/B/C × 3 scenarios)
- [ ] Generate: EMA metrics, directive effectiveness, baseline comparisons
- [ ] Prepare 30% for human expert scoring (n≥75 conversations)

**Stream (c): Human Expert Scoring**
- [ ] Week 10: Final rubric preparation + expert briefing
- [ ] Weeks 11-14: Experts score independently (blinded, double-rater)
  - 30% of synthetic (n≥75, ~600 turns)
  - 100% of real caregiver (n=20-30, 60-90 turns)
  - 5 criteria: tone, engagement, stress reduction, relevance, accuracy (each 0-2)
- [ ] Calibration: Fleiss' κ check every 20-30 responses; target κ≥0.75
- [ ] Consensus scoring if >0.5-point disagreement

**Stream (d): Crisis Protocol Monitoring**
- [ ] Document any Level 4 (crisis) detections during real caregiver sessions
- [ ] Verify automatic crisis line contacts delivered (TeleFon 143, 112)
- [ ] Log researcher notification + action taken
- [ ] Zero protocol violations permitted

**Stream (e): Baseline Comparisons**
- [ ] Generic Non-Adaptive: Standard prompt, no personality
- [ ] Memory-Only: mem0 library, no personality detection
- [ ] Policy-Only: RAG without personality adaptation
- [ ] Adaptive: Full system
- [ ] Match A/B design: 20 conversations per baseline
- [ ] Score ALL on same 5 criteria (human experts)

**Success Gate:** r≥0.60 personality, r≥0.50 stress, d≥0.30 baselines, κ≥0.75 team, zero crisis violations

---

### PHASE 6: ANALYSIS & ADVANCED VALIDATION (Weeks 15-16)
**What:** Integrate results, validate correlations, analyze temporal dynamics
**Key Actions:**
- [ ] Generate Real vs. Synthetic validation table (engagement, stress, directives)
- [ ] Correlation analysis: BFI-44 vs. inferred OCEAN (target r≥0.60)
- [ ] Correlation analysis: PSS-10 vs. system stress levels (target r≥0.50)
- [ ] **Vector Autoregression (VAR):** Engagement-stress temporal causality
- [ ] **Policy Audit:** Systematic review of 250 policy claims; hallucination classification
- [ ] Generate all tables: effect sizes, κ scores, convergence curves, baseline comparison
**Success Gate:** r≥0.60 personality, r≥0.50 stress, baseline d≥0.30, policy ≥95% accuracy

---

### PHASE 7: ANALYSIS & WRITING (Weeks 17-19)
**What:** Write thesis chapters; synthesize findings
**Key Actions:**
- [ ] Methods: Implementation, data collection, evaluation frameworks, rubrics
- [ ] Results: Validation tables, statistical summaries, crisis protocol outcomes
- [ ] Discussion: Findings, limitations, comparison to existing work, implications
- [ ] Conclusion: Proof-of-concept achieved, limitations, future research roadmap
- [ ] Generate figures (10+): Convergence curves, baseline charts, validation scatters
**Success Gate:** Draft thesis complete; honest limitations documented

---

### PHASE 8: FINALIZATION (Week 20)
**What:** Final review, presentation prep, code handover
**Key Actions:**
- [ ] Incorporate supervisor feedback
- [ ] **Update abstract/title to reflect real caregiver + human expert scope**
- [ ] Final QA: Consistency checks, citations, figure quality
- [ ] Prepare presentation slides (visual summary, key findings)
- [ ] GitHub repository (code + documentation)
- [ ] Defense readiness review
**Success Gate:** Publication-ready thesis; clear presentation; reproducible code

---

## SUCCESS METRICS CHECKLIST

### IRB & ETHICS ✓
- [ ] Main study IRB approved
- [ ] Crisis protocol IRB approved
- [ ] Caregiver study IRB approved
- [ ] All informed consents signed
- [ ] Team crisis training: 100% participation, ≥80% quiz

### EXPERT VALIDATION ✓
- [ ] SUS ≥ 70
- [ ] Appropriateness ≥ 4.0/5.0
- [ ] Tone-fit ≥ 80%
- [ ] Policy accuracy 100% (expert-verified)
- [ ] Evaluator certification: κ ≥ 0.70

### REAL CAREGIVER ✓
- [ ] n = 20-30 recruited, ≥80% retention
- [ ] Personality: r ≥ 0.60 vs. BFI-44
- [ ] Stress: r ≥ 0.50 vs. PSS-10
- [ ] Engagement: Consistent with synthetic (t-test p>0.05)
- [ ] Mitigation: ≥ 60% high-stress → lower stress
- [ ] Usability: ≥ 4.0/5.0

### SYNTHETIC EVALUATION ✓
- [ ] N ≥ 250 conversations
- [ ] Human-LLM agreement: κ ≥ 0.70
- [ ] Baseline effect: Cohen's d ≥ 0.30
- [ ] EMA: 6-8 turns convergence, σ² < 0.15
- [ ] Policy: ≥ 95% correct, < 5% critical hallucinations
- [ ] Inter-run consistency: ≥ 0.85

### HUMAN EXPERT SCORING ✓
- [ ] 30% synthetic scored (n ≥ 75)
- [ ] 100% real caregiver scored (60-90 turns)
- [ ] Blinded double-rating
- [ ] Team κ ≥ 0.75
- [ ] Mean scores ≥ 1.4/2.0

### CRISIS PROTOCOL ✓
- [ ] IRB approved
- [ ] Automated contacts implemented (143, 112)
- [ ] Researcher notification protocol
- [ ] Team training completed
- [ ] Secure crisis log maintained
- [ ] Zero violations

---

## RESOURCE ALLOCATION

| Role | Weeks | Hours/Week | Total | Compensation |
|------|-------|-----------|-------|--------------|
| **Thesis Author** | 1-20 | 30-40 | 600-800h | Thesis credit |
| **Supervisor** | 1-20 | 2 (meetings) | 40h | Supervisor role |
| **Domain Experts (n=5-8)** | 3-5 | 2-3 each | 30-40h | CHF 50-100 voucher |
| **Evaluators (n=2-3)** | 10,11-14 | 5 each | 30-40h | CHF 200-300 each |
| **Caregivers (n=20-30)** | 11-14 | 1 (3 sessions) | 20-30h | CHF 50-100 each |
| **Ethics/IRB Support** | 1-2, 8-9 | 1-2 | 6-8h | Internal |

**Total Study Budget:**
- Participant compensation: ~CHF 3,000-4,000 (caregivers + experts)
- LLM API: ~CHF 200-500
- Infrastructure: Existing ZHAW resources
- **Total:** CHF 3,200-4,500

---

## CRITICAL PATH DEPENDENCIES

```
Week 1-2: Foundation
    ↓
Week 1-2: IRB Submissions (Main + Crisis)
    ├→ Week 3-5: Expert Pilot (pending approval)
    ├→ Week 8-9: Caregiver Recruitment (pending approval)
    └→ Week 8-9: Caregiver IRB (follow-up)

Week 3-5: Expert Pilot
    └→ Week 10: Train 2-3 experts as evaluators

Week 6-8: RAG & Benchmarking
    └→ Week 9-10: Integration with generation module

Week 7-10: Implementation
    ├→ Week 9: Stress driver validation
    ├→ Week 10: EMA sensitivity + engagement + stress calibration
    └→ Week 10: Expert evaluator certification

Week 8-9: Caregiver Recruitment
    └→ Week 11-14: Real caregiver sessions

Week 11-14: Multi-Stream Evaluation
    ├→ Weeks 11-14: Human expert scoring (all 30% + 100% real)
    ├→ Weeks 11-14: Synthetic evaluation (N≥250)
    └→ Weeks 11-14: Crisis monitoring

Week 15-16: Advanced Analysis
    └→ Week 17-19: Writing phase

Week 17-19: Writing
    └→ Week 20: Finalization + Defense
```

**Critical Gates:**
1. **Week 2:** IRB approval status (main + crisis) determines Phase 2 start
2. **Week 10:** Evaluator certification (κ ≥ 0.70) gates Phase 5 human scoring
3. **Week 14:** Real caregiver data complete (≥80% retention) for Phase 6 analysis
4. **Week 16:** All analysis complete by start of writing phase

---

## WEEKLY MEETING AGENDA TEMPLATE

**Supervisor Meeting (2 hours, weekly)**
- [ ] Prior week progress (what's done?)
- [ ] Blockers & risks (what's stuck?)
- [ ] Next week focus (what's priority?)
- [ ] Resource needs (any blockers?)
- [ ] Document updates (version control?)

**Recommended Cadence:**
- Weeks 1-5: Weekly (expert pilot intensity)
- Weeks 6-10: Bi-weekly (implementation stable)
- Weeks 11-14: Weekly (real caregiver + expert scoring intensity)
- Weeks 15-20: Weekly (analysis + writing push)

---

## KEY CONTACTS & RESOURCES

**IRB & Ethics:**
- ZHAW Research Ethics Committee: [contact]
- Crisis Line Partnership: TeleFon 143, SOS Amitié
- FADP Compliance: [university legal contact]

**Domain Experts:**
- Spitex Coordinator: [name, contact]
- Geriatrician: [name, contact]
- Home Care Nurse: [name, contact]

**LLM & APIs:**
- Primary: GPT-4 (OpenAI)
- Evaluator (Cross-Model): Claude or Gemini (TBD Week 10)
- Vector DB: Pinecone or Weaviate

**Recruitment Partners:**
- Spitex Organizations: [list 3-5 partners]
- Caregiver Support Groups: [list contacts]

---

## RED FLAGS & CONTINGENCIES

**If IRB delays past Week 4:**
→ Begin expert pilot prep (rubric, recruitment) without participant data collection

**If Caregiver Recruitment <15 by Week 9:**
→ Extend recruitment to Week 10; shift real caregiver sessions to Weeks 12-15 (compress timeline)

**If Expert Evaluator Κ < 0.70 after practice:**
→ Extend training (Week 10 + 11); clarify rubric with examples; consider 3rd evaluator

**If Real Caregiver Retention <70%:**
→ Document reasons; analyze completers vs. dropouts; report as limitation

**If LLM-Human Agreement κ < 0.65:**
→ Expand human audit to 50% (from 30%); investigate evaluator drift; re-train if needed

**If Policy Accuracy < 90%:**
→ Retrain on failed examples; document hallucination types; limit claims to validated domains

---

## DELIVERY CHECKLIST

**Week 20 Deliverables:**
- [ ] Final thesis v1.0 (PDF)
- [ ] Presentation slides (10-15 slides)
- [ ] GitHub repository (code + docs)
- [ ] Data anonymization verification
- [ ] All consent forms archived
- [ ] Crisis protocol documentation
- [ ] Expert rubric + scoring records
- [ ] Validation tables (all summaries)
- [ ] Handover memo for supervisor

---

**Last Updated:** October 22, 2025  
**Next Review:** Week 3 (Expert Pilot Kickoff)

