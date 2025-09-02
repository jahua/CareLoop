---
Title: "Personality-Aware Behavior Regulation Improves Emotional Support Quality in Chatbots: A Simulation Study for Healthcare Settings"
Authors: Samuel Devdas
Affiliations: Lucerne University of Applied Sciences and Arts (HSLU), MSc IDS, Lucerne, Switzerland
Correspondence: samuel.devdas@stud.hslu.ch
Keywords: Big Five, Zurich Model, conversational AI, emotional support, elder care, personalization, large language models (LLMs)
Article Type: Original Article (Short/Brief Report)
---

## Abstract
Artificial intelligence companions are increasingly explored to support psychosocial well-being in healthcare, particularly for older adults at risk of loneliness. We present a personality-adaptive chatbot that detects user Big Five (OCEAN) traits in real time and dynamically regulates conversational behavior using prompts aligned with the Zurich Model of Social Motivation (security, arousal, affiliation). In simulated dialogues representing two extreme personality profiles—Type A (high OCEAN) and Type B (low OCEAN)—we compare regulated assistants (dynamic detection + behavior modulation) against non-adaptive baselines. A structured Evaluation Matrix rated responses on emotional tone, relevance/coherence, personality needs addressed, and (for regulated bots) detection and regulation effectiveness, using a blinded Evaluator GPT.

Across 10 chatbots and 120 message pairs, regulated assistants achieved perfect comparable scores on shared criteria (36/36), while baselines averaged 23.6–24.0/36, yielding a 33–34% improvement. Criterion-wise, regulated assistants reached near-perfect detection and regulation effectiveness and consistently addressed personality-specific needs; baselines did not. These results indicate that real-time personality detection and behavior regulation substantially improve emotional alignment and conversational quality, with practical implications for elder care, digital companions, and mental health support. Limitations include simulated users, short dialogues, discrete trait labels, and automated evaluation. Future work will involve human participants, longitudinal interactions, multimodal cues, and clinical-grade evaluation protocols.

## Highlights
- Personality-adaptive chatbot maps Big Five traits to Zurich Model–aligned regulation prompts in real time.
- Regulated assistants improved shared evaluation criteria by ~34% over non-adaptive baselines.
- Strong potential for elder care and mental health support where psychological safety and personalization matter.

## 1. Introduction
Loneliness and social isolation in older adults are linked with adverse health outcomes, including depression, cognitive decline, and mortality [1–3]. AI companions are a promising, scalable approach to augment psychosocial support, yet many systems rely on generic prompts and static user profiles, limiting personalization and emotional alignment [4–6].

The Five-Factor Model (Big Five; OCEAN) provides a robust foundation for modeling personality differences that affect interpersonal interaction [7]. To translate personality into adaptive behavior, we leverage the Zurich Model of Social Motivation, which organizes motivational systems along security, arousal, and affiliation and can guide conversational stance and tone [8].

We investigate whether real-time personality detection combined with Zurich Model–aligned behavior regulation can improve emotional support quality in chatbot interactions for healthcare-relevant contexts, with a focus on older adults. We implement a modular detection–regulation pipeline and evaluate performance against non-adaptive baselines in controlled, short-form dialogues using structured, blinded assessments.

## 2. Methods
### 2.1 Study design
We conducted a controlled simulation comparing personality-adaptive (regulated) assistants to non-adaptive (baseline) assistants under two extreme user personality profiles: Type A (OCEAN +1,+1,+1,+1,+1) and Type B (OCEAN −1,−1,−1,−1,−1). For each personality type, 5 regulated and 5 baseline assistants engaged in 6-turn dialogues, yielding 60 turns per type and 120 total evaluated message pairs.

### 2.2 Personality detection module
After each user message, the regulated assistant updated a discrete OCEAN vector with values in {−1, 0, +1}, where 0 denotes insufficient evidence. Trait detectors were modular and updated cumulatively over dialogue turns to reduce premature classification. The detection vector was logged and passed to the regulation engine per turn.

