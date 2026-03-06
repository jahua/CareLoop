---
title: "Personality-Adaptive Conversational AI for Emotional Support: A Simulation Study Using Big Five Detection and Zurich Model Regulation"
documentclass: article
geometry: "a4paper, top=1.5cm, bottom=3.5cm, left=1.75cm, right=1.75cm"
fontfamily: "times"
fontsize: "12pt"
linestretch: 1.5
numbersections: true
secnumdepth: 3
indent: true
header-includes:
  - \usepackage{setspace}
  - \onehalfspacing
  - \usepackage{amsmath}
  - \usepackage{amsfonts}
  - \usepackage{amssymb}
  - \usepackage{graphicx}
  - \usepackage{booktabs}
  - \usepackage{longtable}
  - \usepackage{array}
  - \usepackage{multirow}
  - \usepackage{wrapfig}
  - \usepackage{float}
  - \usepackage{colortbl}
  - \usepackage{pdflscape}
  - \usepackage{tabu}
  - \usepackage{threeparttable}
  - \usepackage{threeparttablex}
  - \usepackage[normalem]{ulem}
  - \usepackage{makecell}
  - \usepackage{xcolor}
---

## Abstract 

**Background**: Conversational agents often lack adaptive mechanisms that account for individual personality differences, limiting personalized interaction quality. This gap is particularly relevant for applications in mental health, elder care, and social support contexts.

**Objective**: To evaluate the technical feasibility of a personality-adaptive framework that detects Big Five (OCEAN) traits in real time and modulates conversational behavior via Zurich Model–aligned regulation through controlled simulation.

**Methods**: We implemented a modular system comprising: (i) discrete OCEAN detection {−1, 0, +1} with cumulative refinement using prompt-based personality trait inference; (ii) trait‑to‑motivational domain mapping (security, arousal, affiliation) grounded in established psychological theory; and (iii) dynamic behavior adaptation. The system was evaluated through controlled simulation using two extreme personality profiles (Type A: all traits +1; Type B: all traits −1) against non‑adaptive baselines. Ten simulated conversations (6-turn dialogues per conversation) were conducted comparing personality-adaptive agents to baseline agents across both personality types, assessed using a structured GPT‑4 evaluator with comprehensive scoring matrix.

**Results**: In simulation, regulated agents demonstrated substantially superior performance in personality-specific adaptation. Detection accuracy reached 100% (58/58 correct assessments) for extreme simulated profiles with perfect regulation effectiveness (59/59, 100%). The largest effect was observed for Personality Needs Addressed, where regulated agents achieved 100% success compared to baseline's 8.62% (Cohen's d = 4.58, p < 0.001), representing a 91.38 percentage point improvement. Both conditions performed equivalently on Emotional Tone (100% vs 100%) and Relevance & Coherence (100% vs 98.33%), indicating that personality adaptation specifically enhanced personalization without compromising basic conversational quality. 

**Conclusions**: Simulation results demonstrate technical feasibility of personality‑adaptive conversational systems using real-time detection and theoretically-grounded behavior regulation. The proof-of-concept framework addresses personalization gaps in conversational AI while establishing requirements for future validation with real users. Findings should be interpreted as simulation-based technical demonstration requiring extensive human subject validation before any real-world deployment.

**Keywords:** conversational agents; personality detection; adaptive interaction; Big Five; Zurich Model; simulation study; behavior regulation; proof-of-concept; healthcare AI; mental health

# Introduction

## Background and Motivation

Loneliness in older adults represents a persistent public health concern with far-reaching implications for both physical and mental health outcomes. Epidemiological studies have consistently demonstrated that social isolation and loneliness are associated with elevated morbidity and mortality rates comparable to established risk factors such as obesity and smoking [1]. In Switzerland and other developed nations, demographic factors including living alone, multimorbidity, and mobility limitations contribute to increased social disconnection among elderly populations [2]. This demographic trend is not unique to Switzerland; rather, it reflects a global phenomenon that demands urgent attention from healthcare systems, policymakers, and technology developers.

The aging population crisis presents unprecedented challenges for healthcare systems worldwide. According to the United Nations, the global population aged 60 years and older is projected to reach 2.1 billion by 2050, representing more than 20% of the world's population, with approximately 80% residing in low- and middle-income countries [5]. This demographic shift creates extraordinary demand for scalable, personalized healthcare solutions that can address not only physical health needs but also the critical psychosocial dimensions of well-being. Traditional healthcare delivery models, which rely primarily on in-person consultations and standardized treatment protocols, are increasingly inadequate to meet the diverse and complex needs of this expanding elderly population.

In response to these challenges, conversational agents—also referred to as chatbots, virtual assistants, or conversational artificial intelligence (AI) systems—have emerged as promising tools for delivering healthcare screening, promoting treatment adherence, and providing psychosocial support [3,4]. These systems offer several advantages: they are available 24/7, can serve unlimited numbers of users simultaneously, maintain consistency in service delivery, and can be deployed at scale with relatively low marginal costs. Recent implementations have demonstrated effectiveness in mental health screening, medication adherence support, and basic emotional companionship for isolated populations.

However, despite these promising developments, current conversational agents in healthcare contexts suffer from a fundamental limitation: most systems rely on uniform, one-size-fits-all interaction strategies that fail to account for individual psychological differences. This standardization overlooks substantial evidence from personality psychology demonstrating that individual differences in personality traits significantly influence communication preferences, therapeutic alliance formation, and treatment outcomes. The absence of personality-aware adaptation in current systems represents a critical gap that limits both the effectiveness and the acceptability of conversational AI in healthcare applications.

## Current State of Personality-Aware Conversational AI

Personality-aware interaction has been proposed as a potential solution to the limitations of standardized conversational systems. The Big Five personality model (also known as the Five-Factor Model or OCEAN model), which conceptualizes personality along five broad dimensions—Openness to Experience, Conscientiousness, Extraversion, Agreeableness, and Neuroticism—has emerged as the dominant framework for personality representation in computational systems due to its empirical validation, cross-cultural applicability, and theoretical parsimony [9]. However, existing implementations of personality-aware conversational systems exhibit several critical shortcomings that limit their practical applicability.

First, many current systems employ static personality profiles established through one-time initialization, typically using explicit personality questionnaires administered before the conversation begins. This approach suffers from multiple limitations: it imposes additional user burden, may yield inaccurate results due to self-report biases, remains fixed throughout the interaction regardless of emerging behavioral evidence, and fails to capture the dynamic nature of personality expression in conversational contexts. Second, even systems that attempt dynamic personality inference often lack theoretical grounding in established motivational psychology frameworks, resulting in ad-hoc adaptation strategies that may not align with psychological theory or established best practices. Third, existing evaluation frameworks for personality-aware systems focus primarily on user satisfaction and engagement metrics, neglecting systematic assessment of therapeutic appropriateness, user safety, and alignment with individual psychological needs—dimensions that are critical for healthcare applications.

## Research Gaps and Study Motivation

Through systematic review of existing literature and current implementations, we identify three critical research gaps that this study addresses:

**Gap 1: Static Versus Dynamic Personality Detection**. Most existing conversational AI systems—including systems like PROMISE [7] and personality-aligned prompting frameworks—rely on static personality profiles established through one-time initialization using explicit questionnaires administered before conversations begin. This approach fails to capture the dynamic nature of personality expression as conversations unfold and cannot adapt to emerging behavioral evidence throughout dialogue turns. The static approach imposes user burden through explicit assessment, may yield inaccurate results due to self-report biases, and remains fixed throughout the interaction regardless of observable personality cues emerging during conversation. In contrast, a continuous, real-time detection-regulation loop that progressively refines personality estimates based on linguistic and behavioral cues throughout the conversation represents an essential but underexplored capability for healthcare applications, particularly for emotionally vulnerable populations where subtle personality cues may emerge gradually during therapeutic dialogue.

**Gap 2: Lack of Theoretically-Grounded Psychological Regulation Frameworks**. A critical gap exists in systems that explicitly operationalize psychological regulation theories to guide conversational behavior adaptation. While systems like EmoAda and evaluation frameworks like FEEL advance emotion tracking and assessment, few systematically translate personality traits into behavior modifications grounded in established motivational psychology frameworks. Most personality-aware systems employ ad-hoc adaptation strategies without explicit connection to psychological theory regarding how and why chatbot behavior should adapt. This absence of theoretical foundation raises fundamental concerns about the psychological validity and therapeutic appropriateness of personality-based adaptations. The Zurich Model of Social Motivation—which conceptualizes human behavior through three core motivational domains (security, arousal, and affiliation) with systematic mappings to Big Five personality traits [11]—provides a theoretically-grounded framework for translating detected traits into appropriate behavioral modifications, yet remains underexplored in conversational AI behavior regulation.

**Gap 3: Rigorous Evaluation of Adaptive Effectiveness with Systematic Frameworks**. Better evaluation methods are needed that can rigorously examine adaptive effectiveness in controlled personality scenarios. Existing evaluation methodologies focus predominantly on generic metrics such as user satisfaction, engagement duration, and perceived naturalness, which are insufficient for assessing the quality of personality-specific adaptation. These generic metrics fail to evaluate detection accuracy, regulation effectiveness, therapeutic appropriateness, or alignment with individual psychological needs—dimensions critical for assessing personality-adaptive systems in healthcare contexts. Comprehensive, multi-dimensional evaluation frameworks specifically designed for personality-adaptive healthcare conversational AI remain absent from the literature, highlighting the need for systematic assessment approaches that enable traceable evaluation of personality-specific adaptation quality.

## Study Objectives and Key Innovations

This study demonstrates the technical feasibility and performance improvements achievable through real-time personality detection coupled with theoretically-grounded behavioral regulation in controlled experimental conditions for healthcare applications.

**Research Hypothesis**: We hypothesize that conversational agents incorporating real-time Big Five personality detection and Zurich Model-aligned behavior regulation will demonstrate significantly higher conversational quality (>20% improvement) compared to non-adaptive baseline agents across multiple evaluation dimensions (detection accuracy, regulation effectiveness, emotional tone, relevance, and personality needs addressed) in simulation with extreme personality profiles.

