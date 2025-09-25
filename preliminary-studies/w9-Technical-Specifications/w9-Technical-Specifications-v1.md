# Executive Summary (MVP)

This proposal investigates a small, auditable conversational system that adapts tone and pacing using per‑turn OCEAN signals inferred from the user’s message. The system is strictly dialog‑grounded: responses must be entailed by the current turn. The MVP favors clarity, low latency, and reproducibility to enable controlled evaluation.

Expected contribution: (1) a transparent pipeline from OCEAN cues → directives → grounded responses; (2) prompts and lightweight rules that reduce hallucination; (3) an evaluation harness to measure stability, directive adherence, and grounding.

```
User message
  |
  v
Ingest
  |
  v
Detect OCEAN (discrete)
  |
  v
Parse JSON / threshold
  |
  v
Regulate -> directives
  |
  v
Generate grounded reply
  |
  v
Format output
```

Table 1. End‑to‑End Turn (MVP)

| Stage | Input | Output | Contract |
|---|---|---|---|
| Ingest | {session_id, message} | conversation_context | Normalize minimal turn context. |
| Detect | conversation_context | ocean_disc ∈ {−1,0,1}^5 | Return JSON only; per‑turn signals. |
| Parse | raw LLM JSON | clean ocean_disc | Strict schema; safe neutral fallback. |
| Regulate | ocean_disc | ≤5 directives | Map traits to tone, pacing, structure. |
| Generate | directives, turn_text | 70–150 word reply | Grounded; ≤2 questions; policy‑constrained. |
| Format | above | {session_id, reply, ocean_disc} | Compact, auditable payload. |

Table 2. OCEAN → Directive Mapping (illustrative)

| Trait (+1 / −1) | Tone/Pacing effect | Example directive |
|---|---|---|
| O +1 / −1 | Invite small exploration / Prefer familiar | "Suggest one new approach" / "Use familiar examples" |
| C +1 / −1 | Structure steps / Keep flexible | "Provide 2–3 concise steps" / "Offer optional paths" |
| E +1 / −1 | Energetic tone / Calm tone | "Use active verbs" / "Use reflective phrasing" |
| A +1 / −1 | Warm, collaborative / Neutral | "Acknowledge briefly" / "State points succinctly" |
| N +1 / −1 | Reassure more / Reassure less | "Normalize concerns in one line" / "Avoid over‑reassurance" |

Table 3. Evaluation Plan (targets for small study)

| Dimension | Metric | Target | Rationale |
|---|---|---|---|
| Stability | Oscillation after initial turns | <10% | Avoid jarring tone shifts. |
| Adherence | Policy adherence score | >90% | Directives reliably shape replies. |
| Grounding | Novel claim rate | <5% | Maintain dialog‑bounded content. |
| Latency | P95 per turn | ≤2.5s | Keep interaction responsive. |

---

# Technical Specifications

## 1. Chapter Purpose & Scope

This chapter formalizes the system from *N8N Architecture v1* into buildable specifications: pipeline behavior, N8N workflow design, prompts, algorithms, state/data schemas, APIs, and validation targets. The system operates as **dialog-only, prompt-only** with **OCEAN vector** as the sole persistent memory state.

The specifications provide implementation-ready details for developers to build the personality-adaptive conversational AI system, ensuring deterministic behavior, comprehensive audit trails, and healthcare compliance requirements are met through precise technical definitions.

### 1.1 Core Scope (MVP)

In scope (now):
- Single-turn pipeline: ingest → detect(discrete) → parse → regulate → generate → format-output
- Discrete OCEAN detection and Zurich Model directives
- Manual execution; no database or web API; 20s timeout per LLM call

Out of scope (deferred):
- History windowing, EMA smoothing, verification/refinement, checkpointing
- Database persistence and webhook endpoints
- Advanced observability (beyond basic node logs)

## 2. Operating Assumptions

The system operates without external knowledge bases or tools; all responses must be **conversation-grounded** using a "quote-and-bound" approach that prevents hallucination by ensuring every assertion is entailed by recent dialog turns. Sessions are stateless at the API layer with state fetched and saved per turn to enable horizontal scaling.

## 2.1 Current MVP (Discrete Workflow implemented)

The current implementation corresponds to a minimal, discrete variant focused on per-turn operation with no persistence or verification passes. It is materialized in `/MVP/workflows/Discrete_workflow.json` and includes:

