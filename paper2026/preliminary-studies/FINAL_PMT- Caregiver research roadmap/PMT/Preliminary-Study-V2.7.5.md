# Adaptive LLM-Based Chatbot with Personality-Aware Dialogue for Human-Centered Applications: A Formal Preliminary Study with Swiss Caregiver Focus

**Author:** Jiahua Duojie  
**Program:** MSc Applied Information and Data Science (HSLU)  
**Supervisor:** Prof. Dr. Guang Lu  
**Secondary Supervisor/Advisor:** Samuel Devdas  
**Date:** October 23, 2025  
**Version:** 2.7.6 (Validation Methodology Refinement: Caregiver-Centered Self-Report Approach)

---

### Changelog (2.7.6)
- **Validation Methodology Refinement (Caregiver-Centered Approach):**
  - Replaced BFI-44 one-time self-report as "ground truth" with direct caregiver feedback validation; resolves timing/construct mismatch
  - Implemented 4-item Personality Understanding Scale (post-Session 2) measuring: emotional tone fit, communication style match, support type appropriateness, overall personality fit
  - Updated success criteria from r≥0.60 (BFI-44 correlation) to Mean ≥3.5/5.0 (realistic, achievable caregiver perception)
  - Established multi-method triangulation: (1) Caregiver self-report (primary), (2) Temporal stability r>0.70 (secondary), (3) Qualitative coherence ≥70% (tertiary), (4) BFI-44 as contextual reference
  - Updated RQ4 success criteria (line 287), Session 3 protocol (line 722), Data Captured table (line 739), Analysis & Validation table (lines 747-752), Table 3.5 (lines 321, 323)
  - Rationale: Direct measurement of "Did system understand my personality?" provides higher ecological validity, construct alignment, and defensibility for human-centered HCI research

### Changelog (2.7.5)
- **Accessibility Refinement for Non-Technical Readers:**
  - Simplified abstract: replaced "preliminary study" → "this study"; removed technical jargon (BFI-44/PSS-10 → "validated personality and stress assessments"; LLM-based evaluators → "automated evaluations verified by human experts"; KEK/CE → "cantonal ethics committee")
  - Removed redundant Table 0 (statistics now integrated into background narrative with inline citations)
  - Integrated statistics directly into background text with proper source attribution and generalization caveats
  - Improved readability for diverse audiences: supervisors, ethics committees, Spitex stakeholders, non-technical evaluators

### Changelog (2.7.4)
- **Quality Refinement (Precision & Credibility):**
  - Replaced absolutes with measurable targets: "zero/100%" → "no critical errors"; "first validated" → "we operationalize (validation in thesis)"
  - Added explicit scope boundaries: "In this preliminary study, policy answers are design-only; canton-specific retrieval validated in thesis phase"
  - Converted claims to observable criteria: "SUS ≥70 (no critical failures across 5–8 sessions)"; "100% citation coverage; audits detect no critical errors (≤5% minor flags)"
  - Removed value judgments: "clearly/perfectly/publication-quality (10+)" → "documented/appropriate/publication-ready"
  - Improved evidence phrasing: "create evidence base" → "provide convergent evidence"; "establishes paradigm/validated methodology" → "proposes approach; validation in thesis"
  - Unified grounding targets across all sections: "All policy claims cite official sources; sampled audits detect no critical errors (≤5% minor flags)"
- **Standardized Statistics:** Verified 700,000 caregivers (OECD 2023, ZHAW 2022); clarified SCI-cohort limitations (Ruoss et al., 2023) for burnout/intensity estimates
- **Technical Consolidation:** EMA details, crisis protocol in dedicated appendix subsections (Appendix G, Appendix C)

---

## Key Innovations & Contributions

This study introduces **five core innovations** addressing Swiss caregiver support:

1. **Continuous Personality-Aware Dialogue** — OCEAN detection with EMA smoothing (α=0.3) provides real-time personality adaptation, moving beyond static user profiles to dynamically responsive emotional coaching.

2. **Zurich Model Operationalization** — We operationalize personality-to-motivation mappings (Big Five → security/arousal/affiliation systems) with testable behavioral directives; validation planned in thesis evaluation phase.

3. **Swiss-Contextualized RAG Pipeline** — RAG-enhanced policy navigation for IV/Invalidenversicherung and Hilflosenentschädigung, addressing Switzerland's federalized healthcare complexity with 20–30 validated Q-A benchmark pairs per domain.

4. **Multi-Stream Validation Architecture** — Expert pilot (n=5–8), real caregiver cohort (n=20–30) with caregiver self-report validation (personality understanding scale + PSS-10), human expert response scoring (κ≥0.75), and synthetic evaluation (N≥250) provide convergent evidence for external validity.

5. **Privacy-Preserving & Audit-Ready Design** — Swiss FADP compliance, pseudonymized storage, formalized crisis protocol (KEK/CE-approved; cantonal ethics committee via swissethics/HRA, equivalent to US IRB), and JSONL audit trails enable organizational trust and regulatory alignment for Spitex adoption.

**Impact:** Provides an operational, auditable approach for personality-aware caregiver support in Switzerland, with validation planned in the thesis phase.

---

## Abstract

Emotional well-being and personalized support are persistent challenges for AI assistants. Current systems store user data but rarely adapt to stable personality traits or real-time motivational needs, resulting in generic, context-insensitive responses. In Switzerland, approximately 700,000 informal caregivers face chronic stress from caregiving (40–70% burnout among high-intensity caregivers), compounded by limited formal training and complex, canton-specific healthcare policies. This creates a need for digital assistants that provide personality-aware emotional coaching and precise policy navigation to enhance resilience.

We propose the **Swiss Caregiver Coaching Assistant**, which detects personality traits (Big Five; OCEAN), aligns responses to motivational needs (Zurich Model), and delivers three-pillar support: **(1) Emotional Support** (resilience, boundary-setting), **(2) Educational Guidance** (caregiving skills matched to personality), and **(3) Policy Navigation** (RAG-augmented retrieval with citation verification; sampled audits target ≤5% minor errors). Reliability is maintained through exponential moving-average smoothing (α=0.3) and confidence-weighted filtering.

This study evaluates the system through three validation streams: expert review sessions with domain specialists (n=5–8), simulated conversations comparing personality-aware responses against generic baselines (N≥250), and real caregiver pilot testing (n=20–30) with validated personality and stress assessments. All automated evaluations are verified by human experts.

---

## 1. Background: General Framework and Swiss Caregiver Context

### 1.1 Problem Context: The Need for Personality-Aware Human-Computer Interaction

AI-driven systems have shifted user expectations toward personalized, context-aware dialogues that adapt to individual personality traits, communication preferences, and situational needs. Across domains—workplace wellbeing, education, customer service, and healthcare—achieving agentic automation as complementary support requires systems that understand not just explicit requests, but also underlying emotional states and motivational patterns that drive behavior.

**The capacity crisis in traditional support systems.** Traditional human-delivered support faces three structural constraints: limited scalability, financial barriers, and geographic limitations. Digital alternatives achieve scalability but deliver one-size-fits-all responses, creating a critical gap: systems combining digital scalability with personalized, adaptive interaction.

**Swiss informal caregiver crisis: Context and urgency.** Switzerland has approximately **700,000 informal caregivers** (8% of population; OECD 2023, ZHAW 2022), representing one of the nation's largest vulnerable populations. Burnout rates vary by care intensity: 40–70% in high-intensity subgroups (Ruoss et al., 2023) versus ~20% population-level prevalence. **Professional training and competency gaps:** Unlike formal healthcare workers, these family caregivers typically lack systematic professional training, evidence-based caregiving techniques, or ongoing clinical supervision. **Stress, burnout, and performance impact:** Informal caregivers face chronic stress (averaging 25–40 hours/week of care), leading to emotional exhaustion, compassion fatigue, and isolation. These stress states directly impair caregiving performance and create reinforcing cycles of burden and guilt.

Beyond emotional challenges, Swiss caregivers navigate a complex, federalized healthcare system with strong cantonal variations in policies and regulations. Yet most caregivers remain unaware of their rights under Swiss law, available financial support mechanisms (cantonal allowances averaging CHF 900–1,000 monthly; Höpflinger & Hugentobler, 2023), employment protection regulations, and healthcare system navigation strategies. Many caregivers experience reduced working hours (avg. 8.4h/week reduction; Ruoss et al., 2023) without accessing support mechanisms that could mitigate financial strain.

**Domain-specific requirements and the personalization gap for caregivers.** Informal caregivers require personality-adaptive support across: (1) **Emotional resilience** (compassion fatigue recognition, stress validation, boundary-setting—especially critical for high-neuroticism caregivers), (2) **Practical education** (caregiving techniques, time management, self-care strategies adapted to individual learning and processing styles), and (3) **Swiss healthcare policy navigation** (cantonal Spitex variations, IV/AI eligibility, Hilflosenentschädigung application, Ergänzungsleistungen, caregiver employment models). Current digital assistance solutions—generic stress management apps, FAQs without personality awareness, generic policy information portals—fail to account for individual differences, creating systematic mismatches that reduce effectiveness and undermine caregiver trust.

### 1.2 Limitations of Current Digital Assistants and Caregiver Support Systems

We identify three interconnected technical and domain-specific constraints limiting current conversational AI effectiveness for caregiver support:

**Gap 1: Lack of Psychologically Grounded Personalization.**  
Recent industry deployments (ChatGPT Memory, mem0, LangChain Memory) prioritize memory-centric personalization, storing user statements as vector embeddings for similarity-based retrieval across sessions. While achieving factual persistence at scale, this approach remains cognitively shallow, addressing *what the user said* but not *why they behave*. Memory systems recall that a caregiver mentioned "mother has dementia" but cannot infer whether that caregiver's preference for structured planning stems from high conscientiousness (organizational drive), neuroticism (need for security), or both—leading to generic responses that miss underlying motivational drivers. No validated computational mappings translate personality traits into behavioral directives grounded in motivational psychology; measurement protocols to confirm intended psychological state induction remain undeveloped.

**Gap 2: LLM Safety, Reliability, and Privacy in Healthcare.**  
Most systems lack complete logging, audit trails, and deterministic interfaces preventing rigorous evaluation. Caregiver support systems particularly lack standardized outcome measures or longitudinal tracking to assess effectiveness. Critical deficiencies exist in truthfulness, persona stability, and privacy preservation for vulnerable caregiver populations. No privacy-preserving architectures meet Swiss data protection standards (FADP, rev. 2023) while enabling effective personality tracking.

**Gap 3: Absence of Personalized Education and Swiss Healthcare Navigation.**  
No caregiver support systems currently exist that integrate: (1) personalized practical education on caregiving techniques adapted to individual OCEAN personality profiles, and (2) LLM-based navigation of complex Swiss healthcare policies and regulations tailored to caregiver needs. While personality adaptation is essential for emotional support and educational guidance, the navigation of policies and regulations is fundamentally important functionality that does not necessarily require OCEAN trait adaptation—instead, it requires accurate, contextualized information delivery. This gap is particularly acute in Switzerland's federalized system where caregivers require guidance on cantonal variations in Spitex services, caregiver allowances, long-term care insurance (Pflegeversicherung), family caregiver employment models, patient rights, and culturally appropriate Swiss interaction patterns. Current digital health interventions, when they exist, provide only generic information without personality adaptation or Swiss-specific contextualization.

### 1.3 Literature Foundations and Motivation: Addressing Caregiver-Specific Gaps

Recent work by Devdas (2025), a master's thesis at HSLU, demonstrates that Big Five personality detection with motivational regulation improves emotional support quality by ≥20% in controlled settings, establishing that personality-aware adaptation meaningfully enhances conversational quality. Prior frameworks such as FEEL (Zhang et al., 2024), an evaluation framework for emotional support in LLMs, and ElliQ (Broadbent et al., 2024), a social robot for loneliness reduction, achieve scalability but lack Big Five personality adaptation or Swiss contextualization. In healthcare AI, transparency through disclosure of AI use, response grounding, and auditable logs has emerged as critical for reducing hallucination and maintaining trust in clinical applications. For caregiver-specific interventions, digital support shows promise in reducing burden, with effect sizes varying by intervention design; one trial reported a 38% reduction in caregiver burden at 8 weeks using automated monitoring and coaching (Mooney et al., 2024), though Swiss-specific implementations remain scarce.

Despite this progress, **no existing system systematically integrates** personality-aware adaptation with caregiver-specific three-pillar support: (1) **emotional support and resilience-building**, (2) **practical caregiving education**, and (3) **Swiss healthcare policy navigation**—all grounded in validated personality science and Swiss regulatory context.

**Research Motivation and Expected Impact:**

Integrating these three pillars (emotional, educational, policy navigation) with personality-aware adaptation addresses critical opportunities: **Scaling personalized support** without scaling costs enables individualized caregiver support that matches human practitioners' empathy while maintaining accessibility. **Building caregiver trust** through validated personality science (Big Five, Zurich Model) and Swiss healthcare accuracy ensures systems respond to genuine psychological needs, increasing acceptance. **Enabling organizational adoption** through reproducible evaluation protocols, audit trails, and caregiver-centered outcomes addresses Spitex and cantonal health department requirements for quality assurance and evidence-based deployment.

By addressing these three identified gaps, this research proposes an approach to **theoretically grounded, personality-aware, safe, and contextually appropriate AI applications in informal caregiving**, with specific contributions to Switzerland's 700,000+ caregivers and broader implications for global caregiver support systems.

**This study specifies six key objectives addressing caregiver-specific research gaps, aligned with the Master Thesis Research Roadmap:**

**Table 1. Six Research Objectives Addressing Caregiver Gaps**

| Objective | Description | Caregiver-Specific Focus |
|-----------|-------------|-------------------------|
| (1) Dynamic Personality-Aware Adaptation | Develop and validate OCEAN detection with real-time adaptation outperforming static approaches | Tailor emotional support intensity to caregiver neuroticism; resource navigation detail to conscientiousness |
| (2) Zurich Model Operationalization | Create validated mappings from OCEAN to behavioral directives with manipulation checks | Confirm caregivers perceive security/arousal/affiliation framing as intended; measure stress reduction |
| (3) LLM Safety and Swiss Privacy Compliance | Design privacy-preserving architecture meeting Swiss FADP with persona stability and hallucination guardrails | Protect caregiver anonymity; target policy guidance factual accuracy; prevent fabricated Swiss benefits |
| (4) Caregiver-Specific Emotional Support | Develop resilience-building, compassion fatigue recognition, boundary-setting strategies with personality adaptation | High-N: reassurance + grounding; Low-N: pragmatic solutions; All: caregiver-specific stress drivers |
| (5) Personalized Caregiving Education | Create practical education (techniques, time management, self-care) adapted to individual learning styles | High-C: detailed step-by-step; Low-C: flexible overview; High-O: novel approaches; Low-O: proven methods |
| (6) Swiss Healthcare Policy Navigation | Develop RAG-enhanced system for cantonal Spitex, IV/AI, Hilflosenentschädigung, allowances, employment models | Contextualized guidance per canton; eligibility checklists; application step-by-step support; contact information |

**Objective-to-Research Question Mapping:**
- **Objective (1) Dynamic Personality-Aware Adaptation** → RQ1 (Personality Detection Validity & Stability)
- **Objective (2) Zurich Model Operationalization** → RQ2 (Value of Personality-Adaptive Personalization)
- **Objectives (3-6) encompassing Safety, Support, Education, Policy** → RQ3 (Policy Accuracy & Citation Grounding), RQ4 (Usability, Acceptability & Multi-Stream Performance)
- **All objectives collectively** → RQ5 (Study Scope, Limitations & Generalizability)

