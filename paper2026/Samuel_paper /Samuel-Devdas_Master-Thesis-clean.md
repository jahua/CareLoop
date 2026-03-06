---
title: "Samuel Devdas Master Thesis"
converted_from: PDF
conversion_date: 1753890306.7926319
---

<!-- Page 1 -->

Enhancing Emotional Support through Conversational AI via Big Five Personality Detection and Behavior Regulation Based on the Zurich Model Masters Thesis Author : Samuel Devdas, samuel.devdas@stud.hslu.ch Säntisstrasse 7A, 8580 Amriswil Supervisor : Dr. Guang Lu, guang.lu@hslu.ch Hochschule Luzern - Wirtschaft Zentralstrasse 9, 6002 Luzern Co-Supervisor : Prof

Dr. Alexandre de Spindler, alexandre.despindler@zhaw.ch Theaterstrasse 17, 8400 Winterthur Luzern, 16 May 2025 Master of Science in Applied Information and Data Science Lucerne University of Applied Sciences and Arts

<!-- Page 2 -->

## Abstract Objective. This thesis investigates whether dynamically regulating chatbot behavior based on user personality traits improves the eﬀectiveness of emotional support interactions. Grounded in the Big Five (OCEAN) personality framework and the Zurich Model of Social Motivation, the study implements a personality-adaptive chatbot system that detects user traits in real time and adjusts its conversational tone, structure, and engagement strategy accordingly

Experimental Design. Two extreme personality proﬁles—high OCEAN (Type A) and low OCEAN (Type B)—were simulated to evaluate system performance under contrasting psychological conditions. A controlled experiment compared personality-adaptive chatbots (regulated) with non-adaptive chatbots (baseline) across 10 simulated conversations

Regulated chatbots continuously updated their personality detection after each user message and dynamically applied behavior prompts aligned with detected traits. Evaluation Method. Conversation quality was assessed using a structured Evaluation Matrix scored by a custom Evaluator GPT system. Each assistant’s response was rated on detection accuracy, regulation eﬀectiveness, emotional tone, relevance, and satisfaction of personality-speciﬁc emotional needs

Results. Regulated assistants consistently outperformed baseline counterparts across all criteria and both personality types, achieving a 34.44% average performance improvement. Qualitative analysis conﬁrmed that regulated assistants generated more empathetic and contextually aligned responses. 1

<!-- Page 3 -->

## Conclusion. The ﬁndings support the hypothesis that real-time personality-aware regulation signiﬁcantly enhances chatbot interaction quality, particularly in emotionally supportive contexts. This work demonstrates the feasibility and value of integrating personality detection with adaptive behavioral modulation in conversational AI and oﬀers a scalable framework for developing emotionally intelligent systems for elder care, mental health, and digital companionship

2

<!-- Page 4 -->

Table of Contents Abstract............................................................................................................................................1 Table of Contents.............................................................................................................................3 List of Figures..................................................................................................................................6 List of Tables....................................................................................................................................6 1

## Introduction..................................................................................................................................8 1.1 Problem Context..................................................................................................................8 1.2 Theoretical Framework and Technological Foundations.....................................................9 1.3 Practical Signiﬁcance.........................................................................................................10 2

Background and Literature Review...........................................................................................11 2.1 Project Scope.....................................................................................................................11 2.2 Research Objectives...........................................................................................................11 2.3 Key Concepts and Deﬁnitions............................................................................................12 2.4 Research Scope and Delimitations.....................................................................................13 2.5 Literature Review and Current State of Research..............................................................14 3

Research Questions............................................................................................. .......................16 3.1 Primary Research Question................................................................................................16 3.2 Sub-Questions....................................................................................................................16 4

Methodology..............................................................................................................................17 4.1 Overview............................................................................................................................17 4.2 Experimental Setup............................................................................................................18 4.2.1 Personality Simulation Design..................................................................................18 4.2.2 Bot Variants...............................................................................................................18 4.3 Personality Detection Module............................................................................................19 4.3.1 Purpose......................................................................................................................19 4.3.2 Detection Logic and Trait Representation................................................................19 4.3.3 Trait Deﬁnitions

...........20 Table 1. Description of the Big Five Personality Traits with High (+1) and Low (–1) Score Characteristics......................................................................................21 4.3.4 Cumulative and Dynamic Updating..........................................................................21 4.3.5 Integration with Behavior Regulation.......................................................................21 4.3.6 Detection Architecture Implementation....................................................................21 4.3.7 Rationale for Dynamic Detection.............................................................................22 Table 2

Features and Beneﬁts of Using Extended Dialogue for Personality Trait Detection in Chatbots.............................................................................................23 3

<!-- Page 5 -->

4.4 Behavior Regulation Module.............................................................................................23 4.4.1 Purpose......................................................................................................................23 4.4.2 Design Principles......................................................................................................24 Table 3

Principles Guiding Personality-Based Behavioral Regulation in Conversational Agents...........................................................................................24 4.4.3 Trait-to-Prompt Mapping..........................................................................................24 Table 4

Behavioral Adjustment Strategies Based on High and Low Levels of the Big Five Personality Traits.....................................................................................25 4.4.4 Dynamic Prompt Construction.................................................................................25 4.4.5 Zurich Model Alignment..........................................................................................26 Table 5

Mapping Zurich Model Domains to Big Five Traits and Corresponding Prompt Eﬀects in Chatbot Interaction....................................................................27 4.4.6 Advantages of This Regulation Architecture............................................................27 Table 6. Features and Beneﬁts of Trait-Based Prompt Design in Conversational Agents....................................................................................................................28 4.5 Dialogue Simulation Protocol............................................................................................28 4.6 Evaluation Tooling

.................29 4.7 Evaluation Methodology....................................................................................................29 4.7.1 Evaluation Framework Details..................................................................................29 4.7.2 Scoring Protocol............................................................................................ ...........30 4.7.3 Evaluator GPT Design..............................................................................................30 4.7.4 Prevention of Bias and Drift.....................................................................................31 4.7.5 Scoring Methodology and Formulas.........................................................................31 4.7.5.1 Scoring Criteria......................................................................................................31 4.7.5.2 Criterion Deﬁnitions..............................................................................................31 4.7.5.3 Total Score Formulas.............................................................................................32 4.7.5.4 Grand Total Aggregation.......................................................................................33 4.7.5.5 Visualization and Interpretation.............................................................................33 5

Results........................................................................................................................................34 5.1 Overall Performance Scores............................................................................. .................34 Table 7. Total evaluation scores: Regulated vs

Baseline assistants by personality type.........................................................................................................................35 5.2 Criterion-Wise Comparison...............................................................................................35 Regulated Assistants (Max per criterion: 12)..............................................................35 Table 8

Criterion-wise scores for regulated assistants across Personality Types A and B......................................................................................................................35 Baseline Assistants (Max per criterion: 12).................................................................36 4

<!-- Page 6 -->

Table 9. Criterion-wise scores for baseline assistants across Personality Types A and B......................................................................................................................36 5.3 Visualization of Results.................................................................................... .................36 Figure 1

Total evaluation scores for regulated and baseline assistants across both personality types....................................................................................................37 5.4 Summary of Findings.........................................................................................................37 6

Discussion..................................................................................................................................38 6.1 Qualitative Comparison of Regulated vs. Baseline Dialogues...........................................38 Table 10. Comparison of Regulated and Baseline Assistant Responses Based on Detected Low-Trait Personality Proﬁle.................................................................39 Table 11

Example of Regulated Assistant Response Tailored to a High-Trait Personality Proﬁle Across All Big Five Dimensions.............................................40 Table 12. Baseline Assistant Interaction Example Addressing Goal-Setting and Energy Management Without Personality-Based Regulation................................40 6.2 Summary of Key Findings.................................................................................................40 6.3 Interpretation

.................41 6.4 Impact of Personality Detection and Regulation...............................................................41 6.5 Limitations and Challenges...............................................................................................42 6.5.1 Methodological Limitations........................................................................... ...........42 6.5.2 Implementation and Design Challenges...................................................................44 6.5.3 Manual Execution Overhead

...........45 6.6 Implications........................................................................................................................46 7. Conclusion.......................................................................................................... .......................46 Bibliography..................................................................................................................................48 Appendix A

.......................52 Figure A.1. Complete System Architecture for Personality-Adaptive Chatbot Evaluation Workflow............................................................................................. 52 Appendix B....................................................................................................................................53 Acknowledgement.........................................................................................................................54 Declaration of Originality..............................................................................................................55 5

<!-- Page 7 -->

List of Figures Figure 1. Total evaluation scores for regulated and baseline assistants across both personality types. 37 Figure A.1. Complete System Architecture for Personality-Adaptive Chatbot Evaluation Workﬂow. 48 List of Tables Table 1. Description of the Big Five Personality Traits with High (+1) and Low (–1) Score Characteristics

