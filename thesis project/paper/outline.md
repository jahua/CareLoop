# Manuscript Outline (APA 7, 30-page target)

## Working Title

**Personality-Aware Digital Coaching Through Adaptive Dialogue: Design, Implementation, and Pilot Evaluation with Swiss Caregivers**

---

## Page Budget

| Section | Pages | Notes |
|---------|-------|-------|
| Title + Abstract | 1 | 250-word abstract |
| Introduction | 5 | Integrates gap, aim, RQs |
| Related Work | 4 | Three focused themes |
| System Design | 7 | Core technical contribution |
| Evaluation | 4 | Design, measures, procedure |
| Results | 4 | One subsection per RQ cluster |
| Discussion | 3 | Interpretation, limits, future |
| Conclusion | 0.5 | |
| References | 2.5 | ~40–50 entries |
| **Total** | **~30** | Appendices online-only if needed |

---

## Abstract (250 words)

**Problem.** Digital coaching systems personalize through mood tracking or conversation memory, but neither captures the stable personality traits that predict how users respond to different coaching styles — a third personalization layer that human coaches apply implicitly.

**System.** We present CareLoop, a personalized coaching architecture that adds this missing layer: continuous Big Five (OCEAN) inference from dialogue, stabilized via EMA smoothing, translated into behavioral directives that modulate emotional tone, relevance, and responsiveness. Four coaching modes (emotional support, practical education, policy navigation, mixed) with hybrid vector + FTS retrieval and mandatory grounding verification. Three pipeline invariants: personality always runs, retrieval is conditional, grounding is mandatory for policy content. Hybrid LLM + heuristic intent router with confidence gating and safety overrides.

**Evaluation.** Automated pillar test matrices (130+ cases across four modes), latency and load benchmarks, and audit-trail validation provide pilot evidence of system reliability, routing accuracy, and grounding safety.

**Contribution.** A modular coaching architecture demonstrating that personality-aware modulation can coexist with factual grounding in a single auditable pipeline. Swiss informal caregivers as pilot use case; designed for domain transfer.

**Keywords:** personalized digital coaching, personality-aware dialogue, large language models, retrieval-augmented generation, Swiss caregivers, adaptive human-computer interaction

---

## 1. Introduction (~5 pages)

A single flowing section with no numbered subsections. Internally organized as six paragraphs/blocks:

**Opening (¶1).** What makes coaching effective is adaptation to the individual — not just content. Human coaches implicitly learn personality-driven preferences. As coaching moves digital, the design question is: what mechanisms achieve comparable adaptation?

**Three personalization layers (¶2).** Current digital coaching personalizes through three layers: (1) transient mood tracking (Woebot, Wysa — reactive, per-turn), (2) conversation memory (ChatGPT Memory, mem0 — content recall across sessions), (3) stable personality modeling (unaddressed by any deployed system). Each layer serves a different function; layers 1–2 are necessary but insufficient for personalized coaching because they don't capture *who the user is*. The AutoSurvey literature confirms this gap: persona-aware generation conditions on static profiles but does not detect or stabilize traits from live dialogue (AutoSurvey §1.3, §2.6).

**Why personality matters for coaching (¶3).** Big Five traits predict coaching outcomes (de Haan et al., 2013; Jones et al., 2016). The contribution is not classification but *modulation*: translating stabilized traits into directives that adapt coaching style across three quality dimensions. Prior work on adaptive dialogue management uses RL or meta-learning for policy adaptation (AutoSurvey §4.1–4.2), but these require large training data. CareLoop's directive-based modulation is a lightweight, interpretable alternative.

**Coexistence with factual accuracy (¶4).** Coaching domains combine emotional support with domain knowledge. Current apps sidestep this by avoiding domain retrieval (Woebot/Wysa) or skipping personality adaptation (RAG systems). CareLoop must solve both: style modulation + factual grounding with architectural enforcement.

**Swiss caregivers (¶5).** ~700,000 caregivers with dual burden: emotional stress + fragmented policy navigation. Exercises all three personalization layers simultaneously + demands grounded guidance.

**Gap table + contribution (¶6).** Three-layer personalization deficit table (transient state, memory, personality, style, domain knowledge, content/style separation). Memory and mood are necessary but insufficient. No system combines personality-trait-based modulation with domain retrieval and mandatory grounding. Cite the two AutoSurvey outputs as structured literature evidence: neither survey identifies a system that integrates all three components — this is the strongest available confirmation that the gap is real.

