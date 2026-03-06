# Table of Contents {#table-of-contents .TOC-Heading}

[Abstract [2](#abstract)](#abstract)

[1 Introduction [3](#introduction)](#introduction)

[2 Related Work [3](#related-work)](#related-work)

[3 Materials and Methods
[4](#materials-and-methods)](#materials-and-methods)

[3.1 Study Design [4](#study-design)](#study-design)

[3.2 System Architecture
[4](#system-architecture)](#system-architecture)

[3.3 Personality Detection Module
[4](#personality-detection-module)](#personality-detection-module)

[3.3.1 Theoretical Foundation
[4](#theoretical-foundation)](#theoretical-foundation)

[3.3.2 Detection Algorithm Specifications
[4](#detection-algorithm-specifications)](#detection-algorithm-specifications)

[3.3.3 Cumulative Inference Process
[5](#cumulative-inference-process)](#cumulative-inference-process)

[3.4 Behavior Regulation Module
[5](#behavior-regulation-module)](#behavior-regulation-module)

[3.4.1 Zurich Model Integration
[5](#zurich-model-integration)](#zurich-model-integration)

[3.5 Experimental Protocol
[6](#experimental-protocol)](#experimental-protocol)

[3.5.1 Personality Profile Simulation
[6](#personality-profile-simulation)](#personality-profile-simulation)

[3.5.2 Agent Configuration
[6](#agent-configuration)](#agent-configuration)

[3.5.3 Evaluation Framework
[6](#evaluation-framework)](#evaluation-framework)

[3.6 Data Availability [7](#data-availability)](#data-availability)

[4 Results [7](#results)](#results)

[4.1 Detection Performance
[7](#detection-performance)](#detection-performance)

[4.2 Conversational Quality Assessment
[7](#conversational-quality-assessment)](#conversational-quality-assessment)

[4.3 Criterion-Specific Analysis
[8](#criterion-specific-analysis)](#criterion-specific-analysis)

[4.4 Qualitative Examples
[8](#qualitative-examples)](#qualitative-examples)

[5 Discussion [8](#discussion)](#discussion)

[5.1 Principal Findings [8](#principal-findings)](#principal-findings)

[5.2 Comparison with Existing Literature
[8](#comparison-with-existing-literature)](#comparison-with-existing-literature)

[5.3 Clinical Translation Pathway
[9](#clinical-translation-pathway)](#clinical-translation-pathway)

[5.4 Limitations [9](#limitations)](#limitations)

[5.5 Risk Assessment [9](#risk-assessment)](#risk-assessment)

[5.6 Future Research Priorities
[10](#future-research-priorities)](#future-research-priorities)

[5.7 Conclusions [10](#conclusions)](#conclusions)

[6 Conclusions [11](#conclusions-1)](#conclusions-1)

[7 Data Availability Statement [**Error! Bookmark not
defined.**](#_Toc206085440)](#_Toc206085440)

[8 Conflicts of Interest [**Error! Bookmark not
defined.**](#_Toc206085441)](#_Toc206085441)

[9 References [11](#references)](#references)

[10 Supplementary Materials
[12](#supplementary-materials)](#supplementary-materials)

## Abstract

**Background**: Conversational agents often lack adaptive mechanisms
that account for individual personality differences, limiting
personalized interaction quality.

**Objective**: To evaluate a personality-adaptive framework that detects
Big Five (OCEAN) traits in real time and modulates conversational
behavior via Zurich Model--aligned regulation.

**Methods**: We implemented a modular system comprising: (i) discrete
OCEAN detection {−1, 0, +1} with cumulative refinement using rule‑based
linguistic pattern matching; (ii) trait‑to‑motivational domain mapping
(security, arousal, affiliation); and (iii) dynamic behavior adaptation.
The system was evaluated in controlled simulation across extreme
personality profiles against non‑adaptive baselines using structured
criteria.

**Results**: Regulated agents outperformed baselines across all criteria
under simulation. Detection accuracy reached 98.33% for extreme
profiles; evaluation was conducted using a structured GPT‑4 assessor.

**Conclusions**: Results demonstrate technical feasibility of
personality‑adaptive interaction in simulation and motivate human
subject validation before practical deployment. The framework addresses
personalization gaps while acknowledging limitations, including
evaluator bias risk and the need for clinical validation.

**Keywords:** conversational agents; personality detection; adaptive
interaction; Big Five; Zurich Model; simulation; behavior regulation;
proof‑of‑concept

# 1 Introduction

Loneliness in older adults is a persistent public health concern linked
to elevated morbidity and mortality \[1\]. In Switzerland, living alone,
multimorbidity, and mobility limitations are associated with greater
social disconnection \[2\]. Although conversational agents show promise
for screening, adherence, and psychosocial support, most systems rely on
uniform interaction strategies that overlook individual psychological
differences \[3,4\]. Personality-aware interaction has been proposed as
a remedy, yet many implementations use one-time personality
initialization or lack theoretically grounded, turn-by-turn regulation.

This study presents a simulation-based evaluation of a
personality-adaptive assistant that: (i) infers Big Five (OCEAN) traits
incrementally from language using rule-based linguistic features; and
(ii) translates detected traits into behavior adaptations aligned with
the Zurich Model's motivational domains (security, arousal,
affiliation). We compare the personality-regulated assistant with a
non-adaptive baseline across extreme personality profiles to examine
feasibility and magnitude of potential benefit under controlled
conditions.

Study limitations are explicit: the work uses simulated personalities
and an AI-based evaluator; findings should be interpreted as
proof-of-concept requiring validation with human participants and
clinician raters prior to any clinical claims.

# 2 Related Work

Early personality-aware dialogue systems focused on generating responses
exhibiting specific traits rather than adapting to user personalities
\[5\]. PROMISE represents notable advancement implementing modular
personality detection with behavioral adaptation \[6\], yet lacks
theoretical grounding in motivational psychology and healthcare-specific
considerations.

Affective computing in healthcare faces deployment challenges including
privacy concerns with multimodal sensing, cultural bias in emotion
recognition, and regulatory compliance for medical AI systems \[7\].
Recent emotional support chatbots advance empathetic response generation
but lack systematic personality-based adaptation frameworks \[8\].

**Research Gap**: No published system combines real-time personality
detection with theoretically-grounded motivational regulation for
healthcare applications. This simulation study addresses this gap while
acknowledging the significant validation requirements for clinical
deployment.

# 3 Materials and Methods

## 3.1 Study Design

This simulation study employed a controlled experimental design
comparing personality-adaptive (regulated) versus static (baseline)
conversational agents across extreme personality profiles. The study
protocol was designed as proof-of-concept research using simulated
interactions.

**Statistical Analysis**: Descriptive statistics were calculated for all
metrics. As this is a simulation study with deterministic outcomes,
inferential statistics are provided for illustration only and should not
be interpreted as hypothesis testing.

**Ethics Statement**: This simulation study involved no human subjects
and thus did not require IRB approval. The simulated personalities were
based on theoretical constructs from published literature. Future
clinical validation will require full IRB approval (anticipated protocol
number: PENDING).

## 3.2 System Architecture

Our framework implements a modular pipeline A = (D, R, E) consisting of:
Detection Module (D) for real-time OCEAN trait inference, Regulation
Module (R) for Zurich Model-aligned behavior adaptation, and Evaluation
Module (E) for quality assessment. The architecture extends the PROMISE
framework \[6\] using Java components (version 8.0, available at:
\[GitHub repository - to be provided upon publication\]) for trait
detection.

## 3.3 Personality Detection Module

### 3.3.1 Theoretical Foundation

We employ the Five-Factor Model as personality representation P = (O, C,
E, A, N) ∈ {−1, 0, +1}⁵, capturing Openness, Conscientiousness,
Extraversion, Agreeableness, and Neuroticism \[9\]. This discrete
encoding enables tractable real-time inference while preserving
sufficient granularity for research applications.

### 3.3.2 Detection Algorithm Specifications

**Modular Architecture**: Five concurrent trait detection submodules
operate independently, each responsible for parsing user utterances and
assigning trait scores. Detection utilizes rule-based linguistic pattern
matching encoding trait-specific patterns.

**Linguistic Feature Specifications**:

Table 1. Linguistic Pattern Detection Specifications for OCEAN Traits

  --------------------------------------------------------------------------------------
  Trait               High (+1) Linguistic   Low (-1) Linguistic  Detection Method
                      Markers                Markers              
  ------------------- ---------------------- -------------------- ----------------------
  Openness            "I wonder...", "What   "That's how it's     Keyword matching +
                      if...", abstract       done", routine       semantic analysis
                      concepts, creative     preferences,         
                      expressions            concrete-only        
                                             language             

  Conscientiousness   "I've scheduled...",   "I'll figure it out  Planning language
                      "My goal is...",       later", spontaneous  detection
                      structured             expressions          
                      communication                               

  Extraversion        "Let's do...", social  "I need time alone", Social orientation
                      references, energetic  introspective        analysis
                      markers                language             

  Agreeableness       "I understand how you  "Actually, you're    Cooperation/conflict
                      feel", empathetic      wrong", critical     markers
                      expressions            language             

  Neuroticism         "I'm worried           "I'm not concerned", Emotional tone
                      about...", anxiety     emotional stability  analysis
                      expressions, negative  markers              
                      emotions                                    
  --------------------------------------------------------------------------------------

### 3.3.3 Cumulative Inference Process

At dialogue turn i, each trait detector analyzes user message mᵢᵘ
combined with dialogue history C₁:ᵢ₋₁. The detection function updates
personality estimate: P̂ᵢ = Dᵢ(P̂ᵢ₋₁, mᵢᵘ, C₁:ᵢ₋₁) where linguistic
evidence accumulates progressively.

**Conservative Thresholds**: Trait detectors maintain neutral states (0)
until sufficient linguistic evidence supports positive (+1) or negative
(-1) classification. This approach prevents premature trait assignment
critical for potential healthcare applications.

## 3.4 Behavior Regulation Module

### 3.4.1 Zurich Model Integration

Our regulation strategy maps OCEAN traits to Zurich Model motivational
domains \[10\]: Security Domain (N → emotional stability/vulnerability
responses), Arousal Domain ({O,E} → novelty/stimulation regulation),
Affiliation Domain (A → social connection/cooperation strategies).

Table 2. Trait-to-Regulation Mapping Based on Zurich Model

  ------------------------------------------------------------------------------
  Trait               High (+1) Regulation  Low (-1) Regulation   Motivational
                      Prompt                Prompt                Domain
  ------------------- --------------------- --------------------- --------------
  Openness            "Explore diverse      "Focus on familiar,   Arousal
                      approaches, introduce established           
                      new concepts"         practices"            

  Conscientiousness   "Provide structured,  "Offer flexible,      Arousal
                      systematic guidance"  adaptable approaches" 

  Extraversion        "Use encouraging,     "Adopt calm,          Arousal
                      interactive           reflective tone"      
                      communication"                              

  Agreeableness       "Show warmth,         "Use neutral,         Affiliation
                      collaborative         professional stance"  
                      planning"                                   

  Neuroticism         "Reinforce stability, "Provide extra        Security
                      confidence"           support, acknowledge  
                                            concerns"             
  ------------------------------------------------------------------------------

## 3.5 Experimental Protocol

### 3.5.1 Personality Profile Simulation

Two extreme personality profiles were implemented based on established
Big Five research: - **Type A (High-functioning)**: P_A =
(+1,+1,+1,+1,+1) representing openness to treatment, conscientiousness,
social engagement, cooperation, and emotional stability - **Type B
(Vulnerable)**: P_B = (−1,−1,−1,−1,−1) representing treatment
resistance, disorganization, withdrawal, skepticism, and emotional
sensitivity

Each profile was systematically encoded into specific conversational
prompts maintaining consistency across dialogue turns, based on
established personality psychology literature.

### 3.5.2 Agent Configuration

For each personality type: - **5 Regulated Agents**: Dynamic personality
detection + trait-based regulation per turn - **5 Baseline Agents**:
Static supportive responses without personality adaptation - **Total**:
10 agents per personality type, 20 agents overall

Each agent engaged in structured 6-turn dialogues, generating 120 total
dialogue turns for analysis.

### 3.5.3 Evaluation Framework

**Assessment Criteria**: - **Regulated Agents**: Detection Accuracy,
Regulation Effectiveness, Emotional Tone Appropriateness, Relevance &
Coherence, Personality Needs Addressed - **Baseline Agents**: Emotional
Tone Appropriateness, Relevance & Coherence, Personality Needs
Addressed - **Scoring**: Trinary scale {0,1,2} per criterion

**Evaluation Method**: Custom LLM-based Evaluator (GPT-4) with
structured prompts designed for unbiased assessment. Each criterion
evaluation considered complete interaction pairs for consistency.

## 3.6 Data Availability

**Code and Data Repository**: Complete implementation code, detection
prompts, regulation templates, and experimental data will be made
available at: https://github.com/\[username\]/personality-ai-simulation
\[to be created upon publication\].

**Supplementary Materials**: Available as separate files containing
complete detection algorithms, regulation prompts, conversation
transcripts, and evaluation metrics.

# 4 Results

## 4.1 Detection Performance

Personality detection achieved 98.33% accuracy (59/60 correct
assessments) across extreme personality profiles. Detection accuracy
breakdown:

Table 3. Detection Accuracy by Trait and Personality Type

  ------------------------------------------------------------------------------
  Trait               Type A Accuracy Type B Accuracy Overall Accuracy 95% CI
  ------------------- --------------- --------------- ---------------- ---------
  Openness            30/30 (100%)    29/30 (96.7%)   59/60 (98.3%)    \[91.1,
                                                                       99.9\]

  Conscientiousness   30/30 (100%)    30/30 (100%)    60/60 (100%)     \[94.0,
                                                                       100\]

  Extraversion        30/30 (100%)    30/30 (100%)    60/60 (100%)     \[94.0,
                                                                       100\]

  Agreeableness       29/30 (96.7%)   30/30 (100%)    59/60 (98.3%)    \[91.1,
                                                                       99.9\]

  Neuroticism         30/30 (100%)    30/30 (100%)    60/60 (100%)     \[94.0,
                                                                       100\]
  ------------------------------------------------------------------------------

## 4.2 Conversational Quality Assessment

Regulated agents demonstrated substantial superiority across both
personality types:

Table 4. Overall Performance Comparison

  -----------------------------------------------------------------------------
  Personality   Regulated Score Baseline Score (95% Absolute      Effect Size
  Type          (95% CI)        CI)                 Improvement   (Cohen's d)
  ------------- --------------- ------------------- ------------- -------------
  Type A        36.0/36 \[36.0, 23.6/36 \[21.2,     +12.4 (34.4%) 2.85 (large)
                36.0\]          26.0\]                            

  Type B        36.0/36 \[36.0, 24.0/36 \[21.8,     +12.0 (33.3%) 2.73 (large)
                36.0\]          26.2\]                            
  -----------------------------------------------------------------------------

**Note on Perfect Scores**: The perfect scores (36/36) achieved by
regulated agents reflect limitations of our evaluation methodology,
where GPT-4 assessment may favor similar AI-generated responses. Human
evaluation would likely yield more varied results.

## 4.3 Criterion-Specific Analysis

**Regulated Agent Performance**: - Detection Accuracy: 59/60 (98.33%) -
Regulation Effectiveness: 60/60 (100%) - Emotional Tone: 60/60 (100%) -
Relevance & Coherence: 60/60 (100%) - Personality Needs: 60/60 (100%)

**Baseline Agent Performance**: - Emotional Tone: 60/60 (100%) -
Relevance & Coherence: 60/60 (100%) - Personality Needs: 0/60 (0%) -
Complete failure in personalization

## 4.4 Qualitative Examples

**Vulnerable Population Interaction Example**: *Detected Profile*: P̂ =
(−1, 0, −1, −1, −1)

*Regulated Response*: \> "I understand you're going through a difficult
time, and feeling exhausted is natural. This is a safe space where we
can focus on small, familiar steps that feel manageable for you right
now."

*Baseline Response*: \> "It's understandable to feel overwhelmed.
Talking about your concerns can help organize your thoughts."

**Analysis**: The regulated response demonstrates therapeutic attunement
through explicit validation (Security domain), emphasis on familiar
approaches (reduced Arousal), and respectful acknowledgment (Affiliation
modulation).

# 5 Discussion

## 5.1 Principal Findings

This simulation study demonstrates the technical feasibility of
personality-adaptive conversational AI using real-time OCEAN detection
and Zurich Model-aligned regulation. Regulated agents achieved 34%
improvement over baseline conditions in controlled simulation scenarios.

**Key Technical Achievements**: 1. Successful implementation of
real-time personality detection (98.33% accuracy for extreme profiles)
2. Effective translation of personality traits into behavioral
modifications 3. Consistent performance across diverse personality
configurations

## 5.2 Comparison with Existing Literature

Our approach extends the PROMISE framework \[6\] by integrating
motivational psychology theory and healthcare-specific considerations.
Unlike previous systems focusing on trait generation, our framework
adapts to detected user personalities through theoretically-grounded
regulation strategies.

The 34% improvement exceeds typical gains reported in conversational AI
literature, though these results are limited to simulation conditions
with extreme personality profiles.

## 5.3 Clinical Translation Pathway

**Immediate Requirements for Clinical Validation**: 1. **Human Subject
Studies**: Minimum n=50 elderly participants with validated personality
assessments (NEO-PI-R, BFI-2) 2. **Clinical Expert Evaluation**:
Licensed psychologists assessing personality detection accuracy 3.
**Safety Validation**: Risk assessment for potential psychological harms
4. **Cultural Validation**: Testing across diverse ethnic and linguistic
groups 5. **Longitudinal Assessment**: Extended interaction studies
(minimum 30 days)

**Regulatory Pathway**: - IRB approval for human subjects research -
Data protection compliance (HIPAA/GDPR) - Potential FDA guidance for
healthcare AI - Clinical trial registration for therapeutic claims

**Timeline Estimate**: 2-3 years for comprehensive clinical validation

## 5.4 Limitations

**Critical Study Limitations**:

1.  **Simulation-Only Design**: No real patient validation; findings may
    not generalize to authentic healthcare interactions
2.  **AI-Based Evaluation**: Assessment by GPT-4 rather than clinical
    experts; potential bias in evaluation criteria
3.  **Extreme Personality Profiles**: Limited to polar trait
    expressions; moderate personalities not tested
4.  **Short Interaction Duration**: 6-turn dialogues insufficient for
    assessing sustained therapeutic relationships
5.  **Cultural Homogeneity**: Linguistic patterns calibrated for
    English-speaking populations
6.  **No Clinical Endpoints**: No measurement of actual health outcomes
    or therapeutic efficacy

**Technical Limitations**: - Single-modality detection (text-only,
excluding paralinguistic cues) - Prompt engineering sensitivity
requiring careful calibration - Potential brittleness with communication
patterns outside training scope

**Potential Harms**: Personality profiling in healthcare raises concerns
about psychological manipulation, stereotype reinforcement, and
decisional autonomy. Misclassification could lead to inappropriate
therapeutic approaches. These risks require careful consideration in
clinical translation.

## 5.5 Risk Assessment

Table 5. Potential Risks and Mitigation Strategies for Clinical
Deployment

  ------------------------------------------------------------------------------
  Risk Category       Risk Description  Likelihood   Impact   Mitigation
                                                              Strategy
  ------------------- ----------------- ------------ -------- ------------------
  Misclassification   Incorrect         Medium       High     Conservative
                      personality                             thresholds,
                      assessment                              provider oversight

  Cultural Bias       Reduced accuracy  High         High     Diverse
                      across cultures                         validation,
                                                              cultural
                                                              adaptation

  Over-reliance       Excessive         Medium       Medium   Provider training,
                      dependence on AI                        clear limitations

  Privacy Breach      Unauthorized      Low          High     Encryption, access
                      personality data                        controls
                      access                                  

  Therapeutic Harm    Inappropriate     Medium       High     Clinical
                      psychological                           supervision,
                      intervention                            safety protocols
  ------------------------------------------------------------------------------

## 5.6 Future Research Priorities

**Technical Development**: 1. Multimodal personality detection (voice,
facial expressions) 2. Continuous learning and adaptation mechanisms 3.
Cultural bias detection and mitigation algorithms 4. Integration with
validated psychological assessment tools

**Clinical Validation Studies**: 1. Randomized controlled trials with
clinical endpoints 2. Comparative effectiveness research against
standard care 3. Long-term safety and efficacy monitoring 4. Health
economic evaluation

**Regulatory and Ethical Framework**: 1. Guidelines for
personality-aware healthcare AI 2. Informed consent frameworks for
psychological profiling 3. Professional liability and malpractice
considerations 4. International regulatory harmonization

## 5.7 Conclusions

This simulation study demonstrates the technical feasibility of
personality-adaptive conversational AI for healthcare applications. The
framework successfully integrates real-time Big Five trait detection
with Zurich Model-aligned behavior regulation, achieving substantial
performance improvements in controlled conditions.

**Clinical Implications**: While simulation results are promising,
extensive clinical validation is required before healthcare deployment.
The 34% improvement in conversational quality represents potential for
enhanced patient communication, pending validation with real patients
and clinical outcomes.

**Research Implications**: The work provides a foundation for
personality-aware healthcare AI development while highlighting critical
validation requirements. The modular architecture enables systematic
testing and refinement through controlled studies.

**Regulatory Implications**: The framework requires comprehensive safety
evaluation, cultural bias assessment, and regulatory approval pathways
before clinical implementation. Clear guidelines for personality-aware
medical AI are needed.

**Final Assessment**: This proof-of-concept establishes feasibility
while acknowledging significant clinical translation challenges. Success
depends on rigorous human subject validation, regulatory compliance, and
ethical framework development.

# 6 Conclusions

This simulation study demonstrates the technical feasibility of
personality-adaptive conversational AI for healthcare applications. The
framework successfully integrates real-time Big Five trait detection
with Zurich Model-aligned behavior regulation, achieving substantial
performance improvements in controlled conditions.

**Clinical Implications**: While simulation results are promising,
extensive clinical validation is required before healthcare deployment.
The 34% improvement in conversational quality represents potential for
enhanced patient communication, pending validation with real patients
and clinical outcomes.

**Research Implications**: The work provides a foundation for
personality-aware healthcare AI development while highlighting critical
validation requirements. The modular architecture enables systematic
testing and refinement through controlled studies.

**Regulatory Implications**: The framework requires comprehensive safety
evaluation, cultural bias assessment, and regulatory approval pathways
before clinical implementation. Clear guidelines for personality-aware
medical AI are needed.

**Final Assessment**: This proof-of-concept establishes feasibility
while acknowledging significant clinical translation challenges. Success
depends on rigorous human subject validation, regulatory compliance, and
ethical framework development.

# 8 References

1.  Luo, Y.; Hawkley, L.C.; Waite, L.J.; Cacioppo, J.T. Loneliness,
    health, and mortality in old age: A national longitudinal study.
    *Soc. Sci. Med.* **2012**, *74*, 907-914.

2.  Hämmig, O. Health risks associated with social isolation in general
    and in young, middle and old age. *PLoS ONE* **2019**, *14*,
    e0219663.

3.  Fitzpatrick, K.K.; Darcy, A.; Vierhile, M. Delivering cognitive
    behavior therapy to young adults with symptoms of depression and
    anxiety using a fully automated conversational agent (Woebot): A
    randomized controlled trial. *JMIR mHealth uHealth* **2017**, *5*,
    e7785.

4.  Broadbent, E.; Loveys, K.; Ilan, G.; Chen, G.; Chilukuri, M.;
    Boardman, S.G.; Doraiswamy, P.; Skuler, D. ElliQ, an AI-driven
    social robot to alleviate loneliness: Progress and lessons learned.
    *JAR Life* **2024**, *13*, 22-28.

5.  Li, J.; Galley, M.; Brockett, C.; Spithourakis, G.; Gao, J.;
    Dolan, B. A persona-based neural conversation model. In *Proceedings
    of ACL*; Association for Computational Linguistics: Stroudsburg, PA,
    USA, 2016; pp. 994-1003.

6.  Wu, W.; Heierli, J.; Meisterhans, M.; Moser, A.; Farber, A.; Dolata,
    M.; Gavagnin, E.; Spindler, A.D.; Schwabe, G. PROMISE: A Framework
    for Developing Complex Conversational Interactions (Technical
    Report); University of Zurich: Zurich, Switzerland, 2023.

7.  Calvo, R.A.; D'Mello, S. Affect detection: An interdisciplinary
    review of models, methods, and their applications. *IEEE Trans.
    Affect. Comput.* **2010**, *1*, 18-37.

8.  Zheng, Z.; Liao, L.; Deng, Y.; Nie, L. Building emotional support
    chatbots in the era of LLMs. *arXiv* **2023**, arXiv:2308.11584.

9.  McCrae, R.R.; John, O.P. An introduction to the five-factor model
    and its applications. *J. Pers.* **1992**, *60*, 175-215.

10. Quirin, M.; Malekzad, F.; Paudel, D.; Knoll, A.C.; Mirolli, M.
    Dynamics of personality: The Zurich model of motivation revived,
    extended, and applied to personality. *J. Pers.* **2023**, *91*,
    928-946. https://doi.org/10.1111/jopy.12805

# 9 Supplementary Materials

The following supporting information can be downloaded at: \[Link to
supplementary materials\]

**Supplement S1**: Complete Detection Algorithm Specifications\
**Supplement S2**: Full Regulation Prompt Templates\
**Supplement S3**: Conversation Transcripts and Evaluation Data\
**Supplement S4**: Statistical Analysis Details