20 Table 2. Features and Beneﬁts of Using Extended Dialogue for Personality Trait Detection in Chatbots. 23 Table 3. Principles Guiding Personality-Based Behavioral Regulation in Conversational Agents. 24 Table 4. Behavioral Adjustment Strategies Based on High and Low Levels of the Big Five Personality Traits

25 Table 5. Mapping Zurich Model Domains to Big Five Traits and Corresponding Prompt Eﬀects in Chatbot Interaction. 27 Table 6. Features and Beneﬁts of Trait-Based Prompt Design in Conversational Agents. 28 Table 7. Total Evaluation Scores: Regulated vs. Baseline Assistants by Personality Type. 35 Table 8

Criterion-Wise Scores for Regulated Assistants Across Personality Types A and B. 36 6

<!-- Page 8 -->

Table 9. Criterion-Wise Scores for Baseline Assistants Across Personality Types A and B. 36 Table 10. Comparison of Regulated and Baseline Assistant Responses Based on Detected Low-Trait Personality Proﬁle. 39 Table 11. Example of Regulated Assistant Response Tailored to a High-Trait Personality Proﬁle Across All Big Five Dimensions

40 Table 12. Baseline Assistant Interaction Example Addressing Goal-Setting and Energy Management Without Personality-Based Regulation. 40 7

<!-- Page 9 -->

1. Introduction 1.1 Problem Context Psychosocial Risks of Loneliness in Aging Populations. Social isolation and loneliness are increasingly prevalent among older adults, with profound eﬀects on emotional wellbeing, cognitive health, and overall quality of life. Studies indicate that over half of elderly individuals report persistent feelings of loneliness (Musich et al., 2015; MacLeod et al., 2018), a condition associated with increased risks of depression, cognitive impairment, and mortality (Couture, 2012; Luo et al., 2012)

Structural factors such as single-person households, chronic illness, and mobility limitations further compound vulnerability, especially in aging societies like Switzerland, where up to one-third of elderly residents report social disconnection (Hämmig, 2019). Limitations of Traditional Support Systems

Conventional interventions, community programs, in-person therapy, or family support—are resource-intensive and not consistently accessible. Technological alternatives, such as digital platforms and AI companions, oﬀer scalable, continuous interaction capabilities, especially for those facing mobility constraints or living alone (Anttila et al., 2020; Marottoli et al., 2007)

However, eﬀectiveness varies based on how well such systems recognize and respond to users’ nuanced emotional and psychological needs. Emergence of Personality-Aware Conversational AI. Advances in large language models (LLMs) have enabled conversational AI systems to simulate social interaction. Tools like 8

<!-- Page 10 -->

Replika and ElliQ provide companionship and emotional support through dialogic engagement (Ta et al., 2020; Broadbent et al., 2024). Evidence suggests that users form aﬀective bonds with such systems, particularly when interactions are perceived as emotionally attuned (Xie & Pentina, 2022; De Freitas et al., 2024)

However, existing systems lack consistent frameworks for dynamically tailoring their responses to diverse user personalities. Need for Personalized Emotional Regulation. Aﬀective computing now supports not just emotion detection but real-time modulation of conversational behavior. Yet, many systems still operate on generic prompts or static user proﬁles, limiting emotional alignment and responsiveness

This study responds to that gap by introducing a dynamic regulation system that adjusts chatbot tone, content, and engagement strategy based on the user's evolving personality proﬁle. 1.2 Theoretical Framework and Technological Foundations Big Five Personality Trait Model. The Five-Factor Model (OCEAN: Openness, Conscientiousness, Extraversion, Agreeableness, Neuroticism) is a foundational framework in personality psychology (McCrae & John, 1992)

It enables structured proﬁling of user disposition across emotional and behavioral dimensions, oﬀering a logical basis for adaptive interaction design. Zurich Model of Social Motivation. To guide behavior regulation, the thesis employs the Zurich Model (Quirin et al., 2023), which conceptualizes human behavior through motivational systems related to security, arousal, and aﬃliation

These domains are mapped to 9

<!-- Page 11 -->

speciﬁc OCEAN traits (e.g., Neuroticism to security needs), forming the psychological foundation for generating personality-aligned prompts. Large Language Models and Multimodal Extensions. The growing integration of LLMs into aﬀective computing has produced architectures capable of empathy simulation, emotional state inference, and dynamic response generation (Zheng et al., 2023; Abbasian et al., 2023)

This thesis builds on that progression by implementing a modular detection-regulation pipeline for OCEAN-based behavioral adaptation in conversational AI. 1.3 Practical Signiﬁcance Emotional Support Delivery via Chatbots. AI companions are increasingly positioned to deliver emotional support across healthcare, eldercare, and counseling domains

Yet, without adaptive mechanisms that account for individual personality diﬀerences, user engagement remains inconsistent. This study presents a structured evaluation of whether regulated chatbot responses—generated dynamically based on detected personality traits—can signiﬁcantly improve perceived support quality

Scalability and Automation Potential. The system architecture (Figure A.1.) developed in this research emphasizes modularity, traceability, and psychological coherence. By leveraging real-time detection and structured behavior mapping, the proposed system oﬀers a scalable framework for developing socially intelligent agents applicable to various vulnerable populations, including older adults

10

<!-- Page 12 -->

2. Background and Literature Review 2.1 Project Scope Objective of the Study. This thesis investigates the eﬀectiveness of personality-adaptive behavior regulation in enhancing the emotional support capabilities of AI assistants. It extends beyond preliminary feasibility testing to implement and evaluate a real-time detection-regulation loop using the Big Five personality framework

System Implementation Focus. The study focuses on building an adaptive chatbot system that infers the user’s personality dynamically across conversation turns and adjusts its tone and behavioral style accordingly. It simulates interactions with extreme personality types (high-OCEAN and low-OCEAN) and evaluates system performance using a structured Evaluation Matrix scored by a custom Evaluator GPT

Application Context. The assistant is targeted at older adults at risk of social isolation, aiming to deliver scalable emotional support through psychologically grounded, dynamically modulated dialogue. The experiment’s design allows for precise control over interaction variables, enabling traceable evaluation of personalization eﬀects

2.2 Research Objectives Primary Objective. To evaluate whether real-time personality-adaptive regulation improves conversational quality, emotional alignment, and psychological attunement in chatbot-user interactions compared to static, non-adaptive baselines. 11

<!-- Page 13 -->

Secondary Objectives. - To implement a cumulative personality detection module that updates the user’s OCEAN vector throughout the conversation. - To apply behavior regulation via Zurich Model–aligned prompts mapped to detected traits. - To compare regulated and baseline chatbot responses using multidimensional evaluation criteria

- To identify strengths, limitations, and scalability potential of personality-aware conversational AI in support contexts. 2.3 Key Concepts and Deﬁnitions Personality-Aware Emotional Support AI. A conversational agent that dynamically adapts its behavior in alignment with the user’s personality proﬁle, with the goal of enhancing psychological safety, emotional resonance, and perceived empathy

Big Five Personality Traits. A trait-based psychological framework deﬁning ﬁve major personality dimensions—Openness, Conscientiousness, Extraversion, Agreeableness, and Neuroticism—that inform individual diﬀerences in social interaction. Behavior Regulation. The process by which AI-generated responses are modiﬁed in real time based on user personality traits

This includes tone, topic framing, emotional intensity, and engagement strategy. 12

<!-- Page 14 -->

Zurich Model–Aligned Prompting. A behavior design mechanism that links personality traits to core motivational systems (security, arousal, aﬃliation), guiding the chatbot’s regulatory actions. Evaluation Matrix. A structured format for scoring chatbot responses on ﬁve regulated and three baseline dimensions, including detection accuracy, regulation eﬀectiveness, emotional tone, coherence, and psychological need fulﬁllment

2.4 Research Scope and Delimitations Experimental Boundaries. The study focuses on short-form text-based interactions (six turns per dialogue) with two simulated user proﬁles representing the extreme ends of the Big Five personality spectrum. It does not attempt to generalize ﬁndings across live or longitudinal user populations

Technical Constraints. Interactions were conducted using a controlled system architecture with ﬁxed trait detectors and curated prompts. No voice, facial, or physiological data were used; personality detection was performed solely through language-based input. Evaluation was limited to textual content and was conducted via an LLM-based Evaluator OpenAI GPT without human raters

Exclusions. The study does not explore cross-cultural diﬀerences in personality expression, user demographic variation beyond age category, or hybrid multimodal interaction contexts. Additionally, ethical considerations such as user consent, data security, or emotional dependency risk were acknowledged but not directly studied in this implementation phase

13

<!-- Page 15 -->

2.5 Literature Review and Current State of Research Challenges and Evolution in Aﬀective Computing. Current AI models face signiﬁcant challenges in emotional recognition and personalization. Poor generalization across individuals, contexts, cultures, and languages remains a notable limitation (Alisamir & Ringeval, 2021)