**Research questions (¶6, table).**

| RQ | Focus |
|----|-------|
| RQ1 | Can continuous OCEAN inference with EMA produce valid, temporally stable trait estimates? |
| RQ2 | Does personality modulation improve emotional tone, relevance, and emotional-needs responsiveness versus non-adaptive baselines? |
| RQ3 | Can RAG-enhanced policy navigation achieve full citation coverage with no critical grounding errors? |
| RQ4 | Does the hybrid LLM router correctly classify intent across four modes with acceptable latency? |
| RQ5 | Does the system achieve acceptable reliability under load with full audit coverage? |

---

## 2. Related Work (~4 pages)

Three focused subsections. Each ends with a sentence connecting to the present study. Use the AutoSurvey outputs (`AutoSurvey/output/`) as structured reference mines — extract 3–5 strong citations per subsection, always verify before citing.

### 2.1 Digital Coaching Systems and Personalization Mechanisms

**Deployed systems and their personalization layers.**
- Three architectural models: rule-based CBT (Woebot), hybrid NLP (Wysa), LLM-based memory (ChatGPT, mem0)
- What each personalizes: mood → content recall → (nothing for stable traits)
- Coaching effectiveness varies by personality (de Haan et al., 2013; Jones et al., 2016; Smither et al., 2019)

**Personality-aware dialogue: state of the art.**
- Personality-aware dialogue foundations: Yarkoni (2010), Park et al. (2015), Mairesse & Walker (2010), Devdas (2025)
- Persona-aware response generation via LLMs: conditioning on persona profiles improves consistency but does not address temporal stability (AutoSurvey §1.3, §3.1; Li et al., 2016 [64]; Zheng et al., 2019 [80])
- Dynamic personality modeling: attention mechanisms and latent variable models explored for context-dependent trait expression, but no prior work uses EMA smoothing with confidence gating (AutoSurvey §2.6)
- Adaptive dialogue management: RL, meta-learning, and multi-task learning adapt policies to personality, but these require large training data or complex reward design; none operate as a lightweight directive-based modulation layer (AutoSurvey §4.1–4.4)
- Zurich Model as theoretical bridge from OCEAN to coaching behavior — not mentioned in either AutoSurvey output, confirming novelty of this grounding framework

**Gap.** No deployed system combines: (1) continuous trait detection from dialogue, (2) temporal stabilization across turns, (3) formal directive-based modulation, in an operational coaching pipeline. Prior work focuses on either personality classification or persona-conditioned generation, but not on the intermediate step of *stabilized trait-to-directive translation* that enables consistent coaching adaptation.

### 2.2 Retrieval-Augmented Generation and Grounding

**RAG in health-adjacent and coaching contexts.**
- RAG for factual accuracy: vector retrieval + generation with source attribution
- Hybrid retrieval strategies (vector + lexical/FTS) for improved recall
- Grounding verification and hallucination prevention as design requirements
- Knowledge graph integration for persona consistency explored (AutoSurvey §2.5, §3.3), but KGs address persona *knowledge* not *factual policy grounding*
- No prior system architecturally separates content accuracy from style adaptation — personality modulation and factual grounding are typically conflated or one is omitted

**Gap.** No system integrates personality-aware style modulation with mandatory grounding verification as explicit pipeline invariants. CareLoop's three invariants (universal personality, conditional retrieval, mandatory grounding) are a novel architectural contribution.

### 2.3 Digital Support for Informal Caregivers

**Caregiver burden and digital interventions.**
- Caregiver burden, burnout, and unmet support needs (~700,000 Swiss informal caregivers)
- Digital interventions show promise: Mooney et al. (2024) report 38% burden reduction with automated coaching at 8 weeks
- Current tools: generic stress-management apps, FAQ portals, Spitex information sites — none personality-adaptive
- Swiss policy complexity (cantonal fragmentation, IV/AHV/EL/Hilflosenentschädigung)
- The AutoSurvey explicitly lacks caregiver-specific coverage (no caregiver datasets, no caregiver-facing systems reviewed) — this gap in the literature itself is evidence for the novelty of the use case

**Gap.** No caregiver support tool combines emotionally adaptive coaching, practical self-management education, and grounded Swiss policy navigation in a single system. The absence of caregiver-specific work in two comprehensive surveys (Gemma and Qwen outputs) confirms this is an underexplored application domain for personality-aware dialogue.

