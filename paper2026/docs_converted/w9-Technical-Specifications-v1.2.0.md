## Personality-Adaptive Conversational AI System

### Executive Summary

This document formalizes a **dialog-only, prompt-only**
personality-adaptive conversational AI system that uses OCEAN
personality traits as the sole persistent memory state. The system
operates through a deterministic pipeline: **ingest → detect → regulate
→ generate → format**, ensuring therapeutic consistency and healthcare
compliance.

**Core Innovation**: Real-time personality inference from conversation
turns, mapped to behavioral directives via the Zurich Model, producing
grounded responses without external knowledge dependencies.

**Expected Contribution**: 1. Transparent pipeline from OCEAN cues →
directives → grounded responses 2. Lightweight rules that reduce
hallucination through dialog-only grounding 3. Evaluation harness
measuring stability, directive adherence, and grounding

\-\--

## 1. System Architecture

### 1.1 Core Pipeline (MVP)

User Message → Ingest → Detect OCEAN → Parse → Regulate → Generate →
Format Output

**Pipeline Stages**: - **Ingest**: Normalize user input into
conversation context - **Detect**: LLM-based discrete OCEAN inference
(-1, 0, 1 values) - **Parse**: Extract and validate personality vector
with fallback thresholds - **Regulate**: Map traits to ≤5 behavioral
directives (Zurich Model) - **Generate**: Create grounded reply (70-150
words, ≤2 questions) - **Format**: Return compact JSON payload

### 1.2 Operating Principles

\- **Dialog-Only Grounding**: All responses must be entailed by
conversation history - **Stateless Sessions**: State fetched/saved per
turn for horizontal scaling - **Deterministic Behavior**: Reproducible
outputs for controlled evaluation - **Healthcare Compliance**: Audit
trails, PII protection, regulatory adherence

\-\--

## 2. N8N Workflow Implementation

### 2.1 MVP Workflow (Implemented)