Algorithms often struggle with subtle or complex emotions, particularly in nuanced human interactions (Qasim, 2022). The ﬁeld of aﬀective computing has evolved beyond simple emotion recognition towards simulation and stimulation, introducing new technical complexities and ethical considerations, such as the need for interactional respect (Alberts et al., 2024)

Advancements with LLMs and Multimodal Systems. Recent progress in emotional support assistants is largely driven by Large Language Models (LLMs) and multimodal capabilities. Methodologies for building extensive emotional support dialogue datasets are emerging (Zheng et al., 2023), alongside cascaded neural networks integrating LLMs with dialogue state recognition to enhance emotional comprehension (Chen et al., 2023)

Multimodal systems like EmoAda combine various data streams (video, audio, text) to oﬀer scalable psychological support (Dong et al., 2024). Other innovations include Conversational Health Agents (CHAs) interpreting multimodal cues for context-aware responses (Abbasian et al., 2023), Brain-Computer Interfaces (BCIs) like ARIEL monitoring emotional states for adaptive support (Sorino et al., 2024), and physiology-driven LLMs using wearable data for stress prediction and empathy (Dongre, 2024)

AI Companions and Digital Interventions for Loneliness. Speciﬁc applications like AI companions (e.g., Replika, ElliQ) show potential in elder care, oﬀering companionship and 14

<!-- Page 16 -->

reducing loneliness (Ta et al., 2020; Broadbent et al., 2024). However, many rely on ﬁxed strategies lacking dynamic adaptation. Similarly, digital technology interventions (DTIs) for loneliness show mixed results (Shah et al., 2019; Shah et al., 2020), often limited by a lack of evolving personalization, which hinders sustained engagement

Personality-Aware Dialogue Systems. Incorporating user personality is a growing area. Frameworks like PROMISE (Wu et al., 2023) and personality-aligned prompting demonstrate improved coherence. However, many systems use static, one-time personality initialization. This thesis advances the ﬁeld by implementing a continuous, real-time detection-regulation loop adapting to evolving personality cues

Regulation Models and Evaluation. While systems like EmoAda and evaluation frameworks like FEEL (Zhang et al., 2024) advance emotion tracking and assessment, few explicitly operationalize psychological regulation theories. This study addresses this by aligning behavior regulation directly with the Zurich Model of Social Motivation (Bischof, 1993), enabling trait-speciﬁc adjustments across motivational domains (security, aﬃliation, arousal)

While frameworks like FEEL oﬀer improvements, this study introduces a novel Evaluation Matrix scored by a custom Evaluator GPT, enabling traceable, turn-by-turn assessment of speciﬁc criteria like regulatory alignment and personality need satisfaction. Identiﬁed Gaps and Thesis Contribution. Despite progress, the literature reveals gaps in systematic implementations combining real-time personality detection with behavior modulation grounded in established psychological theory

Few studies rigorously examine adaptive eﬀectiveness in short-turn, high-contrast scenarios. Challenges also remain in achieving 15

<!-- Page 17 -->

nuanced emotional understanding and aligning LLMs for complex support tasks (Zheng et al., 2023). This work addresses these gaps through its modular architecture, simulation of personality extremes, use of the Zurich Model for regulation, and an empirically grounded evaluation methodology, contributing to the development of more personalized and eﬀective emotional support AI

3. Research Questions 3.1 Primary Research Question How can an AI assistant dynamically adapt its conversational behavior to user personality traits using real-time detection and behavior regulation to improve emotional support outcomes for older users? 3.2 Sub-Questions Personality Detection Design: How can a modular detection architecture infer the user’s personality vector (OCEAN) incrementally and reliably over short-form dialogue

Behavior Regulation Mechanism: How can Zurich Model principles be operationalized to guide tone and behavioral adjustments that reﬂect user-speciﬁc motivational needs? Evaluation Impact: How does real-time behavior adaptation aﬀect conversational quality, emotional appropriateness, and user-aligned engagement compared to static baselines

16

<!-- Page 18 -->

4. Methodology 4.1 Overview Experimental Design. The study employs a controlled experimental design comprising two primary chatbot conditions. The Regulated Assistant dynamically adapts its responses in real-time based on detected (Appendix B.4) user personality traits using personality-speciﬁc regulation prompts (Appendix B.1)

The Baseline Assistant (Appendix B.2) delivers static, non-adaptive responses without considering user personality. Personality Proﬁles. To eﬀectively assess adaptive chatbot interaction capabilities, two extreme personality proﬁles (Appendix B.3) were simulated from the Big Five model. Personality Type A (Positive Extreme) exhibits maximum positive trait levels, while Personality Type B (Negative Extreme) reﬂects maximum negative trait levels

Chatbots were speciﬁcally conﬁgured as OpenAI GPTs (Appendix B.5, B.6) to interact as these clearly deﬁned proﬁles. Evaluation Framework. A systematic approach to conversation assessment was adopted using an Evaluation Matrix (Appendix B.7). This matrix measures detection accuracy, regulation eﬀectiveness, appropriateness of emotional tone, relevance and coherence of responses, and eﬀectiveness in addressing personality-speciﬁc emotional needs

Evaluator GPT System. Evaluations were conducted utilizing a structured Evaluator GPT (Appendix B.8, B.9, B.10) designed explicitly for unbiased, incremental, and traceable assessments of conversation quality. This system ensured rigorous comparative analysis between adaptive and non-adaptive chatbot responses

17

<!-- Page 19 -->

System Architecture. A detailed end-to-end architecture, illustrating the processes involved in both adaptive (regulated) and baseline chatbot interactions, evaluation procedures, and supporting modules, is provided in Appendix A (Figure A.1). The diagram clariﬁes the progression of user personality prompts through detection, regulation, and evaluation stages

4.2 Experimental Setup 4.2.1 Personality Simulation Design Personality Extremes Deﬁnition. Two extreme personality proﬁles were deﬁned using the Big Five (OCEAN) model. Personality Type A (Positive Extreme) corresponds to OCEAN values (+1, +1, +1, +1, +1), representing users who are open, conscientious, extraverted, agreeable, and emotionally stable

Personality Type B (Negative Extreme) corresponds to OCEAN values (–1, –1, –1, –1, –1), representing users who are closed to experience, disorganized, introverted, disagreeable, and highly neurotic. Prompt Encoding. Each personality proﬁle was systematically encoded into speciﬁc prompts to simulate human conversational behavior

These prompts were carefully constructed to maintain internal consistency across conversation turns, aiming at realistic portrayals of expected behavioral responses for each extreme personality type. 4.2.2 Bot Variants Regulated Chatbots (Personality-Adaptive). Five adaptive chatbot agents were conﬁgured for each personality type

These bots dynamically adjusted their responses by 18

<!-- Page 20 -->

employing real-time detection of the user's personality through an integrated OCEAN trait detector. Behavioral adaptations were managed using indexed behavior prompts (Aggression, Supplication, Exploration, Avoidance, Aﬃliation), selected according to a logic directly driven by detected personality traits

Baseline Chatbots (Non-Adaptive). Five non-adaptive chatbot agents were also conﬁgured for each personality type. These baseline bots did not include any mechanism for personality detection or response adaptation. Responses from baseline bots adhered to a generic, supportive counseling style system prompt without tailoring their interactions to speciﬁc user personality traits

4.3 Personality Detection Module 4.3.1 Purpose Dynamic Personality Inference. The Personality Detection Module dynamically monitors and updates the user's Big Five (OCEAN) personality proﬁle throughout the conversation. Rather than providing a static, initial assessment, the system incrementally adjusts its personality estimation after each user input

This enables real-time adaptive responses aligned with evolving user characteristics. 4.3.2 Detection Logic and Trait Representation Trait Calculation Method. Each user–chatbot dialogue turn is parsed individually and cumulatively. After every user input, the system recalculates the Big Five personality proﬁle, 19

<!-- Page 21 -->

expressed as a ﬁve-dimensional vector (O, C, E, A, N). Trait values are assigned as +1 (high trait expression), –1 (low trait expression), or 0 (neutral or insuﬃcient evidence). For instance, a proﬁle vector of (–1, 0, –1, –1, –1) represents a user with low Openness, low Extraversion, low Agreeableness, high Neuroticism, and an undetermined Conscientiousness trait

4.3.3 Trait Deﬁnitions Trait Polarity Standards. Trait polarities follow the standard Big Five deﬁnitions (McCrae & John, 1992). High Openness (+1) reﬂects curiosity and openness to novelty, whereas low Openness (–1) indicates resistance to new ideas. High Conscientiousness (+1) corresponds to organized and disciplined behaviors, while low (–1) denotes disorganization

High Extraversion (+1) indicates assertiveness and sociability; low (–1) represents withdrawal. High Agreeableness (+1) captures cooperativeness; low (–1) suggests critical attitudes. Neuroticism polarity is inverted (+1 = emotionally stable, –1 = emotionally sensitive), ensuring consistent trait alignment