---

## 3. System Design (~7 pages)

The core technical contribution. Five subsections.

### 3.1 Architecture and Pipeline Invariants

High-level architecture: Next.js API route → N8N 9-stage workflow → PostgreSQL + pgvector → Google Gemma-3 via NVIDIA API.

**Pipeline overview** (one concise list, not 17 numbered steps):
- API pre-processing: hybrid LLM intent routing, session isolation, conditional vector retrieval
- N8N orchestration: ingest → load state → detect (OCEAN + EMA) → regulate (directives) → retrieve (merge evidence) → generate → ground-verify → quality-verify → format + persist
- API post-processing: mode override, optional LLM regeneration, citation overlay, grounding invariant check, dual audit write

**Three pipeline invariants** (one table — the single canonical statement):

| Invariant | Rule | Enforcement |
|-----------|------|-------------|
| Universal personality | OCEAN detection + regulation run for every turn in every mode | N8N executes Detection → EMA → Regulation before mode branching; API flags violations |
| Conditional retrieval | Evidence retrieval runs only when factual content is needed | API `shouldRetrieveEvidence()` gates on mode + keyword signals + opt-out phrases |
| Mandatory grounding | Policy/mixed responses must have citations | N8N verifier checks claim-evidence overlap; API checks citation count; 0 citations → warning |

**Four coaching modes** (one table):

| Mode | Personality | Retrieval | Grounding |
|------|------------|-----------|-----------|
| Emotional support | Full modulation | Skipped | Not required |
| Practical education | Full modulation | Conditional | If citations present |
| Policy navigation | Style only (facts invariant) | Always | Mandatory |
| Mixed | Full + style | Always | Mandatory |

Include **Figure 1**: architecture diagram (API ↔ N8N ↔ DB ↔ LLM). Keep it to one figure.

### 3.2 Personality Detection and Stabilization

Covers detection, EMA, and modulation in one subsection (these are tightly coupled). This is the central technical contribution of the paper. Position it explicitly against the literature.

**Detection.** LLM-based OCEAN inference (Gemma-3, temperature 0) producing per-turn traits in [−1, +1] with per-trait confidence in [0, 1]. Heuristic keyword fallback when LLM unavailable. Prior 6 turns loaded from DB.

*Literature positioning:* Prior personality detection in dialogue relies on fine-tuned classifiers (Basto, 2021 [61]; Wen et al., 2024 [118]) or persona embeddings (Li et al., 2016 [64]; Majumder et al., 2020 [63]). CareLoop uses zero-shot LLM inference with structured JSON output, avoiding fine-tuning while producing continuous trait values rather than discrete labels.

**EMA stabilization.** In-session α = 0.3; cross-session α = 0.2. Confidence threshold 0.4 (below → keep prior value). Stability criterion: variance < 0.05 after 6+ turns.

*Literature positioning:* The AutoSurvey (§2.6) identifies dynamic/contextual personality representation as an open problem, noting that "traditional approaches often rely on static personality profiles." Prior work explores attention mechanisms and latent variable models for dynamic representation but does not address temporal stabilization of noisy per-turn detections. EMA with confidence gating is a novel, lightweight mechanism that fills this gap without requiring additional model training.

**Trait-to-directive modulation.** Five trait pairs mapped to behavioral directives (threshold: |trait| > 0.15, confidence ≥ 0.35). Directives govern tone, structure, warmth, and pacing. Default when no trait exceeds threshold: warm, supportive, exploratory. Modulation is universal — it runs in all four modes. In policy/mixed modes, directives shape presentation without altering factual content.

*Literature positioning:* Adaptive dialogue management typically uses RL reward shaping (AutoSurvey §4.1) or meta-learning (§4.2) to adapt policies. These are powerful but data-hungry and opaque. CareLoop's directive-based modulation is interpretable (each directive traces to a specific trait threshold), auditable (directives are logged per turn), and does not require training — making it suitable for pilot deployment in sensitive coaching domains.

Include **Figure 2**: EMA convergence example (Neuroticism across 6+ turns). One compact trait-to-directive table (move full 10-row version to appendix).

### 3.3 Hybrid Intent Router

Five-layer classification:
1. Explicit requested mode (confidence 1.0)
2. LLM router (structured JSON, temperature 0, cached 5 min)
3. Confidence gate (< 0.5 → fall to heuristic)
4. Keyword heuristic fallback (26 policy / 17 education / 15 emotional terms + history inheritance)
5. Hard safety override (force retrieval for policy keywords regardless of source)

