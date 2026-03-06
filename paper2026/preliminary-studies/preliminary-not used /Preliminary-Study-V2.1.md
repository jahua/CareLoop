# Adaptive LLM-Based Chatbot with Personality-Aware Dialogue for Human-Centered Applications: A Formal Preliminary Study

**Author:** [Your Name]  
**Program:** MSc Applied Information and Data Science (HSLU)  
**Supervisors:** Prof. Dr. Guang Lu; Prof. Dr. Alexandre de Spindler  
**Date:** [YYYY-MM-DD]  
**Version:** 1.0 (Formal Academic Manuscript)

---

## Abstract

Emotional wellbeing and personalized support represent fundamental challenges across diverse human-centered applications, from mental health assistance and educational guidance to customer service and workplace coaching. While conversational AI offers scalable solutions for emotional support and personalized interaction, many existing digital assistants remain generic and fail to adapt to users' individual personality differences, limiting their effectiveness in providing meaningful, contextually appropriate assistance. This preliminary study proposes a reproducible, N8N-orchestrated framework for personality-aware dialogue that integrates per-turn Big Five (OCEAN) personality detection with behavior regulation grounded in the Zurich Model of Social Motivation.

Building on the empirical findings of Devdas (2025), who demonstrated substantial performance gains (34% improvement) for personality-adaptive chatbots over non-adaptive baselines in controlled simulations, we implement a transparent detect→regulate→generate pipeline with deterministic contracts, quote-and-bound dialog grounding, and neutral fallbacks. Our approach operationalizes continuous OCEAN inference (values in [−1.0, +1.0]) with EMA smoothing, mapped to Zurich-aligned behavioral directives that modulate conversational tone, pacing, warmth, and novelty in real time.

We specify a comprehensive evaluation harness based on a scripted LLM evaluator and structured rubric to assess detection accuracy, regulation effectiveness, tone appropriateness, relevance and coherence, and the satisfaction of personality-specific emotional needs. The methodology includes simulation protocols with extreme personality profiles (Type A: all +1s; Type B: all −1s), automated scoring procedures, and reproducibility measures through fixed model versions, seeds, and comprehensive logging.

The outcome is a technically reproducible pathway to implement, test, and extend personality-aware conversational systems oriented to human-centered applications, with emphasis on transparency, traceability, and safety. This work contributes to the growing field of affective computing by providing a practical framework that bridges personality psychology theory with operational AI systems suitable for mental health support, educational assistance, customer service, workplace coaching, and general emotional companion applications.

Positioning and thesis scope: This preliminary study defines the thesis trajectory. The master’s thesis, titled “Adaptive LLM‑Based Chatbot with Personality‑Aware Dialogue for Human‑Centered Applications,” will implement a focused Stress Self‑Regulation Micro‑Coach to demonstrate the architecture’s key objective: a reusable, reliable, and personality‑adaptable pipeline that supports future research across domains.

**Keywords:** personality-aware chatbot; OCEAN; Zurich Model; behavior regulation; N8N; evaluation; dialog grounding; human-centered AI; emotional support; emotional assistant; digital companion

---

## 1. Background

### 1.1 Problem Context: Emotional Wellbeing and Personalized Support Challenges

Emotional wellbeing and personalized support represent fundamental challenges across diverse populations and application domains. Modern society faces increasing demands for accessible, responsive emotional assistance that can adapt to individual needs, preferences, and personality traits. Traditional support systems often struggle with scalability, consistency, and personalization, whether in healthcare settings, educational environments, customer service interactions, or general emotional companionship scenarios.

The need for personalized emotional support spans multiple demographics and contexts: students requiring adaptive learning assistance, employees needing workplace emotional guidance, customers seeking empathetic service interactions, and individuals across all age groups requiring accessible mental health support. Current digital assistance solutions frequently provide generic, one-size-fits-all responses that fail to account for individual personality differences, communication preferences, and contextual emotional needs (Ta et al., 2020; Broadbent et al., 2024). This mismatch between user needs and system capabilities highlights the urgent requirement for adaptive, personality-aware conversational agents that can provide contextually appropriate emotional support across varied human-centered applications.

### 1.2 Limitations of Current Digital Assistants

Digital assistants and conversational AI systems have emerged as promising scalable interventions for personalized support across various domains. Systems ranging from customer service chatbots to educational tutoring agents have demonstrated user engagement and show potential for enhancing user experience through conversational interfaces (Ta et al., 2020; Broadbent et al., 2024). However, their effectiveness varies significantly and often depends on whether conversations feel emotionally attuned and personally relevant to individual users (Xie & Pentina, 2022; De Freitas et al., 2024).

A fundamental limitation of existing systems lies in their reliance on generic prompts or static user profiles. Most current implementations fail to adapt dynamically to evolving user signals, personality cues, or emotional states within conversations. This one-size-fits-all approach can lead to mismatched interactions where, for example, an introverted, anxious user receives overly energetic responses that increase rather than decrease stress, or where a highly conscientious user receives vague guidance that fails to meet their need for structure and detailed information.

Recent advances in large language models (LLMs) have enabled more nuanced and context-sensitive dialogue generation (Zheng et al., 2023; Abbasian et al., 2023). However, practical implementations still lack consistent, transparent mechanisms to adapt conversational behavior based on inferred personality traits. The gap between LLM capabilities and their application to personality-aware dialogue represents a significant opportunity for improving outcomes in diverse human-centered applications, from mental health support to educational assistance and customer service interactions.

### 1.3 Research Gap and Contribution

Existing chatbots rarely integrate dynamic trait detection with psychologically grounded regulation and reproducible evaluation frameworks. Current systems typically exhibit one or more of the following limitations: (i) minimal adaptation capabilities relying on static user profiles established during onboarding; (ii) lack of transparent trait-to-behavior mappings that would allow for scientific validation and systematic optimization; or (iii) insufficient audit trails and logging mechanisms to support rigorous assessment and quality assurance across diverse applications.

Recent work by Devdas (2025) demonstrated that real-time personality detection using the Big Five (OCEAN) framework combined with behavior regulation aligned to the Zurich Model of Social Motivation can significantly improve conversation quality, showing approximately 34% relative improvement on shared evaluation criteria versus non-adaptive baselines in controlled simulations. This empirical foundation motivates the development of a structured, reproducible pipeline for detection→regulation→generation, coupled with a comprehensive evaluation framework that isolates the specific benefits of personality-aware regulation.

This preliminary study addresses these gaps through a research-grade, N8N-orchestrated implementation featuring deterministic node contracts, comprehensive logging, and neutral fallback mechanisms. Our approach provides the transparency and reproducibility necessary for scientific validation while maintaining the operational simplicity required for practical deployment across diverse human-centered applications including mental health support, educational assistance, customer service, and general emotional companionship.

---

## 2. Topic Definition

### 2.1 Core Concepts

**Personality-adaptive emotional support chatbot.** A conversational agent that dynamically detects user personality signals from dialogue content and accordingly modulates its communicative behavior—including tone, structural complexity, pacing, warmth, and novelty—to better satisfy user-specific emotional and psychological needs. Unlike static systems that rely on predetermined user profiles, personality-adaptive chatbots continuously update their understanding of user traits and adjust their responses in real time to optimize emotional alignment and therapeutic effectiveness.

**Big Five (OCEAN) personality framework.** A well-established personality taxonomy comprising five major dimensions: Openness to experience, Conscientiousness, Extraversion, Agreeableness, and Neuroticism (McCrae & John, 1992). This framework provides a structured basis for personality inference and has been extensively validated across cultures and contexts. In our implementation, we employ **continuous per-turn inference with values in the range [−1.0, +1.0]** representing the full spectrum from low to high trait expression. This continuous representation is essential for (i) Exponential Moving Average (EMA) smoothing which requires fine-grained values to prevent quantization noise, (ii) capturing motivational intensity as conceptualized by the Zurich Model, and (iii) enabling nuanced behavioral adaptations that match the dimensional nature of personality traits established by personality psychology research (Costa & McCrae, 1992; Quirin et al., 2023).

**Zurich Model alignment.** Our personality-to-behavior mapping approach is grounded in the Zurich Model of Social Motivation (Quirin et al., 2023), which conceptualizes human behavior through three fundamental motivational systems: security, arousal, and affiliation. We operationalize this framework by mapping OCEAN traits to these motivational domains: Neuroticism influences security-related behaviors (comfort provision vs. stability reassurance), Openness and Extraversion modulate arousal through novelty and energy regulation, and Agreeableness affects affiliation through warmth and collaborative stance adjustments. Conscientiousness serves as a structural modifier, influencing the organization and specificity of guidance provided.

**Dialog grounding and safety constraints.** All system responses must be strictly grounded in the user's conversational input, employing a "quote-and-bound" approach that prevents hallucination by ensuring every assertion is entailed by recent dialogue turns. This constraint is particularly critical for human-centered applications where accuracy, reliability, and user trust are paramount.

### 2.2 Scope and Application Context

**Human-centered applications.** Our framework targets applications emphasizing personalization, empathy, and adaptive user interaction across diverse domains, specifically: mental health support, educational assistance, customer service interactions, workplace coaching, and general emotional companionship. The system is designed to complement human interaction by providing consistent availability, emotional attunement, and personality-aware responses while maintaining appropriate boundaries and escalation mechanisms when professional human intervention is needed.

**Technical scope.** The preliminary study focuses on dialog-only, prompt-only interactions without multimodal data or external knowledge retrieval in the MVP implementation. This constraint ensures privacy protection, reduces complexity, and maintains focus on the core personality detection and regulation mechanisms. Future extensions may incorporate multimodal inputs and external knowledge sources while preserving the foundational architecture.

**Evaluation framework.** Our assessment methodology employs a structured rubric examining five key dimensions: detection accuracy (how well inferred OCEAN traits match user personality cues), regulation effectiveness (appropriate application of trait-specific behavioral strategies), emotional tone appropriateness (alignment with user emotional state and personality), relevance and coherence (contextual appropriateness and logical consistency), and personality needs satisfaction (addressing trait-specific emotional and interactional requirements) (Devdas, 2025; Zhang et al., 2024).

### 2.3 Primary Use Case: Stress Self-Regulation Micro-Coach

**Target population and context.** For this preliminary study, we focus on a **stress self-regulation micro-coach for adult learners** (e.g., MSc students, bootcamp participants, professional development cohorts) managing workload pressure, deadline anxiety, and time-management challenges. This use case is selected for: (i) strong theoretical alignment with Zurich Model motivational domains (security, arousal, affiliation), (ii) minimal regulatory and ethics risk (non-clinical coaching boundary), (iii) clear measurable outcomes (engagement, stress de-escalation, coping skill adoption), and (iv) high transferability to adjacent domains (workplace coaching, customer service, educational tutoring).

**Three coaching modes (intent-based).** The system supports three primary interaction patterns mapped to common stress-related needs:

1. **Vent & Validate (Affiliation + Security):** User seeks emotional release and affect labeling. System provides empathetic acknowledgment, normalizes feelings, and helps articulate emotional states. Personality adaptations: High Neuroticism receives extra reassurance and grounding; High Agreeableness receives warm, collaborative validation; Low Agreeableness receives direct, matter-of-fact acknowledgment.

2. **Plan & Structure (Security + Arousal):** User needs time management, task prioritization, or workload breakdown. System offers structured planning support adapted to personality. High Conscientiousness receives detailed step-by-step plans with timelines; Low Conscientiousness receives flexible options avoiding rigid schedules; High Openness receives creative prioritization methods; Low Openness receives proven, familiar frameworks.

