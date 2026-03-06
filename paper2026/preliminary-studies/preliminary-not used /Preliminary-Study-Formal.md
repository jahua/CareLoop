# Adaptive LLM-Based Chatbot with Personality-Aware Dialogue for Human-Centered Applications: A Formal Preliminary Study

Author: <Your Name>  
Program: MSc Applied Information and Data Science (HSLU)  
Supervisors: Prof. Dr. Guang Lu; Prof. Dr. Alexandre de Spindler  
Date: <YYYY-MM-DD>  
Version: 0.3 (Formal PMT Manuscript)

---

## Abstract
Loneliness and emotional strain among older adults and other vulnerable groups present persistent public-health challenges. While conversational AI promises scalable support, many assistants remain generic and fail to adapt to users’ individual differences. This preliminary study proposes a reproducible, N8N-orchestrated framework for personality-aware dialogue that integrates per-turn Big Five (OCEAN) personality detection with behavior regulation grounded in the Zurich Model of Social Motivation. Building on the empirical findings of Devdas (2025), who showed substantial performance gains for personality-adaptive chatbots over non-adaptive baselines, we implement a transparent detect→regulate→generate pipeline with deterministic contracts, quote-and-bound dialog grounding, and neutral fallbacks. We specify an evaluation harness based on a scripted LLM evaluator and a structured rubric to assess detection accuracy, regulation effectiveness, tone appropriateness, relevance and coherence, and the satisfaction of personality-specific emotional needs. The outcome is a technically reproducible pathway to implement, test, and extend personality-aware conversational systems oriented to human-centered applications, with an emphasis on transparency, traceability, and safety.

Keywords: personality-aware chatbot; OCEAN; Zurich Model; behavior regulation; N8N; evaluation; dialog grounding; human-centered AI

---

## 1. Background
Loneliness and social isolation affect a significant proportion of older adults and are linked to depression, cognitive decline, and elevated mortality risk (Couture, 2012; Hämmig, 2019; Musich et al., 2015). Digital companions (e.g., Replika, ElliQ) increasingly serve as scalable interventions for lightweight emotional support and companionship (Ta et al., 2020; Broadbent et al., 2024). However, their effectiveness varies and often depends on whether conversations feel emotionally attuned and personally relevant (Xie & Pentina, 2022; De Freitas et al., 2024). Many systems rely on generic prompts or static user profiles, limiting the capacity to adapt to evolving user signals in real time.

Recent LLM advances enable more nuanced and context-sensitive dialogue (Zheng et al., 2023), yet practical implementations still lack consistent, transparent mechanisms to adapt conversational behavior to inferred personality traits. Devdas (2025) demonstrated that real-time personality detection using the Big Five (OCEAN) and behavior regulation aligned to the Zurich Model can significantly improve conversation quality—showing ~34% relative improvement on shared criteria versus non-adaptive baselines in controlled simulations. This motivates a structured, reproducible pipeline for detection→regulation→generation and a clear evaluation framework that isolates the benefits of personality-aware regulation.

Existing chatbots rarely integrate dynamic trait detection with psychologically grounded regulation and reproducible evaluation. Systems either: (i) adapt minimally (static profiles), (ii) lack transparent trait-to-behavior mappings, or (iii) provide insufficient audit trails to support scientific assessment and healthcare alignment. A research-grade, N8N-orchestrated implementation with deterministic node contracts, logs, and neutral fallbacks addresses these gaps.


## 2. Topic Definition
- Personality-adaptive emotional support chatbot. A conversational agent that detects the user’s personality signals and accordingly modulates tone, structure, pacing, warmth, and novelty to better satisfy user-specific emotional needs.
- Big Five (OCEAN). A personality framework with Openness, Conscientiousness, Extraversion, Agreeableness, and Neuroticism (McCrae & John, 1992). We use discrete per-turn inference in {−1, 0, +1} to drive unambiguous regulatory actions.
- Zurich Model alignment. Personality-to-behavior mapping grounded in the Zurich Model of Social Motivation (Quirin et al., 2023), operationalized via three motivational domains: security (Neuroticism), arousal (Openness/Extraversion), and affiliation (Agreeableness). Conscientiousness modulates structural guidance.
- Scope. Human-centered applications emphasizing safety and empathy: elder care, wellbeing, and lightweight mental health support. The PMT is dialog-only, prompt-only; no multimodal data or external retrieval in MVP; privacy- and safety-aware.
- Evaluation. Structured rubric assessing: detection accuracy, regulation effectiveness, emotional tone appropriateness, relevance and coherence, and personality-needs addressed (Devdas, 2025; Zhang et al., 2024).