The study presents three core technical innovations addressing the identified gaps, alongside a real-world translation framework for healthcare deployment:

**Innovation 1: Real-Time OCEAN Detection with Cumulative Refinement** (Addressing Gap 1: Static vs. Dynamic Detection). We implemented a prompt-based personality inference system that continuously analyzes user utterances to detect Big Five (OCEAN) personality traits in real time through cumulative refinement. Unlike static initialization approaches prevalent in systems like PROMISE [7], the system progressively updates personality estimates as conversational evidence accumulates across dialogue turns. The detection system employs discrete trait encoding {−1, 0, +1} with neutral defaults (0) maintained until sufficient linguistic evidence emerges, preventing premature misclassification while enabling dynamic adaptation to evolving personality cues. This continuous detection-regulation loop directly addresses the gap of static, one-time personality initialization that fails to capture the dynamic nature of personality expression during conversations.

**Innovation 2: Zurich Model-Aligned Behavior Regulation** (Addressing Gap 2: Lack of Theoretical Grounding). We operationalized the Zurich Model of Social Motivation [11] to establish explicit, psychologically-grounded mappings between detected Big Five traits and three core motivational domains: Security Domain (N → emotional stability/vulnerability responses addressing safety needs), Arousal Domain ({O,E} → novelty/stimulation regulation managing exploration preferences), and Affiliation Domain (A → social connection/cooperation strategies modulating interpersonal engagement). This theoretically-grounded approach directly addresses the gap of ad-hoc adaptation strategies in existing systems, ensuring that personality-based behavioral modifications align with established motivational psychology theory rather than arbitrary design choices. The trait-to-regulation mapping provides the psychological validity and interpretability essential for healthcare contexts.

**Innovation 3: Multi-Dimensional Evaluation Framework** (Addressing Gap 3: Rigorous Adaptive Evaluation). We developed a novel Evaluation Matrix scored by a custom "Evaluator GPT" to enable traceable, turn-by-turn assessment of personality-adaptive conversational quality. The framework systematically assesses five key dimensions: (i) detection accuracy—correctness of personality trait inference across dialogue turns; (ii) regulation effectiveness—appropriateness of trait-driven behavioral adaptations; (iii) emotional tone appropriateness—therapeutic suitability of affective responses for detected personality profiles; (iv) relevance and coherence—logical consistency and contextual appropriateness of responses; and (v) personality needs addressed—degree of alignment with individual psychological requirements. This multi-dimensional approach enables rigorous examination of adaptive effectiveness in controlled, high-contrast personality scenarios, addressing the limitation of generic evaluation metrics that fail to assess personality-specific adaptation quality.

**Innovation 4: Real-World Translation Roadmap and Healthcare Deployment Pathway**. Beyond demonstrating technical feasibility through simulation-based evaluation, we provide an explicit real-world translation roadmap that operationalizes the validation requirements into a structured framework for healthcare deployment. The roadmap specifies concrete requirements for transition from proof-of-concept to clinical deployment: (i) human subject validation protocols with validated personality assessments (NEO-PI-R, BFI-2) including minimum sample sizes (n=50+) and study designs (RCTs); (ii) domain expert evaluation frameworks by licensed healthcare professionals; (iii) comprehensive safety validation procedures addressing misclassification risks, cultural bias, therapeutic harm, and privacy concerns; (iv) cultural adaptation and testing protocols across diverse populations; (v) longitudinal assessment protocols (minimum 30 days) for sustained effectiveness; (vi) regulatory compliance pathways (IRB approval, HIPAA/GDPR, FDA guidance) with specific requirements; and (vii) healthcare system integration specifications including EHR integration and healthcare workflow considerations. This framework addresses the critical gap between simulation-based proof-of-concept research and deployable healthcare systems.

## Expected Contributions and Simulation-Based Findings

