## 1. Chapter Purpose & Scope

This chapter formalizes the system from *N8N Architecture v1* into
buildable specifications: pipeline behavior, N8N workflow design,
prompts, algorithms, state/data schemas, APIs, and validation targets.
The system operates as **dialog-only, prompt-only** with **OCEAN
vector** as the sole persistent memory state.

The specifications provide implementation-ready details for developers
to build the personality-adaptive conversational AI system, ensuring
deterministic behavior, comprehensive audit trails, and healthcare
compliance requirements are met through precise technical definitions.

## 2. Operating Assumptions

The system operates without external knowledge bases or tools; all
responses must be **conversation-grounded** using a \"quote-and-bound\"
approach that prevents hallucination by ensuring every assertion is
entailed by recent dialog turns. Sessions are stateless at the API layer
with state fetched and saved per turn to enable horizontal scaling.

Performance targets inherit from Architecture v1: P95 latencies of 2.5
seconds for standard responses and 5.0 seconds with refinement passes.
The system prioritizes stability and predictability over rapid
personality adaptation, maintaining therapeutic consistency essential
for healthcare applications.

## 3. End-to-End Pipeline (per turn)

Each conversation turn executes a single deterministic loop: **ingest →
detect → smooth → regulate → generate → verify → checkpoint**. The
ingest step normalizes user input and updates the rolling conversation
window. Detection performs LLM-based OCEAN personality inference.
Smoothing stabilizes personality estimates using exponential moving
averages. Regulation maps personality traits to communication policies.
Generation crafts dialog-grounded replies following policy directives.
Verification checks policy adherence and grounding, triggering
refinement if needed. Checkpointing persists the authoritative state for
session continuity.

Success paths deliver responses directly after verification passes,
while failure paths trigger a single refinement attempt before accepting
the result and continuing to checkpoint for system resilience.

## 4. N8N Workflow Specification

### 4.1 Workflow Nodes --- responsibilities & contracts