## 3. Research Questions
Primary RQ. How can an adaptive LLM-based chatbot use real-time personality detection and Zurich-guided behavior regulation to improve conversational quality and user-aligned support compared to non-adaptive baselines?

Sub-RQs.
1) Detection. What prompt strategies and contracts yield reliable per-turn OCEAN inference in short dialogues?  
2) Regulation. How should Zurich-aligned directives be composed to harmonize potentially conflicting trait signals without incoherence?  
3) Evaluation. Which scripted, blinded LLM-based procedures provide reliable and reproducible scoring of regulated and baseline responses?  
4) Orchestration. What N8N workflow design best balances traceability, performance, and simplicity for detect→regulate→generate?  
5) Generalization. How do results differ between extreme simulated profiles and more naturalistic dialogues, and what limits emerge for transfer to live users?

Mapping to methodology. RQ1–2 are validated by per-turn logs, directive audits, and outcome metrics; RQ3 by multi-run consistency and bias controls; RQ4 by workflow instrumentation; RQ5 by scenario variation.


## 4. Methodology
We implement a reproducible, dialog-grounded pipeline with deterministic contracts, neutral fallbacks, and node-level logging, orchestrated in N8N. The MVP focuses on the discrete per-turn variant; extended workflow adds smoothing and verification.

### 4.1 System Architecture
Two variants:
- Target (future): ingest → detect → smooth → regulate → generate → verify → checkpoint
- MVP (implemented): ingest → detect(discrete) → parse → regulate → generate → format-output

Figure 1. N8N MVP Workflow (Manual Trigger → Edit Fields → Ingest → Detect (HTTP/Code) → Parse JSON → Build Regulation (Function) → Generate (HTTP/Code) → Format Output). Source: `preliminary-studies/w9-Technical-Specifications/MVP/workflows/Discrete_workflow.json`.

### 4.2 Detection Module (Per-turn OCEAN)
- Input: `message` text. Output: `ocean_disc ∈ {−1,0,+1}^5` for O,C,E,A,N.
- Contract: Strict JSON-only response. Temperature 0.1, max_tokens 200, 20s timeout. Endpoint per MVP (e.g., `gemini-1.5-pro` via `https://ai.juguang.chat/v1/chat/completions`).
- Parsing: Try direct JSON parse; otherwise extract the first JSON object. If only continuous scores exist, threshold with τ=0.2 to recover discrete signs. On invalid/missing fields, set neutral zeros.
- Optional variance reduction: self-consistency (k=3) and per-trait majority vote (off in MVP to meet latency targets).

### 4.3 Regulation Module (Zurich-aligned)
- Mapping. Non-neutral traits activate directives:
  - N: −1 → “offer extra comfort; acknowledge anxieties”; +1 → “reassure stability and confidence”.
  - O: +1 → “invite small exploration/novelty”; −1 → “reduce novelty; focus on familiar”.
  - E: +1 → “use energetic, engaging tone”; −1 → “adopt calm, reflective tone”.
  - A: +1 → “warm, collaborative language”; −1 → “neutral, matter-of-fact stance”.
  - C: +1 → “provide 2–3 structured steps”; −1 → “keep guidance flexible and low-pressure”.
- Conflict handling: deterministic ordering; templates that merge signals coherently.

### 4.4 Generation (Quote-and-Bound)
- Constraints: Ground responses strictly in the user’s text (no external claims); 70–150 words; ≤2 questions; temperature 0.7; 20s timeout.
- Fallback: On error, send a short, supportive message plus metadata fields for traceability.