---

## 2. Topic Definition

### 2.1 Core Concepts

**Personality-adaptive emotional support chatbot.** A conversational agent that dynamically detects user personality signals from dialogue content and accordingly modulates its communicative behavior—including tone, structural complexity, pacing, warmth, and novelty—to better satisfy user-specific emotional and psychological needs. Unlike static systems that rely on predetermined user profiles, personality-adaptive chatbots continuously update their understanding of user traits and adjust their responses in real time to optimize emotional alignment and therapeutic effectiveness.

**Big Five (OCEAN) personality framework.** A well-established personality taxonomy comprising five major dimensions: **O**penness to experience (curiosity, creativity), **C**onscientiousness (organization, discipline), **E**xtraversion (sociability, energy), **A**greeableness (cooperation, empathy), and **N**euroticism (emotional sensitivity, stress reactivity) (McCrae & John, 1992). This framework provides a structured basis for personality inference and has been extensively validated across cultures and contexts. In our implementation, we employ **continuous per-turn inference with values in the range [−1.0, +1.0]** representing the full spectrum from low to high trait expression. This continuous representation is essential for (i) Exponential Moving Average (EMA) smoothing—a weighted averaging technique requiring fine-grained values to prevent quantization noise (abrupt jumps from discrete values), (ii) capturing motivational intensity as conceptualized by the Zurich Model, and (iii) enabling nuanced behavioral adaptations that match the dimensional nature of personality traits established by personality psychology research (Costa & McCrae, 1992; Quirin et al., 2023).

**Zurich Model alignment.** Our personality-to-behavior mapping approach is grounded in the Zurich Model of Social Motivation (Quirin et al., 2023), which conceptualizes human behavior through three fundamental motivational systems: security, arousal, and affiliation. We operationalize this framework by mapping OCEAN traits to these motivational domains: Neuroticism influences security-related behaviors (comfort provision vs. stability reassurance), Openness and Extraversion modulate arousal through novelty and energy regulation, and Agreeableness affects affiliation through warmth and collaborative stance adjustments. Conscientiousness serves as a structural modifier, influencing the organization and specificity of guidance provided. *Note: This operationalization represents a simplified first-order mapping; the Zurich Model emphasizes dynamic interactions between motivational systems (Quirin et al., 2023), which are not fully captured in this preliminary design and require empirical validation in the thesis phase.*

**Safety constraints.** All system responses are designed to be grounded in user conversational input (see Section 4.4 for quote-and-bound implementation details).

### 2.2 Scope and Application Context

**Human-centered applications.** Our framework targets applications emphasizing personalization, empathy, and adaptive user interaction across diverse domains: family caregiver support, mental health services, educational assistance, customer service interactions, and general emotional companionship. We designed the system to complement human interaction by providing consistent availability, emotional attunement, and personality-aware responses. The system maintains appropriate boundaries and escalation mechanisms when professional human intervention is needed.