**Webhook Trigger Node** - *Type:* N8N Webhook Trigger - *Purpose:*
Receive user input and initiate workflow execution - *Inputs:* HTTP POST
with \`{session_id: \"uuid\", message: \"user input text\"}\` -
*Outputs:* \`session_id\`, \`raw_message\`, workflow execution context -
*Configuration:* POST endpoint \`/chat/webhook\`, JSON body parsing

**Ingest Function Node** - *Type:* N8N Function Node - *Purpose:*
Normalize user input and update rolling history window - *Inputs:*
\`raw_message\`, database query results from previous turns - *Outputs:*
\`clean_msg\` (normalized message), trimmed \`history\` (N turns +
salient quotes) - *Logic:* JavaScript function for text sanitization,
history window management, salient quote extraction

**Detect HTTP Node** - *Type:* N8N HTTP Request Node - *Purpose:*
Per-turn OCEAN inference from dialog context only via LLM API -
*Inputs:* \`clean_msg\`, compact \`history\` - *Outputs:* \`raw_ocean\`
(ṗ_t), \`trait_conf\` (confidence scores), \`evidence_quotes\` -
*Configuration:* POST to LLM endpoint (OpenAI/Anthropic), structured
JSON prompt with exact schema requirements (see §6)

**Smooth Function Node** - *Type:* N8N Function Node - *Purpose:*
Stabilize personality estimates and compute stability flag - *Inputs:*
\`raw_ocean\`, \`ocean_prev\`, \`trait_conf\` - *Outputs:* \`ocean\`
(p̂\_t), \`stable\` (boolean flag) - *Logic:* JavaScript implementation
of EMA updates with confidence weighting, delta caps, stability
threshold checking

**Regulate Function Node** - *Type:* N8N Function Node - *Purpose:* Map
OCEAN traits to style controls and generate policy plan (≤4
directives) - *Inputs:* \`ocean\`, \`stable\` - *Outputs:*
\`policy_plan\` (list of behavioral directives) - *Logic:* JavaScript
implementation of linear transformation with conflict resolution for
competing personality indicators

**Generate HTTP Node** - *Type:* N8N HTTP Request Node - *Purpose:*
Craft personality-adapted reply guided by policy plan; strictly
dialog-bounded - *Inputs:* \`policy_plan\`, \`history\` - *Outputs:*
\`draft_reply\` - *Configuration:* POST to LLM endpoint with
quote-and-bound generation prompt, policy adherence and conversation
grounding constraints

**Verify Function Node** - *Type:* N8N Function Node - *Purpose:*
Enforce policy adherence and dialog grounding requirements - *Inputs:*
\`draft_reply\`, \`policy_plan\`, \`history\` - *Outputs:* \`decision ∈
{accept, refine}\`, \`reasons\` (failure explanations) - *Logic:*
JavaScript implementation of policy compliance checking, novel claim
detection, grounding verification

**Refine HTTP Node** *(conditional)* - *Type:* N8N HTTP Request Node -
*Purpose:* Fix tone or remove novel claims; no new content
introduction - *Inputs:* \`draft_reply\`, \`reasons\`, \`policy_plan\`,
\`history\` - *Outputs:* \`final_reply\` - *Configuration:* POST to LLM
endpoint with refinement prompt for targeted corrections based on
verification failures, tone adjustment only

**Deliver Function Node** - *Type:* N8N Function Node - *Purpose:*
Return final reply with minimal metadata for API response - *Inputs:*
\`final_reply\` or \`draft_reply\`, \`policy_plan\`, \`ocean\` -
*Outputs:* API payload with response and system state preview - *Logic:*
JavaScript function to format final HTTP response

**Database Query Node** *(initial)* - *Type:* N8N Postgres Node -
*Purpose:* Retrieve existing conversation history and personality
state - *Inputs:* \`session_id\` from webhook trigger - *Outputs:*
Previous \`history\`, \`ocean_prev\`, session metadata -
*Configuration:* SELECT query from state_snapshots and turns tables

**Database Write Node** *(final)* - *Type:* N8N Postgres Node -
*Purpose:* Persist authoritative state JSON to database for session
continuity - *Inputs:* Updated \`history\`, \`ocean\`, \`policy_plan\`,
flags, timings - *Outputs:* Database snapshot row with immutable
execution ID - *Configuration:* INSERT operations to state_snapshots and
turns tables

### 4.2 Workflow Connections & routing

**Sequential workflow connections:** 1. \`Webhook Trigger → Database
Query Node\` (retrieve session history) 2. \`Database Query → Ingest
Function → Detect HTTP → Smooth Function → Regulate Function → Generate
HTTP → Verify Function\` form the main processing pipeline with
deterministic sequential execution.

**Conditional routing:** - \`Verify Function → IF Node\` evaluates
decision field - IF \`decision == \"refine\"\` → \`Refine HTTP Node →
Deliver Function\` - IF \`decision == \"accept\"\` → \`Deliver
Function\` - \`Deliver Function → Database Write Node\` for final state
persistence

**Error handling connections:** - HTTP Request nodes connect to \`Error
Handling Function\` on failure - Error handler routes to neutral
response delivery while preserving conversation state - All execution
paths lead to Database Write for audit trail maintenance

The workflow maintains deterministic and replayable execution with
explicit failure handling through N8N\'s built-in error routing and
retry mechanisms.

## 5. Core Algorithms

### 5.1 Detection → Smoothing (personality state)

The personality detection and smoothing algorithm operates through two
sequential steps combining LLM inference with temporal stabilization:

\$\$ \\tilde{\\mathbf p}\_t = F(m_t\^{u},\\,\\mathcal
H\_{1:t-1})\\quad\\text{(LLM prompt, continuous or signed)} \$\$

\$\$ \\hat{\\mathbf p}\_t=(1-\\alpha_t)\\hat{\\mathbf
p}*{t-1}+\\alpha_t\\tilde{\\mathbf p}\_t,\\;\\;
\\alpha_t=\\mathrm{calib}(\\mathrm{conf}\_t)\\in\[0,1\] \$\$*

Raw personality estimates \$\\tilde{\\mathbf p}\_t\$ are produced by
structured LLM prompts analyzing conversation context. The exponential
moving average uses confidence-weighted learning rates \$\\alpha_t\$
calibrated from detection confidence scores. Values are clipped to
\$\\hat{\\mathbf p}\_t\\in\[-1,1\]\^5\$ with per-trait delta caps
preventing behavioral whiplash. The system sets \`stable=true\` when ≥3
traits satisfy \$\|\\hat p_t\|\\ge\\tau\$ (threshold typically 0.3).

### 5.2 Regulation (policy mapping)

Personality traits are mapped to behavioral directives through linear
transformation with conflict resolution:

\$\$ \\mathbf s=\\mathrm{clip}(W\\hat{\\mathbf p}\_t+b)\\ \\Rightarrow\\
\\text{directives over: warmth, directness/hedging, assertiveness,
pacing/verbosity, Q:S ratio} \$\$

The weight matrix \$W\$ and bias vector \$b\$ encode Zurich Model
motivational mappings from OCEAN traits to communication style controls.
Conflict resolution handles competing indicators (e.g., high Openness +
low Extraversion yields exploratory questions with gentle pacing rather
than rapid exchanges). Output consists of ≤4 plain-English directives
targeting specific behavioral dimensions.

### 5.3 Verify (policy & grounding gate)

Verification operates as a pass/fail gate with explicit reasoning for
failed cases. The system detects out-of-dialog claims by checking
whether each assertion is entailed by recent conversation turns. Policy
adherence is verified by comparing generated responses against
behavioral directives from the regulation stage.

The system allows at most one **Refine** pass per turn to maintain
latency targets. If refinement fails or is not attempted, the system
accepts the draft response to ensure conversation continuity. All
verification decisions are logged with specific failure reasons for
debugging and system improvement.

## 6. Prompt Interfaces (skeletons)

### Detection Prompt (returns JSON)

Structured output requiring exact JSON keys with no prose commentary:

{\"ocean\":{\"O\":0.2,\"C\":-0.1,\"E\":0.0,\"A\":0.6,\"N\":-0.4},

\"trait_conf\":{\"O\":0.7,\"C\":0.6,\"E\":0.55,\"A\":0.75,\"N\":0.7},

\"evidence_quotes\":\[\"User said \'I prefer trying new
approaches\'\",\"Shows structured thinking patterns\"\]}

The prompt analyzes conversation context to infer OCEAN traits with
confidence scores and supporting evidence quotes from the dialog.

### Regulation Prompt (policy plan)

Input consists of smoothed OCEAN vector plus brief conversation history.
Output generates ≤4 behavioral directives targeting specific style
dimensions:

Example output: \`\[\"validate user concerns briefly\",\"ask one
open-ended question\",\"use concise sentences\",\"avoid imperative
language\"\]\`

### Generation Prompt (quote-and-bound)

Instructions emphasize using only dialog content while adhering to
policy directives. Response length and question limits are enforced
through prompt constraints. All assertions must be grounded in
conversation history.

### Verify / Refine Prompts

Verifier returns structured assessment: \`{pass: bool, reasons:
\[\"novel claim detected\", \"policy directive violated\"\]}\`. Refine
prompt modifies tone and removes novel claims while preserving core
response content and dialog grounding.

## 7. Authoritative State & Data Schemas

### 7.1 State JSON (single source of truth)

The system persists this complete state object after every turn,
providing the single authoritative source for session state and enabling
deterministic replay:

{

\"session_id\":\"uuid\",

\"turn_index\":17,

\"history\":\[{\"role\":\"user\",\"text\":\"How are you feeling
today?\"},{\"role\":\"assistant\",\"text\":\"I\'m doing well, thank you
for asking. How has your day been going?\"}\],

\"ocean\":{\"O\":0.4,\"C\":-0.1,\"E\":0.0,\"A\":0.5,\"N\":-0.3},

\"trait_conf\":{\"O\":0.72,\"C\":0.61,\"E\":0.58,\"A\":0.74,\"N\":0.69},

\"stable\":true,

\"policy_plan\":\[\"validate briefly\",\"ask one open
question\",\"concise sentences\",\"avoid imperatives\"\],

\"flags\":{\"refined_once\":false,\"neutral_fallback\":false},

\"timings_ms\":{\"detect\":380,\"generate\":920,\"verify\":210,\"total\":1510},

\"last_updated\":\"2024-09-02T14:33:00Z\"

}

This unified object simplifies replay scenarios, system analysis, and
compliance auditing by maintaining complete conversation state with
personality estimates, behavioral policies, and execution metadata in a
single retrievable record.

### 7.2 Database schema (research-minimal)

PostgreSQL schema optimized for personality-adaptive conversation
management:

\-- Core session management

CREATE TABLE sessions (

session_id UUID PRIMARY KEY,

created_at TIMESTAMP DEFAULT NOW(),

last_updated TIMESTAMP DEFAULT NOW()

);

\-- Individual conversation turns

CREATE TABLE turns (

id SERIAL PRIMARY KEY,

session_id UUID REFERENCES sessions(session_id),

turn_index INTEGER NOT NULL,

role VARCHAR(10) NOT NULL, \-- \'user\' or \'assistant\'

text TEXT NOT NULL,

created_at TIMESTAMP DEFAULT NOW()

);

\-- Authoritative state snapshots

CREATE TABLE state_snapshots (

id SERIAL PRIMARY KEY,

session_id UUID REFERENCES sessions(session_id),

turn_index INTEGER NOT NULL,

state_json JSONB NOT NULL,

created_at TIMESTAMP DEFAULT NOW()

);

\-- Performance indexes

CREATE INDEX idx_snapshots_session_turn ON state_snapshots(session_id,
turn_index);

CREATE INDEX idx_turns_session_created ON turns(session_id, created_at);

CREATE INDEX idx_sessions_updated ON sessions(last_updated);

The JSONB storage enables efficient querying of personality states and
policy configurations while maintaining schema flexibility for research
iterations.

## 8. API Specification (N8N Webhooks)

### Core Endpoints

**POST /webhook/chat** *(N8N Webhook Trigger)* - Request: \`{session_id:
\"uuid\", message: \"user input text\"}\` - Response: \`{reply:
\"assistant response\", policy_plan: \[\"directive1\", \"directive2\"\],
ocean_preview: {\"O\":0.4,\"C\":-0.1,\"E\":0.0,\"A\":0.5,\"N\":-0.3},
timings_ms: {\"detect\":380,\"generate\":920,\"verify\":210},
execution_id: \"n8n_execution_uuid\"}\` - Implementation: N8N webhook
trigger node initiating the personality detection workflow

**GET /api/session/{id}/state** *(FastAPI/Next.js API Route)* -
Response: Complete state JSON object from latest turn - Implementation:
Direct database query outside N8N workflow

**GET /api/session/{id}/summary** *(FastAPI/Next.js API Route)* -
Response: \`{summary_bullets: \[\"Key conversation points\"\], ocean:
{\...}, last_directives: \[\...\], turn_count: 17}\` - Implementation:
Database aggregation query with personality state summary

**POST /webhook/session/reset** *(N8N Webhook Trigger)* - Request:
\`{session_id: \"uuid\"}\` - Response: \`{status: \"success\", message:
\"Session reset to neutral state\"}\` - Effect: Triggers N8N workflow to
clear history and reset OCEAN to neutral \[0,0,0,0,0\]

### N8N Workflow Management

\- **Workflow Execution History**: Available through N8N UI for
debugging and audit trails - **Webhook URLs**: Generated by N8N for each
workflow trigger endpoint - **Error Handling**: N8N built-in error
catching with custom error response workflows - **Monitoring**: N8N
execution logs provide detailed workflow performance metrics

## 9. Performance & Reliability

The system inherits latency targets from Architecture v1: P95 2.5s
standard responses, 5.0s with refinement. Timeout configuration includes
30s total request timeout, 15s per LLM call, and single refinement
budget per turn.

Neutral fallback activates on system failures, returning
conversation-appropriate responses while preserving session state.
Circuit breakers protect against LLM provider failures with exponential
backoff retry patterns. Short context windows (salient quote extraction)
and prompt caching optimize performance while maintaining conversation
quality.

Bounded retry mechanisms prevent cascade failures while comprehensive
error logging enables rapid debugging and system improvement in
production healthcare environments.

## 10. Observability

### Execution Tracing

Per-node timing collection in \`timings_ms\` object captures detect,
smooth, regulate, generate, verify, and refine execution durations.
Prompt and model version tags enable A/B testing and regression analysis
across system updates.

### Decision Logging

Verification decisions (accept/refine) are logged with specific failure
reasons enabling system optimization and compliance monitoring. Example
trace record:

{

\"trace_id\": \"uuid\",

\"session_id\": \"uuid\",

\"turn_index\": 17,

\"node_timings\": {\"detect\": 380, \"generate\": 920, \"verify\": 210},

\"decisions\": {\"verify_result\": \"refine\", \"refine_reason\":
\"novel claim detected\"},

\"state_checkpoint_id\": \"checkpoint_uuid\",

\"model_versions\": {\"detect\": \"gpt-4-v1.2\", \"generate\":
\"gpt-4-v1.2\"}

}

This comprehensive logging supports debugging, performance optimization,
and regulatory compliance requirements for healthcare deployments.

## 11. Security & Privacy (framework-agnostic)

The dialog-only grounding approach ensures no external data dependencies
or privacy leakage through external API calls. PII redaction operates
through pre-processing hooks before state persistence. Role-based access
control (RBAC) restricts state access to authorized personnel with
configurable data retention policies supporting GDPR and HIPAA
compliance.

Audit logging captures all personality detection and regulation
decisions with immutable timestamps. Session state encryption protects
sensitive conversation data at rest while maintaining queryability for
compliance and debugging purposes.

## 12. Testing & Evaluation

### Automated Testing Framework

Scripted dialog replay enables deterministic testing with conversation
scenarios and expected personality adaptations. Regression testing
validates prompt version changes against established behavioral
baselines.

### Performance Metrics

\- **Stability Time**: Turns required to achieve stable personality
detection (target: ≤5 turns) - **Oscillation Rate**: Frequency of
personality estimate changes after stability (target: \<10%) - **Policy
Adherence Score**: Compliance with behavioral directives (target:
\>90%) - **Grounding Violations**: Novel claims not supported by dialog
(target: \<5%) - **P95 Latency**: Response time distribution (target:
2.5s/5.0s with refinement)

### Evaluation Harness

Minimal testing infrastructure provides conversation simulation,
personality ground truth comparison, and automated metric collection
enabling continuous system validation and improvement cycles.

## 13. Deployment Notes

### Container Architecture

Containerized services enable independent scaling with N8N workflow
engine connecting to shared PostgreSQL database. N8N containers handle
workflow execution while Next.js frontend containers serve client
interfaces and supplementary API routes.

### Deployment Strategies

Blue/green deployment patterns support prompt version updates with zero
downtime. Canary releases enable gradual rollout of model or prompt
changes with automatic rollback on performance degradation.

### Configuration Management

Environment variables control model identifiers, prompt version tags,
timeout values, and database connections. Configuration validation
ensures consistent deployment across development, staging, and
production environments.

\-\--

{ \"name\": \"Personality Adaptive Chat Workflow\", \"nodes\": \[ {
\"id\": \"webhook-trigger\", \"name\": \"Chat Webhook\", \"type\":
\"n8n-nodes-base.webhook\", \"position\": \[250, 300\], \"parameters\":
{ \"httpMethod\": \"POST\", \"path\": \"chat\", \"responseMode\":
\"responseNode\" } }, { \"id\": \"db-query-history\", \"name\": \"Get
Session History\", \"type\": \"n8n-nodes-base.postgres\", \"position\":
\[450, 300\], \"parameters\": { \"operation\": \"executeQuery\",
\"query\": \"SELECT state_json FROM state_snapshots WHERE session_id =
\$1 ORDER BY turn_index DESC LIMIT 1\" } }, { \"id\":
\"ingest-function\", \"name\": \"Ingest & Normalize\", \"type\":
\"n8n-nodes-base.function\", \"position\": \[650, 300\], \"parameters\":
{ \"functionCode\": \"// Normalize input and update conversation
history\" } }, { \"id\": \"detect-llm\", \"name\": \"Personality
Detection\", \"type\": \"n8n-nodes-base.httpRequest\", \"position\":
\[850, 300\], \"parameters\": { \"method\": \"POST\", \"url\":
\"https://api.openai.com/v1/chat/completions\", \"authentication\":
\"predefinedCredentialType\", \"nodeCredentialType\": \"openAiApi\" } },
{ \"id\": \"smooth-function\", \"name\": \"Smooth Personality\",
\"type\": \"n8n-nodes-base.function\", \"position\": \[1050, 300\],
\"parameters\": { \"functionCode\": \"// EMA smoothing with confidence
weighting\" } } \], \"connections\": { \"webhook-trigger\": {\"main\":
\[\[\"db-query-history\"\]\]}, \"db-query-history\": {\"main\":
\[\[\"ingest-function\"\]\]}, \"ingest-function\": {\"main\":
\[\[\"detect-llm\"\]\]}, \"detect-llm\": {\"main\":
\[\[\"smooth-function\"\]\]} } }

\*\*N8N Workflow Features:\*\*

\- \*\*Webhook-triggered execution\*\* for real-time chat processing

\- \*\*Database integration\*\* for session persistence and history
retrieval

\- \*\*HTTP nodes\*\* for LLM API calls (detection, generation,
refinement)

\- \*\*Function nodes\*\* for personality smoothing, policy regulation,
and verification

\- \*\*Conditional routing\*\* through IF nodes for refinement decisions

\- \*\*Error handling\*\* through N8N\'s built-in error routing
capabilities

\- \*\*Execution logging\*\* through N8N\'s native workflow monitoring

\*\*Implementation Notes:\*\*

\- Complete workflow includes additional nodes for regulate, generate,
verify, refine, deliver, and database write operations

\- Function node JavaScript code implements the core algorithms from
Section 5

\- HTTP Request nodes handle all LLM interactions with proper
authentication

\- Postgres nodes manage session state persistence and retrieval

\- Conditional IF nodes route workflow execution based on verification
results

Analyze this conversation to infer personality traits. Return JSON only:
{\"ocean\": {\"O\": float, \"C\": float, \"E\": float, \"A\": float,
\"N\": float}, \"trait_conf\": {\"O\": float, \"C\": float, \"E\":
float, \"A\": float, \"N\": float}, \"evidence_quotes\": \[string,
string, \...\]} Values in \[-1,1\], confidence in \[0,1\]. No prose
commentary.

\### Regulation Prompt

Given OCEAN traits and conversation context, generate ≤4 behavioral
directives. Input: {\"ocean\": {\...}, \"stable\": bool, \"history\":
\[\...\]} Output: \[\"directive focusing on warmth/tone\", \"directive
on directness\", \...\] Target dimensions: warmth, directness/hedging,
assertiveness, pacing, question ratio.

\### Generation Prompt

Generate response following directives. CRITICAL: Only use conversation
content. Policy directives: \[\...\] Conversation: \[\...\]
Requirements: Quote/paraphrase dialog only, follow directives, cap
questions at 1-2.

\### Verify Prompt

Check response for: (1) Policy directive compliance (2) Dialog grounding
Response: \"\...\" Policy: \[\...\] History: \[\...\] Return: {\"pass\":
bool, \"reasons\": \[string, \...\]} Flag novel claims not supported by
conversation.

## Appendix A --- N8N Workflow Configuration (JSON Schema)

## Appendix B --- Prompt Skeletons

### Detection Prompt
