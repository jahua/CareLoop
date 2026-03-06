# Phase 1 Stage Report Presentation

Version: 1.0  
Last Updated: 2025-10-01  
Owner: MSc AID Thesis – Personality-Aware Adaptive Chatbot

---

## 1. Application Overview (What this stage delivers)

- **Goal**: - Investigate whether the implemented pipeline can extend to multi-agent orchestration for broader applications.​

- Develop a personality-aware dialogue system that dynamically adapts tone, structure, and content to users' motivational profiles across
diverse use cases.
- **Primary use cases**:
  - Mental Health Support Leverage OCEAN personality traits and targeted prompts (inspired by Samuel et al.'s framework) to deliver empathetic,tailored interventions.​

    - Personalized Education Adapt educational content and delivery to align with users' personality profiles for personalized learning experiencesthat drive optimal engagement. Potential: Personality-aware chatbots significantly enhance student motivation and academic outcomes by
  delivering tailored feedback and support, fostering greater retention and deeper comprehension.​

  - Customer Support Tailor interaction approaches to users' personality traits for more intuitive, effective exchanges that boost satisfaction and
  streamline resolutions. Potential: Personality-tailored chatbots improve customer loyalty and operational efficiency through customized,
  responsive dialogues that minimize wait times and personalize resolutions.​

Elderly Companion Combat loneliness through conversational AI companions; note: Proven market entry challenges in Switzerland highlight
need for culturally sensitive design.
- **Key characteristics**:
  - Continuous OCEAN values in [-1.0, 1.0] per turn
  - EMA smoothing (α=0.3) with confidence filtering (≥0.4)
  - PostgreSQL persistence for sessions, turns, and personality states
  - Zurich Model-aligned regulation mapping

---

## 2. Architecture (High level)

```
Client → API (Webhook) → N8N Workflow
                        ├─ Enhanced Ingest
                        ├─ Load Previous State (PostgreSQL)
                        ├─ Combine Inputs → Merge Previous State
                        ├─ Detection (GPT-4) + EMA
                        ├─ Regulation (Directive Mapping)
                        ├─ Generation (GPT-4)
                        ├─ Verification & Refinement
                        └─ Save Session/Turns/States (PostgreSQL)
                            ↓
                        Return API Response
```

- **Models**: GPT-4 (detection + generation)
- **State**: PostgreSQL (sessions, turns, EMA states)
- **Smoothing**: Exponential Moving Average (per trait)
- **Observability**: Node-level logs, verification metadata, performance metrics

---

## 3. Workflow (Node-by-node)

| Step | Node | Purpose | Inputs → Outputs |
|------|------|---------|------------------|
| 1 | Webhook Trigger | Receive POST | `{session_id, message, turn_index}` → pass-through |
| 2 | Enhanced Ingest | Normalize, validate | request → `{session_id, clean_msg, turn_index, conversation_context}` |
| 3 | Load Previous State | Fetch last EMA state | `{session_id}` → `{ocean, confidence, stable, turn_index}` (or empty) |
| 4 | Combine Inputs | Wait for both | ingest + db → combined data |
| 5 | Merge Previous State | Merge context + prior | combined → `{...inputData, previous_state}` |
| 6 | Detection (GPT-4) + EMA | Detect OCEAN + smooth | context + previous → `{ocean[-1..1], confidence[0..1], stable}` |
| 7 | Regulation | Map traits to directives | `{ocean, confidence, stable}` → `{directives, policy_plan}` |
| 8 | Generation (GPT-4) | Produce response | `{directives, policy_plan, context}` → `{assistant_response}` |
| 9 | Verification | Validate response | `{assistant_response}` → `{verified_response, verification_score}` |
| 10 | Save (PostgreSQL) | Persist | sessions, turns, personality_states |
| 11 | Return | Output | `{assistant_response, updated_state, metadata}` |

---

## 4. Why Continuous Values (−1.0 to 1.0)

- **Theoretical**: Big Five traits and Zurich Model motivations are dimensional, not categorical.
- **EMA compatibility**: Discrete bins (−1,0,1) create quantization noise; EMA requires fine-grained values.
- **Adaptation nuance**: Enables intensity-proportional behavior (e.g., 0.3 vs 0.8 Openness).
- **Research & statistics**: Preserves information for correlation/regression; ~79% more information vs discrete.

Basic sketch (distribution example):
```
Freq │     ╱─╲
     │    ╱   ╲     (most users near 0)
     │   ╱     ╲
     │  ╱       ╲
     │ ╱         ╲
     │╱___________╲
     └─────────────── O trait
         -1   0   +1
```

---

## 5. EMA Smoothing

Parameters: `α = 0.3`, `confidence_threshold = 0.4`, `stabilization_turns = 6`

Update rule per trait T:
```
if confidence_T ≥ 0.4:
  EMA_T[t] = α * current_T[t] + (1 - α) * EMA_T[t-1]
else:
  EMA_T[t] = EMA_T[t-1]
```

Convergence example (Openness):
```
Turn:     1      2      3      4      5      6
Detected: 0.5    0.7    0.6    0.8    0.7    0.7
EMA:      0.15 → 0.315 → 0.40 → 0.52 → 0.574 → 0.612 (stable)
```

---

## 6. Database Schema (Phase 1)

| Table | PK | Purpose | Key Columns |
|-------|----|---------|-------------|
| `chat_sessions` | `session_id` | Session metadata | `total_turns`, `status`, timestamps |
| `conversation_turns` | `(session_id, turn_index)` | User/assistant turns + verification | `user_message`, `assistant_response`, `directives_applied` |
| `personality_states` | `(session_id, turn_index)` | EMA-smoothed OCEAN + confidence | `ocean_o/c/e/a/n`, `confidence_*`, `stable`, `ema_applied` |
| `performance_metrics` | `(session_id, turn_index)` | Timing, tokens (optional) | `detection_latency_ms`, `generation_latency_ms` |

Helper functions (examples):
```
get_latest_personality_state(session_id)
get_conversation_history(session_id, limit)
```

---

## 7. Detection Algorithm (GPT-4 + Zurich Model)

Prompt contract (simplified):
```
Return JSON only:
{
  "ocean": {"O": [-1..1], "C": [-1..1], "E": [-1..1], "A": [-1..1], "N": [-1..1]},
  "confidence": {"O": [0..1], "C": [0..1], "E": [0..1], "A": [0..1], "N": [0..1]},
  "reasoning": "<brief motivational analysis>"
}
Focus on WHY (approach/avoidance), evidence clarity, and consistency.
```

Confidence usage:
- Update only when `confidence ≥ 0.4` (per trait)
- Track stability after ≥6 consistent updates with low variance

---

## 8. Regulation Mapping (Zurich Model)

Activation: apply directives when `|trait_value| ≥ 0.2` and `confidence ≥ 0.4`.

| Trait | If positive (approach) | If negative (avoidance) |
|------|-------------------------|--------------------------|
| Openness | Introduce novelty, creative angles | Use familiar, concrete examples |
| Conscientiousness | Provide structured steps, plans | Keep flexible, avoid rigid timelines |
| Extraversion | Energetic, collaborative tone | Calm, reflective tone; respect autonomy |
| Agreeableness | Warm, cooperative language | Direct, matter-of-fact, boundary-respecting |
| Neuroticism | Reassurance, safety plans | Pragmatic, confident framing |

Intensity scaling example:
```
|C| in [0.2, 0.4): "somewhat flexible"
|C| in [0.4, 0.6): "flexible options; minimize structure"
|C| ≥ 0.6:         "strongly emphasize flexibility; avoid rigid frameworks"
```

---

## 9. Scope of Formal Thesis (Phase 2+)

### Primary Research Question
How can an adaptive LLM-based chatbot employ real-time personality detection and Zurich Model-guided behavior regulation to improve conversational quality and user-aligned emotional support compared to non-adaptive baseline systems?

### Sub-Research Questions

**RQ1 - Detection Mechanisms**: What prompt strategies and inference procedures yield reliable per-turn OCEAN assessment in short dialogue contexts?

**RQ2 - Regulation Strategies**: How should Zurich Model-aligned directives be composed to harmonize conflicting personality signals without incoherent behaviors?

**RQ3 - Evaluation Methodology**: Which LLM-based evaluation procedures provide reliable assessment with necessary bias controls?

**RQ4 - System Architecture**: What N8N workflow design optimally balances transparency, performance, and operational simplicity?

**RQ5 - Generalization and Limitations**: How do results vary between extreme simulated profiles and naturalistic patterns, and what limits emerge for live user interactions?

### Thesis Extension Framework

**Enhanced System Architecture**:
- Temporal smoothing (EMA for trait stability)
- Response verification modules
- Comprehensive PostgreSQL state persistence

**Human Validation Studies**:
- Human participant studies with ethical oversight
- Validate generalizability of simulation results
- Real-world deployment challenges across application domains

**Advanced Evaluation Methodologies**:
- Human evaluators alongside automated scoring
- Inter-rater reliability measures
- Longitudinal conversation quality assessment

**Application Integration**:
- Integration with existing systems (teletherapy, LMS, CRM)
- Adaptive decision support features
- Escalation protocols to human support

**Multimodal Extensions** (future):
- Voice analysis, facial expression recognition
- Physiological monitoring (privacy-evaluated)

### Publication Strategy

- **Academic**: CHI, AAAI, Journal of Personality and Social Psychology, TOCHI, CSCW
- **Open Source**: N8N workflows, evaluation framework, analysis tools
- **Industry**: Technology and education conferences
- **Policy**: Contribute to AI safety and ethics regulatory frameworks

---

## 10. KPIs and Evaluation (Phase 1)

- **EMA Convergence**: turns to stability (target 6–8)
- **Smoothness**: post-stability variance < 0.15
- **Regulation Effectiveness**: rubric-based, GPT-4 evaluator
- **Engagement**: conversation-turns per session (CPS)
- **Latency**: end-to-end response time

Simple time-series sketch (EMA):
```
Value
0.8 ─┐      ╭───╮      
0.6 ─┤   ╭──╯   ╰──╮   
0.4 ─┤ ╭─╯         ╰─╮ 
0.2 ─┼─╯             ╰─
     └────────────────── Turn
       1   2   3   4   5
```

---

## 11. Risks & Mitigations

| Risk | Impact | Mitigation |
|------|--------|------------|
| LLM variability | Medium | Fixed prompts, model pinning, retries |
| Confidence miscalibration | Medium | Thresholding, evaluator audits |
| Data drift | Medium | Monitoring, periodic revalidation |
| Privacy | High | No PII in logs, secure storage |

---

## 12. References (Internal)

- `ZURICH_MODEL_APPLICATION.md`
- `CONTINUOUS_VS_DISCRETE_PERSONALITY_VALUES.md`
- `EMA_IMPLEMENTATION_DETAILED.md`
- `DATABASE_DESIGN_AND_DATAFLOW.md`
- `CONFIDENCE_CALCULATION_EXPLAINED.md`

---

## Appendix: Remarks & Interpretation (Why and How)

### 1) Application Overview
- **Why it matters**: Aligns stakeholders on the concrete outcomes of Phase 1 and the problem-solution fit across domains.
- **How to interpret/use**: Use as the top-level scope statement for proposals, demos, and thesis framing; map each use case to evaluation scenarios.

### 2) Architecture
- **Why it matters**: Shows the separation of concerns (ingest, state, detect, smooth, regulate, generate) required for reliability and explainability.
- **How to interpret/use**: Validate that any change (e.g., model swap) touches only its layer; use to reason about latency and failure isolation.

### 3) Workflow
- **Why it matters**: Documents exact node contracts; enables reproducibility and debugging in N8N.
- **How to interpret/use**: Treat as the runbook for execution tracing; when output deviates, inspect inputs/outputs at the last correct node.

### 4) Why Continuous Values
- **Why it matters**: Continuous traits enable EMA, statistical validity, and nuanced adaptation; discrete bins cause flicker and information loss.
- **How to interpret/use**: When reporting results, prefer trajectories and confidence intervals over categorical labels; justify analysis methods accordingly.

### 5) EMA Smoothing
- **Why it matters**: Converts noisy per-turn detections into stable trajectories, reflecting human-like personality inference over time.
- **How to interpret/use**: Read α as responsiveness (higher = faster adaptation); monitor stability flags to gate heavier adaptations and claims.

### 6) Database Schema
- **Why it matters**: Provides longitudinal memory, auditability, and analysis capability across sessions and turns.
- **How to interpret/use**: Join `conversation_turns` with `personality_states` by `(session_id, turn_index)` to analyze directive efficacy and convergence.

### 7) Detection Algorithm
- **Why it matters**: Defines the contract the LLM must satisfy (JSON, continuous values, confidence) to keep the pipeline deterministic.
- **How to interpret/use**: If parsing or values drift, first validate prompt conformance; triage with small, controlled context windows.

### 8) Regulation Mapping
- **Why it matters**: Translates psychology into actionable UI/UX behaviors (tone, structure, content) in a traceable way.
- **How to interpret/use**: Use thresholds (|v| ≥ 0.2) as guardrails; scale directive intensity with |v| and suppress low-confidence traits.

### 9) Thesis Scope (Phase 2+)
- **Why it matters**: Defines the research trajectory from MVP to validated, publishable findings.
- **How to interpret/use**: Prioritize human validation and explainability; log evidence to support claims about personalization benefits.

### 10) KPIs and Evaluation
- **Why it matters**: Connects system internals (EMA, directives) to measurable outcomes (stability, tone, engagement).
- **How to interpret/use**: Track convergence (turns to stable), post-stability variance, and response quality; report with confidence bands.

### 11) Risks & Mitigations
- **Why it matters**: Surfaces operational and methodological risks early to protect validity and reliability.
- **How to interpret/use**: Link each mitigation to monitoring; e.g., confidence miscalibration → periodic evaluator audits and threshold tuning.

### 12) References (Internal)
- **Why it matters**: Establishes traceability between implementation and documentation.
- **How to interpret/use**: Cite specific sections when writing the thesis (methods and appendix) to streamline academic review.