### 4.5 N8N Workflow Nodes (MVP)
Table 1. Node responsibilities and I/O.

| Node | Type | Purpose | Inputs | Outputs |
|---|---|---|---|---|
| Manual Trigger | N8N Manual | Start execution | — | — |
| Edit Fields | Set | Provide test JSON | `{session_id, message}` | Payload |
| Ingest | Function | Normalize, build context | Payload | `session_id, clean_msg, conversation_context` |
| Detect OCEAN | Code/HTTP | Call LLM; return JSON | Context | `ocean_disc` |
| Parse JSON | Code | Extract JSON; threshold | API response | `ocean_disc, turn_text` |
| Build Regulation | Function | Map traits→directives | `ocean_disc` | `directives` (≤5) |
| Generate | Code/HTTP | Produce reply | `directives, turn_text` | API response + fields |
| Format Output | Function | Emit compact payload | Upstream fields | `{session_id, reply, turn_text, ocean_disc}` |

### 4.6 Dialogue Simulation Protocol
- Profiles: Type A (+1,+1,+1,+1,+1) and Type B (−1,−1,−1,−1,−1); optional mid-traits.
- Dialogues: 6 turns per conversation; 5–10 bots per condition.
- Exports: JSONL/CSV with user text, reply, `ocean_disc`, directives, timings.

### 4.7 Evaluation Framework
- Criteria: (Regulated) Detection Accuracy; Regulation Effectiveness; Tone; Relevance & Coherence; Personality Needs Addressed. (Baseline) Tone; Relevance & Coherence; Needs.
- Scoring: Trinary per criterion per row—Yes=2, Not sure=1, No=0; totals per bot and per condition.
- Evaluator: Scripted LLM evaluator; blinded rows; randomized order; multiple runs; fixed prompt.
- Visualization: Bar/line charts for totals and criterion-wise scores.

Table 2. Evaluation matrix (excerpt schema).

| Row | Persona | User Message | Assistant Reply | ocean_disc | Directives | DetAcc | RegEff | Tone | Rel&Co | Needs | Total |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | A-Reg-1 | … | … | {…} | [ … ] | 2 | 2 | 2 | 2 | 2 | 10 |

### 4.8 Automation & Reproducibility
- Fixed parameters: model versions, temperature, seeds, timeouts; archived prompts/configs.
- Logging: per-turn JSONL with inputs, `ocean_disc`, directives, reply, timings; export to CSV for analysis.
- Safety: neutral fallbacks; dialog-only grounding; error handling recorded.


## 5. Underlying Data Sources
- Simulated dialogues and prompts  
  - Personality Type A/B prompts and bot scripts.  
  - Location: `preliminary-studies/w9-Technical-Specifications/MVP/` (see `workflows`, scripts).  
  - License/usage: internal research use; ensure compliance with LLM provider ToS.
- Detection/regulation prompt libraries  
  - Versioned prompts in Appendix; linked to workflow nodes.  
  - License/usage: authored for this study; research use.
- Evaluation materials  
  - Scripted evaluator prompt (Appendix); matrix templates; aggregation scripts.  
  - Derived from Devdas (2025) rubric with adaptations; research use.
- Optional corpora (qualitative checks only)  
  - Public emotional-support datasets (to be added if used); respect dataset licenses; no PII.
- Logs/artefacts  
  - JSONL/CSV exports of runs stored under `preliminary-studies/preliminary-handover/output/` (to be created).  
  - Ensure anonymization if any human inputs are later included (future thesis stage).


## 6. Technology, Software, and Applications
We prioritize an N8N-first design for transparency and operational simplicity, with alternatives considered.

Table 3. Tool justification and versions (PMT baseline).

