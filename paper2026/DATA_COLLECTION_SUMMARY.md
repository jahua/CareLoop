# Data Collection Summary: Preliminary Study

## Overview

**This preliminary study collects TWO TYPES of data:**

1. **Expert Pilot System Logs** (Weeks 3-5)
2. **LLM Stress Testing Evaluation Data** (Weeks 11-14)

**NOT COLLECTED:** Clinical outcomes, real caregiver burden measurements, longitudinal engagement tracking (these are future study scope)

---

## Data Source #1: Expert Pilot System Logs

**When:** Weeks 3-5 (Expert pilot sessions, n=5-8 domain specialists)

**What's Logged:**

### Personality Detection Data
- OCEAN trait values per turn (O, C, E, A, N ∈ [-1.0, +1.0])
- Confidence scores per trait (0.0-1.0)
- EMA smoothing application (T_smoothed = 0.3 × T_detected + 0.7 × T_previous)
- Stability flag (TRUE when variance <0.15 for ≥6 turns)

### Behavioral Response Data
- Directives triggered (e.g., "Novel concepts", "Energetic tone", "Structured steps")
- Directive intensity (percentage of max based on trait magnitude)
- Coaching mode active (Emotional Support / Resource Navigation / Self-Care Planning)
- Generated response text + metadata

### Technical Performance Data
- Detection latency (target <1.5s p95)
- Generation latency (target <1.5s p95)
- Total tokens used (input + output)
- LLM model/temperature used
- Errors or fallbacks triggered

### Policy Retrieval Data
- Query intent classification
- Policy chunks retrieved (top-3)
- Citation presence/accuracy
- Hallucination flags (if any)

### Session Metadata
- session_id (UUID)
- expert_id, turn_index
- Session duration, total turns
- Conversation flow (3 core tasks: policy query, caregiving guidance, tone assessment)

**Storage:** PostgreSQL + JSONL audit logs  
**Size:** ~5-8 sessions × 8-10 turns × 500 bytes/turn ≈ 20-40 MB

---

## Data Source #2: LLM Stress Testing & Simulated Evaluation

**When:** Weeks 11-14 (Automated simulated conversations)

**What's Evaluated:**

### Simulated Conversation Design
- **Profiles:** Type A (high OCEAN), Type B (low OCEAN), Type C (mixed)
- **Scenarios:** 
  1. Emotional burden & role strain (Emotional Support mode)
  2. Benefit navigation confusion (Resource Navigation mode)
  3. Self-care neglect & burnout risk (Self-Care Planning mode)
- **Total:** N ≥ 250 conversations (3 profiles × 3 scenarios × 10 turns × 3 runs)

### EMA Stability Metrics
- **Convergence:** Turns required to reach `stable=TRUE` (target 6-8)
- **Final variance:** σ² post-stabilization (target <0.15)
- **Temporal consistency:** Pearson r across session segments (target >0.7)
- **Early-turn bias:** Variance in first 3 turns vs. turns 6+

### Response Quality Evaluation
**Per-turn scoring (0-2 scale, 7 criteria):**

| Criterion | Measurement | Score |
|-----------|-------------|-------|
| Detection Accuracy | Trait alignment with personality cues | 0/1/2 |
| EMA Convergence | Smooth progression toward stability | 0/1/2 |
| Confidence Calibration | Confidence matches evidence strength | 0/1/2 |
| Regulation Effectiveness | Correct directive application | 0/1/2 |
| Emotional Tone | Tone matches personality & state | 0/1/2 |
| Relevance & Coherence | Contextual appropriateness | 0/1/2 |
| Personality Needs | Addresses trait-specific requirements | 0/1/2 |

**Total per-turn: 0-14 points**

### Hallucination Detection
- Policy claims with/without citations
- Fabricated benefits (checked against official documents)
- Factual accuracy of policy statements (100% target)
- Grounding violations (assertions not in conversation)

### Baseline Comparison
- **Adaptive system** (personality-aware with directives)
- **Non-adaptive baseline** (generic responses)
- **Memory-only baseline** (mem0-style factual recall, no personality)
- **Detection-only baseline** (personality detection without regulation)