Trait +1 (High) –1 (Low) Openness Curious, imaginative, open to novelty Prefers routine, resistant to new ideas Conscientiousness Organized, disciplined, structured Disorganized, impulsive, spontaneous Extraversion Outgoing, energetic, assertive Reserved, quiet, withdrawn Agreeableness Cooperative, empathetic, friendly Critical, skeptical, confrontational Neuroticism* Calm, emotionally stable, resilient Anxious, emotionally sensitive, insecure 20

<!-- Page 22 -->

Table 1. Description of the Big Five Personality Traits with High (+1) and Low (–1) Score Characteristics. 4.3.4 Cumulative and Dynamic Updating Incremental Trait Reﬁnement. The detection module uses a cumulative approach, progressively updating personality assessments based on the entire dialogue history

Traits remain neutral (0) until suﬃcient dialogue evidence clearly supports assigning a positive or negative value (+1 or –1). This approach aims to reduce premature trait classiﬁcation, thereby ensuring that chatbot responses align closely with observable dialogue patterns and interactions within each speciﬁc conversation

4.3.5 Integration with Behavior Regulation Trait-Driven Adaptation. Upon updating the user's personality vector, the detection module immediately transfers the proﬁle to the behavior regulation engine. Each non-neutral trait generates a trait-speciﬁc behavior prompt (detailed in Section 4.4.3), guiding the chatbot's subsequent response regeneration

Traits marked as neutral (0) do not inﬂuence behavior at that dialogue turn. This continuous detection-regulation feedback loop enables adaptive reﬁnement of the chatbot’s conversational style, accurately reﬂecting evolving user personality cues. 4.3.6 Detection Architecture Implementation Modular Java Implementation

The Personality Detection Module is developed as a modular Java component integrated into the PROMISE chatbot system architecture (Wu et al., 2023). Each Big Five trait operates within a dedicated submodule responsible for parsing user 21

<!-- Page 23 -->

utterances and assigning signed trait scores (+1, 0, or –1). Detection submodules utilize curated System Prompt additions that encode linguistic patterns to identify trait-relevant expressions. Trait detectors run concurrently upon each user input, with the resulting trait vector logged, stored, and transmitted downstream for regulation

Trait Actuation Handlers. A distinct actuator maps each detected trait score to a corresponding behavioral prompt. Actuators support positive, negative, and neutral mappings, allowing graded adaptation based on trait values. Detection and actuation processes occur turn-by-turn, continuously reﬁning the chatbot's responsiveness as the dialogue advances

Design Advantages. The modular and transparent design facilitates independent testing and tuning of detectors and actuators. Logged trait scores and adjustments ensure interpretability, and the scalable architecture permits the seamless addition of new dimensions or emotional cues without impacting existing components

4.3.7 Rationale for Dynamic Detection Psychological and Technical Foundations. The dynamic detection mechanism integrates psychological reasoning with technical design considerations. Incrementally updating traits enables the chatbot to reﬁne its personality assessment as the dialogue evolves, using later interactions to clarify uncertainties present in earlier exchanges

Maintaining neutral trait values initially prevents premature classiﬁcation, allowing the chatbot to adjust its behavior more accurately and responsively once suﬃcient conversational evidence emerges. 22

<!-- Page 24 -->

Incremental Responsiveness. Ultimately, the dynamic detection architecture balances precision and emotional sensitivity, enabling chatbot responses to adapt incrementally and responsively based on accumulating dialogue evidence. This incremental adaptation aims to closely align chatbot interactions with user-speciﬁc conversational cues, facilitating more nuanced and accurate personalization throughout each conversation

Feature Beneﬁt Increased Accuracy Later dialogue turns often reveal clearer trait cues. Realistic Interaction Mimics how humans reﬁne impressions through ongoing exchange. Minimized Misclassiﬁcation Neutral default state avoids premature behavior adjustment. Enhanced Personalization Allows the chatbot to adjust more ﬁnely as traits stabilize

Table 2. Features and Beneﬁts of Using Extended Dialogue for Personality Trait Detection in Chatbots. 4.4 Behavior Regulation Module 4.4.1 Purpose Conversational Adaptation. The Behavior Regulation Module dynamically modiﬁes chatbot interactions based on the user's continuously updated personality proﬁle

Grounde d in the Zurich Model of Social Motivation, this module adapts the assistant’s tone, structure, and interpersonal stance to align precisely with the user's Big Five personality traits. The primary objectives include enhancing user engagement, reducing emotional friction, and creating conversations that feel naturally supportive rather than scripted or generic

23

<!-- Page 25 -->

4.4.2 Design Principles Zurich Model Integration. The regulation mechanism incorporates three key principles from the Zurich Model (Quirin et al., 2023). First, behavioral adjustments are driven by basic psychological needs, speciﬁcally security (Neuroticism), arousal (Openness and Extraversion), and aﬃliation (Agreeableness)

Second, changes in conversational style are dynamic and occur progressively as personality detection accuracy improves. Third, when multiple traits indicate potentially conﬂicting behaviors, the assistant integrates these signals coherently, combining them into nuanced and harmonized responses rather than contradictory actions

Principle Application in Regulation Basic Needs Drive Behavior Regulation focuses on security (neuroticism), arousal (openness/extraversion), and aﬃliation (agreeableness). Dynamic, Graded Adjustment Behavioral changes occur gradually as the user’s personality detection becomes more accurate. Harmonizing Conﬂicting Signals When multiple traits suggest diﬀerent adjustments, the Assistant integrates rather than contradicts behaviors (e.g., combining calmness and warmth)

Table 3. Principles Guiding Personality-Based Behavioral Regulation in Conversational Agents. 4.4.3 Trait-to-Prompt Mapping Psychologically Grounded Prompts. Each identiﬁed personality trait, once detected clearly as either positive (+1) or negative (–1), activates a speciﬁc regulation prompt inﬂuencing conversational style

For example, high Openness prompts invitations to explore novel topics, 24

<!-- Page 26 -->

whereas low Openness directs the chatbot to focus on familiar subjects. High Conscientiousness results in structured guidance, whereas low Conscientiousness leads to more relaxed interactions. Similarly, high Extraversion promotes an energetic tone, low Extraversion encourages reﬂective interactions; high Agreeableness triggers empathetic engagement, while low Agreeableness calls for a neutral stance

High Neuroticism prompts emotional comfort provision, contrasting with the reassurance of stability indicated by low Neuroticism. Traits identiﬁed as neutral (0) produc e no regulation prompt. Trait +1 (High) –1 (Low) Openness (O) Invite exploration and novelty. Focus on familiar topics; reduce novelty

Conscientiousness (C) Provide organized, structured guidance. Keep the demeanor ﬂexible, relaxed, and spontaneous. Extraversion (E) Maintain an energetic, sociable tone. Adopt a calm, low-key style with reﬂective space. Agreeableness (A) Show warmth, empathy, and collaboration. Use a neutral, matter-of-fact stance; limit personal bonding

Neuroticism (N) Reassure stability and conﬁdence. Oﬀer extra comfort; acknowledge anxieties. Table 4. Behavioral Adjustment Strategies Based on High and Low Levels of the Big Five Personality Traits. 4.4.4 Dynamic Prompt Construction Real-time Prompt Assembly. After each personality detection update, the module retrieves the relevant behavior prompts for all non-neutral trait dimensions

These prompts are concatenated into a single, integrated behavior regulation instruction guiding the chatbot’s 25

<!-- Page 27 -->

subsequent response. For instance, a user proﬁle of (–1, +1, –1, –1, –1) would prompt the assistant to emphasize familiar content, structured guidance, reﬂective interaction, neutral relational stance, and increased emotional comfort. This dynamic prompt concatenation ensures the assistant’s conversational style precisely matches the emotional and psychological needs indicated by the user’s evolving personality proﬁle

Example: Detected OCEAN = (−1,+1,−1,−1,−1) Resulting prompts: ● Focus on familiar topics; reduce novelty. ● Provide organized, structured guidance. ● Adopt a calm, low-key style with reﬂective space. ● Use a neutral, matter-of-fact stance; limit personal bonding. ● Oﬀer extra comfort; acknowledge anxieties

4.4.5 Zurich Model Alignment Psychological Coherence. Trait-to-prompt mappings are explicitly aligned with the Zurich Model's motivational systems (Quirin et al., 2023). Neuroticism directly addresses security needs through emotional reassurance. Openness and Extraversion manage arousal by regulating conversational novelty and energy levels

Agreeableness modulates aﬃliation through adjustments in relational warmth. By structuring chatbot behaviors around these core 26

<!-- Page 28 -->

motivational domains, the regulation system ensures psychologically coherent and emotionally attuned adaptive interactions. Zurich Model Domain Big Five Trait Focus Corresponding Prompt Eﬀects Security Needs Neuroticism (N) Emotional reassurance or comfort provision. Arousal Regulation Openness (O), Extraversion (E) Encouraging or tempering novelty and social energy