| Layer | Choice (version) | Alternatives | Rationale |
|---|---|---|---|
| Orchestration | N8N (>=1.x) | crewAI/AutoGen; custom FastAPI | Visual, traceable nodes; quick iteration; matches W9 specs |
| LLM (detect/gen) | Gemini 1.5 Pro via `ai.juguang` API; OpenAI GPT-4.x (alt) | Claude; Llama | Availability, stable endpoints, prompt control |
| Storage/State | JSONL logs (PMT); Postgres (extended) | Redis; SQLite | Simple research logging; upgrade path for persistence |
| Evaluation | Scripted LLM evaluator | Human raters (later) | Reproducible, scalable; later human validation |
| Vector DB | None in MVP; FAISS/pgvector (opt) | Milvus | Not needed for dialog-only; optional future retrieval |
| Containers | Docker Compose | K8s | Local reproducibility; simple deployment |

Environment and configs: see `MVP/env.example` and `docker-compose.yml`. Node timeouts and temperatures per Section 4; credentials stored via environment variables or N8N credentials vault.


## 7. Annotated Disposition
1) Background — Context and gap motivating personality-aware, human-centered dialogue.  
2) Topic Definition — Core constructs: per-turn OCEAN detection; Zurich-based regulation; scope boundaries.  
3) Research Questions — Testable questions tied to detection, regulation, evaluation, orchestration, and generalization.  
4) Methodology — N8N workflow, node contracts, prompts, metrics, and analysis procedures.  
5) Underlying Data Sources — Prompts, scripts, evaluator designs, logs.  
6) Technology, Software, Applications — Justified stack and alternatives.  
7) Project Risks — Risk matrix with mitigations and ownership.  
8) Work and Research Plan — Timeline, milestones, deliverables, and responsibilities.  
9) References — APA-style citations and consistency checks.  
10) Appendix — Prompts, matrices, diagrams, configs, and version sheets.


## 8. Project Risks
Table 4. Risk matrix (likelihood, impact, owner, mitigation).

| Risk | Likelihood | Impact | Owner | Mitigation |
|---|---|---|---|---|
| Simulated data realism | Medium | Medium | Author | Add mid-traits; plan human review in thesis |
| Evaluator bias/drift | Medium | High | Author | Fixed prompt; multiple runs; randomization; QA spot checks |
| Prompt sensitivity | Medium | Medium | Author | Version prompts; A/B tests; directive audits |
| Non-determinism/model updates | Medium | High | Author | Pin versions; fix seeds; archive configs |
| Latency overruns | Low | Medium | Author | 20s caps; reduce tokens; single-pass MVP |
| Privacy/ethics | Low | High | Author + Supervisor | Anonymize; consent; secure storage; ethics note |
| Tool/vendor lock-in | Medium | Medium | Author | Abstract endpoints; alt providers; minimal deps |
| Scope creep | Medium | Medium | Author | Freeze MVP; defer smoothing/verify to extension |
| Reproducibility gaps | Low | High | Author | JSONL logs; config/version sheets; scripts |
| Operational errors | Medium | Medium | Author | Scripts (`test_*.sh`); dry-runs; error logging |


## 9. Work and Research Plan
Timeline (indicative; adjust to semester calendar).

Table 5. Gantt-style plan with milestones and deliverables.

| Week(s) | Activity | Outputs/Deliverables | Owner |
|---|---|---|---|
| 1–2 | Literature review; finalize RQs; stack choice | Background; RQs; tool table | Author |
| 3–4 | Implement N8N MVP nodes; seed prompts; logging | Workflow JSON; prompts; logs | Author |
| 5–6 | Simulation runs; evaluator scripting; aggregation | Evaluation matrix; charts | Author |
| 7 | Analysis; write Results/Discussion; risks | Draft figures; risk matrix | Author |
| 8 | Draft PMT; compile Appendix; internal review | PMT manuscript v1; appendix | Author |
| 9 | Revisions; finalize PMT; thesis planning | PMT v2; thesis scope | Author + Supervisors |


## 10. References (APA-style)
Abbasian, M., Azimi, I., Rahmani, A. M., & Jain, R. C. (2023). Conversational health agents: A personalized LLM-powered agent framework. arXiv preprint arXiv:2310.02374.

