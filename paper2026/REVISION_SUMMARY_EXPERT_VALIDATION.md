# Preliminary Study Revision Summary: Expert-Validated Scope
**Date:** October 22, 2025  
**Supervisor Guidance:** Leverage in-house domain experts for rapid validation  
**Primary Change:** Converted from clinical outcome measurement to expert-only preliminary validation

## Key Changes Made

### 1. **Research Questions (RQ1-RQ5) Reframed**
- **RQ1:** Now focuses on EMA stability validation via N≥250 simulated conversations (no real caregiver measurement)
- **RQ2:** Simulated coaching effectiveness vs. non-adaptive baseline (no caregiver participants)
- **RQ3:** RAG policy grounding accuracy verified by expert domain specialists in think-aloud sessions
- **RQ4:** **NEW** - Expert usability & appropriateness assessment (n=5-8 in-house specialists) as primary validation
- **RQ5:** **NEW** - Explicit scope documentation acknowledging limitations (expert-only, no clinical outcomes, 2 policy domains)

### 2. **Eliminated Clinical Outcomes**
- ❌ Removed: "CBI burden reduction ≥10% over 8-week intervention"
- ❌ Removed: "n=30-50 Swiss caregiver participant study with BFI-44 ground truth"
- ❌ Removed: "Sustained Engagement ≥60% return rate over 4 weeks"
- ❌ Removed: "Thesis Phase E6: Human Validation with clinical measurements"

### 3. **Expert Pilot Elevated to Primary Validation**
**Scope:** n=5–8 in-house domain specialists (Spitex coordinators, geriatricians, home care nurses)

**Validation Methods:**
- Structured think-aloud protocol (3 core tasks: policy query, caregiving guidance, tone assessment)
- System Usability Scale (SUS ≥70)
- Expert appropriateness ratings (≥4.0/5.0)
- Policy accuracy verification (100% expert-verified, zero hallucinations)
- Emotional tone-fit assessment (≥80% alignment)
- Semi-structured exit interviews for qualitative insights

**Timeline:** Weeks 3-5 (expert recruitment and testing)

### 4. **Simulated Evaluation as Technical Validation**
**Scope:** N≥250 synthetic caregiver conversations with three personality profiles (Type A/B/C)

**Validation Methods:**
- EMA stability convergence (6-8 turns, σ<0.15)
- Temporal consistency (r>0.7)
- Directive effectiveness via automated + human-spot-checked evaluation
- A/B comparison vs. non-adaptive baseline (target ≥20% improvement, Cohen's d≥0.3)

**Timeline:** Weeks 11-14 (simulated evaluation & iteration)

### 5. **Work Plan Timeline Updated**
- ✅ **Phase 1 (Weeks 1-2):** Foundation
- ✅ **Phase 2 (Weeks 3-5):** Expert Pilot (PRIMARY VALIDATION)
- ✅ **Phase 3 (Weeks 6-8):** RAG & Q-A Benchmarking
- ✅ **Phase 4 (Weeks 7-10):** Implementation & UI
- ✅ **Phase 5 (Weeks 11-14):** Simulated Evaluation & Iteration
- ✅ **Phase 6 (Weeks 15-16):** Final Expert Assessment
- ✅ **Phase 7 (Weeks 17-19):** Analysis & Writing
- ✅ **Phase 8 (Week 20):** Finalization

### 6. **Experimental Validation Refined**
**Retained (Preliminary Scope):**
- E1: Expert Pilot
- E2: EMA Sensitivity Analysis (α parameter tuning)
- E3: Directive Quality & Effectiveness
- E4: Human-LLM Agreement (κ≥0.70)
- E5: Policy Grounding Verification

**Removed (Out of Scope):**
- E6: Human Validation with clinical outcomes

### 7. **Abstract & Scope Clarifications**
- ✅ Clarified this is a **proof-of-concept preliminary study** with expert validation
- ✅ Emphasized expert pilot is **primary validation method**
- ✅ Explicitly stated "Clinical outcome measurement...are deferred to future research phases"
- ✅ Reinforced non-clinical coaching scope

### 8. **Future Work Reframed**
Clinical research and caregiver outcome measurement are now explicitly positioned as **separate future phases** requiring:
- Independent IRB approvals
- Larger sample sizes (n=150+)
- Longitudinal tracking infrastructure
- Different timeline and resources

## Impact on Feasibility

### ✅ Advantages
- **Rapid validation:** Expert pilots completed in Weeks 3-5 (vs. 8-week clinical trials)
- **In-house resources:** Domain experts readily available from ZHAW/Spitex networks
- **Clear scope:** Proof-of-concept validation without clinical measurement complexity
- **Foundation for future:** Results support future clinical research if warranted
- **Focus on technical validation:** System architecture, personality detection, and policy accuracy as clear technical goals

### ⚠️ Scope Limitations (Explicitly Documented)
- Expert-only validation (n=5-8, not population-representative)
- Synthetic conversations for technical metrics
- 2-policy-domain pilot (IV, Hilflosenentschädigung only)
- Swiss German language prototype
- No measurement of real-world caregiver outcomes or engagement

## Documentation Status

All changes tracked in document:
- **Section 3.2 (RQ1-5):** Expert-validated scope
- **Section 4.6:** Use-case metrics focused on expert assessment
- **Section 4.6.7:** Experimental validation (E1-E5, E6 removed)
- **Section 6.2:** Updated work plan and timeline
- **Section 7.1-7.2:** Future work clarifies separate phases for clinical research
- **Abstract & Scope:** Repeatedly clarifies expert-only preliminary validation

## Alignment with Supervisor Guidance

✅ **Leverages in-house domain experts** for rapid, expert-informed validation  
✅ **Removes unrealistic clinical outcome measurement** goals  
✅ **Establishes clear proof-of-concept** validation scope  
✅ **Provides foundation** for future clinical research if warranted  
✅ **Maintains technical rigor** via simulated evaluation and automated metrics  
✅ **Enables 20-week thesis completion** within realistic resource constraints  

---

**Next Steps:** Review with supervisor; confirm alignment; proceed with expert recruitment (Week 1-2).
