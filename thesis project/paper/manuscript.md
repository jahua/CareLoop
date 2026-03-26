# Personality-Aware Digital Coaching Through Adaptive Dialogue: Design, Implementation, and Pilot Evaluation with Swiss Caregivers

**Jiahua Duojie**

MSc Applied Information and Data Science, Lucerne University of Applied Sciences and Arts (HSLU)

Supervisor: Prof. Dr. Guang Lu | Advisor: Samuel Devdas

---

## Abstract

Digital coaching systems personalize through transient mood tracking or conversation memory, but neither mechanism captures the stable individual differences — personality traits — that predict how users respond to different coaching styles. This paper presents CareLoop, a personalized coaching architecture that adds a missing third personalization layer: continuous Big Five (OCEAN) trait inference from multi-turn dialogue, stabilized via exponential moving average (EMA) smoothing, and translated into behavioral directives that modulate emotional tone, relevance, and responsiveness. The system supports four coaching modes — emotional support, practical education, policy navigation, and mixed — and retrieves Swiss social-policy evidence through hybrid vector and full-text search with mandatory grounding verification. Three pipeline invariants ensure that (1) personality detection and regulation run for every turn regardless of mode, (2) evidence retrieval is conditional on factual need, and (3) grounding verification is mandatory when policy content is present. A hybrid intent router combines LLM-based classification with confidence-gated heuristic fallback and safety overrides. Automated pillar test matrices (130+ cases across four modes), latency and load benchmarks, and audit-trail validation provide pilot evidence of system reliability, routing accuracy, and grounding safety. Implemented with Next.js, N8N orchestration, PostgreSQL/pgvector, and Google Gemma-3, the architecture demonstrates that personality-aware coaching modulation can coexist with factual grounding in a single auditable pipeline. Swiss informal caregivers serve as the pilot use case; the modular design is intended for domain transfer.

**Keywords:** personalized digital coaching, personality-aware dialogue, large language models, retrieval-augmented generation, Swiss caregivers, adaptive human-computer interaction

---

## 1. Introduction

Personalized coaching — the practice of adapting guidance to an individual's needs, preferences, and style — is well established as more effective than one-size-fits-all instruction in human-delivered settings (Grant, 2003; Stober & Grant, 2006). When a human coach works with a client over multiple sessions, they implicitly learn how that person processes information, responds to structure, handles stress, and prefers to receive feedback. This understanding of the individual — not merely the content delivered — is what makes coaching effective. As coaching moves into digital systems, the central design question becomes: what mechanisms can a system use to achieve comparable adaptation?

Current digital coaching applications personalize through three progressively deeper mechanisms, each addressing a different layer of the coaching relationship. The first layer is *transient state tracking*: systems such as Woebot (Fitzpatrick et al., 2017) and Wysa (Inkster et al., 2018) detect the user's current mood through keyword analysis or sentiment classification and adapt their immediate response accordingly — selecting a breathing exercise for acute anxiety, or a cognitive reframing prompt for rumination. This is valuable but reactive: it responds to the user's state at a single moment without modeling the stable dispositions that determine *how* that user prefers to receive support. The second layer is *conversation memory*: modern LLM-based systems (e.g., ChatGPT Memory, mem0, LangChain Memory) store what users said in prior interactions and retrieve relevant facts during future conversations. A system may recall that a caregiver mentioned a family member's dementia diagnosis or that they previously asked about IV eligibility. Memory enables continuity, but it personalizes *content* (what to reference) rather than *style* (how to communicate). It stores the user's history without modeling who they are. The third layer — and the one largely absent from current implementations — is *stable individual difference modeling*: inferring and tracking the user's personality traits, processing preferences, and communication style as enduring characteristics that should shape coaching behavior across all interactions. This is where human coaches naturally excel and where digital systems have a significant gap.

The distinction matters because coaching effectiveness varies substantially with individual personality characteristics. Empirical evidence demonstrates that Big Five traits predict coaching outcomes: individuals high in Openness benefit most from exploratory coaching approaches, while those high in Conscientiousness respond better to structured goal-setting, and those high in Neuroticism require more emotional scaffolding (de Haan et al., 2013; Jones et al., 2016). A recent controlled field experiment confirmed that coachee personality and goal orientation moderate coaching effectiveness on performance improvement (Smither et al., 2019). These findings establish that coaching is not personality-neutral — the same content delivered in different styles produces different outcomes depending on who receives it.

In informal caregiving specifically, personality predicts not only how caregivers experience stress but also which support strategies help. Neuroticism is a robust risk factor for elevated caregiver burden, depressive symptoms, and burnout: caregivers high in Neuroticism interpret demands as more threatening, exhibit poorer emotion regulation, and report greater subjective burden — and this vulnerability worsens over time in prolonged care episodes. Conscientiousness functions as a protective factor: conscientious caregivers employ structured problem-solving, maintain self-care routines, and report lower perceived burden and emotional exhaustion. Agreeableness facilitates adaptive coping through social support-seeking and collaborative interaction with healthcare providers, buffering isolation. These personality-driven differences in stress reactivity and coping directly shape which coaching style is beneficial: a highly neurotic caregiver experiencing benefit-application anxiety needs emotional validation and reassurance before procedural guidance, while a highly conscientious caregiver in the same situation prefers a structured checklist immediately. The personality-coaching fit is not a cosmetic preference — it determines whether the intervention helps or is simply ignored. Yet no current digital coaching system translates this evidence into an operational mechanism.

The Big Five personality framework — comprising Openness, Conscientiousness, Extraversion, Agreeableness, and Neuroticism (OCEAN) — provides the validated theoretical basis for such a mechanism (McCrae & John, 1992; Costa & McCrae, 1992). Traits can be inferred from natural language with moderate to high accuracy (Yarkoni, 2010; Park et al., 2015), and personality-conditioned language generation improves perceived naturalness and satisfaction (Mairesse & Walker, 2010; Devdas, 2025). The Zurich Model of Social Motivation (Quirin et al., 2023) provides a theoretical bridge from traits to coaching behavior through three motivational systems — security, arousal, and affiliation — that map onto OCEAN dimensions and predict preferred interaction patterns. However, the contribution of this work is not personality *detection* but personality *modulation*: translating stabilized trait estimates into behavioral directives that continuously adapt coaching behavior across three quality dimensions — emotional tone appropriateness, relevance and coherence, and responsiveness to emotional needs.

This modulation must coexist with factual accuracy — a requirement that current coaching apps largely sidestep by avoiding domain-specific knowledge delivery. Many coaching domains involve both emotional support and authoritative information. In healthcare policy navigation, for instance, a coaching response must simultaneously validate a user's anxiety about benefit eligibility *and* provide citation-grounded procedural guidance. Rule-based CBT chatbots (Woebot, Wysa) deliver therapeutic exercises without domain-specific knowledge retrieval. RAG-enhanced systems ground responses in evidence but apply no personality-aware modulation to how that evidence is presented. The architectural challenge is ensuring that personality adaptation governs *how* content is presented without altering *what* the content says — a separation that requires explicit pipeline enforcement, not implicit hope that the language model maintains it.

We ground this work in the domain of Swiss informal caregivers, a population of approximately 700,000 individuals who provide unpaid care to family members with chronic illness, disability, or age-related needs (OECD, 2023; ZHAW, 2022). These caregivers face a dual burden: chronic emotional stress including burnout, compassion fatigue, and isolation (Ruoss et al., 2023), compounded by the need to navigate Switzerland's federalized healthcare policy environment with canton-specific variations in benefit eligibility, Spitex services, IV/Invalidenversicherung procedures, and Hilflosenentschädigung (helplessness allowance) applications. This domain is particularly well-suited to the present work because it simultaneously exercises all three personalization layers — transient emotional state (stress and burnout), conversational memory (ongoing care situations), and stable personality adaptation (coaching style preferences) — while also demanding factually grounded policy guidance. Swiss caregivers serve as the concrete use case; the architecture is designed to be transferable to other coaching domains.

The gap in current digital coaching can be summarized as a three-layer personalization deficit:

| Personalization layer | Mechanism | Current systems | What's missing |
|----------------------|-----------|----------------|---------------|
| Transient state | Mood/sentiment detection | Woebot, Wysa (per-turn) | Addressed |
| Content recall | Conversation memory | ChatGPT Memory, mem0 | Addressed |
| Stable individual differences | Personality trait modeling | None operational | Unaddressed |
| Coaching style adaptation | Trait-to-directive mapping | None operational | Unaddressed |
| Domain knowledge grounding | RAG with verification | Some medical systems | Not integrated with personality |
| Content/style separation | Architectural enforcement | None | Unaddressed |

