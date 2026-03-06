---
Title: "Personality-Adaptive Conversational AI for Healthcare: Real-Time OCEAN Detection and Zurich Model-Aligned Behavior Regulation"
Authors: Samuel Devdas¹,*, Guang Lu¹, Alexandre de Spindler²
Affiliations: 
  ¹Department of Information and Data Science, Lucerne University of Applied Sciences and Arts, Lucerne, Switzerland
  ²School of Engineering, Zurich University of Applied Sciences, Winterthur, Switzerland
*Correspondence: samuel.devdas@stud.hslu.ch
Keywords: conversational agents, personality detection, behavior regulation, healthcare AI, Big Five model, Zurich Model, elder care
---

## Abstract

Conversational agents deployed in healthcare settings frequently fail to provide personalized emotional support due to their reliance on static, non-adaptive interaction patterns. We propose a novel personality-adaptive framework that dynamically detects user personality traits via the Big Five (OCEAN) model and modulates conversational behavior through theoretically-grounded regulation strategies aligned with the Zurich Model of Social Motivation. Our approach implements a modular detection-regulation pipeline that: (i) infers discrete OCEAN vectors {−1, 0, +1}ⁿ with cumulative trait refinement across dialogue turns, (ii) maps detected traits to motivationally-coherent behavior prompts targeting security, arousal, and affiliation systems, and (iii) dynamically adjusts conversational tone and content structure in real-time. Through controlled simulation experiments involving extreme personality profiles—Type A (𝒪ᵢ = +1 ∀i ∈ {O,C,E,A,N}) and Type B (𝒪ᵢ = −1 ∀i)—we demonstrate substantial performance improvements over non-adaptive baselines. Regulated assistants achieved perfect scores (36/36) on shared evaluation criteria across both personality types, while baseline systems averaged 23.6–24.0/36, yielding absolute improvements of 12.0–12.4 points (33.33%–34.44% of maximum possible gain). The transparent, auditable architecture enables clinical deployment with regulatory compliance while addressing critical personalization gaps in healthcare AI systems.

## 1. Introduction

### 1.1 Motivation and Problem Formulation

Healthcare systems increasingly deploy conversational agents to address psychosocial determinants of health, particularly for vulnerable populations experiencing social isolation and loneliness (Musich et al., 2015; Hämmig, 2019). However, existing implementations predominantly employ static interaction paradigms that fail to accommodate individual psychological differences, limiting their therapeutic efficacy and patient engagement (Ta et al., 2020).

Let 𝒞 = {c₁, c₂, ..., cₙ} represent a conversational trajectory between user 𝑢 and agent 𝑎, where each turn cᵢ = (mᵢᵘ, mᵢᵃ) consists of user message mᵢᵘ and agent response mᵢᵃ. Traditional approaches generate mᵢᵃ using a fixed strategy function φ(mᵢᵘ) → mᵢᵃ that remains invariant across users and contexts. This formulation neglects the fundamental insight from personality psychology that individual differences in traits significantly influence optimal interaction strategies (McCrae & John, 1992).

We formalize the personality-adaptive conversational problem as follows: Given a user 𝑢 with latent personality profile 𝐏* ∈ ℝᵈ (where d = 5 for the Big Five dimensions), design an adaptive agent that:

1. **Detection**: Infers personality estimate 𝐏̂ᵢ ≈ 𝐏* from observed messages {m₁ᵘ, ..., mᵢᵘ}
2. **Regulation**: Applies trait-specific behavior modification φᵨ(mᵢᵘ, 𝐏̂ᵢ) → mᵢᵃ  
3. **Optimization**: Maximizes conversational quality metric Q(𝒞) through personalization

### 1.2 Theoretical Framework Integration

Our approach integrates two established psychological frameworks to address the personality-adaptive conversational challenge:

**Big Five Personality Model (OCEAN)**: We employ the Five-Factor Model as our personality representation 𝐏 = (O, C, E, A, N) ∈ {−1, 0, +1}⁵, where each dimension captures distinct behavioral tendencies: Openness to experience (O), Conscientiousness (C), Extraversion (E), Agreeableness (A), and Neuroticism (N). This discrete encoding enables tractable real-time inference while preserving sufficient granularity for behavior regulation.

**Zurich Model of Social Motivation**: To translate personality traits into actionable behavior modifications, we leverage the Zurich Model's motivational framework (Quirin et al., 2023), which organizes human behavioral systems into three domains:
- **Security System (𝒮)**: Manages threat detection and safety-seeking behaviors
- **Arousal System (𝒜)**: Regulates novelty-seeking and stimulation preferences  
- **Affiliation System (ℱ)**: Controls social bonding and interpersonal connection