**Source**: \`MVP/workflows/Discrete_workflow.json\`

  --------------------------------------------------------------------------------
  Manual Trigger    N8N Manual        Start workflow    Triggers execution
                    Trigger           manually          
  ----------------- ----------------- ----------------- --------------------------
  Edit Fields       N8N Set           Provide test      Raw JSON payload
                                      input             
                                      \`{session_id,    
                                      message}\`        

  Ingest            N8N Function      Normalize         \`conversation_context\`
                                      message, build    
                                      context           

  Detect OCEAN      N8N Code (LLM)    Infer discrete    \`ocean_disc\` JSON
                                      OCEAN traits      

  Parse Detection   N8N Code          Validate JSON,    Clean \`ocean_disc\`
                                      apply thresholds  

  Regulate          N8N Function      Map traits to     \`directives\` array
                                      directives        

  Generate Response N8N Code (LLM)    Create grounded   Full response
                                      reply             

  Format Output     N8N Function      Compact API       Final JSON
                                      payload           

                                                        
  --------------------------------------------------------------------------------

**Configuration**: - LLM calls: 20s timeout, temperature 0.1 (detect) /
0.7 (generate) - No database persistence, smoothing, or verification in
MVP - Manual execution mode for controlled testing

### 2.2 Full Workflow (Planned)

**Enhanced Pipeline**: \`Webhook → Database Query → Ingest → Detect →
Smooth → Regulate → Generate → Verify → Refine → Deliver → Database
Write\`

**Key Additions**: - **Smoothing**: EMA with confidence weighting for
trait stability - **Verification**: Policy adherence and grounding
validation - **Refinement**: Single-pass correction for failed
verifications - **Persistence**: PostgreSQL state snapshots and
conversation history

\-\--

## 3. Core Algorithms

### 3.1 OCEAN Detection (Discrete)

**Algorithm**: Per-turn personality inference with robust fallback

function detectOCEAN(clean_msg, threshold = 0.2) {

if (clean_msg.isEmpty()) return neutralOCEAN();

const prompt = buildJSONOnlyPrompt();

const response = callLLM(prompt, temperature: 0.1, timeout: 20s);

try {

const parsed = JSON.parse(response);

if (parsed.ocean_disc && isValidDiscrete(parsed.ocean_disc)) {

return parsed.ocean_disc;

}

if (parsed.ocean) {

return thresholdContinuous(parsed.ocean, threshold);

}

} catch (error) {

return extractJSONSpan(response) \|\| neutralOCEAN();

}

return neutralOCEAN();

}

**Fallback Strategy**: - Extract first JSON object from malformed
responses - Threshold continuous scores: \`disc(v) = v ≥ τ ? 1 : v ≤ -τ
? -1 : 0\` - Default to neutral \`{O:0, C:0, E:0, A:0, N:0}\` on any
failure

### 3.2 Regulation Mapping (Zurich Model)

**Algorithm**: Trait-to-directive translation with conflict resolution

function regulateDirectives(ocean_disc) {

const directives = \[\];

// Extraversion → Energy level

if (ocean_disc.E === 1) directives.push(\"use energetic, engaging
tone\");

else if (ocean_disc.E === -1) directives.push(\"adopt calm, reflective
tone\");

// Agreeableness → Warmth

if (ocean_disc.A === 1) directives.push(\"acknowledge and affirm
briefly\");

else if (ocean_disc.A === -1) directives.push(\"state points succinctly,
neutral tone\");

// Conscientiousness → Structure

if (ocean_disc.C === 1) directives.push(\"provide 2-3 concise,
structured steps\");

else if (ocean_disc.C === -1) directives.push(\"offer flexible guidance,
optional paths\");

// Openness → Novelty

if (ocean_disc.O === 1) directives.push(\"suggest one small, low-risk
exploration\");

else if (ocean_disc.O === -1) directives.push(\"use familiar examples;
reduce novelty\");

// Neuroticism → Reassurance

if (ocean_disc.N === 1) directives.push(\"normalize concerns in one
line\");

else if (ocean_disc.N === -1) directives.push(\"avoid
over-reassurance\");

return directives.slice(0, 5); // Cap at 5 directives

}

### 3.3 Grounded Generation

**Algorithm**: Dialog-bounded response synthesis

function generateResponse(directives, turn_text) {

const systemPrompt = \`Follow these behavior directives strictly:
\${directives.join(\', \')}.

Constraints: grounded in user text only; ≤2 questions; 70-150 words.\`;

const response = callLLM(systemPrompt, turn_text, temperature: 0.7,
timeout: 20s);

return {

reply: trim(response),

session_id: getSessionId(),

ocean_disc: getCurrentOCEAN(),

directives: directives

};

}

\-\--

## 4. Data Schemas

### 4.1 State JSON (Single Source of Truth)

{

\"session_id\": \"uuid\",

\"turn_index\": 17,

\"history\": \[

{\"role\": \"user\", \"text\": \"How are you feeling today?\"},

{\"role\": \"assistant\", \"text\": \"I\'m doing well, thank you for
asking.\"}

\],

\"ocean\": {\"O\": 0.4, \"C\": -0.1, \"E\": 0.0, \"A\": 0.5, \"N\":
-0.3},

\"trait_conf\": {\"O\": 0.72, \"C\": 0.61, \"E\": 0.58, \"A\": 0.74,
\"N\": 0.69},

\"stable\": true,

\"policy_plan\": \[\"validate briefly\", \"ask one open question\",
\"concise sentences\"\],

\"flags\": {\"refined_once\": false, \"neutral_fallback\": false},

\"timings_ms\": {\"detect\": 380, \"generate\": 920, \"verify\": 210,
\"total\": 1510},

\"last_updated\": \"2024-09-02T14:33:00Z\"

}

### 4.2 Database Schema (PostgreSQL)

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

role VARCHAR(10) NOT NULL,

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

\-\--

## 5. API Specification

### 5.1 Core Endpoints

**POST /webhook/chat** (N8N Webhook) - **Request**: \`{session_id:
\"uuid\", message: \"user input\"}\` - **Response**: \`{reply:
\"response\", policy_plan: \[\...\], ocean_preview: {\...}, timings_ms:
{\...}}\`

**GET /api/session/{id}/state** (FastAPI/Next.js) - **Response**:
Complete state JSON from latest turn

**GET /api/session/{id}/summary** (FastAPI/Next.js) - **Response**:
\`{summary_bullets: \[\...\], ocean: {\...}, last_directives: \[\...\],
turn_count: N}\`

**POST /webhook/session/reset** (N8N Webhook) - **Request**:
\`{session_id: \"uuid\"}\` - **Effect**: Reset session to neutral state

### 5.2 MVP Execution Mode

**Manual Trigger**: No webhook, input via \`Edit Fields\` node **Output
Format**:

{

\"session_id\": \"uuid\",

\"reply\": \"assistant response\",

\"turn_text\": \"original user message\",

\"ocean_disc\": {\"O\": 0, \"C\": 0, \"E\": 0, \"A\": 0, \"N\": 0}

}

\-\--

## 6. Performance & Reliability

### 6.1 Latency Targets

\- **P95 Standard Response**: ≤2.5 seconds - **P95 With Refinement**:
≤5.0 seconds - **LLM Call Timeout**: 20 seconds (MVP) / 15 seconds
(full) - **Total Request Timeout**: 30 seconds

### 6.2 Error Handling

**Fallback Strategy**: - Detection errors → neutral OCEAN vector -
Generation errors → supportive stock response - System failures →
conversation-appropriate fallback with preserved state

**Circuit Breakers**: Exponential backoff for LLM provider failures
**Retry Logic**: Bounded retry mechanisms prevent cascade failures

\-\--

## 7. Evaluation Framework

### 7.1 Performance Metrics

  -----------------------------------------------------------------------
  \*\*Stability Time\*\*  ≤5 turns                Achieve stable
                                                  personality detection
  ----------------------- ----------------------- -----------------------
  \*\*Oscillation         \<10%                   Avoid jarring tone
  Rate\*\*                                        shifts

  \*\*Policy              \>90%                   Directives reliably
  Adherence\*\*                                   shape replies

  \*\*Grounding           \<5%                    Maintain dialog-bounded
  Violations\*\*                                  content

  \*\*P95 Latency\*\*     ≤2.5s                   Keep interaction
                                                  responsive

                                                  
  -----------------------------------------------------------------------

### 7.2 Testing Infrastructure

**Automated Testing**: - Scripted dialog replay for deterministic
testing - Regression testing for prompt version changes - Personality
ground truth comparison - Automated metric collection

**Evaluation Harness**: - Conversation simulation - Behavioral baseline
validation - Continuous system improvement cycles

\-\--

## 8. Security & Compliance

### 8.1 Privacy Protection

\- **Dialog-Only Grounding**: No external data dependencies - **PII
Redaction**: Pre-processing hooks before persistence - **Session
Encryption**: Data protection at rest - **Access Control**: RBAC with
configurable retention policies

### 8.2 Healthcare Compliance

\- **Audit Logging**: Immutable timestamps for all decisions -
**GDPR/HIPAA Support**: Configurable data retention - **Regulatory
Adherence**: Comprehensive decision trails - **State Encryption**:
Queryable yet protected conversation data

\-\--

## 9. Deployment Architecture

### 9.1 Container Strategy

\- **N8N Workflow Engine**: Independent scaling for workflow execution -
**PostgreSQL Database**: Shared state persistence - **Next.js
Frontend**: Client interfaces and supplementary APIs - **Container
Orchestration**: Independent service scaling

### 9.2 Deployment Patterns

\- **Blue/Green Deployment**: Zero-downtime prompt updates - **Canary
Releases**: Gradual model rollout with auto-rollback - **Configuration
Management**: Environment-based model/prompt control - **Validation**:
Consistent deployment across environments

\-\--

## 10. Implementation Roadmap

### 10.1 MVP (Current)

\- ✅ Discrete OCEAN detection - ✅ Basic regulation mapping - ✅
Grounded generation - ✅ Manual workflow execution

### 10.2 Phase 1 (Next)

\- 🔄 EMA smoothing implementation - 🔄 Verification/refinement
pipeline - 🔄 Database persistence - 🔄 Webhook API endpoints

### 10.3 Phase 2 (Future)

\- ⏳ Advanced observability - ⏳ A/B testing framework - ⏳ Performance
optimization - ⏳ Production deployment

\-\--

Analyze this conversation turn to infer personality traits. Return JSON
only:

{\"ocean_disc\": {\"O\": -1\|0\|1, \"C\": -1\|0\|1, \"E\": -1\|0\|1,
\"A\": -1\|0\|1, \"N\": -1\|0\|1}}

No prose commentary. Values: -1 (low), 0 (neutral), 1 (high).

### Regulation Prompt

Given OCEAN traits, generate ≤4 behavioral directives.

Input: {\"ocean_disc\": {\...}}

Output: \[\"directive1\", \"directive2\", \...\]

Target: warmth, directness, assertiveness, pacing, question ratio.

### Generation Prompt

Generate response following directives. CRITICAL: Only use conversation
content.

Policy directives: \[\...\]

User text: \"\...\"

Requirements: Quote/paraphrase dialog only, follow directives, 70-150
words, ≤2 questions.

### Verification Prompt

Check response for: (1) Policy compliance (2) Dialog grounding

Response: \"\...\"

Policy: \[\...\]

History: \[\...\]

Return: {\"pass\": bool, \"reasons\": \[\...\]}

\-\--

*This specification provides implementation-ready details for building a
personality-adaptive conversational AI system with deterministic
behavior, comprehensive audit trails, and healthcare compliance
requirements.*

## Appendix A: Prompt Templates

### Detection Prompt (Discrete)