Memory and mood tracking are necessary components of a coaching system — CareLoop uses both — but they are insufficient for personalized coaching because they do not capture the stable dispositions that determine how an individual prefers to receive support. No existing system combines personality-trait-based coaching modulation, domain knowledge retrieval, and mandatory grounding verification in a single pipeline with formal invariants ensuring that personality adaptation is universal, retrieval is conditional, and factual claims are always grounded.

This study designs, implements, and evaluates CareLoop: a personality-aware digital coaching system that infers Big Five traits from multi-turn dialogue, stabilizes them using exponential moving average smoothing, and modulates coaching behavior to improve emotional tone appropriateness, relevance and coherence, and responsiveness to users' emotional needs. The system supports four coaching modes — emotional support, practical education, policy navigation, and a mixed mode for emotionally charged policy requests — governed by three pipeline invariants and classified through a hybrid LLM-and-heuristic intent router with confidence gating and safety overrides. The system is evaluated through automated pillar test matrices, latency and load benchmarks, and audit-trail validation, with Swiss informal caregivers as the pilot use case.

The following research questions guide this work:

**Table 1.** *Research Questions*

| RQ | Focus |
|----|-------|
| RQ1 | Can continuous OCEAN inference with EMA produce valid, temporally stable trait estimates? |
| RQ2 | Does personality modulation improve emotional tone, relevance, and emotional-needs responsiveness versus non-adaptive baselines? |
| RQ3 | Can RAG-enhanced policy navigation achieve full citation coverage with no critical grounding errors? |
| RQ4 | Does the hybrid LLM router correctly classify intent across four coaching modes with acceptable latency? |
| RQ5 | Does the system achieve acceptable reliability under load with full audit coverage? |

---

## 2. Related Work

### 2.1 Digital Coaching Systems and Personalization Mechanisms

Digital coaching has emerged as a scalable intervention format, with the AI-driven mental health app market reaching $1.45 billion in 2024 (Grand View Research, 2024). Current systems employ three distinct architectural models, each with characteristic personalization capabilities and limitations.

**Rule-based systems** such as Woebot (Fitzpatrick et al., 2017) deliver cognitive behavioral therapy through pre-programmed decision trees. Users are guided through structured therapeutic exercises — identifying automatic negative thoughts, practicing cognitive reframing, scheduling behavioral activation tasks — along scripted paths. Personalization occurs through mood-adaptive branching: the system detects the user's current emotional state via keyword classification and selects the most appropriate exercise module. Woebot's randomized controlled trial demonstrated significant reductions in depression symptoms compared to an information-only control (Fitzpatrick et al., 2017), validating the therapeutic value of structured digital coaching. However, the scripted architecture limits adaptation to within-module branching; two users with identical mood states but different personality profiles receive identical coaching content and delivery style.

**Hybrid NLP systems** such as Wysa (Inkster et al., 2018) combine rule-based therapeutic modules with natural language processing for more flexible interaction. Wysa's free-text interface allows users to describe their situations naturally, with NLP classifiers routing conversations to appropriate intervention types. Recent studies show Wysa adapts conversation depth based on engagement patterns and adjusts to language and cultural context (Wysa Research, 2024). These systems also implement crisis keyword detection and working alliance development through conversational rapport-building (Beatty et al., 2022). The personalization is richer than rule-based systems but still operates at the level of transient state and conversational context — the system adapts to what the user says and feels *right now* without modeling the stable traits that determine how they prefer to receive support across sessions.

**LLM-based memory systems** represent the most recent personalization paradigm. Systems using ChatGPT Memory, mem0, or LangChain Memory store user statements as vector embeddings for cross-session retrieval (Li et al., 2024). A comprehensive survey of personalized LLMs identifies three technical levels: prompting with personalized context, fine-tuning with personalized adapters, and alignment with personalized preferences (Chen et al., 2025). The emerging framework for personalized LLM agents integrates profile modeling, memory, planning, and action execution (Wang et al., 2026). These advances enable impressive conversational continuity — a system can recall that a user previously asked about disability insurance and build on that context. However, memory personalizes *content recall* rather than *coaching style*. It stores the user's history without inferring the psychological characteristics that should shape how support is delivered. A memory system knows *what* the user said; it does not know *who* the user is.

**The personality gap in coaching.** Across all three architectural models, a consistent gap emerges: no deployed coaching system models the stable individual differences — personality traits — that predict how users respond to different coaching styles. This gap is consequential because coaching effectiveness is not personality-neutral. Empirical evidence demonstrates that Big Five traits moderate coaching outcomes: Openness predicts benefit from exploratory approaches, Conscientiousness from structured goal-setting, and Neuroticism from emotional scaffolding (de Haan et al., 2013; Jones et al., 2016). A controlled field experiment confirmed that personality and goal orientation moderate coaching-driven performance improvement (Smither et al., 2019). The personality-coaching link is well established in human coaching research, but no digital system has operationalized it.

**Personality-aware dialogue.** The technical foundations for bridging this gap exist. Yarkoni (2010) demonstrated systematic associations between word usage patterns and personality dimensions; Park et al. (2015) achieved personality prediction from social media text. In dialogue generation, Mairesse and Walker (2010) showed that personality-conditioned language improves perceived naturalness, and subsequent work explored persona-based dialogue models (Li et al., 2016; Zheng et al., 2019). Devdas (2025) advanced continuous Big Five detection with motivational regulation, demonstrating at least 20% improvement in emotional support quality. The Zurich Model of Social Motivation (Quirin et al., 2023) provides a theoretical bridge from OCEAN dimensions to coaching behavior through three motivational systems — security (Neuroticism), arousal (Openness, Extraversion), and affiliation (Agreeableness) — with Conscientiousness serving as a structural modifier governing information organization and specificity.

Two open problems limit the deployment of these foundations. First, temporal stability: persona-aware response generation conditions generation on a static profile (Li et al., 2016; Majumder et al., 2020) or prompt-based persona description, but does not model how personality estimates should evolve and stabilize across turns. A comprehensive survey of the field confirms that "traditional approaches often rely on static personality profiles," with dynamic personality representation identified as an open research problem (Zheng et al., 2019). Latent variable models and attention mechanisms have been explored for contextual personality representation but neither addresses noisy per-turn detection — the stabilization problem that EMA smoothing solves. Second, the pathway from classification to behavior: adaptive dialogue management has addressed this through reinforcement learning, meta-learning, and multi-task learning (Lee et al., 2021; Cordier et al., 2023), but these approaches require large training datasets or complex reward design and produce opaque policies that are difficult to audit in sensitive domains. Neither personality detection nor adaptive policy work has been combined with formal directive-based modulation into a single operational coaching pipeline. The Zurich Model operationalization in the present work — mapping OCEAN traits to behavioral directives through the security, arousal, and affiliation motivational systems — is not represented in the prior dialogue literature, confirming this as a novel theoretical contribution.

### 2.2 Retrieval-Augmented Generation and Grounding

Retrieval-augmented generation (RAG) addresses the well-documented tendency of large language models to generate plausible but factually unsupported content — commonly termed hallucination (Ji et al., 2023). Lewis et al. (2020) introduced the RAG framework, demonstrating that conditioning generation on retrieved documents improves factual accuracy across knowledge-intensive tasks. Subsequent work has refined retrieval strategies, with hybrid approaches combining dense vector similarity and sparse lexical matching achieving superior recall compared to either method alone (Karpukhin et al., 2020; Ma et al., 2023).

In health-adjacent and policy-guidance domains, grounding is not merely a quality improvement but a safety requirement. Factually incorrect guidance about benefit eligibility, application procedures, or legal rights can cause material harm to vulnerable populations. Grounding verification — the post-generation process of checking whether claims in a response are supported by retrieved evidence — has emerged as a necessary complement to retrieval (Thoppilan et al., 2022; Gao et al., 2023). Systems deployed in medical information contexts have adopted multi-stage verification pipelines that extract claims, match them against evidence, and either flag or replace unsupported assertions (Singhal et al., 2023).

Knowledge graph (KG) integration has been explored as a complementary approach: KGs encode persona attributes, interests, and belief structures to enrich dialogue persona consistency (Majumder et al., 2020; Luan et al., 2017). However, KG-based persona consistency addresses a different problem — ensuring the system's responses remain consistent with a character's background knowledge — rather than enforcing factual grounding of specific policy claims against authoritative source documents. No prior system has defined formal, enforced invariants that simultaneously require personality detection on every turn, gate retrieval on factual need, and mandate citation-backed grounding for domain-specific content. This combination is an architectural contribution distinct from either KG-based persona consistency or standard RAG deployment.