### 2.3 Behavior regulation module
For each non-neutral trait, a corresponding behavior prompt was added to the assistant’s instruction set:
- Openness: invite exploration (+1) vs. reduce novelty (−1)
- Conscientiousness: structured guidance (+1) vs. flexible, low-structure approach (−1)
- Extraversion: energetic, sociable tone (+1) vs. calm, reflective style (−1)
- Agreeableness: warmth and collaboration (+1) vs. neutral, matter-of-fact stance (−1)
- Neuroticism (emotional stability): reassure stability (+1) vs. offer comfort and acknowledge anxieties (−1)

Prompts were designed to align with Zurich Model motivational systems: security (N), arousal (O, E), and affiliation (A). The final regulation instruction was the concatenation of all applicable trait prompts for each turn.

### 2.4 Bot variants
- Regulated: real-time detection + dynamic regulation prompts applied each turn.
- Baseline: generic supportive counseling style; no detection or regulation.

### 2.5 Evaluation
We used a structured Evaluation Matrix rated by a blinded Evaluator GPT, scoring each assistant response on: Emotional Tone Appropriateness, Relevance & Coherence, Personality Needs Addressed (both groups), and additionally Detection Accuracy and Regulation Effectiveness (regulated only). The trinary scale (Yes=2, Not Sure=1, No=0) produced comparable totals (max 36/36) for shared criteria and extended totals for regulated assistants.

## 3. Results
### 3.1 Overall performance
On shared criteria, regulated assistants scored 36.0/36 for both personality types, while baseline assistants averaged 23.6/36 (Type A) and 24.0/36 (Type B). This corresponds to absolute improvements of 12.4 and 12.0 points, or 34.44% and 33.33% of the maximum possible score.

### 3.2 Criterion-wise performance
Regulated assistants scored near-perfectly across Detection Accuracy and Regulation Effectiveness and perfectly on Emotional Tone, Relevance/Coherence, and Personality Needs Addressed. Baseline assistants performed adequately on tone and coherence but consistently failed to address personality-specific needs due to their non-adaptive nature.

### 3.3 Qualitative differences
For Type B (low OCEAN), regulated assistants adopted a calm, low-key tone, focused on familiar content, maintained a neutral stance, and offered explicit comfort—consistently matching security needs. Baselines remained broadly supportive but generic, missing skepticism and resistance cues. For Type A (high OCEAN), regulated assistants leveraged novelty, structured guidance, warmth, and energy, which engaged the user’s curiosity and drive more effectively than baselines.

## 4. Discussion
### 4.1 Implications for healthcare
Results suggest that personality-aware regulation can improve the perceived quality and psychological alignment of supportive conversations, which is critical for elder care, mental health triage, and digital companionship. The architecture is transparent and maintainable (explicit trait-to-behavior mappings), enabling clinical teams to audit and adapt regulation strategies to population needs and institutional guidelines.

### 4.2 Relation to prior work
Personality-aware dialogue frameworks and multimodal affective systems have shown promise, yet many rely on static profiles or emotion-only cues [4–6,9–11]. Our contribution integrates dynamic, turn-by-turn personality detection with motivationally grounded behavior regulation, showing consistent gains in emotional tone, coherence, and needs alignment.

### 4.3 Opportunities and challenges for healthcare deployment
- Regulatory and safety governance: Personality-adaptive behavior requires transparent mappings, audit logs, and guardrails to prevent harmful suggestions; alignment with clinical governance, ISO/IEC AI risk management, and data protection is essential.
- Equity and bias: Trait detection may vary across cultures, languages, and demographics. Bias auditing, calibration, and human oversight are required to avoid disparate performance.
- Clinical integration: Workflow fit (triage, check-ins, companionship), escalation protocols, and supervision models need definition; hybrid human-in-the-loop designs are likely in early deployments.
- Data privacy and consent: Personality estimation is sensitive data; explicit consent, minimization, and secure storage are necessary.
- Efficacy and outcomes: Beyond simulated gains, trials should measure engagement, symptom reduction, adherence, and cost-effectiveness against standard care.
- Technical robustness: Handling adversarial inputs, uncertainty, and long-range context requires monitoring, fallback behaviors, and continuous evaluation.