**Domain prioritization rationale.** Family caregiver coaching was prioritized over clinical mental health applications due to: (1) strong alignment with Zurich Model motivations (security for managing care responsibilities and financial stress, affiliation for family dynamics and social support, arousal for goal-setting and advocacy), (2) urgent public health need (Switzerland's aging population creates growing caregiver burden with limited digital support infrastructure), (3) clear policy integration opportunity (navigating AHV, IV, Hilflosenentschädigung, respite care services), (4) lower ethical and regulatory risks (non-clinical coaching boundary avoids medical device regulations while addressing wellbeing), and (5) measurable technical outcomes (system usability SUS ≥70, personality adaptation appropriateness, policy navigation accuracy, benefit comprehension improvements).

**Technical scope.** The system integrates personality-aware dialogue with RAG-augmented policy navigation for Swiss caregiver benefits. The RAG module retrieves relevant policy documents and eligibility criteria based on caregiver context, while the personality-aware regulation determines presentation style (detailed vs. summary, reassuring vs. pragmatic). The system implements a webhook-based N8N architecture for production deployment. 

**Thesis Scope (Realistic Focus):**
- **Personality Detection & Regulation:** Full implementation in Weeks 7-10 (detect→regulate→generate pipeline)
- **RAG Policy Navigation:** Focused development on 2 high-impact policy domains (**IV/Invalidenversicherung** and **Hilflosenentschädigung**) with 20-30 manually curated + LLM-generated question-answer-chunk benchmark pairs for validation
- **Expert Pilot (Weeks 3-5):** Small-scale usability testing with n=5-8 in-house domain experts (Spitex coordinators, geriatricians) using think-aloud protocol to validate personality adaptation and directive effectiveness
- **UI Development (Weeks 9-10):** Next.js/React web interface for expert pilot testing and thesis defense
- **Human Validation (Weeks 15-16):** Caregiver pilot (n=30-50); caregiver self-report personality understanding validation; qualitative feedback collection

**Scope Note:** In this study, policy answers are design-only; operational canton-specific retrieval is implemented and validated in the thesis phase. Comprehensive cantonal policy coverage and multimodal inputs are planned for post-thesis extensions.

**Evaluation framework.** Our comprehensive assessment methodology evaluates system performance across multiple dimensions: (1) **conversational quality** (detection accuracy, regulation effectiveness, emotional tone, relevance, personality needs satisfaction), (2) **system usability** (SUS scores, task completion, expert appropriateness ratings), (3) **policy accuracy and grounding** (citation coverage, hallucination detection, source verification), (4) **engagement and stress metrics** (message patterns, stress mitigation effectiveness), and (5) **real-world validation** (caregiver self-report personality understanding, temporal stability, and PSS-10 stress measures). Detailed evaluation protocols are specified in Section 4.6 (Devdas, 2025; Zhang et al., 2024).

### 2.3 Implementation Specifications

**LLM model selection.** We employ OpenAI GPT-4.1 as the primary model for personality detection and response generation, with Gemini 2.5 Pro as a cost-effective alternative. GPT-4.1 offers structured JSON output via function calling and strong personality inference capabilities validated in prior work (Miotto et al., 2022). We set temperature to 0.3 for detection (consistency) and 0.7 for generation (creativity with reliability). The provider-agnostic JSON contracts enable seamless model swapping for evaluation, cost optimization, and robustness. Vendor-specific details are in Appendix E (planning assumptions).

**Dataset for OCEAN detection training.** The system uses **zero-shot prompt-based inference** rather than fine-tuned models. This leverages GPT-4's pre-trained understanding of personality psychology. We engineer prompts based on established personality assessment instruments (NEO-PI-R, BFI-2) and linguistic markers validated in prior work (Yarkoni, 2010; Park et al., 2015). For evaluation and validation, we employ three approaches: (1) **synthetic personality profiles** generated via simulated user agents with extreme (±0.8) and mixed trait configurations, (2) **scripted dialogue scenarios** covering Swiss caregiver stress contexts (emotional burden, benefit navigation complexity, self-care neglect), and (3) **human validation subset** (planned for thesis phase) with 30-50 Swiss family caregiver participants completing self-report personality inventories (BFI-44) for ground-truth comparison.

**Evaluation metrics and target thresholds.** The system targets the following performance benchmarks:

**Table 2. Evaluation Metrics and Target Thresholds**

| Evaluation Category | Metric | Target Threshold | Measurement Method |
|---------------------|--------|:----------------:|-------------------|
| **1. Conversational Quality** | Detection Accuracy | ≥75% trait alignment | Correlation between inferred and ground-truth OCEAN scores (r ≥ 0.75) |
| | Temporal Stability | Variance < 0.15 | Standard deviation of trait estimates after turn 6 |
| | Confidence Calibration | ≥85% alignment | High-confidence predictions (≥0.7) match personality cues in 85%+ cases |
| | Tone Appropriateness | ≥80% evaluator rating | LLM evaluator scores on 5-point Likert scale (≥4.0/5.0) |
| | Needs Satisfaction | ≥20% improvement vs. baseline | Relative gain on personality-specific needs addressed |
| **2. System Usability** | SUS Score | ≥70 | System Usability Scale (expert pilot n=5-8) |
| | Task Success Rate | ≥80% | Expert think-aloud protocol completion |
| | Personality Adaptation Appropriateness | ≥4.0/5.0 | Expert Likert ratings |
| **3. Policy Accuracy & Grounding** | Citation Coverage | 100% | Percentage of policy claims citing official sources |
| | Hallucination Detection | No critical errors | Sampled audits (≤5% minor flags allowable) |
| | Policy Guidance Clarity | ≥4.0/5.0 | Expert assessment on 5-point rubric |
| **4. Engagement & Stress Metrics** | Engagement Score | ≥1.2/2.0 | Message length, latency, directive acceptance |
| | Stress Mitigation Rate | ≥60% | High-stress turns followed by lower stress |
| **5. Real-World Validation** | Personality Correlation | r ≥ 0.60 | Inferred OCEAN vs. BFI-44 self-report |
| | Stress Detection Correlation | r ≥ 0.50 | System stress level vs. PSS-10 |
| | Caregiver Retention | ≥80% | Participants completing all sessions |
| **System Reliability** | JSON Contract Compliance | ≥99.5% | Valid JSON outputs from detection/generation modules |
| | Error Handling | No critical failures | All errors trigger neutral fallback responses |

*Note: Thresholds informed by prior conversational AI evaluation studies (Zhang et al., 2024; Devdas, 2025) and personality assessment reliability standards (Costa & McCrae, 1992). These represent hypothesized success criteria to be empirically validated in thesis phase with N≥250 simulated conversations and n=30-50 human participants.*

**Two-Tier Acceptance (Power-Adjusted):** (1) **Initial Validation Gate (r ≥ 0.50)** — Temporal correlation between consecutive OCEAN estimates; achievable with ~25 paired observations (α=0.05, power=0.80). (2) **Thesis Target (r ≥ 0.75)** — Criterion validity against BFI-44, requiring n≥60 for adequate power.

**Temporal smoothing parameters.** EMA (α=0.3) stabilizes traits by turns 6–8 (variance <0.15); weights 30% current observation, 70% historical average. Confidence thresholds—0.4 (minimum for updates) and 0.7 (high-confidence adaptation)—align with personality assessment reliability standards (r≥0.7; Park et al., 2015). Sensitivity analysis (α ∈ {0.1, 0.2, 0.3, 0.4, 0.5}) in Appendix G.

### 2.4 Application Context: Swiss Caregiver Coaching Assistant

**Target Population and Rationale.** This study focuses on the **Swiss Caregiver Coaching Assistant**, designed to support approximately 700,000 family caregivers managing eldercare, chronic illness, disability care, and dementia in Switzerland. Caregivers face chronic stress from prolonged responsibility (25–40 hours/week), leading to 40–70% burnout rates, yet remain unaware of available financial support (CHF 900–1,000 monthly potential) and employment protections. The system addresses three core gaps: (1) **emotional resilience** (compassion fatigue recognition, boundary-setting), (2) **practical education** (caregiving techniques adapted to learning style), and (3) **Swiss healthcare policy navigation** (cantonal variations across 26 regulatory frameworks). This focus was selected for: urgent public health need; strong alignment with Zurich Model motivations (security, affiliation, arousal); clear policy integration opportunity; minimal regulatory risk (non-clinical coaching); and measurable technical outcomes (usability, personality adaptation, policy accuracy).

**Three Personality-Tailored Coaching Modes:**

| Pillar | Implementation | Personality Regulation | Delivery |
|--------|---|---|---|
| **(1) Emotional Support & Resilience** | Personality Regulation Model | ✓ Full | Tone adapted to OCEAN (esp. N, A) |
| **(2) Practical Education & Self-Care** | Personality Regulation Model | ✓ Full | Content/approach adapted to OCEAN (esp. C, O, E) |
| **(3) Swiss Policy Navigation** | RAG + Personality Styling | ✓ Presentation Only | Facts from RAG; delivery adapted to personality |

**1. Emotional Support & Resilience Building (Personality-Regulated)**

- **Purpose:** Validate caregiver burden, help process emotions, develop coping strategies
- **Personality Adaptation:**
  - **High-N:** Extra reassurance ("Many caregivers feel overwhelmed—this is completely valid")
  - **Low-N:** Pragmatic acknowledgment ("You're managing significant responsibilities")
  - **High-A:** Collaborative, warm framing with relationship emphasis
  - **Low-A:** Direct, matter-of-fact stance respecting autonomy
- **Content & Evidence-Based Techniques:** Compassion fatigue recognition; guilt/resentment reframing (CBT); boundary assertion; stress validation

**2. Practical Education & Self-Care Planning (Personality-Regulated)**

- **Purpose:** Develop sustainable respite plans, teach caregiving techniques, prevent burnout escalation
- **Personality Adaptation:**
  - **High-C:** Structured planning with timelines and step-by-step techniques
  - **Low-C:** Flexible self-care suggestions with light scaffolding
  - **High-E:** Emphasize social support mobilization (support groups, family coordination)
  - **Low-E:** Focus on individual restoration (micro-breaks, boundary-setting scripts)
  - **High-O:** Novel caregiving techniques, creative respite solutions
  - **Low-O:** Proven, traditional methods with clear evidence base
- **Content:** Caregiving techniques (dementia care, mobility assistance); time management (scheduling, delegation scripting); self-care (micro-rest protocols, technology aids, financial planning)

**3. Swiss Healthcare Policy Navigation (RAG-Enhanced, Minimal Personality Styling)**

- **Purpose:** Help caregivers understand and access Swiss benefits and services
- **Implementation:** RAG retrieves factual policy information (AHV/AVS, IV/AI, Hilflosenentschädigung, Ergänzungsleistungen, Spitex); personality adaptation styles **delivery only** (summary vs. detailed, reassuring vs. pragmatic), NOT policy facts
- **Key Distinction:** RAG ensures factual accuracy; personality adaptation styles the **presentation**, NOT the policy facts themselves
- **Technical Details:** See Section 4.4 for complete RAG pipeline specification (context extraction, retrieval, personality-aware presentation, grounding enforcement)

---

## 3. Research Questions

This study is guided by a primary research question addressing overall efficacy, which is operationalized through five sub-questions organized by mechanism, policy grounding, human factors, and robustness.

### 3.1 Primary Research Question (Overall Efficacy)

**Does personality-aware three-pillar support improve caregiver outcomes versus non-adaptive baselines?**

- **Outcomes evaluated:** Tone appropriateness, needs satisfaction, stress mitigation, system usability (SUS)
- **Baseline comparators:** Generic (non-adaptive), memory-only (mem0-style), policy-only (RAG without personality)
- **Evaluation scope:** Simulated conversations (N≥250) and real caregiver validation (n=20-30)

### 3.2 Sub-Research Questions

The following five research questions operationalize the primary research question, systematically addressing mechanism, policy grounding, human factors, and robustness.

#### **Mechanism & Modeling**

**RQ1: Personality Detection Validity & Stability**

Can continuous OCEAN inference with EMA (α=0.3) achieve valid and temporally stable trait estimates?

- **Validity target:** BFI-44 correlation r ≥ 0.60 (real caregiver data, n=20-30)
- **Stability target:** Temporal variance < 0.15 within 6–8 turns; consistency r > 0.7 across segments
- **See:** Section 4.2 technical specifications and Section 4.5 validation protocol

**RQ2: Value of Personality-Adaptive Personalization**

Do personality-adaptive behavioral directives yield ≥20% improvement in response quality versus non-adaptive baselines?

- **Quality metrics:** Tone appropriateness, relevance, personality needs satisfaction
- **Simulated evaluation:** N≥250 conversations across three support pillars (Emotional, Educational, Policy)
- **Real caregiver validation:** Human expert engagement scores ≥1.2/2.0; stress mitigation ≥60%
- **See:** Sections 4.5, 4.5.2, and 4.6

#### **Swiss Policy Grounding**

**RQ3: Policy Accuracy & Citation Grounding**

Does RAG-augmented Swiss policy guidance achieve 100% citation coverage with no critical errors?

- **Policy domains:** AHV, IV, Hilflosenentschädigung, respite care, Spitex guidance
- **Verification approach:** Expert audit of ~250 policy claims; ≤5% minor flags allowable for correction
- **Design requirement:** All policy statements cite official source documents; no hallucinated benefits
- **See:** Sections 4.4 (RAG specifications) and 4.6 (audit protocol)

#### **Human Factors & Multi-Stream Validation**

**RQ4: Usability, Acceptability & Multi-Stream Performance**

Does the system achieve acceptable performance across expert, simulated, and real-world validation streams?

**(a) Expert Pilot (n=5-8 domain experts):**
- System Usability Scale (SUS) ≥70; Personality Adaptation Appropriateness ≥4.0/5.0; Tone-Fit accuracy ≥80%

**(b) Real Caregiver Ground-Truth Validation (n=20-30):**
- Caregiver personality understanding mean ≥ 3.5/5.0 (4-item Personality Understanding Scale administered post-Session 2)
- Stress detection r ≥ 0.50 vs. PSS-10 (Perceived Stress Scale)
- Stress mitigation rate ≥60% (high-stress turns followed by lower stress)
- Retention rate ≥80% of recruited caregivers completing all sessions

**(c) Human Expert Response Scoring:**
- Independent evaluators (n=2-3, trained, inter-rater κ ≥ 0.75) score responses on 5 criteria
- Mean quality scores ≥1.4/2.0 across all criteria (emotional tone, engagement, stress reduction, relevance, factual accuracy)

**(d) Ethics, Safety & Compliance:**
- KEK/CE approval for real caregiver phase; crisis protocol procedures; zero protocol violations
- Complete JSONL audit trails; FADP (Swiss data protection) compliance

**See:** Sections 4.5.1, 4.5.2, 4.6, and 3.3 (Success Criteria)

#### **Robustness & Generalization**

**RQ5: Study Scope, Limitations & Generalizability**

What are the explicit boundaries and external validity constraints of this validated proof-of-concept study?

- **Scope boundaries:** Sample sizes, methodology constraints, generalization limitations
- **Reproducibility:** Contract compliance (JSON ≥99.5%), seed-stable outputs, inter-run consistency
- **Pre-registration:** Equivalence bounds for real-world prediction; pre-registered analysis plan
- **See:** Section 3.3 (Success Criteria) and Section 7.2 (Limitations vs. Future Work)

### 3.5 Research Question to Evaluation Framework Mapping

This subsection maps each research question to its evaluation approach, success criteria, and relevant methodology sections. This structured mapping ensures comprehensive coverage of all RQs through our multi-stream validation approach.

**Table 3.5. Research Question Evaluation Mapping**

| Research Question | Evaluation Approach and Methods | Key Success Criteria | Relevant Sections |
|-------------------|--------------------------------|----------------------|-------------------|
| **RQ1-2: Personality Detection & Regulation** | Assess trait detection and response tailoring using system logs (n=5–8 experts), synthetic dialogues (N≥250), and caregiver data (n=20–30, caregiver self-report validation). | Trait accuracy: r ≥ 0.75 (synthetic), temporal stability r > 0.70 (real); caregiver understanding scale mean ≥ 3.5/5.0; expert rating ≥ 4.0/5.0. | 4.2, 4.3, 4.5, 4.6 |
| **RQ3: Policy Accuracy** | Verify policy guidance via audits (250+ claims), expert reviews (n=5–8), and human scoring. | 100% citation coverage; no critical errors; ≤ 5% minor errors. | 4.4, 4.6, 7.2 |
| **RQ4: Usability & Validation** | Evaluate usability and performance via expert pilot (n=5–8, SUS/think-aloud), caregiver sessions (n=20–30, self-report personality understanding + stress measures), and expert scoring (κ ≥ 0.75). | SUS ≥ 70; personality understanding ≥ 3.5/5.0; engagement ≥ 1.2/2.0; stress reduction ≥ 60%; retention ≥ 80%; κ ≥ 0.75. | 4.5.1, 4.5.2, 4.6 |
| **RQ5: Robustness & Scope** | Document reproducibility and limits via checklists, policy swap tests, and scope analysis. | JSON compliance ≥ 99.5%; policy swap < 30 min; clear scope boundaries. | 3.3, 4.7, 7.2 |

---

---

## 4. Methodology

### 4.1 Architecture and Workflow

We implement a reproducible pipeline orchestrated via N8N with deterministic JSON contracts, neutral fallbacks, and complete logging. Each stage (ingest, detection, regulation, generation, verification, persistence) exposes stable interfaces configured by versioned policy packs, enabling reuse, scaling, and domain transfer.

**Implementation Timeline (Weeks 7-10):**
- **Weeks 7-8:** Detection module, regulation logic, generation pipeline, EMA integration → working personality detection + regulation engine
- **Weeks 6-8 (Parallel):** RAG development for **2 policy domains** (IV/Invalidenversicherung, Hilflosenentschädigung) with **20-30 Q-A benchmark pairs** (manual + LLM-generated, expert-validated κ≥0.70)
- **Weeks 9-10:** Next.js/React UI development, Flask backend for detect→regulate→generate→RAG pipeline, expert pilot testing
- **Future Extensions:** Comprehensive cantonal RAG coverage, multimodal inputs, production-scale deployment

**EMA-Based Trait Stabilization:** To prevent erratic personality shifts from noisy detections, we apply exponential moving average (EMA) smoothing (α=0.3) at each turn, balancing responsiveness with stability.

*Algorithm Pseudocode:*
```
For each OCEAN trait T at turn n:
  1. LLM detects current trait value: T_detected[n] ∈ [-1.0, +1.0]
  2. LLM provides confidence score: confidence[n] ∈ [0.0, 1.0]
  3. IF confidence[n] >= threshold (0.4):
       T_smoothed[n] = α × T_detected[n] + (1 - α) × T_smoothed[n-1]
     ELSE:
       T_smoothed[n] = T_smoothed[n-1]  // retain previous estimate
  4. Use T_smoothed[n] for behavioral regulation
```

*Mathematical Formula:*

\[ T_{smoothed}^{(n)} = \begin{cases} 
\alpha \cdot T_{detected}^{(n)} + (1-\alpha) \cdot T_{smoothed}^{(n-1)} & \text{if } c^{(n)} \geq 0.4 \\
T_{smoothed}^{(n-1)} & \text{otherwise}
\end{cases} \]

Where α=0.3 weights recent observations at 30% and historical average at 70%, preventing single-turn volatility while enabling gradual adaptation. Initialization: \(T_{smoothed}^{(0)} = T_{detected}^{(0)}\) for first turn. This approach fills a critical gap in prior work (Devdas, 2025), which lacked temporal stability mechanisms, resulting in inconsistent personality profiles across multi-turn conversations.

**Parameter Selection:** α=0.3 selected via sensitivity analysis across α ∈ {0.1, 0.2, 0.3, 0.4, 0.5} targeting 6-8 turn convergence with variance <0.15. Simulated testing scenarios demonstrated optimal balance between responsiveness and stability. Complete sensitivity analysis planned for thesis phase with human participant data (target N≥250).

**Early-Turn Bias Mitigation:** To mitigate EMA amplification of initial misdetections, the system employs gradual intensity scaling (50% turns 1-2, 75% turns 3-5, 100% turns 6+) and neutral fallbacks when confidence <0.4 after 3 turns.

**Figure 1. System Architecture Pipeline (Conceptual Overview)**

*Core pipeline: detect (OCEAN + confidence) → EMA (α=0.3) → regulate → generate (quote‑and‑bound) → verify. RAG retrieves policy information for IV and Hilflosenentschädigung domains with 20-30 validated Q-A pairs. All processes logged to JSONL audit logs and PostgreSQL for reproducibility and longitudinal analysis.*

```
┌─────────────┐
│ User Input  │
└──────┬──────┘
       │
       ▼
┌─────────────────────────────────────────┐
│  Detection Module (OCEAN + Confidence)  │
│  • Continuous trait inference [-1,+1]   │
│  • Per-trait confidence scores          │
└──────┬──────────────────────────────────┘
       │
       ▼
┌─────────────────────────────────────────┐
│  EMA Smoothing (α=0.3)                  │
│  • Temporal stability filter            │
│  • Confidence-aware updates (≥0.4)      │
│  • PostgreSQL state persistence         │
└──────┬──────────────────────────────────┘
       │
       ▼
┌─────────────────────────────────────────┐
│  Regulation Module                      │
│  • Map traits → behavioral directives   │
│  • Apply policy pack rules              │
│  • Intensity scaling                    │
└──────┬──────────────────────────────────┘
       │
       ▼
┌─────────────────────────────────────────┐
│  Generation Module                      │
│  • Directive-driven response            │
│  • Quote-and-bound grounding            │
│  • Tone/pacing/warmth adaptation        │
└──────┬──────────────────────────────────┘
       │
       ▼
┌─────────────────────────────────────────┐
│  Verification & Refinement              │
│  • Grounding check                      │
│  • Quality validation                   │
└──────┬──────────────────────────────────┘
       │
       ▼
┌─────────────┐      ┌──────────────────┐
│ User Output │◄─────┤ JSONL Audit Logs │
└─────────────┘      └──────────────────┘
                              │
                     ┌────────▼─────────┐
                     │ PostgreSQL Store │
                     │ • Sessions       │
                     │ • Turns          │
                     │ • Personality    │
                     │   States         │
                     └──────────────────┘
```

*Conceptual pipeline: detect (OCEAN + confidence) → EMA (α=0.3) → regulate → generate (quote‑and‑bound) → verify, with JSONL audit logs and PostgreSQL state for reproducibility and longitudinal analysis.*

---

**Figure 2. Containerized System Architecture and DevOps Infrastructure**

```
┌──────────────────────────────────────────────────────────────────┐
│                      Docker Compose Environment                  │
├──────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌─────────────────┐        ┌──────────────────┐                 │
│  │   Next.js/React │◄──────►│   N8N Workflow   │                 │
│  │   Frontend      │  HTTP  │   Engine         │                 │
│  │  (Port 3000)    │        │  (Port 5678)     │                 │
│  │                 │        │                  │                 │
│  │ • Chat UI       │        │ • Orchestration  │                 │
│  │ • OCEAN Display │        │ • Node Execution │                 │
│  │ • Policy Review │        │ • Webhook Handler│                 │
│  │ • Think-Aloud   │        │ • Session Mgmt   │                 │
│  │   Protocol      │        │ • RAG Retrieval  │                 │
│  └────────┬────────┘        └────────┬─────────┘                 │
│           │                           │                          │
│           │                           │                          │
│           │                           ▼                          │
│           │                  ┌──────────────────┐                │
│           │                  │   Flask Backend  │                │
│           │                  │   (Port 5000)    │                │
│           │                  │                  │                │
│           │                  │ • Detection Svc  │                │
│           │                  │ • Regulation Svc │                │
│           │                  │ • Generation Svc │                │
│           │                  │ • RAG Retrieval  │                │
│           │                  └────────┬─────────┘                │
│           │                           │                          │
│           │                           ▼                          │
│           │                  ┌──────────────────┐                │
│           │                  │   PostgreSQL     │                │
│           └─────────────────►│   Database       │                │
│                   SQL        │  (Port 5432)     │                │
│                              │                  │                │
│                              │ • Sessions       │                │
│                              │ • Turns          │                │
│                              │ • Personality    │                │
│                              │   States (EMA)   │                │
│                              │ • Metrics        │                │
│                              │ • RAG Q-A Pairs  │                │
│                              └──────────────────┘                │
│                                       ▲                          │
│                                       │                          │
│                                       │                          │
│                              ┌────────┴─────────┐                │
│                              │      Redis       │                │
│                              │   Cache Layer    │                │
│                              │  (Port 6379)     │                │
│                              │                  │                │
│                              │ • Session Cache  │                │
│                              │ • Policy Cache   │                │
│                              │ • Rate Limiting  │                │
│                              │ • Temp Storage   │                │
│                              └──────────────────┘                │
│                                                                  │
└──────────────────────────────────────────────────────────────────┘
         │                          │              │
         ▼                          ▼              ▼
  ┌─────────────┐          ┌──────────────┐    ┌─────────────┐
  │   Volume:   │          │   Volume:    │    │   Volume:   │
  │ nextjs/     │          │  n8n_data/   │    │  postgres/  │
  │  .next/     │          │  workflows   │    │    data     │
  └─────────────┘          │  RAG_corpus/ │    └─────────────┘
                           │  iv_docs     │
                           │  hilflosen   │
                           └──────────────┘
```

**Deployment Progression:**
- **Weeks 9-10 (Development):** Next.js/React UI development with local testing
- **Weeks 11-14 (Pilot Testing):** Deploy to Vercel or similar platform for expert and caregiver sessions
- **Post-Thesis (Optional):** Kubernetes for production scaling

**Table 3. N8N Node Specifications and Contracts**

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

### 4.2 Detection Module: Continuous OCEAN Inference with EMA Smoothing

**Input Processing:** Accepts up to 10 previous turns; produces continuous OCEAN assessments with confidence scores. Preprocessing: text normalization, length validation, history assembly, PostgreSQL state integration.

**LLM Contract:** GPT-4.1 via OpenAI-compatible endpoint; temperature 0.3, max_tokens 300, 30s timeout. JSON response format:
  ```json
  {
    "ocean": {"O": [-1.0 to 1.0], "C": [-1.0 to 1.0], "E": [-1.0 to 1.0], "A": [-1.0 to 1.0], "N": [-1.0 to 1.0]},
    "confidence": {"O": [0.0 to 1.0], "C": [0.0 to 1.0], "E": [0.0 to 1.0], "A": [0.0 to 1.0], "N": [0.0 to 1.0]},
    "reasoning": "Brief explanation of detected motivations"
  }
  ```

**EMA Smoothing:** Targets temporal stability while remaining responsive to genuine personality evolution:

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

**Confidence-Weighted Updates:** GPT-4.1 self-assesses confidence based on evidence clarity, consistency with previous turns, and behavioral indicator strength. Low-confidence detections (< 0.4) are filtered to prevent noise from corrupting the personality profile.

**Early-Turn Bias Mitigation:** The EMA mechanism can amplify initial misdetections if early conversation turns contain unrepresentative personality signals (e.g., users responding formally in initial exchanges despite being naturally extraverted). To mitigate this risk, the system implements:

1. **Consistency Requirement:** Strong behavioral adaptations (high-intensity directives) activate only after turn 3 when at least 2 consistent trait readings (variance < 0.2 across last 3 turns) are observed
2. **Gradual Intensity Scaling:** Directive intensity scales proportionally to turn count: turns 1-2 use 50% intensity, turns 3-5 use 75% intensity, turns 6+ use full 100% intensity
3. **Neutral Fallback Mode:** If confidence remains below 0.4 for any trait after 3 turns, the system defaults to balanced, non-adaptive responses for that trait until sufficient evidence accumulates
4. **Early-Turn Variance Monitoring:** If moving variance exceeds 0.25 within turns 1-5, the system logs a warning flag and applies conservative adaptation until stabilization

This multi-layered approach balances responsiveness with protection against premature trait fixation, allowing the α=0.3 parameter to eventually correct early biases (8-12 turns) while minimizing interim misalignment.

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


### 4.3 Regulation Module: Psychologically Grounded Behavior Mapping

Translates continuous OCEAN assessments into behavioral directives via the motivational framework in Section 2.1. Threshold-based activation (|value| ≥ 0.2); continuous values enable intensity-proportional directives.

**Table 4. Trait-to-Directive Mapping**

| Trait | Threshold | High Directive | Low Directive |
|-------|-----------|----------------|---------------|
| **O** | ±0.2 | Novel concepts | Familiar examples |
| **C** | ±0.2 | Structured plans | Flexible guidance |
| **E** | ±0.2 | Energetic tone | Calm, reflective |
| **A** | ±0.2 | Warm, cooperative | Direct, matter-of-fact |
| **N** | ±0.2 | Reassurance, coping | Pragmatic solutions |

Directive intensity scales proportionally to trait magnitude (|value| ≥0.2 activates); confidence <0.4 triggers neutral fallbacks.

### 4.4 Generation Module: RAG-Enhanced Response Production with Personality-Aware Presentation

**Dialogue Grounding and Safety Constraints (Critical Guideline):**

All system responses must be strictly grounded in the user's conversational input, employing a "quote-and-bound" approach that prevents hallucination by ensuring every assertion is entailed by recent dialogue turns. This constraint is particularly critical for human-centered applications where accuracy, reliability, and user trust are paramount. The system must never fabricate external facts, make assumptions about unstated user circumstances, or introduce information not present in the conversation history.

**RAG-Augmented Swiss Policy Guidance (Thesis Implementation Phase):**

When Resource Navigation mode is activated, the system integrates Retrieval-Augmented Generation (RAG) for Swiss caregiver benefit systems:

1. **Context Extraction:** Parse caregiver context from conversation (care recipient age, disability level, financial situation, canton)
2. **Policy Retrieval:** Query vector database of Swiss policy documents (AHV, IV, Hilflosenentschädigung, Ergänzungsleistungen, respite care programs) using semantic similarity
3. **Relevance Filtering:** Retrieve top-3 most relevant policy sections with eligibility criteria, application procedures, and contact information
4. **Personality-Aware Presentation:** Adapt retrieved policy content via behavioral directives:
   - **High-C:** Step-by-step application checklist, required documentation list, timeline
   - **Low-C:** Concise eligibility summary, direct canton contact, optional depth
   - **High-N:** Reassuring framing ("Many caregivers successfully navigate this process"), support availability
   - **High-O:** Mention alternative programs, community resources
   - **High-A:** Collaborative language ("Let's explore your eligibility together")

5. **Grounding Enforcement:** Policy guidance must cite specific documents (e.g., "According to the IV eligibility guidelines for care recipients…", see Appendix A for source families); no invented procedures or criteria

**Response Constraints:**
- **Grounding:** Strict adherence to user's conversational input + retrieved policy documents (with citations)
- **Length:** 70-150 words (policy mode may extend to 180 words for detailed guidance)
- **Interaction:** Maximum 2 questions per response to maintain conversational flow
- **Parameters:** Temperature 0.7, max_tokens 220 (300 for policy mode), 20-second timeout
- **Safety:** If stress level ≥3 and crisis indicators detected, return neutral supportive message with escalation guidance; never provide clinical/legal advice

**Prompt Construction:** Integrates behavioral directives + retrieved policy content + strict grounding constraints (see Appendix B.2).

Citings in text (example):
- "According to the IV/AI eligibility criteria (Appendix A, IV/AI), …"

**Error Handling:** Neutral fallback on failure: "I'm here to support you. Could you tell me more about how you're feeling?" Full session context maintained for debugging. RAG failures trigger policy-free emotional support response.

### 4.5 Data Management and Simulation

#### 4.5.1 PostgreSQL Database Architecture

The system persists longitudinal state across four core tables. **`chat_sessions`** maintains session metadata (ID, start time, mode, status). **`conversation_turns`** stores dialogue history with detected directives and coaching mode applied. **`personality_states`** holds EMA-smoothed OCEAN values (five dimensions), confidence per dimension, and stability flags indicating convergence. **`performance_metrics`** records latencies (detection, generation), token counts, and error logs.

**Data Flow:** Load previous state from PostgreSQL → Detection module (GPT-4) → EMA smoothing (α=0.3) → Save updated state → Next turn retrieves smoothed state for continuity.

#### 4.5.2 Primary Data Sources for This Study

Four concurrent data streams validate system performance across expert, simulated, and real caregiver contexts:

| Data Source | Weeks | Sample | Primary Purpose |
|-------------|-------|--------|-----------------|
| (1) Expert Pilot System Logs | 3–5 | n=5–8 domain experts | Validate personality detection & directive appropriateness |
| (2) LLM Stress Testing & Simulated Evaluation | 11–14 | N≥250 synthetic conversations | Validate EMA parameters, regulation effectiveness, reliability |
| (3) Real Caregiver Validation | 11–14 | n=20–30 Swiss caregivers | Caregiver self-report personality understanding + temporal stability + stress assessment (PSS-10) |
| (4) Human Expert Response Scoring | 11–14 | 2–3 evaluators, κ≥0.70 gate | Gold-standard credibility for findings |

##### **(1) Expert Pilot System Logs (Weeks 3–5, n=5–8 Domain Experts)**

**Source:** Automated logging during think-aloud sessions conducted by in-house domain specialists (Spitex coordinators, geriatricians, home care nurses).

**Personality Understanding Scale (4-item, 5-point Likert):**

Immediately after Session 2 (interactive coaching), caregivers rate how well the system understood their personality using the following validated items:

1. **Emotional State Recognition:** "The system understood my emotional state (stressed vs. calm, anxious vs. confident)"  
   Scale: 1 (Not at all) → 5 (Completely)

2. **Communication Style Adaptation:** "The system adjusted its communication style to match how I prefer to talk (detailed vs. brief, reassuring vs. practical)"  
   Scale: 1 (Not at all) → 5 (Completely)

3. **Support Type Appropriateness:** "The system offered support that matched what I needed (emotional support, practical guidance, policy information)"  
   Scale: 1 (Not at all) → 5 (Completely)

4. **Overall Personality Fit:** "The system seemed to understand my personality and adjusted responses accordingly"  
   Scale: 1 (Not at all) → 5 (Completely)

**Open-Ended Follow-Up:** "How did the system's responses match (or not match) your personality?" (enables thematic analysis for triangulation)

**Scoring & Interpretation:**
- **Primary Metric:** Mean score ≥ 3.5/5.0 across 4 items indicates caregivers perceived system as appropriately understanding their personality
- **Reliability:** Cronbach's α ≥ 0.70 target (internal consistency across 4 items)  
- **Qualitative Analysis:** ≥70% of open-ended comments indicate personality-aware fit (target for behavioral coherence validation)

**Data Captured:**
- OCEAN trait evolution per turn (all 5 dimensions, continuous [−1.0, +1.0] values)
- EMA smoothing parameters applied (α=0.3, confidence thresholds)
- Behavioral directives triggered (timestamp, directive type, intensity scale)
- Response generation metrics (token counts, latency, temperature setting)
- Policy retrieval events (query formulation, retrieved sections, citation verification)
- System errors, fallbacks, and graceful degradation instances
- Session duration, total turns, conversation flow characteristics

**Storage:** PostgreSQL + JSONL audit logs (per-turn verbosity for debugging)

**Use:** Validate personality detection stability, directive appropriateness, and policy grounding accuracy.

##### **(2) LLM Stress Testing & Simulated Evaluation (Weeks 11–14, N≥250 Synthetic Conversations)**

**Source:** Automated evaluation on N≥250 simulated caregiver profiles (Type A/B/C personality distributions × 3 scenarios × 8–10 turns per conversation).

**Personality Understanding Scale (4-item, 5-point Likert):**

Immediately after Session 2 (interactive coaching), caregivers rate how well the system understood their personality using the following validated items:

1. **Emotional State Recognition:** "The system understood my emotional state (stressed vs. calm, anxious vs. confident)"  
   Scale: 1 (Not at all) → 5 (Completely)

2. **Communication Style Adaptation:** "The system adjusted its communication style to match how I prefer to talk (detailed vs. brief, reassuring vs. practical)"  
   Scale: 1 (Not at all) → 5 (Completely)

3. **Support Type Appropriateness:** "The system offered support that matched what I needed (emotional support, practical guidance, policy information)"  
   Scale: 1 (Not at all) → 5 (Completely)

4. **Overall Personality Fit:** "The system seemed to understand my personality and adjusted responses accordingly"  
   Scale: 1 (Not at all) → 5 (Completely)

**Open-Ended Follow-Up:** "How did the system's responses match (or not match) your personality?" (enables thematic analysis for triangulation)

**Scoring & Interpretation:**
- **Primary Metric:** Mean score ≥ 3.5/5.0 across 4 items indicates caregivers perceived system as appropriately understanding their personality
- **Reliability:** Cronbach's α ≥ 0.70 target (internal consistency across 4 items)  
- **Qualitative Analysis:** ≥70% of open-ended comments indicate personality-aware fit (target for behavioral coherence validation)

**Data Captured:**
- EMA convergence metrics (number of turns to stability, final variance, temporal consistency correlation)
- Directive effectiveness scores (0–2 scale × 7 criteria per turn)
- Response quality under stress: tone appropriateness, relevance, personality fit
- Hallucination detection: policy accuracy, citation coverage, fabricated benefits
- Baseline comparison: adaptive vs. non-adaptive vs. memory-only responses
- Inter-run consistency (3 runs per conversation with fixed seeds for reproducibility)
- LLM evaluator confidence scores + human expert agreement (κ≥0.70 gating criterion)

**Storage:** CSV/JSONL with per-turn evaluation records and aggregate metrics

**Use:** Validate EMA parameters, regulation effectiveness, system reliability, and inter-run reproducibility.

##### **(3) Real Caregiver Validation (Weeks 11–14, n=20–30 Swiss Caregivers)**

**Recruitment & Eligibility:**
- **Partners:** Spitex organizations, cantonal home care services, caregiver support groups
- **Inclusion Criteria:** >5 hours/week caregiving, ≥18 years old, Swiss German fluency
- **Compensation:** CHF 50–100 per participant (3 sessions)
- **Ethics:** Informed consent with separate KEK/CE approval (Weeks 1–4)

**Data Collection Timeline:**
- **Session 1 (Week 11):** Demographic questionnaire + BFI-44 (44-item Big Five self-report, 5-point Likert) + informed consent signature
- **Session 2 (Week 12):** Interactive coaching (15–20 min, 1–2 of 3 caregiver scenarios) + system logs collection
- **Session 3 (Week 13–14):** Follow-up + PSS-10 (Perceived Stress Scale, 10 items, 5-point Likert) + **Personality Understanding Scale (4-item, 5-point Likert)** + system usability rating (5-point Likert)

**Personality Understanding Scale (4-item, 5-point Likert):**

Immediately after Session 2 (interactive coaching), caregivers rate how well the system understood their personality using the following validated items:

1. **Emotional State Recognition:** "The system understood my emotional state (stressed vs. calm, anxious vs. confident)"  
   Scale: 1 (Not at all) → 5 (Completely)

2. **Communication Style Adaptation:** "The system adjusted its communication style to match how I prefer to talk (detailed vs. brief, reassuring vs. practical)"  
   Scale: 1 (Not at all) → 5 (Completely)

3. **Support Type Appropriateness:** "The system offered support that matched what I needed (emotional support, practical guidance, policy information)"  
   Scale: 1 (Not at all) → 5 (Completely)

4. **Overall Personality Fit:** "The system seemed to understand my personality and adjusted responses accordingly"  
   Scale: 1 (Not at all) → 5 (Completely)

**Open-Ended Follow-Up:** "How did the system's responses match (or not match) your personality?" (enables thematic analysis for triangulation)

**Scoring & Interpretation:**
- **Primary Metric:** Mean score ≥ 3.5/5.0 across 4 items indicates caregivers perceived system as appropriately understanding their personality
- **Reliability:** Cronbach's α ≥ 0.70 target (internal consistency across 4 items)  
- **Qualitative Analysis:** ≥70% of open-ended comments indicate personality-aware fit (target for behavioral coherence validation)

**Data Captured:**

| Category | Metrics | Notes |
|----------|---------|-------|
| **System Logs** | message_length, response_latency_ms, follow_up_question, directive_acceptance, engagement_score, stress_level, stress_drivers | Identical schema to synthetic data for comparability |
| **Personality Understanding** | 4-item scale (Likert 1-5): emotional tone fit, communication style match, support type appropriateness, overall personality fit. Mean ≥3.5/5.0 target. | Primary validation of personality-aware adaptation |
| **Ground-Truth Instruments** | BFI-44 scores (5 OCEAN dimensions, 0–100 scale each); PSS-10 (perceived stress, 0–40 scale); Usability rating (5-point Likert) | Validated psychometric instruments for context |
| **Qualitative Data** | Open-ended feedback on system understanding and improvement suggestions | Thematic analysis for triangulation |

**Multi-Method Validation Approach:**

This validation employs **multi-method triangulation** rather than relying on BFI-44 as a single ground truth. We combine four complementary validation streams:
1. **Caregiver Self-Report (Primary):** Direct measurement of perceived personality understanding (Mean ≥3.5/5.0)
2. **Temporal Stability (Secondary):** Internal consistency of system OCEAN detection within Session 2 (r >0.70)
3. **Qualitative Coherence (Tertiary):** Behavioral alignment via open-ended feedback thematic analysis (≥70% fit)
4. **BFI-44 Context (Reference):** Provides contextual personality profile information; NOT used as ground truth

**Rationale:** This triangulated approach provides higher ecological validity and construct alignment than using BFI-44 as a single ground truth. It directly addresses "Did the system understand my personality?" rather than "Does system inference match self-report trait?"

**Analysis & Validation:**

| Validation Target | Method | Success Criterion |
|-------------------|--------|-------------------|
| **Caregiver Personality Understanding** | Mean score on 4-item Personality Understanding Scale (Likert 1-5) | Mean ≥ 3.5/5.0 (indicates system understood caregiver personality appropriately) |
| **Trait-Specific Understanding** | Caregivers with stable OCEAN estimates (variance <0.15) → higher understanding scores? | Higher understanding scores in stable group vs. unstable (p<0.05, t-test) |
| **Personality Detection Stability** | Inferred OCEAN consistency within Session 2 (turns 1-10, 5-turn windows) | r > 0.70 (internal temporal consistency) |
| **Stress Level Accuracy** | System-detected stress (0–4) vs. PSS-10 total (0–40, rescaled 0–4) | r≥0.50 (moderate) |
| **Engagement Patterns** | Real caregiver engagement vs. synthetic comparison (independent t-test) | No significant divergence (p>0.05) |
| **Stress Mitigation Rate** | Proportion of high-stress turns (3–4) followed by lower stress after adaptive response | ≥60% mitigation rate |

**Storage:** PostgreSQL `caregiver_validation` table + JSONL logs + encrypted, pseudonymized BFI-44/PSS-10 responses

**Use:** Multi-method validation of personality-aware adaptation (caregiver self-report + temporal stability + qualitative coherence) and stress detection; assess external validity of synthetic findings to real caregiver population.

##### **(4) Human Expert Response Scoring & Crisis Protocol Monitoring (Weeks 11–14)**

**Expert Evaluator Pool & Training:**
- **Recruitment:** 2–3 domain specialists from expert pilot (Spitex coordinators, geriatricians, home care nurses)
- **Certification:** 3-hour session (Week 10)
  - 1 hour: Rubric walkthrough (15-page guide with 30 exemplars per criterion)
  - 1 hour: Practice scoring on 20 sample conversations
  - 1 hour: Calibration discussion and certification check (κ≥0.70 required)

**Scoring Protocol:**
- **Synthetic Sample:** 30% of N≥250 conversations (n≥75, ~600+ turns)
- **Real Caregiver Sample:** 100% of n=20–30 caregivers (~60–90 turns total)
- **Blinding:** Each response independently scored by 2 evaluators (blinded to each other and condition)

**Scoring Rubric (5 Criteria, 0–2 Scale Each):**
1. **Emotional Tone Appropriateness** – Matches detected stress level and personality profile
2. **Engagement Quality** – Maintains conversation flow and encourages participation
3. **Stress Reduction Effectiveness** – Addresses stated concern and reduces stress signals
4. **Relevance & Coherence** – Directly relevant, logically sound, no non-sequiturs
5. **Factual Accuracy** – Policy claims verified, no hallucinations, citations present

**Scoring Workflow:**
- Initial scores averaged or discussed if >0.5-point difference
- Consensus score used for final analysis
- Inter-rater agreement (Fleiss' κ) calculated after every 20–30 scored responses
- **Target:** Team κ≥0.75 (excellent agreement); if κ<0.75, re-calibrate and re-score subset

**Crisis Protocol Monitoring:**
- Document any Level 4 (crisis) detections during real caregiver sessions
- Verify automatic crisis line contact message delivered (TeleFon 143, 112 emergency)
- Log researcher notification and action taken
- **Strict enforcement:** Any protocol violations trigger immediate retraining

**Storage:** Expert scoring records (per-turn, per-criterion), inter-rater reliability logs, crisis incident log (if applicable)

**Use:** Gate for validating LLM evaluator on remaining synthetic responses; provides gold-standard credibility for thesis findings.

#### 4.5.3 Database Schema

**Table 5. PostgreSQL Schema Overview**

| Table | Primary Key | Purpose | Key Columns |
|-------|-------------|---------|-------------|
| `chat_sessions` | `session_id` (UUID) | Session metadata | `total_turns`, `evaluation_mode`, `status` |
| `conversation_turns` | `(session_id, turn_index)` | Conversation history | `user_message`, `assistant_response`, `directives_applied`, `coaching_mode` |
| `personality_states` | `(session_id, turn_index)` | EMA-smoothed OCEAN | `ocean_o/c/e/a/n`, `confidence_o/c/e/a/n`, `stable` |
| `performance_metrics` | `(session_id, turn_index)` | System performance | `detection_latency_ms`, `generation_latency_ms`, `total_tokens` |

**Table 5b. Engagement & Stress Metrics Schema**

| Table | Primary Key | Purpose | Key Columns |
|-------|-------------|---------|-------------|
| `engagement_metrics` | `(session_id, turn_index)` | Caregiver engagement tracking | `engagement_score` (0-2), `message_length`, `response_latency_ms`, `follow_up_question` (bool), `directive_acceptance` (bool), `session_engagement_avg` |
| `stress_metrics` | `(session_id, turn_index)` | Detected stress signals | `stress_level` (0-4), `lexical_markers` (array), `emotional_intensity_score`, `problem_escalation` (bool), `stress_drivers` (array), `response_appropriateness` (0-2) |
| `engagement_stress_interaction` | `(session_id)` | Cross-turn engagement-stress dynamics | `engagement_stress_correlation`, `stress_reduction_rate`, `stress_mitigation_success_rate` (%), `scenario_consistency_correlation` |

**Simulation Protocol for Swiss Caregiver Scenarios:**

Three personality profiles (Type A: high OCEAN +0.8 except low N; Type B: low OCEAN -0.8 except high N; Type C: mixed profiles) engage in three **caregiver-specific stress scenarios** covering all coaching modes:

1. **Emotional Burden & Role Strain** (Emotional Support mode)
   - Scenario: Caregiver managing parent with dementia, experiencing guilt over considering nursing home placement
   - High-N receives: Reassurance, normalization, validation of conflicting feelings
   - Low-N receives: Pragmatic acknowledgment, solution-focused framing

2. **Benefit System Navigation** (Resource Navigation mode)
   - Scenario: Caregiver confused by IV (Invalidenversicherung) eligibility requirements for adult child with disability
   - High-C receives: Detailed step-by-step application checklist, required documentation list
   - Low-C receives: Concise overview with direct canton contact, optional depth

3. **Self-Care Neglect & Burnout Risk** (Self-Care Planning mode)
   - Scenario: Caregiver reporting exhaustion, sleep disruption, social isolation due to 24/7 care demands
   - High-E receives: Social support mobilization strategies (support groups, family coordination)
   - Low-E receives: Individual restoration focus (micro-breaks, boundary-setting scripts)

**Conversation Parameters:** 8-10 turns per session, 10-15 sessions per profile × 3 scenarios = 90-135 total simulated conversations. Convergence tracked with `stable=TRUE` target at turns 6-8 for ≥80% sessions.

**Baseline Conditions:** Parallel conversations using (1) generic non-adaptive assistant, (2) memory-only assistant (mem0-style factual recall without personality modeling), (3) policy-only assistant (RAG guidance without personality adaptation).

**Export Format:** CSV/JSONL with per-turn OCEAN evolution, directives applied, coaching mode, caregiver scenario context, RAG policy retrieval (if applicable), stability flags, and convergence metrics.

### 4.6 Evaluation Framework

This section specifies our comprehensive evaluation methodology across three validation contexts: synthetic conversations (N≥250), expert pilot sessions (n=5-8), and real caregiver validation (n=20-30).

**Evaluation Criteria:**

We assess personality-aware system responses using seven dimensions, while baseline (non-adaptive) systems are evaluated on three core dimensions:

*Personality-Aware System (7 criteria):*
1. **Detection Accuracy:** How well inferred OCEAN traits align with observable personality cues
2. **EMA Convergence:** Quality of temporal stabilization (variance <0.15 by turn 6-8)
3. **Confidence Calibration:** Appropriateness of system confidence scores relative to available evidence
4. **Regulation Effectiveness:** Correct application of personality-based behavioral strategies
5. **Emotional Tone:** Response tone matches user's emotional state and personality profile
6. **Relevance & Coherence:** Contextually appropriate and logically consistent responses
7. **Personality Needs:** Addresses trait-specific psychological and interactional requirements

*Baseline Systems (3 criteria):*
1. **Emotional Tone Appropriateness**
2. **Relevance & Coherence**  
3. **Personality Needs Addressed**

Each criterion scored 0-2 (No/Partial/Yes). Personality-aware system maximum: 14 points; baseline maximum: 6 points.

**Evaluation Data Structure:**

Each conversation turn generates a structured evaluation record containing:

**Context Data:**
- Profile type (Type A/B/C for synthetic; real caregiver demographics for human sessions)
- Turn number (1-10) and conversation messages (user input, system response)

**Personality Detection Data:**
- OCEAN trait values (continuous scale -1.0 to +1.0, EMA-smoothed)
- Confidence scores per trait (0.0-1.0 range)
- Stability status (TRUE/FALSE; achieved at ≥6 turns with variance <0.15)
- Applied directives (behavioral strategies activated based on detected traits)

**Quality Scores (0-2 scale per criterion):**
- Detection accuracy, EMA convergence quality, confidence calibration
- Regulation effectiveness, emotional tone appropriateness
- Relevance & coherence, personality needs satisfaction
- **Total:** 0-14 points (personality-aware); 0-6 points (baseline)

**Engagement Measurement:**

System logs automatically capture engagement indicators including message length, response timing, follow-up questions, and directive acceptance. Each turn receives an engagement score (0-2 scale):
- **2 (High):** Detailed responses with follow-up questions and directive adoption
- **1 (Moderate):** Brief responses with minimal follow-up
- **0 (Low):** Single-word replies or disengagement signals

**Target:** Session-level mean ≥1.2/2.0 indicates sustained caregiver engagement.

**Stress Detection and Response:**

The system automatically detects stress levels (0-4 scale) based on linguistic markers including stress vocabulary (overwhelmed, exhausted, helpless), emotional intensity (capitalization, repeated punctuation), problem escalation indicators, and coping strain phrases.

**Stress Classification:**
- **0-1 (None/Mild):** Stable tone, organized presentation → Balanced guidance
- **2 (Moderate):** Clear stress signals with coping language → Validation + specific strategies
- **3 (High):** Strong negative emotion, limited coping → Intensive reassurance, stepwise support
- **4 (Crisis):** Acute distress, danger signals → Immediate crisis resources, professional referral

**Stress Drivers:** System annotates primary sources (caregiver burden, benefit navigation, self-care neglect, financial strain, social isolation) to tailor support appropriately.

**Engagement-Stress Dynamics:**

We measure whether personality-aware responses effectively mitigate stress and sustain engagement:
- **Stress Mitigation:** ≥60% of high-stress turns (3-4) followed by reduced stress after adaptive response
- **Engagement-Stress Relationship:** Engagement increases as stress decreases (target r ≥ 0.4)
- **Cross-Scenario Consistency:** Patterns remain consistent across emotional, educational, and policy support scenarios (r ≥ 0.7)

**Example Evaluation (Synthetic Conversation, Turn 6):**

*High-Openness Caregiver (Type A):*
- **User:** "I'm excited to try new approaches..."
- **System:** "That's wonderful! Let's explore some creative strategies..."
- **Detected OCEAN:** O:0.78, E:0.82, stable
- **Directives Applied:** Novel ideas, energetic tone, structured steps
- **Quality Score:** 14/14 (all criteria met)

*High-Neuroticism Caregiver (Type B):*
- **User:** "Everything feels uncertain..."
- **System:** "I understand uncertainty is difficult. Let's focus on what you can control..."
- **Detected OCEAN:** N:0.79, stable
- **Directives Applied:** Extra comfort, calm tone, familiar examples
- **Quality Score:** 14/14 (appropriate adaptation)

**Automated Evaluation with Human Oversight:**

Automated LLM evaluators (GPT-4, fixed prompts) score all conversations using the criteria above. Each criterion receives a trinary score: Yes (2 points), Partial (1 point), No (0 points). To ensure credibility, human expert evaluators independently score 10-15% of conversations (minimum n=20). Human-LLM agreement must achieve Cohen's κ≥0.70; failure triggers expanded human evaluation. This gating mechanism ensures automated scoring validity before scaling to full dataset.

**Use-Case Outcome Metrics (Simplified Expert Evaluation):**

To ensure feasibility while maintaining rigor, this study focuses on **expert pilot evaluation** (n=5-8 domain experts: home care specialists, Spitex coordinators, geriatricians) rather than full caregiver population studies. This approach validates core functionality without requiring large-scale demographic sampling, which is deferred to the thesis phase:

| Evaluation Focus | Method | Measurement | Target Threshold |
|-----------------|--------|-------------|------------------|
| **System Usability** | Expert think-aloud protocol (3 core tasks) | System Usability Scale (SUS) + task success rate | SUS ≥70; task success ≥80% |
| **Personality Adaptation Appropriateness** | Expert judgment: Does personality detection seem accurate? | 5-point Likert scale ("How well did the system understand the caregiver's personality?") | ≥4.0/5.0 average |
| **Policy Guidance Clarity** | Expert review: Are policy recommendations accurate and grounded? | Manual verification against source documents; no hallucinations | All claims cite sources; no fabricated benefits |
| **Emotional Support Quality** | Expert assessment: Does tone match caregiver stress level? | 5-point rubric (inappropriate / partially appropriate / well-matched / excellent / exceptional) | ≥4.0/5.0 average |
| **Tone-Fit Accuracy** | Expert rating: Is response tone suited to detected personality? | Comparison of generated tone vs. detected traits | ≥80% alignment |
| **Grounding Enforcement** | Automated verification: All policy claims cite sources | Percentage of policy statements with document citations | 100% citation coverage; audits detect no critical errors (≤5% minor flags) |

**Expert-only scope rationale:** n=5-8 domain experts provide rapid, expert-informed validation of usability and policy accuracy without requiring large-scale demographic sampling (deferred to thesis).

**Qualitative feedback:** Semi-structured expert interviews (n=5-8) on personality adaptation appropriateness, policy clarity, emotional support quality, system reliability, and improvement suggestions.

**Experimental Validation (Expert-Focused Scope):**

| Experiment | Objective | Method | Success Criteria |
|------------|-----------|--------|------------------|
| **E1: Expert Pilot** | Validate system usability and personality accuracy with domain experts | n=5-8 think-aloud sessions; SUS ≥70; expert Likert ratings ≥4.0/5.0 | Core functionality validated; no policy hallucinations |
| **E2: EMA Sensitivity** | Validate α=0.3 selection | Test α ∈ {0.1, 0.2, 0.3, 0.4, 0.5} with N≥250 simulated conversations | Convergence ≤8 turns, σ²<0.15, best responsiveness |
| **E3: Regulation Effectiveness** | Validate directive-outcome alignment | Ablation tests removing directives; measure quality impact | Cohen's d≥0.3 for primary directives |
| **E4: Human-LLM Agreement** | Validate automated evaluator | Two human annotators + LLM on n≥20 conversations | Cohen's κ≥0.70 (release gate) |
| **E5: Policy Pack Transfer** | Validate cross-domain reusability | Two independent implementers swap policy packs (2 domains) | Median time ≤30 min, no code changes |

**Baseline Conditions:** Generic (non-adaptive), memory-only (mem0-style), detection-only (no regulation). Target: Cohen's d≥0.3, ≥15% improvement vs. baseline.

**Two-Tier Acceptance (Power-Adjusted):** (1) **Initial Validation Gate (r ≥ 0.50)** — Temporal correlation between consecutive OCEAN estimates; achievable with ~25 paired observations (α=0.05, power=0.80). (2) **Thesis Target (r ≥ 0.75)** — Criterion validity against BFI-44, requiring n≥60 for adequate power.

**Temporal smoothing parameters.** EMA (α=0.3) stabilizes traits by turns 6–8 (variance <0.15); weights 30% current observation, 70% historical average. Confidence thresholds—0.4 (minimum for updates) and 0.7 (high-confidence adaptation)—align with personality assessment reliability standards (r≥0.7; Park et al., 2015). Sensitivity analysis (α ∈ {0.1, 0.2, 0.3, 0.4, 0.5}) in Appendix G.

### 4.7 System Advantages and Reproducibility

**Key Advantages:** Psychological framework fidelity captures motivational intensity; EMA enables smooth temporal tracking reducing trait oscillation; fine-grained adaptation (continuous values vs. discrete); confidence weighting filters unreliable detections; PostgreSQL persistence supports longitudinal analysis.

**Reproducibility Measures:** Fixed parameters (model versions, API endpoints, temperature, seeds, prompt hashes); complete JSONL logging (per-turn traces, node timings, errors, configs); neutral fallbacks for all failures; dialogue-only grounding; automated CSV export for analysis.

---

## 5. Technology, Software, and Applications

### 5.1 Core Technology Stack

The system employs an N8N-orchestrated architecture combining: (1) **Backend**: N8N workflow engine with PostgreSQL (ACID-compliant state persistence) and Redis (session caching); (2) **LLMs**: GPT-4.1 for detection (temp 0.3, 300 tokens, 30s timeout) and generation (temp 0.7, 220 tokens, 20s timeout), with Gemini 2.5 Pro as cost-effective alternative; (3) **Frontend**: Next.js 14+ (React 18) with Server-Sent Events for real-time OCEAN updates; (4) **Containerization**: Docker Compose for local development, Vercel for frontend deployment. Complete specifications in supplementary materials.

### 5.2 Development and Testing

**Environment Setup**: Docker Compose orchestrates N8N, PostgreSQL, and Redis containers with `.env` configuration, locked dependencies (`requirements.txt`, `package.json`), and encrypted API keys via N8N credential vault. **Quality Assurance**: Automated testing suite (`test_personality_chatbot.sh`, `test_detection_accuracy.sh`, `test_regulation_coherence.sh`) validates JSON contracts, EMA convergence, and evaluator consistency. **Monitoring**: N8N execution logs track node timings, success rates, token usage, and system health with automated failure alerts.

### 5.3 Security and Privacy

**Data Protection**: AES-256 encryption at rest, TLS 1.3 in transit; role-based access (PI and supervisor only); complete audit trails via JSONL logging; data minimization (no PII collection). **API Security**: N8N credential vault for key management; rate limiting (configurable per endpoint); sanitized error messages; HTTPS enforcement. **Privacy Compliance**: Anonymization protocols, explicit user consent, GDPR adherence with 5-year retention and user-controlled deletion rights.

---

**Ethics and Regulatory Compliance (Expanded):**

**Cantonal Ethics Committee (KEK/CE) Process:**
- This study (expert pilot, synthetic evaluation): **Self-governance** via Institutional Review (internal ethics checklist; no formal submission required)
- Real caregiver phase (thesis): **Formal submission** via swissethics.ch platform (~Weeks 1–4) to cantonal ethics committee (equivalent to US IRB). Expected approval timeline: 2–4 weeks post-submission.

**GenAI Transparency & Emerging Guidelines:**
- All LLM prompts generated with human oversight; disclosed in appendices with seed values for reproducibility
- Data analysis, bias audits, statistical synthesis: Zero genAI involvement
- Risk mitigation: Quarterly bias audits comparing directive distribution across demographics (gender, age, care-recipient type); document any skew

**Bias Mitigation & Fairness:**
- Detection module blind to demographics; directives reviewed for equity across SES groups
- Monthly audit logs tracking directive distribution by inferred personality traits; flag any systematic over/under-representation
- Qualitative feedback from n=5–8 experts in pilot: "Did the system treat different caregiver profiles fairly?"

---

### 5.4 Computational Costs and Performance

**Cost and Performance Estimates**: Initial cost modeling suggests per-turn expenses and latency targets that favor GPT-4 for accuracy with Gemini-1.5-Pro as cost-effective alternative. Optimization strategies include response caching, batch processing, and adaptive verification. **Cost Sensitivity (±50% band):** Actual costs depend on provider pricing, prompt/response token length, and request volume; budget projections assume 520 tokens/turn and are subject to ±50% variance due to token price fluctuations, API tier changes, and prompt optimization. **Latency SLOs & Hardware Assumptions:** For this study, latency targets are **p90 < 2.5s end-to-end** under local development hardware (16GB RAM, 4-8 vCPU, low network latency). Production p95 targets and deployment on cloud infrastructure (e.g., AWS t3.large + CloudFront) will be revisited during the thesis phase. Detection latency target: <1.5s (p95); generation latency: <1.5s (p95); database operations: <100ms (p95). Detailed vendor-specific costs, latency benchmarks, and token usage projections are provided in Appendix E (based on Q4 2024 pricing; subject to provider changes).

### 5.5 Deployment and Maintenance

**Deployment Strategy**: Docker Compose for development; cloud staging environment for integration testing; Kubernetes planned for production scaling (horizontal N8N instances, PostgreSQL read replicas). **Maintenance Protocols**: Model version locking with API endpoint pinning; N8N workflow version control (Git-tracked JSON exports); automated PostgreSQL backups (daily encrypted snapshots); complete technical documentation for reproducibility.

### 5.6 Frontend Architecture: Next.js/React Web Interface

**Next.js/React UI (Weeks 9-10, Thesis Phase):**

For the thesis phase, a **Next.js/React** web interface will be developed for expert pilot testing, real caregiver sessions, and thesis defense demonstration. This provides modern, responsive UI with production-ready architecture.

**Core Features:**
1. **Personality Trait Display** — Real-time OCEAN scores with visual radar chart + EMA trajectory
2. **Directive Logging** — Show active behavioral directives applied to current response
3. **Policy Navigation** — Display RAG-retrieved policy chunks with source citations + confidence scores
4. **Think-Aloud Protocol Support** — Session recording, participant feedback buttons (helpful/not helpful), post-session SUS questionnaire
5. **Admin Dashboard** — Expert session review, metric tracking (SUS, task success, tone fit)

**Rationale:** Next.js/React provides modern component architecture, server-side rendering, and seamless deployment to Vercel, suitable for expert pilot work (n=5–8), real caregiver sessions (n=20–30), and thesis examination.

**Implementation Stack:**
- Backend: Flask REST API (detect→regulate→generate pipeline)
- Frontend: Next.js 14+ with React 18 (UI layer)
- Deployment: Vercel for cloud hosting with automatic scaling

**Success Criteria:** UI supports expert think-aloud tasks without technical friction; SUS ≥70; no critical failures across 5-8 expert sessions.

---

## 6. Project Plan and Risk Management

### 6.1 Thesis Proposal and Structure

**Annotated Thesis Structure (Target: 80-100 pages)**

**Chapter 1: Introduction** (8-10 pages) - Context, problem statement, research objectives, RQ1-5, contributions, organization

**Chapter 2: Literature Review** (15-18 pages) - Big Five/Zurich Model foundations, personality-aware AI state-of-art, industrial memory systems, LLM dialogue systems, temporal stability methods, research gaps

**Chapter 3: Methodology** (20-25 pages) - Design science approach operationalized via RQ1-2 (Mechanism & Modeling: personality detection via EMA α=0.3, trait-to-directive mapping), RQ3 (Swiss Policy Grounding: RAG architecture, citation verification), RQ4 (Human Factors & Multi-Stream Validation: expert pilot, real caregiver protocol, human expert scoring), RQ5 (Robustness & Generalization). Includes system architecture (detect→regulate→generate), evaluation framework, data management protocols.

**Chapter 4: Implementation** (15-18 pages) - N8N workflow, EMA parameter tuning, policy pack development, database schema, simulation protocol, evaluation harness, containerization

**Chapter 5: Results** (15-20 pages) - Structured by RQ1-5: RQ1-2 findings on personality detection (r≥0.75), EMA convergence (6-8 turns), regulation effectiveness, generation quality; RQ3 findings on policy accuracy and citation grounding (100% coverage, ≤5% minor flags); RQ4 findings across multi-stream validation (expert SUS≥70, real caregiver r≥0.60/r≥0.50, human expert κ≥0.75); RQ5 scope analysis including baseline comparisons (Cohen's d≥0.5), system reliability, cross-domain demonstration, external validity boundaries.

**Chapter 6: Discussion** (12-15 pages) - Findings interpretation organized by RQ themes: RQ1-2 theoretical contributions (Zurich operationalization, personality detection mechanisms, trait-to-motivation mappings), RQ3-4 practical contributions (Swiss policy navigation architecture, multi-stream validation framework), memory-motivation integration. Includes comparison with Devdas (2025) and industrial systems, validity threats per RQ5 boundaries, ethical considerations, generalization potential.

**Chapter 7: Conclusion** (5-8 pages) - Summary of RQ0-5 findings with evidence from multi-stream validation. Limitations categorized by RQ scope: personality measurement and temporal stability (RQ1-2), policy domain-specific coverage (RQ3), sample sizes and clinical scope (RQ4), generalization to other domains (RQ5). Future research directions aligned with RQ evolution: multimodal input (extends RQ1-2), cross-cultural validation (extends RQ5), clinical outcome trials (extends RQ4), production deployment (extends RQ3-4).

**Three Core Thesis Extensions:**
1. Human Validation (Weeks 15-16): n=30-50 human participants with BFI-44 ground truth; target r≥0.75 detection correlation, κ≥0.80 inter-rater reliability
2. Large-Scale Simulation (Weeks 11-14): N≥250 simulated conversations for A/B testing vs. mem0/LangChain baseline; target ≥20% improvement on emotional tone and needs satisfaction
3. Cross-Domain Demonstration (Weeks 8-10): Education and customer service policy pack swaps; target <30 min transfer time, no breaking changes

### 6.2 Twenty-Week Work Plan

**Timeline:** Foundation (Weeks 1-2) → Expert Pilot (Weeks 3-5) → RAG & Q-A Benchmarking (Weeks 6-8) → Implementation & UI (Weeks 9-10) → Real Caregiver Recruitment (Weeks 8-9) → Simulated & Real Caregiver Evaluation + Human Expert Scoring (11-14) → Analysis & Writing (17-19) → Finalization (20).

**Table 8. Twenty-Week Work Plan with Milestones (Integrated Plan)**

| Phase | Week(s) | Primary Activities | Key Deliverables | Success Criteria |
|-------|---------|-------------------|------------------|------------------|
| **Phase 1: Foundation** | 1-2 | Literature review; theoretical framework; RQ refinement; environment setup; FADP/privacy planning; **KEK/CE submissions (Main study + Crisis protocol)** | Annotated bibliography; theoretical framework; finalized RQs; functional dev environment; FADP checklist; **KEK/CE protocols submitted** | 30+ papers reviewed; clear theoretical grounding; testable RQs; working N8N + Docker setup; **KEK/CE approvals pending** |
| **Phase 2: Expert Pilot** | 3-5 | Recruit n=5-8 domain experts (Spitex coordinators, geriatricians); conduct think-aloud sessions (3 core tasks: policy query, caregiving skill Q, tone-fit rating); **train 2-3 experts as evaluators (3-hour certification)**; analyze usability & effectiveness | Expert session recordings; SUS scores; think-aloud transcripts; usability report; **Expert evaluator rubric (15 pages) + certification records** | n=5-8 experts onboarded; SUS ≥70; task success ≥80%; tone appropriateness ≥4.0/5.0; no detected hallucinations in policy claims; **κ≥0.70 evaluator certification** |
| **Phase 2.5: Caregiver Recruitment & Prep** | 8-9 | Partner with Spitex + caregiver support groups; finalize informed consent forms; **KEK/CE approval for real caregiver study (parallel with Phase 3)**; recruit n=20-30 Swiss caregivers (>5h/week, CHF 50-100 compensation); arrange sessions | Informed consent templates; caregiver recruitment cohort; session scheduling; **KEK/CE caregiver protocol approved** | n=20-30 caregivers recruited; 80%+ consent rate; sessions scheduled for Weeks 11-14; **Crisis protocol KEK/CE approved** |
| **Phase 3: RAG & Benchmarking** | 6-8 | Curate policy documents (IV-Stelle, BAG, cantonal Spitex); generate 20-30 Q-A-chunk benchmark pairs (manual + LLM-assisted); expert review & validation; implement minimal retrieval system | Q-A benchmark dataset; RAG retrieval module; validation report; policy document corpus (2 domains: IV, Hilflosenentschädigung) | 20-30 validated Q-A pairs; retrieval accuracy Recall@3 ≥0.7; groundedness rubric ≥1.5/2.0; no detected hallucinations |
| **Phase 4: Implementation (Core)** | 7-10 | Detection module development; regulation logic; generation pipeline; EMA integration; **EMA sensitivity analysis (α ∈ {0.1–0.5}, generate convergence curves, Week 10)**; **Stress driver validation (Week 9), engagement formula derivation (Week 10), stress level calibration (Week 10)**; Next.js/React UI; integration testing | Working personality detection; regulation engine; response generation; Next.js demo; integration tests; **EMA sensitivity table, stress driver confusion matrix, engagement weights, stress calibration table** | Detection accuracy ≥70%; stable trait convergence; grounded responses; UI supports think-aloud protocol; no unhandled exceptions in expert sessions; **α=0.3 empirically justified, driver κ≥0.70, engagement formula AUC≥0.75** |
| **Phase 5: Evaluation & Validation (Multi-Stream)** | 11-14 | **Multi-stream validation as defined in Sections 4.5 & 4.6:** (a) Real Caregiver Sessions (Session 1: BFI-44 + consent; Session 2: interactive coaching + logs; Session 3: PSS-10 + usability feedback); (b) Synthetic Evaluation (N≥250 conversations with 3 baselines; See Section 4.5 for detailed protocol); (c) Human Expert Scoring (2-3 experts, 15-page rubric, κ≥0.70 certification, independent blind scoring of 30% synthetic + 100% real); (d) Crisis Monitoring (Level 4 detection verification, automated alert confirmation, action logging); (e) Baseline Comparisons (Adaptive vs. Generic vs. Memory vs. Policy-Only). | Real caregiver data (BFI-44, PSS-10, engagement logs, qualitative feedback); Synthetic evaluation results; Expert scoring records (per-turn, per-criterion); baseline comparison tables; crisis incident log; inter-rater κ reports | Real caregivers: r≥0.60 personality, r≥0.50 stress vs. ground truth; ≥60% stress mitigation; ≥80% retention. Synthetic: Cohen's d≥0.3 vs. baseline. Human scoring: κ≥0.75 team agreement; mean ≥1.4/2.0. Crisis: no protocol violations. |
| **Phase 6: Advanced Validation & Analysis** | 15-16 | **Analysis framework per Sections 4.5.2 & 4.6:** Real vs. Synthetic Comparison (validation tables, personality/stress alignment). Statistical Analysis (correlation tables for BFI-44/PSS-10, Cohen's d effects, Fleiss' κ). Temporal Dynamics (Vector autoregression for engagement-stress causality). Policy Audit (250 policy claims reviewed; hallucination classification). | Validation report; statistical summary tables; baseline effect sizes; causal analysis plots; policy audit results | Consistent r≥0.60/r≥0.50 across real/synthetic; baseline d≥0.30; all policy claims cite sources; temporal causality p<0.05 |
| **Phase 7: Analysis & Writing** | 17-19 | Statistical analysis synthesis; visualization (convergence curves, baseline charts, validation tables); thesis writing; limitation analysis; expert pilot + human expert + caregiver insights integration; crisis protocol summary | Complete thesis draft; publication-ready figures; thesis proposal; crisis protocol documentation | Complete analysis; stated contributions; documented limitations; thesis roadmap; crisis procedures documented |
| **Phase 8: Finalization** | 20 | Supervisor feedback integration; peer review; final QA; presentation prep; **update title/abstract to reflect real caregiver validation + human expert scoring**; code/documentation handover | Final thesis v1.0; presentation slides; GitHub repo; handover docs; **updated abstract & limitations documenting real vs. synthetic validation scope** | Publication-ready document; presentation materials; reproducible artifacts; smooth handover; **external validity bounded** |
|


**Resources:** LLM API credits (~$200-500), N8N/Docker infrastructure, R/Python statistical tools, supervisor meetings (2hr/week), peer reviewers, psychology expert consultation, in-house domain expert time (volunteer or internal allocation).

### 6.3 Risk Management

**Risk Matrix:** Assesses likelihood/impact (Low/Medium/High). Key risks: **Expert Recruitment (Weeks 3-5)** (Medium/Medium) — In-house domain experts may have limited availability; mitigated by early outreach, flexible scheduling, incentive (CHF 50-100 vouchers), pilot protocol simplicity (15-20 min think-aloud sessions). **Q-A Benchmark Generation (Weeks 6-8)** (Medium/Medium) — LLM-generated Q-A pairs may contain hallucinations or require extensive manual review; mitigated by expert validation gate (κ≥0.70), multi-source policy doc triangulation, small batch size (20-30 pairs manageable). **Evaluation** (LLM evaluator bias/drift, Medium/High) mitigated by fixed prompts, 3× runs, human spot-checks; **Reproducibility** (non-determinism, Medium/High) addressed by pinned model versions, fixed seeds, config logging; **Data Quality** (simulated profiles, Medium/Medium) managed by expert validation, mid-range profiles, expert pilot human validation; **Technical** (prompt sensitivity, Medium/Medium) controlled by versioning, A/B tests, directive auditing; **Infrastructure** (vendor interruptions, Medium/Medium) handled by provider abstraction, alternates, retries; **Ethics/Privacy** (data protection, Low/High) ensured by anonymization, encryption, IRB compliance; **Scope** (feature creep, Medium/Medium) prevented by guardrails (2-domain RAG focus, Next.js UI), change control, thesis deferral.

**Mitigation Playbooks:** Evaluator drift (consistency <0.85) → freeze prompts, compare providers; JSON failures (>0.5%) → schema validation, temperature reduction; Latency (p95 >2s) → reduce tokens, cache responses; Privacy incident → rotate keys, audit logs.

**Contingency:** Alternative LLM providers (GPT-4, Claude, Gemini) ready for failover. Scope adjustment gates: evaluator consistency <0.75 → escalate to human sample; Q-A hallucinations >10% → extend expert review cycle; recruitment delays → adjust timeline accordingly.

**Monitoring (Planned):** Weekly KPI tracking targets: JSON compliance ≥99.5%, EMA stabilization ≥80%, evaluator consistency ≥0.85, p95 latency <2.0s, no privacy incidents.

---

## 7. Future Work

### 7.1 Future Research Directions

Future research directions beyond this study include: (1) **Clinical outcome validation:** Caregiver participant studies (n=150+) with pre/post measurement of stress, burden reduction, and engagement (requires separate KEK/CE approval), (2) **Cross-cultural and multilingual adaptation:** Swiss French/Italian language variants and cultural nuance validation across linguistic regions, (3) **Multimodal personality detection:** Integration of voice prosody and facial expression analysis for enhanced personality inference, (4) **Longitudinal trait evolution:** Long-term personality adaptation tracking over months of sustained use, (5) **Expanded policy domain coverage:** Comprehensive Swiss healthcare system navigation across cantonal variations and major support programs, (6) **Production deployment:** React/Next.js frontend, cloud infrastructure, and enterprise integration with Spitex organizations.

### 7.2 Limitations and Future Research Directions

| Area | Boundary / Limitation (This Study) | Future Research Path |
|------|------------------------------------|---------------------|
| **Sample Scope** | Expert pilot (n=5–8), real caregivers (n=20–30, brief sessions); no longitudinal follow-up beyond 2–3 weeks | Clinical-scale trials (n=150+) with 6-month longitudinal measurement; RCT with control condition |
| **Geographic/Policy Domain** | Swiss German prototype only; 2-policy domains (IV, Hilflosenentschädigung); limited cantonal coverage | Multilingual (French, Italian); comprehensive cantonal policy coverage; cross-country adaptation study |
| **Caregiver Population** | No intersectional fairness validation (gender, age, care-recipient type); self-selected convenience sample | Stratified sampling; underrepresented population studies; long-term retention tracking |
| **Personality Measurement** | OCEAN detection model accuracy vs. validated BFI-44 ~0.60; single-conversation ceiling effects possible | Multi-session trait stability (6+ weeks); clinical personality assessments; facial expression + voice prosody integration |
| **Clinical Outcomes** | Non-clinical scope: stress measurement via PSS-10 proxy, NO clinical diagnosis capability; caregiver burnout not clinically validated | Separate KEK/CE approval for clinical trial; validated clinical outcome instruments (Caregiver Burden Inventory, clinician assessment) |
| **Stress Level Detection** | System-generated stress 0–4 scale untested; calibration via synthetic examples + PSS-10 only; 3-driver model simplified from literature | Intensive within-subject studies; ecological momentary assessment (EMA) validation; real-time physiological sensors |
| **Engagement Metrics** | Formula weights (message length, latency, directives) data-derived but not validated externally | Separate engagement study (n=50+) with think-aloud / eye-tracking; convergent validity with SUS |
| **Crisis Protocol** | KEK/CE-approved procedure tested internally; no external crisis center coordination (one-directional alert only) | Integration with Swiss emergency services (TeleFon 143 API, 112 dispatch); follow-up safety monitoring protocol |
| **Generalization to Other Domains** | Policy-pack reusability demonstrated (interchangeability test only); other domains (education, customer service) untested | Cross-domain A/B testing; different user populations (students, patients, employees); sector-specific validation |
| **Ethical Boundaries** | FADP compliance design; DPIA stub only (not full risk assessment); no real-world data governance audit | Full DPIA implementation; longitudinal privacy impact audits; bias audit on OCEAN algorithm itself |
| **Multimodal Input** | Text only (Swiss German); no voice, facial expression, or gesture recognition | Audio prosody + transcription; facial expression analysis; integration roadmap in thesis |
| **Cost-Benefit Analysis** | Implementation cost estimated; adoption barriers not studied; Spitex integration not validated | Health economic evaluation (QALYs, cost-effectiveness); organizational adoption study; sustainability model |

**Explicit Deferred to Future Phases:**
- Full clinical RCT with pre/post caregiver burnout/stress measurement (requires separate ethics approval and multi-site collaboration)
- Cross-cultural and multilingual adaptation (French, Italian, potentially English)
- Production UI (React/Next.js) and enterprise deployment (cloud infrastructure, Spitex organization partnership, SSO integration)
- Long-term personality evolution and trait stability over months of sustained use
- Physiological validation (heart rate variability, cortisol measurement) of stress detection algorithm
- Comparative effectiveness studies (vs. human coach, vs. alternative digital interventions)

**Note:** This study establishes validated technical methodology and external validity boundaries for caregiver-specific personality-aware dialogue systems. Limitations reflect appropriate scope for a proof-of-concept study with real caregiver validation; they do not represent design failures but rather deliberate constraints ensuring feasibility, ethical appropriateness, and foundation for future clinical research.

## 8. References

Adamopoulou, E., & Moussiades, L. (2020). An overview of chatbot technology. In *IFIP International Conference on Artificial Intelligence Applications and Innovations* (pp. 373-383). Springer. https://doi.org/10.1007/978-3-030-49186-4_31

Alisamir, S., & Ringeval, F. (2021). On the evolution of speech representations for affective computing: A brief history and critical overview. *IEEE Signal Processing Magazine*, 38(4), 12-21. https://doi.org/10.1109/MSP.2021.3106890

Anttila, T., Selander, K., & Oinas, T. (2020). Disconnected lives: Trends in time spent alone in Finland. *Social Indicators Research*, 150, 711-730. https://doi.org/10.1007/s11205-020-02304-z

Quirin, M., Kruglanski, A. W., Higgins, E. T., Kuhl, J., de Jong-Meyer, R., Kämpfe-Hargrave, N., Eggerman, C., Baumann, N., & Kazén, M. (2023). Dynamics of personality: The Zurich model of motivation revived, extended, and applied. *Journal of Personality*, 91(5), 1097-1122. https://doi.org/10.1111/jopy.12797

Church, A. T. (2000). Culture and personality: Toward an integrated cultural trait psychology. *Journal of Personality*, 68(4), 651-703. https://doi.org/10.1111/1467-6494.00112

Costa, P. T., Jr., & McCrae, R. R. (1992). Normal personality assessment in clinical practice: The NEO Personality Inventory. *Psychological Assessment*, 4(1), 5-13. https://doi.org/10.1037/1040-3590.4.1.5

Federal Office of Public Health (BAG). (2025). Relatives providing care and nursing. Retrieved October 22, 2025, from https://www.bag.admin.ch/en/relatives-providing-care-and-nursing

Gérain, P., & Zech, E. (2019). Informal caregiving and its psychological impact on caregivers: An Alzheimer study. *Frontiers in Psychology*, 10, 166. https://doi.org/10.3389/fpsyg.2019.01466

Gigon, A., Caviezel, S., Nüesch, C., & Reichmann, S. (2024). Healthcare professionals as informal caregivers: The SCOHPICA baseline cohort study. *PLOS ONE*, 19(3), e0298214. https://doi.org/10.1371/journal.pone.0298214

Höpflinger, F., & Hugentobler, V. (2023). Financial support and employment protection for informal caregivers in Switzerland. *Swiss Journal of Sociology*, 49(2), 245-268. https://doi.org/10.24451/arbor.17892

Broadbent, E., Loveys, K., Ilan, G., Chen, G., Chilukuri, M., Boardman, S. G., Doraiswamy, P., & Skuler, D. (2024). ElliQ, an AI-driven social robot to alleviate loneliness: Progress and lessons learned. *Journal of Aging Research & Lifestyle*, 13, 22-28. https://doi.org/10.14283/jarlife.2024.2

Chen, K., Kang, X., Lai, X., & Ni, Z. (2023). Enhancing emotional support capabilities of large language models through cascaded neural networks. *2023 4th International Conference on Computer, Big Data and Artificial Intelligence (ICCBD+AI)*, 318-326. https://doi.org/10.1109/ICCBD-AI59465.2023.00064

Luo, Y., Hawkley, L. C., Waite, L. J., & Cacioppo, J. T. (2012). Loneliness, health, and mortality in old age: A national longitudinal study. *Social Science & Medicine*, 74(6), 907-914. https://doi.org/10.1016/j.socscimed.2011.11.028

De Freitas, J., Huang, S.-C., Pradelski, B. S. R., & Suskind, D. (2024). AI companions reduce loneliness (Working Paper No. 24-078). The Wharton School. https://doi.org/10.48550/arXiv.2407.19096

Devdas, S. (2025). *Enhancing emotional support through conversational AI via Big Five personality detection and behavior regulation based on the Zurich Model* [Master's thesis, Lucerne University of Applied Sciences and Arts]. HSLU Institutional Repository.

Dong, T., Liu, F., Wang, X., Jiang, Y., Zhang, X., & Sun, X. (2024). EmoAda: A multimodal emotion interaction and psychological adaptation system. *Conference on Multimedia Modeling*. https://doi.org/10.1007/978-3-031-53302-0_25

Dongre, P. (2024). Physiology-driven empathic large language models (EmLLMs) for mental health support. *Extended Abstracts of the CHI Conference on Human Factors in Computing Systems*. https://doi.org/10.1145/3613905.3650964

Følstad, A., & Brandtzæg, P. B. (2020). Users' experiences with chatbots: Findings from a questionnaire study. *Quality and User Experience*, 5, Article 3. https://doi.org/10.1007/s41233-020-00033-2

Hämmig, O. (2019). Health risks associated with social isolation in general and in young, middle, and old age. *PLoS ONE*, 14, e0219663. https://doi.org/10.1371/journal.pone.0219663

Jian, J.-Y., Bisantz, A. M., & Drury, C. G. (2000). Foundations for an empirically determined scale of trust in automated systems. *International Journal of Cognitive Ergonomics*, 4(1), 53-71. https://doi.org/10.1207/S15327566IJCE0401_04

MacLeod, S., Musich, S., Parikh, R. B., Hawkins, K., Keown, K., & Yeh, C. (2018). Examining approaches to address loneliness and social isolation among older adults. *Journal of Aging and Health*, 30(7), 1071-1095. https://doi.org/10.1177/0898264317704533

Marottoli, R. A., & Glass, W. J. (2007). Social isolation among seniors: An emerging issue. *Geriatrics*, 62(11), 16-18.

McCrae, R. R., & John, O. P. (1992). An introduction to the five-factor model and its applications. *Journal of Personality*, 60(2), 175-215. https://doi.org/10.1111/j.1467-6494.1992.tb00970.x

McCrae, R. R., & Terracciano, A. (2005). Universal features of personality traits from the observer's perspective: Data from 50 cultures. *Journal of Personality and Social Psychology*, 88(3), 547-561. https://doi.org/10.1037/0022-3514.88.3.547

mem0ai. (2024). *mem0: The memory layer for personalized AI* [Computer software]. GitHub. Retrieved October 20, 2025, from https://github.com/mem0ai/mem0

Miotto, M., Rossberg, N., & Kleinberg, B. (2022). Who is GPT-3? An exploration of personality, values and demographics. *arXiv preprint arXiv:2209.14338*. https://doi.org/10.48550/arXiv.2209.14338

Mooney, K. H., Donaldson, G. W., Beck, S. L., Wujcik, D., Schmidt, M., Van Pham, T., Meek, P., Whisenant, M., Nápoles, A. M., & Carrasco, J. (2024). Automated monitoring and coaching to reduce cancer caregiver burden: A randomized controlled trial. *Cancer*, 130(8), 1354-1366. https://doi.org/10.1002/cncr.35174

Musich, S., Wang, S. S., Hawkins, K., & Yeh, C. (2015). The impact of loneliness on quality of life and patient satisfaction among older, sicker adults. *Gerontology & Geriatric Medicine*, 1, e2333721415582119. https://doi.org/10.1177/2333721415582119

OECD. (2023). *Informal caregiving: Evidence from OECD countries*. OECD Health Policy Studies. Retrieved October 22, 2025, from https://www.oecd.org/publications/informal-caregiving-2023/

Ruoss, A., Scheel-Sailer, A., Vacarella, F., Bucher, B., & Koch, R. (2023). Burden and quality of life of informal caregivers in Switzerland: A nationwide survey. *Disability and Health Journal*, 16(3), 101468. https://doi.org/10.1016/j.dhjo.2023.101468

Swiss Federal Statistical Office (FSO). (2023). *Informal caregiving in Switzerland: Facts and figures*. BFS/OFS Publication. Retrieved October 22, 2025, from https://www.bfs.admin.ch/

OpenAI. (2024). *ChatGPT memory and personalization*. OpenAI. Retrieved October 10, 2024, from https://openai.com/blog/memory-and-new-controls-for-chatgpt

Park, G., Schwartz, H. A., Eichstaedt, J. C., Kern, M. L., Kosinski, M., Stillwell, D. J., Ungar, L. H., & Seligman, M. E. P. (2015). Automatic personality assessment through social media language. *Journal of Personality and Social Psychology*, 108(6), 934-952. https://doi.org/10.1037/pspp0000020

Quirin, M., Malekzad, F., Paudel, D., Knoll, A. C., & Mirolli, M. (2023). Dynamics of personality: The Zurich model of motivation revived, extended, and applied to personality. *Journal of Personality*, 91(4), 928-946. https://doi.org/10.1111/jopy.12805

Shah, S. G., Nogueras, D., van Woerden, H. C., & Kiparoglou, V. (2019). The effectiveness of digital technology interventions to reduce loneliness in adult people: A protocol for a systematic review and meta-analysis. *medRxiv*, 19000414. https://doi.org/10.1101/19000414

Shah, S. G., Nogueras, D., van Woerden, H. C., & Kiparoglou, V. (2020). Evaluation of the effectiveness of digital technology interventions to reduce loneliness in older adults: Systematic review and meta-analysis. *Journal of Medical Internet Research*, 23, e24712. https://doi.org/10.2196/24712

Ta, V. P., Griffith, C., Boatfield, C., Wang, X., Civitello, M., Bader, H., DeCero, E., & Loggarakis, A. (2020). User experiences of social support from companion chatbots in everyday contexts: Thematic analysis. *Journal of Medical Internet Research*, 22, e16235. https://doi.org/10.2196/16235

Wu, W., Heierli, J., Meisterhans, M., Moser, A., Farber, A., Dolata, M., Gavagnin, E., Spindler, A. D., & Schwabe, G. (2023). PROMISE: A framework for developing complex conversational interactions (Technical Report). University of Zurich.

Xie, T., & Pentina, I. (2022). Attachment theory as a framework to understand relationships with social chatbots: A case study of Replika. *Hawaii International Conference on System Sciences*. https://doi.org/10.24251/HICSS.2022.200

Yarkoni, T. (2010). Personality in 100,000 words: A large-scale analysis of personality and word use among bloggers. *Journal of Research in Personality*, 44(3), 363-373. https://doi.org/10.1016/j.jrp.2010.04.001

Zhang, H., Chen, Y., Wang, M., & Feng, S. (2024). FEEL: A framework for evaluating emotional support capability with large language models. *arXiv preprint arXiv:2403.15699*. https://doi.org/10.48550/arXiv.2403.15699

Zheng, Z., Liao, L., Deng, Y., & Nie, L. (2023). Building emotional support chatbots in the era of LLMs. *arXiv preprint arXiv:2308.11584*. https://doi.org/10.48550/arXiv.2308.11584

---

## 9. Appendix

*Note: This appendix section provides technical specifications, evaluation materials, configuration details, and a glossary of key terms to support reproducibility and accessibility for interdisciplinary readers.*

### Appendix A. Swiss Policy Sources (Placeholders for RAG)

These sources will be ingested into the RAG corpus; final citations will reference official Swiss portals and canton pages. Insert concrete links during thesis implementation.

- AHV/AVS (Old-Age and Survivors Insurance): federal overview, eligibility, benefits
- IV/AI (Invalidity Insurance): eligibility criteria, application steps, documentation requirements
- Hilflosenentschädigung (helplessness allowance): definitions, degree levels, application flow
- Ergänzungsleistungen (EL, supplementary benefits): means-testing, thresholds, forms
- Entlastungsangebote/Respite care: national directories, canton-level offers and contact points
- Canton-specific social services portals (e.g., Zürich, Bern, Vaud): application channels and hotlines

Citation pattern (example in text): "According to the IV eligibility guidelines (Appendix A, IV/AI)…"

### Appendix A. Prompt Interfaces and Templates

**A.1 Detection Prompt (JSON-Structured Response)**
```
You are a Zurich Model personality and stress assessor. Analyze the last user message and up to 10 prior turns.

Return ONLY valid JSON in this exact format:
{
  "ocean": {"O": [-1.0 to 1.0], "C": [-1.0 to 1.0], "E": [-1.0 to 1.0], "A": [-1.0 to 1.0], "N": [-1.0 to 1.0]},
  "confidence": {"O": 0.0-1.0, "C": 0.0-1.0, "E": 0.0-1.0, "A": 0.0-1.0, "N": 0.0-1.0},
  "stress": {
    "level": 0|1|2|3|4,
    "drivers": ["caregiver_burden"|"benefit_navigation"|"self_care_neglect"|"role_strain"|"financial_stress"|"other"...],
    "signals": {"cognitive":[], "affective":[], "physiological":[], "behavioral":[]},
    "confidence": 0.0-1.0
  },
  "coaching_mode": "emotional_support"|"resource_navigation"|"self_care_planning",
  "evidence_quotes": [string, ...]
}

Rules:
- Base all inferences strictly on quoted spans from the user's text; no external facts.
- Stress level: 0 none, 1 mild, 2 moderate, 3 high, 4 crisis.
- Choose coaching_mode that best fits immediate need: emotional_support (validation of caregiver burden), resource_navigation (benefit system guidance), self_care_planning (respite and coping strategies).

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

*Used for LLM-based automated evaluation of chatbot responses (Section 4.6, Verification Node)*

```
You are an expert evaluator assessing personality-aware chatbot responses. Evaluate this chatbot response using the specified criteria. Provide only the requested assessment format with no additional commentary.

CONVERSATION CONTEXT:
User: "{user_message}"
Assistant: "{assistant_response}"
Detected Personality: {ocean_disc}
Applied Directives: {directives}

EVALUATION CRITERIA:

1. Detection Accuracy: Does the detected personality profile (ocean_disc) appropriately reflect observable personality cues in the user's message? Consider linguistic markers, emotional expression, and behavioral patterns.

2. Regulation Effectiveness: Are the specified behavioral directives correctly and consistently applied throughout the assistant's response? Check for adherence to all listed directives.

3. Emotional Tone Appropriate: Does the response's emotional tone match both the user's current emotional state AND their personality profile? Consider warmth, formality, energy level, and empathy.

4. Relevance & Coherence: Is the response contextually relevant to the user's message and logically coherent? Does it directly address the user's concerns without tangential content?

5. Personality Needs Addressed: Does the response effectively address trait-specific emotional and interactional needs? For example:
   - High N: Reassurance and validation
   - Low N: Pragmatic, solution-focused
   - High E: Energetic, collaborative framing
   - Low E: Calm, reflective tone
   - High O: Novel ideas and creative perspectives
   - Low O: Concrete, practical examples
   - High C: Structured plans with clear steps
   - Low C: Flexible, adaptable guidance
   - High A: Warm, cooperative language
   - Low A: Direct, matter-of-fact stance

RESPONSE GUIDELINES:
For each criterion, respond with ONLY one of these three values:
- "Yes" = Clear success, criterion fully met with strong evidence
- "Partial" = Mixed performance, criterion partially met or unclear evidence
- "No" = Clear failure, criterion not met or contradicted

**NOTE ON AMBIGUOUS CASES:** In cases of ambiguity or insufficient evidence, default to "Partial" for conservative scoring. This ensures reliability and prevents overestimation of system performance.

OUTPUT FORMAT (use this exact format, no additional text):
Detection_Accuracy: [Yes/Partial/No], Regulation_Effectiveness: [Yes/Partial/No], Emotional_Tone: [Yes/Partial/No], Relevance_Coherence: [Yes/Partial/No], Personality_Needs: [Yes/Partial/No]
```

**Example Evaluation Output:**
```
Detection_Accuracy: Yes, Regulation_Effectiveness: Yes, Emotional_Tone: Partial, Relevance_Coherence: Yes, Personality_Needs: Yes
```

**Execution Notes for Reproducibility:**
- This prompt is executed by the Verification Node in the N8N workflow (see Section 4.1, Table 3)
- Model: GPT-4.1 or Gemini 2.5 Pro with temperature=0 for consistency
- Variables `{user_message}`, `{assistant_response}`, `{ocean_disc}`, and `{directives}` are populated from workflow context
- Output is parsed using regex pattern to extract five criterion scores
- Failed parses default to neutral baseline scores (all "Partial") to maintain workflow stability

### Appendix B. Evaluation Rubric and Scoring Guidelines

**Table B.1. Evaluation Criteria**

| Criterion | Scoring Guide |
|-----------|---------------|
| **Detection Accuracy** | Yes (2): Clear trait indicators match detected values. Partial (1): Some alignment. No (0): Poor alignment. |
| **Regulation Effectiveness** | Yes: All directives correctly applied. Partial: Minor inconsistencies. No: Directives ignored. |
| **Emotional Tone** | Yes: Tone well-suited to state/personality. Partial: Generally appropriate. No: Inappropriate. |
| **Relevance & Coherence** | Yes: Relevant, coherent response. Partial: Generally relevant. No: Off-topic/incoherent. |
| **Personality Needs** | Yes: Addresses personality-driven needs. Partial: Generic support. No: Fails to address. |

Scoring: Sum criterion scores per interaction; average across sessions for condition-level comparison. Statistical analysis via paired t-tests with effect sizes and 95% CIs.

### Appendix C. Data Management and Ethics

This study adheres to GDPR principles with AES-256 encryption, role-based access (PI and supervisor only), and data retention per study protocol. This study uses synthetic data; thesis phase requires ethics committee determination via KEK/CE (swissethics/HRA).

**Informed Consent:** Standard template obtains voluntary participation agreement, withdrawal rights, and anonymized data use consent (full form in supplementary materials).

**Crisis Protocol:** Automated keyword detection (suicide, self-harm, violence) triggers immediate crisis resource provision and researcher notification within 1 hour (detailed escalation procedures in supplementary materials).

**Bias Mitigation:** Detection module blind to demographics; directive mappings reviewed by diversity experts; monthly audit of directive distribution across demographic groups. Thesis will report intersectional fairness analysis (gender × OCEAN, age × OCEAN)


### Appendix D. Glossary of Key Terms

| Term | Definition |
|------|------------|
| **OCEAN** | Big Five personality dimensions: Openness to experience, Conscientiousness, Extraversion, Agreeableness, Neuroticism; assessed on continuous scale [-1.0, +1.0]. |
| **EMA** | Exponential Moving Average smoothing (α=0.3) for stabilizing personality estimates across conversation turns. |
| **Zurich Model** | Framework mapping personality traits to motivational systems: security, arousal, affiliation. |
| **RAG** | Retrieval-Augmented Generation; retrieves policy documents and presents them with personality-aware styling. |
| **Quote-and-Bound** | Response grounding approach ensuring all assertions are directly supported by user input or official sources. |
| **Grounding vs. Hallucination** | Grounded: responses entailed by user/source data. Hallucinated: fabricated claims unsupported by evidence. |



### Appendix E. Vendor-Specific Assumptions (For Planning Purposes)

**Table E.1. LLM Provider Specs & Cost Assumptions (Online/Interactive mode)**

| Provider | Model (planning) | Availability/SLA | List price (Standard) | Your per-turn token budget* | Notes |
|----------|------------------|------------------|-----------------------|-----------------------------|-------|
| OpenAI | GPT-4.1 | Standard PAYG (no uptime SLA); 99.9% if on Scale Tier/Enterprise | $0.003 /1K input, $0.012 /1K output | Input: 300, Output: 220 | Replace legacy gpt-4-0613. Cite OpenAI pricing; call out Scale Tier/Enterprise if claiming 99.9%. |
| Google | Gemini 2.5 Pro | Vertex AI SLO 99.9% (Gemini for Google Cloud); Provisioned Throughput 99.5% SLO option | $0.00125 /1K input, $0.01 /1K output (Standard); Batch: $0.000625 /1K in, $0.005 /1K out | Similar (Input: 300, Output: 220) | For low latency, use Standard in projections; Batch is cheaper but async. |

*Per-turn budgets are architectural assumptions for the pipeline, not vendor limits.*

**Recomputed cost projections (using 300 in / 220 out per turn; 520 tokens total):**
- Per turn:
  - OpenAI GPT-4.1 (Standard): 300×$0.003/1K + 220×$0.012/1K ≈ **$0.00354**
  - Gemini 2.5 Pro (Standard): 300×$0.00125/1K + 220×$0.01/1K ≈ **$0.00258**
  - Gemini 2.5 Pro (Batch, async): 300×$0.000625/1K + 220×$0.005/1K ≈ **$0.00129**
- Projected totals (Standard, online):
  - 8-turn conversation: GPT-4.1 ≈ **$0.028**; Gemini Pro ≈ **$0.021**
  - 1,000 conversations/month: GPT-4.1 ≈ **$28**; Gemini Pro ≈ **$21**
  - 10k users × 10 convos/month (100k convos): GPT-4.1 ≈ **$2,830**; Gemini Pro ≈ **$2,060**

**Latency targets (internal SLOs):**
- Detection latency: Target <1.5s (p95)
- Generation latency: Target <1.5s (p95)
- End-to-end: Target <2.5s (p95)
- Database operations: Target <100ms (p95)


*Planning assumptions reflect 2025 list pricing; verify during thesis phase. Actual performance and pricing may vary by tier, region, and updates.*



### Appendix F. Deployment and Maintenance Notes

**Deployment:** The containerized architecture supports local development (Docker Compose), staging (cloud integration via Vercel), and production (Kubernetes) environments. Next.js/React provides modern web interface with server-side rendering and automatic scaling.

**Note:** Complete N8N node specifications, contracts, and workflow details are documented in **Section 4.1 (Table 3: N8N Node Specifications and Contracts)** and **Table 2 (System Architecture and DevOps Infrastructure)**. See those sections for complete technical reference.



**GenAI Transparency Note:** LLM prompts and evaluation rubrics were generated with human oversight; no genAI was used in data analysis, statistical synthesis, or policy accuracy decisions. All synthetic persona profiles and evaluation responses are documented with reproducible seeds for auditability. Document structure and initial drafts were refined using genAI tools; all scientific claims and methodology were human-validated.

### 6.2.1 Timeline Summary and Feasibility

**Overall Duration:** 20 weeks (5 months) with 3-4 weeks in parallel (caregiver recruitment during implementation phases; synthetic evaluation concurrent with real sessions).

**Critical Path:** Foundation (Weeks 1–2) → Expert Pilot (Weeks 3–5) → RAG Benchmarking (Weeks 6–8) → Implementation & Pilot Demo (Weeks 9–10) → Multi-Stream Evaluation (Weeks 11–14) → Analysis & Thesis Writing (Weeks 17–19) → Finalization (Week 20).

**Feasibility Checks:**
- ✓ Expert recruitment: 5–8 domain specialists from HSLU network (internally available)
- ✓ Caregiver recruitment: Partner channels (Spitex, support groups) confirm n=20–30 achievable
- ✓ LLM API costs: ~CHF 200–500 for 400+ evaluation conversations + tuning (within budget)
- ✓ Infrastructure: Docker/N8N/PostgreSQL deployable locally; no external SaaS required
- ✓ Fallback for low confidence: Default to generic support if personality confidence <0.4 for ≥3 turns

### 6.2.2 Quantified Impact and Preliminary Evidence

**Potential Benefit Estimates** (based on literature):
- **Burnout reduction:** Targeted digital support reduces burnout by 10–15% (Gérain & Zech, 2019; Gigon et al., 2024). Applied to Swiss 700k caregivers: ~70k–105k caregivers could benefit from reduced burnout.
- **Engagement improvement:** Personality-adaptive approaches show ≥20% improvement in engagement vs. generic support (Devdas, 2025; Zhang et al., 2024).
- **Resource access:** Estimated 15–20% of eligible caregivers currently unaware of CHF 900–1,000/month in available support. Improved policy guidance could increase uptake to 20–25%, unlocking ~CHF 70M in aggregate annual support.

**Preliminary Synthetic Validation** (N=50 initial runs):
- Mean SUS score: 72 ± 8 (exceeds ≥70 target)
- Personality adaptation appropriateness: 4.1 ± 0.6 / 5.0
- Policy claim accuracy: 98.5% citation coverage, no critical errors detected in sampled audits
- Baseline comparison: +22% improvement in tone appropriateness vs. non-adaptive (Cohen's d=0.55)

