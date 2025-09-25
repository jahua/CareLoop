# Adaptive LLM-Based Chatbot with Personality-Aware Dialogue for Human-Centered Applications

Author: <Your Name>  
Affiliation: Lucerne University of Applied Sciences and Arts (HSLU)  
Supervisors: Prof. Dr. Guang Lu; Prof. Dr. Alexandre de Spindler  
Date: <YYYY-MM-DD>  
Version: 0.2 (Manuscript)

## Abstract
Loneliness and emotional strain among older adults and vulnerable populations remain persistent public-health concerns. Conversational AI offers scalable support but frequently fails to adapt to individual differences in personality, leading to generic and sometimes misaligned guidance. We present an N8N-orchestrated framework for personality-aware dialogue that integrates per-turn Big Five (OCEAN) trait detection with behavior regulation grounded in the Zurich Model of Social Motivation. Our method operationalizes a transparent detect→regulate→generate pipeline as an execution-ready N8N workflow (MVP) with deterministic contracts, strict grounding, and neutral fallbacks. Building on Samuel Devdas’ thesis, we adopt discrete OCEAN inference and trait-to-directive mappings to modulate tone, pacing, warmth, and novelty, while ensuring dialog grounding via quote-and-bound prompts. We outline a reproducible evaluation harness using a scripted LLM-based rubric to compare regulated versus baseline agents on tone appropriateness, relevance/coherence, and personality-need satisfaction, with detection and regulation checks for the regulated condition. This work contributes a technically reproducible, safety-aware pipeline and an evaluation design suitable for research and healthcare-aligned deployments.

Keywords: personality-aware chatbot; OCEAN; Zurich Model; regulation; N8N; evaluation; dialog grounding

## 1. Introduction
Loneliness and social isolation are prevalent among older adults and are associated with adverse outcomes across emotional wellbeing, cognition, and mortality risk. Digital companions show promise for scalable support, yet many systems employ generic prompting or static profiles that overlook users’ evolving psychological dispositions. Without sensitivity to personality traits such as Openness or Neuroticism, chatbots can produce ill-matched tones (e.g., overly energetic for introverted users) or introduce novelty that elevates stress for anxious users.

Advances in large language models (LLMs) enable nuanced conversation, but the lack of transparent, reproducible mechanisms for adapting behavior to personality remains a gap. Personality-aware dialogue requires two capabilities: (1) inferring a user’s personality cues from language, and (2) translating those cues into concrete, psychologically coherent behavior changes. Samuel Devdas’ thesis demonstrated that combining OCEAN detection with Zurich Model–aligned regulation substantially improves conversation quality over non-adaptive baselines in controlled simulations.

This paper proposes a buildable, testable framework to implement personality-aware dialogue using N8N as the orchestration layer. Our core contributions are:
- A modular detect→regulate→generate pipeline implemented as an N8N workflow with precise node contracts, timeouts, and fallbacks (MVP).
- A transparent regulation design that maps discrete OCEAN traits to Zurich-aligned directives controlling tone, pacing, warmth, structure, and novelty.
- A reproducible evaluation harness with a scripted LLM-based rubric comparing regulated and baseline responses on shared criteria, with additional detection/regulation checks for the regulated agents.
- A deployment-ready path emphasizing dialog grounding, auditability, and safety measures suitable for human-centered and healthcare contexts.

## 2. Background & Literature Review
### 2.1 Theoretical foundations
- Big Five (OCEAN). The Five-Factor Model characterizes personality across Openness, Conscientiousness, Extraversion, Agreeableness, and Neuroticism, providing a practical basis for conversational adaptation. In our pipeline, traits are inferred per turn as discrete values {−1, 0, +1} to drive clear regulatory actions.
- Zurich Model of Social Motivation. The Zurich Model frames behavior around motivational systems—security, arousal, and affiliation. We operationalize these as: Neuroticism → security (comfort vs. reassurance), Openness/Extraversion → arousal (novelty and energy modulation), Agreeableness → affiliation (warmth vs. neutrality). This mapping supports psychologically coherent style changes.

### 2.2 Related work
- Companion chatbots (e.g., Replika, ElliQ) and emotional support systems show user engagement but often rely on generic prompts. Personality-aware prompting frameworks (e.g., PROMISE) and evaluation approaches (e.g., FEEL) contribute methods but rarely combine real-time detection with explicit psychological regulation.
- Multi-modal systems (e.g., EmoAda) extend sensing but introduce complexity and data concerns; our scope focuses on dialog-only grounding and personality-based regulation for transparency and reproducibility.

### 2.3 Research gaps
- Lack of integrated, reproducible pipelines that (i) infer OCEAN traits per turn, (ii) translate traits into Zurich-aligned directives, and (iii) evaluate end-to-end conversational outcomes against baselines with clear rubrics and logs.
- Limited transparency in how personality cues lead to concrete behavioral changes; we address this via explicit trait-to-directive mappings and node-level logging.

## 3. Research Questions
Primary RQ. How can an adaptive LLM-based chatbot use real-time personality detection and Zurich-guided behavior regulation to improve conversational quality and user-aligned support versus non-adaptive baselines?