3. **Cope & Rehearse (Security + Arousal):** User requires immediate stress-relief techniques or behavioral rehearsal for challenging situations. System guides evidence-based coping strategies. High Extraversion receives social coping suggestions (talk it out, seek support); Low Extraversion receives solitary techniques (breathing exercises, journaling); High Neuroticism receives grounding exercises and safety anchors; Low Neuroticism receives challenge-focused cognitive reappraisal.

**Evidence-based techniques.** The system integrates established stress-management interventions including Mental Contrasting with Implementation Intentions (MCII) for goal-obstacle planning, Cognitive Reappraisal for reframing stressors, grounding exercises (5-4-3-2-1 sensory technique, box breathing), and micro-planning strategies (15-minute time blocks, single-task focus). All techniques are adapted to personality profiles through the Zurich Model directive mapping.

**Safety boundaries.** The system operates strictly within non-clinical coaching boundaries: no medical advice, no diagnosis, no crisis intervention beyond referral. All responses include implicit safety constraints ensuring dialog grounding, emotional appropriateness, and escalation readiness for future human-validation phases.

---

## 3. Research Questions

### 3.1 Primary Research Question

How can an adaptive LLM-based chatbot employ real-time personality detection and Zurich Model-guided behavior regulation to improve conversational quality and user-aligned emotional support compared to non-adaptive baseline systems?

This question addresses the fundamental hypothesis that dynamic personality adaptation can meaningfully enhance therapeutic outcomes in digital mental health interventions. It encompasses both the technical challenge of reliable personality inference from limited conversational data and the psychological challenge of translating personality insights into effective behavioral modifications.

### 3.2 Sub-Research Questions (Scoped for Stress Micro-Coach)

**RQ1 - Detection Mechanisms:** Can continuous OCEAN inference with EMA smoothing achieve stable, confidence-weighted personality estimates within 6–8 turns in stress-coaching dialogue contexts? This question examines: (i) prompt engineering for JSON-structured continuous values and confidence scores, (ii) EMA parameter tuning (α=0.3) for temporal stability, (iii) confidence-weighted update filtering (threshold ≥0.4), and (iv) variance reduction achieving < 0.15 post-stabilization.

**RQ2 - Regulation Strategies:** Do Zurich Model-aligned, intensity-scaled directives mapped to three coaching modes (Vent & Validate, Plan & Structure, Cope & Rehearse) improve tone appropriateness and personality-specific needs satisfaction versus a non-adaptive baseline? This addresses: (i) intent classification accuracy for coaching modes, (ii) directive-outcome alignment in personality-adapted responses, (iii) conflict resolution when multiple trait signals activate competing directives, and (iv) evidence-based technique integration (MCII, cognitive reappraisal, grounding exercises).

**RQ3 - Evaluation Methodology:** Does the scripted, blinded LLM evaluator yield ≥ 0.85 inter-run consistency and detect ≥ 20% performance gains on shared criteria (tone, relevance/coherence, needs addressed) with 95% confidence intervals? This question focuses on: (i) rubric operationalization for stress-coaching contexts, (ii) bias control through randomized assessment order and multiple independent runs, (iii) convergence of automated and human spot-check evaluations, and (iv) statistical power for detecting meaningful effect sizes.

**RQ4 - System Architecture (Reusability Focus):** Does the Personality Adapter module with config-driven policy packs enable domain transfer (stress coaching → customer service / tutoring) without code changes, while maintaining ≥ 99.5% JSON contract compliance and 100% graceful fallback coverage? This examines: (i) interface stability across use cases, (ii) policy pack swap procedures (< 30 minutes), (iii) comprehensive observability (JSONL traces, node timings, contract validation), and (iv) reproducibility measures (seed fixation, version locking, configuration snapshots).

**RQ5 - Generalization and Limitations:** How do experimental results vary between extreme simulated personality profiles (Type A: all +0.8, Type B: all -0.8) and mixed profiles (e.g., +0.6, -0.7, +0.3, +0.8, -0.4), and what scope limitations constrain transfer to live user interactions in educational and workplace settings? This addresses: (i) profile-stratified performance analysis, (ii) scenario generalization across stress contexts (workload, deadlines, interpersonal conflicts), (iii) simulation-to-human validity gaps, and (iv) ethical and safety boundaries for real-world deployment.

### 3.3 Success Criteria (Architecture-Oriented)

To ensure the system meets the objective of building a **reusable, reliable, and personality-adaptable chatbot architecture**, we define explicit success criteria across three dimensions:

**Reusability:**
- **Personality Adapter Module:** Stable API contracts for detect→regulate→generate pipeline with comprehensive interface documentation
- **Config-Driven Policy Packs:** YAML/JSON configuration files enabling domain transfer (stress coaching → customer service → tutoring) without code modifications
- **Evaluator Harness:** Portable assessment framework with pluggable rubrics and automated scoring procedures
- **Success Threshold:** Policy pack swap completed in < 30 minutes; zero breaking changes to core contracts during preliminary study

**Reliability:**
- **JSON Contract Compliance:** ≥ 99.5% valid structured outputs from detection and generation modules
- **EMA Stabilization:** ≥ 80% of sessions achieve stable personality estimates (variance < 0.15) within 6–8 turns
- **Confidence Calibration:** Low-confidence detections (< 0.4) correctly filtered; high-confidence detections (≥ 0.7) show ≥ 85% alignment with personality cues
- **Graceful Degradation:** 100% of failures handled with neutral fallback responses; zero unhandled exceptions; comprehensive error logging

**Effectiveness (vs. Non-Adaptive Baseline):**
- **Primary Outcome:** ≥ 20% relative improvement on shared evaluation criteria (tone appropriateness, relevance/coherence, personality needs addressed) with 95% confidence intervals
- **Secondary Outcomes:** 
  - Intent classification accuracy ≥ 85% for three coaching modes
  - Directive-outcome alignment ≥ 80% (evaluator-assessed)
  - Inter-run evaluator consistency ≥ 0.85 (Pearson correlation)

**Observability and Reproducibility:**
- Complete per-turn JSONL traces with OCEAN evolution, directives applied, confidence scores, and response metadata
- Reproducible seeds, version-locked models/prompts, and configuration snapshots for all experimental runs
- Automated testing suite covering contract validation, EMA convergence, and evaluator determinism

### 3.4 Mapping to Methodology

These research questions and success criteria directly inform our methodological approach: RQ1-2 are validated through comprehensive per-turn logging, directive auditing, and outcome metric analysis; RQ3 through multi-run consistency testing and systematic bias controls; RQ4 through detailed workflow instrumentation, policy pack validation, and interface stability testing; and RQ5 through systematic variation of simulation scenarios (extreme vs. mixed profiles, diverse stress contexts) and careful documentation of scope limitations.

---

## 4. Methodology

### 4.1 System Architecture Overview

We implement a reproducible, dialog-grounded pipeline featuring deterministic contracts, neutral fallback mechanisms, and comprehensive node-level logging, orchestrated through N8N workflow automation. The architecture prioritizes transparency and auditability while maintaining the operational simplicity necessary for research reproducibility and practical deployment across diverse human-centered applications.

**Implemented Architecture:**
```
Webhook → Enhanced Ingest → Load Previous State (PostgreSQL) → Combine Inputs → 
Merge Previous State → Zurich Model Detection (EMA) → Enhanced Regulation → 
Enhanced Generation → Verification & Refinement → Save to PostgreSQL 
(Sessions, Turns, Personality States) → Return API Response
```

This production-ready architecture features: (i) **Exponential Moving Average (EMA) smoothing** (α=0.3) for temporal personality stability, (ii) **PostgreSQL persistence** for longitudinal analysis across sessions, (iii) **confidence-weighted updates** filtering low-certainty detections (threshold ≥0.4), (iv) **Zurich Model-aligned regulation** mapping continuous OCEAN values to motivational directives, and (v) comprehensive audit trails with node-level logging for reproducibility and quality assurance.

### 4.2 N8N Workflow Implementation

**Figure 1. N8N Production Workflow Architecture**
```
[Webhook: POST Zurich] → [Enhanced Ingest] → [Load Previous State (PostgreSQL)]
                                                           ↓
[Combine Inputs] ← ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ┘
       ↓
[Merge Previous State] → [Zurich Model Detection (GPT-4 + EMA)]
       ↓
[Stress Assessment & Mode Classification] → [Enhanced Regulation (Directive Mapping)] → [Enhanced Generation (GPT-4)]
       ↓
[Verification & Refinement] → [Save Session (PostgreSQL)]
       ↓                              ↓
[Return API Response] ← ─ ─ ─ [Save Turns & States (PostgreSQL)]
```
*Source: `preliminary-studies/w9-Technical-Specifications/MVP/Phase-1/workflows/phase1-2-postgres-manual.json`*

**Table 1. N8N Node Specifications and Contracts**

| Node | Type | Purpose | Input Contract | Output Contract |
|------|------|---------|---------------|-----------------|
| Webhook Trigger | N8N Webhook | Accept POST requests | `{session_id, message, turn_index}` | Execution context |
| Enhanced Ingest | Code | Normalize input, validate session | Input payload | `{session_id, clean_msg, turn_index, conversation_context}` |
| Load Previous State | PostgreSQL | Retrieve last personality state | `{session_id}` | `{ocean: {O,C,E,A,N}, confidence: {...}, stable}` or empty |
| Combine Inputs | Merge | Wait for both inputs | Enhanced Ingest + PostgreSQL outputs | Combined data object |
| Merge Previous State | Code | Merge current + previous | Combined inputs | `{inputData + previous_state}` |
| Zurich Model Detection | Code/HTTP | GPT-4 personality detection + EMA | Context + previous state | `{ocean: {O,C,E,A,N ∈ [-1.0,1.0]}, confidence: {...}, stable}` |
| Stress Assessment & Mode Classification | Function/HTTP | Infer stress level (0–4), drivers, and coaching mode | `{session_id, conversation_context}` | `{stress_level: 0-4, drivers: [...], coaching_mode: vent_validate|plan_structure|cope_rehearse, confidence}` |
| Enhanced Regulation | Function | Map continuous traits to directives | `{ocean, confidence, stable}` | `{directives: [...], policy_plan: [...]}` |
| Enhanced Generation | Code/HTTP | GPT-4 regulated response | `{directives, policy_plan, context}` | `{assistant_response, metadata}` |
| Verification & Refinement | Code | Validate response quality | Generated response | `{verified_response, verification_score}` |
| Save Session | PostgreSQL | Upsert session metadata | `{session_id, total_turns}` | Success confirmation |
| Save Turns | PostgreSQL | Store conversation turns | `{session_id, turn_index, messages}` | Success confirmation |
| Save Personality State | PostgreSQL | Store EMA-smoothed OCEAN | `{session_id, turn_index, ocean, confidence, stable}` | Success confirmation |
| Return API Response | Code | Format final output | All upstream data | `{assistant_response, personality_state, session_metadata}` |

### 4.3 Detection Module: Continuous OCEAN Inference with EMA Smoothing

**Input Processing:** The detection module accepts conversational context (up to 10 previous turns) and produces continuous OCEAN personality assessments with confidence scores. Input preprocessing includes text normalization, length validation, conversation history assembly, and integration with previous personality state from PostgreSQL.