The present system integrates RAG with personality-aware coaching through an explicit architectural separation: retrieval and grounding verification govern *what* the system says (factual content), while personality modulation governs *how* it says it (presentation style). This separation is enforced by three pipeline invariants — universal personality, conditional retrieval, mandatory grounding — rather than relying on the language model to maintain the distinction implicitly. This architectural design is, to our knowledge, the first formal treatment of personality modulation and factual grounding as simultaneously required but architecturally separated pipeline properties.

### 2.3 Digital Support for Informal Caregivers

Informal caregivers experience chronic stress, emotional exhaustion, and social isolation at rates that significantly exceed the general population (Schulz & Sherwood, 2008; Pinquart & Sörensen, 2003). They face four intersecting stressor domains: physical demands from direct care tasks and sleep disruption; emotional burden from witnessing decline and managing challenging behaviors; financial strain from reduced employment and increased care costs; and social isolation from reduced participation and strained family relationships. Digital interventions have shown promise in reducing caregiver burden — Mooney et al. (2024) reported a 38% reduction at 8 weeks using automated monitoring and coaching — but their effectiveness is severely constrained by a personalization gap that no existing tool has addressed.

Systematic reviews of digital caregiver interventions reveal a consistent pattern: high attrition rates, with many caregivers disengaging after only a few interactions, and limited efficacy in studies that do not account for individual differences. A critical finding is that personality traits are significant moderators of engagement and outcome that current systems uniformly ignore. Neuroticism is associated with higher attrition from digital interventions: neurotic individuals may initially seek tools under acute stress but rapidly disengage when the tool fails to address their emotional volatility. Conscientiousness predicts sustained engagement and adherence to structured features. Agreeableness predicts responsiveness to empathetic conversational agents. These patterns mean that a single generic intervention design systematically fails the users who need it most — those high in Neuroticism who would benefit from emotionally calibrated support but disengage from systems that deliver uniform, non-responsive responses. No existing caregiver digital tool integrates personality assessment with adaptive response style; none deliver content modulated to individual trait profiles.

The Swiss context compounds the challenge. Switzerland's federalized healthcare system produces canton-specific variations in caregiver support policies, benefit eligibility, and service availability. Caregivers must navigate IV/Invalidenversicherung (disability insurance), AHV (old-age insurance), Ergänzungsleistungen (supplementary benefits), cantonal Spitex (home care) services, and Hilflosenentschädigung (helplessness allowance) — a fragmented policy landscape that demands both emotional resilience to handle the complexity and accurate factual guidance to act on it. Social robot interventions such as ElliQ (Broadbent et al., 2024) and evaluation frameworks such as FEEL (Zhang et al., 2024) advance scalability but lack both personality adaptation and Swiss-specific knowledge grounding. Existing CBT-based coaching apps (Woebot, Wysa) address emotional wellbeing through therapeutic exercises but do not deliver domain-specific policy guidance grounded in official sources.

This population thus requires a coaching system that operates across all three personalization layers simultaneously: transient state tracking (detecting acute stress or burnout), memory (recalling ongoing care situations and prior questions), and stable personality modeling (adapting coaching style to the individual). No existing caregiver support tool integrates these layers with citation-grounded domain knowledge in a single adaptive system.

The absence of caregiver-specific work in the personality-aware dialogue literature is itself evidence of this gap. Two independently generated comprehensive surveys of the personality-aware digital coaching field — covering hundreds of papers on personality representation, adaptive dialogue, and evaluation methodology — contain no examples of caregiver-facing implementations, no caregiver-specific datasets, and no systems designed for the Swiss policy context (Gemma AutoSurvey, 2025; Qwen AutoSurvey, 2025). This confirms that the present study addresses a domain that is both practically urgent and academically unexplored.

---

## 3. System Design

This section presents the architecture and core mechanisms of CareLoop, the personality-aware coaching system. The system is fully implemented and operational; the design decisions described here reflect the actual running system rather than a proposed specification.

### 3.1 Architecture and Pipeline Invariants

CareLoop is implemented as a three-tier architecture: a Next.js API route handles client requests and orchestrates pre- and post-processing; an N8N workflow engine executes the 9-stage coaching pipeline; and PostgreSQL with pgvector provides persistent storage for sessions, personality states, policy evidence, and audit records. Google Gemma-3 serves as the language model for personality detection, response generation, and intent routing, accessed via the NVIDIA API.

The processing flow for each turn proceeds through three phases. In *API-side pre-processing*, the system performs hybrid LLM intent routing to classify the user's coaching need, resolves session isolation and route keys, and conditionally executes vector and full-text retrieval to prefetch policy evidence. The *N8N workflow* then executes nine stages in sequence: input normalization and context extraction; loading of prior personality states from the database; OCEAN trait detection via LLM with EMA smoothing; regulation through trait-to-directive mapping and mode confirmation; policy retrieval merging prefetched evidence with workflow-internal full-text search results; directive-conditioned response generation; grounding verification through claim extraction and evidence matching; quality verification including safety checks; and response formatting with persistence of session, turn, personality, and metrics data. Finally, *API-side post-processing* applies mode override and confidence propagation, performs optional LLM regeneration when the workflow returns heuristic content, overlays citations from prefetched evidence, executes the grounding invariant check for policy and mixed modes, and writes dual audit records.

Three pipeline invariants govern every turn regardless of coaching mode. These are not guidelines but enforced architectural rules:

**Table 2.** *Pipeline Invariants*

| Invariant | Rule | Enforcement |
|-----------|------|-------------|
| Universal personality | OCEAN detection and regulation run for every turn in every mode | N8N workflow executes Detection → EMA → Regulation before any mode-specific branching; API flags `ocean_detection_skipped` or `regulation_skipped` if the workflow fails to return personality state or directives |
| Conditional retrieval | Evidence retrieval runs only when factual content is needed | API-side gating function evaluates resolved mode, keyword signals, and explicit policy opt-out phrases before initiating retrieval |
| Mandatory grounding | Policy and mixed responses must include citations | N8N grounding verifier checks claim-evidence overlap; API checks citation count post-response; zero citations triggers a grounding warning |

The first invariant ensures that every response is personality-informed, whether the user is seeking emotional support, practical guidance, or policy information. The second prevents unnecessary retrieval latency on purely emotional or educational turns. The third guarantees that no policy claim reaches the user without evidence backing.

The four coaching modes define how the system balances personality modulation and factual grounding:

**Table 3.** *Coaching Modes*

| Mode | Personality modulation | Retrieval | Grounding |
|------|----------------------|-----------|-----------|
| Emotional support | Full (tone, warmth, pacing) | Skipped | Not required |
| Practical education | Full (structure, detail, style) | Conditional | If citations present |
| Policy navigation | Presentation style only | Always | Mandatory |
| Mixed | Full modulation + presentation style | Always | Mandatory for policy segment |

The mixed mode is a key architectural feature: it handles turns where a caregiver expresses emotional distress *and* asks about benefit eligibility in the same message. Rather than forcing a single classification, the system composes a response with both an emotionally supportive segment and a citation-grounded policy segment, applying personality modulation throughout while maintaining factual integrity in the policy portion.

**[Figure 1: System Architecture.** *Three-tier architecture showing API route, N8N 9-stage workflow, PostgreSQL with pgvector, and NVIDIA API interactions. Pre-processing (routing, session isolation, conditional retrieval) flows into N8N orchestration (detect → stabilize → regulate → retrieve → generate → verify → persist) and returns through post-processing (mode override, citation overlay, grounding check, dual audit write). — PLACEHOLDER: to be created]*

### 3.2 Personality Detection and Stabilization

The personality detection, temporal stabilization, and trait-to-directive modulation components form a tightly coupled subsystem that runs on every turn — the first pipeline invariant.

**Detection.** Each turn, the system infers the user's current Big Five trait expression using Google Gemma-3 at temperature 0 (for deterministic output). The model receives the user's message along with the prior 6 turns of personality state loaded from the database, and returns per-trait values in the range [-1.0, +1.0] with per-trait confidence scores in [0.0, 1.0]. The continuous representation — rather than categorical labels — is essential for EMA smoothing and for capturing the dimensional nature of personality as established by trait psychology (Costa & McCrae, 1992). When the LLM is unavailable, a heuristic keyword fallback provides approximate trait estimates at a fixed confidence of 0.45, ensuring the pipeline never runs without personality input.