- Manual trigger and input setup: `When clicking ‘Execute workflow’` → `Edit Fields`
- Per-turn ingest: `Ingest (Per-turn, no smoothing)` creates `conversation_context = "user: <msg>"`
- Discrete detection: `Detect OCEAN (Discrete, Gemini Pro)` requests an LLM to return `{"ocean_disc": {O|C|E|A|N: -1|0|1}}`
- Parsing: `Parse Detection JSON` extracts `ocean_disc` and falls back to thresholding continuous scores if needed
- Regulation: `Build Regulation Directives (Zurich Model)` maps discrete traits to ≤5 directives
- Generation: `Generate Response (Gemini Pro)` produces a 70–150 word reply, grounded in user text, with ≤2 questions
- Output formatting: `Format Output` returns `{session_id, reply, turn_text, ocean_disc}`

Notes:
- No database reads/writes, smoothing, verification, or refinement are executed in this MVP.
- Both LLM calls use a 20s timeout; temperature is 0.1 for detection and 0.7 for generation.

Performance targets inherit from Architecture v1: P95 latencies of 2.5 seconds for standard responses and 5.0 seconds with refinement passes. The system prioritizes stability and predictability over rapid personality adaptation, maintaining therapeutic consistency essential for healthcare applications.

## 3. End-to-End Pipeline (per turn)

There are two variants:

- Target full loop (future): **ingest → detect → smooth → regulate → generate → verify → checkpoint**
- Current MVP (implemented): **ingest → detect(discrete) → parse → regulate → generate → format-output**

In the MVP, the ingest step normalizes user input and creates a per-turn `conversation_context`. Detection performs LLM-based OCEAN personality inference in discrete form. The parse step extracts JSON and thresholds continuous outputs if necessary. Regulation maps discrete traits to communication directives. Generation crafts dialog-grounded replies following directives with length and question caps. The output step formats `{session_id, reply, turn_text, ocean_disc}`.

## 4. N8N Workflow Specification

### 4.0 MVP Workflow (Implemented)

Source: `preliminary-studies/w9-Technical-Specifications/MVP/workflows/Discrete_workflow.json`

| Step | Node Type | Purpose | Output |
| --- | --- | --- | --- |
| Manual Trigger | N8N Manual Trigger | Start workflow manually | Triggers downstream nodes |
| Edit Fields | N8N Set | Provide test input JSON `{session_id, message}` | Raw JSON payload |
| Ingest | N8N Function | Normalize message, build conversation context | `session_id`, `clean_msg`, `conversation_context` |
| Detect OCEAN | N8N Code (LLM call) | Infer discrete OCEAN traits (−1, 0, 1) | `ocean_disc` JSON |
| Parse Detection | N8N Code | Validate JSON, threshold if continuous scores appear | `ocean_disc`, `turn_text` |
| Regulate | N8N Function | Map traits to up to 5 directives (Zurich Model) | `directives` + metadata |
| Generate Response | N8N Code (LLM call) | Create reply (70–150 words, ≤2 questions) following directives | Full response payload |
| Format Output | N8N Function | Compact API payload | `{session_id, reply, turn_text, ocean_disc}` |

👉 Summary: The MVP is linear, single-turn only, with no memory or verification.

### 4.1 Full Workflow (Planned)

| Step | Node Type | Purpose | Output |
| --- | --- | --- | --- |
| Webhook Trigger | N8N Webhook | Receive user message via API | `session_id`, `raw_message` |
| Database Query | N8N Postgres | Retrieve past history + previous state | `history`, `ocean_prev` |
| Ingest | Function | Normalize input, update rolling history | `clean_msg`, `history` |
| Detect | HTTP Request | Infer OCEAN traits with LLM | `raw_ocean`, `trait_conf` |
| Smooth | Function | Stabilize traits with EMA smoothing | `ocean`, `stable` flag |
| Regulate | Function | Generate behavioral policy plan | `policy_plan` |
| Generate | HTTP Request | Draft reply (quote-and-bound prompt) | `draft_reply` |
| Verify | Function | Check policy adherence + grounding | Decision: accept/refine |
| Refine (if needed) | HTTP Request | Adjust tone/remove novel claims | `final_reply` |
| Deliver | Function | Format final API response | Reply + state preview |
| Database Write | Postgres | Save new state snapshot | Persistent record |