**LLM Contract Specification:**
- **Model:** GPT-4 (or GPT-4-turbo) via OpenAI-compatible API endpoint
- **Parameters:** Temperature 0.3 (balances consistency with nuance), max_tokens 300, 30-second timeout
- **Response Format:** JSON with continuous values and confidence scores:
  ```json
  {
    "ocean": {"O": [-1.0 to 1.0], "C": [-1.0 to 1.0], "E": [-1.0 to 1.0], "A": [-1.0 to 1.0], "N": [-1.0 to 1.0]},
    "confidence": {"O": [0.0 to 1.0], "C": [0.0 to 1.0], "E": [0.0 to 1.0], "A": [0.0 to 1.0], "N": [0.0 to 1.0]},
    "reasoning": "Brief explanation of detected motivations"
  }
  ```

**Exponential Moving Average (EMA) Smoothing:**

The system applies EMA smoothing to achieve temporal stability while remaining responsive to genuine personality evolution:

```javascript
// EMA Parameters
const EMA_ALPHA = 0.3;  // Weight for current detection (30%)
const MIN_CONFIDENCE_THRESHOLD = 0.4;  // Minimum confidence to update
const STABILIZATION_TURNS = 6;  // Turns required for stability designation

// Per-trait smoothing
for (trait in ['O', 'C', 'E', 'A', 'N']) {
  if (currentConfidence[trait] >= MIN_CONFIDENCE_THRESHOLD) {
    smoothed[trait] = EMA_ALPHA * current[trait] + (1 - EMA_ALPHA) * previous[trait];
  } else {
    smoothed[trait] = previous[trait];  // Keep previous if confidence too low
  }
}

// Stability determination
stable = (consistentTurns >= STABILIZATION_TURNS && variance < 0.15);
```

**Confidence-Weighted Updates:** GPT-4 self-assesses confidence based on evidence clarity, consistency with previous turns, and behavioral indicator strength. Low-confidence detections (< 0.4) are filtered to prevent noise from corrupting the personality profile.

**Example Evolution Across 6 Turns:**
```
Turn 1: detected=0.5, conf=0.6  → smoothed = 0.3×0.5 + 0.7×0.0 = 0.15
Turn 2: detected=0.7, conf=0.7  → smoothed = 0.3×0.7 + 0.7×0.15 = 0.315
Turn 3: detected=0.6, conf=0.9  → smoothed = 0.3×0.6 + 0.7×0.315 = 0.40
Turn 4: detected=0.8, conf=0.8  → smoothed = 0.3×0.8 + 0.7×0.40 = 0.52
Turn 5: detected=0.7, conf=0.8  → smoothed = 0.3×0.7 + 0.7×0.52 = 0.574
Turn 6: detected=0.7, conf=0.9  → smoothed = 0.3×0.7 + 0.7×0.574 = 0.612
                                   → STABLE = TRUE (6 consistent turns, low variance)
```

### 4.4 Regulation Module: Zurich Model-Aligned Behavior Mapping

The regulation module translates continuous OCEAN personality assessments into specific behavioral directives that guide response generation. This mapping is grounded in the Zurich Model's three motivational domains (Security, Arousal, Affiliation) and leverages threshold-based activation (|value| ≥ 0.2) to produce psychologically coherent conversational adaptations. Continuous values enable intensity-proportional directives: stronger trait expressions generate more emphatic guidance.

**Table 2. Continuous Trait-to-Directive Mapping Schema**

| Trait | Threshold | Zurich Domain | Behavioral Directive (Intensity-Scaled) |
|-------|-----------|---------------|----------------------------------------|
| **Openness (O)** | O > 0.2 | Arousal | "Introduce novel concepts and creative perspectives" (scaled by O value) |
| | O < -0.2 | Arousal | "Use concrete, familiar examples; avoid abstract novelty" (scaled by |O|) |
| **Conscientiousness (C)** | C > 0.2 | Structure | "Provide structured plans with clear steps and organization" (scaled by C) |
| | C < -0.2 | Structure | "Keep guidance flexible; avoid rigid timelines or prescriptive steps" (scaled by |C|) |
| **Extraversion (E)** | E > 0.2 | Arousal | "Use energetic, engaging tone; frame as collaborative" (scaled by E) |
| | E < -0.2 | Arousal | "Adopt calm, reflective tone; respect need for introspection" (scaled by |E|) |
| **Agreeableness (A)** | A > 0.2 | Affiliation | "Use warm, empathetic language; emphasize cooperation" (scaled by A) |
| | A < -0.2 | Affiliation | "Maintain matter-of-fact, direct stance; respect autonomy" (scaled by |A|) |
| **Neuroticism (N)** | N > 0.2 | Security | "Provide reassurance; acknowledge concerns; offer coping strategies" (scaled by N) |
| | N < -0.2 | Security | "Match confident tone; focus on pragmatic solutions" (scaled by |N|) |

**Directive Intensity Scaling Example:**
```javascript
// Conscientiousness C = -0.7 (strong avoidance of structure)
if (C < -0.2 && confidence_C >= 0.4) {
  intensity = Math.abs(C);  // 0.7
  if (intensity > 0.6) {
    directive = "Strongly emphasize flexibility; actively avoid any rigid frameworks or detailed schedules";
  } else if (intensity > 0.4) {
    directive = "Provide flexible options; minimize structure";
  } else {
    directive = "Keep guidance somewhat flexible";
  }
}
```

**Conflict Resolution:** Continuous values enable nuanced harmonization. For O=0.7 (moderate novelty-seeking) with E=-0.5 (moderate introversion): "Introduce creative ideas through calm, thoughtful exploration that respects personal reflection time." The system weights directives by trait magnitude and confidence, producing coherent multi-trait adaptations.

### 4.5 Generation Module: Quote-and-Bound Response Production

**Response Constraints:**
- **Grounding:** All responses must be strictly grounded in user's conversational input; no external claims or information
- **Length:** 70-150 words to ensure substantive but focused responses
- **Interaction:** Maximum 2 questions per response to maintain conversational flow
- **Parameters:** Temperature 0.7, max_tokens 220, 20-second timeout
 - **Safety:** If `stress_level ≥ 3` and crisis indicators (e.g., self-harm/violence terms) are detected, return a neutral, supportive message with escalation guidance; never provide clinical advice.

**Prompt Construction:** The generation prompt integrates behavioral directives with strict grounding constraints:
```
"You are a supportive assistant. Follow these behavior directives strictly: [concatenated directives]. 
Coaching mode: {coaching_mode}. 
Constraints: Stay grounded in the user's text only; ask at most 1-2 questions; respond in 70-150 words."
```

**Error Handling:** On generation failure, the system provides a supportive fallback message while preserving all metadata fields for debugging and continuity: "I'm here to support you. Could you tell me more about how you're feeling?" with full session context maintained.

### 4.6 PostgreSQL Database Schema and Persistence

**Database Architecture:** The system employs PostgreSQL for comprehensive state management, enabling longitudinal personality tracking, conversation replay, and research analysis.

**Table 3. Database Schema Overview**

| Table Name | Primary Key | Purpose | Key Columns |
|------------|-------------|---------|-------------|
| `chat_sessions` | `session_id` (UUID) | Session metadata | `total_turns`, `evaluation_mode`, `status`, `created_at` |
| `conversation_turns` | `(session_id, turn_index)` | Conversation history | `user_message`, `assistant_response`, `directives_applied`, `coaching_mode`, `stress_level`, `stress_drivers` |
| `personality_states` | `(session_id, turn_index)` | EMA-smoothed OCEAN values | `ocean_o/c/e/a/n`, `confidence_o/c/e/a/n`, `stable`, `ema_applied` |
| `performance_metrics` | `(session_id, turn_index)` | System performance | `detection_latency_ms`, `generation_latency_ms`, `total_tokens` |

**Helper Functions:**
```sql
-- Retrieve latest personality state for session
CREATE FUNCTION get_latest_personality_state(p_session_id UUID)
RETURNS TABLE(ocean_o FLOAT, ocean_c FLOAT, ocean_e FLOAT, ocean_a FLOAT, ocean_n FLOAT, ...);

-- Get conversation history for context window
CREATE FUNCTION get_conversation_history(p_session_id UUID, p_limit INTEGER)
RETURNS TABLE(turn_index INTEGER, user_message TEXT, assistant_response TEXT);
```

**Data Flow:**
1. **Turn Start:** Load previous personality state from `personality_states` table
2. **Detection:** GPT-4 analyzes conversation → produces raw OCEAN + confidence
3. **EMA Smoothing:** Blend current with previous state (α=0.3)
4. **Persistence:** Save smoothed state, conversation turn, session metadata to PostgreSQL
5. **Next Turn:** Retrieve smoothed state as `previous_state` for EMA continuity

### 4.7 Dialogue Simulation Protocol (Stress Micro-Coach Scenarios)

**Personality Profiles (Continuous):**
- **Type A (High OCEAN):** OCEAN values approximately (+0.8, +0.8, +0.8, +0.8, -0.8) representing open, conscientious, extraverted, agreeable, emotionally stable users
- **Type B (Low OCEAN):** OCEAN values approximately (-0.8, -0.8, -0.8, -0.8, +0.8) representing closed, disorganized, introverted, disagreeable, emotionally sensitive users
- **Type C (Mixed Profile):** e.g., (+0.6, -0.7, +0.3, +0.8, -0.4) for generalization testing (moderate openness, low conscientiousness, slight extraversion, high agreeableness, moderate emotional stability)
- **Expected Variance:** ±0.15 per trait to simulate natural conversation variability

**Stress-Coaching Scenarios (Intent Coverage):**
Each personality profile engages in three standardized stress scenarios covering all coaching modes:

1. **Workload Overload (Vent & Plan):** "I have three major deadlines this week and I don't know where to start. Everything feels overwhelming..." → Expected intents: Vent & Validate (turns 1-3), Plan & Structure (turns 4-8)

2. **Deadline Anxiety (Cope & Plan):** "My thesis defense is in two days and I'm panicking. I can't focus and my mind keeps racing..." → Expected intents: Cope & Rehearse (turns 1-4), Plan & Structure (turns 5-8)

3. **Interpersonal Conflict (Vent & Cope):** "I had a difficult meeting with my supervisor and I'm still upset about it. I don't know how to handle the next conversation..." → Expected intents: Vent & Validate (turns 1-4), Cope & Rehearse (turns 5-10)

**Conversation Structure:**
- **Length:** 8-10 turns per conversation to allow EMA convergence and stability assessment
- **Replication:** 10-15 sessions per personality profile × 3 scenarios = 90-135 total conversations
- **Turn Composition:** User messages exhibit clear personality cues aligned with profile; assistant responses logged with applied directives and coaching mode classification
- **Convergence Tracking:** Monitor when `stable=TRUE` flag activates (target: turns 6-8 for ≥ 80% sessions)

**Baseline Condition (Non-Adaptive):**
For comparative evaluation, generate parallel conversations using a generic empathetic assistant prompt without personality detection or Zurich Model regulation. Baseline receives identical user messages to enable direct comparison on shared criteria (tone, relevance/coherence, needs addressed).

**Data Export:** PostgreSQL queries generate comprehensive CSV/JSONL logs including:
- Per-turn OCEAN evolution (raw detection + EMA-smoothed + confidence)
- Applied directives, coaching mode classifications, and policy plans
- Response latencies, token usage, and contract compliance flags
- Stability flags, convergence metrics, and variance tracking
- Scenario metadata (workload/deadline/interpersonal) for stratified analysis

### 4.8 Evaluation Framework

**Assessment Dimensions:**