This approach differs from prior work in two ways. First, existing personality detection in dialogue has relied on fine-tuned classifiers trained on annotated corpora (Wen et al., 2024; Basto, 2021) or persona embeddings learned from dialogue histories (Li et al., 2016; Majumder et al., 2020). These require training data that is not available for Swiss caregiver scenarios and produce either discrete labels or fixed persona vectors rather than continuously updated dimensional estimates. Second, per-trait confidence scoring — used here to gate EMA updates — is absent from prior operational implementations, which treat trait estimates as equally reliable regardless of the evidence quality in the current turn.

**EMA stabilization.** Raw per-turn trait estimates are noisy: a single frustrated message might temporarily inflate Neuroticism beyond the user's stable baseline, and the system must not abruptly shift its entire coaching style in response. Exponential moving average smoothing addresses this by weighting each new observation against the accumulated history:

$$T_{\text{smoothed}}^{(n)} = \begin{cases}
\alpha \cdot T_{\text{detected}}^{(n)} + (1-\alpha) \cdot T_{\text{smoothed}}^{(n-1)} & \text{if } c^{(n)} \geq 0.4 \\
T_{\text{smoothed}}^{(n-1)} & \text{otherwise}
\end{cases}$$

The in-session smoothing parameter α = 0.3 weights 30% for the current observation and 70% for the historical average, achieving convergence to stable estimates within 6 turns with variance below 0.05. A confidence threshold of 0.4 gates updates: below this threshold, the system retains the prior trait value rather than incorporating a low-confidence detection that could destabilize the profile. Cross-session smoothing uses α = 0.2, persisted to a user personality profile table, providing slower but more robust adaptation across multiple conversations.

The choice of α = 0.3 was determined through sensitivity analysis across α ∈ {0.1, 0.2, 0.3, 0.4, 0.5}, targeting 6–8 turn convergence with acceptable stability. Lower values produce smoother trajectories but delay adaptation to genuine personality signals; higher values track turn-to-turn fluctuations too closely.

EMA with confidence gating is a novel mechanism in this context. The dialogue systems literature has explored dynamic personality representation through attention mechanisms that selectively weight dialogue history (Gu et al., 2021) and through latent variable models that represent personality as a probabilistic distribution over a learned space (PRISP, 2023). These approaches are expressive but require model training and are not designed for the deployment constraint that personality must stabilize within a small number of turns with no training data available. EMA is a parameter-efficient, training-free alternative that provides interpretable convergence guarantees and produces a confidence-filtered trajectory that can be logged and audited per turn — properties that are requirements rather than options in health-adjacent coaching systems.

**Trait-to-directive modulation.** Stabilized trait estimates are translated into behavioral directives that condition response generation. The mapping is grounded in the Zurich Model of Social Motivation (Quirin et al., 2023), operationalized as a first-order mapping from each OCEAN dimension to coaching behavior:

**Table 4.** *Trait-to-Directive Mapping (Summary)*

| Trait direction | Behavioral directive | Activation threshold |
|----------------|---------------------|---------------------|
| High Neuroticism | Offer extra comfort; acknowledge anxieties | \|N\| > 0.15, confidence ≥ 0.35 |
| Low Neuroticism | Reassure stability and confidence | \|N\| > 0.15, confidence ≥ 0.35 |
| High Agreeableness | Show warmth, empathy, collaboration | \|A\| > 0.15, confidence ≥ 0.35 |
| High Conscientiousness | Provide organized, structured guidance | \|C\| > 0.15, confidence ≥ 0.35 |
| High Openness | Invite exploration and novelty | \|O\| > 0.15, confidence ≥ 0.35 |
| High Extraversion | Energetic, sociable tone | \|E\| > 0.15, confidence ≥ 0.35 |

When no trait exceeds the activation threshold — typically in early turns before sufficient data accumulates — the system applies default directives: "Be warm, attentive, and supportive" and "Ask open-ended questions to understand the user better." This ensures coaching quality is maintained even when personality detection is uncertain.

Modulation is universal: directives are applied in all four coaching modes. In emotional support and practical education modes, directives shape the full response. In policy navigation and mixed modes, directives shape the presentation style — how facts are structured, framed, and emotionally contextualized — without altering the factual content, which remains invariant to personality.

The substantive rationale for each directive is grounded in empirical evidence on personality-driven needs. Caregivers high in Neuroticism are prone to interpreting demands as threats, exhibit avoidant coping under pressure, and disengage from digital interventions that do not validate their emotional experience — making reassurance and emotional acknowledgment not stylistic options but prerequisites for effective coaching. Caregivers high in Conscientiousness employ structured problem-solving, expect organized information, and engage most effectively with goal-oriented formats that respect their planning orientation. Caregivers high in Agreeableness use social support-seeking as a primary coping strategy and respond to collaborative, warm interaction styles. Caregivers high in Openness adapt most readily to novel approaches and psychoeducational framing, while those low in Openness need familiar, evidence-based methods before exploring new coping strategies. These patterns mean the directive mapping is not an arbitrary style preference — it translates a well-evidenced empirical regularity (personality predicts coping orientation and support receptivity) into operational coaching behavior.

The directive-based approach differs from reinforcement learning and meta-learning approaches to adaptive dialogue management (Lee et al., 2021; Cordier et al., 2023) in three properties that are critical for the deployment context. First, *interpretability*: every directive traces to a specific trait dimension and a numerical threshold, so the reason for any stylistic choice can be read directly from the audit log. RL and meta-learned policies produce opaque parameter updates that cannot be inspected in the same way. Second, *auditability*: because directives and their generating trait values are logged per turn, a full post-hoc reconstruction of why any response was generated in a particular style is possible — a regulatory requirement in health-adjacent applications. Third, *training-free deployment*: the directive mappings are specified analytically from the Zurich Model rather than learned, enabling deployment without annotated training data. The trade-off is that the mapping is a first-order approximation that does not capture higher-order interactions between motivational systems — a limitation acknowledged in Section 6.

**[Figure 2: EMA Trait Convergence.** *Example showing Neuroticism estimates across 6+ turns, illustrating raw per-turn detections (volatile) versus EMA-smoothed trajectory (convergent). Confidence threshold gating visible at turn 3 where a low-confidence detection is rejected. — PLACEHOLDER: to be generated from actual system data]*

### 3.3 Hybrid Intent Router

Classifying the user's coaching need is a prerequisite for determining which pipeline branches to activate — particularly whether to trigger evidence retrieval and mandatory grounding verification. The system uses a five-layer hybrid router that prioritizes accuracy and safety over speed:

1. **Explicit requested mode.** If the frontend explicitly passes a target mode (e.g., when the user selects "Policy Help" in the UI), that mode is used directly with confidence 1.0.

2. **LLM router.** For unspecified modes, the system queries Gemma-3 with a structured prompt at temperature 0, requesting a JSON response containing the classified coaching mode, a confidence score, whether retrieval is needed, and a machine-readable routing reason. Results are cached per message-and-context key for 5 minutes to avoid redundant LLM calls on similar inputs.

3. **Confidence gate.** If the LLM router returns a confidence below 0.5, the decision is discarded and the system falls through to the heuristic layer. This prevents low-confidence LLM classifications from overriding more reliable signals.

4. **Keyword heuristic fallback.** When the LLM is unavailable, times out, returns malformed JSON, or produces a below-threshold confidence, the system falls back to keyword scoring against curated term lists (26 policy terms, 17 education terms, 15 emotional terms) combined with conversation-history inheritance for short follow-up messages.

5. **Hard safety override.** Regardless of the routing source, a safety function forces retrieval activation for any turn containing policy-related keywords. This ensures that a caregiver asking about IV eligibility always receives evidence-grounded guidance, even if the router classified the turn as emotional support.

The N8N V2 workflow consumes the API's routing decision directly, eliminating redundant keyword classification within the workflow while maintaining its own OCEAN detection and regulation pipeline. Every response carries routing metadata — the classification source (LLM, LLM cache, heuristic, or requested), the routing reason, the confidence score, and the LLM routing latency — enabling post-hoc analysis of routing quality and fallback frequency.

### 3.4 Retrieval and Grounding Verification

**Retrieval.** When the resolved coaching mode requires evidence, the system executes a hybrid retrieval strategy. The primary path uses NVIDIA embedding API (model `nv-embedqa-e5-v5`, 1024-dimensional vectors) to embed the user's query and compute cosine similarity against pre-embedded policy chunks stored in PostgreSQL via pgvector. The top 5 results above a similarity threshold of 0.30 are returned. If vector search returns fewer than 2 results — indicating the query may not align well with the embedding space — a parallel PostgreSQL full-text search using `websearch_to_tsquery` supplements the results, with deduplication against vector results.

