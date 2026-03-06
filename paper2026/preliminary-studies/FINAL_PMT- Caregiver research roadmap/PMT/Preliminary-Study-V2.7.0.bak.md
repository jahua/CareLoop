# Adaptive LLM-Based Chatbot with Personality-Aware Dialogue for Human-Centered Applications: A Formal Preliminary Study with Swiss Caregiver Focus

**Author:** Jiahua Duojie  
**Program:** MSc Applied Information and Data Science (HSLU)  
**Supervisor:** Prof. Dr. Guang Lu  
**Secondary Supervisor/Advisor:** Samuel Devdas  
**Date:** October 22, 2025  
**Version:** 2.7.0 (Integrated Caregiver Research Roadmap)

---

### Changelog (2.7.0)
- Full integration of Master Thesis Caregiver Research Roadmap into preliminary study framework
- Expanded Swiss caregiver context with prevalence, challenges, and policy landscape
- Detailed four research gaps specific to informal caregiving
- Enhanced use case with three personality-tailored coaching modes: Emotional Support, Resource Navigation, Self-Care Planning
- Integrated RAG-based Swiss benefits navigation (AHV, IV, Hilflosenentschädigung) as production goal
- Expanded six-objective research framework addressing caregiver-specific needs
- Added comprehensive evaluation framework with caregiver-centered outcome metrics
- Integrated risk management with caregiver recruitment and technical deployment challenges
- Enhanced timeline with caregiver pilot phases and longitudinal tracking protocols
- Success criteria now include user-centered caregiver outcomes (SUS, burden reduction, benefit navigation)

---

## Abstract

Emotional well-being and personalization remain persistent challenges in human-centered AI, particularly for vulnerable populations such as informal caregivers who face chronic stress, compassion fatigue, and complex healthcare navigation requirements. While conversational AI systems achieve scalability, generic assistants rarely adapt to individual personality differences or domain-specific needs, limiting their capacity to provide context-appropriate support. This preliminary study specifies a modular, workflow-orchestrated architecture for personality-aware dialogue that integrates Big Five (OCEAN) personality detection with Zurich Model–aligned behavioral regulation under strict dialogue grounding constraints, specifically instantiated for **Swiss informal caregivers** (approximately 700,000 individuals, representing 8% of the population) who face emotional burden, federalized healthcare policy navigation complexity, and systematic self-care neglect.

We extend detect→regulate→generate with temporal stability, reproducibility, cross-domain reusability, and caregiver-specific needs assessment. Contributions: (1) EMA smoothing with confidence-aware filtering for stable per-turn traits; (2) configurable policy packs enabling domain transfer via configuration; (3) audit-ready contracts (JSON schemas, version locks, per-turn logs); (4) integration of factual memory with motivational modeling; (5) **planned RAG-enhanced generation for Swiss caregiver policy navigation** (AHV, IV, Hilflosenentschädigung, Spitex services, cantonal variations); and (6) human-centered interface usable as research instrument. All metrics and thresholds are targets for thesis-phase validation with n=30-50 Swiss caregiver participants.

We instantiate the **Swiss Caregiver Coaching Assistant** with three personality-tailored modes (Emotional Support for compassion fatigue and role strain; Resource Navigation for Swiss benefits and policy guidance; Self-Care Planning for respite and coping strategies) informed by Switzerland's 700,000+ informal caregivers and the 40-70% experiencing burnout. The evaluation plan covers detection validity and stability, regulation/tone quality, coherence and relevance, policy guidance accuracy, system reliability, and caregiver-centered outcomes (System Usability Scale ≥75, perceived helpfulness ≥4.0/5.0, sustained engagement ≥60% retention, Caregiver Burden Inventory reduction ≥10%).

Reading guide: Section 1 motivates and situates the work in the Swiss caregiver context; Section 2 defines the scope and primary use case; Section 3 states the research questions and links them to objectives; Section 4 details methodology and architecture; Sections 5–6 cover technology and the project plan; Sections 7–8 outline future work and references; the Appendix provides prompts, evaluation rubrics, and source placeholders.

---

## 1. Background: General Framework and Swiss Caregiver Context

### 1.1 Problem Context: The Need for Personality-Aware Human-Computer Interaction

The rapid rise of AI-driven systems has shifted user expectations toward personalized, context-aware dialogues that adapt to individual personality traits, communication preferences, and situational needs, moving beyond transactional interactions. This transformation spans critical application domains—workplace productivity and wellbeing, education and skill development, customer service, and healthcare—where users increasingly expect systems to understand not merely task requirements but also personal preferences, emotional states, and motivational patterns.

**The capacity crisis in traditional support systems.** Traditional human-delivered support faces three structural constraints: limited scalability (practitioners serve limited client loads, creating waitlists and access barriers), financial barriers (professional counseling and coaching services often require substantial out-of-pocket costs that restrict accessibility), and geographic limitations (requiring physical proximity or specific time zones). Meanwhile, digital alternatives such as rule-based chatbots and FAQ systems achieve scalability but deliver one-size-fits-all responses that cannot adapt beyond predefined scripts (Adamopoulou & Moussiades, 2020), ignoring individual personality differences and context-specific needs. This creates a critical gap: systems combining digital scalability with personalized, adaptive interaction.

**Swiss informal caregiver crisis: Context and urgency.** Switzerland has approximately **700,000 informal caregivers** (8% of population), representing one of the nation's largest vulnerable populations [ZHAW Institute of Nursing, 2022]. **Professional training and competency gaps:** Unlike formal healthcare workers, these family caregivers typically lack systematic professional training, evidence-based caregiving techniques, or ongoing clinical supervision, leaving them to learn through trial-and-error in high-stakes caregiving situations. This professional training gap creates urgent needs for accessible, evidence-based practical guidance on caregiving techniques, emotional regulation strategies, crisis management protocols, and self-care practices adapted to their unique contexts and personality profiles. **Stress, burnout, and performance impact:** Informal caregivers face chronic stress from prolonged caregiving responsibilities (avg. care intensity: 25-40 hours/week), leading to elevated burnout rates (40-70% report significant burnout symptoms), emotional exhaustion, secondary traumatic stress, compassion fatigue, guilt, and isolation. These stress and negative mood states directly impair caregiving performance, decision-making quality, patient safety, and ability to provide consistent care, creating a vicious cycle where decreased performance increases guilt and stress, further deteriorating both caregiver wellbeing and care quality.

Beyond emotional challenges, Swiss caregivers navigate a complex, federalized healthcare system with strong cantonal variations (26 cantons = 26 regulatory frameworks). Yet most caregivers remain unaware of their rights under Swiss law, available financial support mechanisms (cantonal allowances averaging CHF 900–1,000 monthly support potential; Höpflinger & Hugentobler, 2023), employment protection regulations, and healthcare system navigation strategies. Many caregivers experience reduced working hours (avg. 8.4h/week reduction) without accessing support mechanisms that could mitigate financial strain.

**Domain-specific requirements and the personalization gap for caregivers.** Informal caregivers require personality-adaptive support across: (1) **Emotional resilience** (compassion fatigue recognition, stress validation, boundary-setting—especially critical for high-neuroticism caregivers), (2) **Practical education** (caregiving techniques, time management, self-care strategies adapted to individual learning and processing styles), and (3) **Swiss healthcare policy navigation** (cantonal Spitex variations, IV/AI eligibility, Hilflosenentschädigung application, Ergänzungsleistungen, caregiver employment models). Current digital assistance solutions—generic stress management apps, FAQs without personality awareness, generic policy information portals—fail to account for individual differences, creating systematic mismatches that reduce effectiveness and undermine caregiver trust.

### 1.2 Limitations of Current Digital Assistants and Caregiver Support Systems

We synthesize four interconnected technical and domain-specific constraints limiting current conversational AI effectiveness for caregiver support:

**Gap 1: Lack of Dynamic Personality-Aware Adaptation**  
Existing systems employ static, rule-based personalization that ignores individual OCEAN personality traits and Zurich Model motivational states, resulting in suboptimal engagement and effectiveness. Current caregiver support applications lack validated personalization frameworks and do not model individual personality differences, producing inconsistent user experiences. Furthermore, the field lacks standardized evaluation protocols or longitudinal tracking to assess technical performance and user acceptance of personality-adaptive interventions, hindering reproducibility and meta-analysis.