### 4.2 Workflow Connections & Routing (Full Workflow — Planned)

| Type | Connections / Logic | Purpose |
| --- | --- | --- |
| Sequential | `Webhook Trigger → Database Query → Ingest → Detect → Smooth → Regulate → Generate → Verify` | Forms the main processing pipeline with deterministic, step-by-step execution. |
| Conditional | `Verify → IF Node` → If refine: `Refine → Deliver`; If accept: `Deliver` | Ensures responses either go through refinement or are delivered directly. |
| Persistence | `Deliver → Database Write` | Saves final system state for auditability and replay. |
| Error Handling | Failed HTTP Requests → `Error Handling Function → Neutral Response → Database Write` | Provides safe fallback behavior while maintaining state and logs. |

👉 Summary: The workflow is deterministic and replayable, with explicit conditional branches and robust error handling to ensure predictability and audit trails.

## 5. Core Algorithms

### 5.1 Detection → Smoothing (personality state)

The personality detection and smoothing algorithm operates through two sequential steps combining LLM inference with temporal stabilization:

$$
\tilde{\mathbf p}_t = F(m_t^{u},\,\mathcal H_{1:t-1})\quad\text{(LLM prompt, continuous or signed)}
$$

$$
\hat{\mathbf p}_t=(1-\alpha_t)\hat{\mathbf p}_{t-1}+\alpha_t\tilde{\mathbf p}_t,\;\; \alpha_t=\mathrm{calib}(\mathrm{conf}_t)\in[0,1]
$$

Raw personality estimates $\tilde{\mathbf p}_t$ are produced by structured LLM prompts analyzing conversation context. The exponential moving average uses confidence-weighted learning rates $\alpha_t$ calibrated from detection confidence scores. Values are clipped to $\hat{\mathbf p}_t\in[-1,1]^5$ with per-trait delta caps preventing behavioral whiplash. The system sets `stable=true` when ≥3 traits satisfy $|\hat p_t|\ge\tau$ (threshold typically 0.3).

### 5.2 Regulation (policy mapping)

Personality traits are mapped to behavioral directives through linear transformation with conflict resolution:

$$
\mathbf s=\mathrm{clip}(W\hat{\mathbf p}_t+b)\ \Rightarrow\ \text{directives over: warmth, directness/hedging, assertiveness, pacing/verbosity, Q:S ratio}
$$

The weight matrix $W$ and bias vector $b$ encode Zurich Model motivational mappings from OCEAN traits to communication style controls. Conflict resolution handles competing indicators (e.g., high Openness + low Extraversion yields exploratory questions with gentle pacing rather than rapid exchanges). Output consists of ≤4 plain-English directives targeting specific behavioral dimensions.

### 5.3 Verify (policy & grounding gate)

Verification operates as a pass/fail gate with explicit reasoning for failed cases. The system detects out-of-dialog claims by checking whether each assertion is entailed by recent conversation turns. Policy adherence is verified by comparing generated responses against behavioral directives from the regulation stage.

The system allows at most one **Refine** pass per turn to maintain latency targets. If refinement fails or is not attempted, the system accepts the draft response to ensure conversation continuity. All verification decisions are logged with specific failure reasons for debugging and system improvement.

### 5.4 Detection (MVP discrete) — algorithm

Inputs: `clean_msg` (single turn text). Output: `ocean_disc` with values in {-1, 0, 1} for {O, C, E, A, N}.

- Build prompt with strict JSON-only instruction returning `{"ocean_disc":{...}}` for THIS TURN ONLY.
- Call LLM with temperature 0.1, max_tokens 200, 20s timeout.
- Parse response:
  - Attempt `JSON.parse(content)`; if fails, extract first `{...}` span and parse.
  - If only continuous `ocean` is present, convert to discrete using threshold τ = 0.2:
    - `disc(v) = 1 if v ≥ τ; -1 if v ≤ -τ; else 0` applied per trait.
  - Validate keys and values; on any invalid/missing field, set neutral `{O:0,C:0,E:0,A:0,N:0}`.
- Return `ocean_disc`.

Optional variance reduction (off by default to meet latency): self-consistency with k=3 samples and per-trait majority vote; ties resolve to 0.

### 5.5 Generation (MVP) — algorithm