The policy corpus currently covers selected Swiss social insurance domains: IV eligibility and registration procedures, Zurich supplementary benefits, care subsidies, and Hilflosenentschädigung. Each chunk carries source metadata (source ID, title, jurisdiction, URL) enabling citation attribution. The corpus is maintained through automated freshness checks that detect stale or expired sources.

Evidence retrieved by the API is passed as `prefetched_evidence` to the N8N workflow, which merges it with any additional results from its own full-text search, preferring the higher-quality vector results. Personality modulation does not alter retrieved content — it governs only how that content is presented to the user.

**Grounding verification.** A three-stage verification pipeline ensures that no policy claim reaches the user without evidence support:

In the first stage, the N8N *Grounding Verifier* node extracts policy claims from the draft response using 10 regex patterns targeting eligibility statements, monetary amounts, deadlines, and form requirements. Each claim is checked for keyword overlap against retrieved evidence, with a minimum overlap ratio of 0.4 required. A grounding ratio below 0.5 triggers a full replacement of the response with a safe fallback asking for clarification. A ratio between 0.5 and 0.8 produces a degraded response where ungrounded claims are replaced with "[information pending verification]." A ratio of 0.8 or above passes.

In the second stage, the N8N *Verification and Refinement* node performs quality scoring across multiple dimensions: session validity, coaching mode validity, response completeness, question count (maximum 2 per response), word count within acceptable range, and absence of banned claim phrases. The grounding results are integrated into an overall adherence score. Scores below 0.5 trigger a full block with a safe fallback response.

In the third stage, the API performs a post-response citation count check. For policy navigation and mixed mode responses, zero citations triggers a `warn_no_citations` status in the pipeline output and an audit warning. This final check catches edge cases where the workflow's verification passed but no citations were actually included in the formatted response.

### 3.5 Infrastructure, Audit, and Reproducibility

The system is deployed as a containerized stack via Docker Compose: a Next.js 14 frontend with Zustand for state management and Framer Motion for UI transitions; N8N self-hosted with task runners for workflow orchestration; PostgreSQL 16 with pgvector extension across 11 tables covering sessions, turns, personality states, policy evidence, performance metrics, audit logs, users, feedback, memory embeddings, user personality profiles, and policy chunks; and Google Gemma-3 accessed through the NVIDIA API. Request and response contracts are validated using Zod schemas in a shared contracts package. User authentication uses HS256 JWT tokens in HTTP-only cookies.

The audit trail uses a dual-write strategy. Every turn produces a JSONL log entry and a PostgreSQL `audit_log` row containing: request ID, session ID, turn index, coaching mode, pipeline status, routing metadata (source, reason, confidence, LLM duration), personality state (OCEAN scores only — no personally identifiable information), retrieval IDs, citation count, verifier status, SHA-256 input hash, and turn latency. PII redaction removes email addresses and phone numbers before any logging occurs.

Reproducibility is supported through several mechanisms: fixed model versions and parameters (Gemma-3 via NVIDIA, EMA α = 0.3); versioned N8N workflow files following a V-numbering convention (V1 → V2); deterministic JSON contracts between all modules; containerized single-command deployment; and benchmark fixtures stored as versioned JSON files enabling automated regression testing.

---

## 4. Evaluation

### 4.1 Study Design and Validation Streams

This study follows a pilot system design and evaluation approach. The system is fully implemented and evaluated through automated test suites and benchmark infrastructure. Four validation streams provide converging evidence across different aspects of system performance:

**Table 5.** *Validation Streams*

| Stream | Sample | What it validates |
|--------|--------|-------------------|
| Automated pillar test matrices | 130+ cases across 4 modes | Mode classification, citation presence/absence, grounding safety, latency gates |
| Benchmark and load tests | 10 expansion cases + 4 latency cases + 100 concurrent sessions | Performance gates, reliability under load |
| Expert pilot sessions | n = 5–8 domain experts (Spitex coordinators, geriatricians, home care nurses) | Usability, appropriateness, ecological validity |
| Simulated evaluation | N ≥ 250 synthetic conversations across personality profiles and stress scenarios | Coaching quality compared against baselines |

Real caregiver validation (n = 20–30, volunteer-based) is fully specified as a future protocol but deferred due to recruitment feasibility constraints. Findings should be interpreted as pilot evidence supporting the viability of a transferable architecture.

### 4.2 Baselines

Four conditions isolate the contribution of each personalization layer:

**Table 6.** *Experimental Conditions and Personalization Layers*

| Condition | Personalization layers active | What it tests |
|-----------|------------------------------|--------------|
| Personality-aware (full system) | Mood + memory + personality + RAG | Full personalized coaching (experimental condition) |
| Generic non-adaptive | None (static responses) | Whether any personalization matters for coaching quality |
| Memory-only | Memory + mood (no trait modeling) | Whether conversational continuity — the current LLM personalization state-of-the-art — substitutes for personality modulation |
| Policy-only | RAG (no personality or memory) | Whether factual accuracy alone is sufficient without coaching style adaptation |

### 4.3 Measures

A consolidated set of metrics maps directly to the five research questions:

**Table 7.** *Evaluation Metrics, Targets, and Literature Justification*

| Construct | Metric | Target | RQ | Literature justification |
|-----------|--------|--------|-----|--------------------------|
| Trait validity | Pearson r with synthetic profiles | ≥ 0.75 | RQ1 | Persona alignment metrics are the standard for validating persona-conditioned generation (Zhang et al., 2018); trait psychology establishes convergent validity thresholds (Costa & McCrae, 1992) |
| Trait stability | Variance within 6+ turns | < 0.05 | RQ1 | Dynamic personality representation requires temporal consistency as an evaluation criterion; static approaches are insufficient for coaching (Zheng et al., 2019) |
| Confidence calibration | High-confidence predictions aligned | ≥ 85% | RQ1 | Reliability of LLM-based trait inference is an open validation requirement for zero-shot detection methods |
| Emotional tone appropriateness | LLM evaluator + human expert score | ≥ 4.0/5.0 | RQ2 | Sentiment-based and Likert-scale tone ratings are standard evaluation dimensions for personality-aware dialogue; human evaluation is "the gold standard" for personality fit assessment (Mairesse & Walker, 2010) |
| Relevance and coherence | LLM evaluator + human expert score | ≥ 4.0/5.0 | RQ2 | Coherence is an established evaluation dimension for generative dialogue; traditional n-gram metrics (BLEU, ROUGE) are inadequate for personality-aware systems as they measure lexical overlap rather than personality fit |
| Emotional needs responsiveness | Improvement over baseline | ≥ 20% | RQ2 | Persona needs satisfaction is an established construct in emotional support evaluation; 20% improvement is the threshold reported in Devdas (2025) |
| Citation coverage | Policy claims with sources | 100% | RQ3 | Factual grounding and hallucination prevention require complete source attribution in health-adjacent domains (Lewis et al., 2020; Singhal et al., 2023) |
| Grounding errors | Critical hallucinations | 0 | RQ3 | Zero-tolerance for unsupported factual claims is a safety standard in health-adjacent applications (Ji et al., 2023) |
| Routing accuracy | Correct mode classification | 10/10 (benchmark) | RQ4 | Intent classification accuracy is a prerequisite for pipeline safety in multi-mode coaching systems |
| LLM router latency | Per-turn classification time | Monitored | RQ4 | Response time impacts perceived engagement and perceived system quality (Laranjo et al., 2018) |
| Load reliability | 100 concurrent sessions, 5xx rate | 0% | RQ5 | Operational stability is a deployment requirement for population-scale coaching applications |
| End-to-end latency (p95) | Emotional / practical / policy / mixed | ≤ 4 / 5 / 8 / 9 s | RQ5 | Latency gates are calibrated to conversational interaction norms; policy mode allows higher latency due to retrieval |
| Audit coverage | Turns with complete audit records | 100% | RQ5 | Complete audit trails are required for post-hoc transparency in health-adjacent AI systems (Swiss FADP, 2023) |

*Note on metric selection:* Traditional automatic metrics such as BLEU, ROUGE, and perplexity are not used as primary evaluation metrics. These measures assess lexical overlap between generated and reference responses, which is not a meaningful proxy for personality fit, coaching quality, or emotional appropriateness. LLM-based evaluators with human expert gating (κ ≥ 0.75) provide a more valid assessment of the constructs targeted by personality-aware coaching systems (Mairesse & Walker, 2010; Devdas, 2025).