Sub-RQs.
1) Detection: What prompt strategies yield reliable per-turn OCEAN inference in short dialogues?  
2) Regulation: How should directives be composed to harmonize potentially conflicting trait signals?  
3) Evaluation: Which automated procedures (LLM-based, scripted, blinded) provide reliable and reproducible scoring?  
4) Orchestration: What N8N designs best balance traceability and performance for detect→regulate→generate?  
5) Generalization: How do results differ between extreme simulated profiles and more naturalistic dialogs?

Link to evaluation. Sub-RQs map to rubric dimensions: detection accuracy and regulation effectiveness evaluate the pipeline core; tone, relevance/coherence, and needs addressed quantify outcome quality.

## 4. Methodology
We implement a dialog-only, prompt-only system with deterministic contracts, neutral fallbacks, and strict dialog grounding.

### 4.1 System architecture (N8N, MVP)
Pipeline: ingest → detect(discrete) → parse → regulate → generate → format-output.  
- Ingest. Normalize user input; construct per-turn `conversation_context` (no persistence in MVP).  
- Detect OCEAN (Discrete). LLM call returns `{"ocean_disc": {O|C|E|A|N: -1|0|1}}` with temperature 0.1 and 20s timeout.  
- Parse Detection JSON. Extract JSON; if only continuous scores appear, threshold with τ=0.2 to derive discrete values.  
- Build Regulation Directives (Zurich). Map non-neutral traits to ≤5 directives (comfort vs reassurance; novelty/energy modulation; warmth; structure vs flexibility).  
- Generate Response. Quote-and-bound generation grounded strictly in user text; 70–150 words; ≤2 questions; temp 0.7; 20s timeout.  
- Format Output. Emit `{session_id, reply, turn_text, ocean_disc}`.

N8N nodes: Manual Trigger, Edit Fields, Function/Code, HTTP, IF (optional in extended workflow), and Format Function. Source workflow: `w9-Technical-Specifications/MVP/workflows/Discrete_workflow.json`.

### 4.2 Detection module
- Input: single-turn text.  
- Output: `ocean_disc` with values in {−1, 0, +1}.  
- Prompting: strict JSON-only response; neutral fallback `{0,...,0}` on error.  
- Optional self-consistency: k-sampling with per-trait majority voting (off in MVP to meet latency targets).

### 4.3 Regulation module
- Trait-to-directive mapping aligned to Zurich domains:  
  - N: −1 → “offer extra comfort”; +1 → “reassure stability/confidence”.  
  - O: +1 → “invite small exploration/novelty”; −1 → “reduce novelty; focus on familiar”.  
  - E: +1 → “use energetic tone”; −1 → “adopt calm, reflective tone”.  
  - A: +1 → “warm, collaborative language”; −1 → “neutral, matter-of-fact stance”.  
  - C: +1 → “2–3 structured steps”; −1 → “flexible, low-pressure guidance”.  
- Conflict handling: deterministic ordering and templating to avoid contradictory instructions.

### 4.4 Dialogue simulation protocol
- Profiles: Type A (+1,+1,+1,+1,+1) and Type B (−1,−1,−1,−1,−1), plus optional mid-trait variants.  
- Conversations: 6 turns; 5–10 bots per condition.  
- Exports: JSONL/CSV including user text, reply, `ocean_disc`, and directives.

### 4.5 Evaluation framework
- Criteria: Detection Accuracy, Regulation Effectiveness, Tone, Relevance & Coherence, Personality Needs Addressed.  
- Scoring: trinary (2 = Yes, 1 = Not sure, 0 = No); per-row totals aggregate to per-bot scores.  
- Evaluator: scripted LLM evaluator with fixed prompt, blinded rows, randomized order; multiple runs for consistency checks.  
- Baselines: non-adaptive assistants scored on the shared criteria (Tone, Relevance & Coherence, Needs).  
- Visualization: bar/line charts comparing regulated vs baseline.

### 4.6 Reproducibility & safety
- Fixed model versions, temperature, seeds, and timeouts; archive prompts/configs.  
- Dialog-only grounding; neutral fallbacks; error handling recorded in logs.  
- Privacy/ethics: anonymize any human inputs; consent and storage policies for future pilot studies.

## 5. (Planned) Results and Analysis
We expect regulated assistants to outperform baseline assistants on shared criteria, replicating prior gains in tone appropriateness, coherence, and personality-need alignment. Latency targets follow the MVP constraints (20s per LLM call; P95 2.5–5.0s in extended workflows).

## 6. Discussion and Future Work
Our N8N-based design emphasizes interpretability and operational simplicity. Future work will add EMA smoothing, verification/refinement gates, Postgres persistence, and human-in-the-loop validation.

## 7. Conclusion
An N8N-executed detect→regulate→generate pipeline offers a practical and transparent approach to personality-aware conversational support. The framework, prompts, and evaluation harness provide a reproducible path toward psychologically coherent, human-centered chatbot interactions.

## References
- Samuel Devdas (2025); Quirin et al. (2023); Zhang et al. (2024); Zheng et al. (2023); W8/W9 technical documents; HSLU guidelines.

## Appendix
- Workflow JSON; prompts; evaluator rubric; config/versions; scripts.