### 4.4 Limitations
- Simulated users (extreme OCEAN): limits ecological validity.
- Short dialogues (6 turns): does not test longitudinal rapport or adherence.
- Discrete trait labels: reduces granularity; intermediate or transient states are not modeled.
- Automated evaluation (Evaluator GPT): requires triangulation with human raters and clinical outcomes.
- Interface constraints: no fine-grained control over LLM parameters; manual orchestration limits scalability.

### 4.5 Future work
- Human studies with older adults; safety monitoring and clinical endpoints.
- Longer interactions to measure engagement, adherence, and well-being outcomes.
- Finer-grained trait scoring and trait-interaction models; automated prompt optimization.
- Multimodal signals (speech, prosody, wearables) for improved detection and regulation.
- Clinical integration, governance, and bias auditing; cost-effectiveness analyses.

## 5. Conclusions
In controlled simulations, personality-adaptive assistants grounded in the Zurich Model substantially outperformed non-adaptive baselines on emotional tone, coherence, and personality-need alignment, improving shared criteria by ~34%. These findings support the integration of real-time personality detection and motivationally aligned regulation into healthcare-oriented conversational systems, especially for elder care and mental health support.

## Statements and Declarations
- Institutional Review Board Statement: Not applicable (simulated users; no human subjects).
- Informed Consent Statement: Not applicable.
- Data Availability Statement: Simulation prompts, evaluation templates, and representative dialogues are available upon reasonable request; a curated replication package will be released in a public repository post-review.
- Code and Materials Availability: Trait detectors, regulation prompts, and evaluation scripts (redacted for review) will be shared under an open-source license upon acceptance.
- Funding: None.
- Acknowledgments: We thank Dr. Guang Lu and Prof. Dr. Alexandre de Spindler for supervision and guidance.
- Conflicts of Interest: The author declares no conflicts of interest.

## References
[1] Musich, S., Wang, S. S., Hawkins, K., & Yeh, C. (2015). The Impact of Loneliness on Quality of Life and Patient Satisfaction Among Older, Sicker Adults. Gerontology and Geriatric Medicine, 1.
[2] Couture, L. (2012). Loneliness Linked to Serious Health Problems and Death Among Elderly. Activities, Adaptation & Aging, 36, 266–268.
[3] Hämmig, O. (2019). Health Risks Associated with Social Isolation in General and in Young, Middle, and Old Age. PLoS ONE, 14.
[4] Ta, V. P., et al. (2020). User Experiences of Social Support From Companion Chatbots in Everyday Contexts. Journal of Medical Internet Research, 22.
[5] Broadbent, E., et al. (2024). ElliQ, an AI-Driven Social Robot to Alleviate Loneliness: Progress and Lessons Learned. JAR Life, 13, 22–28.
[6] De Freitas, J., et al. (2024). AI Companions Reduce Loneliness. Wharton Working Paper 24-078. arXiv.
[7] McCrae, R. R., & John, O. P. (1992). An Introduction to the Five-Factor Model and Its Applications. Journal of Personality, 60(2), 175–215.
[8] Quirin, M., et al. (2023). Dynamics of Personality: The Zurich Model of Motivation Revived, Extended, and Applied to Personality. Journal of Personality, 91(4), 928–946.
[9] Zheng, Z., Liao, L., Deng, Y., & Nie, L. (2023). Building Emotional Support Chatbots in the Era of LLMs. arXiv:2308.11584.
[10] Abbasian, M., et al. (2023). Conversational Health Agents: A Personalized LLM-Powered Agent Framework. arXiv:2310.02374.
[11] Zhang, H., Chen, Y., Wang, M., & Feng, S. (2024). FEEL: A Framework for Evaluating Emotional Support Capability with Large Language Models. arXiv:2403.15699.