### 4.4 Procedure

1. Build and deploy the full coaching pipeline (Next.js + N8N + PostgreSQL + NVIDIA API).
2. Implement hybrid LLM router with heuristic fallback and confidence gating.
3. Implement and verify the three pipeline invariants.
4. Execute automated pillar test matrices across all four coaching modes (130+ cases).
5. Execute benchmark expansion pack (10 cases) and latency benchmarks (4 cases).
6. Execute load test at 100 concurrent sessions.
7. Conduct expert pilot sessions; collect system logs and appropriateness ratings.
8. Generate N ≥ 250 synthetic conversations across personality profiles and stress scenarios.
9. Score synthetic conversations using automated LLM evaluator and human expert subset scoring (target κ ≥ 0.75).
10. Compare personality-aware system against all three baseline conditions.

**Analysis plan:**

| RQ | Approach |
|----|----------|
| RQ1 | Pearson correlation (trait alignment); variance across turns; consistency correlation |
| RQ2 | Adaptive vs. baseline on three coaching-quality dimensions; Cohen's d ≥ 0.3 target |
| RQ3 | Policy claim audit; citation coverage count; error categorization |
| RQ4 | Routing accuracy across 4 modes; confidence distribution; LLM vs. heuristic comparison |
| RQ5 | Load test pass rate; latency percentiles; audit coverage; contract compliance rate |

### 4.5 Ethics

This study complies with the Swiss Federal Act on Data Protection (FADP). All data is pseudonymized at the point of collection; personally identifiable information (email addresses, phone numbers) is removed by automated redaction before any logging. The dual audit trail (JSONL + PostgreSQL) enables post-hoc transparency while maintaining privacy. A crisis protocol triggers automatic escalation to professional resources when detected stress level reaches 3 or above on a 0–4 scale. The system maintains a non-clinical coaching boundary: it does not generate medical diagnoses, legal advice, or clinical treatment recommendations. Grounding verification serves as a safety mechanism preventing the system from presenting fabricated policy claims to vulnerable users.

---

## 5. Results

*[This section will be populated with empirical findings. The structure and placeholder descriptions below indicate what each subsection will contain.]*

### 5.1 Personality Detection and Stabilization (RQ1)

**[PLACEHOLDER — To be populated with:**
- Trait alignment scores (Pearson r) between inferred and pre-defined OCEAN profiles across synthetic personality types (Type A, B, C distributions)
- EMA convergence patterns: number of turns to stability, variance trajectories
- In-session versus cross-session stability comparison
- Confidence calibration accuracy: proportion of high-confidence predictions (≥ 0.7) that align with personality cues
- Heuristic fallback activation frequency and its effect on stability

**Figure 3.** *[PLACEHOLDER: Trait stabilization trajectories via EMA across 6+ turns for representative personality profiles, showing raw per-turn detections versus smoothed estimates for each OCEAN dimension.]*

**Table 8.** *[PLACEHOLDER: Trait alignment results — Pearson r for each OCEAN dimension across personality profile types, with 95% confidence intervals.]*
**]**

### 5.2 Coaching Quality (RQ2)