N8N V2 workflow consumes the API's routing decision, eliminating duplicate classification. Routing metadata (source, reason, confidence, LLM latency) attached to every response and audit record.

### 3.4 Retrieval and Grounding Verification

**Retrieval.** Hybrid vector + FTS. Vector: NVIDIA embeddings (1024-dim, `nv-embedqa-e5-v5`), pgvector cosine similarity, top-5, threshold ≥ 0.30. FTS fallback when vector returns < 2 results. Evidence passed as `prefetched_evidence` to workflow, merged with N8N's own FTS results. Personality does not modulate content — only presentation style.

**Grounding verification (two-stage + API invariant).**
- Stage 1 (N8N): extract claims via regex, check evidence overlap (ratio < 0.5 → fail with safe fallback; 0.5–0.8 → degraded; ≥ 0.8 → pass).
- Stage 2 (N8N): quality scoring (session validity, question count, word count, banned phrases; score < 0.5 → block).
- Stage 3 (API): post-response citation count check for policy/mixed (0 citations → `warn_no_citations`).

### 3.5 Infrastructure, Audit, and Reproducibility

One compact subsection. Move detailed tech-stack table and ops dashboard details to appendix.

**Stack summary** (prose, not table): Next.js 14 frontend with Zustand state management; N8N workflow orchestration (Docker); PostgreSQL 16 with pgvector (11 tables); Google Gemma-3 via NVIDIA API; Zod contract schemas; JWT auth; Docker Compose deployment.

**Audit.** Dual write: JSONL + PostgreSQL `audit_log`. Per-turn record includes request ID, session, mode, pipeline status, routing metadata, personality (OCEAN only, no PII), citation count, verifier status, input hash (SHA-256), latency. PII redaction before logging.

**Reproducibility.** Fixed model versions; versioned workflow files (V-numbering); deterministic JSON contracts; containerized deployment; benchmark fixtures as versioned JSON.

---

## 4. Evaluation (~4 pages)

### 4.1 Validation Streams and Study Design

This is a pilot system design and evaluation study. Four validation streams:

| Stream | Sample | What it validates |
|--------|--------|-------------------|
| Automated pillar matrices | 130+ cases across 4 modes | Mode routing, citations, grounding, latency |
| Benchmark + load tests | 10 expansion + 4 latency + 100 concurrent | Performance gates, reliability |
| Expert pilot | n = 5–8 domain experts | Usability, appropriateness |
| Simulated evaluation | N ≥ 250 synthetic conversations | Coaching quality across baselines |

Real caregiver validation (n = 20–30) is specified as a future protocol.

### 4.2 Baselines

| Condition | Description |
|-----------|-------------|
| Personality-aware (full) | Detection + EMA + modulation + RAG + hybrid routing |
| Generic non-adaptive | No personality detection or adaptation |
| Memory-only | Factual recall without trait modeling |
| Policy-only | RAG guidance without personality adaptation |

### 4.3 Measures

One consolidated table (not six sub-subsections). Each measure is grounded in evaluation methodology from the field.

| Construct | Metric | Target | Literature Justification |
|-----------|--------|--------|--------------------------|
| Trait validity | Pearson r with synthetic profiles | ≥ 0.75 | Persona alignment metrics (AutoSurvey §5.5.4); personality assessment standards (Costa & McCrae, 1992) |
| Trait stability | Variance within 6+ turns | < 0.05 | Dynamic personality representation requires temporal consistency (AutoSurvey §2.6) |
| Emotional tone | LLM evaluator / human expert | ≥ 4.0/5.0 | Sentiment-based and Likert-scale tone ratings are standard (AutoSurvey §5.1, §5.3) |
| Relevance & coherence | LLM evaluator / human expert | ≥ 4.0/5.0 | Coherence as evaluation dimension (AutoSurvey §5.5.3) |
| Emotional needs | Improvement over baseline | ≥ 20% | Persona needs satisfaction as established construct (AutoSurvey §5.5.4; Devdas, 2025) |
| Citation coverage | Policy claims with sources | 100% | Factual grounding and hallucination prevention (RAG literature) |
| Grounding errors | Critical hallucinations | 0 | Zero-tolerance for critical errors in health-adjacent domains |
| Routing accuracy | Correct mode (benchmark) | 10/10 | Intent classification accuracy as system reliability metric |
| Load reliability | 100 concurrent, 5xx rate | 0% | Operational stability requirement |
| Latency (p95) | Emotional / practical / policy / mixed | ≤ 4 / 5 / 8 / 9 s | Response time impacts perceived engagement (AutoSurvey §5.4) |

