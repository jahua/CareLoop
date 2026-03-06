# Research Gap Summary
## Adaptive LLM-Based Chatbot with Personality-Aware Dialogue for Human-Centered Applications for Informal Home Caregivers

---

Despite growing interest in AI-driven caregiver support, no existing systems combine real-time personality detection with adaptive coaching grounded in psychological theory. The literature reveals six critical gaps that this thesis aims to address:

### Gap 1: Lack of Personality-Aware Adaptation
Existing digital health and micro-coaching systems use static, rule-based personalization and overlook individual personality profiles. No current intervention dynamically adapts to caregivers' OCEAN traits or Zurich Model (Security–Arousal–Affiliation, S–A–A) motivational states [Surveys 1, 2, 5, 6]. While daily motivational micro-coaching demonstrates effectiveness in reducing caregiver stress and enhancing resilience, these interventions fail to account for individual differences in psychological needs, resulting in suboptimal engagement and outcomes across diverse caregiver populations.

### Gap 2: Unrealized Zurich Model Operationalization
The Zurich Model offers a strong theoretical foundation for understanding human motivation, yet no validated digital interface or computational mappings translate S–A–A dimensions into chatbot regulation strategies [Surveys 2, 5, 6]. Critical deficiencies include: (a) absence of standardized measurement protocols to confirm targeted S–A–A states are induced during coaching sessions via EMA, psychophysiology, or interaction logs; (b) lack of causal validation through dismantling trials testing whether Security elevation increases adherence and disclosure; and (c) unexplored affiliation pathways in dyadic/group coaching where social dynamics alter optimal policies.

### Gap 3: LLM Reliability and Safety Challenges
Current LLM-based health tools face reliability, truthfulness, and safety issues that impede deployment for vulnerable caregiver populations [Surveys 3, 4, 7]. They lack robust methods for: (a) maintaining persona stability while adapting communication style to user personality without deceptive identity drift; (b) managing hallucinations through guardrail strategies combining retrieval, reasoning traces, and uncertainty disclosure tailored to health guidance; (c) ensuring privacy-preserving deployment via on-device or federated architectures with formal privacy guarantees under home connectivity constraints; and (d) demonstrating truthfulness and calibration across varying health literacy levels and home contexts.

### Gap 4: Caregiver-Specific Implementation Deficit
Existing coaching frameworks rarely consider caregiver-specific needs [Surveys 1, 4]. Key implementation gaps include: (a) unknown dose–response relationships regarding optimal frequency, intensity, and timing of micro-interactions that maximize outcomes while minimizing burden; (b) absence of comparative effectiveness studies of virtual agents versus embodied robots versus hybrid human-in-the-loop models for home-based coaching; (c) unclear best practices for safety escalation protocols detecting risk (suicidality, burnout thresholds) and triggering stepped-care without false alarms; and (d) limited strategies for reducing disparities across low digital literacy, low-resource settings, and culturally diverse caregivers while preserving intervention fidelity.

### Gap 5: Swiss Healthcare Context Specificity
No existing research addresses personality-adaptive care coaching within Switzerland's unique healthcare ecosystem, which presents distinct challenges: (a) cantonal policy variations where home care systems differ significantly across Swiss regions [MDPI, 2024], yet no AI systems adapt to these variations; (b) unaddressed economic stress—23% income reduction (~CHF 970 monthly) faced by Swiss caregivers [PMC, 2023]—requiring specialized psychological support; (c) Spitex integration gap where no digital coaching systems connect with Switzerland's home care services or family caregiver employment models [SSPH+, 2023]; and (d) multi-language requirements (German, French, Italian) for personality-adaptive systems serving Switzerland's linguistically diverse caregiver population.

### Gap 6: Lack of Methodological and Evaluation Standards
The field lacks standardized evaluation protocols, long-term outcome studies, fairness auditing, and cost-effectiveness assessments for adaptive coaching systems, hindering comparability and large-scale validation [Surveys 1, 2, 4, 5, 6]. Specific deficiencies include: (a) absence of consensus on minimal core outcome sets (stress, resilience, engagement, adverse events) to enable meta-analyses; (b) limited studies on habit formation, durability of gains, and relapse dynamics over 6–12 months after coach withdrawal; (c) underdeveloped methods for culturally sensitive S–A–A targets and fairness-aware personalization untested at scale; and (d) lack of implementation science frameworks examining cost-effectiveness, adoption rates, reach, and sustainment profiles in health systems.

---

## Research Contribution

This thesis addresses these gaps by developing an **adaptive LLM-based care coach** that:

1. **Bridges Theory and Practice**: Integrates real-time OCEAN personality detection with Zurich Model-guided S–A–A regulation to create the first theoretically grounded, personality-adaptive coaching system for caregivers.

2. **Operationalizes Psychological Constructs**: Develops validated computational mappings from S–A–A dimensions to chatbot regulation strategies, including measurement protocols via EMA, psychophysiology, and interaction logs.

3. **Ensures Safety and Reliability**: Implements privacy-preserving architecture, persona stability mechanisms, hallucination guardrails, and safety escalation protocols tailored for vulnerable caregiver populations.

4. **Addresses Caregiver-Specific Needs**: Designs micro-coaching strategies validated through expert consultation that account for dose–response relationships, modality effectiveness, and cultural adaptation.

5. **Contextualizes for Swiss Healthcare**: Adapts the system to Switzerland's unique ecosystem including cantonal policy variations, Spitex integration, economic stress support (CHF 970 monthly loss), and multi-language requirements.

6. **Establishes Evaluation Standards**: Employs rigorous evaluation protocols with validated psychometric tools (PSS, CD-RISC), mixed-methods assessment, long-term follow-up, and implementation science frameworks to enable reproducibility and comparability.

By systematically addressing these six critical gaps, this research establishes a new paradigm for human-centered, personality-aware AI applications in informal caregiving, with implications extending beyond Switzerland to global caregiver support systems.

---

**Survey References:**
- Survey 1: Enhancing Caregiver Resilience Through Daily Motivational Micro-Coaching
- Survey 2: Human-Centered Chatbot Development Using Zurich Model
- Survey 3: Human–AI Interaction in Home Care (LLM-Based Care Coach)
- Survey 4: LLM-Based Care Coach Perceptions
- Survey 5: Integrating Zurich Model Feedback Loops in Personality-Adaptive Coaching (Outline)
- Survey 6: Integrating Zurich Model Feedback Loops in Personality-Adaptive Coaching (Content)
- Survey 7: Towards Reliable and Personality-Adaptive LLM Chatbots in Care Coaching

**Context References:**
- [MDPI, 2024] Swiss home care system variations
- [PMC, 2023] Caregiver economic burden (23% income reduction)
- [SSPH+, 2023] Family caregiver employment by home care agencies
