*For EMA-Regulated Assistants (7 criteria):*
1. **Detection Accuracy:** Alignment between continuous OCEAN inference and simulated personality cues
2. **EMA Convergence Quality:** Smooth progression toward stable personality estimate (low variance, appropriate α)
3. **Confidence Calibration:** Appropriate confidence scores matching evidence strength
4. **Regulation Effectiveness:** Appropriate application of intensity-scaled behavioral strategies
5. **Emotional Tone Appropriateness:** Match between response tone and user emotional state/personality
6. **Relevance & Coherence:** Contextual appropriateness and logical consistency
7. **Personality Needs Addressed:** Satisfaction of trait-specific emotional and interactional requirements

*For Baseline Assistants (3 criteria):*
1. **Emotional Tone Appropriateness**
2. **Relevance & Coherence**  
3. **Personality Needs Addressed**

**Table 4. Evaluation Matrix Schema (Continuous Values)**

| Row | Profile | Turn | User Message | Assistant Reply | OCEAN (Smoothed) | Confidence | Stable | Directives | Det.Acc | EMA.Conv | Conf.Cal | Reg.Eff | Tone | Rel&Coh | Needs | Total |
|-----|---------|------|--------------|-----------------|------------------|------------|--------|------------|---------|----------|----------|---------|------|---------|-------|-------|
| 1 | A-High | 6 | "I'm excited to try new approaches..." | "That's wonderful! Let's explore some creative strategies..." | O:0.78, C:0.65, E:0.82, A:0.71, N:-0.68 | O:0.85, C:0.78, ... | TRUE | ["Introduce novel ideas", "Energetic tone", "Structured steps"] | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 14 |
| 2 | B-Low | 6 | "Everything feels uncertain..." | "I understand uncertainty is difficult. Let's focus on what you can control..." | O:-0.72, C:-0.68, E:-0.75, A:-0.61, N:0.79 | O:0.81, C:0.76, ... | TRUE | ["Familiar examples", "Calm tone", "Flexible guidance", "Extra comfort"] | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 14 |

**EMA-Specific Metrics:**
- **Convergence Rate:** Turns required to reach `stable=TRUE` (target: 6-8 turns)
- **Smoothness:** Variance in OCEAN values across turns (target: < 0.15 after stabilization)
- **Confidence-Weighted Accuracy:** Correlation between confidence scores and actual detection accuracy
- **Temporal Consistency:** Autocorrelation of OCEAN values (should be high, r > 0.7)

**Scoring Protocol:**
- **Scale:** Trinary scoring (Yes=2, Partial=1, No=0) for each criterion
- **Aggregation:** Per-session averages, per-profile comparisons, stability-stratified analysis
- **Evaluator:** GPT-4-based scripted evaluator with fixed prompts, blinded assessment, randomized order
- **Bias Control:** Multiple evaluation runs, inter-run consistency ≥ 0.85, systematic prompt validation

**Visualization:** 
- Time-series plots showing OCEAN evolution with EMA smoothing
- Convergence curves comparing different personality profiles
- Bar charts comparing regulated vs. baseline performance with 95% confidence intervals
- Heatmaps showing trait-directive-outcome relationships

### 4.9 Key Advantages of Continuous + EMA Architecture

**Theoretical Alignment:**
- **Zurich Model Fidelity:** Continuous values capture motivational intensity as conceptualized in the Zurich Model (Quirin et al., 2023), not just categorical "high/low" states
- **Big Five Foundations:** Aligns with NEO-PI-R and established personality psychology which treat traits as dimensional, not categorical (Costa & McCrae, 1992)
- **Information Preservation:** 79% more information content vs. discrete {-1, 0, 1} representation (38 bits vs. 8 bits for all 5 traits)

**Technical Benefits:**
- **EMA Smoothing Feasibility:** Discrete values create quantization noise preventing convergence; continuous enables smooth temporal tracking
- **Fine-Grained Adaptation:** Can distinguish moderate (0.3) from strong (0.8) trait expression, enabling proportional directive intensity
- **Confidence Weighting:** Low-confidence detections filtered without binary commit/reject decisions
- **Statistical Power:** Enables proper correlation, regression, and distributional analysis for research validation

**Practical Impact:**
- **Reduced Flickering:** EMA prevents personality estimates from jumping erratically between turns
- **Graceful Evolution:** System adapts gradually as it gathers evidence, mimicking human personality perception
- **Longitudinal Tracking:** PostgreSQL persistence enables analysis of personality stability across extended interactions
- **Research Reproducibility:** Continuous logs support detailed analysis of detection accuracy, convergence dynamics, and regulation effectiveness

**Comparison with Discrete Baseline:**
```
Discrete System: Turn 1: +1 → Turn 2: +1 → Turn 3: 0 → Turn 4: +1 (flickering)
Continuous + EMA: Turn 1: 0.15 → Turn 2: 0.31 → Turn 3: 0.40 → Turn 4: 0.52 (smooth)
```

### 4.10 Automation and Reproducibility Measures

**Parameter Fixation:**
- Model versions and API endpoints documented and archived
- Temperature, token limits, and timeout values specified in configuration files
- Random seeds fixed for all stochastic processes
- Prompt versions tracked with cryptographic hashes

**Comprehensive Logging:**
- Per-turn JSONL files with complete interaction traces
- Node execution timings and error rates
- Configuration snapshots for each experimental run
- Automated CSV export for statistical analysis

**Safety and Error Handling:**
- Neutral fallback responses for all failure modes
- Dialog-only grounding enforcement
- Comprehensive error logging with stack traces
- Graceful degradation maintaining conversation continuity

---

## 5. Underlying Data Sources

### 5.1 Technical Documentation Repository

**Comprehensive Technical Documentation:**
The implementation is supported by extensive technical documentation covering all system aspects:

| Document | Location | Purpose | Key Content |
|----------|----------|---------|-------------|
| **EMA Implementation** | `MVP/Docs/EMA_IMPLEMENTATION_DETAILED.md` | Complete EMA technical breakdown | α=0.3 parameter justification, node-by-node flow, PostgreSQL schema, turn-by-turn examples, convergence analysis |
| **Continuous Values Rationale** | `MVP/Docs/CONTINUOUS_VS_DISCRETE_PERSONALITY_VALUES.md` | Justification for continuous representation | Theoretical foundation (Zurich Model, Big Five), mathematical proofs, 79% information gain analysis, academic citations |
| **Confidence Calculation** | `MVP/Docs/CONFIDENCE_CALCULATION_EXPLAINED.md` | GPT-4 self-assessment mechanism | How confidence scores are generated, filtering thresholds, calibration examples, EMA integration |
| **Database Design** | `MVP/Docs/DATABASE_DESIGN_AND_DATAFLOW.md` | PostgreSQL architecture | Complete schema (4 tables, helper functions), data flow diagrams, indexing strategy, ER diagrams, query examples |
| **Zurich Model Application** | `MVP/Docs/ZURICH_MODEL_APPLICATION.md` | Complete Zurich Model framework | Approach-avoidance motivation theory, OCEAN-to-directive mapping, practical examples (mental health, education, customer service), 90KB comprehensive guide |
| **Workflow Explanation** | `MVP/Phase-1/docs/WORKFLOW_DETAILED_EXPLANATION.md` | Complete N8N workflow documentation | Node-by-node breakdown, data contracts, error handling, 30KB technical reference |
| **Deployment Guide** | `MVP/Phase-1/docs/PHASE1_DEPLOYMENT_GUIDE.md` | Production deployment procedures | Environment setup, configuration, testing, monitoring |
| **Troubleshooting Docs** | `MVP/Phase-1/docs/` (4 fix guides) | Bug fixes and solutions | SESSION_ID_FIX, MERGE_STATE_DEBUG_FIX, POSTGRESQL_CONNECTION_FIX, COMBINE_INPUTS_FIX |

**Total Documentation:** 200+ pages (7 major documents + 4 troubleshooting guides) covering theoretical foundations, implementation details, and operational procedures.

### 5.2 Simulated Dialogue Components

**Personality Type A/B Simulation Scripts**
- **Location:** `preliminary-studies/w9-Technical-Specifications/MVP/workflows/` and associated script directories
- **Content:** Carefully crafted user messages exhibiting clear personality indicators across OCEAN dimensions
- **Validation:** Scripts reviewed for psychological authenticity and trait clarity by domain experts
- **License/Usage:** Internal research use; compliance with LLM provider Terms of Service ensured
- **Format:** Structured JSON with personality labels, message content, and expected trait indicators

**Example Type A (High OCEAN ~0.8) Messages with Expected Detection:**
- "I'm really excited to explore new creative approaches!" 
  - Expected: O≈0.7-0.9, E≈0.6-0.8, confidence O/E≥0.7
- "I've created a comprehensive organizational system with clear milestones."
  - Expected: C≈0.7-0.9, confidence C≥0.8
- "I deeply value collaboration and everyone's contributions."
  - Expected: A≈0.6-0.9, confidence A≥0.7
- "I feel confident and optimistic about handling challenges."
  - Expected: N≈-0.6 to -0.8 (emotionally stable), confidence N≥0.7

**Example Type B (Low OCEAN ~-0.8) Messages with Expected Detection:**
- "I prefer sticking to familiar, proven methods rather than experimenting."
  - Expected: O≈-0.6 to -0.9, confidence O≥0.7
- "My approach is flexible and spontaneous; I don't plan much."
  - Expected: C≈-0.6 to -0.9, confidence C≥0.8
- "I work best independently with minimal social interaction."
  - Expected: E≈-0.6 to -0.9, confidence E≥0.7
- "I feel anxious and worried about uncertain situations."
  - Expected: N≈0.6 to 0.9 (high neuroticism), confidence N≥0.8

**Convergence Tracking Example:**
```
Session: Type A User, Openness Trait
Turn 1: "I love trying new things!" → detected=0.7, conf=0.6 → EMA=0.21
Turn 3: "Novel ideas fascinate me" → detected=0.8, conf=0.8 → EMA=0.45
Turn 6: "Change excites me" → detected=0.75, conf=0.85 → EMA=0.68 → STABLE
```

### 5.2 Detection and Regulation Prompt Libraries

**Versioned Prompt Collection**
- **Location:** Appendix A with cross-references to workflow node implementations
- **Content:** JSON-structured detection prompts, behavioral directive templates, generation constraints
- **Versioning:** Semantic versioning (v1.0.0) with change logs for prompt modifications
- **License/Usage:** Authored for this study; available for research use with attribution
- **Validation:** Prompts tested for consistency, clarity, and effectiveness across multiple model versions

**Detection Prompt Template (Continuous + Confidence):**
```
You are a Zurich Model personality detection system. Analyze the conversation 
to infer Big Five (OCEAN) personality traits as continuous approach-avoidance 
motivational dimensions.

Return JSON:
{
  "ocean": {"O": [-1.0 to 1.0], "C": [-1.0 to 1.0], "E": [-1.0 to 1.0], 
            "A": [-1.0 to 1.0], "N": [-1.0 to 1.0]},
  "confidence": {"O": [0-1], "C": [0-1], "E": [0-1], "A": [0-1], "N": [0-1]},
  "reasoning": "Brief motivational analysis"
}

Focus on:
- WHY user behaves (motivation) not just WHAT they do
- Approach vs avoidance language patterns
- Consistency with previous turns
- Evidence clarity (determines confidence)

Conversation History: {last_10_turns}
Current Message: {user_message}
```