Inputs: `directives` (≤5 strings), `turn_text` (user text). Output: `reply`.

- Construct system content: “Follow these behavior directives strictly: [directives]. Constraints: grounded in user text only; ≤2 questions; 70–150 words.”
- Provide `turn_text` as user content (fallback to a safe generic instruction if empty).
- Call LLM with temperature 0.7, max_tokens 220, 20s timeout.
- Post-processing: trim; no verification/refinement pass in MVP (constraints enforced via prompt only).
- Error fallback: short supportive message with breathing tip; include `session_id`, `ocean_disc`, and `directives` in the JSON payload for traceability.

## 6. Prompt Interfaces (skeletons — MVP emphasis)

### Detection Prompt (returns JSON)
Structured output requiring exact JSON keys with no prose commentary:

```json
{"ocean":{"O":0.2,"C":-0.1,"E":0.0,"A":0.6,"N":-0.4},
 "trait_conf":{"O":0.7,"C":0.6,"E":0.55,"A":0.75,"N":0.7},
 "evidence_quotes":["User said 'I prefer trying new approaches'","Shows structured thinking patterns"]}
```

The prompt analyzes conversation context to infer OCEAN traits with confidence scores and supporting evidence quotes from the dialog.

### Detection Prompt (MVP discrete)
Return JSON only with signed discrete traits for this turn only. No prose commentary:

```
{"ocean_disc":{"O":-1|0|1,"C":-1|0|1,"E":-1|0|1,"A":-1|0|1,"N":-1|0|1}}
```

### Regulation Prompt (policy plan — MVP uses ocean_disc only)
Input consists of discrete `ocean_disc` (MVP) or smoothed `ocean` (future) plus brief conversation history. Output generates ≤4 behavioral directives targeting specific style dimensions:

Example output: `["validate user concerns briefly","ask one open-ended question","use concise sentences","avoid imperative language"]`

### Generation Prompt (quote-and-bound)
Instructions emphasize using only dialog content while adhering to policy directives. Response length and question limits are enforced through prompt constraints. All assertions must be grounded in conversation history.

### Generation Prompt (MVP constraints)
Follow these behavior directives strictly; stay grounded in user text only; 70–150 words; ask at most 1–2 questions. Example system content construction:

```
"You are a supportive assistant. Follow these behavior directives strictly: [<directives JSON>]. Constraints: stay grounded in the user text only; 1-2 questions max; 70-150 words."
```

### Verify / Refine Prompts
Verifier returns structured assessment: `{pass: bool, reasons: ["novel claim detected", "policy directive violated"]}`. Refine prompt modifies tone and removes novel claims while preserving core response content and dialog grounding.

## 7. Authoritative State & Data Schemas

### 7.1 State JSON (single source of truth)

The system persists this complete state object after every turn, providing the single authoritative source for session state and enabling deterministic replay:

```json
{
  "session_id":"uuid",
  "turn_index":17,
  "history":[{"role":"user","text":"How are you feeling today?"},{"role":"assistant","text":"I'm doing well, thank you for asking. How has your day been going?"}],
  "ocean":{"O":0.4,"C":-0.1,"E":0.0,"A":0.5,"N":-0.3},
  "trait_conf":{"O":0.72,"C":0.61,"E":0.58,"A":0.74,"N":0.69},
  "stable":true,
  "policy_plan":["validate briefly","ask one open question","concise sentences","avoid imperatives"],
  "flags":{"refined_once":false,"neutral_fallback":false},
  "timings_ms":{"detect":380,"generate":920,"verify":210,"total":1510},
  "last_updated":"2024-09-02T14:33:00Z"
}
```

This unified object simplifies replay scenarios, system analysis, and compliance auditing by maintaining complete conversation state with personality estimates, behavioral policies, and execution metadata in a single retrievable record.

### 7.2 Database schema (research-minimal)

PostgreSQL schema optimized for personality-adaptive conversation management:

```sql
-- Core session management
CREATE TABLE sessions (
    session_id UUID PRIMARY KEY,
    created_at TIMESTAMP DEFAULT NOW(),
    last_updated TIMESTAMP DEFAULT NOW()
);

-- Individual conversation turns
CREATE TABLE turns (
    id SERIAL PRIMARY KEY,
    session_id UUID REFERENCES sessions(session_id),
    turn_index INTEGER NOT NULL,
    role VARCHAR(10) NOT NULL, -- 'user' or 'assistant'
    text TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT NOW()
);

-- Authoritative state snapshots
CREATE TABLE state_snapshots (
    id SERIAL PRIMARY KEY,
    session_id UUID REFERENCES sessions(session_id),
    turn_index INTEGER NOT NULL,
    state_json JSONB NOT NULL,
    created_at TIMESTAMP DEFAULT NOW()
);

-- Performance indexes
CREATE INDEX idx_snapshots_session_turn ON state_snapshots(session_id, turn_index);
CREATE INDEX idx_turns_session_created ON turns(session_id, created_at);
CREATE INDEX idx_sessions_updated ON sessions(last_updated);
```

The JSONB storage enables efficient querying of personality states and policy configurations while maintaining schema flexibility for research iterations.

## 8. API Specification (N8N Webhooks)

### Core Endpoints

**POST /webhook/chat** *(N8N Webhook Trigger)*
- Request: `{session_id: "uuid", message: "user input text"}`
- Response: `{reply: "assistant response", policy_plan: ["directive1", "directive2"], ocean_preview: {"O":0.4,"C":-0.1,"E":0.0,"A":0.5,"N":-0.3}, timings_ms: {"detect":380,"generate":920,"verify":210}, execution_id: "n8n_execution_uuid"}`
- Implementation: N8N webhook trigger node initiating the personality detection workflow

**GET /api/session/{id}/state** *(FastAPI/Next.js API Route)*
- Response: Complete state JSON object from latest turn
- Implementation: Direct database query outside N8N workflow

**GET /api/session/{id}/summary** *(FastAPI/Next.js API Route)*
- Response: `{summary_bullets: ["Key conversation points"], ocean: {...}, last_directives: [...], turn_count: 17}`
- Implementation: Database aggregation query with personality state summary

**POST /webhook/session/reset** *(N8N Webhook Trigger)*
- Request: `{session_id: "uuid"}`
- Response: `{status: "success", message: "Session reset to neutral state"}`
- Effect: Triggers N8N workflow to clear history and reset OCEAN to neutral [0,0,0,0,0]

### N8N Workflow Management
- **Workflow Execution History**: Available through N8N UI for debugging and audit trails
- **Webhook URLs**: Generated by N8N for each workflow trigger endpoint
- **Error Handling**: N8N built-in error catching with custom error response workflows
- **Monitoring**: N8N execution logs provide detailed workflow performance metrics

### 8.1 MVP Execution Mode & Response

- Execution Mode: Manual trigger (`When clicking ‘Execute workflow’`), no webhook used
- Input: Provided in `Edit Fields` node as raw JSON `{session_id, message}`
- Output payload (from `Format Output`):

```json
{
  "session_id": "uuid",
  "reply": "assistant response",
  "turn_text": "original user message",
  "ocean_disc": {"O": 0, "C": 0, "E": 0, "A": 0, "N": 0}
}
```

## 9. Performance & Reliability

The system inherits latency targets from Architecture v1: P95 2.5s standard responses, 5.0s with refinement. Timeout configuration includes 30s total request timeout, 15s per LLM call, and single refinement budget per turn.

MVP overrides (Discrete workflow):
- 20s timeout per LLM call (n8n code node HTTP helper)
- No smoothing, verification, or refinement in the execution path
 - Deterministic fallbacks: neutral `ocean_disc` on detect errors; supportive stock reply on generate errors

Neutral fallback activates on system failures, returning conversation-appropriate responses while preserving session state. Circuit breakers protect against LLM provider failures with exponential backoff retry patterns. Short context windows (salient quote extraction) and prompt caching optimize performance while maintaining conversation quality.

Bounded retry mechanisms prevent cascade failures while comprehensive error logging enables rapid debugging and system improvement in production healthcare environments.

## 10. Observability

### Execution Tracing
Per-node timing collection in `timings_ms` object captures detect, smooth, regulate, generate, verify, and refine execution durations. Prompt and model version tags enable A/B testing and regression analysis across system updates.

MVP note: Only detect and generate incur LLM timings; parse/regulate/format are measured via node execution logs.
Additional MVP guidance: Capture node-level logs for directives and final `ocean_disc` to support troubleshooting without database state.

### Decision Logging
Verification decisions (accept/refine) are logged with specific failure reasons enabling system optimization and compliance monitoring. Example trace record:

```json
{
  "trace_id": "uuid",
  "session_id": "uuid", 
  "turn_index": 17,
  "node_timings": {"detect": 380, "generate": 920, "verify": 210},
  "decisions": {"verify_result": "refine", "refine_reason": "novel claim detected"},
  "state_checkpoint_id": "checkpoint_uuid",
  "model_versions": {"detect": "gpt-4-v1.2", "generate": "gpt-4-v1.2"}
}
```

This comprehensive logging supports debugging, performance optimization, and regulatory compliance requirements for healthcare deployments.

## 11. Security & Privacy (framework-agnostic)

The dialog-only grounding approach ensures no external data dependencies or privacy leakage through external API calls. PII redaction operates through pre-processing hooks before state persistence. Role-based access control (RBAC) restricts state access to authorized personnel with configurable data retention policies supporting GDPR and HIPAA compliance.

Audit logging captures all personality detection and regulation decisions with immutable timestamps. Session state encryption protects sensitive conversation data at rest while maintaining queryability for compliance and debugging purposes.

## 12. Testing & Evaluation

### Automated Testing Framework
Scripted dialog replay enables deterministic testing with conversation scenarios and expected personality adaptations. Regression testing validates prompt version changes against established behavioral baselines.

### Performance Metrics
- **Stability Time**: Turns required to achieve stable personality detection (target: ≤5 turns)
- **Oscillation Rate**: Frequency of personality estimate changes after stability (target: <10%)
- **Policy Adherence Score**: Compliance with behavioral directives (target: >90%)
- **Grounding Violations**: Novel claims not supported by dialog (target: <5%)
- **P95 Latency**: Response time distribution (target: 2.5s/5.0s with refinement)

### Evaluation Harness
Minimal testing infrastructure provides conversation simulation, personality ground truth comparison, and automated metric collection enabling continuous system validation and improvement cycles.

## 13. Deployment Notes

### Container Architecture
Containerized services enable independent scaling with N8N workflow engine connecting to shared PostgreSQL database. N8N containers handle workflow execution while Next.js frontend containers serve client interfaces and supplementary API routes.

### Deployment Strategies
Blue/green deployment patterns support prompt version updates with zero downtime. Canary releases enable gradual rollout of model or prompt changes with automatic rollback on performance degradation.

### Configuration Management
Environment variables control model identifiers, prompt version tags, timeout values, and database connections. Configuration validation ensures consistent deployment across development, staging, and production environments.

---

## Appendix A — N8N Workflow Configuration (JSON Schema)

```json
{
  "name": "Personality Adaptive Chat Workflow",
  "nodes": [
    {
      "id": "webhook-trigger",
      "name": "Chat Webhook",
      "type": "n8n-nodes-base.webhook",
      "position": [250, 300],
      "parameters": {
        "httpMethod": "POST",
        "path": "chat",
        "responseMode": "responseNode"
      }
    },
    {
      "id": "db-query-history",
      "name": "Get Session History", 
      "type": "n8n-nodes-base.postgres",
      "position": [450, 300],
      "parameters": {
        "operation": "executeQuery",
        "query": "SELECT state_json FROM state_snapshots WHERE session_id = $1 ORDER BY turn_index DESC LIMIT 1"
      }
    },
    {
      "id": "ingest-function",
      "name": "Ingest & Normalize",
      "type": "n8n-nodes-base.function",
      "position": [650, 300],
      "parameters": {
        "functionCode": "// Normalize input and update conversation history"
      }
    },
    {
      "id": "detect-llm",
      "name": "Personality Detection",
      "type": "n8n-nodes-base.httpRequest",
      "position": [850, 300],
      "parameters": {
        "method": "POST",
        "url": "https://api.openai.com/v1/chat/completions",
        "authentication": "predefinedCredentialType",
        "nodeCredentialType": "openAiApi"
      }
    },
    {
      "id": "smooth-function",
      "name": "Smooth Personality",
      "type": "n8n-nodes-base.function", 
      "position": [1050, 300],
      "parameters": {
        "functionCode": "// EMA smoothing with confidence weighting"
      }
    }
  ],
  "connections": {
    "webhook-trigger": {"main": [["db-query-history"]]},
    "db-query-history": {"main": [["ingest-function"]]},
    "ingest-function": {"main": [["detect-llm"]]},
    "detect-llm": {"main": [["smooth-function"]]}
  }
}
```