Broadbent, E., Loveys, K., Ilan, G., Chen, G., Chilukuri, M., Boardman, S. G., Doraiswamy, P., & Skuler, D. (2024). ElliQ, an AI-driven social robot to alleviate loneliness: Progress and lessons learned. JAR Life, 13, 22–28.

Couture, L. (2012). Loneliness linked to serious health problems and death among elderly. Activities, Adaptation & Aging, 36, 266–268.

De Freitas, J., Huang, S.-C., Pradelski, B. S. R., & Suskind, D. (2024). AI companions reduce loneliness (Working Paper No. 24-078). The Wharton School. https://doi.org/10.48550/arXiv.2407.19096

Hämmig, O. (2019). Health risks associated with social isolation in general and in young, middle, and old age. PLoS ONE, 14.

McCrae, R. R., & John, O. P. (1992). An introduction to the five-factor model and its applications. Journal of Personality, 60(2), 175–215.

Quirin, M., Malekzad, F., Paudel, D., Knoll, A. C., & Mirolli, M. (2023). Dynamics of personality: The Zurich model of motivation revived, extended, and applied to personality. Journal of Personality, 91(4), 928–946.

Ta, V. P., Griffith, C., Boatfield, C., Wang, X., Civitello, M., Bader, H., DeCero, E., & Loggarakis, A. (2020). User experiences of social support from companion chatbots in everyday contexts: Thematic analysis. Journal of Medical Internet Research, 22.

Xie, T., & Pentina, I. (2022). Attachment theory as a framework to understand relationships with social chatbots: A case study of Replika. Proceedings of the Hawaii International Conference on System Sciences.

Zhang, H., Chen, Y., Wang, M., & Feng, S. (2024). FEEL: A framework for evaluating emotional support capability with large language models. arXiv preprint arXiv:2403.15699.

Zheng, Z., Liao, L., Deng, Y., & Nie, L. (2023). Building emotional support chatbots in the era of LLMs. arXiv preprint arXiv:2308.11584.

Devdas, S. (2025). Enhancing emotional support through conversational AI via Big Five personality detection and behavior regulation based on the Zurich Model (Master’s thesis). HSLU.


## 11. Appendix
### Appendix A. Prompt Interfaces (MVP)
- Detection (JSON-only): `{"ocean_disc":{"O":-1|0|1,"C":-1|0|1,"E":-1|0|1,"A":-1|0|1,"N":-1|0|1}}`  
- Generation (constraints): Follow directives strictly; ground in user text only; 70–150 words; ≤2 questions; temp=0.7; timeout=20s.

### Appendix B. Evaluation Rubric (excerpt)
Table B1. Criterion definitions and decision rules.

| Criterion | Definition | Decision rule (Yes/1/0) |
|---|---|---|
| Detection Accuracy | `ocean_disc` matches persona cues | Clear match / partial / mismatch |
| Regulation Effectiveness | Directives applied correctly | Correct / partial / incorrect |
| Tone Appropriate | Emotional tone matches persona and state | Matched / uncertain / misaligned |
| Relevance & Coherence | Contextually relevant and coherent | Relevant / partial / off-topic |
| Personality Needs | Addresses persona-specific needs | Addresses / partial / not addressed |

### Appendix C. Configurations and Versions (PMT)
- Models: `gemini-1.5-pro` (detect/gen) via `ai.juguang` API; alternative `gpt-4.x` for replication.  
- Parameters: detect temp=0.1, max_tokens=200; generate temp=0.7, max_tokens=220; 20s timeout per call.  
- Seeds: fixed for reproducibility (recorded per run).  
- N8N: version ≥1.x; workflow JSON located at `.../MVP/workflows/Discrete_workflow.json`.  
- Containers: Docker Compose; env variables per `MVP/env.example`.

### Appendix D. Figures and Workflow
- Figure 1. N8N MVP Workflow (see Section 4.1).  
- Extended workflow (future): add Smooth (EMA), Verify, Refine, and DB persistence nodes as per `w9-Technical-Specifications-v1.2.pdf`.