**Generation Constraint Template (Directive-Driven):**
```
You are a supportive assistant. Follow these Zurich Model-aligned behavioral 
directives:
{directives_list}

Policy Plan: {policy_plan}

CONSTRAINTS:
- Ground all responses in user's text only
- Respond in 70-150 words
- Ask at most 1-2 questions
- Match emotional tone to personality (detected: {ocean_values})

User Message: {user_message}
Context: {conversation_context}
```

### 5.3 Evaluation Materials and Rubrics

**Scripted Evaluator Components**
- **Location:** Appendix B with complete rubric definitions and decision trees
- **Content:** Criterion definitions, scoring guidelines, example evaluations, bias control procedures
- **Derivation:** Adapted from Devdas (2025) evaluation framework with modifications for automated scoring
- **License/Usage:** Research use; methodology available for replication studies
- **Validation:** Inter-rater reliability testing with human evaluators (planned for thesis phase)

**Evaluation Rubric Excerpt:**
```
Detection Accuracy: Does the ocean_disc vector appropriately reflect personality cues in the user's message?
- Yes (2): Clear alignment between detected traits and behavioral indicators
- Partial (1): Some alignment but missing or incorrect trait assessments
- No (0): Poor alignment or systematic misdetection
```

### 5.4 Optional External Corpora

**Emotional Support Datasets (Future Extension)**
- **Purpose:** Qualitative validation and naturalistic testing
- **Sources:** Public datasets such as ESConv (Emotional Support Conversations) with appropriate licensing
- **Usage:** Supplementary analysis only; no PII or sensitive content
- **Preprocessing:** Anonymization, content filtering, personality annotation by trained raters
- **Compliance:** Full adherence to dataset licenses and ethical guidelines

### 5.5 Experimental Logs and Artifacts

**Data Storage and Management**
- **Location:** `preliminary-studies/preliminary-handover/output/` (to be created during execution)
- **Format:** JSONL for raw logs, CSV for analysis, PNG/SVG for visualizations
- **Content:** Complete interaction traces, evaluation scores, timing data, error logs
- **Anonymization:** No personal data in MVP; anonymization protocols established for future human studies
- **Retention:** Data retained for replication and follow-up studies with appropriate security measures
- **Backup:** Version-controlled storage with regular automated backups

---

## 6. Technology, Software, and Applications

### 6.1 Orchestration Platform Selection

We prioritize an N8N-first architecture to maximize transparency, operational simplicity, and research reproducibility while maintaining the flexibility necessary for iterative development and potential production deployment.

**Table 4. Comprehensive Technology Stack Justification**

| Layer | Primary Choice | Version | Alternatives Considered | Selection Rationale |
|-------|---------------|---------|------------------------|-------------------|
| **Orchestration** | N8N | ≥1.x | crewAI, AutoGen, custom FastAPI | Visual workflow design enables transparent audit trails; node-based architecture matches experimental design; rapid iteration capabilities; production-grade with PostgreSQL integration |
| **LLM (Detection)** | GPT-4 / GPT-4-turbo | Latest stable | Gemini 1.5 Pro, Claude-3, Llama-2 | Superior personality inference capabilities; reliable JSON-structured outputs with confidence scores; extensive validation in personality psychology research |
| **LLM (Generation)** | GPT-4 / GPT-4-turbo | Latest stable | Gemini 1.5 Pro, Claude-3 | Excellent directive-following; nuanced emotional tone adaptation; consistency with detection model for personality coherence |
| **API Gateway** | OpenAI-compatible | Current | ai.juguang.chat, Direct OpenAI | Standard OpenAI API format; broad model compatibility; enterprise-grade reliability and rate limiting |
| **Storage/State** | PostgreSQL | 13+ | JSONL+CSV, Redis, MongoDB | **Production-grade persistence**; ACID compliance for personality state integrity; powerful querying for longitudinal analysis; helper functions for EMA operations |
| **Evaluation** | GPT-4-based Evaluator | v1.0 | Human raters, Claude, automated metrics | Consistent scoring across thousands of interactions; validated rubric adherence; blinded assessment capability |
| **State Management** | PostgreSQL + EMA | α=0.3 | In-memory caching, Redis | **Temporal smoothing** with database persistence; enables cross-session personality continuity; research-grade audit trails |
| **Containerization** | Docker Compose | Latest | Kubernetes, bare metal | Local development simplicity; PostgreSQL containerization; straightforward N8N deployment |
| **Visualization** | Python (Matplotlib + Seaborn) | 3.8+ | R/ggplot2, Plotly | Publication-quality time-series plots; EMA convergence visualization; statistical analysis integration |

### 6.2 Development Environment and Configuration

**Environment Management:**
- **Configuration:** Environment variables via `.env` files and N8N credential vault
- **Documentation:** Complete setup procedures in `MVP/README.md`
- **Dependencies:** Locked versions in `requirements.txt` and `package.json`
- **Secrets:** API keys managed through N8N's encrypted credential system

**Container Architecture:**
```yaml
# docker-compose.yml excerpt
services:
  n8n:
    image: n8nio/n8n:latest
    environment:
      - N8N_BASIC_AUTH_ACTIVE=true
      - WEBHOOK_URL=http://localhost:5678
    volumes:
      - n8n_data:/home/node/.n8n
      - ./workflows:/home/node/.n8n/workflows
  
  postgres:
    image: postgres:13
    environment:
      - POSTGRES_DB=n8n_research
      - POSTGRES_USER=n8n
    volumes:
      - postgres_data:/var/lib/postgresql/data
```

**Model Configuration Parameters:**
- **Detection:** Temperature 0.1, max_tokens 200, timeout 20s
- **Generation:** Temperature 0.7, max_tokens 220, timeout 20s  
- **Retry Logic:** Exponential backoff with maximum 3 attempts
- **Rate Limiting:** Compliance with API provider limits (requests/minute)

### 6.3 Quality Assurance and Testing Framework

**Automated Testing Suite:**
- **Unit Tests:** Individual node functionality validation
- **Integration Tests:** End-to-end workflow execution verification
- **Performance Tests:** Latency and throughput measurement under load
- **Regression Tests:** Consistency validation across model updates

**Testing Scripts (Available in MVP/):**
- `test_personality_chatbot.sh`: Complete workflow validation
- `test_detection_accuracy.sh`: Trait inference verification  
- `test_regulation_coherence.sh`: Directive mapping validation
- `bypass_login.sh`: Development environment setup

**Monitoring and Observability:**
- **Workflow Metrics:** Node execution times, success rates, error frequencies
- **Model Performance:** Token usage, response quality, API reliability
- **System Health:** Memory usage, disk space, network connectivity
- **Alert System:** Automated notifications for failures or performance degradation

### 6.4 Security and Privacy Considerations

**Data Protection:**
- **Encryption:** All data at rest and in transit using AES-256 encryption
- **Access Control:** Role-based permissions for workflow modification and data access
- **Audit Trails:** Comprehensive logging of all system interactions and modifications
- **Data Minimization:** Collection limited to research-essential information only

**API Security:**
- **Authentication:** Secure API key management through N8N credential vault
- **Rate Limiting:** Compliance with provider limits to prevent service disruption
- **Error Handling:** Sanitized error messages preventing information leakage
- **Network Security:** HTTPS enforcement for all external communications

**Privacy Compliance:**
- **Anonymization:** No personal identifiers in research data
- **Consent Protocols:** Established procedures for any future human participant studies
- **Data Retention:** Clear policies for data lifecycle management
- **Regulatory Compliance:** GDPR and institutional review board requirements addressed

### 6.5 Scalability and Production Considerations

**Performance Optimization:**
- **Caching:** Response caching for identical personality profiles and directives
- **Batch Processing:** Efficient handling of multiple conversation evaluations
- **Resource Management:** Memory and CPU optimization for sustained operation
- **Load Balancing:** Horizontal scaling capabilities for increased throughput

**Deployment Strategies:**
- **Development:** Local Docker Compose for research and testing
- **Staging:** Cloud-based deployment for integration testing
- **Production:** Kubernetes orchestration for scalable real-world deployment (future)
- **Backup and Recovery:** Automated backup procedures with point-in-time recovery

**Maintenance and Updates:**
- **Model Versioning:** Systematic tracking of LLM model updates and performance impacts
- **Workflow Evolution:** Version control for N8N workflow modifications
- **Dependency Management:** Regular security updates and compatibility testing
- **Documentation:** Comprehensive technical documentation and user guides

---

## 7. Annotated Disposition

This section provides a comprehensive overview of the preliminary study structure and anticipated thesis development, with each component annotated to clarify its purpose and contribution to the overall research program.

### 7.1 Thesis Structure (Annotated)

**Chapter 1: Introduction** — Context and motivation; problem statement; thesis objective: demonstrate a reusable, reliable, personality‑adaptable architecture via the Stress Self‑Regulation Micro‑Coach (derived from this preliminary study).

**Chapter 2: Literature Review and Research Gaps** — Personality‑adaptive dialogue systems; Zurich Model foundations; stress assessment in dialog; evaluation methodologies; derive gaps and hypotheses that the architecture addresses.

**Chapter 3: Methodology and System Design** — N8N pipeline design; modular Personality Adapter (Detection: continuous OCEAN+EMA; Regulation: policy‑pack Zurich mapping; Generation: quote‑and‑bound + verification); stress assessment & mode classification; privacy/safety; database schema.

**Chapter 4: Implementation and Validation** — Workflow implementation details; contract checks; simulation protocols (Type A/B/Mixed across stress scenarios); automated evaluator setup; metrics and analysis scripts.

**Chapter 5: Results** — Detection validity (expert agreement, ICC, BFI‑44 correlation); regulation effectiveness; tone/relevance/needs outcomes vs. baseline; safety/reliability; ablations; cost metrics.

**Chapter 6: Discussion** — Interpretation; relation to prior work; threats to validity; fairness and ethics; generalization to other domains; implications for reusable research infrastructure.

**Chapter 7: Conclusion** — Contributions: validated architecture, standardized evaluation protocols, stress micro‑coach demonstration; limitations; roadmap for future research (caregiver support, customer service, tutoring); open‑science assets.

**Appendices** — Prompts and schemas; workflow JSON; evaluation rubric; statistical analysis code; reproducibility checklist; consent/privacy templates.

### 7.2 Thesis Extension Framework

**Enhanced System Architecture** — The thesis phase will extend the MVP implementation with temporal smoothing algorithms (exponential moving averages for trait stability), response verification modules (policy adherence and grounding validation), and comprehensive state persistence (PostgreSQL integration for longitudinal analysis).

**Human Validation Studies** — Following successful simulation-based validation, the thesis will incorporate human participant studies with appropriate ethical oversight, informed consent procedures, and professional supervision. These studies will validate the generalizability of simulation results and provide insights into real-world deployment challenges across diverse application domains.

**Advanced Evaluation Methodologies** — The thesis will incorporate human evaluators alongside automated scoring, develop inter-rater reliability measures, and conduct longitudinal assessment of conversation quality over extended interactions. This multi-faceted evaluation approach will strengthen the evidence base for human-centered applications.

**Application Integration Pathway** — The thesis will explore integration with existing systems across various domains, develop adaptive decision support features, and establish protocols for escalation to human support when appropriate. This work will bridge the gap between research prototype and practical deployment in diverse human-centered applications.

**Multimodal Extensions** — Future work may incorporate voice analysis, facial expression recognition, and physiological monitoring to enhance personality detection accuracy and provide more comprehensive emotional state assessment. These extensions will be carefully evaluated for privacy implications and practical utility across diverse application contexts.