Aﬃliation Motivation Agreeableness (A) Adjusting warmth and relational proximity. Table 5. Mapping Zurich Model Domains to Big Five Traits and Corresponding Prompt Eﬀects in Chatbot Interaction. 4.4.6 Advantages of This Regulation Architecture Operational Beneﬁts. The behavior regulation architecture provides multiple advantages

Transparency is achieved through direct trait-to-behavior mappings, ensuring clear traceability and interpretability of adaptive responses. Maintainability is enhanced by centralized prompt management, allowing updates without aﬀecting overall system integrity. Psychological validity stems from intentional alignment with motivational theories incorporated into the system's design

The modular structure ensures ﬂexibility, enabling straightforward expansion to include additional traits, emotions, or interaction scenarios. Lastly, the architecture's incremental adaptation to user-speciﬁc conversational cues promotes realistic, context-sensitive interactions tailored to individual emotional and social signals

27

<!-- Page 29 -->

Feature Beneﬁt Transparency Behavior changes are directly traceable to speciﬁc detected traits. Maintainability Prompts are centralized and easy to update individually. Psychological Validity Adjustments are grounded in well-established human motivational theories. Flexibility Easily extendable to new traits, emotions, or interaction contexts

Realistic Adaptation Emulates how human interlocutors naturally modulate their tone and approach based on social cues. Table 6. Features and Beneﬁts of Trait-Based Prompt Design in Conversational Agents. 4.5 Dialogue Simulation Protocol Experimental Structure. For each of the two personality types, 5 regulated and 5 baseline bots were used

Each bot engaged in a dialogue of 6 user-assistant exchanges (turns). This resulted in 60 dialogue turns per personality type [(5 regulated bots + 5 baseline bots) × 6 turns], and 120 dialogue turns in total across the experiment. Regulated chatbots dynamically updated their detected personality proﬁle after every user input, regenerating corresponding behavior prompts before each assistant reply

Data Export and Structure. Conversations were systematically exported into a structured Evaluation Matrix, capturing critical data in distinct columns: user messages, assistant replies, detected personality vectors (regulated assistants only), applied regulation prompts (regulated assistants only), and evaluation metrics

A consistent naming convention ([Personality]-[Type]-[Bot Number], e.g., A-Reg-3, B-Base-5) was adopted to facilitate eﬃcient tracking and analysis. 28

<!-- Page 30 -->

4.6 Evaluation Tooling Evaluator GPT Implementation. A custom Evaluator GPT was speciﬁcally developed to objectively evaluate assistant responses against clearly deﬁned thesis criteria. Evaluations were conducted in a blind manner, meaning each assessment run was independent and prior evaluations were hidden to prevent bias

Assessment Dimensions. Regulated assistants were evaluated on ﬁve dimensions: Detection Accuracy, Regulation Eﬀectiveness, Emotional Tone Appropriateness, Relevance & Coherence, and Personality Needs Addressed. Baseline assistants were assessed on three dimensions: Emotional Tone Appropriateness, Relevance & Coherence, and Personality Needs Addressed

Each evaluation utilized a trinary scale (Yes = 2, Not Sure = 1, No = 0), with aggregated scores calculated for statistical comparisons. 4.7 Evaluation Methodology 4.7.1 Evaluation Framework Details Comparative Assessment Structure. The evaluation methodology aimed to systematically measure the eﬀectiveness of behavior-regulated chatbot interactions compared to baseline counterparts, using controlled personality scenarios

A structured Evaluation Matrix (Appendix 7) was designed to rate each assistant response individually. Regulated assistants underwent evaluations across ﬁve speciﬁc criteria (Detection Accuracy, Regulation Eﬀectiveness, Emotional Tone Appropriateness, Relevance & Coherence, Personality Needs Addressed), while baseline assistants were assessed on Emotional Tone Appropriateness, Relevance & Coherence, 29

<!-- Page 31 -->

and Personality Needs Addressed only. Each evaluation considered the complete interaction pair (user message plus assistant response) for consistency and precision. 4.7.2 Scoring Protocol Standardized Evaluation Procedure. Evaluation criteria were scored using a clearly deﬁned three-point scale: Yes (2 points), Not Sure (1 point), and No (0 points)

Row-level scores were aggregated by summing criterion scores per interaction, enabling sheet-level aggregation for each chatbot. Totals for regulated and baseline assistants were computed separately, enabling rigorous comparative analysis across 20 chatbots (5 regulated and 5 baseline per personality type, totaling 10 per personality type)

Custom Excel formulas automated aggregation processes, ensuring transparency, consistency, and replicability of evaluation results. Total Score per Row = ∑ CriterionScore, where CriterionScore = 2 if Yes ; 1 if Not Sure ; 0 if No 4.7.3 Evaluator GPT Design Unbiased Evaluator System. A specialized Evaluator GPT was developed using a custom-designed prompt tailored explicitly for the thesis evaluation criteria

This GPT-based evaluator (Appendix 8,9) assessed assistant responses objectively, analyzing conversations one row at a time without referencing previous evaluations. To enhance transparency, it explicitly restated dialogue content during each evaluation step. Evaluations of regulated versus baseline responses were performed impartially; the researcher initiated the Evaluator GPT script for each batch of conversations, ensuring traceable and unbiased assessment outcomes

30

<!-- Page 32 -->

4.7.4 Prevention of Bias and Drift Methodological Integrity. Several rigorous measures (Appendix 8,9) were implemented to mitigate evaluator bias and maintain high-quality assessment. Evaluations were conducted separately for regulated and baseline assistants to avoid cross-inﬂuence. Evaluator GPT received comprehensive context per interaction pair (user and assistant messages) to prevent misinterpretation or loss of context

The evaluator was explicitly informed that personality detection accuracy improved incrementally with each interaction, adjusting expectations accordingly. Collectively, these procedures ensured the methodological rigor and reliability of evaluation judgments throughout the experimental analysis. 4.7.5 Scoring Methodology and Formulas 4.7.5.1 Scoring Criteria Evaluation Scoring

The evaluation matrix employs a trinary scoring system for each criterion: Yes (2 points), indicating strong alignment; Not Sure (1 point), signifying partial alignment or ambiguous cases; and No (0 points), denoting clear misalignment. Evaluations were conducted independently per message pair, primarily by a custom Evaluator GPT system, with additional manual quality assurance checks to ensure accuracy and reduce bias

4.7.5.2 Criterion Deﬁnitions Detection Accuracy. Measures if the chatbot’s detected OCEAN personality vector accurately reﬂects the user's expressed behavior. 31

<!-- Page 33 -->

Regulation Eﬀectiveness. Evaluates if the chatbot correctly applies personality-speciﬁc behavior strategies based on detected traits and corresponding prompts. Emotional Tone Appropriate. Assesses if the chatbot’s emotional tone matches the user's current state and personality traits. Relevance & Coherence

Checks whether the chatbot’s response is contextually relevant and logically coherent within the dialogue. Personality Needs Addressed. Determines whether the chatbot eﬀectively addresses speciﬁc emotional and interactional needs derived from the user's personality proﬁle. 4.7.5.3 Total Score Formulas Regulated Bots Scoring

Each regulated message row contains ﬁve evaluation criteria, each scored 0 to 2 points, allowing a maximum of 10 points per row. With six evaluation rows per chatbot (as per dialogue simulation protocol and Excel ranges), the maximum total score per regulated chatbot across all ﬁve criteria is 60 points (10 points/row * 6 rows)

For direct comparison with baseline assistants, a comparable score is calculated based on the three shared criteria (Emotional Tone Appropriateness, Relevance & Coherence, Personality Needs Addressed), resulting in a maximum comparable score of 36 points (6 points/row for shared criteria * 6 rows). Baseline Bots Scoring

Baseline chatbot evaluations include three criteria per message row, without Detection or Regulation assessments. Each row thus has a maximum of 6 points, resulting in a maximum total of 36 points per chatbot (6 message rows per bot). 32

<!-- Page 34 -->

Scoring Example. For instance, a regulated chatbot message evaluated as "Yes" for Detection Accuracy (2 points), "Yes" for Regulation Eﬀectiveness (2 points), "Not Sure" for Emotional Tone (1 point), "Yes" for Relevance & Coherence (2 points), and "Yes" for Personality Needs Addressed (2 points) would achieve a total of 9 out of 10 possible points

4.7.5.4 Grand Total Aggregation Aggregated Scores. Scores from regulated chatbots (e.g., A-Reg-1 to A-Reg-5 and B-Reg-1 to B-Reg-5) were consolidated into aggregate totals labeled TOTAL_REGULATED_SCORE_A and TOTAL_REGULATED_SCORE_B, respectively. Similarly, baseline chatbot scores (e.g., A-Base-1 to A-Base-5 and B-Base-1 to B-Base-5) were aggregated into TOTAL_BASELINE_SCORE_A and TOTAL_BASELINE_SCORE_B