**N8N Workflow Features:**
- **Webhook-triggered execution** for real-time chat processing
- **Database integration** for session persistence and history retrieval  
- **HTTP nodes** for LLM API calls (detection, generation, refinement)
- **Function nodes** for personality smoothing, policy regulation, and verification
- **Conditional routing** through IF nodes for refinement decisions
- **Error handling** through N8N's built-in error routing capabilities
- **Execution logging** through N8N's native workflow monitoring

**Implementation Notes:**
- Complete workflow includes additional nodes for regulate, generate, verify, refine, deliver, and database write operations
- Function node JavaScript code implements the core algorithms from Section 5
- HTTP Request nodes handle all LLM interactions with proper authentication
- Postgres nodes manage session state persistence and retrieval
- Conditional IF nodes route workflow execution based on verification results

## Appendix B — Algorithms

### B.1 Algorithm for generating an initial solution

**Algorithm 1: Generating an initial solution**

```
1: Input: task description Ttask, datasets D, score function ℎ, number of retrieved models 𝑀,
2: {T 𝑖 model, T 𝑖 code}𝑀 𝑖=1 = Aretriever (Ttask)
3: for 𝑖 = 1 to 𝑀 do
4:   𝑠𝑖 init = Ainit (Ttask, T 𝑖 model, T 𝑖 code)
5:   Evaluate ℎ(𝑠𝑖 init) using D
6: end for
7:  𝑠0 ← 𝑠𝜋(1) init
8:  ℎbest ← ℎ(𝑠0)
9:  for 𝑖 = 2 to 𝑀 do
10:   𝑠candidate ← Amerger (𝑠0, 𝑠𝜋(𝑖) init)
11:   Evaluate ℎ(𝑠candidate) using D
12:   if ℎ(𝑠candidate) ≥ ℎbest then
13:     𝑠0 ← 𝑠candidate
14:     ℎbest ← ℎ(𝑠0)
15:   else
16:     break
17:   end if
18: end for
19: Output: initial solution 𝑠0
```

### B.2 Detection (MVP discrete) — pseudocode

**Algorithm 2: OCEAN discrete detection (per turn)**

```
1: Inputs: clean turn text m, threshold τ = 0.2, model id, endpoint URL,
2:         temperature = 0.1, max_tokens = 200, timeout = 20s
3: if m is empty then
4:     return ocean_disc = {O:0, C:0, E:0, A:0, N:0}
5: end if
6: Build prompt requiring JSON-only: {"ocean_disc":{"O":-1|0|1,"C":-1|0|1,"E":-1|0|1,"A":-1|0|1,"N":-1|0|1}}
7: res ← LLMCall(model, endpoint, system_prompt, user = "Text: " + m,
8:               temperature, max_tokens, timeout)
9: content ← res.choices[0].message.content or ""
10: try
11:    parsed ← JSON.parse(content)
12: catch
13:    jspan ← first JSON object extracted from content using /\{[\s\S]*\}/
14:    parsed ← (jspan ? JSON.parse(jspan) : {})
15: end try
16: if parsed.ocean_disc exists and all values ∈ {-1,0,1} then
17:     return parsed.ocean_disc
18: else if parsed.ocean exists then
19:     define disc(v) = (v ≥ τ ? 1 : (v ≤ -τ ? -1 : 0))
20:     return {O: disc(parsed.ocean.O||0), C: disc(parsed.ocean.C||0),
21:             E: disc(parsed.ocean.E||0), A: disc(parsed.ocean.A||0),
22:             N: disc(parsed.ocean.N||0)}
23: else
24:     return {O:0, C:0, E:0, A:0, N:0}
25: end if
26: (Optional) Self-consistency: repeat k times; per-trait majority vote; ties → 0
```

### B.3 Regulation mapping (Zurich-inspired) — pseudocode