### 7.3 Publication and Dissemination Strategy

**Academic Publications** — Results will be submitted to peer-reviewed venues spanning computer science (CHI, AAAI), psychology (Journal of Personality and Social Psychology), and human-computer interaction (TOCHI, CSCW) to reach interdisciplinary audiences.

**Open Source Contributions** — The N8N workflow, evaluation framework, and analysis tools will be made available under appropriate open source licenses to support replication and community development.

**Industry and Professional Community Engagement** — Findings will be presented at technology, education, and digital interaction conferences to facilitate adoption by practitioners across diverse domains and inform best practice guidelines.

**Policy and Regulatory Input** — The research will contribute to emerging regulatory frameworks for AI systems by providing evidence-based guidance on safety, efficacy, and ethical deployment of personality-aware conversational systems across human-centered applications.

---


## 8. Project Risks

### 8.1 Risk Assessment Framework

This section presents a comprehensive analysis of potential challenges that could impact the successful completion of this preliminary study, organized by risk category with detailed mitigation strategies and responsibility assignments.

Scoring method and heat levels (inspired by caregiver roadmap): Likelihood and Impact are assessed on a 3‑level scale (Low/Medium/High). Heat is the qualitative product of the two; items with Medium×High or High×Medium and above trigger mitigation playbooks and weekly review.

**Table 5. Comprehensive Project Risk Matrix**

| Risk Category | Specific Risk | Likelihood | Impact | Owner | Mitigation Strategy | Early Indicators | Timeline |
|---------------|---------------|------------|---------|--------|-------------------|-----------------|----------|
| **Data Quality** | Simulated personality profiles lack realism | Medium | Medium | Author | Validate with psychology experts; add mid‑range profiles; pilot human validation | Low evaluator agreement; anomalous directive patterns | Weeks 2-3 |
| **Evaluation** | LLM evaluator bias or drift | Medium | High | Author | Fixed prompts with hashes; 3× runs; randomized order; human spot‑checks | Inter‑run consistency < 0.85; sudden score shifts | Ongoing |
| **Technical** | Prompt sensitivity affecting consistency | Medium | Medium | Author | Prompt versioning; A/B tests; directive auditing | Regression in JSON compliance; style oscillations | Weeks 3-4 |
| **Reproducibility** | Non‑determinism in model responses | Medium | High | Author | Pin model versions; fixed seeds; full config logging | Re‑runs diverge > 5% on shared metrics | Week 1 |
| **Performance** | Latency exceeding thresholds | Low | Medium | Author | Timeout caps; token budgets; single‑pass pipeline | p95 latency > 2s; timeouts > 1% | Weeks 4-5 |
| **Ethics/Privacy** | Data protection gaps | Low | High | Author + Supervisor | Anonymization; encryption; access control; IRB as needed | Missing audit logs; access without RBAC | Week 1 |
| **Infrastructure** | Vendor/service interruptions | Medium | Medium | Author | Provider abstraction; alternates ready; backoff/retry | API error rate spikes; throttling events | Ongoing |
| **Scope** | Feature creep beyond MVP | Medium | Medium | Author | Scope guardrails; change control; defer to thesis | Backlog growth; missed milestones | Ongoing |
| **Validation** | Weak reproducibility documentation | Low | High | Author | JSONL traces; config snapshots; scripts | Missing artifacts; non‑runnable analyses | Ongoing |
| **Operations** | Manual execution errors | Medium | Medium | Author | Automation; dry‑runs; recovery procedures | Frequent hotfixes; repeated manual steps | Weeks 5-6 |

### 8.2 Risk Mitigation Strategies and Playbooks

**Data Quality Assurance**
To address concerns about the realism of simulated personality profiles, we will conduct systematic validation with domain experts in personality psychology. The initial extreme profiles (Type A: all +1s, Type B: all -1s) will be supplemented with mid-range combinations that reflect more naturalistic personality patterns. Additionally, the thesis phase will incorporate human participant validation to assess the ecological validity of simulation results.

**Evaluation Reliability**
The risk of evaluator bias represents a significant threat to research validity. Our mitigation approach includes: (1) fixed evaluation prompts with cryptographic hashing to prevent drift, (2) multiple independent evaluation runs with consistency analysis, (3) randomized assessment order to prevent systematic biases, (4) human spot-checking of automated evaluations, and (5) inter-rater reliability testing in the thesis phase.

**Technical Robustness**
Prompt sensitivity could undermine the consistency and reproducibility of results. We address this through systematic prompt versioning with semantic version numbers, A/B testing of prompt variations to identify optimal formulations, comprehensive auditing of generated directives, and maintenance of prompt libraries with detailed change logs.

**Reproducibility Assurance**
Non-deterministic model behavior poses risks to scientific reproducibility. Our comprehensive mitigation strategy includes: pinning specific model versions with documented API endpoints, fixing random seeds for all stochastic processes, archiving complete configuration snapshots for each experimental run, implementing comprehensive logging of all system interactions, and creating automated reproduction scripts for key findings.

**Mitigation Playbooks (triggered by Early Indicators):**
- Evaluator drift (consistency < 0.85): Freeze current prompts; rerun with fixed seeds; compare across providers; re‑baseline with human spot‑checks; document deltas.
- JSON contract failures (>0.5%): Enable strict schema validation and auto‑retry; reduce temperature; add minimal repair step; log offending examples for prompt hardening.
- Latency regressions (p95 > 2s): Reduce max_tokens; cache static sections; parallelize I/O; switch to alternate endpoint; monitor token usage.
- Privacy incident (RBAC/audit gap): Disable non‑essential access; rotate keys; enable detailed audit logging; perform post‑mortem and add compensating controls.
- Crisis content handling gaps: Enforce safety regex; route to neutral fallback; surface escalation text; flag session for review.

### 8.3 Contingency Planning

**Alternative Model Providers**
Should primary LLM services become unavailable, we maintain ready access to alternative providers (OpenAI GPT-4, Anthropic Claude) with equivalent API interfaces. All prompts and evaluation procedures are designed to be provider-agnostic, enabling rapid switching without experimental disruption.

**Evaluation Fallback Procedures**
If automated LLM evaluation proves unreliable, we have established protocols for transitioning to human evaluation with trained raters. Evaluation rubrics are designed to be interpretable by both automated and human assessors, and we maintain relationships with qualified evaluators for rapid deployment.

**Scope Adjustment Protocols (Decision Gates and Rollbacks)**
Should technical challenges or resource constraints threaten project completion, we activate decision gates: (a) If evaluator consistency < 0.75 after two prompt fixes, switch to human evaluation sample (n=30) and freeze further prompt changes; (b) If JSON compliance < 98.5% for two weeks, prioritize contract hardening over feature work; (c) If latency p95 > 3s in week 5, drop non‑critical nodes. Minimal viable study: basic detection, simple regulation, comparative baseline; document deferrals.

**Timeline Buffer Management**
The project timeline includes built-in buffers for unexpected challenges, with non-critical features identified for potential deferral to the thesis phase. Regular milestone reviews will enable early identification of delays and proactive scope adjustments.

### 8.4 Monitoring and Review Procedures

**Weekly Risk Assessment**
Each week includes a structured risk review examining: progress against planned milestones, emergence of new risks or changes in existing risk profiles, effectiveness of current mitigation strategies, and need for additional resources or support.

**Stakeholder Communication**
Regular updates to supervisors include explicit risk status reporting with early escalation of issues requiring additional resources or guidance. Monthly progress reports include updated risk assessments and mitigation effectiveness analysis.

**Documentation and Learning**
All risk events and mitigation outcomes are documented to support future project planning and contribute to best practices for similar research endeavors. This documentation will inform the thesis phase risk management approach and support knowledge transfer to other researchers.

**Operational KPIs (tracked weekly):**
| KPI | Target | Action Threshold |
|-----|--------|------------------|
| JSON contract compliance | ≥ 99.5% | < 98.5% triggers contract hardening playbook |
| EMA stabilization by turn 8 | ≥ 80% sessions | < 70% triggers detection prompt review |
| Evaluator inter‑run consistency | ≥ 0.85 | < 0.80 triggers drift investigation |
| p95 latency | < 2.0s | > 2.5s triggers performance playbook |
| Incident rate (per 1k turns) | < 1.0 | ≥ 2.0 triggers post‑mortem and fixes |
| Privacy/security incidents | 0 | Any incident triggers escalation and audit |

---

## 9. Work and Research Plan

### 9.1 Timeline Overview

The research plan spans nine weeks with carefully sequenced activities designed to build foundational understanding, implement core technical components, conduct experimental validation, and produce comprehensive documentation. The timeline balances ambitious research goals with realistic resource constraints while maintaining flexibility for unexpected challenges or opportunities.

**Table 6. Detailed Work Plan with Milestones and Deliverables**

| Phase | Week(s) | Primary Activities | Key Deliverables | Success Criteria | Owner | Dependencies |
|-------|---------|-------------------|------------------|------------------|--------|--------------|
| **Foundation** | 1-2 | Literature review completion; RQ finalization; technology stack validation | Comprehensive background section; finalized research questions; validated tool configuration | Background ≥1.5 pages with ≥3 citations; testable RQs mapped to methodology; working N8N environment | Author | Access to academic databases; N8N installation |
| **Implementation** | 3-4 | N8N workflow development; prompt engineering; logging system setup | Complete workflow JSON; validated prompt library; automated logging infrastructure | Functional detect→regulate→generate pipeline; consistent JSON outputs; comprehensive logs | Author | LLM API access; N8N expertise |
| **Validation** | 5-6 | Simulation execution; automated evaluation; data analysis | Evaluation matrices; comparative charts; statistical analysis | Completed simulations for both personality types; evaluator consistency >0.8; significant results | Author | Simulation scripts; evaluation prompts |
| **Analysis** | 7 | Results interpretation; visualization creation; limitation analysis | Draft Results section; publication-quality figures; comprehensive Discussion | Clear performance differences; professional visualizations; honest limitation assessment | Author | Analysis tools; statistical software |
| **Documentation** | 8 | PMT manuscript completion; appendix assembly; internal review | Complete PMT v1.0; comprehensive appendices; peer review feedback | All sections meet acceptance criteria; reproducible artifacts; constructive feedback | Author | Supervisor availability; peer reviewers |
| **Finalization** | 9 | Revision integration; final quality assurance; thesis planning | Final PMT v2.0; thesis proposal outline; presentation materials | Polished manuscript; clear thesis roadmap; conference-ready presentation | Author + Supervisors | Revision feedback; thesis planning meeting |

### 9.2 Detailed Activity Breakdown

**Weeks 1-2: Foundation Phase**
*Literature Review and Theoretical Grounding*
- Systematic review of personality-aware dialogue systems literature
- Deep dive into Zurich Model applications in conversational AI
- Analysis of current evaluation methodologies for emotional support chatbots
- Integration of findings into comprehensive background section

*Research Question Refinement*
- Workshop sessions with supervisors to refine research questions
- Mapping of RQs to specific experimental procedures and success metrics  
- Validation of research scope against available resources and timeline
- Documentation of research question evolution and rationale

*Technology Stack Validation*
- N8N installation and configuration in development environment
- LLM API access verification and quota establishment
- Docker environment setup for reproducible development
- Initial workflow prototyping and feasibility testing

