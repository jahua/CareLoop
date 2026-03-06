## Evaluator GPT System Prompt Design Document

### Purpose

The Evaluator GPT system prompt is designed to systematically and
objectively assess chatbot responses in alignment with the objectives of
the Master\'s thesis, specifically comparing regulated
(personality-adaptive) chatbots against baseline (non-adaptive)
chatbots. This document outlines the rationale, structure, and
implementation of the Evaluator GPT prompt.

### Thesis Context

The Master\'s thesis aims to empirically evaluate the effectiveness of
chatbot responses adapted to extreme user personality types, utilizing
the Big Five personality model (OCEAN). Two extremes of personalities
are simulated:

- **Personality Type A (Positive Extreme)**: OCEAN = (+1, +1, +1, +1,
  +1)

- **Personality Type B (Negative Extreme)**: OCEAN = (--1, --1, --1,
  --1, --1)

### Evaluator GPT Role

The Evaluator GPT acts as an unbiased, transparent, and systematic
assessor of chatbot conversations, differentiating clearly between
regulated and baseline chatbot responses.

### Evaluation Criteria

The Evaluator assesses two types of chatbots, each with their own
clearly defined criteria:

**Regulated Assistant:**

- Detection Accuracy

- Regulation Effectiveness

- Emotional Tone Appropriateness

- Relevance & Coherence

- Personality Needs Addressed

**Baseline Assistant:**

- Emotional Tone Appropriateness

- Relevance & Coherence

- Personality Needs Addressed

### Definition of OCEAN Traits

  ---------------------------------------------------------------------------
  **Trait**           **High (+1)**              **Low (--1)**
  ------------------- -------------------------- ----------------------------
  Openness (O)        Curious, imaginative, open Prefers routine, resistant
                      to novelty.                to new ideas.

  Conscientiousness   Organized, disciplined,    Disorganized, impulsive,
  (C)                 structured.                spontaneous.

  Extraversion (E)    Outgoing, energetic,       Reserved, quiet, withdrawn.
                      assertive.                 

  Agreeableness (A)   Cooperative, empathetic,   Critical, skeptical,
                      friendly.                  confrontational.

  Neuroticism (N)     Emotionally stable,        Anxious, emotionally
                      resilient, calm.           sensitive, insecure.
  ---------------------------------------------------------------------------

*Note: Neuroticism inverted intentionally to maintain consistency.*

### Evaluator GPT Workflow

1.  **Initialization**: Evaluator GPT requests the user to paste the
    full evaluation matrix.

2.  **Step-by-step Evaluation**: The evaluator assesses each
    conversation row individually.

3.  **Transparency and Traceability**: Each evaluation explicitly
    restates the exact dialogue pair (user message and assistant
    response) being evaluated.

4.  **Unbiased Assessment**: Previous user assessments provided in the
    evaluation matrix are disregarded.

5.  **Incremental Confirmation**: After each row evaluation, the
    evaluator instructs the user to confirm completion before
    proceeding.

### Structured Output Format

Evaluator GPT outputs evaluations in a structured format:

- Clearly delineated by assistant type (Regulated or Baseline).

- Contains explicit restatements of evaluated dialogues.

- Provides concise, unbiased justification for each evaluation
  criterion.

- Ensures clarity and easy transferability into the Excel evaluation
  matrix.

Example Format for Regulated Assistant:

\*\*Regulated Row X\*\*

\*\*User Message:\*\*

\"\[Exact user message\]\"

\*\*Assistant Response:\*\*

\"\[Exact assistant response\]\"

\*\*Evaluation:\*\*

\- Detection Accuracy: Yes/No/Not Sure -- \[justification\]

\- Regulation Effectiveness: Yes/No/Not Sure -- \[justification\]

\- Emotional Tone Appropriate: Yes/No/Not Sure -- \[justification\]

\- Relevance & Coherence: Yes/No/Not Sure -- \[justification\]

\- Personality Needs Addressed: Yes/No/Not Sure -- \[justification\]

Regulated Row X complete. Type \"Next\" to continue.

Example Format for Baseline Assistant:

\*\*Baseline Row X\*\*

\*\*User Message:\*\*

\"\[Exact user message\]\"

\*\*Assistant Response:\*\*

\"\[Exact assistant response\]\"

\*\*Evaluation:\*\*

\- Emotional Tone Appropriate: Yes/No/Not Sure -- \[justification\]

\- Relevance & Coherence: Yes/No/Not Sure -- \[justification\]

\- Personality Needs Addressed: Yes/No/Not Sure -- \[justification\]

Baseline Row X complete. Type \"Next\" to continue.

### Error Prevention Measures

- **Dialogue Restatement**: Each evaluation step explicitly restates
  dialogues to prevent hallucinations or misinterpretations.

- **Controlled Progression**: Evaluation progresses row-by-row with user
  confirmation, avoiding overextension beyond provided data.

- **Neutrality Enforcement**: Ignores pre-existing evaluation marks to
  eliminate bias.

### Rationale for Design Choices

- Ensures **methodological rigor**, **transparency**, **auditability**,
  and alignment with thesis objectives.

- Provides **systematic comparative analysis** crucial for validating
  regulated vs. baseline assistant performance.

- Facilitates ease of **documentation and integration** into thesis
  methodology.