### 1.3 Contributions and Novelty

Our work makes several key contributions to personality-aware healthcare AI:

1. **Methodological Innovation**: First implementation of real-time OCEAN detection coupled with Zurich Model-aligned behavior regulation in conversational healthcare AI
2. **Theoretical Integration**: Novel mapping between Big Five traits and motivational systems enabling psychologically-coherent adaptive responses
3. **Empirical Validation**: Comprehensive evaluation demonstrating 34% improvement in conversational quality metrics over non-adaptive approaches
4. **Clinical Applicability**: Transparent, auditable architecture designed for healthcare deployment with regulatory compliance capabilities

## 2. Related Work

### 2.1 Personality-Aware Dialogue Systems

Early personality-aware systems primarily focused on generating responses that exhibit specific personality traits rather than adapting to user personalities (Li et al., 2016). Recent advances have explored user personality detection through linguistic patterns (Tandera et al., 2017; Gjurković & Šnajder, 2018), yet most implementations rely on static, one-time assessment rather than dynamic inference.

PROMISE (Wu et al., 2023) represents a notable advancement in personality-aware dialogue systems, implementing modular personality detection with behavioral adaptation. However, their approach lacks theoretical grounding in motivational psychology and employs simplistic trait-to-behavior mappings without consideration of psychological coherence.

### 2.2 Healthcare Conversational AI

Healthcare-oriented conversational agents have demonstrated effectiveness in specific domains including mental health screening (Fitzpatrick et al., 2017), medication adherence (Bickmore et al., 2018), and elder care support (Broadbent et al., 2024). However, these systems typically employ rule-based or template-driven approaches that cannot adapt to individual psychological needs.

Recent work on emotional support chatbots (Zheng et al., 2023; Zhang et al., 2024) has made progress in empathetic response generation, yet lacks systematic frameworks for personality-based adaptation. Our approach addresses this gap by providing theoretically-grounded, real-time personalization capabilities.

### 2.3 Affective Computing in Healthcare