**Gap 2: Zurich Model Theory-Practice Disconnect**  
Recent industry deployments (ChatGPT Memory, mem0, LangChain Memory) prioritize memory-centric personalization, storing user statements as vector embeddings for similarity-based retrieval across sessions. While achieving factual persistence at scale, **this approach remains cognitively shallow**, addressing *what the user said* but not *why they behave*. Memory systems recall that a caregiver mentioned "mother has dementia" but cannot infer whether that caregiver's preference for structured planning stems from high conscientiousness (organizational drive), neuroticism (need for security), or both—leading to generic responses that miss underlying motivational drivers. No validated computational mappings translate Zurich Model of Social Motivation constructs into behavioral directives; measurement protocols to confirm intended motivational state induction remain undeveloped. The field lacks manipulation checks to confirm that adapted responses are perceived as intended by users.

**Gap 3: LLM Safety, Reliability, and Privacy in Healthcare**  
Most systems lack comprehensive logging, audit trails, and deterministic interfaces preventing rigorous evaluation. Caregiver support systems particularly lack standardized outcome measures or longitudinal tracking to assess effectiveness. Critical deficiencies exist in truthfulness, persona stability, and privacy preservation for vulnerable caregiver populations. No privacy-preserving architectures meet Swiss data protection standards (FADP, rev. 2023) while enabling effective personality tracking.

**Gap 4: Absence of Personalized Education and Swiss Healthcare Navigation**  
No comprehensive caregiver support systems currently exist that integrate: (1) personalized practical education on caregiving techniques adapted to individual OCEAN personality profiles, and (2) LLM-based navigation of complex Swiss healthcare policies and regulations tailored to caregiver needs. While personality adaptation is essential for emotional support and educational guidance, the navigation of policies and regulations is fundamentally important functionality that does not necessarily require OCEAN trait adaptation—instead, it requires accurate, contextualized information delivery. This gap is particularly acute in Switzerland's federalized system where caregivers require guidance on cantonal variations in Spitex services, caregiver allowances, long-term care insurance (Pflegeversicherung), family caregiver employment models, patient rights, and culturally appropriate Swiss interaction patterns. Current digital health interventions, when they exist, provide only generic information without personality adaptation or Swiss-specific contextualization.

### 1.3 Motivation and Contributions: Addressing Caregiver-Specific Gaps

Despite growing interest in personality-aware conversational AI and digital caregiver support, **no existing system systematically integrates**: (1) continuous personality detection and regulation, (2) caregiver-specific emotional support and resilience-building, (3) personality-adapted practical caregiving education, and (4) accurate Swiss healthcare policy navigation—all grounded in validated personality science and Swiss regulatory context.

**Research Motivation and Expected Impact:**

While informal caregivers face documented stressors, existing digital support systems lack personality-adaptive emotional support and Swiss-specific healthcare knowledge navigation. This research develops a personality-aware chatbot providing: (1) emotional support tailored to individual personality profiles, and (2) accurate navigation of complex Swiss healthcare policies. Three key opportunities motivate this work:

- **Scaling personalized support without scaling costs:** Continuous personality adaptation enables digital systems to deliver individualized caregiver support that matches human practitioners' empathy and responsiveness, addressing Switzerland's caregiver capacity crisis while maintaining accessibility and affordability.
- **Building caregiver trust through psychological validity:** Grounding adaptations in validated personality science (Big Five, Zurich Model) and Swiss healthcare accuracy ensures that systems respond to genuine caregiver psychological needs and practical requirements, increasing acceptance and long-term engagement.
- **Enabling Swiss healthcare organizations' adoption through reliability:** Providing reproducible evaluation protocols, audit trails, deterministic interfaces, and caregiver-centered outcomes addresses organizational requirements (Spitex services, cantonal health departments, employee assistance programs) for quality assurance, compliance, and evidence-based deployment.

Recent work by Devdas (2025) provides crucial empirical validation, demonstrating substantial performance gains through personality-adaptive assistants in controlled simulations using Big Five detection and Zurich Model regulation. This establishes the conceptual foundation—that personality-aware regulation meaningfully improves conversational quality—motivating production-ready, Swiss-contextualized system architectures.

By systematically addressing these four interconnected gaps, this research establishes a new paradigm for **theoretically grounded, personality-aware, safe, and contextually appropriate AI applications in informal caregiving**, with specific contributions to Switzerland's 700,000+ caregivers and broader implications for global caregiver support systems.

**This preliminary study specifies six key objectives addressing caregiver-specific research gaps, aligned with the Master Thesis Research Roadmap:**

**Table 1. Six Research Objectives Addressing Caregiver Gaps**

|| Objective | Description | Caregiver-Specific Focus |
||-----------|-------------|-------------------------|
|| (1) Dynamic Personality-Aware Adaptation | Develop and validate OCEAN detection with real-time adaptation outperforming static approaches | Tailor emotional support intensity to caregiver neuroticism; resource navigation detail to conscientiousness |
|| (2) Zurich Model Operationalization | Create validated mappings from OCEAN to behavioral directives with manipulation checks | Confirm caregivers perceive security/arousal/affiliation framing as intended; measure stress reduction |
|| (3) LLM Safety and Swiss Privacy Compliance | Design privacy-preserving architecture meeting Swiss FADP with persona stability and hallucination guardrails | Protect caregiver anonymity; ensure policy guidance factual accuracy; prevent fabricated Swiss benefits |
|| (4) Caregiver-Specific Emotional Support | Develop resilience-building, compassion fatigue recognition, boundary-setting strategies with personality adaptation | High-N: reassurance + grounding; Low-N: pragmatic solutions; All: caregiver-specific stress drivers |
|| (5) Personalized Caregiving Education | Create practical education (techniques, time management, self-care) adapted to individual learning styles | High-C: detailed step-by-step; Low-C: flexible overview; High-O: novel approaches; Low-O: proven methods |
|| (6) Swiss Healthcare Policy Navigation | Develop RAG-enhanced system for cantonal Spitex, IV/AI, Hilflosenentschädigung, allowances, employment models | Contextualized guidance per canton; eligibility checklists; application step-by-step support; contact information |

---

## 2. Topic Definition

### 2.1 Core Concepts

**Personality-adaptive emotional support chatbot.** A conversational agent that dynamically detects user personality signals from dialogue content and accordingly modulates its communicative behavior—including tone, structural complexity, pacing, warmth, and novelty—to better satisfy user-specific emotional and psychological needs. Unlike static systems that rely on predetermined user profiles, personality-adaptive chatbots continuously update their understanding of user traits and adjust their responses in real time to optimize emotional alignment and therapeutic effectiveness.

**Big Five (OCEAN) personality framework.** A well-established personality taxonomy comprising five major dimensions: **O**penness to experience (curiosity, creativity), **C**onscientiousness (organization, discipline), **E**xtraversion (sociability, energy), **A**greeableness (cooperation, empathy), and **N**euroticism (emotional sensitivity, stress reactivity) (McCrae & John, 1992). This framework provides a structured basis for personality inference and has been extensively validated across cultures and contexts. In our implementation, we employ **continuous per-turn inference with values in the range [−1.0, +1.0]** representing the full spectrum from low to high trait expression. This continuous representation is essential for (i) Exponential Moving Average (EMA) smoothing—a weighted averaging technique requiring fine-grained values to prevent quantization noise (abrupt jumps from discrete values), (ii) capturing motivational intensity as conceptualized by the Zurich Model, and (iii) enabling nuanced behavioral adaptations that match the dimensional nature of personality traits established by personality psychology research (Costa & McCrae, 1992; Quirin et al., 2023).

**Zurich Model alignment.** Our personality-to-behavior mapping approach is grounded in the Zurich Model of Social Motivation (Quirin et al., 2023), which conceptualizes human behavior through three fundamental motivational systems: security, arousal, and affiliation. We operationalize this framework by mapping OCEAN traits to these motivational domains: Neuroticism influences security-related behaviors (comfort provision vs. stability reassurance), Openness and Extraversion modulate arousal through novelty and energy regulation, and Agreeableness affects affiliation through warmth and collaborative stance adjustments. Conscientiousness serves as a structural modifier, influencing the organization and specificity of guidance provided. *Note: This operationalization represents a simplified first-order mapping; the Zurich Model emphasizes dynamic interactions between motivational systems (Quirin et al., 2023), which are not fully captured in this preliminary design and require empirical validation in the thesis phase.*

**Safety constraints.** All system responses are designed to be grounded in user conversational input (see Section 4.4 for quote-and-bound implementation details).

### 2.2 Scope and Application Context