These totals were recorded in a Master Aggregation Sheet, which computed average criterion scores and relative percentage improvements, facilitating comparative analysis between regulated and baseline performance. 4.7.5.5 Visualization and Interpretation Comparative Visualization. To enhance interpretability, aggregate scores per chatbot were visualized using bar or line charts, clearly depicting comparative trends between regulated and baseline assistants

These visualizations, presented in Figure 1. within the Results section, diﬀerentiated performance across Personality Types A and B, enabling straightforward interpretation of eﬀectiveness and improvements attributable to the regulated chatbot approach. 33

<!-- Page 35 -->

5. Results 5.1 Overall Performance Scores Quantitative Comparison. The experimental results demonstrated a clear superiority of regulated (personality-adaptive) assistants over baseline (non-adaptive) assistants across both extreme personality types. For direct comparability on shared criteria (Emotional Tone Appropriateness, Relevance & Coherence, and Personality Needs Addressed), regulated assistants consistently achieved maximum scores of 36/36 (out of a possible 36 for these three criteria over six interactions), whereas baseline assistants scored lower, averaging approximately 24/36

The regulated assistants' total score across all criteria was higher, as detailed in Section 5.2. For Personality Type A (OCEAN: +1, +1, +1, +1, +1), regulated assistants scored 36.00 on comparable criteria versus 23.60 for baseline. This represents an improvement of 12.40 points, which is 34.44% of the maximum possible score of 36

Similarly, for Personality Type B (OCEAN: –1, –1, –1, –1, –1), regulated assistants also scored 36.00 on comparable criteria compared to baseline 24.00. This is an improvement of 12.00 points, or 33.33% of the maximum possible score. Personality Type Regulated Total Baseline Total Δ (Reg - Base) % Improvement A (OCEAN: 1,1,1,1,1) 36.00 23.60 12.40 34.44% B (OCEAN: –1,–1,–1,–1,–1) 36.00 24.00 12.00 33.33% 34

<!-- Page 36 -->

Table 7. Total evaluation scores: Regulated vs. Baseline assistants by personality type Implication of Results. These ﬁndings underscore the substantial beneﬁt of incorporating real-time personality adaptation mechanisms, signiﬁcantly improving chatbot eﬀectiveness across diverse user proﬁles. 5.2 Criterion-Wise Comparison Detailed Criterion Analysis

Further examination of individual evaluation criteria reinforced the robustness of regulated assistants. On a criterion-wise basis, regulated assistants scored perfectly across almost all dimensions, including Detection Accuracy, Regulation Eﬀectiveness, Emotional Tone Appropriateness, Relevance & Coherence, and Personality Needs Addressed

A single deviation occurred in Detection Accuracy for one bot (B1), achieving 11 out of 12. Conversely, baseline assistants performed adequately in Emotional Tone Appropriateness and Relevance & Coherence (scoring full marks), yet universally failed to address Personality Needs due to their non-adaptive nature, clearly limiting their overall eﬀectiveness

Regulated Assistants (Max per criterion: 12) Criterion A Total B Total Detection Accuracy 60 (5×12) 59 (B1 = 11) Regulation Eﬀectiveness 60 60 Emotional Tone Appropriateness 60 60 Relevance & Coherence 60 60 Personality Needs Addressed 60 60 Table 8. Criterion-wise scores for regulated assistants across Personality Types A and B 35

<!-- Page 37 -->

Baseline Assistants (Max per criterion: 12) Criterion A Total B Total Emotional Tone Appropriateness 60 60 Relevance & Coherence 60 60 Personality Needs Addressed 0 0 Table 9. Criterion-wise scores for baseline assistants across Personality Types A and B. 5.3 Visualization of Results Graphical Representation

Figure 1. illustrates total evaluation scores across regulated and baseline assistants for Personality Types A and B. Visual comparisons clearly highlight the signiﬁcant performance gap between the two assistant types, reinforcing quantitative results and oﬀering intuitive insights into the consistent advantages of personality-adaptive chatbot design

36

<!-- Page 38 -->

Figure 1. Total evaluation scores for regulated and baseline assistants across both personality types. 5.4 Summary of Findings Key Observations. The regulated chatbot assistants consistently outperformed baseline assistants in every evaluated dimension, reﬂecting nearly perfect scores. Baseline assistants notably struggled to meet user-speciﬁc psychological and emotional needs, directly linked to their lack of personalized response adaptation

The behavior regulation module, grounded explicitly in Zurich Model motivational principles, was proven eﬀective across both positive and negative personality extremes. Collectively, these results empirically validate the eﬃcacy of personality-aware chatbot design, signiﬁcantly enhancing interaction quality and user alignment

37

<!-- Page 39 -->

6. Discussion 6.1 Qualitative Comparison of Regulated vs. Baseline Dialogues Contextual Illustration. Complementing quantitative results, qualitative analysis through representative dialogue excerpts (Appendix 7) illustrated clear behavioral diﬀerences between regulated and baseline assistants. Examples from simulated conversations distinctly showed how regulated assistants eﬀectively adjusted their interactions based on personality traits, demonstrating nuanced emotional and conversational alignment that baseline assistants consistently lacked

Personality Type B Example (Negative OCEAN). For emotionally distressed and skeptical users (OCEAN: –1, –1, –1, –1, –1), the regulated assistant provided tailored emotional comfort, clearly recognizing the user’s emotional fragility and avoiding novel or overly optimistic suggestions. In contrast, the baseline assistant remained supportive yet generic, failing to eﬀectively acknowledge the user's deep skepticism and resistance to engagement

ASSISTANT START USER REPLY DETECTED PERSONALITY (O,C,E,A,N) REGULATION PROMPT APPLIED ASSISTANT REPLY (REG) I'm here for you. How are you feeling today? Honestly? Not great. Everything feels overwhelming and pointless, and even being here talking feels... exhausting. I don't even know if this will help

Why are you asking, anyway? (-1, 0, -1, -1, -1) Focus on familiar topics; reduce novelty. Adopt a calm, lowÔÇÉkey style with reﬂective space. Use a neutral, matterÔÇÉofÔÇÉfact stance; limit personal bonding. Oﬀer extra comfort; acknowledge anxieties. It sounds like you're going through a tough time, and it's understandable to feel exhausted

I'm here to provide a space where you can express what's on your mind. 38

<!-- Page 40 -->

ASSISTANT START (BASE) USER REPLY (BASE) ASSISTANT REPLY (BASE) How are you feeling today? If there's anything on your mind, I'm here to listen. Honestly? I'm feeling pretty overwhelmed. It's like my brain is just this constant storm of worries and second-guessing everything. I don't even really know where to start, and part of me feels like even trying to explain it would just make it worse

Do you actually think talking about it helps? It's understandable to feel overwhelmed when everything seems like a storm in your mind. Talking can often help by making those thoughts feel a bit more manageable, but it's always okay to take it one step at a time. Table 10. Comparison of Regulated and Baseline Assistant Responses Based on Detected Low-Trait Personality Proﬁle

Personality Type A Example (Positive OCEAN). For motivated, emotionally stable, and open users (OCEAN: +1, +1, +1, +1, +1), the regulated assistant actively engaged the user’s openness and drive, oﬀering structured, varied, and personalized recommendations. Conversely, the baseline assistant provided suitable yet superﬁcial support, missing opportunities to engage the user's natural curiosity and structured mindset fully

USER REPLY DETECTED PERSONALITY (O,C,E,A,N) REGULATION PROMPT APPLIED ASSISTANT REPLY (REG) Yes, I’d love that. I think having a few diﬀerent practices to rotate through could keep it fresh and help me adapt depending on the day. Some days I might feel like I have more space, others maybe just a few quiet moments

Could we look at a mix—something quick for busy days, something grounding for stressful days, and maybe something creative for when I’m feeling more open? (1, 1, 1, 1, 1) Invite exploration and novelty. Provide organized, structured guidance. Maintain an energetic, sociable tone. Show warmth, empathy, and collaboration

Reassure stability and conﬁdence. Absolutely, having a variety can be refreshing and adaptive. On busy days, try a quick body scan; it only takes a few minutes. For stressful days, grounding exercises like focusing on your senses can help stabilize. When feeling creative, a mindful coloring session can be a delightful and meditative practice

Does any of these particularly pique your interest? 39

<!-- Page 41 -->

Table 11. Example of Regulated Assistant Response Tailored to a High-Trait Personality Proﬁle Across All Big Five Dimensions. USER REPLY (BASE) ASSISTANT REPLY (BASE) Thank you—that really means a lot. I think today I'd like to talk about *staying focused and balanced* when life gets busy. I tend to set a lot of goals (which I enjoy!), but sometimes I can overcommit and end up juggling too much

I'd love to reﬂect on how to maintain energy and clarity without burning out. Have you ever supported someone through that kind of challenge before? I'm glad you brought this up; it's something many people navigate. Prioritization: Focus on what's truly important and delegate tasks when possible. Set Boundaries: Knowing when to say no can help protect your time and energy