**Weeks 3-4: Implementation Phase**
*N8N Workflow Development*
- Implementation of all workflow nodes per technical specifications
- Integration of LLM API calls with proper error handling
- Development of personality detection prompts with JSON schema validation
- Creation of regulation directive mapping with conflict resolution logic

*Prompt Engineering and Validation*
- Systematic development of detection prompts with trait-specific indicators
- Generation constraint templates ensuring dialog grounding
- Evaluation prompts with clear rubric definitions and examples
- A/B testing of prompt variations for optimal performance

*Infrastructure and Logging*
- Comprehensive logging system for all node interactions
- Automated data export procedures for analysis pipeline
- Configuration management and version control setup
- Testing framework development for continuous validation

**Weeks 5-6: Validation Phase**
*Simulation Execution*
- Systematic execution of personality Type A and Type B simulations
- Data collection across multiple bot instances for statistical reliability
- Real-time monitoring of system performance and error rates
- Quality assurance checks for data completeness and consistency

*Automated Evaluation*
- Deployment of scripted LLM evaluator across all collected conversations
- Multiple evaluation runs with consistency analysis
- Bias control procedures including randomization and blind assessment
- Statistical analysis of evaluation reliability and validity

*Preliminary Analysis*
- Descriptive statistics for all evaluation criteria
- Comparative analysis between regulated and baseline conditions
- Effect size calculations and statistical significance testing
- Initial interpretation of findings and identification of patterns

**Weeks 7: Analysis Phase**
*Results Interpretation*
- Comprehensive statistical analysis of experimental outcomes
- Qualitative analysis of conversation examples and regulatory effectiveness
- Comparison with Devdas (2025) baseline results for validation
- Identification of unexpected findings and their implications

*Visualization and Presentation*
- Creation of publication-quality charts and graphs
- Development of workflow diagrams and system architecture visuals
- Statistical result presentation with appropriate confidence intervals
- Integration of visual elements with narrative analysis

*Limitation and Risk Analysis*
- Honest assessment of experimental limitations and scope constraints
- Analysis of risk mitigation effectiveness and lessons learned
- Identification of threats to validity and their potential impact
- Recommendations for future research and methodology improvements

**Weeks 8: Documentation Phase**
*Manuscript Completion*
- Integration of all research components into coherent PMT document
- Comprehensive appendix assembly with all reproducible artifacts
- Reference list completion with consistent APA formatting
- Internal quality assurance review for completeness and clarity

*Peer Review Process*
- Submission to qualified peer reviewers for independent assessment
- Integration of constructive feedback and revision recommendations
- Validation of technical accuracy and methodological soundness
- Preparation of response to reviewer comments and suggested improvements

**Week 9: Finalization Phase**
*Final Revisions*
- Integration of supervisor and peer reviewer feedback
- Final proofreading and formatting consistency checks
- Validation of all references and technical specifications
- Preparation of final manuscript for submission

*Thesis Planning*
- Development of thesis proposal outline building on PMT findings
- Identification of thesis-phase extensions and human validation studies
- Resource planning for thesis implementation including ethical approvals
- Timeline development for thesis completion and defense

*Presentation Preparation*
- Creation of conference-style presentation summarizing key findings
- Development of demonstration materials for system capabilities
- Preparation for academic presentation and defense of methodology
- Documentation of lessons learned and recommendations for future researchers

### 9.3 Resource Requirements and Support

**Technical Resources**
- N8N Pro license for advanced workflow features (if needed)
- LLM API credits sufficient for experimental requirements (~$200-500)
- Cloud computing resources for backup and collaboration
- Statistical analysis software (R/Python with appropriate libraries)

**Human Resources**
- Supervisor meetings: 2 hours weekly for guidance and feedback
- Peer review: 2-3 qualified reviewers for manuscript assessment
- Domain expert consultation: Psychology expertise for personality profile validation
- Technical support: N8N and API troubleshooting as needed

**Institutional Support**
- Access to academic databases for literature review
- Computational resources for data analysis and visualization
- Presentation opportunities for feedback and validation
- Ethical review board consultation for future human studies

### 9.4 Quality Assurance and Monitoring

**Progress Tracking**
- Weekly milestone reviews with quantitative progress metrics
- Regular supervisor meetings with structured progress reports
- Peer accountability partnerships for motivation and feedback
- Documentation of challenges and problem-solving approaches

**Quality Control**
- Systematic code review for all technical implementations
- Independent validation of statistical analyses and interpretations
- Peer review of written materials before supervisor submission
- Reproducibility testing of all experimental procedures

**Risk Monitoring**
- Weekly risk assessment updates with mitigation effectiveness analysis
- Early warning systems for timeline or resource constraints
- Contingency plan activation procedures for critical path disruptions
- Stakeholder communication protocols for major issues

This comprehensive work plan provides a structured approach to completing the preliminary study while maintaining the flexibility necessary for high-quality research. The detailed timeline and milestone structure enable effective progress monitoring while the built-in quality assurance procedures ensure research integrity and reproducibility.

---

## 10. References

Abbasian, M., Azimi, I., Rahmani, A. M., & Jain, R. C. (2023). Conversational health agents: A personalized LLM-powered agent framework. *arXiv preprint arXiv:2310.02374*.

Alisamir, S., & Ringeval, F. (2021). On the evolution of speech representations for affective computing: A brief history and critical overview. *IEEE Signal Processing Magazine*, 38, 12-21.

Anttila, T., Selander, K., & Oinas, T. (2020). Disconnected lives: Trends in time spent alone in Finland. *Social Indicators Research*, 150, 711-730.

Bischof, N. (1993). The Zurich model of social motivation. *Journal of Psychological Systems*, 201, 5-43.

Broadbent, E., Loveys, K., Ilan, G., Chen, G., Chilukuri, M., Boardman, S. G., Doraiswamy, P., & Skuler, D. (2024). ElliQ, an AI-driven social robot to alleviate loneliness: Progress and lessons learned. *JAR Life*, 13, 22-28.

Chen, K., Kang, X., Lai, X., & Ni, Z. (2023). Enhancing emotional support capabilities of large language models through cascaded neural networks. *2023 4th International Conference on Computer, Big Data and Artificial Intelligence (ICCBD+AI)*, 318-326.

Couture, L. (2012). Loneliness linked to serious health problems and death among elderly. *Activities, Adaptation & Aging*, 36, 266-268.

De Freitas, J., Huang, S.-C., Pradelski, B. S. R., & Suskind, D. (2024). AI companions reduce loneliness (Working Paper No. 24-078). The Wharton School. https://doi.org/10.48550/arXiv.2407.19096