**Human-centered applications.** Our framework targets applications emphasizing personalization, empathy, and adaptive user interaction across diverse domains: family caregiver support, mental health services, educational assistance, customer service interactions, and general emotional companionship. We designed the system to complement human interaction by providing consistent availability, emotional attunement, and personality-aware responses. The system maintains appropriate boundaries and escalation mechanisms when professional human intervention is needed.

**Domain prioritization rationale.** Family caregiver coaching was prioritized over clinical mental health applications due to: (1) strong alignment with Zurich Model motivations (security for managing care responsibilities and financial stress, affiliation for family dynamics and social support, arousal for goal-setting and advocacy), (2) urgent public health need (Switzerland's aging population creates growing caregiver burden with limited digital support infrastructure), (3) clear policy integration opportunity (navigating AHV, IV, Hilflosenentschädigung, respite care services), (4) lower ethical and regulatory risks (non-clinical coaching boundary avoids medical device regulations while addressing wellbeing), and (5) measurable outcomes (caregiver stress reduction, benefit system navigation success, self-care adoption, sustained engagement).

**Technical scope.** The system integrates personality-aware dialogue with RAG-augmented policy navigation for Swiss caregiver benefits (AHV, IV, Hilflosenentschädigung, Ergänzungsleistungen, respite care programs). The RAG module retrieves relevant policy documents and eligibility criteria based on caregiver context, while the personality-aware regulation determines presentation style (detailed vs. summary, reassuring vs. pragmatic). The system implements a webhook-based N8N architecture for production deployment. The preliminary study focuses on personality detection and regulation mechanisms; RAG integration and multimodal inputs are planned for thesis implementation phase (Weeks 7-10).

**Evaluation framework.** Our assessment methodology employs a structured rubric examining five key dimensions: detection accuracy (how well inferred OCEAN traits match user personality cues), regulation effectiveness (appropriate application of trait-specific behavioral strategies), emotional tone appropriateness (alignment with user emotional state and personality), relevance and coherence (contextual appropriateness and logical consistency), and personality needs satisfaction (addressing trait-specific emotional and interactional requirements) (Devdas, 2025; Zhang et al., 2024).

### 2.3 Implementation Specifications

**LLM model selection.** We employ OpenAI GPT-4.1 as the primary model for personality detection and response generation, with Gemini 2.5 Pro as a cost-effective alternative. GPT-4.1 offers structured JSON output via function calling and strong personality inference capabilities validated in prior work (Miotto et al., 2022). We set temperature to 0.3 for detection (consistency) and 0.7 for generation (creativity with reliability). The provider-agnostic JSON contracts enable seamless model swapping for evaluation, cost optimization, and robustness. Vendor-specific details are in Appendix E (planning assumptions).

**Dataset for OCEAN detection training.** The system uses **zero-shot prompt-based inference** rather than fine-tuned models. This leverages GPT-4's pre-trained understanding of personality psychology. We engineer prompts based on established personality assessment instruments (NEO-PI-R, BFI-2) and linguistic markers validated in prior work (Yarkoni, 2010; Park et al., 2015). For evaluation and validation, we employ three approaches: (1) **synthetic personality profiles** generated via simulated user agents with extreme (±0.8) and mixed trait configurations, (2) **scripted dialogue scenarios** covering Swiss caregiver stress contexts (emotional burden, benefit navigation complexity, self-care neglect), and (3) **human validation subset** (planned for thesis phase) with 30-50 Swiss family caregiver participants completing self-report personality inventories (BFI-44) for ground-truth comparison.

**Evaluation metrics and target thresholds.** The system targets the following performance benchmarks:

**Evidence Map: Validation Status**

| Claim Type | Evidence Status | Validation Plan |
|------------|-----------------|-----------------|
| **Architecture specifications** | Design complete | Implementation in thesis Weeks 7-10 |
| **EMA parameters (α=0.3)** | Theory-derived | Empirical validation in thesis Weeks 11-14 (N≥250) |
| **Performance thresholds** | Target hypotheses | Human validation in thesis Weeks 15-16 (n=30-50) |
| **Cross-domain reusability** | Design claim | Timed experiments in thesis Weeks 8-10 |

**Table 2. Evaluation Metrics and Target Thresholds**

| Metric | Target Threshold | Measurement Method |
|--------|:----------------:|-------------------|
| **Detection Accuracy** | ≥75% trait alignment | Correlation between inferred and ground-truth OCEAN scores (r ≥ 0.75) |
| **Temporal Stability** | Variance < 0.15 | Standard deviation of trait estimates after turn 6 |
| **Confidence Calibration** | ≥85% alignment | High-confidence predictions (≥0.7) match personality cues in 85%+ cases |
| **JSON Contract Compliance** | ≥99.5% | Percentage of valid JSON outputs from detection/generation modules |
| **Tone Appropriateness** | ≥80% evaluator rating | LLM evaluator scores on 5-point Likert scale (≥4.0/5.0) |
| **Needs Satisfaction** | ≥20% improvement vs. baseline | Relative gain on personality-specific needs addressed |
| **System Reliability** | 100% graceful fallback | Zero unhandled exceptions; all errors trigger neutral responses |

*Note: Thresholds informed by prior conversational AI evaluation studies (Zhang et al., 2024; Devdas, 2025) and personality assessment reliability standards (Costa & McCrae, 1992). These represent hypothesized success criteria to be empirically validated in thesis phase with N≥250 simulated conversations and n=30-50 human participants.*

**Temporal smoothing parameters.** EMA smoothing employs α (alpha) = 0.3, the smoothing factor weighting 30% current observation and 70% historical average. This balances responsiveness to new evidence with stability from past assessments. The α=0.3 selection aligns with personality psychology literature suggesting trait stability emerges after 5-10 behavioral observations (Costa & McCrae, 1992), targeting convergence within 6-8 turns. Confidence thresholds—0.4 (minimum for trait updates) and 0.7 (high-confidence for aggressive adaptation)—are informed by personality assessment reliability standards where correlation r≥0.7 indicates acceptable validity (Park et al., 2015). These parameters represent theoretically grounded hypotheses to be empirically validated against human ground-truth data (BFI-44) in the thesis phase, with sensitivity analysis (α ∈ {0.1, 0.2, 0.3, 0.4, 0.5}) planned as Experiment E2.

### 2.4 Primary Use Case: Swiss Caregiver Coaching Assistant

**Target population and context.** This thesis focuses on the **Swiss Caregiver Coaching Assistant** supporting approximately 700,000 family caregivers managing eldercare, chronic illness, disability care, and dementia care in Switzerland. The assistant helps users:
- **Navigate emotional burden:** Validate stress, recognize compassion fatigue, assert healthy boundaries, sustain motivation
- **Access practical support:** Learn evidence-based caregiving techniques, time management, self-care strategies, respite planning
- **Understand Swiss healthcare policies:** Navigate cantonal Spitex variations, IV/AI eligibility, Hilflosenentschädigung, Ergänzungsleistungen, caregiver employment models, patient rights, advance directives

This use case is selected for: (i) **urgent public health need** (700,000+ Swiss caregivers, 40-70% experiencing burnout with limited digital support infrastructure); (ii) **strong alignment with motivational framework**—security needs (financial stability, care responsibility assurance), affiliation needs (family dynamics, social support), arousal needs (goal-setting, advocacy); (iii) **clear policy integration opportunity** (navigating 26-canton federalized system); (iv) **minimal regulatory risk** (non-clinical coaching boundary avoids medical device regulations while addressing wellbeing); (v) **measurable outcomes** (caregiver stress reduction, benefit navigation success, self-care adoption, sustained engagement, policy comprehension).

**Three personality-tailored coaching modes:**

1. **Emotional Support & Resilience Building**
   - **Purpose:** Validate caregiver burden and role strain; help process emotions; develop coping strategies
   - **Personality Adaptation:**
     - **High-N caregivers:** Extra reassurance and normalization ("Many caregivers feel overwhelmed—this is completely understandable and valid")
     - **Low-N caregivers:** Pragmatic acknowledgment ("You're managing significant responsibilities with limited support")
     - **High-A caregivers:** Collaborative, warm framing with relationship emphasis
     - **Low-A caregivers:** Direct, matter-of-fact stance respecting autonomy
   - **Content:** Compassion fatigue recognition, guilt reframing, boundary assertion, stress validation

2. **Resource Navigation & Swiss Healthcare Policy Guidance**
   - **Purpose:** Help caregivers understand and access Swiss benefits, services, and support systems
   - **Personality Adaptation:**
     - **High-C caregivers:** Detailed step-by-step eligibility checklists, required documentation lists, application timelines, clear procedures
     - **Low-C caregivers:** Concise eligibility summaries, direct canton contacts, optional depth, flexibility emphasized
     - **High-O caregivers:** Mention emerging support models, creative respite solutions, innovation opportunities
     - **High-A caregivers:** Collaborative language ("Let's explore your eligibility together")
     - **High-N caregivers:** Reassuring framing ("Many caregivers successfully navigate this; here's support available")
   - **Content (RAG-Enhanced):** 
     - **Swiss Federal Benefits:** AHV/AVS (Old-Age Insurance), IV/AI (Invalidity Insurance), Hilflosenentschädigung (helplessness allowance)
     - **Supplementary Programs:** Ergänzungsleistungen (supplementary benefits), canton-specific caregiver allowances
     - **Services:** Spitex navigation (service explanation, coverage, respite care options, costs), care coordination
     - **Employment:** Caregiver leave policies, employment protection, reduced work models
     - **Healthcare System:** Patient rights, advance directives, long-term care insurance (Pflegeversicherung)
   - **Canton-Specific Variations:** Zurich, Bern, Geneva, Vaud, St. Gallen, and other major cantons with documented program differences

3. **Self-Care Planning & Respite Strategies**
   - **Purpose:** Develop sustainable coping and respite plans; prevent burnout escalation
   - **Personality Adaptation:**
     - **High-E caregivers:** Emphasize social support mobilization (caregiver support groups, family coordination meetings, peer networks)
     - **Low-E caregivers:** Focus on individual restoration (micro-breaks, boundary-setting scripts, solitude time, journaling)
     - **High-C caregivers:** Structured respite planning with timelines and contingencies
     - **Low-C caregivers:** Flexible self-care suggestions with light scaffolding
   - **Content:** Micro-rest protocols (5-minute breaks, grounding exercises), delegation scripting, backup care planning, technology aids for caregiving, financial planning

**RAG-Augmented Swiss Policy Guidance (Thesis Implementation Phase, Weeks 7-10):**

The system integrates Retrieval-Augmented Generation for accurate, grounded Swiss healthcare policy information:

1. **Policy Corpus Preparation:** Curate vector database of official Swiss policy documents (SSN, Spitex associations, cantonal health departments, IV/AI official guidelines, Ergänzungsleistungen regulations)
2. **Context Extraction:** Parse caregiver situation from conversation (care recipient age/condition, caregiving hours, financial situation, canton, prior benefit applications)
3. **Retrieval Pipeline:** Query policy corpus using semantic similarity to extract top-3 most relevant sections with eligibility criteria, application procedures, contact information
4. **Personality-Aware Presentation:** Adapt retrieved policy content based on OCEAN directives:
   - **High-C:** Structured checklists with timelines and documentation lists
   - **Low-C:** Summary overview with direct contact and optional depth
   - **High-N:** Reassuring framing + step-by-step support
   - **High-O:** Mention alternative programs and creative solutions
   - **High-A:** Collaborative, supportive language
5. **Grounding Enforcement:** All policy guidance must cite specific documents ("According to IV eligibility guidelines for care recipients with dementia…"); no invented procedures or criteria

**Evidence-Based Techniques:** Integrates caregiver-specific CBT strategies (guilt/resentment reframing, role boundary clarification, behavioral activation), respite planning, delegation scripting, and micro-rest protocols (5-minute breaks, box breathing, 5-4-3-2-1 sensory grounding).

**Safety Boundaries:** Non-clinical coaching scope; no medical advice, diagnosis, or crisis intervention beyond referral. Clear disclaimers that system complements but does not replace professional caregiver support programs, Spitex services, or mental health care. Crisis escalation protocol: automated detection of suicidal ideation or self-harm triggers immediate crisis resource provision and researcher notification.

---

## 3. Research Questions
Building on the background and scope, we now articulate the research questions that drive the evaluation and implementation.

### 3.1 Primary Research Question

How can personality-aware dialogue systems support Swiss family caregivers in managing emotional burden, navigating benefit systems, and sustaining self-care through adaptive coaching strategies grounded in the Big Five and Zurich Model frameworks?

This use-case-driven research question addresses the design, implementation, and evaluation of a personality-adaptive caregiver coaching system, encompassing: (1) **domain-specific needs assessment** (caregiver stress profiles, benefit navigation challenges, self-care barriers), (2) **technical implementation** (EMA-based personality detection, RAG-augmented Swiss policy guidance, personality-to-directive mapping for caregiver contexts), (3) **user-centered outcomes** (stress reduction, benefit navigation success, self-care adoption, system usability), and (4) **empirical validation** (demonstrating measurable improvements in caregiver wellbeing and resource access versus non-adaptive baselines).

### 3.2 Sub-Research Questions (Scoped for Swiss Caregiver Coaching)

**RQ1 - Caregiver-Specific Detection:** Can continuous OCEAN inference with EMA smoothing (α=0.3) achieve stable, confidence-weighted personality estimates for family caregivers within 6–8 turns across diverse caregiving contexts (eldercare, chronic illness, disability)? Target measurement: trait variance σ_T <0.15 over 5-turn windows and Pearson correlation r≥0.75 against ground-truth profiles from Swiss caregiver sample (thesis phase validation, n=30-50).

**RQ2 - Caregiver Coaching Effectiveness:** Do intensity-scaled directives mapped to three caregiver coaching modes (Emotional Support, Resource Navigation, Self-Care Planning) improve caregiver stress management, benefit navigation confidence, and self-care adoption versus non-adaptive baseline? Target: ≥20% improvement on caregiver-specific outcomes (stress reduction, navigation success, self-care frequency) via paired t-test (Cohen's d≥0.5) with Swiss caregiver participants.

**RQ3 - RAG-Enhanced Policy Navigation:** Does RAG-augmented Swiss policy guidance (AHV, IV, Hilflosenentschädigung, respite care) combined with personality-aware presentation (detailed vs. summary, reassuring vs. pragmatic) improve benefit system comprehension and application success versus generic information provision? Target: ≥30% improvement in benefit eligibility understanding and application initiation rates.

**RQ4 - Use-Case Outcome Metrics:** Does the system achieve acceptable user-centered performance on: (a) **System Usability Scale (SUS)** ≥75, (b) **Perceived Helpfulness** ≥4.0/5.0 (caregiver-rated), (c) **Sustained Engagement** ≥60% return rate over 4 weeks, (d) **Caregiver Burden Inventory (CBI)** reduction ≥10% over 8-week intervention period? Measured via Swiss caregiver participant study (thesis phase, n=30-50).

**RQ5 - Generalization and Limitations:** How do results vary between caregiver profiles (eldercare vs. chronic illness vs. disability care; high-burden vs. moderate-burden; Swiss German vs. Swiss French regions), and what scope limitations constrain transfer to diverse Swiss caregiver populations? Documents profile-stratified performance analysis and simulation-to-human validity gaps for Swiss context.

RQ–Objective crosswalk (concise):
- RQ1 → Objectives (1) Dynamic Personality-Aware Adaptation, (2) Zurich Model Operationalization
- RQ2 → Objectives (4) Caregiver-Specific Emotional Support, (5) Personalized Caregiving Education
- RQ3 → Objective (6) Swiss Healthcare Policy Navigation
- RQ4 → Objectives (1), (4), (6) via user-centered outcomes and policy comprehension
- RQ5 → All objectives (1–6) via stratified analyses and generalization checks

### 3.3 Success Criteria (Architecture-Oriented)

To build a reusable, reliable, and personality-adaptable chatbot architecture, we define explicit success criteria (to be validated in thesis phase):

**Reusability (Designed):** Stable API contracts for detect→regulate→generate pipeline; config-driven policy packs (YAML/JSON) designed to enable domain transfer without code changes; portable evaluator harness with pluggable metrics. **Target threshold:** Policy pack swap < 30 min (requires thesis-phase timed experiments); zero breaking changes.

**Reliability (Target):** JSON compliance ≥ 99.5%; EMA stabilization in ≥ 80% of sessions (variance < 0.15 within 6-8 turns); confidence calibration (filter < 0.4, align ≥ 85% when ≥ 0.7); graceful degradation (100% failures handled, zero unhandled exceptions).

**Effectiveness (Target):** Primary outcome: ≥ 20% improvement on evaluation criteria (tone, relevance/coherence, needs) with 95% CI. Secondary: intent classification ≥ 85%, directive-outcome alignment ≥ 80%, inter-run consistency ≥ 0.85.

**Observability:** Complete JSONL traces (OCEAN evolution, directives, confidence, metadata); reproducible seeds, version-locked models/prompts, configuration snapshots; automated testing (contracts, EMA, evaluator).

### 3.4 Mapping to Methodology

These research questions and success criteria inform our methodology: RQ1-2 validated through per-turn logging, directive auditing, and outcome metrics; RQ3 through multi-run consistency testing and bias controls; RQ4 through workflow instrumentation, policy pack validation, and interface stability testing; RQ5 through systematic variation of simulation scenarios (extreme vs. mixed profiles, diverse stress contexts) and documentation of scope limitations.

---

## 4. Methodology

### 4.1 Architecture and Workflow

We implement a reproducible pipeline orchestrated via N8N with deterministic JSON contracts, neutral fallbacks, and comprehensive logging. Each stage (ingest, detection, regulation, generation, verification, persistence) exposes stable interfaces configured by versioned policy packs, enabling reuse, scaling, and domain transfer.

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
│  │   Next.js       │◄──────►│   N8N Workflow   │                 │
│  │   Frontend      │  HTTP  │   Engine         │                 │
│  │  (Port 3000)    │        │  (Port 5678)     │                 │
│  │                 │        │                  │                 │
│  │ • User Interface│        │ • Orchestration  │                 │
│  │ • API Routes    │        │ • Node Execution │                 │
│  │ • Chat UI       │        │ • Webhook Handler│                 │
│  └─────────────────┘        └────────┬─────────┘                 │
│           │                           │                          │
│           │                           │                          │
│           │                           ▼                          │
│           │                  ┌──────────────────┐                │
│           │                  │   PostgreSQL     │                │
│           └─────────────────►│   Database       │                │
│                   SQL        │  (Port 5432)     │                │
│                              │                  │                │
│                              │ • Sessions       │                │
│                              │ • Turns          │                │
│                              │ • States         │                │
│                              │ • Metrics        │                │
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
│                              │ • Rate Limiting  │                │
│                              │ • Temp Storage   │                │
│                              └──────────────────┘                │
│                                                                  │
└──────────────────────────────────────────────────────────────────┘
         │                          │                    │
         ▼                          ▼                    ▼
  ┌─────────────┐          ┌──────────────┐    ┌─────────────┐
  │   Volume:   │          │   Volume:    │    │   Volume:   │
  │  frontend/  │          │  n8n_data/   │    │  postgres/  │
  │   .next     │          │  workflows   │    │    data     │
  └─────────────┘          └──────────────┘    └─────────────┘

```

*Docker Compose deployment for Next.js frontend, N8N workflow, PostgreSQL, and Redis. Internal networking and persistent volumes enable durability; external LLM endpoints are accessed over HTTPS.*

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
   - **High-O:** Mention emerging programs, community resources
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

**PostgreSQL Database:** Four core tables persist state for longitudinal analysis: `chat_sessions` (metadata), `conversation_turns` (dialogue history with directives and coaching modes), `personality_states` (EMA-smoothed OCEAN values, confidence, stability flags), `performance_metrics` (latencies, tokens). Helper functions retrieve latest personality state and conversation history for context windows. Data flow: Load previous state → Detection (GPT-4) → EMA smoothing (α=0.3) → Save to PostgreSQL → Next turn retrieves smoothed state for continuity.

**Table 5. PostgreSQL Schema Overview**

| Table | Primary Key | Purpose | Key Columns |
|-------|-------------|---------|-------------|
| `chat_sessions` | `session_id` (UUID) | Session metadata | `total_turns`, `evaluation_mode`, `status` |
| `conversation_turns` | `(session_id, turn_index)` | Conversation history | `user_message`, `assistant_response`, `directives_applied`, `coaching_mode` |
| `personality_states` | `(session_id, turn_index)` | EMA-smoothed OCEAN | `ocean_o/c/e/a/n`, `confidence_o/c/e/a/n`, `stable` |
| `performance_metrics` | `(session_id, turn_index)` | System performance | `detection_latency_ms`, `generation_latency_ms`, `total_tokens` |

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

**Evaluation Matrix Structure:**

The evaluation matrix captures comprehensive assessment data across multiple dimensions for each conversation turn. Each evaluation record includes:

**Conversation Context Fields:**
- **Row ID:** Unique identifier for tracking individual assessments
- **Profile Type:** Simulated personality profile (Type A: high OCEAN; Type B: low OCEAN; Type C: mixed)
- **Turn Number:** Position within conversation sequence (1-10)
- **User Message:** Original user input text
- **Assistant Reply:** Generated system response

**Personality State Fields:**
- **OCEAN Values (Smoothed):** EMA-smoothed continuous trait estimates (e.g., O:0.78, C:0.65, E:0.82, A:0.71, N:-0.68)
- **Confidence Scores:** Per-trait confidence assessments (range 0.0-1.0)
- **Stability Flag:** Boolean indicator (TRUE/FALSE) signaling stable personality estimate (≥6 turns, variance <0.15)
- **Applied Directives:** Array of behavioral directives activated (e.g., ["Introduce novel ideas", "Energetic tone", "Structured steps"])

**Evaluation Criteria Scores (0-2 scale):**
- **Detection Accuracy (Det.Acc):** Alignment between inferred OCEAN and personality cues
- **EMA Convergence (EMA.Conv):** Quality of temporal smoothing and stability progression
- **Confidence Calibration (Conf.Cal):** Appropriateness of confidence scores relative to evidence
- **Regulation Effectiveness (Reg.Eff):** Correct application of behavioral directives
- **Emotional Tone (Tone):** Match between response tone and user state/personality
- **Relevance & Coherence (Rel&Coh):** Contextual appropriateness and logical consistency
- **Personality Needs (Needs):** Satisfaction of trait-specific requirements
- **Total Score:** Sum of all criterion scores (0-14 for regulated; 0-6 for baseline)

**Example Evaluation Records:**

*Type A Profile (High OCEAN), Turn 6:*
- User: "I'm excited to try new approaches..."
- Assistant: "That's wonderful! Let's explore some creative strategies..."
- OCEAN: O:0.78, C:0.65, E:0.82, A:0.71, N:-0.68 (Stable: TRUE)
- Directives: Introduce novel ideas, Energetic tone, Structured steps
- Scores: Det.Acc=2, EMA.Conv=2, Conf.Cal=2, Reg.Eff=2, Tone=2, Rel&Coh=2, Needs=2 (Total: 14/14)

*Type B Profile (Low OCEAN), Turn 6:*
- User: "Everything feels uncertain..."
- Assistant: "I understand uncertainty is difficult. Let's focus on what you can control..."
- OCEAN: O:-0.72, C:-0.68, E:-0.75, A:-0.61, N:0.79 (Stable: TRUE)
- Directives: Familiar examples, Calm tone, Flexible guidance, Extra comfort
- Scores: Det.Acc=2, EMA.Conv=2, Conf.Cal=2, Reg.Eff=2, Tone=2, Rel&Coh=2, Needs=2 (Total: 14/14)

**EMA-Specific Metrics:** Convergence rate (target: 6-8 turns to `stable=TRUE`); smoothness (variance < 0.15 post-stabilization); confidence-weighted accuracy; temporal consistency (r > 0.7).

**Scoring Protocol:** Trinary (Yes=2, Partial=1, No=0); per-session averages, per-profile comparisons; GPT-4 evaluator with fixed prompts, blinded assessment, randomized order; inter-run consistency ≥ 0.85. 

**Human Triangulation Requirement:** All LLM evaluator outputs require human validation on a 10-15% sample (minimum n=20 conversations) with two trained annotators. Target: Cohen's κ≥0.70 for human-LLM agreement on shared items. LLM evaluator used for scale but not as sole arbiter. Human-LLM agreement κ≥0.70 serves as a release gate for thesis claims; failure triggers expanded human evaluation.

**Use-Case Outcome Metrics (Swiss Caregiver-Specific):**

Beyond technical evaluation, the thesis phase includes **caregiver-centered outcome measurement** with Swiss family caregiver participants (n=30-50, 8-week intervention):

| Outcome Domain | Metric | Measurement Instrument | Target Threshold |
|----------------|--------|------------------------|------------------|
| **System Usability** | Usability score | System Usability Scale (SUS) | ≥75/100 |
| **Perceived Helpfulness** | Caregiver-rated usefulness | 5-point Likert scale ("How helpful was this interaction?") | ≥4.0/5.0 average |
| **Sustained Engagement** | Return rate | 4-week session count (≥1 session/week) | ≥60% retention |
| **Caregiver Stress** | Burden reduction | Caregiver Burden Inventory (CBI) pre/post | ≥10% reduction |
| **Benefit Navigation** | Application initiation | Self-reported benefit application starts (AHV, IV, respite) | ≥30% of eligible caregivers |
| **Self-Care Adoption** | Coping strategy use | Weekly self-care frequency log (respite, boundaries, support) | ≥20% increase from baseline |
| **Policy Comprehension** | Benefit understanding | 5-question quiz on eligibility criteria (pre/post interaction) | ≥30% improvement |

**Qualitative Feedback Collection:** Semi-structured exit interviews (n=10-15) exploring: (1) personality adaptation appropriateness, (2) policy guidance clarity, (3) emotional support quality, (4) trust and transparency perceptions, (5) suggestions for improvement. Thematic analysis via NVivo for emergent themes.

**Thesis Phase Experimental Validation (Preregistered):**

| Experiment | Objective | Method | Success Criteria |
|------------|-----------|--------|------------------|
| **E1: Detection Validity** | Validate OCEAN inference accuracy | n=30-50 participants complete BFI-44; correlate with system inferences | Pearson r≥0.75 per trait |
| **E2: EMA Sensitivity** | Validate α=0.3 selection | Test α ∈ {0.1, 0.2, 0.3, 0.4, 0.5} with N≥250 simulated conversations | Convergence ≤8 turns, σ²<0.15, best responsiveness |
| **E3: Regulation Effectiveness** | Validate directive-outcome alignment | Ablation tests removing directives; measure quality impact | Cohen's d≥0.3 for primary directives |
| **E4: Human-LLM Agreement** | Validate automated evaluator | Two human annotators + LLM on n≥20 conversations | Cohen's κ≥0.70 (release gate) |
| **E5: Policy Pack Transfer** | Validate cross-domain reusability | Two independent implementers swap education/customer service packs | Median time ≤30 min, zero code changes |

**Baseline Conditions:** Generic (non-adaptive), memory-only (mem0-style), detection-only (no regulation). Target metrics: Cohen's d≥0.5, p<0.05, ≥20% relative improvement.

### 4.7 System Advantages and Reproducibility

**Key Advantages:** Psychological framework fidelity captures motivational intensity; EMA enables smooth temporal tracking reducing trait oscillation; fine-grained adaptation (continuous values vs. discrete); confidence weighting filters unreliable detections; PostgreSQL persistence supports longitudinal analysis.

**Reproducibility Measures:** Fixed parameters (model versions, API endpoints, temperature, seeds, prompt hashes); comprehensive JSONL logging (per-turn traces, node timings, errors, configs); neutral fallbacks for all failures; dialogue-only grounding; automated CSV export for analysis.

---

## 5. Technology, Software, and Applications

### 5.1 Core Technology Stack

The system employs an N8N-orchestrated architecture combining: (1) **Backend**: N8N workflow engine with PostgreSQL (ACID-compliant state persistence) and Redis (session caching); (2) **LLMs**: GPT-4.1 for detection (temp 0.3, 300 tokens, 30s timeout) and generation (temp 0.7, 220 tokens, 20s timeout), with Gemini 2.5 Pro as cost-effective alternative; (3) **Frontend**: Next.js 14+ (React 18) with Server-Sent Events for real-time OCEAN updates; (4) **Containerization**: Docker Compose for local development, Vercel for frontend deployment. Complete specifications in supplementary materials.

### 5.2 Development and Testing

**Environment Setup**: Docker Compose orchestrates N8N, PostgreSQL, and Redis containers with `.env` configuration, locked dependencies (`requirements.txt`, `package.json`), and encrypted API keys via N8N credential vault. **Quality Assurance**: Automated testing suite (`test_personality_chatbot.sh`, `test_detection_accuracy.sh`, `test_regulation_coherence.sh`) validates JSON contracts, EMA convergence, and evaluator consistency. **Monitoring**: N8N execution logs track node timings, success rates, token usage, and system health with automated failure alerts.

### 5.3 Security and Privacy

**Data Protection**: AES-256 encryption at rest, TLS 1.3 in transit; role-based access (PI and supervisor only); comprehensive audit trails via JSONL logging; data minimization (no PII collection). **API Security**: N8N credential vault for key management; rate limiting (configurable per endpoint); sanitized error messages; HTTPS enforcement. **Privacy Compliance**: Anonymization protocols, explicit user consent, GDPR adherence with 5-year retention and user-controlled deletion rights.

### 5.4 Computational Costs and Performance

**Cost and Performance Estimates**: Preliminary cost modeling suggests per-turn expenses and latency targets that favor GPT-4 for accuracy with Gemini-1.5-Pro as cost-effective alternative. Optimization strategies include response caching, batch processing, and adaptive verification. Detailed vendor-specific costs, latency estimates, and token usage projections are provided in Appendix E (based on 2024 pricing; subject to verification in thesis phase).

### 5.5 Deployment and Maintenance

**Deployment Strategy**: Docker Compose for development; cloud staging environment for integration testing; Kubernetes planned for production scaling (horizontal N8N instances, PostgreSQL read replicas). **Maintenance Protocols**: Model version locking with API endpoint pinning; N8N workflow version control (Git-tracked JSON exports); automated PostgreSQL backups (daily encrypted snapshots); comprehensive technical documentation for reproducibility.

### 5.6 Frontend Architecture: React/Next.js Human-Centered Interface

Five innovation areas (condensed):

1) Progressive Personality Visualization
- Levels: icon status → tooltip traits → expandable radar + EMA trends
- Goal: reduce cognitive load while maintaining awareness (SUS target ≥75)

2) Transparent Control Panel
- Trait override sliders; visible directives; policy pack selector
- Goal: increase trust and appropriateness (target ≥4.0/5.0)

3) Performance Monitoring
- Real-time latency display; adaptive streaming; timeout warnings
- Goal: mitigate frustration; track per-session performance

4) Accessibility-First Design (WCAG 2.1 AA)
- Screen reader labels; keyboard navigation; high contrast; scalable type
- Goal: inclusive interaction; plan voice I/O as future extension

5) Frontend as Research Instrument
- Feature flags; session interaction recording; heatmaps; exit surveys
- Experiments: visualization, transparency, performance (n≈150 total)

---

## 6. Project Plan and Risk Management

### 6.1 Thesis Proposal and Structure

**Annotated Thesis Structure (Target: 80-100 pages)**

**Chapter 1: Introduction** (8-10 pages) - Context, problem statement, research objectives, RQ1-5, contributions, organization

**Chapter 2: Literature Review** (15-18 pages) - Big Five/Zurich Model foundations, personality-aware AI state-of-art, industrial memory systems, LLM dialogue systems, temporal stability methods, research gaps

**Chapter 3: Methodology** (20-25 pages) - Design science approach, system architecture (detect→regulate→generate), EMA smoothing (α=0.3), trait-to-directive mapping, evaluation framework, data management

**Chapter 4: Implementation** (15-18 pages) - N8N workflow, EMA parameter tuning, policy pack development, database schema, simulation protocol, evaluation harness, containerization

**Chapter 5: Results** (15-20 pages) - Detection accuracy (r≥0.75), EMA convergence (6-8 turns), regulation effectiveness, generation quality, baseline comparison (Cohen's d≥0.5), human validation (n=30-50), memory-personality hybrid comparison, cross-domain demonstration, system reliability

**Chapter 6: Discussion** (12-15 pages) - Findings interpretation, theoretical contributions (Zurich operationalization, memory-motivation integration), practical contributions (production architecture, reusability), comparison with Devdas (2025) and industrial systems, validity threats, ethical considerations, generalization potential

**Chapter 7: Conclusion** (5-8 pages) - Summary, RQ1-5 answers, limitations (EMA parameters, sample size, cultural bias), future work (multimodal input, cross-cultural validation, long-term adaptation, clinical applications)

**Three Core Thesis Extensions:**
1. Human Validation (Weeks 15-16): n=30-50 human participants with BFI-44 ground truth; target r≥0.75 detection correlation, κ≥0.80 inter-rater reliability
2. Large-Scale Simulation (Weeks 11-14): N≥250 simulated conversations for A/B testing vs. mem0/LangChain baseline; target ≥20% improvement on emotional tone and needs satisfaction
3. Cross-Domain Demonstration (Weeks 8-10): Education and customer service policy pack swaps; target <30 min transfer time, zero breaking changes

### 6.2 Twenty-Week Work Plan

**Timeline:** Foundation (weeks 1-3) → Design & Architecture (4-6) → Implementation Phase 1 (7-10) → Evaluation & Iteration (11-14) → Human Validation (15-16) → Analysis & Writing (17-19) → Finalization (20).

**Table 8. Twenty-Week Work Plan with Milestones**

| Phase | Week(s) | Primary Activities | Key Deliverables | Success Criteria |
|-------|---------|-------------------|------------------|------------------|
| **Phase 1: Foundation** | 1-3 | Comprehensive literature review; theoretical framework development; RQ refinement; environment setup | Annotated bibliography; theoretical framework document; finalized RQs; functional dev environment | 30+ papers reviewed; clear theoretical grounding; testable RQs; working N8N + Docker setup |
| **Phase 2: Design & Architecture** | 4-6 | System architecture design; module specification; contract definition; pilot testing | Architecture diagrams; JSON contracts; design documentation; pilot results | Modular design validated; stable contracts; successful pilot conversations |
| **Phase 3: Implementation (Core)** | 7-10 | Detection module development; regulation logic; generation pipeline; EMA integration; PostgreSQL setup | Working personality detection; regulation engine; response generation; persistence layer | Detection accuracy ≥70%; stable trait convergence; grounded responses; persistent state |
| **Phase 4: Evaluation & Iteration** | 11-14 | Automated evaluation framework; simulation execution (N≥250); A/B testing; prompt optimization; bug fixes | Evaluation harness; simulation dataset; performance metrics; refined prompts | Inter-run reliability ≥0.85; statistically significant improvements; reproducible results |
| **Phase 5: Human Validation** | 15-16 | Ethics approval; participant recruitment (n=30-50); human studies; BFI-44 ground truth; qualitative feedback | IRB approval; participant data; validation results; user feedback | Ethical compliance; detection correlation r≥0.75; positive user reception |
| **Phase 6: Analysis & Writing** | 17-19 | Statistical analysis; visualization; preliminary study writing; limitation analysis; thesis outline | Complete preliminary study document; publication-quality figures; thesis proposal | Comprehensive analysis; clear contributions; honest limitations; thesis roadmap |
| **Phase 7: Finalization** | 20 | Supervisor feedback integration; peer review; final QA; presentation preparation; handover documentation | Final preliminary study v2.0; presentation slides; code repository; handover docs | Publication-ready document; clear presentation; reproducible artifacts; smooth handover |


**Resources:** LLM API credits (~$200-500), N8N/Docker infrastructure, R/Python statistical tools, supervisor meetings (2hr/week), peer reviewers, psychology expert, ethics board consultation.

### 6.3 Risk Management

**Risk Matrix:** Assesses likelihood/impact (Low/Medium/High). Key risks: **Evaluation** (LLM evaluator bias/drift, Medium/High) mitigated by fixed prompts, 3× runs, human spot-checks; **Reproducibility** (non-determinism, Medium/High) addressed by pinned model versions, fixed seeds, config logging; **Data Quality** (simulated profiles, Medium/Medium) managed by expert validation, mid-range profiles, pilot human validation; **Technical** (prompt sensitivity, Medium/Medium) controlled by versioning, A/B tests, directive auditing; **Infrastructure** (vendor interruptions, Medium/Medium) handled by provider abstraction, alternates, retries; **Ethics/Privacy** (data protection, Low/High) ensured by anonymization, encryption, IRB compliance; **Scope** (feature creep, Medium/Medium) prevented by guardrails, change control, thesis deferral.

**Mitigation Playbooks:** Evaluator drift (consistency <0.85) → freeze prompts, compare providers; JSON failures (>0.5%) → schema validation, temperature reduction; Latency (p95 >2s) → reduce tokens, cache responses; Privacy incident → rotate keys, audit logs.

**Contingency:** Alternative providers (GPT-4, Claude) ready; thesis phase human evaluation fallback (n=30-50); scope adjustment gates (e.g., evaluator <0.75 → switch to human sample).

**Monitoring (Planned):** Weekly KPI tracking targets: JSON compliance ≥99.5%, EMA stabilization ≥80%, evaluator consistency ≥0.85, p95 latency <2.0s, zero privacy incidents.

---

## 7. Future Work

### 7.1 Future Research Directions

Future work includes human validation (n=150), cross-cultural adaptation, multimodal personality detection (voice, facial expression), longitudinal trait evolution tracking, and clinical application with IRB oversight. The thesis phase addresses immediate limitations through stratified sampling, expert directive review, and memory-personality hybrid comparison studies.

---

### 7.2 Limitations vs. Future Work (Quick Summary)

| Area | Key Limitation (Now) | Planned Improvement (Thesis/Future) |
|------|-----------------------|-------------------------------------|
| Detection | Theory-derived EMA α=0.3, no human validation | Sensitivity sweep (α ∈ {0.1–0.5}); r≥0.75 vs. BFI-44 |
| Regulation | Theory-mapped directives; no empirical ablation | Directive ablations; effect sizes (d≥0.3) and expert review |
| RAG | Policy retrieval not yet implemented | Build Swiss caregiver RAG with citations and grounding checks |
| Evaluation | LLM evaluator only; no κ gate | Human triangulation (κ≥0.70) as release gate |
| Reusability | Policy-pack transfer untested | Timed swaps across domains (≤30 min, zero code changes) |
| Ethics/Bias | Intersectional fairness untested | Bias audits (gender×OCEAN, age×OCEAN); mitigation playbooks |

Notes: Summary is for reader orientation; detailed plans remain in Sections 4–6.

## 8. References

Abbasian, M., Azimi, I., Rahmani, A. M., & Jain, R. C. (2023). Conversational health agents: A personalized LLM-powered agent framework. *arXiv preprint arXiv:2310.02374*. https://doi.org/10.48550/arXiv.2310.02374

Adamopoulou, E., & Moussiades, L. (2020). An overview of chatbot technology. In *IFIP International Conference on Artificial Intelligence Applications and Innovations* (pp. 373-383). Springer. https://doi.org/10.1007/978-3-030-49186-4_31

Alisamir, S., & Ringeval, F. (2021). On the evolution of speech representations for affective computing: A brief history and critical overview. *IEEE Signal Processing Magazine*, 38(4), 12-21. https://doi.org/10.1109/MSP.2021.3106890

Anttila, T., Selander, K., & Oinas, T. (2020). Disconnected lives: Trends in time spent alone in Finland. *Social Indicators Research*, 150, 711-730. https://doi.org/10.1007/s11205-020-02304-z

Quirin, M., Kruglanski, A. W., Higgins, E. T., Kuhl, J., de Jong-Meyer, R., Kämpfe-Hargrave, N., Eggerman, C., Baumann, N., & Kazén, M. (2023). Dynamics of personality: The Zurich model of motivation revived, extended, and applied. *Journal of Personality*, 91(5), 1097-1122. https://doi.org/10.1111/jopy.12797

Church, A. T. (2000). Culture and personality: Toward an integrated cultural trait psychology. *Journal of Personality*, 68(4), 651-703. https://doi.org/10.1111/1467-6494.00112

Costa, P. T., Jr., & McCrae, R. R. (1992). Normal personality assessment in clinical practice: The NEO Personality Inventory. *Psychological Assessment*, 4(1), 5-13. https://doi.org/10.1037/1040-3590.4.1.5

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

Musich, S., Wang, S. S., Hawkins, K., & Yeh, C. (2015). The impact of loneliness on quality of life and patient satisfaction among older, sicker adults. *Gerontology & Geriatric Medicine*, 1, e2333721415582119. https://doi.org/10.1177/2333721415582119

OpenAI. (2024). *ChatGPT memory and personalization*. OpenAI. Retrieved October 10, 2024, from https://openai.com/blog/memory-and-new-controls-for-chatgpt

Park, G., Schwartz, H. A., Eichstaedt, J. C., Kern, M. L., Kosinski, M., Stillwell, D. J., Ungar, L. H., & Seligman, M. E. P. (2015). Automatic personality assessment through social media language. *Journal of Personality and Social Psychology*, 108(6), 934-952. https://doi.org/10.1037/pspp0000020

Quirin, M., Malekzad, F., Paudel, D., Knoll, A. C., & Mirolli, M. (2023). Dynamics of personality: The Zurich model of motivation revived, extended, and applied to personality. *Journal of Personality*, 91(4), 928-946. https://doi.org/10.1111/jopy.12805

Shah, S. G., Nogueras, D., van Woerden, H. C., & Kiparoglou, V. (2019). The effectiveness of digital technology interventions to reduce loneliness in adult people: A protocol for a systematic review and meta-analysis. *medRxiv*, 19000414. https://doi.org/10.1101/19000414

Shah, S. G., Nogueras, D., van Woerden, H. C., & Kiparoglou, V. (2020). Evaluation of the effectiveness of digital technology interventions to reduce loneliness in older adults: Systematic review and meta-analysis. *Journal of Medical Internet Research*, 23, e24712. https://doi.org/10.2196/24712

Sorino, P., Biancofiore, G., Lofú, D., Colafiglio, T., Lombardi, A., Narducci, F., & Di Noia, T. (2024). ARIEL: Brain-computer interfaces meet large language models for emotional support conversation. *Adjunct Proceedings of the 32nd ACM Conference on User Modeling, Adaptation and Personalization*. https://doi.org/10.1145/3631700.3665185

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
  "ocean": {"O": -1.0 to 1.0, "C": -1.0 to 1.0, "E": -1.0 to 1.0, "A": -1.0 to 1.0, "N": -1.0 to 1.0},
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
| **Emotional Tone** | Yes: Tone perfectly suited to state/personality. Partial: Generally appropriate. No: Inappropriate. |
| **Relevance & Coherence** | Yes: Highly relevant, coherent response. Partial: Generally relevant. No: Off-topic/incoherent. |
| **Personality Needs** | Yes: Clearly addresses personality-driven needs. Partial: Generic support. No: Fails to address. |

Scoring: Sum criterion scores per interaction; average across sessions for condition-level comparison. Statistical analysis via paired t-tests with effect sizes and 95% CIs.

### Appendix C. Data Management and Ethics

This study adheres to GDPR principles with AES-256 encryption, role-based access (PI and supervisor only), and 5-year retention. Preliminary study uses synthetic data (no IRB required). Thesis phase requires ethics approval before human recruitment (n=150).

**Informed Consent:** Standard template obtains voluntary participation agreement, withdrawal rights, and anonymized data use consent (full form in supplementary materials).

**Crisis Protocol:** Automated keyword detection (suicide, self-harm, violence) triggers immediate crisis resource provision and researcher notification within 1 hour (detailed escalation procedures in supplementary materials).

**Bias Mitigation:** Detection module blind to demographics; directive mappings reviewed by diversity experts; monthly audit of directive distribution across demographic groups. Thesis will report intersectional fairness analysis (gender × OCEAN, age × OCEAN)

---
### Appendix D. Glossary of Key Terms

**OCEAN:** Acronym for the Big Five personality dimensions: Openness, Conscientiousness, Extraversion, Agreeableness, Neuroticism. Each trait is assessed on a continuous scale from -1.0 (low) to +1.0 (high).

**Type A/B/C Personality Profiles (Simulation Reference):**

| Profile Type | O | C | E | A | N | Behavioral Characteristics | Use in Study |
|--------------|---|---|---|---|---|---------------------------|--------------|
| **Type A: High OCEAN** | +0.8 | +0.8 | +0.8 | +0.8 | **-0.8** (low) | Curious, organized, sociable, cooperative, emotionally stable. Responds well to novelty, structure, collaborative tone, and confident guidance. | Tests system adaptation to highly functional, proactive users |
| **Type B: Low OCEAN** | -0.8 | -0.8 | -0.8 | -0.8 | **+0.8** (high) | Prefers familiarity, flexible plans, solitary work, autonomy, and reassurance. Needs calm tone, familiar examples, and extra emotional support. | Tests system adaptation to anxious, cautious users requiring sensitivity |
| **Type C: Mixed/Balanced** | +0.3 | -0.4 | +0.6 | +0.2 | -0.5 | Moderate curiosity, low structure preference, high sociability, moderate cooperation, moderate stability. Requires nuanced, multi-dimensional adaptation. | Tests system's ability to handle realistic, complex personality profiles |

*Notes:* 
- Type A/B represent **extreme profiles** for stress-testing directive mappings; Type C represents **realistic mixed profiles** common in actual populations.
- Simulation uses these archetypes to ensure system handles full spectrum of personality variation.
- Thesis phase includes additional profiles (e.g., High N + High C, Low E + High O) to test specific trait interactions.

**EMA (Exponential Moving Average):** A statistical smoothing technique that computes weighted averages giving exponentially decreasing weights to older observations. In this system, EMA stabilizes personality trait estimates across conversation turns by blending current detections (30% weight, α=0.3) with historical averages (70% weight).

**α (Alpha):** The smoothing factor in EMA calculations, set to 0.3 in this implementation. Determines the balance between responsiveness to new observations (higher α) and stability from historical data (lower α).

**JSON Contracts:** Standardized data formats (JSON) defining exact structure of inputs/outputs for each system module, ensuring interoperability and systematic testing.

**Policy Packs:** Modular configuration files (YAML or JSON) encapsulating domain-specific behavioral rules, coaching modes, and regulation directives. Enable rapid domain transfer without code modification.

**Zurich Model:** A psychological framework conceptualizing human motivation through three fundamental systems: security (safety/comfort needs), arousal (novelty/stimulation needs), and affiliation (social connection needs). Used to map personality traits to behavioral adaptations.

**Dialogue Grounding:** The constraint that all system responses must be strictly entailed by the user's conversational input, preventing fabrication of external information or facts not present in the dialogue.

**Quote-and-Bound:** A generation approach ensuring every assertion in responses is directly grounded in quoted user statements, critical for preventing hallucination in human-centered applications.

**Grounding vs. Hallucination (Detailed):** 
- **Grounded response:** "You mentioned feeling exhausted from caring for your mother 24/7. Let's explore respite care options." → Directly references user's stated concern
- **Hallucinated response:** "I see you're caring for your mother who has advanced dementia and lives in Zurich." → Fabricates specific medical/location details not mentioned by user
- **Why it matters:** In personality-adaptive systems, hallucination risks are heightened because the system infers psychological states. Strict grounding prevents the system from making unwarranted assumptions about user situations, maintaining trust and safety. Our system enforces grounding through: (1) prompt constraints ("Base responses ONLY on user input"), (2) verification module checking for external claims, and (3) neutral fallbacks when context is insufficient.

**Confidence-Aware Filtering:** A mechanism that only updates personality estimates when detection confidence exceeds a minimum threshold (≥0.4), preventing noise from low-quality inferences.

**Confidence Calibration (Detailed):**
A confidence score is **well-calibrated** when it accurately reflects the reliability of a prediction. For personality detection:
- **Well-calibrated:** If the system assigns confidence=0.8 to Extraversion=+0.6, then 80% of such predictions should be accurate (within ±0.2 of ground truth)
- **Overconfident (poorly calibrated):** System assigns confidence=0.9 but only 60% of predictions are accurate → unreliable, may trigger inappropriate adaptations
- **Underconfident:** System assigns confidence=0.5 but 85% of predictions are accurate → missed opportunities for personality adaptation
- **Our approach:** Threshold ≥0.4 for trait updates balances false positives (acting on noise) vs. false negatives (missing genuine signals). Thesis phase will empirically validate calibration by comparing confidence scores to ground-truth accuracy (BFI-44 correlation) across confidence bins (0.0-0.4, 0.4-0.7, 0.7-1.0). Target: ≥85% accuracy for confidence ≥0.7.

**N8N:** An open-source workflow automation platform enabling visual design of data pipelines. Used for orchestrating the detection→regulation→generation→verification process with transparent node-based architecture.

**PostgreSQL:** An open-source relational database system used for persistent storage of conversation sessions, personality states, and performance metrics, enabling longitudinal analysis.

**Vector Embeddings:** Numerical representations of text in high-dimensional space (typically 768-1536 dimensions for modern LLMs), enabling semantic similarity comparisons. Used by memory-based systems like mem0 and LangChain Memory.

**mem0:** An open-source memory layer for AI applications that stores user interactions as vector embeddings, enabling factual recall across sessions without explicit personality modeling.

**LangChain Memory:** A framework component for managing conversational context and history in LLM applications, supporting various memory strategies (buffer, summary, entity extraction).

**Graceful Fallback:** Error handling mechanism that ensures system failures produce neutral, supportive responses rather than crashes, maintaining user experience even during technical failures.

---

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

---