The primary contribution of this work is demonstrating the technical feasibility of personality-adaptive conversational systems through controlled simulation. Results show that in simulated scenarios, regulated agents incorporating real-time personality detection and Zurich Model-aligned behavior regulation achieve perfect detection accuracy (100%, n=58) and regulation effectiveness (100%, n=59). Most critically, personality adaptation dramatically improved the system's ability to address personality-specific needs: regulated agents achieved 100% success compared to baseline's 8.62%, representing a 91.38 percentage point improvement with very large effect size (Cohen's d = 4.58, p < 0.001). Notably, both conditions performed equivalently on fundamental conversational quality metrics (Emotional Tone: 100% vs 100%; Relevance & Coherence: 100% vs 98.33%), demonstrating that personality adaptation enhanced personalization without compromising basic interaction quality.

These simulation-based findings provide several insights for conversational AI development. First, the performance improvements in controlled scenarios suggest that personality-aware adaptation is technically feasible and may warrant investigation with real users. Second, the successful integration of the Zurich Model demonstrates that established psychological theory can be operationalized to guide AI behavior adaptation in systematic, interpretable ways. Third, the multi-dimensional evaluation framework provides a replicable methodology for assessing personality-adaptive conversational systems in controlled experimental settings.

The potential relevance of this work extends to three application domains that could benefit from personalized conversational systems: (i) mental health support tools, where personalized communication may enhance user engagement; (ii) elder care companion systems, where individual differences in personality may influence technology acceptance; and (iii) social support applications, where sustained user engagement depends on appropriate interaction styles. However, these potential applications require extensive validation with real users before any claims about effectiveness or therapeutic outcomes can be made.

## Study Limitations and Scope

It is essential to explicitly acknowledge the limitations and scope of this research. This study employs a simulation-based approach using synthetic personality profiles and AI-based evaluation rather than real user interactions and human expert assessment. Consequently, findings should be interpreted strictly as proof-of-concept evidence demonstrating technical feasibility under controlled conditions, NOT as evidence of real-world effectiveness or real-world utility. The simulation approach enables systematic experimentation with extreme personality profiles and controlled comparison of regulated versus baseline performance, but introduces critical limitations regarding ecological validity and generalizability.

Specifically, the study focuses on extreme personality profiles (all traits at +1 or −1) to maximize detection signal and enable clear demonstration of regulation effects. Performance with moderate personality expressions remains completely untested. The evaluation employs a custom GPT-4-based assessor rather than human evaluators, potentially introducing bias favoring AI-generated responses and lacking the professional judgment necessary for healthcare applications. The short interaction duration (6 dialogue turns) is insufficient to assess sustained relationships or long-term engagement. Cultural considerations are limited to English-speaking contexts, and the text-only modality excludes potentially informative paralinguistic cues. Most critically, NO real users were involved—all interactions were between simulated personality profiles and the chatbot system.

These fundamental limitations mean the work remains at the proof-of-concept stage. Future research must include: (i) human subject studies with real users and validated personality assessments; (ii) human expert evaluation by domain specialists (psychologists, healthcare professionals); (iii) comprehensive safety validation; (iv) cultural adaptation and testing across diverse populations; (v) longitudinal assessment protocols; and (vi) regulatory compliance frameworks. Only through such extensive validation can any claims about real-world applicability, user benefit, or healthcare utility be made. The real-world translation roadmap provided in this paper outlines these requirements but does not constitute human subject validation.

## Paper Structure

The remainder of this paper is organized as follows: Section 2 (Related Work) provides a comprehensive review of existing research on personality-aware dialogue systems, affective computing, and conversational AI evaluation methodologies, situating this work within the broader research landscape. Section 3 (Materials and Methods) describes the simulation study design, system architecture, personality detection module, behavior regulation module, and experimental protocol in detail. Section 4 (Results) presents quantitative performance metrics from simulation and qualitative examples demonstrating the technical implementation of personality-adaptive regulation. Section 5 (Discussion) interprets the simulation findings, compares results with existing literature, outlines requirements for future human subject validation, acknowledges limitations, and proposes next research steps. Section 6 (Conclusions) summarizes the key technical contributions and implications of this simulation-based proof-of-concept for future conversational AI research.

# Related Work

This section provides a comprehensive review of research relevant to personality-adaptive conversational AI with potential applications in supportive interaction contexts. We organize the review into five thematic areas: (1) personality models and detection methods, (2) personality-aware dialogue systems, (3) affective computing and emotional support systems, (4) motivational psychology frameworks for behavior regulation, and (5) evaluation methodologies for conversational AI.

## Personality Models and Detection Methods

The Big Five personality model, also known as the Five-Factor Model (FFM) or OCEAN model, represents the most widely validated framework for personality assessment in psychological research [9]. This model characterizes personality along five broad dimensions: Openness to Experience (imagination, curiosity, intellectual engagement), Conscientiousness (organization, goal-directedness, self-discipline), Extraversion (sociability, energy, assertiveness), Agreeableness (cooperation, empathy, trust), and Neuroticism (emotional instability, anxiety, vulnerability). Extensive cross-cultural research has demonstrated the robustness and generalizability of this model across diverse populations, languages, and measurement methods, making it an ideal foundation for computational personality systems.

Computational personality detection methods can be broadly categorized into three approaches: questionnaire-based explicit assessment, behavioral inference from digital traces, and linguistic analysis of conversational content. Questionnaire-based methods, such as the NEO Personality Inventory-Revised (NEO-PI-R) and the Big Five Inventory (BFI), provide validated psychometric instruments but impose user burden and may suffer from social desirability bias. Behavioral inference approaches analyze digital footprints such as social media activity, smartphone usage patterns, and online browsing behavior to infer personality traits. While these methods enable unobtrusive assessment, they raise privacy concerns and may not be applicable in healthcare contexts with strict data protection requirements.

Linguistic analysis methods, which infer personality traits from textual communication, have gained prominence in conversational AI research. Mairesse et al. (2007) pioneered computational personality recognition from text, achieving moderate correlations with self-reported personality scores using linguistic features extracted from essays and blog posts. Schwartz et al. (2013) demonstrated that language use on Facebook predicts Big Five personality traits, establishing large-scale benchmarks for text-based personality prediction. More recently, deep learning approaches using transformer-based language models have achieved state-of-the-art performance on personality detection tasks, though questions remain about their interpretability and robustness across diverse conversational contexts.

The majority of personality detection research has focused on offline analysis of substantial text corpora (e.g., social media history, essays) rather than real-time inference from ongoing conversations. This distinction is critical for conversational AI applications, where personality estimates must be formed and updated dynamically as the conversation progresses. Real-time personality detection faces unique challenges including limited linguistic evidence in early conversation turns, the need for computationally efficient inference methods, and the requirement for graceful handling of uncertain or ambiguous trait expressions. Our work addresses these challenges through prompt-based personality inference with cumulative refinement, enabling real-time adaptation while maintaining detection accuracy.

## Personality-Aware Dialogue Systems

The field of personality-aware dialogue systems has evolved significantly over the past decade. Early research focused primarily on generating responses that exhibit specific personality traits rather than adapting to user characteristics. Li et al. (2016) introduced persona-based neural conversation models that generate responses consistent with predefined personality profiles, representing an important step toward personality-aware dialogue but without actual user personality detection [6]. Zhang et al. (2018) extended this work by conditioning response generation on explicit persona descriptions, enabling more controlled personality expression in dialogue agents.

Subsequent research has attempted to incorporate user personality detection into conversational systems. Mairesse and Walker (2010) developed PERSONAGE, a natural language generation system that adapts linguistic style based on Big Five personality traits, demonstrating that personality-aware language generation improves perceived naturalness and appropriateness. However, PERSONAGE relies on explicit personality initialization rather than dynamic inference from conversation.

More recently, the PROMISE framework developed by Wu et al. (2023) represents notable advancement by implementing modular personality detection with behavioral adaptation [7]. PROMISE separates personality inference, dialogue state tracking, and response generation into distinct components, enabling more flexible system design. The framework demonstrates improved user satisfaction compared to non-adaptive baselines in customer service scenarios. However, PROMISE exhibits several limitations for healthcare applications: it lacks theoretical grounding in motivational psychology frameworks, does not address healthcare-specific requirements such as therapeutic appropriateness and patient safety, and has not been validated in healthcare contexts.

Other recent work has explored personality adaptation in specific domains. Zhou et al. (2021) developed a personality-adaptive persuasion dialogue system that adjusts argumentation strategies based on detected user traits, showing improved persuasion effectiveness. Shumanov and Johnson (2021) investigated personality matching effects in customer service chatbots, finding that personality similarity between user and agent enhances satisfaction but may not optimize task performance. These studies demonstrate the potential value of personality adaptation but remain limited to narrow application domains without consideration of healthcare requirements.

A critical gap in existing personality-aware dialogue systems is the absence of theoretically-grounded frameworks for translating detected personality traits into appropriate behavioral adaptations. Most systems employ ad-hoc adaptation strategies without explicit connection to established psychological theory. This lack of theoretical grounding raises concerns about the psychological validity of personality-based adaptations and limits the interpretability and trustworthiness of such systems, particularly in healthcare contexts where therapeutic appropriateness is paramount.

## Affective Computing and Emotional Support in Healthcare

Affective computing—the development of systems that can recognize, interpret, and respond to human emotions—has become increasingly relevant to healthcare applications. Calvo and D'Mello (2010) provided a comprehensive interdisciplinary review of affect detection methods and applications, establishing theoretical foundations for emotion-aware systems [8]. Subsequent research has demonstrated that emotionally intelligent conversational agents can improve user engagement, therapeutic alliance, and treatment outcomes in mental health contexts.

Several emotional support chatbots have been developed for healthcare applications. Woebot, a cognitive behavioral therapy (CBT) chatbot, has demonstrated effectiveness in reducing depression and anxiety symptoms in young adults through structured therapeutic conversations [3]. Fitzpatrick et al. (2017) showed that fully automated conversational agents can deliver significant improvements in mental health outcomes, challenging traditional assumptions about the necessity of human therapists for all interventions. Similarly, Ly et al. (2017) found that smartphone-based mental health interventions using conversational interfaces achieved comparable outcomes to face-to-face therapy for certain conditions.

Recent advances in large language models (LLMs) have enabled more sophisticated emotional support capabilities. Zheng et al. (2023) explored building emotional support chatbots in the era of LLMs, demonstrating improved empathetic response generation through fine-tuning on emotional support conversation datasets [9]. Sharma et al. (2023) developed DialoGPT-based systems that generate contextually appropriate emotional support responses, outperforming earlier template-based approaches. However, these systems focus primarily on emotional expression without systematic personality-based adaptation.

Healthcare-specific conversational AI faces unique deployment challenges beyond technical performance. Privacy concerns arise from the collection and analysis of sensitive psychological data, particularly when multimodal sensing (voice, facial expressions, physiological signals) is employed. Cultural bias in emotion recognition represents another significant challenge, as emotional expression norms vary substantially across cultures, potentially leading to misinterpretation and inappropriate responses for non-Western populations. Regulatory compliance for medical AI systems adds further complexity, as healthcare applications must satisfy stringent requirements for safety, efficacy, and data protection under frameworks such as FDA guidance in the United States and the Medical Device Regulation (MDR) in the European Union.

ElliQ, an AI-driven social robot designed to alleviate loneliness in older adults, represents a notable implementation of affective computing principles in elder care [4]. Broadbent et al. (2024) reported that ElliQ successfully increased social engagement and reduced perceived loneliness among elderly users through proactive conversation initiation and personalized content delivery. However, ElliQ does not implement explicit personality detection or theoretically-grounded personality adaptation, relying instead on implicit personalization through usage pattern learning.

Despite these advances, current emotional support chatbots lack systematic frameworks for personality-based adaptation. While these systems demonstrate empathetic response generation, they do not explicitly model or adapt to individual differences in personality traits that significantly influence therapeutic effectiveness. The integration of personality detection with emotional support capabilities represents a critical opportunity for advancing healthcare conversational AI.

## Motivational Psychology Frameworks for Behavior Regulation

The Zurich Model of Social Motivation, proposed by Bischof (1975, 1985) and recently extended by Quirin et al. (2023), provides a comprehensive framework for understanding human behavior through three core motivational systems [11]. The Security System regulates behavior aimed at achieving safety, stability, and protection from threats; when activated, it prompts security-seeking behaviors such as attachment, comfort-seeking, and risk avoidance. The Arousal System governs motivation for stimulation, exploration, and novelty; activation of this system drives exploratory behavior, information-seeking, and engagement with novel experiences. The Affiliation System manages social bonding, cooperation, and interpersonal connection; when active, it promotes prosocial behavior, empathy, and collaborative activities.

Quirin et al. (2023) demonstrated that the Zurich Model's three motivational domains map systematically onto Big Five personality traits, providing a theoretical bridge between personality description and motivational dynamics [11]. Specifically, Neuroticism correlates negatively with security system regulation, high Openness and Extraversion associate with arousal system activation, and Agreeableness relates to affiliation system dominance. This mapping suggests that personality traits can be understood as stable individual differences in the relative strengths and sensitivities of these three motivational systems.

The Zurich Model has been successfully applied to understanding diverse psychological phenomena including emotional regulation, interpersonal relationships, and psychopathology. Kobyliński et al. (2020) demonstrated that motivational system dynamics mediate the relationship between personality and emotional regulation strategies, with arousal-dominant individuals preferring cognitive reappraisal while security-dominant individuals favor emotional suppression. However, despite its theoretical richness and empirical validation, the Zurich Model has not previously been applied to guide conversational AI behavior regulation.

Other motivational frameworks have been proposed for understanding human behavior. Self-Determination Theory (SDT) posits three basic psychological needs—autonomy, competence, and relatedness—that drive human motivation and well-being. Reinforcement Sensitivity Theory (RST) conceptualizes motivation through behavioral activation and inhibition systems responsive to reward and punishment signals. While these frameworks offer valuable insights, the Zurich Model's explicit mapping to Big Five personality traits and its comprehensive coverage of security, arousal, and affiliation domains make it particularly well-suited for personality-adaptive conversational systems.

The integration of motivational psychology frameworks with conversational AI represents an underexplored opportunity. By grounding behavioral adaptations in established psychological theory, systems can achieve greater therapeutic appropriateness, interpretability, and trustworthiness. Our work represents the first implementation of Zurich Model-aligned behavior regulation in a conversational AI system, establishing explicit mappings between detected Big Five traits and motivational domain-specific regulatory strategies.

## Evaluation Methodologies for Healthcare Conversational AI

Evaluating conversational AI systems for healthcare applications presents unique challenges that extend beyond traditional dialogue system evaluation. Standard metrics such as BLEU (bilingual evaluation understudy) and ROUGE (recall-oriented understudy for gisting evaluation) focus on surface-level linguistic similarity between generated and reference responses, providing little insight into therapeutic appropriateness, user safety, or patient-centeredness. Perplexity-based metrics assess language model quality but do not evaluate whether responses are therapeutically appropriate or psychologically beneficial.

User-centered evaluation metrics, including user satisfaction, engagement duration, and net promoter scores, provide important information about subjective experience but may not correlate with therapeutic effectiveness. Patients may report high satisfaction with systems that provide comforting but suboptimal advice, or may undervalue systems that deliver evidence-based but initially uncomfortable interventions. Thus, satisfaction metrics alone are insufficient for healthcare evaluation.

Healthcare outcome metrics represent the gold standard for evaluating healthcare interventions, including conversational AI systems. For mental health applications, validated instruments such as the Patient Health Questionnaire-9 (PHQ-9) for depression, Generalized Anxiety Disorder-7 (GAD-7) for anxiety, and WHO-5 Well-Being Index provide standardized outcome assessment. Longitudinal randomized controlled trials comparing conversational AI interventions to standard care or active controls enable rigorous evaluation of effectiveness. However, such trials require substantial resources, time, and regulatory compliance, making them impractical for iterative system development.

Several frameworks have been proposed for evaluating conversational AI in healthcare contexts. Laranjo et al. (2018) developed a systematic evaluation framework for health chatbots incorporating dimensions of content accuracy, user safety, user experience, and technical performance. Milne-Ives et al. (2020) proposed quality criteria for mental health apps including evidence-based content, professional credibility, user privacy, and engagement features. However, these frameworks do not address personality-specific adaptation or provide operationalized metrics for assessing personalization quality.

Recent work has begun to explore LLM-based evaluation approaches, where large language models serve as automated assessors of conversation quality. Liu et al. (2023) demonstrated that GPT-4 can reliably evaluate dialogue system responses across multiple dimensions including relevance, informativeness, and naturalness, achieving correlation with human judgments comparable to inter-rater reliability. Zheng et al. (2023) developed Chatbot Arena, a crowdsourced platform using LLM-based evaluation to compare conversational AI systems. While LLM-based evaluation offers scalability and consistency advantages, concerns remain about potential biases, limited domain expertise, and circular reasoning when evaluating LLM-generated outputs using LLM assessors.

Our evaluation framework addresses these challenges by incorporating multiple assessment dimensions specifically relevant to personality-adaptive healthcare conversational AI: detection accuracy (correctness of personality inference), regulation effectiveness (appropriateness of personality-based behavioral adaptations), emotional tone appropriateness (therapeutic suitability of affective responses), relevance and coherence (logical consistency and contextual appropriateness), and personality needs addressed (alignment with individual psychological requirements). This multi-dimensional approach provides comprehensive assessment while acknowledging the limitations of simulation-based evaluation and the necessity for subsequent human subject validation.

## Summary of Literature Gaps

Based on this comprehensive review, we synthesize three critical research gaps that guide this study:

1. **Static Versus Dynamic Personality Detection**: Current systems (including PROMISE [7] and personality-aligned prompting frameworks) rely on static, one-time personality initialization through explicit questionnaires or fixed profiles administered before conversations begin. This approach fails to capture the dynamic nature of personality expression as conversations unfold and cannot adapt to emerging behavioral evidence throughout dialogue turns. The static approach imposes user burden, may yield inaccurate results due to self-report biases, and remains fixed throughout interactions regardless of observable personality cues emerging during conversation. Real-time personality detection with cumulative refinement—where trait estimates are continuously updated based on linguistic cues throughout the conversation—represents an essential but underexplored capability for healthcare applications.

2. **Lack of Theoretically-Grounded Psychological Regulation Frameworks**: A critical gap exists in systems that explicitly operationalize psychological regulation theories to guide conversational behavior adaptation. While systems like EmoAda and FEEL advance emotion tracking, few systematically translate personality traits into behavior modifications grounded in established motivational psychology frameworks. Most personality-aware dialogue systems employ ad-hoc adaptation strategies without principled connection to psychological theory regarding how and why chatbot behavior should adapt, raising fundamental concerns about psychological validity and therapeutic appropriateness. The Zurich Model of Social Motivation [11]—with its systematic mapping of Big Five traits to motivational domains (security, arousal, affiliation)—provides a theoretically-grounded framework yet remains underexplored in conversational AI behavior regulation.

3. **Rigorous Evaluation of Adaptive Effectiveness**: Better evaluation methods are needed that can rigorously examine adaptive effectiveness in controlled personality scenarios. Existing evaluation methodologies emphasize generic metrics (user satisfaction, engagement duration, perceived naturalness) insufficient for assessing personality-specific adaptation quality. These generic metrics fail to evaluate detection accuracy, regulation effectiveness, therapeutic appropriateness, or alignment with individual psychological needs—dimensions critical for assessing personality-adaptive systems in healthcare contexts. Comprehensive, multi-dimensional evaluation frameworks specifically designed for personality-adaptive healthcare conversational AI remain absent from the literature.

**Study Contribution**: This work addresses these three gaps by presenting: (i) real-time Big Five detection with cumulative refinement enabling continuous detection-regulation loops; (ii) Zurich Model-aligned behavior regulation providing theoretically-grounded trait-to-motivation mappings [11]; and (iii) a novel multi-dimensional Evaluation Matrix with custom "Evaluator GPT" for traceable, turn-by-turn assessment. Additionally, we contribute a comprehensive real-world translation roadmap—operationalizing validation requirements into concrete pathways for healthcare deployment including human subject protocols, domain expert evaluation, safety validation, cultural adaptation, regulatory compliance, and healthcare system integration specifications.

# Materials and Methods

## Study Design

This simulation study employed a controlled experimental design comparing personality-adaptive (regulated) versus static (baseline) conversational agents across extreme personality profiles. The study protocol was designed as proof-of-concept research using simulated interactions to establish technical feasibility and evaluate performance improvements under controlled conditions.

**Experimental Structure**: The study employed a 2×2 factorial design comparing two assistant types (regulated vs. baseline) across two personality profiles (Type A vs. Type B). Each condition included 5 independent agent instances to ensure robust evaluation and reduce sampling bias.

**Control Mechanisms**: Baseline agents served as control conditions, providing identical supportive responses without personality adaptation. This design enables direct comparison of the incremental benefit provided by personality-aware regulation while maintaining experimental rigor.

**Statistical Analysis**: Performance was evaluated using a comprehensive statistical framework combining descriptive statistics, effect size analysis, and inferential testing. Evaluation outcomes were obtained from the structured evaluation matrix with categorical judgments (Yes / No / Not Sure) across regulated and baseline assistants, which were then converted to quantitative metrics for statistical analysis.

Specifically:

* **Descriptive statistics** (means, standard deviations, and confidence intervals) were calculated for each evaluation metric (detection accuracy, regulation effectiveness, emotional tone, relevance and coherence, and personality needs addressed).
* **Effect sizes (Cohen's d)** were computed to estimate the magnitude of differences between regulated and baseline assistants, providing standardized measures of practical significance independent of sample size.
* **Inferential statistics** (independent t-tests and Mann-Whitney U tests) were conducted to assess statistical significance. Given the deterministic nature of the simulation design using predefined personality types (Type A and Type B), inferential statistics are included for methodological completeness and to facilitate comparisons with related empirical studies, but should not be interpreted as evidence of generalizable population effects.
* **Reliability analysis** (Cronbach's alpha) was performed to assess internal consistency of the evaluation metrics.

This comprehensive statistical framework enables transparent and rigorous reporting of simulation-based results while acknowledging the limitations of the controlled experimental design, and provides a foundation for future work involving real-user trials where inferential analysis would support population-level generalizations.

**Sample Size Justification**: The study employed 20 total agents (10 per personality type) with 6 dialogue turns each, generating 120 total dialogue turns for analysis. This sample size provides sufficient statistical power to detect meaningful differences between regulated and baseline conditions while maintaining manageable computational requirements for simulation-based evaluation.

**Ethics Statement**: No human subjects were directly involved in the study, as all conversations used for testing were simulated interactions between predefined personality profiles (Type A and Type B) and the chatbot. Because the data was synthetic and non-identifiable, the project did not require formal ethics committee approval. Ethical considerations instead focused on the design of the system prompts and evaluation process, including ensuring neutrality and transparency in Evaluator GPT (e.g., avoiding bias, restating dialogues verbatim, ignoring pre-marked scores), constraining assistant prompts to respectful, non-intrusive, and supportive behavior, and avoiding disallowed or manipulative content by embedding safety guardrails in system instructions. The work was positioned as a methodological proof-of-concept, with explicit recognition that ethical requirements would change if extended to studies with real users.

## System Architecture

Our framework implements a modular pipeline A = (D, R, E) consisting of: Detection Module (D) for real-time OCEAN trait inference, Regulation Module (R) for Zurich Model-aligned behavior adaptation, and Evaluation Module (E) for quality assessment. The architecture extends the PROMISE framework [7] using Java components (version 8.0, available at: [GitHub repository - to be provided upon publication]) for trait detection.

**Modular Design Principles**: The system architecture follows three key design principles: (i) **Separation of Concerns**: Each module operates independently with well-defined interfaces; (ii) **Scalability**: New personality dimensions or regulation strategies can be added without modifying existing components; (iii) **Traceability**: All detection and regulation decisions are logged for analysis and debugging.

**Technical Implementation Details**:
- **Platform**: OpenAI GPT-4 API with custom system prompts for detection, regulation, and evaluation
- **Detection Method**: Prompt-based personality trait inference, where GPT-4 is guided by structured detection prompts to assign Big Five trait scores (–1, 0, +1) based on linguistic and semantic analysis of user utterances
- **Regulation Engine**: Dynamic prompt concatenation based on detected traits with conflict resolution
- **Evaluation System**: Custom Evaluator GPT with structured scoring matrix and bias prevention mechanisms

**Data Flow Architecture**: The system processes user messages through a sequential pipeline: (1) User input → (2) Personality detection → (3) Trait-to-regulation mapping → (4) Prompt assembly → (5) Response generation → (6) Evaluation and logging. Each step maintains state information and provides feedback for continuous improvement.

**Integration with Healthcare Systems**: The modular architecture enables seamless integration with existing healthcare information systems through standardized APIs. The system can be deployed as a standalone service or integrated into electronic health record (EHR) systems for comprehensive patient support.

## Personality Detection Module

### Theoretical Foundation

We employ the Five-Factor Model as personality representation P = (O, C, E, A, N) ∈ {−1, 0, +1}⁵, capturing Openness, Conscientiousness, Extraversion, Agreeableness, and Neuroticism [9]. This discrete encoding enables tractable real-time inference while preserving sufficient granularity for research applications.

**Psychological Validity**: The Big Five model represents the most widely accepted and empirically validated framework for personality assessment in psychological research [9]. The trinary encoding system (−1, 0, +1) provides sufficient granularity for conversational AI applications while maintaining computational efficiency and interpretability.

**Trait Independence Assumption**: Our implementation treats the five personality dimensions as independent and orthogonal, following the standard Big Five framework. While this assumption simplifies the detection and regulation processes, we acknowledge that real-world personality expressions may involve trait interactions that future research should explore.

### Detection System Design and Implementation

**LLM-Based Architecture**: The personality detection system employs a series of GPT-4 instances rather than traditional algorithmic approaches. Each detection instance receives carefully curated system prompts that encode linguistic patterns and behavioral indicators for personality trait identification.

**Prompt Engineering Approach**: Detection utilizes sophisticated prompt engineering rather than traditional rule-based pattern matching. Unlike conventional NLP systems that rely on hand-coded linguistic rules and pattern libraries, our approach leverages GPT-4's semantic understanding capabilities through carefully designed prompts. Each Big Five trait operates within a dedicated detection prompt that guides the LLM to analyze specific aspects of user communication:

- **Openness Detection Prompt**: Analyzes vocabulary complexity, abstract thinking, and novelty-seeking expressions
- **Conscientiousness Detection Prompt**: Evaluates planning language, organizational patterns, and goal-oriented communication
- **Extraversion Detection Prompt**: Assesses social engagement, energy level, and interactive communication style
- **Agreeableness Detection Prompt**: Examines cooperative language, empathy expressions, and conflict resolution patterns
- **Neuroticism Detection Prompt**: Analyzes emotional stability, anxiety indicators, and stress-related language

**Context Integration**: The detection system processes user messages with conversation history context, enabling cumulative personality assessment. Each detection prompt includes:
- Current user message
- Previous conversation turns
- Emerging personality patterns
- Confidence indicators for trait classification

**Detection Thresholds and Confidence**: Trait detectors employ conservative thresholds to prevent premature classification. A trait is only assigned a positive (+1) or negative (-1) value when sufficient linguistic evidence accumulates through multiple conversation turns.

**Structured Scoring Framework**: The "rule-like" aspect of our system refers to the structured evaluation criteria embedded within detection prompts (–1, 0, +1 scoring) rather than traditional NLP rule engines. This framework provides consistent, interpretable personality assessments while leveraging GPT-4's semantic analysis capabilities.

**Prompt Sensitivity and Optimization**: The system acknowledges the sensitivity of LLM-based detection to prompt formulation. Initial prompts were refined through iterative testing to achieve consistent detection accuracy across different conversation styles and personality expressions.

**Pipeline Architecture**: The detection workflow follows a sequential pipeline:
1. **Message Processing**: User input is prepared with conversation context
2. **Prompt Assembly**: Detection prompts are assembled with current context
3. **LLM Inference**: GPT-4 processes prompts to generate trait assessments
4. **Result Parsing**: OCEAN vector is extracted from LLM output
5. **Confidence Assessment**: Detection confidence is evaluated for each trait
6. **State Update**: Personality profile is updated based on new evidence

**Advantages of LLM-Based Detection**:
- **Contextual Understanding**: LLMs can interpret nuanced linguistic patterns
- **Adaptive Learning**: Prompts can be refined based on performance
- **Scalability**: Easy to extend to new personality dimensions
- **Interpretability**: Detection reasoning is transparent through prompt design
- **Flexibility**: Can handle diverse communication styles and cultural contexts
- **Semantic Sophistication**: Leverages advanced language understanding rather than rigid pattern matching

**Limitations and Mitigation Strategies**:
- **Prompt Sensitivity**: Addressed through iterative refinement and testing
- **Context Window Limits**: Mitigated through conversation history summarization
- **Cultural Bias**: Addressed through diverse prompt testing and validation
- **Consistency**: Maintained through standardized prompt templates and validation
- **Semantic Drift**: Unlike traditional rule-based systems, LLM responses may vary; addressed through prompt engineering and validation protocols

## Behavior Regulation Module

### Zurich Model Integration

Our regulation strategy maps OCEAN traits to Zurich Model motivational domains [10]: Security Domain (N → emotional stability/vulnerability responses), Arousal Domain ({O,E} → novelty/stimulation regulation), Affiliation Domain (A → social connection/cooperation strategies).

**Theoretical Foundation**: The Zurich Model of Social Motivation provides a comprehensive framework for understanding human behavior through three core motivational systems: security, arousal, and affiliation [10]. This model offers a theoretically-grounded approach to translating personality traits into actionable behavioral modifications for conversational AI systems.

**Motivational Domain Mapping**: The integration of Big Five traits with Zurich Model domains creates a psychologically coherent framework for behavior regulation:
- **Security Domain**: Addresses basic safety and emotional stability needs, primarily influenced by Neuroticism levels
- **Arousal Domain**: Manages stimulation and novelty preferences, influenced by Openness and Extraversion traits
- **Affiliation Domain**: Regulates social connection and cooperation strategies, primarily influenced by Agreeableness

Table 1. Trait-to-Regulation Mapping Based on Zurich Model

|Trait | High (+1) Regulation Prompt | Low (-1) Regulation Prompt | Motivational Domain |
|-------|----------------------------|----------------------------|-------------------|
|Openness | "Explore diverse approaches, introduce new concepts" | "Focus on familiar, established practices" | Arousal |
|Conscientiousness | "Provide structured, systematic guidance" | "Offer flexible, adaptable approaches" | Arousal |
|Extraversion | "Use encouraging, interactive communication" | "Adopt calm, reflective tone" | Arousal |
|Agreeableness | "Show warmth, collaborative planning" | "Use neutral, professional stance" | Affiliation |
|Neuroticism | "Reinforce stability, confidence" | "Provide extra support, acknowledge concerns" | Security |

**Regulation Prompt Assembly**: The regulation system dynamically assembles behavioral instructions based on detected traits. For each non-neutral trait, the system retrieves the corresponding regulation prompt and concatenates them into an integrated instruction set.

**Conflict Resolution**: When multiple traits suggest potentially conflicting behaviors, the system employs harmonization strategies to create coherent responses. For example, high Openness (+1) combined with low Extraversion (-1) might result in "explore new concepts in a calm, reflective manner."

**Healthcare-Specific Adaptations**: Regulation prompts are specifically designed for healthcare contexts, emphasizing therapeutic appropriateness, patient safety, and professional boundaries. This ensures that personality adaptations enhance rather than compromise the therapeutic relationship.

## Experimental Protocol

### Personality Profile Simulation

Two extreme personality profiles were implemented based on established Big Five research:
- **Type A (High-functioning)**: P_A = (+1,+1,+1,+1,+1) representing openness to treatment, conscientiousness, social engagement, cooperation, and emotional stability
- **Type B (Vulnerable)**: P_B = (−1,−1,−1,−1,−1) representing treatment resistance, disorganization, withdrawal, skepticism, and emotional sensitivity

Each profile was systematically encoded into specific conversational prompts maintaining consistency across dialogue turns, based on established personality psychology literature.

**Profile Encoding Methodology**: Personality profiles were encoded using carefully crafted conversational prompts that consistently exhibit the target trait levels across all dialogue turns. These prompts were developed through iterative refinement to ensure they accurately represent the intended personality characteristics while maintaining conversational naturalness.

**Type A Profile Characteristics**:
- **Openness**: "I'd love to explore different approaches and try new strategies"
- **Conscientiousness**: "Let me organize this systematically and set clear goals"
- **Extraversion**: "I'm excited to work together and share my experiences"
- **Agreeableness**: "I understand and appreciate your perspective, let's collaborate"
- **Neuroticism**: "I feel confident we can handle this together"

**Type B Profile Characteristics**:
- **Openness**: "I don't see the point in trying new things, let's stick to what works"
- **Conscientiousness**: "I'll figure it out when I feel like it, no need to rush"
- **Extraversion**: "I need to be alone right now, I'm not in the mood to socialize"
- **Agreeableness**: "Actually, I disagree with that approach, it won't work for me"
- **Neuroticism**: "I'm worried this will make things worse, I don't feel safe"

### Agent Configuration

For each personality type:
- **5 Regulated Agents**: Dynamic personality detection + trait-based regulation per turn
- **5 Baseline Agents**: Static supportive responses without personality adaptation
- **Total**: 10 agents per personality type, 20 agents overall

Each agent engaged in structured 6-turn dialogues, generating 120 total dialogue turns for analysis.

**Agent Implementation Details**: Each agent was implemented as a separate GPT-4 instance with customized system prompts. Regulated agents received dynamic prompts that updated based on detected personality traits, while baseline agents maintained static supportive prompts throughout all interactions.

**Dialogue Structure**: All conversations followed a standardized 6-turn structure designed to provide sufficient interaction depth for personality detection while maintaining manageable evaluation complexity. Each turn consisted of a user message followed by an assistant response.

**Randomization and Control**: Agent instances were randomly assigned to personality types to minimize potential bias. Baseline agents served as control conditions, ensuring that any performance differences could be attributed to the personality adaptation mechanisms rather than other factors.

### Evaluation Framework

**Assessment Criteria**:
- **Regulated Agents**: Detection Accuracy, Regulation Effectiveness, Emotional Tone Appropriateness, Relevance & Coherence, Personality Needs Addressed
- **Baseline Agents**: Emotional Tone Appropriateness, Relevance & Coherence, Personality Needs Addressed
- **Scoring**: Trinary scale {0,1,2} per criterion

**Evaluation Method**: Custom LLM-based Evaluator (GPT-4) with structured prompts designed for unbiased assessment. Each criterion evaluation considered complete interaction pairs for consistency.

**Scoring Protocol**: The evaluation system employed a trinary scoring scale where:
- **Yes (2 points)**: Strong alignment with evaluation criteria
- **Not Sure (1 point)**: Partial alignment or ambiguous cases
- **No (0 points)**: Clear misalignment with evaluation criteria

**Bias Prevention**: The Evaluator GPT was designed with specific mechanisms to prevent bias, including independent evaluation of each interaction pair and explicit instructions to ignore previous assessments.

## Data Availability

**Code and Data Repository**: Complete implementation code, detection prompts, regulation templates, and experimental data will be made available at: https://github.com/[username]/personality-ai-simulation [to be created upon publication].

**Supplementary Materials**: Available as separate files containing complete detection algorithms, regulation prompts, conversation transcripts, and evaluation metrics.

# Results

## Data Quality and Sample Distribution

The evaluation dataset comprised 59 regulated agent interactions and 58-60 baseline agent interactions (varying by metric) across two extreme personality profiles (Type A: all traits +1; Type B: all traits −1). Figure 1 presents the sample distribution across conditions and personality types.

**[Figure 1 near here]**

**Figure 1.** Sample distribution across experimental conditions. Left panel shows distribution of dialogue turns by personality type (Type A: high-functioning profile; Type B: vulnerable profile). Right panel shows distribution by condition (Regulated vs. Baseline agents). Total n=120 dialogue turns across 20 agent instances.

Data quality assessment revealed minimal missing data (<2%) across all evaluation metrics, with no systematic patterns of missingness by condition or personality type (Figure 2).

**[Figure 2 near here]**

**Figure 2.** Missing data heatmap across evaluation metrics and experimental conditions. White cells indicate complete data; gray cells indicate missing values. Overall missingness rate: 1.7%. No systematic bias detected by condition or personality type.

## Detection and Regulation Performance

Personality detection achieved 100% accuracy (58/58 correct assessments) across extreme personality profiles, with perfect regulation effectiveness (59/59, 100%). Table 1 summarizes the core technical performance metrics.

**Table 1.** Detection and Regulation Performance Summary

| Metric | Success Rate | 95% CI | Performance Level |
|--------|-------------|---------|-------------------|
| Overall Detection Accuracy | 58/58 (100%) | [93.8, 100] | Perfect |
| Regulation Effectiveness | 59/59 (100%) | [93.9, 100] | Perfect |
| Combined Technical Performance | 117/117 (100%) | [96.9, 100] | Perfect |

*Note: Confidence intervals calculated using Clopper-Pearson method for binomial proportions. Perfect scores reflect simulation with extreme personality profiles (+1 or -1 for all traits) and automated GPT-4 evaluation.*

**Detection Performance Analysis**: The personality detection system demonstrated perfect accuracy for extreme personality profiles, validating the technical feasibility of prompt-based personality trait inference in highly controlled simulation conditions. The 100% success rate indicates that the LLM-based detection approach successfully identifies clear, consistent personality signals when traits are expressed at polar extremes.

**Critical Interpretation Context**: Perfect scores must be interpreted within the limitations of the controlled experimental design:
- **Extreme profiles only**: Detection tested exclusively on all-positive (+1,+1,+1,+1,+1) or all-negative (-1,-1,-1,-1,-1) trait combinations, representing the easiest possible detection scenario
- **Simulation environment**: All "user" messages were pre-scripted to consistently exhibit target personality traits across all dialogue turns
- **GPT-4 evaluation**: Automated assessment by the same model family used for detection may introduce systematic bias favoring AI-generated responses
- **Limited generalizability**: Performance with moderate trait values, mixed profiles, or inconsistent personality expressions remains completely untested and likely to be substantially lower

## Personality Vector Analysis

Analysis of detected personality vectors revealed consistent trait patterns across dialogue turns. Figure 3 visualizes the distribution of OCEAN trait values for regulated interactions.

**[Figure 3 near here]**

**Figure 3.** Distribution of detected Big Five (OCEAN) personality trait values. Each panel shows the frequency distribution of trait scores (−1, 0, +1) across all dialogue turns. Type A profiles (blue) cluster at +1; Type B profiles (orange) cluster at −1, confirming successful implementation of extreme personality profiles in simulation.

Figure 4 presents a heatmap visualization of personality patterns across individual agent instances, demonstrating the consistency of personality expression within profiles and clear differentiation between Type A and Type B profiles.

**[Figure 4 near here]**

**Figure 4.** Personality trait heatmap across agent instances and dialogue turns. Rows represent individual agents (A1-A10, B1-B10); columns represent Big Five traits (O, C, E, A, N). Color intensity indicates trait level: red (+1 = high), white (0 = neutral), blue (−1 = low). Clear clustering by personality type validates extreme profile implementation.

## Conversational Quality Assessment

The evaluation revealed a striking selective enhancement pattern: while both regulated and baseline agents performed equivalently on fundamental conversational quality metrics, personality adaptation dramatically improved the system's ability to address personality-specific user needs. Figure 5 presents the overall performance comparison.

**[Figure 5 near here]**

**Figure 5.** Performance comparison across evaluation metrics (Regulated vs. Baseline). Bar heights represent mean success rates; error bars show 95% confidence intervals. Asterisks indicate statistical significance: **p < 0.001; ns = not significant (p > 0.05). Regulated agents show dramatic advantage specifically in Personality Needs Addressed (***) while maintaining equivalent performance on basic quality metrics (Emotional Tone, Relevance & Coherence).

Table 2 provides detailed statistical analysis of performance differences across all evaluation criteria.

**Table 2.** Comprehensive Performance Comparison: Regulated vs. Baseline

| Evaluation Criterion | Regulated (n=59) | Baseline (n=58-60) | Mean Difference | Cohen's d | p-value | Effect Interpretation |
|---------------------|------------------|-------------------|----------------|-----------|---------|----------------------|
| **Detection Accuracy** | 100% (58/58) | N/A | N/A | N/A | N/A | Regulated-only metric |
| **Regulation Effectiveness** | 100% (59/59) | N/A | N/A | N/A | N/A | Regulated-only metric |
| **Emotional Tone Appropriateness** | 100% (59/59) | 100% (60/60) | 0.0% | 0.00 | 1.000 | No difference |
| **Relevance & Coherence** | 100% (59/59) | 98.33% (59/60) | +1.67% | 0.18 | 0.323 | Negligible difference |
| **Personality Needs Addressed** | 100% (59/59) | 8.62% (5/58) | **+91.38%** | **4.58** | **<0.001*** | Very large effect |

*Note: Cohen's d interpretation: 0.2 = small, 0.5 = medium, 0.8 = large, >2.0 = very large. *** indicates p<0.001 (highly significant). N/A = Not Applicable (baseline agents lack detection/regulation capabilities).*

**Key Performance Findings**:

1. **Perfect Technical Implementation**: Both detection (100%, 58/58) and regulation (100%, 59/59) achieved perfect accuracy in the controlled simulation environment, demonstrating technical feasibility of the approach.

2. **Equivalent Basic Quality**: Both conditions performed equivalently on fundamental conversational quality:
   - **Emotional Tone**: Both 100% appropriate (no significant difference, Cohen's d = 0.00, p = 1.000)
   - **Relevance & Coherence**: Minimal difference (Regulated 100% vs Baseline 98.33%; difference = 1.67%, Cohen's d = 0.18, p = 0.323)

3. **Dramatic Personalization Advantage**: The largest and most significant difference emerged in personality-specific adaptation:
   - **Personality Needs Addressed**: Regulated 100% vs Baseline 8.62%
   - **Effect Size**: Cohen's d = 4.58 (very large effect)
   - **Statistical Significance**: p < 0.001 (highly significant)
   - **Practical Impact**: 91.38 percentage point improvement

## Effect Size Analysis

Figure 6 visualizes the effect sizes (Cohen's d) for each evaluation metric, highlighting the magnitude of performance differences.

**[Figure 6 near here]**

**Figure 6.** Effect sizes (Cohen's d) for performance differences between regulated and baseline agents. Horizontal dashed lines indicate conventional effect size thresholds: small (d = 0.2), medium (d = 0.5), large (d = 0.8). The dramatic effect for Personality Needs Addressed (d = 4.58) far exceeds conventional thresholds, while Emotional Tone and Relevance show negligible effects (d < 0.2), confirming selective enhancement pattern.

Figure 7 presents the percentage improvement across metrics, providing an alternative visualization of the selective enhancement pattern.

**[Figure 7 near here]**

**Figure 7.** Percentage improvement from baseline to regulated conditions across evaluation metrics. Personality Needs Addressed shows 91.38 percentage point improvement (1059% relative improvement from 8.62% baseline), while other metrics show minimal or no improvement, demonstrating that personality adaptation specifically targets personalization without affecting basic quality standards.

## Weighted Scoring Analysis

To provide additional quantitative perspective, we analyzed performance using a weighted scoring system where evaluations were scored as YES=2 points, NOT SURE=1 point, NO=0 points (Table 3).

**Table 3.** Weighted Score Performance Comparison (0-2 Scale)

| Metric | Regulated Mean (SD) | Baseline Mean (SD) | Mean Difference | Cohen's d | Improvement % |
|--------|---------------------|-------------------|-----------------|-----------|---------------|
| Emotional Tone | 2.00 (0.00) | 2.00 (0.00) | 0.00 | 0.00 | 0.0% |
| Relevance & Coherence | 2.00 (0.00) | 1.97 (0.26) | +0.03 | 0.18 | 1.7% |
| Personality Needs | 2.00 (0.00) | 0.20 (0.58) | **+1.80** | **4.42** | **90.0%** |

Figure 8 visualizes the weighted score distributions for each metric.

**[Figure 8 near here]**

**Figure 8.** Distribution of weighted scores (0-2 scale) across evaluation metrics by condition. Box plots show median (center line), interquartile range (box), and full range (whiskers). Regulated agents (blue) achieve consistently maximal scores (median = 2.0) across all metrics. Baseline agents (orange) show equivalent performance for Emotional Tone and Relevance but dramatically lower scores for Personality Needs (median = 0.0).

Figure 9 provides a complementary visualization focusing on the total quality scores.

**[Figure 9 near here]**

**Figure 9.** Box plot comparison of total quality scores (summed across Emotional Tone, Relevance & Coherence, and Personality Needs metrics). Regulated agents show consistently high total scores (median = 6.0, perfect performance), while baseline agents show substantially lower total scores due to failure in addressing personality needs. The lack of overlap between distributions confirms the robustness of the selective enhancement effect.

## Statistical Robustness Analysis

To ensure the robustness of our findings, we conducted both parametric (independent t-tests) and non-parametric (Mann-Whitney U) statistical tests. Table 4 summarizes the results of advanced statistical testing.

**Table 4.** Advanced Statistical Testing Results

| Metric | Independent t-test | Mann-Whitney U | Levene's Test | Normality (Shapiro-Wilk) |
|--------|-------------------|----------------|---------------|-------------------------|
| Emotional Tone | t=0, p=1.000 | U=1770, p=1.000 | p>0.05 (equal var.) | Reg: p=1.000, Base: p=1.000 |
| Relevance & Coherence | t=0.99, p=0.323 | U=1799.5, p=0.330 | p=0.323 (equal var.) | Reg: p=1.000, Base: p<0.001 |
| Personality Needs | t=23.99, p<0.001 | U=3392.5, p<0.001 | p=0.009 (unequal var.) | Reg: p=1.000, Base: p<0.001 |

*Note: Both parametric and non-parametric tests converge on identical conclusions, strengthening confidence in findings despite normality violations for baseline scores.*

**Interpretation**: Both parametric (t-test) and non-parametric (Mann-Whitney U) tests converge on identical conclusions:
- No significant difference in emotional tone (p=1.000)
- No significant difference in relevance & coherence (p=0.323-0.330)
- Highly significant difference in personality needs addressed (p<0.001 for both tests)

The violation of normality assumptions for baseline scores (particularly for Personality Needs) justifies the inclusion of non-parametric tests. Crucially, both test families yield consistent results, strengthening confidence in the findings despite the simulation-based design.

**Important Caveat**: These inferential statistics are included for methodological completeness and to facilitate comparison with related empirical studies. However, given the deterministic simulation design (predefined personality profiles, pre-scripted responses), these p-values should NOT be interpreted as evidence of generalizable population effects. The effect sizes (Cohen's d) provide more appropriate interpretation for this proof-of-concept study.

## Criterion-Specific Analysis

**Regulated Agent Performance Across All Metrics**:
- Detection Accuracy: 58/58 (100%) - All personality trait inferences correct
- Regulation Effectiveness: 59/59 (100%) - All behavioral adaptations appropriate
- Emotional Tone: 59/59 (100%) - All responses emotionally appropriate
- Relevance & Coherence: 59/59 (100%) - All responses relevant and coherent
- Personality Needs: 59/59 (100%) - All personality-specific needs addressed

**Baseline Agent Performance**:
- Emotional Tone: 60/60 (100%) - Equivalent to regulated
- Relevance & Coherence: 59/60 (98.33%) - Nearly equivalent to regulated
- Personality Needs: 5/58 (8.62%) - **Critical failure in personalization**

**Performance Gap Analysis**: The baseline agents demonstrated competent performance on fundamental conversational quality dimensions (emotional appropriateness and logical coherence) but exhibited near-complete failure in addressing personality-specific user needs. This pattern highlights the critical limitation of non-adaptive systems: they can maintain basic interaction quality but cannot provide the personalization essential for optimizing therapeutic effectiveness in healthcare contexts where individual differences significantly influence treatment outcomes.

## Qualitative Examples Demonstrating Personality Adaptation

**Example 1: Vulnerable Population Interaction**

*Detected Profile*: P̂ = (−1, 0, −1, −1, −1) [Low Openness, Neutral Conscientiousness, Low Extraversion, Low Agreeableness, High Neuroticism]

*User Message*: "I'm feeling really overwhelmed and anxious. I don't think talking helps."

*Regulated Response* (Zurich Model-Aligned):
> "I understand you're going through a difficult time, and feeling exhausted is completely natural. This is a safe space where we can focus on small, familiar steps that feel manageable for you right now. We don't have to rush into anything—let's just take it one moment at a time."

*Baseline Response* (Non-Adaptive):
> "It's understandable to feel overwhelmed. Talking about your concerns can help organize your thoughts and develop coping strategies."

**Analysis**: The regulated response demonstrates therapeutic attunement through:
- **Security Domain Activation** (High Neuroticism): Explicit validation, safety reassurance ("This is a safe space")
- **Reduced Arousal** (Low Openness/Extraversion): Emphasis on "familiar steps," calm pacing ("one moment at a time")
- **Respectful Distance** (Low Agreeableness): Non-pressuring approach ("We don't have to rush")

In contrast, the baseline response provides generic support without addressing the user's specific personality-driven needs for emotional security, reduced stimulation, and autonomous pacing.

**Example 2: High-Functioning Population Interaction**

*Detected Profile*: P̂ = (+1, +1, +1, +1, +1) [All traits high]

*User Message*: "I'm ready to make some changes. What should I try first?"

*Regulated Response* (Zurich Model-Aligned):
> "Excellent! Your enthusiasm for exploring new approaches is wonderful. Let's create a structured plan together that builds on your natural strengths. What specific goals would you like to focus on first? We can brainstorm multiple options and organize them systematically."

*Baseline Response* (Non-Adaptive):
> "That's great to hear. Setting goals can be very helpful. What would you like to work on?"

**Analysis**: The regulated response actively engages the user's personality strengths:
- **Arousal Domain** (High Openness/Extraversion): Encourages exploration, multiple options, collaborative energy
- **Affiliation Domain** (High Agreeableness): Warm, collaborative framing ("together")
- **Conscientiousness Engagement**: Structured planning, systematic organization

The baseline response provides generic encouragement without leveraging the user's personality-specific strengths for goal-setting and treatment engagement.

## Summary of Key Findings

1. **Technical Feasibility Demonstrated**: Perfect detection (100%, 58/58) and regulation effectiveness (100%, 59/59) establish proof-of-concept for prompt-based personality-adaptive conversational systems in controlled conditions.

2. **Selective Performance Enhancement**: Personality adaptation specifically enhanced personalization (91.38% improvement, Cohen's d = 4.58, p<0.001) without compromising fundamental conversational quality (emotional tone and relevance maintained at ≥98% for both conditions).

3. **Very Large Effect Size**: The Cohen's d = 4.58 effect for personality needs addressed represents an exceptionally large effect, suggesting substantial practical significance if even partially maintained in real-world validation.

4. **Baseline Limitation Identified**: Non-adaptive baseline agents exhibited critical failure (8.62% success) in addressing personality-specific needs despite adequate performance on generic quality metrics, highlighting the necessity of personalization for therapeutic applications.

5. **Simulation-Specific Context**: All findings derive from controlled simulation with extreme personality profiles and automated evaluation, requiring extensive human subject validation before any claims about real-world effectiveness can be made.

---

## Figure File References for Manuscript Preparation

When preparing the final manuscript, insert the following figure files from the `statistical analyis/figures/` directory:


# Discussion

## Principal Findings

This simulation study demonstrates the technical feasibility of personality-adaptive conversational AI using real-time OCEAN detection and Zurich Model-aligned regulation. Regulated agents achieved 34% improvement over baseline conditions in controlled simulation scenarios.

**Key Technical Achievements**:
1. **Successful implementation of real-time personality detection** (98.33% accuracy for extreme profiles)
2. **Effective translation of personality traits into behavioral modifications** through Zurich Model integration
3. **Consistent performance across diverse personality configurations** with large effect sizes
4. **Modular architecture enabling systematic testing and refinement** for healthcare applications

**Potential Relevance**: The substantial performance improvements demonstrated in simulation suggest significant potential for enhancing patient communication, adherence, and therapeutic outcomes in healthcare settings. The personality-aware approach addresses a critical gap in current conversational AI systems by providing truly personalized interactions.

## Comparison with Existing Literature

Our approach extends the PROMISE framework [7] by integrating motivational psychology theory and healthcare-specific considerations. Unlike previous systems focusing on trait generation, our framework adapts to detected user personalities through theoretically-grounded regulation strategies.

**Theoretical Advancement**: The integration of the Zurich Model of Social Motivation with Big Five personality detection represents a novel theoretical contribution to the field of conversational AI. This integration provides a psychologically coherent framework for translating personality traits into actionable behavioral modifications.

**Performance Comparison**: The 34% improvement exceeds typical gains reported in conversational AI literature, though these results are limited to simulation conditions with extreme personality profiles. This substantial improvement demonstrates the potential value of personality-aware adaptation in healthcare contexts.

## Real-World Translation Pathway

**Immediate Requirements for Human Subject Validation**:
1. **Human Subject Studies**: Minimum n=50 elderly participants with validated personality assessments (NEO-PI-R, BFI-2)
2. **Domain Expert Evaluation**: Licensed psychologists assessing personality detection accuracy and therapeutic appropriateness
3. **Safety Validation**: Comprehensive risk assessment for potential psychological harms and therapeutic misalignment
4. **Cultural Validation**: Testing across diverse ethnic, linguistic, and cultural groups to ensure generalizability
5. **Longitudinal Assessment**: Extended interaction studies (minimum 30 days) to assess sustained effectiveness and engagement

**Regulatory Pathway**:
- **IRB Approval**: Full institutional review board approval for human subjects research
- **Data Protection**: HIPAA/GDPR compliance for healthcare data handling and privacy protection
- **FDA Guidance**: Alignment with emerging FDA guidance for healthcare AI systems and healthcare decision support
- **Research Trial Registration**: Registration for therapeutic efficacy claims and research outcome assessment

**Timeline Estimate**: 2-3 years for comprehensive human subject validation, regulatory approval, and initial healthcare deployment

## Limitations

**Critical Study Limitations**:

1. **Simulation-Only Design**: No real user validation; findings may not generalize to authentic interactions. All user inputs were pre-scripted simulated profiles rather than spontaneous human responses, which likely inflates performance metrics.
2. **AI-Based Evaluation Bias**: Assessment by GPT-4 rather than human experts; systematic bias likely favors AI-generated responses. The evaluator may preferentially rate similar AI model outputs, overestimating quality. Human expert evaluation would likely reveal more nuanced performance.
3. **Extreme Personality Profiles Only**: Limited to polar trait expressions (all +1 or all -1); moderate or mixed personality profiles completely untested. Real users exhibit continuous trait distributions that may respond less predictably.
4. **Short Interaction Duration**: 6-turn dialogues insufficient for assessing sustained relationships, rapport development, or long-term engagement essential for healthcare applications.
5. **Cultural and Linguistic Homogeneity**: Patterns calibrated exclusively for English; cross-cultural validity unknown. Personality expression varies significantly across cultures.
6. **No Healthcare Outcomes**: No measurement of actual health outcomes, therapeutic efficacy, user satisfaction, or behavioral changes. Performance limited to automated conversational quality metrics.

**Technical Limitations**:
- Single-modality detection (text-only, excluding paralinguistic cues)
- Prompt engineering sensitivity requiring careful calibration
- Potential brittleness with communication patterns outside training scope
- Limited generalization to moderate personality expressions
- Semantic variability in LLM responses (unlike deterministic rule-based systems)

**Potential Harms**: Personality profiling in healthcare raises concerns about psychological manipulation, stereotype reinforcement, and decisional autonomy. Misclassification could lead to inappropriate therapeutic approaches. These risks require careful consideration in real-world translation.

## Risk Assessment

Table 5. Potential Risks and Mitigation Strategies for Healthcare Deployment

|Risk Category | Risk Description | Likelihood | Impact | Mitigation Strategy |
|---------------|------------------|------------|--------|-------------------|
|Misclassification | Incorrect personality assessment | Medium | High | Conservative thresholds, provider oversight, fallback protocols |
|Cultural Bias | Reduced accuracy across cultures | High | High | Diverse validation cohorts, cultural adaptation algorithms, bias detection systems |
|Over-reliance | Excessive dependence on AI | Medium | Medium | Provider training, clear limitations communication, human oversight requirements |
|Privacy Breach | Unauthorized personality data access | Low | High | End-to-end encryption, access controls, audit logging, HIPAA compliance |
|Therapeutic Harm | Inappropriate psychological intervention | Medium | High | Professional supervision, safety protocols, emergency escalation procedures |

**Risk Mitigation Framework**: The identified risks require a comprehensive mitigation strategy involving technical safeguards, professional oversight, and regulatory compliance. The conservative approach to personality detection and the emphasis on healthcare-specific regulation design help minimize many of these risks.

## Future Research Priorities

**Technical Development**:
1. **Multimodal personality detection** (voice, facial expressions, physiological signals)
2. **Continuous learning and adaptation mechanisms** for improved accuracy over time
3. **Cultural bias detection and mitigation algorithms** for global healthcare applications
4. **Integration with validated psychological assessment tools** for human subject validation
5. **Advanced prompt engineering techniques** to reduce semantic variability and improve consistency

**Human Subject Validation Studies**:
1. **Randomized controlled trials** with research endpoints and therapeutic outcomes
2. **Comparative effectiveness research** against standard care and existing interventions
3. **Long-term safety and efficacy monitoring** for sustained therapeutic benefits
4. **Health economic evaluation** for healthcare system adoption and cost-effectiveness

**Regulatory and Ethical Framework**:
1. **Guidelines for personality-aware healthcare AI** development and deployment
2. **Informed consent frameworks** for psychological profiling and AI interaction
3. **Professional liability and malpractice considerations** for healthcare providers
4. **International regulatory harmonization** for global healthcare AI deployment

**Healthcare Integration**:
1. **Electronic Health Record (EHR) integration** for seamless healthcare workflow
2. **Provider training and education** on personality-aware AI systems
3. **Patient education and engagement** strategies for AI-assisted care
4. **Quality assurance and monitoring** systems for ongoing safety assessment

## Conclusions

This simulation study demonstrates the technical feasibility of personality-adaptive conversational AI for healthcare applications. The framework successfully integrates real-time Big Five trait detection with Zurich Model-aligned behavior regulation, achieving substantial performance improvements in controlled conditions.

**Study Contributions**: This work makes three key contributions to the field of healthcare conversational AI:

1. **Technical Innovation**: First implementation of real-time personality detection with Zurich Model-aligned behavior regulation for healthcare contexts
2. **Evaluation Framework**: Comprehensive assessment methodology for personality-adaptive systems with structured scoring criteria
3. **Research Pathway**: Clear roadmap for human subject validation and healthcare deployment with specific regulatory requirements

**Potential Implications**: While simulation results are promising, extensive human subject validation is required before healthcare deployment. The 34% improvement in conversational quality represents significant potential for enhanced patient communication, adherence, and therapeutic outcomes in mental health, elder care, and chronic disease management contexts.

**Research Implications**: The work provides a foundation for personality-aware healthcare AI development while highlighting critical validation requirements. The modular architecture enables systematic testing and refinement through controlled studies, establishing a framework for future research in adaptive conversational systems.

**Regulatory and Ethical Implications**: The framework requires comprehensive safety evaluation, cultural bias assessment, and regulatory approval pathways before healthcare implementation. Clear guidelines for personality-aware medical AI are needed to ensure patient safety and therapeutic effectiveness.

**Final Assessment and Next Steps**: This proof-of-concept establishes technical feasibility while acknowledging significant real-world translation challenges. Success depends on rigorous human subject validation, regulatory compliance, and ethical framework development. The next phase should focus on human subject validation studies with real patients and healthcare providers to assess therapeutic efficacy and safety in authentic healthcare settings.

**Immediate Next Steps**:
1. **Human Subject Protocol Development**: Design and submit IRB-approved human subject validation studies with elderly populations
2. **Clinical Partnership Development**: Establish collaborations with healthcare institutions for pilot studies
3. **Regulatory Engagement**: Begin discussions with regulatory bodies about approval pathways for healthcare AI
4. **Ethical Framework Development**: Collaborate with ethicists and patient advocates on responsible deployment guidelines

**Long-term Vision**: If validated with real users and healthcare professionals, this framework may contribute to improved healthcare delivery by providing scalable, personalized support that adapts to individual psychological needs. Following successful human trials and regulatory approval, the technology could potentially support mental health care, elder companionship, and chronic disease management applications while maintaining appropriate human oversight and professional supervision essential for therapeutic contexts.

# Data Availability Statement

Research data, complete implementation code, detection prompts, regulation templates, and simulation transcripts are available in a public repository at: https://github.com/[username]/personality-ai-simulation [to be made public upon publication]. Raw simulation logs and evaluation matrices can be requested from the corresponding author.

# Author Contributions

Conceptualization, S.D. and [co-authors if any]; methodology, S.D.; software, S.D.; validation, S.D.; formal analysis, S.D.; investigation, S.D.; resources, S.D.; data curation, S.D.; writing—original draft preparation, S.D.; writing—review and editing, S.D. and [supervisors]; visualization, S.D.; supervision, [G.L. and A.D.]; project administration, S.D. All authors have read and agreed to the published version of the manuscript.

# Funding

This research received no external funding.

# Institutional Review Board Statement

Not applicable. This study involved no human or animal subjects. All experiments were conducted using simulated personality profiles and automated evaluation systems. No institutional review board approval was required or sought.

# Informed Consent Statement

Not applicable. No human participants were involved in this simulation-based study.

# Acknowledgments

The authors would like to thank Dr. Guang Lu (Lucerne University of Applied Sciences and Arts) and Prof. Dr. Alexandre de Spindler (ZHAW) for their supervision and guidance throughout this research. We also acknowledge the PROMISE framework developers (Wu et al., 2023) whose work informed our system architecture.

# Conflicts of Interest

The authors declare no conflicts of interest.

# References

1. Luo, Y.; Hawkley, L.C.; Waite, L.J.; Cacioppo, J.T. Loneliness, health, and mortality in old age: A national longitudinal study. *Soc. Sci. Med.* **2012**, *74*, 907-914.

2. Hämmig, O. Health risks associated with social isolation in general and in young, middle and old age. *PLoS ONE* **2019**, *14*, e0219663.

3. Fitzpatrick, K.K.; Darcy, A.; Vierhile, M. Delivering cognitive behavior therapy to young adults with symptoms of depression and anxiety using a fully automated conversational agent (Woebot): A randomized controlled trial. *JMIR mHealth uHealth* **2017**, *5*, e7785.

4. Broadbent, E.; Loveys, K.; Ilan, G.; Chen, G.; Chilukuri, M.; Boardman, S.G.; Doraiswamy, P.; Skuler, D. ElliQ, an AI-driven social robot to alleviate loneliness: Progress and lessons learned. *JAR Life* **2024**, *13*, 22-28.

5. United Nations Department of Economic and Social Affairs. World Population Ageing 2019: Highlights. *United Nations* **2019**, ST/ESA/SER.A/430.

6. Li, J.; Galley, M.; Brockett, C.; Spithourakis, G.; Gao, J.; Dolan, B. A persona-based neural conversation model. In *Proceedings of ACL*; Association for Computational Linguistics: Stroudsburg, PA, USA, 2016; pp. 994-1003.

7. Wu, W.; Heierli, J.; Meisterhans, M.; Moser, A.; Farber, A.; Dolata, M.; Gavagnin, E.; Spindler, A.D.; Schwabe, G. PROMISE: A Framework for Developing Complex Conversational Interactions (Technical Report); University of Zurich: Zurich, Switzerland, 2023.

8. Calvo, R.A.; D'Mello, S. Affect detection: An interdisciplinary review of models, methods, and their applications. *IEEE Trans. Affect. Comput.* **2010**, *1*, 18-37.

9. Zheng, Z.; Liao, L.; Deng, Y.; Nie, L. Building emotional support chatbots in the era of LLMs. *arXiv* **2023**, arXiv:2308.11584.

10. McCrae, R.R.; John, O.P. An introduction to the five-factor model and its applications. *J. Pers.* **1992**, *60*, 175-215.

11. Quirin, M.; Malekzad, F.; Paudel, D.; Knoll, A.C.; Mirolli, M. Dynamics of personality: The Zurich model of motivation revived, extended, and applied to personality. *J. Pers.* **2023**, *91*, 928-946. https://doi.org/10.1111/jopy.12805

# Supplementary Materials

The following supporting information can be downloaded at: [Link to supplementary materials]

**Supplement S1**: Complete Detection System Design and Implementation Specifications  
**Supplement S2**: Full Regulation Prompt Templates  
**Supplement S3**: Conversation Transcripts and Evaluation Data  
**Supplement S4**: Statistical Analysis Details