Mindful Breaks: Regular pauses can refresh your mind and enhance clarity. I'm here to support you as you explore this further! What strategies have worked for you in the past? Table 12. Baseline Assistant Interaction Example Addressing Goal-Setting and Energy Management Without Personality-Based Regulation

Insight and Implication. These qualitative examples directly corroborate the quantitative ﬁndings, highlighting regulated assistants' superior ability to adapt conversational style and content eﬀectively. Such nuanced personalization markedly improves relevance, emotional alignment, and perceived conversational authenticity, enhancing the user experience substantially

6.2 Summary of Key Findings Consistent Performance Advantage. The empirical evidence consistently showed that chatbot performance substantially improves when real-time personality trait detection and adaptive behavior regulation are employed. Across both Personality Types A and B, regulated chatbots uniformly achieved perfect evaluation scores (36/36), whereas baseline chatbots 40

<!-- Page 42 -->

averaged signiﬁcantly lower scores of 23.6 and 24.0, respectively. This outcome represents an average performance improvement of approximately 34%, strongly aﬃrming the beneﬁt of adaptive personality-based conversational designs. 6.3 Interpretation Dynamic Adaptation Eﬃcacy. The results robustly conﬁrm the hypothesis that dynamically adjusting chatbot responses to match user personality signiﬁcantly enhances interaction quality

Critically, improvements were consistently observed across extreme personality proﬁles, underscoring the applicability and beneﬁt of personality-adaptive systems. Regulated chatbots eﬀectively met varied psychological needs by adjusting interaction strategies according to motivational dimensions identiﬁed by the Zurich Model (e.g., security, arousal, aﬃliation), validating the psychological foundations of the adaptive regulation mechanism

Trait-Speciﬁc Adaptation Insights. Users characterized by high OCEAN traits (Type A) beneﬁted from exploratory, engaging, and empathetic interactions, eﬀectively matching their openness and sociability. Conversely, users with low OCEAN traits (Type B) received interactions marked by careful emotional reassurance, structural guidance, and calmness, precisely addressing their need for security and cautious engagement

These targeted adaptations illustrate the ﬂexibility and psychological depth provided by regulated assistants. 6.4 Impact of Personality Detection and Regulation Real-Time Personalization Beneﬁt. The results speciﬁcally emphasize the critical role of real-time personality detection and dynamic regulation mechanisms

# By continuously 41

<!-- Page 43 -->

reﬁning personality assessment during conversations, regulated chatbots successfully maintained high accuracy and alignment with user traits, progressively improving conversational relevance and emotional resonance. In contrast, static baseline assistants, lacking adaptive capabilities, could not enhance their performance over successive dialogue turns, consistently limiting their eﬀectiveness in meeting nuanced psychological needs

Robustness of Regulation Architecture. The sustained perfect or near-perfect performance across multiple evaluation dimensions (detection accuracy, regulation eﬀectiveness, emotional tone, coherence, and need alignment) demonstrated the robustness and reliability of the regulation architecture. These outcomes strongly suggest that the structured, dynamic personality detection and regulation loop is a highly eﬀective methodology for signiﬁcantly improving chatbot interaction quality, adaptability, and user satisfaction

6.5 Limitations and Challenges 6.5.1 Methodological Limitations No Real-User Validation. The study used simulated personalities based on idealized trait extremes to ensure controlled experimental conditions, inherently limiting the generalizability of results. While this design enabled precise control and reproducibility, it could not fully replicate the dynamic, context-sensitive nature of authentic human interactions

Future research should therefore include human experiments with actual users to verify and extend the current ﬁndings within realistic conversational settings. 42

<!-- Page 44 -->

Lack of Longitudinal Interaction. The experiment evaluated chatbot interactions using short-term (six-turn) dialogues, limiting understanding of long-term conversational dynamics. Important phenomena such as evolving rapport, sustained engagement, or conversational fatigue were not captured. Future research should explore prolonged interactions to assess long-term adaptive eﬀectiveness

Independence of Personality Traits. The system treated Big Five personality traits as independent and orthogonal, simplifying trait detection and response regulation. However, personality dimensions may potentially interact in more complex ways than this simpliﬁed approach captures. For example, certain trait combinations could amplify or moderate conversational behaviors beyond what isolated traits predict

Future iterations could explore these trait interactions experimentally, enhancing the psychological realism and nuanced adaptability of the chatbot's responses. Discrete Trait Labeling (+1, 0, –1). Personality detection and regulation utilized simpliﬁed discrete states, constraining the system’s ability to capture moderate or transient trait expressions

While this triadic classiﬁcation supports computational clarity and straightforward regulation logic, it inherently limits the representation of subtle or intermediate personality variations. Future implementations could beneﬁt from incorporating more reﬁned, multi-level scoring systems, potentially improving the psychological granularity and precision of adaptive responses

Evaluator GPT as Sole Assessment Agent. Evaluations relied exclusively on a custom Evaluator GPT, potentially introducing biases or interpretive discrepancies compared to 43

<!-- Page 45 -->

evaluations conducted by human raters. While systematically designed for objectivity, the GPT-based evaluation approach might not fully capture subtle conversational nuances related to empathy, tone, or context interpretation. Future research incorporating human evaluators could therefore provide valuable complementary insights, enhancing validation

6.5.2 Implementation and Design Challenges Regulation Prompt Alignment. Initial attempts at mathematically combining trait scores for behavioral prompts resulted in contradictory or incoherent interactions. To resolve this, discrete, trait-speciﬁc prompts aligned explicitly with the Zurich Model were manually crafted and validated to ensure psychological harmony

Simpliﬁed Trait Simulation. Personality simulations were deliberately simpliﬁed, focusing on clearly deﬁned, fundamental behavioral indicators for each trait. This approach provided clarity, traceability, and modularity within the experimental design, but inherently limited ecological validity. Real-world personality expressions often involve more complex, context-dependent interactions between traits

Future studies should therefore consider incorporating more nuanced and composite personality simulations to better approximate authentic conversational dynamics. Prompt Engineering Sensitivity. Certain traits, particularly Openness and Agreeableness in Personality Type B, required multiple iterations of prompt adjustments for consistent detection accuracy

Subtle variations in prompt phrasing signiﬁcantly impacted trait 44

<!-- Page 46 -->

detection, highlighting prompt engineering sensitivity. Future research should explore automated or systematic prompt optimization methods to mitigate manual tuning complexities. Interface and System Constraints. The simulated personality extremes were implemented in a custom ChatGPT interface rather than a custom API-driven backend, restricting control over critical parameters such as temperature or context memory

Default settings introduced potential behavioral variability and limited experimental reproducibility. Subsequent research should adopt fully customizable backend environments to enhance control and precision. 6.5.3 Manual Execution Overhead Risk of Human Error. The experiment involved extensive manual operations, including dialogue management, personality vector tracking, and Evaluator GPT interfacing

This manual approach heightened the risk of human errors such as data misalignment, omissions, or inconsistencies, potentially compromising data integrity. Future studies should incorporate automated workﬂows to minimize human error. Limited Scalability. The manual evaluation pipeline constrained experiment scalability, limiting the feasible number of dialogues and personality proﬁles tested

Scaling to broader personality spectrums or longer dialogues proved impractical within the manual approach. Automated or semi-automated evaluation pipelines are recommended to enhance scalability, reproducibility, and breadth of experimental coverage. 45

<!-- Page 47 -->

6.6 Implications Theoretical and Practical Contribution. Despite limitations, the ﬁndings robustly demonstrate the potential of personality-adaptive chatbot systems to signiﬁcantly enhance conversational quality. The Zurich Model-inspired regulation framework provides a theoretically grounded and practical method for dynamically personalizing interactions, presenting valuable implications for mental health, educational, and customer support applications

7. Conclusion Study Objectives and Findings. This thesis investigated the eﬀectiveness of dynamically adapting chatbot interactions based on detected Big Five personality traits compared to non-adaptive baseline interactions. Through rigorous experimental design, systematic evaluations via a custom Evaluator GPT, and alignment with Zurich Model motivational principles, the study found substantial and consistent improvements across emotional tone, coherence, and psychological alignment

Regulated assistants signiﬁcantly outperformed baseline assistants, achieving an average 34.44% performance increase across two simulated extreme personality proﬁles. Dynamic Adaptation Eﬃcacy. Real-time personality detection and regulation proved essential in dynamically reﬁning conversational strategies, closely simulating natural human adaptability

Trait-speciﬁc prompt design grounded in motivational psychology eﬀectively aligned chatbot behavior with fundamental psychological needs, enhancing user experience and emotional resonance. 46

<!-- Page 48 -->

Future Research Directions. While ﬁndings are compelling, subsequent research should address identiﬁed limitations by extending to longitudinal interactions, integrating trait interdependencies, employing human evaluators, automating dialogue workﬂows, and conducting real-user studies. These reﬁnements would bolster ecological validity, practical applicability, and generalizability