*Note on evaluation approach:* The AutoSurvey (§5.1–5.2) confirms that traditional automatic metrics (BLEU, ROUGE, perplexity) are "largely inadequate for evaluating personality-aware systems" because they measure lexical overlap, not personality fit. This justifies CareLoop's use of LLM-based evaluators with human expert gating (κ ≥ 0.75) rather than n-gram metrics. Human evaluation remains "the gold standard" for personality assessment (AutoSurvey §5.2), supporting our expert pilot design.

### 4.4 Procedure and Analysis

Procedure in one numbered list (12 steps condensed to ~8). Analysis plan as one table mapping RQ → approach.

### 4.5 Ethics

Swiss FADP compliance, pseudonymized storage, PII redaction, crisis escalation (stress ≥ 3), non-clinical boundary, grounding verification as safety mechanism. Keep to one paragraph.

---

## 5. Results (~4 pages)

Four subsections, each covering one or two RQs.

### 5.1 Personality Detection and Stabilization (RQ1)
- Trait alignment scores
- EMA convergence and stability
- Confidence calibration

### 5.2 Coaching Quality (RQ2)
- Emotional tone: adaptive vs. baselines
- Relevance and coherence across modes
- Emotional needs responsiveness

### 5.3 Grounding and Routing (RQ3 + RQ4)
- Citation coverage and grounding verifier outcomes
- Routing accuracy, confidence distribution, fallback frequency
- Mixed-mode detection for boundary cases

### 5.4 System Reliability (RQ5)
- Pillar matrix pass rates (130+ cases)
- Latency benchmarks and load test
- Audit coverage and invariant adherence

---

## 6. Discussion (~3 pages)

### 6.1 Interpretation and Contributions

**Principal finding.** Does trait modulation improve coaching quality across three dimensions (tone, coherence, emotional needs)? Interpret effect sizes relative to baselines.

**Five novelty claims against the literature** (use AutoSurvey as evidence base):

| Contribution | What the literature covers | What CareLoop adds |
|---|---|---|
| EMA stabilization | Dynamic personality via attention/latent models (AutoSurvey §2.6) — no temporal smoothing | Lightweight confidence-gated EMA producing stable coaching adaptation without model training |
| Directive-based modulation | RL/meta-learning for policy adaptation (AutoSurvey §4.1–4.4) — data-hungry, opaque | Interpretable, auditable trait-to-directive mapping with logged thresholds |
| Pipeline invariants | No prior system defines formal invariants for personality + grounding coexistence | Three invariants (universal personality, conditional retrieval, mandatory grounding) as architectural principle |
| Content/style separation | Personality modulation and factual grounding typically conflated or one omitted | Explicit architectural separation: modulation shapes presentation, not content |
| Caregiver application | No caregiver-specific personality-aware system in either AutoSurvey output | First pilot of personality-aware coaching for Swiss informal caregivers |

**Hybrid routing** as a pragmatic, multi-layer approach for multi-mode coaching: explain why five-layer classification with safety overrides is more robust than single-model routing.

### 6.2 Reproducibility and Transferability

**Reproducibility.** Fixed model versions, versioned workflows, deterministic JSON contracts, containerized deployment, dual audit logging, benchmark fixtures as versioned JSON. The AutoSurvey (§1.7) calls for "reproducible evaluation protocols" — CareLoop directly responds.

**Transferability.** The detect → stabilize → modulate → generate → retrieve pipeline is domain-agnostic. Domain specificity lives in: (1) policy corpus, (2) scenario templates, (3) coaching mode definitions. Replacing these adapts the system to other coaching contexts (student wellbeing, employee support, chronic disease self-management). Cross-domain validation is future work.

### 6.3 Limitations and Future Work

**Limitations:**
- Pilot scope: automated + expert evidence; real caregiver validation deferred
- English-only; Swiss-language adaptation needed
- Policy corpus limited to selected domains (IV, EL, Spitex)
- Simplified Zurich Model mapping (first-order; dynamic motivational interactions not modeled)
- LLM router latency (3–5s); external API dependency
- Synthetic evaluation cannot fully capture real user variability
- The AutoSurvey identifies cultural bias as a concern (§1.7, §2.7) — CareLoop has not yet been tested across cultural groups