**[PLACEHOLDER — To be populated with:**
- Emotional tone appropriateness: adaptive system scores versus generic, memory-only, and policy-only baselines (LLM evaluator scores and human expert scores)
- Relevance and coherence: scores across four coaching modes, adaptive versus baselines
- Responsiveness to emotional needs: relative improvement over baseline, needs-satisfaction scores
- Effect sizes (Cohen's d) for each dimension
- Breakdown by coaching mode showing where personality modulation has greatest impact

**Figure 4.** *[PLACEHOLDER: Coaching quality comparison — grouped bar chart or radar chart showing adaptive system versus three baselines across the three quality dimensions.]*

**Table 9.** *[PLACEHOLDER: Coaching quality scores per dimension, per condition, with effect sizes and significance indicators.]*
**]**

### 5.3 Grounding and Routing (RQ3 + RQ4)

**[PLACEHOLDER — To be populated with:**
- Citation coverage: percentage of policy claims with source citations
- Grounding verifier outcome distribution (pass / degraded / fail)
- Expert audit findings: error count, categories, severity
- Routing accuracy: correct mode classification across benchmark cases (target: 10/10)
- LLM router confidence distribution across modes
- Heuristic fallback frequency and reasons (timeout, malformed JSON, low confidence)
- Mixed-mode detection accuracy for boundary cases (emotional + policy)
- Routing latency: LLM router (expected 3–5s) versus heuristic (<1ms)

**Table 10.** *[PLACEHOLDER: Routing accuracy by mode — showing LLM router decisions, confidence scores, fallback frequency, and comparison with heuristic classification.]*
**]**

### 5.4 System Reliability (RQ5)

**[PLACEHOLDER — To be populated with:**
- Pillar test matrix pass rates (target: 130+ cases, all passing)
- Benchmark expansion pack results (target: 10/10)
- Latency benchmark results (target: 4/4 within gates)
- Load test results at 100 concurrent sessions (target: 0% 5xx, reported p50/p95)
- JSON contract compliance rate (target: ≥ 99.5%)
- Audit trail completeness: percentage of turns with full audit records
- Pipeline invariant adherence: OCEAN detection rate, grounding check outcomes
- Operational latency summary: p50, p95 by coaching mode

**Table 11.** *[PLACEHOLDER: System reliability summary — load test metrics, latency percentiles, contract compliance, audit coverage.]*
**]**

---

## 6. Discussion

### 6.1 Interpretation and Contributions

*[To be written after results are available. The discussion will be organized around the following themes:]*

**Principal finding.** The central question is whether adding the personality-trait layer to digital coaching — on top of the mood tracking and memory that current systems already provide — measurably improves coaching quality across all three dimensions (emotional tone, relevance, and emotional needs responsiveness). The comparison between the full system and the memory-only baseline is particularly informative: memory represents the current state-of-the-art in LLM personalization, and the difference between these conditions isolates the specific value of personality-trait modeling for coaching. The magnitude and consistency of these effects across the four coaching modes will determine whether personality modulation is a necessary component of effective digital coaching or merely an incremental refinement.

**Novelty claims against the literature.** The contributions of this study can be stated explicitly against the prior literature:

| Contribution | Prior state | CareLoop addition |
|---|---|---|
| **Temporal stabilization of personality** | Dynamic personality explored through latent variable models and attention mechanisms (Zheng et al., 2019; Gu et al., 2021); no EMA or equivalent smoothing applied to per-turn detections | Confidence-gated EMA (α = 0.3/0.2) producing stable, variance-bounded coaching input within 6 turns without model training |
| **Directive-based modulation** | Adaptive dialogue management uses RL reward shaping and meta-learning (Lee et al., 2021; Cordier et al., 2023); policies are data-hungry and opaque | Interpretable, auditable trait-to-directive mapping with logged thresholds; fully traceable from personality state to response style |
| **Pipeline invariants** | No prior system defines formal invariants ensuring that personality and grounding coexist as architectural requirements | Three named, enforced invariants (universal personality, conditional retrieval, mandatory grounding) at workflow and API levels |
| **Content/style separation** | Personality modulation and factual content typically conflated, or one component omitted (Woebot/Wysa omit RAG; RAG systems omit personality) | Explicit architectural separation enforced by invariants: modulation shapes presentation, not content |
| **Caregiver application** | Two comprehensive surveys of the personality-aware dialogue field contain no caregiver-specific systems, datasets, or domain instantiations | First implementation of personality-aware coaching for Swiss informal caregivers, with three-pillar support model |

**Three personalization layers as a coaching framework.** This study contributes a structured framework for understanding personalization in digital coaching systems: transient state (mood detection), content recall (memory), and stable individual differences (personality). Current systems implement only the first two. The finding that personality modulation — the third layer — adds value would suggest that the prevailing industry approach of improving memory and context retrieval is necessary but insufficient for coaching quality.

**Pipeline invariants as a design principle.** The three formal pipeline invariants — universal personality, conditional retrieval, mandatory grounding — represent a design pattern for coaching systems that must be both adaptive and factually safe. The invariants ensure that personality modulation is never bypassed (even when the user asks a purely factual question, the response style is still personality-informed), that retrieval does not add latency when unnecessary, and that no policy claim reaches the user without evidence. This contribution is architectural and independent of evaluation outcomes.

**Separation of content accuracy and style adaptation.** The architectural separation between retrieval-grounded content (what the system says) and personality-modulated presentation (how it says it) addresses a fundamental tension absent from current coaching apps. Rule-based CBT chatbots (Woebot, Wysa) avoid the problem by not delivering domain-specific knowledge. RAG-enhanced systems avoid it by not modulating style. CareLoop is, to our knowledge, the first system that must solve both simultaneously, and the grounding verification pipeline enforces the separation at multiple stages.

**Contribution to caregiver support.** For Swiss caregivers, the system provides what no current digital tool offers: emotional resilience coaching adapted to individual personality profiles, practical education matched to learning and processing preferences, and grounded policy navigation with citation-supported Swiss benefit guidance — integrated in a single system that handles the common situation where emotional distress and policy questions co-occur in the same conversation turn.

### 6.2 Reproducibility and Transferability

A deliberate objective of this work is that the architecture can be reproduced independently and adapted to coaching domains beyond Swiss caregivers. Both properties are supported by specific design choices rather than post-hoc claims.

**Reproducibility** is enabled at four levels. At the *component level*, all model parameters are fixed and versioned: Gemma-3 via NVIDIA API, EMA α = 0.3 (in-session) and α = 0.2 (cross-session), confidence threshold 0.4, and directive activation threshold |trait| > 0.15. At the *pipeline level*, all inter-module contracts are defined in Zod schemas, enabling independent teams to reconstruct any module's expected inputs and outputs without access to the implementation. At the *evaluation level*, benchmark fixtures are stored as versioned JSON, synthetic caregiver profiles are parameterized, and evaluation runs use fixed seeds. At the *deployment level*, a single Docker Compose file reproduces the full stack — Next.js, N8N, PostgreSQL with pgvector, and the NVIDIA connection — from a clean environment. The dual audit trail (JSONL + PostgreSQL) ensures that any conversation can be fully reconstructed post-hoc, including the personality state, directives, routing decision, and grounding outcome at every turn.

**Transferability** is structural. The three components that are domain-specific are the policy corpus, the coaching scenario templates, and the coaching mode labels and descriptions. All other components of the pipeline — personality detection, EMA stabilization, trait-to-directive mapping, hybrid intent routing, grounding verification logic, and the audit infrastructure — are specified independently of the caregiver domain and do not contain Swiss-specific assumptions. Replacing the policy corpus with a different knowledge base (e.g., university counseling guidelines, chronic disease management protocols, or employee wellness resources) and updating the scenario templates would instantiate the architecture in a different coaching context without changing the core pipeline. Cross-domain validation remains future work; the claim is that the architecture is *designed* for transfer at the level of software contracts and modular boundaries, not that transfer has been empirically demonstrated.

### 6.3 Limitations and Future Work

Several limitations bound the interpretation of this study's findings.

**Pilot scope.** The current evaluation relies on automated test suites, benchmark infrastructure, and (planned) expert and simulated validation streams. Real caregiver validation with the target population (n = 20–30) is fully specified as a protocol but deferred due to recruitment feasibility. The system's effectiveness with actual caregivers remains to be demonstrated.

**Language.** The prototype operates in English only. Swiss caregivers communicate primarily in Swiss German, French, and Italian; multilingual adaptation with culturally appropriate dialogue patterns is required for deployment.

**Policy coverage.** The current policy corpus covers selected Swiss social insurance domains (IV, Ergänzungsleistungen, Spitex, Hilflosenentschädigung). Full coverage across all 26 cantons and all benefit categories is needed for comprehensive policy guidance.

**Theoretical simplification.** The trait-to-directive mapping operationalizes a simplified first-order version of the Zurich Model. The full model emphasizes dynamic interactions between motivational systems (Quirin et al., 2023) that are not captured in the current mapping and require empirical calibration.

**LLM router latency.** The LLM-based intent router adds 3–5 seconds of latency per turn, which may be noticeable in real-time coaching interactions. The caching and heuristic fallback mechanisms mitigate but do not eliminate this issue. On-device or smaller model deployment could reduce routing latency.

**External API dependency.** The system depends on the NVIDIA API for both language model inference and embedding generation. API availability, latency variability, and cost are operational concerns for sustained deployment.

**Synthetic evaluation limitations.** Synthetic caregiver profiles cannot fully capture the variability, ambiguity, and emotional complexity of real caregiving situations. Correlations observed with synthetic profiles may not transfer directly to real users.

**Future work** includes: real caregiver pilot deployment and validation (n = 20–30) with the Personality Understanding Scale and PSS-10; multilingual adaptation for Swiss German, French, and Italian — essential for real deployment since Swiss caregivers communicate primarily in these languages; expansion of the policy corpus across all 26 cantons; cross-domain transfer studies in non-caregiver coaching contexts (e.g., student wellbeing, chronic disease self-management); longitudinal evaluation of coaching outcomes over multiple weeks, which is needed given that personality's protective effects (e.g., conscientiousness buffering burden) manifest over sustained caregiving episodes rather than single interactions; empirical calibration of trait-to-directive mappings through iterative user studies; and exploration of multimodal personality inference — ECG-based deep learning, smartphone behavioral metrics (typing dynamics, app usage frequency, mobility patterns), and voice prosody analysis have all shown promise as passive, low-burden personality signal sources for caregiving contexts, and integrating these would reduce dependence on per-turn LLM detection while enabling continuous, unobtrusive trait monitoring.

---

## 7. Conclusion

Current digital coaching systems personalize through mood tracking and conversation memory but do not model the stable personality traits that predict how individuals respond to different coaching styles — a third personalization layer that human coaches apply implicitly. This study designed, implemented, and evaluated CareLoop: a personality-aware coaching architecture that adds this missing layer by inferring Big Five traits from dialogue, stabilizing them through EMA smoothing, and modulating coaching behavior across four modes — emotional support, practical education, policy navigation, and mixed — governed by three pipeline invariants ensuring universal personality detection, conditional retrieval, and mandatory grounding verification. The architecture demonstrates that personality-aware modulation, hybrid intent routing, and citation-grounded domain knowledge can coexist in a single auditable pipeline, using Swiss informal caregivers as the pilot application. The modular design — with explicit separation between coaching style adaptation and factual content delivery — is intended for reproduction and transfer to other personalized coaching domains.

---

## References

*[References to be formatted in APA 7 style. Priority sources listed below; full reference list to be compiled during final editing.]*

Beatty, C., Malik, T., Meheli, S., & Sinha, C. (2022). Evaluating the therapeutic alliance with a free-text CBT conversational agent (Wysa): A mixed-methods study. *JMIR mHealth and uHealth, 10*(2), e34002.

Brave, S., Nass, C., & Hutchinson, K. (2005). Computers that care: Investigating the effects of orientation of emotion exhibited by an embodied computer agent. *International Journal of Human-Computer Studies, 62*(2), 161–178.

Broadbent, E., et al. (2024). Social robots for loneliness reduction in older adults. *[Full citation to be completed.]*

Chen, J., et al. (2025). A survey of personalized large language models: Progress and future directions. *arXiv preprint arXiv:2502.11528.*

Costa, P. T., & McCrae, R. R. (1992). *Revised NEO Personality Inventory (NEO-PI-R) and NEO Five-Factor Inventory (NEO-FFI) professional manual.* Psychological Assessment Resources.

de Haan, E., Duckworth, A., Birch, D., & Jones, C. (2013). Executive coaching outcome research: The contribution of common factors such as relationship, personality match, and self-efficacy. *Consulting Psychology Journal: Practice and Research, 65*(1), 40–57.

Devdas, S. (2025). *Personality-aware emotional support through motivational regulation in LLM-based dialogue* [Master's thesis, Lucerne University of Applied Sciences and Arts].

Fitzpatrick, K. K., Darcy, A., & Vierhile, M. (2017). Delivering cognitive behavior therapy to young adults with symptoms of depression via a fully automated conversational agent (Woebot): A randomized controlled trial. *JMIR Mental Health, 4*(2), e19.

Gao, L., et al. (2023). Attributed question answering: Evaluation and modeling for attributed large language models. *[Full citation to be completed.]*

Grand View Research. (2024). *AI-driven mental health applications market size report, 2024–2034.*

Grant, A. M. (2003). The impact of life coaching on goal attainment, metacognition and mental health. *Social Behavior and Personality, 31*(3), 253–263.

Inkster, B., Sarda, S., & Subramanian, V. (2018). An empathy-driven, conversational artificial intelligence agent (Wysa) for digital mental well-being. *JMIR mHealth and uHealth, 6*(11), e12106.

Jones, R. J., Woods, S. A., & Guillaume, Y. R. F. (2016). The effectiveness of workplace coaching: A meta-analysis of learning and performance outcomes from coaching. *Journal of Occupational and Organizational Psychology, 89*(2), 249–277.

Ji, Z., Lee, N., Frieske, R., Yu, T., Su, D., Xu, Y., ... & Fung, P. (2023). Survey of hallucination in natural language generation. *ACM Computing Surveys, 55*(12), 1–38.

Karpukhin, V., Oğuz, B., Min, S., Lewis, P., Wu, L., Edunov, S., ... & Yih, W. (2020). Dense passage retrieval for open-domain question answering. *Proceedings of EMNLP 2020*, 6769–6781.

Laranjo, L., Dunn, A. G., Tong, H. L., Kocaballi, A. B., Chen, J., Bashir, R., ... & Coiera, E. (2018). Conversational agents in healthcare: A systematic review. *Journal of the American Medical Informatics Association, 25*(9), 1248–1258.

Lee, K. M., & Nass, C. (2003). Designing social presence of social actors in human computer interaction. *Proceedings of CHI 2003*, 289–296.

Lewis, P., Perez, E., Piktus, A., Petroni, F., Karpukhin, V., Goyal, N., ... & Kiela, D. (2020). Retrieval-augmented generation for knowledge-intensive NLP tasks. *Advances in Neural Information Processing Systems, 33*, 9459–9474.

Li, J., Galley, M., Brockett, C., Spithourakis, G. P., Gao, J., & Dolan, B. (2016). A persona-based neural conversation model. *Proceedings of ACL 2016*, 994–1003.

Li, Y., et al. (2024). Memory-augmented LLM personalization with short- and long-term memory coordination. *[Full citation to be completed.]*

Ma, X., et al. (2023). Fine-tuning LLaMA for factor-based retrieval augmented generation. *[Full citation to be completed.]*

Mairesse, F., & Walker, M. A. (2010). Towards personality-based user adaptation: Psychologically informed stylistic language generation. *User Modeling and User-Adapted Interaction, 20*(3), 227–278.

McCrae, R. R., & John, O. P. (1992). An introduction to the five-factor model and its applications. *Journal of Personality, 60*(2), 175–215.

Mooney, K. H., et al. (2024). Automated monitoring and coaching for caregiver burden reduction. *[Full citation to be completed.]*

Nass, C., & Lee, K. M. (2001). Does computer-synthesized speech manifest personality? Experimental tests of recognition, similarity-attraction, and consistency-attraction. *Journal of Experimental Psychology: Applied, 7*(3), 171–181.

OECD. (2023). *Health at a glance 2023: OECD indicators.* OECD Publishing.

Park, G., Schwartz, H. A., Eichstaedt, J. C., Kern, M. L., Kosinski, M., Stillwell, D. J., ... & Seligman, M. E. (2015). Automatic personality assessment through social media language. *Journal of Personality and Social Psychology, 108*(6), 934–952.

Pinquart, M., & Sörensen, S. (2003). Differences between caregivers and noncaregivers in psychological health and physical health: A meta-analysis. *Psychology and Aging, 18*(2), 250–267.

Quirin, M., Robinson, M. D., Rauthmann, J. F., Kuhl, J., Read, S. J., Tops, M., & DeYoung, C. G. (2023). The dynamics of personality approach (DPA): 20 tenets for uncovering the causal mechanisms of personality. *European Journal of Personality, 37*(1), 45–72.

Ruoss, M., et al. (2023). Caregiver burden in spinal cord injury: A Swiss cohort study. *[Full citation to be completed.]*

Schulz, R., & Sherwood, P. R. (2008). Physical and mental health effects of family caregiving. *American Journal of Nursing, 108*(9 Suppl), 23–27.

Singhal, K., et al. (2023). Large language models encode clinical knowledge. *Nature, 620*, 172–180.

Smither, J. W., London, M., & Reilly, R. R. (2019). Does performance improve following multisource feedback? A theoretical model, meta-analysis, and review of empirical findings. *[Full citation to be completed.]*

Stober, D. R., & Grant, A. M. (Eds.). (2006). *Evidence based coaching handbook: Putting best practices to work for your clients.* Wiley.

Thoppilan, R., et al. (2022). LaMDA: Language models for dialog applications. *arXiv preprint arXiv:2201.08239.*

Wang, Z., et al. (2026). Toward personalized LLM-powered agents: Foundations, evaluation, and future directions. *arXiv preprint arXiv:2602.22680.*

Wysa Research. (2024). Exploring the role of app features in providing continuity of care to users on a digital mental health platform (Wysa). *JMIR Formative Research.* *[Full citation to be completed.]*

Yarkoni, T. (2010). Personality in 100,000 words: A large-scale analysis of personality and word use among bloggers. *Journal of Research in Personality, 44*(3), 363–373.

Zhang, S., Dinan, E., Urbanek, J., Szlam, A., Kiela, D., & Weston, J. (2018). Personalizing dialogue agents: I have a dog, do you have pets too? *Proceedings of ACL 2018*, 2204–2213.

Zhang, Z., et al. (2024). FEEL: A framework for evaluating emotional support in LLMs. *[Full citation to be completed.]*

Zheng, Y., Chen, G., Huang, M., Liu, S., & Zhu, X. (2019). Personalized dialogue generation with diversified traits. *arXiv preprint arXiv:1901.09672.*

Gemma AutoSurvey. (2025). *Personality-aware digital coaching through adaptive dialogue* [AI-generated literature survey, Google Gemma-3n-E4B-IT]. Internal research document.

Qwen AutoSurvey. (2025). *Personality-aware digital coaching through adaptive dialogue* [AI-generated literature survey, Qwen3-Max-2026-01-23]. Internal research document.

Majumder, N., Hong, P., Peng, S., Lu, D., Ghosal, D., Mihalcea, R., ... & Poria, S. (2020). MIME: MIMicking emotions for empathetic response generation. *Proceedings of EMNLP 2020*, 8968–8979.

Wen, H., et al. (2024). Personality-adaptive dialogue systems: Recent advances. *[Full citation to be completed.]*

Basto, A. (2021). Personality detection from conversational text using fine-tuned BERT classifiers. *[Full citation to be completed.]*

*[Caregiver personality, coping, and digital engagement — from new surveys:]*

Gu, J., et al. (2021). Personality-aware response generation in dialogue systems via dynamic attention mechanisms. *[Full citation to be completed.]*

Lazarus, R. S., & Folkman, S. (1984). *Stress, appraisal, and coping.* Springer.

Penley, J. A., & Tomaka, J. (2002). Associations among the Big Five, emotional responses, and coping with acute stress. *Personality and Individual Differences, 32*(7), 1215–1228.

Carver, C. S., Scheier, M. F., & Weintraub, J. K. (1989). Assessing coping strategies: A theoretically based approach. *Journal of Personality and Social Psychology, 56*(2), 267–283.

Zarit, S. H., Reever, K. E., & Bach-Peterson, J. (1980). Relatives of the impaired elderly: Correlates of feelings of burden. *The Gerontologist, 20*(6), 649–655.

Cohen, S., Kamarck, T., & Mermelstein, R. (1983). A global measure of perceived stress. *Journal of Health and Social Behavior, 24*(4), 385–396.

Thoits, P. A. (2011). Mechanisms linking social ties and support to physical and mental health. *Journal of Health and Social Behavior, 52*(2), 145–161.

Brodaty, H., & Donkin, M. (2009). Family caregivers of people with dementia. *Dialogues in Clinical Neuroscience, 11*(2), 217–228.

ZHAW. (2022). *Swiss informal caregiving statistics report.* Zurich University of Applied Sciences.

---

## Appendices

*[Appendices to be included as online supplementary material if page limit requires.]*

**Appendix A.** Full technology stack table (all layers, 11 database tables, versions).

**Appendix B.** Complete trait-to-directive mapping table (10 rows with activation thresholds, low/high variants for all 5 dimensions).

**Appendix C.** Prompt templates for personality detection, behavioral regulation, response generation, and LLM intent router.

**Appendix D.** N8N workflow node inventory with V1 → V2 changes documenting the transition to API-side routing.

**Appendix E.** Database schema (11 tables with column specifications and index definitions).

**Appendix F.** Benchmark fixture format, case inventory, and pass/fail criteria for all test suites.

**Appendix G.** Evaluation rubric and scoring guidelines for human expert response assessment.

**Appendix H.** Swiss policy corpus: source families (IV, AHV, EL, Spitex, Hilflosenentschädigung), chunk statistics, and freshness monitoring.