Devdas, S. (2025). *Enhancing emotional support through conversational AI via Big Five personality detection and behavior regulation based on the Zurich Model* [Master's thesis]. Lucerne University of Applied Sciences and Arts.

Dong, T., Liu, F., Wang, X., Jiang, Y., Zhang, X., & Sun, X. (2024). EmoAda: A multimodal emotion interaction and psychological adaptation system. *Conference on Multimedia Modeling*.

Dongre, P. (2024). Physiology-driven empathic large language models (EmLLMs) for mental health support. *Extended Abstracts of the CHI Conference on Human Factors in Computing Systems*.

Hämmig, O. (2019). Health risks associated with social isolation in general and in young, middle, and old age. *PLoS ONE*, 14, e0219663.

Luo, Y., Hawkley, L. C., Waite, L. J., & Cacioppo, J. T. (2012). Loneliness, health, and mortality in old age: A national longitudinal study. *Social Science & Medicine*, 74(6), 907-914.

MacLeod, S., Musich, S., Parikh, R. B., Hawkins, K., Keown, K., & Yeh, C. (2018). Examining approaches to address loneliness and social isolation among older adults. *Journal of Aging and Health*, 30(7), 1071-1095.

Marottoli, R. A., & Glass, W. J. (2007). Social isolation among seniors: An emerging issue. *Geriatrics*, 62(11), 16-18.

McCrae, R. R., & John, O. P. (1992). An introduction to the five-factor model and its applications. *Journal of Personality*, 60(2), 175-215.

Musich, S., Wang, S. S., Hawkins, K., & Yeh, C. (2015). The impact of loneliness on quality of life and patient satisfaction among older, sicker adults. *Gerontology and Geriatric Medicine*, 1, 1-9.

Quirin, M., Malekzad, F., Paudel, D., Knoll, A. C., & Mirolli, M. (2023). Dynamics of personality: The Zurich model of motivation revived, extended, and applied to personality. *Journal of Personality*, 91(4), 928-946. https://doi.org/10.1111/jopy.12805

Shah, S. G., Nogueras, D., van Woerden, H. C., & Kiparoglou, V. (2019). The effectiveness of digital technology interventions to reduce loneliness in adult people: A protocol for a systematic review and meta-analysis. *medRxiv*, 19000414.

Shah, S. G., Nogueras, D., van Woerden, H. C., & Kiparoglou, V. (2020). Evaluation of the effectiveness of digital technology interventions to reduce loneliness in older adults: Systematic review and meta-analysis. *Journal of Medical Internet Research*, 23, e24712.

Sorino, P., Biancofiore, G., Lofú, D., Colafiglio, T., Lombardi, A., Narducci, F., & Di Noia, T. (2024). ARIEL: Brain-computer interfaces meet large language models for emotional support conversation. *Adjunct Proceedings of the 32nd ACM Conference on User Modeling, Adaptation and Personalization*.

Ta, V. P., Griffith, C., Boatfield, C., Wang, X., Civitello, M., Bader, H., DeCero, E., & Loggarakis, A. (2020). User experiences of social support from companion chatbots in everyday contexts: Thematic analysis. *Journal of Medical Internet Research*, 22, e16235.

Wu, W., Heierli, J., Meisterhans, M., Moser, A., Farber, A., Dolata, M., Gavagnin, E., Spindler, A. D., & Schwabe, G. (2023). PROMISE: A framework for developing complex conversational interactions (Technical Report). University of Zurich.

Xie, T., & Pentina, I. (2022). Attachment theory as a framework to understand relationships with social chatbots: A case study of Replika. *Hawaii International Conference on System Sciences*.

Zhang, H., Chen, Y., Wang, M., & Feng, S. (2024). FEEL: A framework for evaluating emotional support capability with large language models. *arXiv preprint arXiv:2403.15699*.

Zheng, Z., Liao, L., Deng, Y., & Nie, L. (2023). Building emotional support chatbots in the era of LLMs. *arXiv preprint arXiv:2308.11584*.

---

## 11. Appendix

### Appendix A. Prompt Interfaces and Templates

**A.1 Detection Prompt (JSON-Structured Response)**
```
You are a Zurich Model personality and stress assessor. Analyze the last user message and up to 10 prior turns.

Return ONLY valid JSON in this exact format:
{
  "ocean": {"O": -1.0 to 1.0, "C": -1.0 to 1.0, "E": -1.0 to 1.0, "A": -1.0 to 1.0, "N": -1.0 to 1.0},
  "confidence": {"O": 0.0-1.0, "C": 0.0-1.0, "E": 0.0-1.0, "A": 0.0-1.0, "N": 0.0-1.0},
  "stress": {
    "level": 0|1|2|3|4,
    "drivers": ["workload"|"uncertainty"|"social"|"health"|"finance"|"other"...],
    "signals": {"cognitive":[], "affective":[], "physiological":[], "behavioral":[]},
    "confidence": 0.0-1.0
  },
  "coaching_mode": "vent_validate"|"plan_structure"|"cope_rehearse",
  "evidence_quotes": [string, ...]
}

Rules:
- Base all inferences strictly on quoted spans from the user's text; no external facts.
- Stress level: 0 none, 1 mild, 2 moderate, 3 high, 4 crisis.
- Choose coaching_mode that best fits immediate need: vent_validate (validation), plan_structure (planning), cope_rehearse (immediate coping).

Conversation: {conversation_context}
User message: {user_message}
```

**A.2 Generation Prompt with Behavioral Directives**
```
You are a supportive conversational assistant. Follow these behavioral directives strictly:
{behavioral_directives}

CRITICAL CONSTRAINTS:
1. Ground all responses strictly in the user's text - no external information or assumptions
2. Respond in 70-150 words
3. Ask at most 1-2 questions
4. Maintain supportive, empathetic tone appropriate to the directives
5. Coaching mode: {coaching_mode}
6. If stress_level ≥ 3 and crisis indicators appear, provide a neutral supportive message and suggest reaching out to a trusted person or local support line; do not provide clinical advice.

User context: "{conversation_context}"
User message: "{user_message}"
```

**A.3 Evaluation Prompt for Automated Assessment**
```
Evaluate this chatbot response using the specified criteria. Provide only the requested assessment format.

CONVERSATION CONTEXT:
User: "{user_message}"
Assistant: "{assistant_response}"
Detected Personality: {ocean_disc}
Applied Directives: {directives}

EVALUATION CRITERIA:
1. Detection Accuracy: Does ocean_disc appropriately reflect personality cues in user message?
2. Regulation Effectiveness: Are behavioral directives correctly applied in the response?
3. Emotional Tone Appropriate: Does response tone match user emotional state and personality?
4. Relevance & Coherence: Is response contextually relevant and logically coherent?
5. Personality Needs Addressed: Does response address trait-specific emotional needs?

For each criterion, respond with: "Yes" (clear success), "Partial" (mixed/unclear), or "No" (clear failure).

Format: Detection_Accuracy: [Yes/Partial/No], Regulation_Effectiveness: [Yes/Partial/No], Emotional_Tone: [Yes/Partial/No], Relevance_Coherence: [Yes/Partial/No], Personality_Needs: [Yes/Partial/No]
```

### Appendix B. Evaluation Rubric and Scoring Guidelines

**Table B.1 Comprehensive Evaluation Criteria Definitions**

| Criterion | Definition | "Yes" (2 points) | "Partial" (1 point) | "No" (0 points) |
|-----------|------------|------------------|---------------------|------------------|
| **Detection Accuracy** | Alignment between `ocean_disc` inference and observable personality cues | Clear trait indicators match detected values; logical inference | Some alignment but missing or questionable trait assessments | Poor alignment or systematic misdetection |
| **Regulation Effectiveness** | Appropriate application of trait-specific behavioral strategies | All relevant directives correctly implemented in response style | Partial directive application or minor inconsistencies | Directives ignored or incorrectly applied |
| **Emotional Tone Appropriate** | Match between response emotional tone and user state/personality | Tone perfectly suited to user's emotional state and personality traits | Generally appropriate tone with minor misalignments | Tone inappropriate or potentially harmful |
| **Relevance & Coherence** | Contextual appropriateness and logical consistency of response | Highly relevant, coherent, and well-structured response | Generally relevant with minor coherence issues | Off-topic, incoherent, or poorly structured |
| **Personality Needs Addressed** | Satisfaction of trait-specific emotional and interactional requirements | Response clearly addresses personality-driven needs | Partially addresses needs or generic support | Fails to address personality-specific needs |

**B.2 Scoring Aggregation Procedures**
- **Row-level scoring:** Sum of all criterion scores for single interaction
- **Bot-level scoring:** Average of all row scores for individual bot instance  
- **Condition-level scoring:** Average across all bots in regulated or baseline condition
- **Statistical analysis:** T-tests, effect sizes, confidence intervals for group comparisons

### Appendix C. Technical Configurations and System Specifications

**C.1 Model Specifications and Parameters**
```yaml
# LLM Configuration
detection_model:
  name: "gemini-1.5-pro"
  endpoint: "https://ai.juguang.chat/v1/chat/completions"
  parameters:
    temperature: 0.1
    max_tokens: 200
    timeout_seconds: 20
    top_p: 1.0

generation_model:
  name: "gemini-1.5-pro"  
  endpoint: "https://ai.juguang.chat/v1/chat/completions"
  parameters:
    temperature: 0.7
    max_tokens: 220
    timeout_seconds: 20
    top_p: 1.0

# Alternative Configuration
fallback_model:
  name: "gpt-4-turbo"
  endpoint: "https://api.openai.com/v1/chat/completions"
  parameters:
    temperature: 0.1  # detection
    # temperature: 0.7  # generation
    max_tokens: 200
    timeout_seconds: 20
```

**C.2 N8N Workflow Node Configuration**
```json
{
  "workflow_version": "1.0.0",
  "nodes": [
    {
      "name": "Manual Trigger",
      "type": "n8n-nodes-base.manualTrigger",
      "position": [250, 300]
    },
    {
      "name": "Edit Fields",
      "type": "n8n-nodes-base.set",
      "parameters": {
        "values": {
          "session_id": "test_session_001",
          "message": "I feel overwhelmed by all these changes lately..."
        }
      },
      "position": [450, 300]
    },
    {
      "name": "Detect OCEAN",
      "type": "n8n-nodes-base.code",
      "parameters": {
        "language": "javascript",
        "code": "// Personality detection implementation\n// See technical specifications for complete code"
      },
      "position": [850, 300]
    }
  ]
}
```

**C.3 Environment Configuration**
```bash
# .env file template
N8N_BASIC_AUTH_ACTIVE=true
N8N_BASIC_AUTH_USER=research_user
N8N_BASIC_AUTH_PASSWORD=secure_password_here

GEMINI_API_KEY=your_gemini_api_key_here
OPENAI_API_KEY=your_openai_api_key_here
JUGUANG_API_KEY=your_juguang_api_key_here

# Logging configuration
LOG_LEVEL=info
LOG_FILE_PATH=./logs/personality_chatbot.log
EXPORT_FORMAT=jsonl

# Database configuration (for extended version)
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
POSTGRES_DB=personality_research
POSTGRES_USER=research_user
POSTGRES_PASSWORD=secure_db_password
```

### Appendix D. Statistical Analysis and Visualization Code

**D.1 Data Analysis Pipeline**
```python
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats

# Load experimental data
def load_evaluation_data(filepath):
    """Load and preprocess evaluation results"""
    df = pd.read_csv(filepath)
    
    # Convert scoring to numeric
    score_mapping = {'Yes': 2, 'Partial': 1, 'No': 0}
    score_columns = ['Detection_Accuracy', 'Regulation_Effectiveness', 
                    'Emotional_Tone', 'Relevance_Coherence', 'Personality_Needs']
    
    for col in score_columns:
        if col in df.columns:
            df[col] = df[col].map(score_mapping)
    
    return df

# Statistical analysis
def analyze_results(df):
    """Perform statistical analysis of regulated vs baseline performance"""
    regulated = df[df['Condition'] == 'Regulated']
    baseline = df[df['Condition'] == 'Baseline']
    
    # Shared criteria comparison
    shared_criteria = ['Emotional_Tone', 'Relevance_Coherence', 'Personality_Needs']
    
    results = {}
    for criterion in shared_criteria:
        reg_scores = regulated[criterion].dropna()
        base_scores = baseline[criterion].dropna()
        
        # T-test
        t_stat, p_value = stats.ttest_ind(reg_scores, base_scores)
        
        # Effect size (Cohen's d)
        pooled_std = np.sqrt(((len(reg_scores) - 1) * reg_scores.var() + 
                             (len(base_scores) - 1) * base_scores.var()) / 
                            (len(reg_scores) + len(base_scores) - 2))
        cohens_d = (reg_scores.mean() - base_scores.mean()) / pooled_std
        
        results[criterion] = {
            'regulated_mean': reg_scores.mean(),
            'baseline_mean': base_scores.mean(),
            'difference': reg_scores.mean() - base_scores.mean(),
            't_statistic': t_stat,
            'p_value': p_value,
            'cohens_d': cohens_d,
            'significant': p_value < 0.05
        }
    
    return results

# Visualization functions
def create_comparison_plot(df, save_path=None):
    """Create publication-quality comparison visualization"""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))
    
    # Overall performance comparison
    performance_data = df.groupby(['Condition', 'Personality_Type'])['Total_Score'].mean().unstack()
    performance_data.plot(kind='bar', ax=ax1, color=['skyblue', 'lightcoral'])
    ax1.set_title('Overall Performance by Condition and Personality Type')
    ax1.set_ylabel('Mean Total Score')
    ax1.legend(title='Personality Type')
    
    # Criterion-wise comparison
    criteria = ['Emotional_Tone', 'Relevance_Coherence', 'Personality_Needs']
    regulated_means = [df[df['Condition'] == 'Regulated'][col].mean() for col in criteria]
    baseline_means = [df[df['Condition'] == 'Baseline'][col].mean() for col in criteria]
    
    x = np.arange(len(criteria))
    width = 0.35
    
    ax2.bar(x - width/2, regulated_means, width, label='Regulated', color='skyblue')
    ax2.bar(x + width/2, baseline_means, width, label='Baseline', color='lightcoral')
    
    ax2.set_title('Criterion-wise Performance Comparison')
    ax2.set_ylabel('Mean Score')
    ax2.set_xticks(x)
    ax2.set_xticklabels(criteria, rotation=45)
    ax2.legend()
    
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
    
    plt.show()

# Usage example
if __name__ == "__main__":
    # Load and analyze data
    df = load_evaluation_data('evaluation_results.csv')
    results = analyze_results(df)
    
    # Print results
    for criterion, stats in results.items():
        print(f"\n{criterion}:")
        print(f"  Regulated: {stats['regulated_mean']:.2f}")
        print(f"  Baseline: {stats['baseline_mean']:.2f}")
        print(f"  Difference: {stats['difference']:.2f}")
        print(f"  Cohen's d: {stats['cohens_d']:.2f}")
        print(f"  Significant: {stats['significant']}")
    
    # Create visualizations
    create_comparison_plot(df, 'performance_comparison.png')
```

**D.2 Reproducibility Checklist**
- [ ] All model versions documented with API endpoints
- [ ] Random seeds fixed and recorded for all stochastic processes  
- [ ] Configuration files archived with cryptographic hashes
- [ ] Complete interaction logs saved in JSONL format
- [ ] Analysis code version controlled with dependency specifications
- [ ] Environment setup documented with container configurations
- [ ] Evaluation procedures validated with consistency checks
- [ ] Statistical analysis methods justified and documented

This comprehensive appendix provides all necessary technical details for reproducing the experimental procedures, analyzing results, and extending the research framework. The combination of detailed prompts, configuration specifications, and analysis code ensures that other researchers can replicate and build upon this work effectively.

---

**Document Statistics:**
- **Total Length:** ~30 pages (estimated)
- **Word Count:** ~15,000 words  
- **Sections:** 11 main sections plus comprehensive appendices
- **Tables:** 6 detailed tables with technical specifications
- **Figures:** 1 workflow diagram with additional visualization code
- **References:** 25+ academic sources in APA format
- **Technical Depth:** Implementation-ready specifications with complete reproducibility documentation

This formal preliminary study document provides a comprehensive foundation for implementing and evaluating personality-aware conversational AI systems, with particular emphasis on transparency, reproducibility, and practical deployment in human-centered applications.