**Future work:**
- Real caregiver pilot (n = 20–30) with Personality Understanding Scale
- Multilingual Swiss adaptation (German, French, Italian)
- Expanded policy corpus across all 26 cantons
- Cross-domain transfer to non-caregiver coaching contexts
- Longitudinal coaching outcomes over multiple weeks
- Empirical calibration of trait-to-directive mappings
- Multimodal personality signals (the AutoSurvey identifies this as a key future direction, §2.4, §2.7)

---

## 7. Conclusion (~0.5 page)

Three sentences:
1. Digital coaching that ignores personality produces generic, less effective support.
2. CareLoop demonstrates that personality-aware modulation, hybrid intent routing, and mandatory grounding verification can coexist in one auditable pipeline, piloted with Swiss caregivers.
3. The modular architecture is designed for reproducibility and transfer to other human-centered coaching domains.

---

## References (~2.5 pages, ~40–50 entries)

APA 7 format. Priority sources organized by section need:

**Big Five and personality in HCI (for §1, §2.1, §3.2):**
- Costa & McCrae (1992) — Big Five validation
- McCrae & John (1992) — OCEAN framework
- Yarkoni (2010) — personality and language use
- Park et al. (2015) — personality prediction from social media
- Mairesse & Walker (2010) — personality generation in dialogue
- Devdas (2025) — personality detection with motivational regulation
- Quirin et al. (2023) — Zurich Model of Social Motivation

**Personality-aware dialogue (from AutoSurvey, for §2.1):**
- Li et al. (2016) [AutoSurvey 64] — persona-based neural conversation model
- Zheng et al. (2019) [AutoSurvey 80] — personalized dialogue with diversified traits
- Miyama & Okada (2022) [AutoSurvey 59] — personality-adapted multimodal dialogue
- Majumder et al. (2020) [AutoSurvey 63] — persona-grounded dialogue with commonsense
- Hilliard et al. (2024) [AutoSurvey 97] — eliciting personality traits in LLMs

**EMA in psychometric modeling (for §3.2):**
- Literature on exponential moving average in signal processing and psychometric time series

**RAG and grounded generation (for §2.2, §3.4):**
- Lewis et al. (2020) — RAG original paper
- Relevant hybrid retrieval literature (vector + lexical)
- Grounding verification and hallucination prevention studies

**Coaching and evaluation (from AutoSurvey, for §2.1, §4.3):**
- de Haan et al. (2013) — coaching effectiveness and personality
- Jones et al. (2016) — coaching outcomes and Big Five
- Zhang et al. (2024) — FEEL evaluation framework
- Cheng et al. (2022) [AutoSurvey 108] — PAL persona-augmented emotional support

**Caregiver burden and Swiss context (for §2.3):**
- OECD (2023) — informal caregiver statistics
- ZHAW (2022) — Swiss caregiver study
- Ruoss et al. (2023) — SCI caregiver cohort
- Mooney et al. (2024) — digital coaching for caregiver burden reduction

**Ethics and privacy (for §4.5):**
- Swiss FADP (rev. 2023)
- Pasricha (2022) [AutoSurvey 71] — AI ethics in smart healthcare

**Caution:** AutoSurvey references [92], [99], [114], [115], [116], [117] are off-topic noise (tennis, quantum computing, Facebook architecture). Do not cite. Always verify each AutoSurvey reference before including.

---

## Appendices (online supplementary or within page limit)

| Appendix | Content |
|----------|---------|
| A | Full technology stack table (11 tables, all layers) |
| B | Full trait-to-directive mapping (10 rows with thresholds) |
| C | Prompt templates (detection, regulation, generation, LLM router) |
| D | N8N workflow node inventory (V1 → V2) |
| E | Database schema |
| F | Benchmark fixture format and case inventory |
| G | Evaluation rubric and scoring guidelines |
| H | Swiss policy corpus families |

---

## Figures (max 5 in main body)

| Figure | Content | Section |
|--------|---------|---------|
| 1 | System architecture (API ↔ N8N ↔ DB ↔ LLM) | §3.1 |
| 2 | EMA trait convergence example | §3.2 |
| 3 | Hybrid router decision flow | §3.3 |
| 4 | Evaluation design (4 streams) | §4.1 |
| 5 | Results summary (radar or bar chart) | §5 |

