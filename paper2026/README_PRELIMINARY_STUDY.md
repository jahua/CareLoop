# Swiss Caregiver Coaching Assistant: Preliminary Study (Expert-Validated)

**Document:** `Preliminary-Study-V2.7.1.md`  
**Updated:** October 22, 2025  
**Supervisor Guidance Applied:** Expert-only validation (NO clinical outcomes)

---

## Study Scope (One Page)

### What We're Building
A **proof-of-concept personality-aware chatbot** for Swiss family caregivers that:
- Detects caregiver personality traits (Big Five: OCEAN) in real-time
- Adapts response tone, structure, and content to personality
- Provides emotional support, caregiving guidance, and Swiss benefit navigation
- Uses Exponential Moving Average (EMA, α=0.3) to stabilize personality estimates

### What We're Validating (This Study)
✅ **Expert Usability** - Do domain experts find the system usable? (SUS ≥70)  
✅ **Personality Appropriateness** - Do experts rate personality adaptation as appropriate? (≥4.0/5.0)  
✅ **Policy Accuracy** - Does system provide factually correct Swiss benefits guidance? (100%, zero hallucinations)  
✅ **Emotional Tone-Fit** - Does response tone match detected personality? (≥80% expert alignment)  
✅ **Technical Reliability** - Does EMA personality detection stabilize? (6-8 turns, σ<0.15, r>0.7)  

### What We're NOT Doing
❌ Clinical outcome measurement (caregiver burden reduction, stress scores)  
❌ Real caregiver participant studies  
❌ Longitudinal engagement tracking  
❌ Behavioral change validation  

→ These are **separate future phases** requiring distinct IRB approvals, funding, and timelines

---

## Data Collection (Two Sources)

### 1. Expert Pilot System Logs (Weeks 3-5)
**n=5-8 in-house domain specialists** (Spitex coordinators, geriatricians, home care nurses)

**Logs captured (automated):**
- OCEAN trait values per turn (5 dimensions × 8-10 turns per session)
- EMA smoothing application (α=0.3, confidence thresholds)
- Directives triggered (type, intensity, timestamp)
- Policy retrieval events (queries, retrieved chunks, citation accuracy)
- System latencies, errors, graceful fallbacks
- Session metadata (duration, conversation flow)

**Analysis:**
- SUS scores (expert think-aloud protocol)
- Personality adaptation appropriateness (5-point Likert)
- Policy accuracy verification (manual expert review)
- Tone-fit assessment (expert judgment)

---

### 2. LLM Stress Testing & Simulated Evaluation (Weeks 11-14)
**N≥250 automated synthetic conversations** with controlled personality profiles

**Test parameters:**
- 3 personality profiles (Type A: high OCEAN, Type B: low OCEAN, Type C: mixed)
- 3 caregiver stress scenarios (emotional burden, benefit confusion, self-care neglect)
- 8-10 turns per conversation × 3 independent runs = ≥250 total conversations

**Metrics evaluated (per-turn):**
- EMA convergence (turns to stability, final variance, temporal consistency)
- Directive effectiveness (7 criteria: detection, regulation, tone, coherence, needs)
- Hallucination detection (policy accuracy, citation coverage)
- Baseline comparison (adaptive vs. non-adaptive vs. memory-only)
- Inter-run consistency (r≥0.85 for reliability; human-LLM agreement κ≥0.70)