**Metric:** Cohen's d ≥ 0.3 for meaningful improvement vs. baseline

### Inter-Run Consistency
- **3 independent runs** per conversation (fixed seed)
- **Consistency target:** r ≥ 0.85 across runs (reliability gate)
- **Evaluator reliability:** κ ≥ 0.70 human-LLM agreement (10-15% sample)

**Storage:** CSV/JSONL with evaluation matrix  
**Size:** 250 conversations × 8 turns × 100 bytes/record ≈ 200 KB

---

## Data Flow Architecture

```
Expert Pilot (Weeks 3-5)
  ├─ Expert session starts
  ├─ User input captured
  ├─ Detection module runs → logs OCEAN + confidence
  ├─ Regulation module runs → logs directives
  ├─ Generation module runs → logs response + latency
  ├─ All data → PostgreSQL + JSONL
  └─ Think-aloud transcript + SUS scores → separate files

Simulated Evaluation (Weeks 11-14)
  ├─ Generate 250 synthetic conversations
  ├─ Run 3 independent iterations (fixed seed)
  ├─ LLM evaluator scores each turn (7 criteria)
  ├─ Human spot-check 10-15% of conversations
  ├─ Compute agreement κ ≥ 0.70 gate
  ├─ Calculate baseline comparisons (Cohen's d)
  └─ All data → CSV/JSONL files
```

---

## Data Security & Storage

**Encryption:**
- PostgreSQL: AES-256 at rest
- JSONL logs: Encrypted on disk
- API keys: N8N credential vault

**Access Control:**
- PI + supervisor only (role-based)
- No PII in expert sessions (pseudonymized IDs)
- Audit trails for all data access

**Retention:**
- 12 months default
- Longer if needed for publication/reproducibility
- User-controlled deletion rights (preliminary only)

---

## Data Analysis Timeline

| Phase | Week | Data Sources | Outputs |
|-------|------|--------------|---------|
| **Expert Pilot** | 3-5 | System logs, think-aloud transcripts | Usability report, expert ratings |
| **System Refinement** | 6-10 | Logs from bug fixes, prompt optimization | Refined system configuration |
| **Simulated Eval** | 11-14 | LLM evaluator scores, baseline comparisons | Performance metrics, effect sizes |
| **Final Analysis** | 15-16 | Integrated expert + simulated data | Technical validation report |
| **Writing** | 17-19 | Synthesized findings | Thesis chapters 4-6 |

---

## Key Deliverables

✅ **Expert Pilot Report** (Week 6)
- SUS scores, expert appropriateness ratings
- Policy accuracy verification (0 hallucinations)
- Qualitative feedback themes
- System reliability assessment

✅ **Simulated Evaluation Report** (Week 15)
- EMA convergence metrics (target 6-8 turns)
- Directive effectiveness (≥20% improvement vs. baseline)
- Inter-run consistency (κ≥0.70 human-LLM agreement)
- Grounding verification (100% citations)

✅ **Technical Validation Summary** (Week 16)
- Combined findings from both data sources
- Scope limitations documented
- Recommendations for next phases

---

## What's NOT Collected

❌ Real caregiver outcomes (burden reduction, stress measurement)  
❌ Longitudinal engagement tracking (return rates, sustained use)  
❌ Caregiver demographic data (age, gender, income)  
❌ Clinical assessments (BFI-44, CBI, PSS-10)  
❌ Real-world deployment metrics  

→ These are reserved for **future clinical validation studies**

---

## Summary

| Data Type | Timeline | Scope | Storage | Analysis |
|-----------|----------|-------|---------|----------|
| **Expert Logs** | Weeks 3-5 | n=5-8, 5-8 sessions | PostgreSQL + JSONL | Usability + appropriateness |
| **LLM Stress Test** | Weeks 11-14 | N≥250 synthetic | CSV/JSONL | Technical validation |
| **Clinical Outcomes** | ❌ Not collected | — | — | Future study |