## Tables (max 6 in main body)

| Table | Content | Section |
|-------|---------|---------|
| 1 | Research questions | §1 |
| 2 | Pipeline invariants | §3.1 |
| 3 | Four coaching modes | §3.1 |
| 4 | Validation streams | §4.1 |
| 5 | Consolidated measures and targets | §4.3 |
| 6 | Baselines | §4.2 |

---

## Author Notes (not part of manuscript)

### Structural decisions made

| Problem | Solution |
|---------|----------|
| §5 Method had 20 sub-sections | Collapsed to 5 in System Design + 5 in Evaluation |
| Pipeline invariants repeated 5 times | Single canonical table in §3.1; referenced by name elsewhere |
| Tech stack / audit / ops dashboard too detailed | One paragraph in §3.5; full tables in appendix |
| Session isolation was standalone section | Folded into §3.1 architecture overview (one sentence) |
| Trait-to-directive mapping had 10-row table | Compact 5-row summary in §3.2; full table in Appendix B |
| 8 validation streams described individually | One summary table in §4.1 |
| Results had 7 sub-sections | Collapsed to 4 (one per RQ cluster) |
| Discussion had 9 sub-sections | Collapsed to 2 (interpretation + limitations) |
| Lit review had 9 sub-sections | Collapsed to 3 focused themes |

### Framing rules
- The main topic is personalized digital coaching through personality-trait modulation (not a chatbot or a software project)
- Swiss caregivers are the use case, not the topic
- Pipeline invariants are an architectural contribution, stated once, referenced by name
- System Design replaces "Method" for the technical contribution; Evaluation is a separate section for the empirical part
- Claims are bounded: "pilot evidence," "demonstrates," "suggests" — never "proves"
- Keep file paths, variable names, and implementation details out of the main body; use appendices

### Novelty map: what CareLoop adds vs. what the literature covers

Use this table when writing each section to ensure every contribution is explicitly positioned.

| Component | Literature State (AutoSurvey evidence) | CareLoop Contribution | Where to State |
|---|---|---|---|
| **Personality detection** | Fine-tuned classifiers or persona embeddings (§2.2, §3.1); mostly discrete labels | Zero-shot LLM inference producing continuous [-1,+1] traits with confidence | §3.2, §2.1 |
| **Temporal stabilization** | Dynamic personality via attention/latent models (§2.6); no EMA | Confidence-gated EMA (α=0.3/0.2) with variance-based stability criterion | §3.2, §2.1 |
| **Trait-to-directive modulation** | RL/meta-learning for policy adaptation (§4.1–4.4) | Lightweight, interpretable, auditable directive mapping without training | §3.2, §6.1 |
| **Content/style separation** | Not addressed — personality and content typically conflated | Explicit architectural invariants separating modulation from grounding | §3.1, §3.4, §6.1 |
| **Pipeline invariants** | No prior formal invariant design for personality+grounding | Three named invariants enforced at workflow and API levels | §3.1, §6.1 |
| **Hybrid intent routing** | Single-model intent classification typical | Five-layer routing with confidence gating and safety overrides | §3.3, §6.1 |
| **Mandatory grounding verification** | Hallucination discussed as concern (§1.7); no enforced verification pipeline | Two-stage N8N verifier + API invariant check with safe fallback | §3.4, §6.1 |
| **Caregiver application** | No caregiver-specific systems in either survey | First personality-aware coaching system for Swiss caregivers | §1, §2.3, §6.1 |
| **Zurich Model operationalization** | Not mentioned in either survey | Trait-to-motivation mapping as theoretical grounding for directives | §2.1, §3.2 |
| **Evaluation approach** | BLEU/ROUGE inadequate for personality (§5.1); human eval gold standard (§5.2) | LLM evaluator with human expert gating + automated pillar matrices | §4.3 |

### AutoSurvey usage protocol
1. Open the relevant AutoSurvey section alongside the manuscript section being written
2. Extract 2–5 verified references per subsection
3. Use AutoSurvey *gaps* (no EMA, no Zurich Model, no caregivers, no pipeline invariants) as explicit novelty evidence
4. Use AutoSurvey evaluation critique (§5.1 on BLEU/ROUGE inadequacy) to justify the evaluation design
5. Never copy AutoSurvey prose — it is a reference mining tool, not a text source
6. Always verify each reference against the original paper before citing (some AutoSurvey references are noisy or off-topic)