**Analysis:**
- EMA parameters validated (target: convergence in 6-8 turns, σ<0.15)
- Directive quality scores (Cohen's d≥0.3 vs. baseline)
- Policy grounding verification (100% citation coverage, zero fabrications)
- System reliability metrics (latency, error rates, graceful degradation)

---

## 20-Week Timeline

| Phase | Week(s) | Activity | Deliverable |
|-------|---------|----------|------------|
| **1. Foundation** | 1-2 | Literature review, theoretical framework, environment setup | FADP compliance plan, dev environment ready |
| **2. Expert Pilot** | 3-5 | Think-aloud sessions with n=5-8 experts (3 core tasks) | Usability report, expert ratings, policy validation |
| **3. RAG & Q-A** | 6-8 | Build policy retrieval system for IV + Hilflosenentschädigung | 20-30 validated Q-A pairs, retrieval accuracy ≥0.7 |
| **4. Implementation** | 7-10 | Detection + regulation + generation + Streamlit UI | Working chatbot prototype, integration tests |
| **5. Simulated Eval** | 11-14 | Run N≥250 synthetic conversations, LLM evaluator, human validation | Performance metrics, Cohen's d improvements, consistency κ≥0.70 |
| **6. Final Expert Review** | 15-16 | Optional additional expert sessions, final validation | Scope documentation, limitations, readiness assessment |
| **7. Analysis & Writing** | 17-19 | Statistical analysis, visualization, thesis writing | Draft thesis chapters 4-6 |
| **8. Finalization** | 20 | Supervisor feedback, final QA, presentation prep | Final thesis v1.0, GitHub repo, presentation slides |

---

## Success Criteria

### Expert Pilot (Weeks 3-5)
- ✅ System Usability Scale (SUS) ≥70
- ✅ Personality adaptation appropriateness ≥4.0/5.0
- ✅ Policy accuracy 100% (zero hallucinations, all claims cited)
- ✅ Emotional tone-fit ≥80% expert alignment
- ✅ Zero system crashes during think-aloud sessions

### Simulated Evaluation (Weeks 11-14)
- ✅ EMA convergence in 6-8 turns for ≥80% of sessions
- ✅ Post-stabilization variance σ<0.15
- ✅ Temporal consistency r>0.7 across segments
- ✅ ≥20% relative improvement vs. non-adaptive baseline (Cohen's d≥0.3)
- ✅ Inter-run consistency r≥0.85 (reliability gate)
- ✅ Human-LLM agreement κ≥0.70 (evaluator validation gate)

### Overall
- ✅ Zero fabricated Swiss benefits in any response
- ✅ 100% citation coverage for all policy claims
- ✅ Clear scope documentation with explicit limitations

---

## Key Files Created/Updated

1. **`Preliminary-Study-V2.7.1.md`** - Main thesis proposal (UPDATED)
   - RQ1-5 reframed for expert-only scope
   - No clinical outcome measurement
   - Expert pilot as primary validation

2. **`DATA_COLLECTION_SUMMARY.md`** - Data sources & collection methods (NEW)
   - Expert pilot system logs (Weeks 3-5)
   - LLM stress testing data (Weeks 11-14)
   - Explicit: NOT collecting clinical outcomes

3. **`FUTURE_CLINICAL_OUTCOMES_ROADMAP.md`** - Informational only (NEW)
   - What clinical studies COULD look like post-preliminary
   - RCT design, sample sizes, instruments
   - Timeline: 6-7 months + separate funding/IRB

4. **`APPROACH_COMPARISON.md`** - Decision tree (NEW)
   - Current scope vs. future clinical studies
   - Go/no-go criteria for clinical validation
   - Caregiver recruitment strategy

5. **`REVISION_SUMMARY_EXPERT_VALIDATION.md`** - Change log (NEW)
   - All modifications made to shift to expert-only scope
   - Removed clinical outcome references
   - Supervisor guidance applied

---

## Quick Checklist

### Before Expert Pilot (Weeks 1-2)
- [ ] Recruit n=5-8 domain experts (in-house ZHAW/Spitex network)
- [ ] Finalize think-aloud protocol (3 core tasks: policy, caregiving, tone)
- [ ] Set up JSONL + PostgreSQL logging infrastructure
- [ ] Prepare SUS questionnaire and consent forms
- [ ] Create FADP privacy checklist

### Expert Pilot (Weeks 3-5)
- [ ] Conduct n=5-8 think-aloud sessions (~60 min each)
- [ ] Collect system logs (OCEAN, directives, latencies)
- [ ] Administer SUS + appropriateness Likert scales
- [ ] Manual expert review: policy accuracy (0 hallucinations?)
- [ ] Record think-aloud audio/transcript

### RAG Development (Weeks 6-8)
- [ ] Curate 20-30 Q-A benchmark pairs (IV, Hilflosenentschädigung)
- [ ] Expert validation: κ≥0.70 agreement on accuracy
- [ ] Implement minimal vector DB retrieval
- [ ] Test for hallucinations: all policy claims cited?

### Implementation (Weeks 7-10)
- [ ] Detection module: OCEAN inference + confidence
- [ ] EMA smoothing: α=0.3, variance tracking
- [ ] Regulation module: trait → directive mapping
- [ ] Generation module: directive-driven responses
- [ ] Streamlit UI: real-time OCEAN display, think-aloud support
- [ ] Integration tests: all components working

### Simulated Evaluation (Weeks 11-14)
- [ ] Generate 250 synthetic conversations (3 profiles × 3 scenarios)
- [ ] LLM evaluator: 7 criteria per turn, 0-2 scoring
- [ ] Human validation: κ≥0.70 on 10-15% sample
- [ ] Baseline comparisons: Cohen's d≥0.3 improvement?
- [ ] EMA analysis: convergence, temporal consistency

### Final Expert Review (Weeks 15-16)
- [ ] Optional final expert sessions (n=3-5)
- [ ] Synthesize expert pilot + simulated results
- [ ] Document scope limitations explicitly
- [ ] Confirm system ready for publication

---

## What Success Looks Like

✅ **Technical:** System detects personality, stabilizes estimates, and applies appropriate directives  
✅ **Expert Validation:** Domain specialists find it usable and appropriate (SUS ≥70, ratings ≥4.0/5.0)  
✅ **Policy Accuracy:** All Swiss benefits guidance is factually correct with citations (100%, zero hallucinations)  
✅ **Reproducibility:** System logs and evaluation data are fully documented and reproducible  
✅ **Scope Clarity:** Explicit documentation of what this preliminary study validates (expert-only) and what it doesn't (clinical outcomes)  
✅ **Foundation:** Results establish proof-of-concept for potential future clinical research IF warranted  

---

## What Success Does NOT Look Like

❌ Real caregivers showing measurable burden reduction (CBI score improvement)  
❌ Long-term engagement metrics or return rates  
❌ Clinical outcome measurement (stress, mood, behavior change)  
❌ Claims about real-world caregiver impact  
❌ Population-representative findings  

→ These belong to **future clinical validation phases**, not this preliminary study

---

## Next Immediate Steps

1. **Week 1-2:** 
   - Confirm expert recruitment (n=5-8) with ZHAW/Spitex contacts
   - Finalize think-aloud protocol & consent forms
   - Set up PostgreSQL + JSONL infrastructure

2. **Week 3-5:** 
   - Conduct expert pilot sessions
   - Collect system logs & SUS scores
   - Verify zero policy hallucinations

3. **Week 6 (Go/No-Go Decision):**
   - If SUS ≥65 and expert ratings ≥3.5/5.0 → Proceed to implementation
   - If SUS <65 or major hallucinations → Redesign and retry
   - Review with supervisor

---

**For questions, refer to:**
- Main proposal: `Preliminary-Study-V2.7.1.md` (Sections 3.2 RQ1-5, 4.6 Evaluation, 6.2 Timeline)
- Data: `DATA_COLLECTION_SUMMARY.md`
- Future paths: `FUTURE_CLINICAL_OUTCOMES_ROADMAP.md`