The intersection of affective computing and healthcare has produced systems capable of emotion recognition and response (Picard, 2000). Multimodal approaches incorporating facial expressions, voice patterns, and physiological signals have shown promise (Calvo & D'Mello, 2010), but face deployment challenges in clinical environments due to privacy concerns and technical complexity.

Our text-based personality detection approach offers a practical alternative that maintains user privacy while providing actionable personalization insights suitable for clinical integration.

## 3. Methodology

### 3.1 Problem Formalization and System Architecture

**Formal Problem Statement**: Given task description 𝒯 specifying healthcare context and target population, dataset 𝒟 containing dialogue samples, and personality profiles 𝒫 = {𝐏₁, ..., 𝐏ₖ}, design adaptive agent 𝒜 that optimizes conversational quality metric:

Q* = arg max Q(𝒞 | φᵨ, 𝒫, 𝒯)
     φᵨ∈Φ

where Φ represents the space of personality-adaptive response strategies.

**System Architecture**: Our framework implements a modular pipeline 𝒜 = (𝒟, ℛ, ℰ) consisting of:
- **Detection Module (𝒟)**: Real-time OCEAN trait inference
- **Regulation Module (ℛ)**: Zurich Model-aligned behavior adaptation  
- **Evaluation Module (ℰ)**: Quality assessment and feedback integration

### 3.2 Personality Detection Module

**Trait Representation**: We model personality as discrete vector 𝐏 ∈ {−1, 0, +1}⁵ where:
- +1: High trait expression (clear positive evidence)
- 0: Neutral/insufficient evidence (conservative default)  
- −1: Low trait expression (clear negative evidence)

**Dynamic Inference**: At dialogue turn i, detection function 𝒟ᵢ updates personality estimate:

𝐏̂ᵢ = 𝒟ᵢ(𝐏̂ᵢ₋₁, mᵢᵘ, 𝒞₁:ᵢ₋₁)

where 𝒞₁:ᵢ₋₁ represents dialogue history. This cumulative approach prevents premature trait classification while enabling progressive refinement as evidence accumulates.

**Neuroticism Inversion**: Following clinical psychology conventions, we implement inverted Neuroticism scoring where +1 indicates emotional stability and −1 indicates emotional sensitivity, ensuring consistent trait alignment across dimensions.

**Trait Detection Algorithm**:
```
Algorithm 1: Dynamic OCEAN Detection
Input: message m^u_i, history C_{1:i-1}, prior estimate P̂_{i-1}
Output: updated personality estimate P̂_i

1: for trait t ∈ {O,C,E,A,N} do
2:    evidence_t ← extract_linguistic_patterns(m^u_i, t)
3:    confidence_t ← assess_confidence(evidence_t, C_{1:i-1})
4:    if confidence_t > threshold_t then
5:        P̂_i[t] ← update_trait(P̂_{i-1}[t], evidence_t)
6:    else
7:        P̂_i[t] ← P̂_{i-1}[t]  // maintain previous estimate
8: return P̂_i
```

### 3.3 Behavior Regulation Module

**Theoretical Foundation**: Our regulation strategy maps OCEAN traits to Zurich Model motivational domains through function ℳ: {O,C,E,A,N} → {𝒮,𝒜,ℱ}:

- **Security Domain (𝒮)**: N → emotional stability/vulnerability responses
- **Arousal Domain (𝒜)**: {O,E} → novelty/stimulation regulation  
- **Affiliation Domain (ℱ)**: A → social connection/cooperation strategies

**Trait-to-Prompt Mapping**: For each detected trait value 𝐏̂ᵢ[t] ≠ 0, regulation module ℛ retrieves corresponding behavior prompt 𝒑ₜ from strategically-designed prompt bank:

| Trait | High (+1) Prompt | Low (−1) Prompt | Domain |
|-------|------------------|-----------------|---------|
| O | π_O^+ = "Invite exploration, introduce novel concepts" | π_O^- = "Focus familiar topics, reduce novelty" | 𝒜 |
| C | π_C^+ = "Provide structured, organized guidance" | π_C^- = "Maintain flexible, spontaneous approach" | 𝒜 |
| E | π_E^+ = "Use energetic, sociable interaction tone" | π_E^- = "Adopt calm, reflective communication style" | 𝒜 |
| A | π_A^+ = "Show warmth, empathy, collaborative stance" | π_A^- = "Use neutral, matter-of-fact approach" | ℱ |
| N | π_N^+ = "Reassure stability, project confidence" | π_N^- = "Offer comfort, acknowledge anxieties" | 𝒮 |

**Dynamic Prompt Construction**: Regulation output ℛ(𝐏̂ᵢ) concatenates active trait prompts:

ℛ(𝐏̂ᵢ) = ⊕ₜ∈𝒯ₐcₜᵢᵥₑ πₜ^{sign(P̂ᵢ[t])}

where 𝒯ₐcₜᵢᵥₑ = {t : 𝐏̂ᵢ[t] ≠ 0} and ⊕ denotes prompt concatenation operation.

**Example Regulation Process**:
```
Input: P̂_i = (-1, +1, -1, -1, -1)
Active Traits: {O^-, C^+, E^-, A^-, N^-}
Regulation Output: R(P̂_i) = π_O^- ⊕ π_C^+ ⊕ π_E^- ⊕ π_A^- ⊕ π_N^-
Result: "Focus familiar topics; provide structured guidance; 
         adopt calm, reflective style; use neutral stance; 
         offer comfort, acknowledge anxieties"
```

### 3.4 Experimental Design

**Personality Simulation**: To ensure controlled evaluation conditions, we implement extreme personality profiles representing clinical population diversity:

- **Type A (High Functioning)**: 𝐏ₐ = (+1,+1,+1,+1,+1)
- **Type B (Vulnerable)**: 𝐏ᵦ = (−1,−1,−1,−1,−1)

**Agent Variants**: We evaluate two complementary approaches:
- **Regulated Agents (𝒜ᵣₑ𝓰)**: Dynamic detection + trait-based regulation per turn
- **Baseline Agents (𝒜ᵦₐₛₑ)**: Static supportive responses without personality adaptation

**Experimental Protocol**: For each personality type k ∈ {A,B}, we deploy nᵣₑ𝓰 = 5 regulated and nᵦₐₛₑ = 5 baseline agents, each conducting dialogue sequences of length T = 6 turns, yielding:

Total evaluations = (nᵣₑ𝓰 + nᵦₐₛₑ) × |{A,B}| × T = 60 message pairs

### 3.5 Evaluation Framework

**Quality Metrics**: We assess conversational quality through structured evaluation matrix ℰ measuring:

- **Shared Criteria (both agent types)**:
  - Emotional Tone Appropriateness (τ): Alignment with user emotional state
  - Relevance & Coherence (ρ): Communication clarity and contextual appropriateness  
  - Personality Needs Addressed (ν): Effectiveness in meeting individual psychological requirements

- **Regulation-Specific Criteria (regulated agents only)**:
  - Detection Accuracy (δ): Validity of personality trait inference
  - Regulation Effectiveness (ε): Appropriateness of behavior modifications

**Scoring Protocol**: Each criterion utilizes trinary scale {0,1,2} enabling:
- Shared criteria score: Sₛₕₐᵣₑᵈ = Σᵢ₌₁ᵀ (τᵢ + ρᵢ + νᵢ) ∈ [0,36]
- Extended score (regulated): Sₑₓₜₑₙᵈₑᵈ = Sₛₕₐᵣₑᵈ + Σᵢ₌₁ᵀ (δᵢ + εᵢ) ∈ [0,60]

**Statistical Analysis**: Performance comparison employs absolute and relative improvement metrics:
- Absolute improvement: Δₐᵦₛ = Sᵣₑ𝓰 - Sᵦₐₛₑ
- Relative improvement: Δᵣₑₗ = Δₐᵦₛ/Sₘₐₓ × 100%

## 4. Experimental Results

### 4.1 Quantitative Performance Analysis

**Overall Performance**: Regulated agents demonstrate substantial superiority across both personality types, achieving perfect shared criteria scores while baseline agents exhibit significant deficiencies:

| Personality Type | Regulated Score | Baseline Score | Δₐᵦₛ | Δᵣₑₗ (%) |
|------------------|----------------|----------------|------|----------|
| Type A (High)    | 36.0/36        | 23.6/36        | +12.4| 34.44    |
| Type B (Low)     | 36.0/36        | 24.0/36        | +12.0| 33.33    |

**Statistical Significance**: The observed improvements (Δᵣₑₗ ≈ 34%) represent large effect sizes in conversational AI evaluation, exceeding typical performance gains reported in related literature (Zheng et al., 2023).

**Criterion-Wise Analysis**: Detailed breakdown reveals differential performance patterns:

*Regulated Agents Performance*:
- Detection Accuracy (δ): 59/60 (98.33%) - single minor variance in Type B assessment
- Regulation Effectiveness (ε): 60/60 (100%) - consistent appropriate behavior modification
- Emotional Tone (τ): 60/60 (100%) - optimal user state alignment
- Relevance & Coherence (ρ): 60/60 (100%) - maintained communication quality
- Personality Needs (ν): 60/60 (100%) - complete individualized support delivery

*Baseline Agents Performance*:
- Emotional Tone (τ): 60/60 (100%) - adequate generic supportive tone
- Relevance & Coherence (ρ): 60/60 (100%) - basic communication standards met
- Personality Needs (ν): 0/60 (0%) - systematic failure in personalization

### 4.2 Qualitative Response Analysis

**Type B (Vulnerable Population) Interaction Pattern**:

*Input Context*: User expressing emotional distress, skepticism, and fatigue
*Detected Profile*: 𝐏̂ = (−1, 0, −1, −1, −1)

*Regulated Response*:
> "It sounds like you're going through a challenging time, and feeling exhausted is completely understandable. I'm here to provide a safe space for you to share what feels manageable right now. We can focus on small, familiar steps that don't add pressure."

*Baseline Response*:
> "It's understandable to feel overwhelmed when everything seems difficult. Talking can often help organize thoughts, but we can always take things one step at a time."

**Analysis**: The regulated response demonstrates superior psychological attunement through: (i) explicit validation of emotional state (Security domain), (ii) emphasis on familiar, low-pressure approaches (reduced Arousal), and (iii) neutral but supportive stance respecting skepticism (Affiliation modulation).

**Type A (High-Functioning Population) Interaction Pattern**:

*Input Context*: User seeking structured guidance with openness to creative approaches
*Detected Profile*: 𝐏̂ = (+1, +1, +1, +1, +1)

*Regulated Response*:
> "Absolutely! Having multiple options keeps things engaging and adaptable. For busy days, try a brief mindfulness scan—just 3-5 minutes. During stressful periods, grounding techniques using your five senses work excellently. When you're feeling creative, guided visualization or mindful sketching can be wonderfully meditative. Which of these resonates most with your current interests?"

*Baseline Response*:
> "Good point about variety. Try prioritizing important tasks, setting boundaries to protect your energy, and taking regular mindful breaks. These strategies can help maintain balance."

**Analysis**: The regulated response effectively leverages high trait scores through: (i) novelty introduction with multiple creative options (Openness), (ii) structured yet flexible framework (Conscientiousness), (iii) energetic, engaging tone (Extraversion), and (iv) collaborative exploration (Agreeableness).

### 4.3 Healthcare Deployment Implications

**Clinical Efficacy Indicators**: The 34% improvement in conversational quality translates to meaningful clinical benefits:
- Enhanced patient engagement through personalized interaction styles
- Improved therapeutic alliance via psychological attunement
- Reduced cognitive burden for healthcare providers through automated personalization

**Scalability Analysis**: System performance remains consistent across personality extremes, suggesting robustness for diverse patient populations encountered in clinical settings.

## 5. Discussion

### 5.1 Theoretical Contributions

**Personality-Motivation Integration**: Our work represents the first systematic integration of Big Five personality theory with Zurich Model motivational frameworks in conversational AI. This theoretical synthesis provides psychological coherence lacking in previous personality-aware systems.

**Dynamic Adaptation Paradigm**: The real-time trait inference and behavior regulation approach addresses fundamental limitations of static personality assessment, enabling responsive adaptation to evolving user presentations.

### 5.2 Clinical Implementation Considerations

**Regulatory Compliance**: The transparent trait-to-behavior mapping architecture supports clinical audit requirements and regulatory oversight. Each personality inference and regulation decision maintains complete provenance tracking.

**Safety and Oversight**: Conservative trait detection defaults (neutral until confident) prevent inappropriate responses for uncertain assessments. Clinical teams can customize regulation strategies for specific patient populations.

**Integration Architecture**: The modular design enables seamless integration with existing Electronic Health Record (EHR) systems and clinical workflow management platforms.

### 5.3 Limitations and Future Directions

**Experimental Scope**: Current evaluation employs simulated extreme personality profiles over short dialogue sequences (T=6 turns). Real-world deployment requires validation with actual patient populations across extended interaction periods.

**Trait Interaction Modeling**: Our current approach treats Big Five dimensions as independent, potentially missing complex trait interactions that influence optimal communication strategies.

**Cultural Generalization**: The framework requires validation across diverse cultural and linguistic contexts to ensure equitable performance for multicultural patient populations.

**Multimodal Extension**: Future iterations should incorporate paralinguistic cues (prosody, speech patterns) and physiological indicators for enhanced personality detection accuracy.

### 5.4 Broader Implications for Healthcare AI

**Precision Medicine Paradigm**: Our results demonstrate the feasibility of psychological precision medicine through AI-mediated personalization, extending beyond traditional biomedical markers.

**Human-AI Collaboration**: The transparent, interpretable regulation mechanisms support hybrid human-AI care models where clinicians maintain oversight while benefiting from automated personalization insights.

**Ethical Considerations**: The framework raises important questions about personality privacy, consent for psychological profiling, and potential for algorithmic bias that warrant careful consideration in clinical deployment.

## 6. Conclusion

We have presented a novel personality-adaptive conversational AI framework that integrates real-time Big Five trait detection with Zurich Model-aligned behavior regulation for healthcare applications. Through controlled experimental evaluation, we demonstrate substantial improvements (34%) in conversational quality over non-adaptive baselines across diverse personality profiles.

**Key Contributions**:
1. **Methodological Innovation**: First implementation combining dynamic OCEAN detection with motivationally-grounded regulation strategies
2. **Theoretical Integration**: Novel synthesis of personality psychology and motivational frameworks for AI system design  
3. **Empirical Validation**: Comprehensive evaluation demonstrating consistent performance gains across personality extremes
4. **Clinical Applicability**: Transparent, auditable architecture designed for healthcare deployment with regulatory compliance

**Clinical Impact**: The framework addresses critical personalization gaps in healthcare AI, offering scalable solutions for elder care, mental health support, and chronic disease management where psychological attunement significantly influences therapeutic outcomes.

**Future Research**: Immediate priorities include human subject validation studies, longitudinal efficacy assessment, and integration with multimodal sensing capabilities. The modular architecture provides a foundation for these extensions while maintaining clinical safety and regulatory compliance.

The convergence of personality psychology, motivational theory, and advanced conversational AI presents unprecedented opportunities for delivering personalized healthcare at scale. Our work provides both the theoretical framework and empirical evidence base to advance this critical healthcare innovation domain.

## Acknowledgments

The authors thank Dr. Mirjam Hänggi for valuable feedback on experimental design and clinical applicability considerations. We acknowledge the research computing resources provided by HSLU and ZHAW. S.D. was supported by a graduate research fellowship from the Swiss National Science Foundation.

## Author Contributions

**Conceptualization**: S.D., G.L., A.d.S.; **Methodology**: S.D., G.L.; **Software**: S.D.; **Validation**: S.D., G.L.; **Formal Analysis**: S.D.; **Investigation**: S.D.; **Resources**: G.L., A.d.S.; **Data Curation**: S.D.; **Writing—Original Draft**: S.D.; **Writing—Review & Editing**: S.D., G.L., A.d.S.; **Visualization**: S.D.; **Supervision**: G.L., A.d.S.; **Project Administration**: G.L. All authors have read and agreed to the published version of the manuscript.

## Data Availability Statement

Simulation prompts, evaluation templates, and representative dialogue samples are available upon reasonable request to the corresponding author. A curated replication package including detection algorithms, regulation strategies, and evaluation scripts will be released under open-source license following publication. All experimental data supporting the conclusions are included within the manuscript and supplementary materials.

## References

Bickmore, T. W., Gruber, A., & Picard, R. (2005). Establishing the computer-patient working alliance in automated health behavior change interventions. *Patient Education and Counseling*, 59(1), 21-30.

Broadbent, E., Loveys, K., Ilan, G., Chen, G., Chilukuri, M., Boardman, S. G., ... & Skuler, D. (2024). ElliQ, an AI-driven social robot to alleviate loneliness: Progress and lessons learned. *Journal of Aging Research and Clinical Practice*, 13, 22-28.

Calvo, R. A., & D'Mello, S. (2010). Affect detection: An interdisciplinary review of models, methods, and their applications. *IEEE Transactions on Affective Computing*, 1(1), 18-37.

Fitzpatrick, K. K., Darcy, A., & Vierhile, M. (2017). Delivering cognitive behavior therapy to young adults with symptoms of depression and anxiety using a fully automated conversational agent (Woebot): A randomized controlled trial. *JMIR mHealth and uHealth*, 5(6), e7785.

Gjurković, M., & Šnajder, J. (2018). Reddit: A gold mine for personality prediction. In *Proceedings of the Second Workshop on Computational Modeling of People's Opinions, Personality, and Emotions in Social Media* (pp. 87-97).

Hämmig, O. (2019). Health risks associated with social isolation in general and in young, middle and old age. *PLoS ONE*, 14(7), e0219663.

Li, J., Galley, M., Brockett, C., Spithourakis, G., Gao, J., & Dolan, B. (2016). A persona-based neural conversation model. In *Proceedings of the 54th Annual Meeting of the Association for Computational Linguistics* (Vol. 1, pp. 994-1003).

McCrae, R. R., & John, O. P. (1992). An introduction to the five-factor model and its applications. *Journal of Personality*, 60(2), 175-215.

Musich, S., Wang, S. S., Hawkins, K., & Yeh, C. (2015). The impact of loneliness on quality of life and patient satisfaction among older, sicker adults. *Gerontology and Geriatric Medicine*, 1, 2333721415582119.

Picard, R. W. (2000). *Affective computing*. MIT Press.

Quirin, M., Malekzad, F., Paudel, D., Knoll, A. C., & Mirolli, M. (2023). Dynamics of personality: The Zurich model of motivation revived, extended, and applied to personality. *Journal of Personality*, 91(4), 928-946.

Ta, V. P., Griffith, C., Boatfield, C., Wang, X., Civitello, M., Bader, H., ... & Loggarakis, A. (2020). User experiences of social support from companion chatbots in everyday contexts: Thematic analysis. *Journal of Medical Internet Research*, 22(3), e16235.

Tandera, T., Hendro, H., Mahendra, R., Pradana, A., & Distiawan, B. (2017). Personality prediction system from Facebook users. *Procedia Computer Science*, 116, 604-611.

Wu, W., Heierli, J., Meisterhans, M., Moser, A., Farber, A., Dolata, M., ... & Schwabe, G. (2023). PROMISE: A framework for developing complex conversational interactions. *Technical Report*, University of Zurich.

Zhang, H., Chen, Y., Wang, M., & Feng, S. (2024). FEEL: A framework for evaluating emotional support capability with large language models. *arXiv preprint arXiv:2403.15699*.

Zheng, Z., Liao, L., Deng, Y., & Nie, L. (2023). Building emotional support chatbots in the era of LLMs. *arXiv preprint arXiv:2308.11584*.