```
1: Input: ocean_disc ∈ {−1,0,1}^5  // {O,C,E,A,N}
2: Define directive_set ← []
3: if ocean_disc.E == 1 then
4:     directive_set.append("use energetic, engaging tone")
5: else if ocean_disc.E == -1 then
6:     directive_set.append("adopt calm, reflective tone")
7: end if
8: if ocean_disc.A == 1 then
9:     directive_set.append("acknowledge and affirm briefly")
10: else if ocean_disc.A == -1 then
11:     directive_set.append("state points succinctly, neutral tone")
12: end if
13: if ocean_disc.C == 1 then
14:     directive_set.append("provide 2–3 concise, structured steps")
15: else if ocean_disc.C == -1 then
16:     directive_set.append("offer flexible guidance, optional paths")
17: end if
18: if ocean_disc.O == 1 then
19:     directive_set.append("suggest one small, low-risk exploration")
20: else if ocean_disc.O == -1 then
21:     directive_set.append("use familiar examples; reduce novelty")
22: end if
23: if ocean_disc.N == 1 then
24:     directive_set.append("normalize concerns in one line")
25: else if ocean_disc.N == -1 then
26:     directive_set.append("avoid over‑reassurance")
27: end if
28: directive_set ← take_first_k(directive_set, k=5)
29: Output: directives = directive_set
```

### B.4 Grounded generation (quote‑and‑bound) — pseudocode

```
1: Input: directives[≤5], turn_text, length_range = [70,150], max_questions = 2
2: system_prompt ← "Follow directives; stay within user text only; 70–150 words; ≤2 questions"
3: user_prompt ← "Text: " + turn_text
4: res ← LLM(system=system_prompt, directives=directives, user=user_prompt,
5:            temperature=0.7, max_tokens=220, timeout=20s)
6: reply ← trim(res.text)
7: reply ← enforce_limits(reply, length_range, max_questions)
8: Output: reply
```

### B.5 Verify and (optional) refine — pseudocode

```
1: Input: reply, directives, turn_text
2: pass_policy ← check_adherence(reply, directives)
3: pass_grounding ← check_dialog_grounding(reply, turn_text)
4: if pass_policy and pass_grounding then
5:     Output: decision = "accept", final_reply = reply
6: else
7:     reasons ← list_policy_or_grounding_failures()
8:     refine_prompt ← build_refine_prompt(reply, reasons, directives, turn_text)
9:     refined ← LLM(system=refine_prompt, temperature=0.3, max_tokens=200, timeout=20s)
10:    Output: decision = "refine", final_reply = trim(refined.text)
11: end if
```

### B.6 End‑to‑End MVP loop (single turn) — pseudocode

```
1: Input: message
2: conversation_context ← "user: " + normalize(message)
3: ocean_disc ← DetectDiscrete(conversation_context)  // see B.2
4: directives ← Regulate(ocean_disc)                  // see B.3
5: reply ← GenerateGrounded(directives, message)      // see B.4
6: Output: { reply, ocean_disc, directives }
```

### B.7 Error handling and neutral fallback — pseudocode

```
1: try
2:    run End‑to‑End MVP loop
3: catch e
4:    ocean_disc ← {O:0,C:0,E:0,A:0,N:0}
5:    directives ← ["be concise","maintain neutral tone","ask at most one question"]
6:    reply ← "Thanks for your message. Here’s a concise response based on what you said."
7:    Output: { reply, ocean_disc, directives, error: summarize(e) }
```

## Appendix C — Prompt Skeletons

### Detection Prompt
```
Analyze this conversation to infer personality traits. Return JSON only:
{"ocean": {"O": float, "C": float, "E": float, "A": float, "N": float},
 "trait_conf": {"O": float, "C": float, "E": float, "A": float, "N": float}, 
 "evidence_quotes": [string, string, ...]}
Values in [-1,1], confidence in [0,1]. No prose commentary.
```

### Regulation Prompt  
```
Given OCEAN traits and conversation context, generate ≤4 behavioral directives.
Input: {"ocean": {...}, "stable": bool, "history": [...]}
Output: ["directive focusing on warmth/tone", "directive on directness", ...]
Target dimensions: warmth, directness/hedging, assertiveness, pacing, question ratio.
```

### Generation Prompt
```
Generate response following directives. CRITICAL: Only use conversation content.
Policy directives: [...]
Conversation: [...]
Requirements: Quote/paraphrase dialog only, follow directives, cap questions at 1-2.
```

### Verify Prompt
```
Check response for: (1) Policy directive compliance (2) Dialog grounding
Response: "..."
Policy: [...]
History: [...]
Return: {"pass": bool, "reasons": [string, ...]}
Flag novel claims not supported by conversation.
```