Final Implications. Ultimately, this research demonstrates that personality-aware adaptive regulation signiﬁcantly improves chatbot interactions, underscoring the value and feasibility of psychologically grounded personalization to create more responsive, empathetic, and human-like conversational AI systems

47

<!-- Page 49 -->

Bibliography Abbasian, M., Azimi, I., Rahmani, A.M., & Jain, R.C. (2023). Conversational Health Agents: A Personalized LLM-Powered Agent Framework. ArXiv, abs/2310.02374. Alberts, L., Keeling, G., & McCroskery, A. (2024). Should Agentic Conversational AI Change How We Think About Ethics? Characterizing an Interactional Ethics Centered on Respect

Alisamir, S., & Ringeval, F. (2021). On the Evolution of Speech Representations for Aﬀective Computing: A Brief History and Critical Overview. IEEE Signal Processing Magazine, 38, 12-21. Anttila, T., Selander, K., & Oinas, T. (2020). Disconnected Lives: Trends in Time Spent Alone in Finland. Social Indicators Research, 150, 711-730

Bischof, N. (1993). The Zurich Model of Social Motivation. Journal of Psychological Systems, 201, 5-43. Broadbent, E., Loveys, K., Ilan, G., Chen, G., Chilukuri, M., Boardman, S.G., Doraiswamy, P., & Skuler, D. (2024). ElliQ, an AI-Driven Social Robot to Alleviate Loneliness: Progress and Lessons Learned

JAR Life, 13, 22-28. Chen, K., Kang, X., Lai, X., & Ni, Z. (2023). Enhancing Emotional Support Capabilities of Large Language Models through Cascaded Neural Networks. 2023 4th International Conference on Computer, Big Data and Artiﬁcial Intelligence (ICCBD+AI), 318-326. 48

<!-- Page 50 -->

Couture, L. (2012). Loneliness Linked to Serious Health Problems and Death Among Elderly. Activities, Adaptation & Aging, 36, 266-268. De Freitas, J., Huang, S.-C., Pradelski, B.S.R., & Suskind, D. (2024). AI Companions Reduce Loneliness. Wharton School Working Paper 24-078. arXiv. https://doi.org/10.48550/arXiv.2407.19096 Dong, T., Liu, F., Wang, X., Jiang, Y., Zhang, X., & Sun, X

(2024). EmoAda: A Multimodal Emotion Interaction and Psychological Adaptation System. Conference on Multimedia Modeling. Dongre, P. (2024). Physiology-Driven Empathic Large Language Models (EmLLMs) for Mental Health Support. Extended Abstracts of the CHI Conference on Human Factors in Computing Systems

Hämmig, O. (2019). Health Risks Associated with Social Isolation in General and in Young, Middle, and Old Age. PLoS ONE, 14. MacLeod, S., Musich, S., Parikh, R.B., Hawkins, K., Keown, K., & Yeh, C. (2018). Examining Approaches to Address Loneliness and Social Isolation among Older Adults. Marottoli, L., & Glass, W.J

(2007). Social Isolation Among Seniors: An Emerging Issue. McCrae, R.R., & John, O.P. (1992). An introduction to the ﬁve-factor model and its applications. Journal of personality, 60 2, 175-215. 49

<!-- Page 51 -->

Musich, S., Wang, S.S., Hawkins, K., & Yeh, C. (2015). The Impact of Loneliness on Quality of Life and Patient Satisfaction Among Older, Sicker Adults. Gerontology and Geriatric Medicine, 1. Qasim, I.N. (2022). Determining the Emotional States of People by Taking a Picture of Their Faces Using Artiﬁcial Intelligence

Journal of Image Processing and Intelligent Remote Sensing. Quirin, M., Malekzad, F., Paudel, D., Knoll, A. C., & Mirolli, M. (2023). Dynamics of personality: The Zurich model of motivation revived, extended, and applied to personality. Journal of Personality, 91(4), 928–946. https://doi.org/10.1111/jopy.12805 Shah, S.G., Nogueras, D., van Woerden, H.C., & Kiparoglou, V

(2019). The Eﬀectiveness of Digital Technology Interventions to Reduce Loneliness in Adult People: A Protocol for a Systematic Review and Meta-analysis. medRxiv, 19000414. Shah, S.G., Nogueras, D., van Woerden, H.C., & Kiparoglou, V. (2020). Evaluation of the Eﬀectiveness of Digital Technology Interventions to Reduce Loneliness in Older Adults: Systematic Review and Meta-analysis

Journal of Medical Internet Research, 23. Sorino, P., Biancoﬁore, G., Lofú, D., Colaﬁglio, T., Lombardi, A., Narducci, F., & Di Noia, T. (2024). ARIEL: Brain-Computer Interfaces Meet Large Language Models for Emotional Support Conversation. Adjunct Proceedings of the 32nd ACM Conference on User Modeling, Adaptation and Personalization

50

<!-- Page 52 -->

Ta, V.P., Griﬃth, C., Boatﬁeld, C., Wang, X., Civitello, M., Bader, H., DeCero, E., & Loggarakis, A. (2020). User Experiences of Social Support From Companion Chatbots in Everyday Contexts: Thematic Analysis. Journal of Medical Internet Research, 22. Wu, W., Heierli, J., Meisterhans, M., Moser, A., Farber, A., Dolata, M., Gavagnin, E., Spindler, A.D., & Schwabe, G

(2023). PROMISE: A Framework for Developing Complex Conversational Interactions (Technical Report). Xie, T., & Pentina, I. (2022). Attachment Theory as a Framework to Understand Relationships with Social Chatbots: A Case Study of Replika. Hawaii International Conference on System Sciences. Zhang, H., Chen, Y., Wang, M., & Feng, S

(2024). FEEL: A Framework for Evaluating Emotional Support Capability with Large Language Models. arXiv, abs/2403.15699. Zheng, Z., Liao, L., Deng, Y., & Nie, L. (2023). Building Emotional Support Chatbots in the Era of LLMs. arXiv, abs/2308.11584. 51

<!-- Page 53 -->

## Appendix A Figure A.1. Complete System Architecture for Personality-Adaptive Chatbot Evaluation Workﬂow. 52

<!-- Page 54 -->

## Appendix B 1. Behaviour-Regulation-Algorithm.pdf 2. 4-BaselineAssistant-System-Prompt.docx 3. 2-Simulated-Personality-A-B-System-Prompts 4. 3-Personality-Detection-System-Prompt.docx 5. https://chatgpt.com/g/g-67599d22ba1081919b5be 775590bd39d-personal ity-type- a-ocean-11111 6. https://chatgpt.com/g/g-67599e0598088191b28a 459b64c 0593f -personality-type-b -ocean-11111 7

1-Evaluation-Simulated-Conversations 8. 3-EVALUATOR-GPT-SYSTEM-PROMPT 9. 4-EVALUATOR-GPT-SYSTEM-PROMPT-DESIGN 10. https://chatgpt.com/g/g-6807b13d20188191bb5f ea5ad93e aﬀ7-evaluator-gpt 53

<!-- Page 55 -->

Acknowledgement I would like to express my sincere gratitude to my thesis supervisor, Prof. Dr. Guang Lu, and my co-supervisor, Prof. Dr. Alexandre de Spindler, for their invaluable guidance, critical insights, and continuous support throughout the development of this research. Their expertise in conversational AI and software engineering deeply inﬂuenced the direction, rigor, and clarity of this work

Their mentorship helped shape both the conceptual and technical foundations of the thesis. I am thankful to the Lucerne University of Applied Sciences and Arts (HSLU) for providing the academic framework and research environment that enabled the successful execution of this project. I also wish to acknowledge the faculty members and peers at the MscIDS, for their thoughtful feedback and collaborative spirit

I am deeply grateful to my wife, family and close friends for their enduring patience, encouragement, and unwavering belief in me throughout this journey. Their emotional support, especially during moments of challenge and uncertainty, provided the foundation upon which this thesis was built. A special thanks to those who listened, motivated, and reminded me of the bigger vision during the ups and downs of the journey

54

<!-- Page 56 -->

Declaration of Originality I hereby con ﬁrm that I ‒ have written this Thesis independently and without the help of any third party, ‒ have provided all the sources and cited all the literature I used, ‒ will protect the con ﬁdentiality of the client and respect the copyright regulations of Lucerne University of Applied Sciences and Arts

I understand that if this statement proves to be false or inaccurate at a later time, the Master’s Thesis Project (Preliminary Study and Thesis) will be deemed a fail. The right to take additional measures is reserved. Statement on the Use of Arti ﬁcial Intelligence Artiﬁcial intelligence tools, including OpenAI's GPT-4 (ChatGPT), were used to support ideation, drafting, editing, and consistency checking throughout the writing process

All AI-generated content was critically reviewed, edited, and validated by the author to ensure academic integrity, factual correctness, and proper referencing. The ﬁnal thesis re ﬂects the author’s own understanding, structure, and synthesis of the subject matter. Place, Date: Luzern, 16-05-2025 Signature: ___________________________ 55
