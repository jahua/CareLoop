# Technical Specifications v1.1
## Personality-Adaptive Conversational AI System

### Executive Summary

This document formalizes a **dialog-only, prompt-only** personality-adaptive conversational AI system that uses OCEAN personality traits as the sole persistent memory state. The system operates through a deterministic pipeline: **ingest → detect → regulate → generate → format**, ensuring therapeutic consistency and healthcare compliance.

**Core Innovation**: Real-time personality inference from conversation turns, mapped to behavioral directives via the Zurich Model, producing grounded responses without external knowledge dependencies.

**Expected Contribution**: 
1. Transparent pipeline from OCEAN cues → directives → grounded responses
2. Lightweight rules that reduce hallucination through dialog-only grounding
3. Evaluation harness measuring stability, directive adherence, and grounding

---

## 1. System Architecture

### 1.1 MVP Implementation Overview

The current MVP implements a **containerized microservices architecture** with the following components:

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Next.js       │    │      N8N        │    │   PostgreSQL    │
│   Frontend      │◄──►│   Workflow      │◄──►│   Database      │
│   (Port 3000)   │    │   Engine        │    │   (Port 5432)   │
│                 │    │   (Port 5678)   │    │                 │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                              │
                              ▼
                       ┌─────────────────┐
                       │     Redis       │
                       │   (Port 6379)   │
                       └─────────────────┘
```

### 1.2 Core Pipeline (Implemented)

**N8N Workflow**: `Manual Trigger → Edit Fields → Ingest → Detect OCEAN → Parse → Regulate → Generate → Format Output`

**Pipeline Stages**:
- **Manual Trigger**: N8N manual execution for testing
- **Edit Fields**: Input JSON `{session_id, message}` configuration
- **Ingest**: Normalize user input into `conversation_context = "user: <msg>"`
- **Detect OCEAN**: Code node calling Juguang API (Gemini-1.5-Pro) for discrete traits
- **Parse**: Extract and validate JSON with fallback thresholds (τ=0.2)
- **Regulate**: Map traits to ≤5 behavioral directives (Zurich Model)
- **Generate**: Code node creating grounded reply (70-150 words, ≤2 questions)
- **Format**: Clean JSON output `{session_id, reply, turn_text, ocean_disc}`

### 1.3 Technology Stack

**Backend Services**:
- **N8N**: Workflow orchestration and API endpoints
- **PostgreSQL 15**: Session state and conversation persistence
- **Redis 7**: Caching and session management
- **Juguang API**: LLM provider (Gemini-1.5-Pro/Flash models)

**Frontend**:
- **Next.js 14**: React-based user interface
- **TypeScript**: Type-safe development
- **Tailwind CSS**: Utility-first styling
- **Lucide React**: Icon components

**Infrastructure**:
- **Docker Compose**: Container orchestration
- **Health Checks**: Service monitoring and dependency management
- **Environment Configuration**: Secure API key management

### 1.4 Operating Principles

- **Dialog-Only Grounding**: All responses must be entailed by conversation history
- **Containerized Deployment**: Docker-based services for scalability
- **API-First Design**: RESTful webhooks and HTTP endpoints
- **Healthcare Compliance**: Audit trails, PII protection, regulatory adherence
- **Development-Ready**: Hot reload, debugging, and testing infrastructure

---

## 2. N8N Workflow Implementation

### 2.1 MVP Workflow (Implemented)

**Source**: `MVP/workflows/Discrete_workflow.json`

| Node | Type | Purpose | Configuration | Output |
|------|------|---------|---------------|--------|
| **Manual Trigger** | `n8n-nodes-base.manualTrigger` | Start workflow manually | Default settings | Triggers execution |
| **Edit Fields** | `n8n-nodes-base.set` | Provide test input JSON | Raw mode: `{session_id, message}` | JSON payload |
| **Ingest** | `n8n-nodes-base.function` | Normalize message, build context | Per-turn processing only | `conversation_context` |
| **Detect OCEAN** | `n8n-nodes-base.code` | Infer discrete OCEAN traits | Juguang API, Gemini-1.5-Pro | `ocean_disc` JSON |
| **Parse Detection** | `n8n-nodes-base.code` | Validate JSON, apply thresholds | τ=0.2 threshold logic | Clean `ocean_disc` |
| **Regulate** | `n8n-nodes-base.function` | Map traits to directives | Zurich Model mapping | `directives` array |
| **Generate Response** | `n8n-nodes-base.code` | Create grounded reply | Juguang API, temperature 0.7 | Full response |
| **Format Output** | `n8n-nodes-base.function` | Compact API payload | Clean JSON structure | Final output |

**API Configuration**:
- **Provider**: Juguang API (`https://ai.juguang.chat/v1/chat/completions`)
- **Models**: Gemini-1.5-Pro (detection), Gemini-1.5-Flash (generation)
- **Timeouts**: 20s per LLM call
- **Temperature**: 0.1 (detection), 0.7 (generation)
- **Max Tokens**: 200 (detection), 220 (generation)

**Execution Mode**:
- Manual trigger for controlled testing
- No database persistence in MVP
- Per-turn processing without history smoothing
- Comprehensive error handling with fallback responses

### 2.2 Full Workflow (Planned)

**Enhanced Pipeline**: `Webhook → Database Query → Ingest → Detect → Smooth → Regulate → Generate → Verify → Refine → Deliver → Database Write`

**Key Additions**:
- **Smoothing**: EMA with confidence weighting for trait stability
- **Verification**: Policy adherence and grounding validation
- **Refinement**: Single-pass correction for failed verifications
- **Persistence**: PostgreSQL state snapshots and conversation history

---

## 3. Deployment Architecture

### 3.1 Container Services

**Docker Compose Stack** (`docker-compose.yml`):

```yaml
services:
  postgres:     # PostgreSQL 15 database
  redis:        # Redis 7 cache
  n8n:          # N8N workflow engine
  # frontend:   # Next.js (commented out in MVP)
```

**Service Configuration**:
- **PostgreSQL**: Port 5432, health checks, persistent volumes
- **Redis**: Port 6379, health checks, data persistence
- **N8N**: Port 5678, webhook endpoints, execution data retention
- **Frontend**: Port 3000 (Next.js, currently disabled in MVP)

### 3.2 Environment Configuration

**Required Environment Variables**:
```bash
# Database
POSTGRES_DB=n8n_personality_ai
POSTGRES_USER=n8n_user
POSTGRES_PASSWORD=n8n_password

# N8N Configuration
N8N_HOST=localhost
N8N_PORT=5678
WEBHOOK_URL=http://localhost:5678

# API Keys
JUGUANG_API_KEY=your_api_key
JUGUANG_API_URL=https://ai.juguang.chat/v1/chat/completions
JUGUANG_MODEL=gemini-1.5-flash
```

### 3.3 Development Workflow

**Setup Process**:
1. **Environment Setup**: Copy `env.example` to `.env` and configure API keys
2. **Service Startup**: `docker-compose up -d` to start all services
3. **Workflow Import**: Import `Discrete_workflow.json` into N8N
4. **Testing**: Use provided test scripts for validation

**Testing Infrastructure**:
- **Automated Tests**: `test_personality_chatbot.sh` - comprehensive test suite
- **Manual Testing**: `test_chatbot.sh` - simple webhook testing
- **Workflow Fixes**: `fix_and_test_workflow.sh` - troubleshooting guide

---

## 4. Core Algorithms

### 4.1 OCEAN Detection (Discrete)

**N8N Code Node Implementation**: Per-turn personality inference with robust fallback

```javascript
// N8N Code Node: Detect OCEAN (Discrete, Gemini Pro)
const apiKey = 'sk-nU7RSKnbZIOwH607r3MfbW5HmP6NIaj1aGVPFGcNDDiL0h5u';
const model = 'gemini-1.5-pro';
const url = 'https://ai.juguang.chat/v1/chat/completions';
const ctx = String($input.first().json.conversation_context || '').trim();

if (!ctx) {
  return [{ json: { choices: [{ message: { content: '{"ocean_disc":{"O":0,"C":0,"E":0,"A":0,"N":0}}' } }] } }];
}

const headers = {
  'Authorization': `Bearer ${apiKey}`,
  'Content-Type': 'application/json'
};

const body = {
  model: model,
  messages: [
    {
      role: 'system',
      content: 'You are a personality detector. Infer Big Five from the user text for THIS TURN ONLY. Return JSON ONLY exactly as: {"ocean_disc":{"O":-1|0|1,"C":-1|0|1,"E":-1|0|1,"A":-1|0|1,"N":-1|0|1}} No prose.'
    },
    {
      role: 'user',
      content: `Text: ${ctx}`
    }
  ],
  temperature: 0.1,
  max_tokens: 200
};

try {
  const res = await this.helpers.httpRequest({
    method: 'POST',
    url: url,
    headers: headers,
    body: body,
    timeout: 20000
  });
  return [{ json: res.json || res }];
} catch (error) {
  return [{ json: { choices: [{ message: { content: '{"ocean_disc":{"O":0,"C":0,"E":0,"A":0,"N":0}}' } }], error: error.message } }];
}
```

**Fallback Strategy**:
- Empty context → neutral OCEAN vector
- API failures → neutral fallback with error logging
- Malformed responses → neutral OCEAN with error details
- Timeout handling → 20s limit with graceful degradation

### 4.2 Regulation Mapping (Zurich Model)

**N8N Function Node Implementation**: Trait-to-directive translation with conflict resolution

```javascript
// N8N Function Node: Build Regulation Directives (Zurich Model)
const inputData = $json || {};
const od = inputData.ocean_disc || { O:0,C:0,E:0,A:0,N:0 };
const sessionId = inputData.session_id || '';
const turnText = inputData.turn_text || '';

const dirs = [];
// Security (N)
if (od.N === -1) dirs.push('offer extra comfort; acknowledge anxieties');
if (od.N === 1)  dirs.push('reassure stability and confidence');
// Arousal (O,E)
if (od.O === 1) dirs.push('invite small exploration/novelty');
if (od.O === -1) dirs.push('reduce novelty; focus on familiar');
if (od.E === 1) dirs.push('use energetic, engaging tone');
if (od.E === -1) dirs.push('adopt calm, reflective tone');
// Affiliation (A)
if (od.A === 1) dirs.push('use warm, collaborative language');
if (od.A === -1) dirs.push('stay neutral and matter-of-fact');
// Conscientiousness (C)
if (od.C === 1) dirs.push('provide 2-3 structured steps');
if (od.C === -1) dirs.push('keep guidance flexible and low-pressure');
// Keep concise
const directives = dirs.slice(0,5);

return {
  session_id: sessionId,
  turn_text: turnText,
  ocean_disc: od,
  directives
};
```

**Directive Categories**:
- **Security (Neuroticism)**: Anxiety management and confidence building
- **Arousal (Openness/Extraversion)**: Energy level and novelty preferences
- **Affiliation (Agreeableness)**: Warmth and collaboration style
- **Structure (Conscientiousness)**: Organization and planning preferences

### 4.3 Grounded Generation

**N8N Code Node Implementation**: Dialog-bounded response synthesis

```javascript
// N8N Code Node: Generate Response (Gemini Pro)
const JUGUANG_API_KEY = 'sk-nU7RSKnbZIOwH607r3MfbW5HmP6NIaj1aGVPFGcNDDiL0h5u';
const MODEL = 'gemini-1.5-pro';
const URL = 'https://ai.juguang.chat/v1/chat/completions';

// Extract all data from the regulation input
const inputData = $input.first()?.json || {};
const directives = inputData?.directives || [];
const sessionId = inputData?.session_id || '';
const turnText = inputData?.turn_text || '';
const oceanDisc = inputData?.ocean_disc || { O:0, C:0, E:0, A:0, N:0 };

let userText = turnText.trim();
if (!userText) {
  userText = 'Please provide a supportive, grounded reply to the user. Context provided separately.';
}

const headers = {
  Authorization: `Bearer ${JUGUANG_API_KEY}`,
  'Content-Type': 'application/json'
};

const sys = [
  'You are a supportive assistant. Follow these behavior directives strictly:',
  JSON.stringify(directives),
  'Constraints: stay grounded in the user text only; 1-2 questions max; 70-150 words.'
].join(' ');

const body = {
  model: MODEL,
  messages: [
    { role: 'system', content: sys },
    { role: 'user', content: userText }
  ],
  temperature: 0.7,
  max_tokens: 220
};

try {
  const res = await this.helpers.httpRequest({ 
    method: 'POST', 
    url: URL, 
    headers, 
    body, 
    timeout: 20000 
  });
  
  const responseData = {
    ...res.json || res,
    session_id: sessionId,
    turn_text: turnText,
    ocean_disc: oceanDisc,
    directives: directives
  };
  
  return { json: responseData };
} catch (e) {
  return {
    json: {
      choices: [{ message: { content: 'Sorry—response is temporarily unavailable. Quick tip: take 3 slow breaths and exhale longer than you inhale.' } }],
      error: { status: e?.response?.status, data: e?.response?.data },
      session_id: sessionId,
      turn_text: turnText,
      ocean_disc: oceanDisc,
      directives: directives
    }
  };
}
```

**Generation Constraints**:
- **Dialog Grounding**: Only reference information from conversation context
- **Length Control**: 70-150 words with 1-2 questions maximum
- **Directive Adherence**: Strictly follow behavioral directives from regulation
- **Error Handling**: Graceful fallback with supportive breathing tip

---

## 5. Frontend Implementation

### 5.1 Next.js Application Structure

**Technology Stack**:
- **Framework**: Next.js 14 with App Router
- **Language**: TypeScript for type safety
- **Styling**: Tailwind CSS for utility-first design
- **Icons**: Lucide React for consistent iconography
- **HTTP Client**: Axios for API communication

**Component Architecture**:
```
src/
├── app/
│   ├── globals.css          # Global styles
│   ├── layout.tsx           # Root layout
│   └── page.tsx             # Main chat page
└── components/
    ├── ChatInterface.tsx    # Main chat UI component
    └── PersonalityDashboard.tsx # OCEAN traits visualization
```

### 5.2 Chat Interface Features

**Core Functionality**:
- **Real-time Messaging**: Send/receive messages with N8N webhook
- **Personality Visualization**: Live OCEAN traits display
- **Session Management**: UUID-based session tracking
- **Responsive Design**: Mobile-friendly interface
- **Auto-scroll**: Automatic message history scrolling

**State Management**:
```typescript
interface PersonalityState {
  ocean: { O: number; C: number; E: number; A: number; N: number };
  stable: boolean;
  confidence_scores: { O: number; C: number; E: number; A: number; N: number };
  policy_plan: string[];
}
```

### 5.3 API Integration

**Webhook Communication**:
- **Endpoint**: `http://localhost:5678/webhook/chat`
- **Method**: POST with JSON payload
- **Request**: `{session_id: string, message: string}`
- **Response**: `{reply: string, ocean: object, policy_plan: string[]}`

---

## 6. Data Schemas

### 6.1 State JSON (Single Source of Truth)

```json
{
    "session_id": "uuid",
    "turn_index": 17,
    "history": [
        {"role": "user", "text": "How are you feeling today?"},
        {"role": "assistant", "text": "I'm doing well, thank you for asking."}
    ],
    "ocean": {"O": 0.4, "C": -0.1, "E": 0.0, "A": 0.5, "N": -0.3},
    "trait_conf": {"O": 0.72, "C": 0.61, "E": 0.58, "A": 0.74, "N": 0.69},
    "stable": true,
    "policy_plan": ["validate briefly", "ask one open question", "concise sentences"],
    "flags": {"refined_once": false, "neutral_fallback": false},
    "timings_ms": {"detect": 380, "generate": 920, "verify": 210, "total": 1510},
    "last_updated": "2024-09-02T14:33:00Z"
}
```

### 6.2 Database Schema (PostgreSQL)

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
    role VARCHAR(10) NOT NULL,
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
```

---

## 7. API Specification

### 7.1 Core Endpoints

**POST /webhook/chat** (N8N Webhook)
- **Request**: `{session_id: "uuid", message: "user input"}`
- **Response**: `{reply: "response", policy_plan: [...], ocean_preview: {...}, timings_ms: {...}}`

**GET /api/session/{id}/state** (FastAPI/Next.js)
- **Response**: Complete state JSON from latest turn

**GET /api/session/{id}/summary** (FastAPI/Next.js)
- **Response**: `{summary_bullets: [...], ocean: {...}, last_directives: [...], turn_count: N}`

**POST /webhook/session/reset** (N8N Webhook)
- **Request**: `{session_id: "uuid"}`
- **Effect**: Reset session to neutral state

### 7.2 MVP Execution Mode

**Manual Trigger**: No webhook, input via `Edit Fields` node
**Output Format**:
```json
{
    "session_id": "uuid",
    "reply": "assistant response",
    "turn_text": "original user message",
    "ocean_disc": {"O": 0, "C": 0, "E": 0, "A": 0, "N": 0}
}
```

---

## 8. Testing & Validation

### 8.1 Automated Test Suite

**Comprehensive Testing Script**: `test_personality_chatbot.sh`

**Test Cases**:
- **High Extraversion**: Social, energetic communication patterns
- **High Introversion**: Quiet, reflective communication style
- **High Neuroticism**: Anxious, worried communication patterns
- **Low Neuroticism**: Confident, optimistic communication
- **High Conscientiousness**: Analytical, structured thinking

**Test Execution**:
```bash
# Run comprehensive test suite
./test_personality_chatbot.sh

# Manual webhook testing
./test_chatbot.sh

# Workflow troubleshooting
./fix_and_test_workflow.sh
```

### 8.2 Performance Validation

**Response Time Monitoring**:
- **Target**: P95 ≤ 2.5 seconds for standard responses
- **Measurement**: End-to-end webhook response time
- **Timeout**: 45-second maximum per test case

**Quality Metrics**:
- **OCEAN Detection**: Valid JSON with discrete values (-1, 0, 1)
- **Response Grounding**: No external knowledge claims
- **Directive Adherence**: Behavioral directives properly applied
- **Error Handling**: Graceful fallbacks on API failures

### 8.3 Development Testing

**Local Development Setup**:
1. **Environment**: Copy `env.example` to `.env`
2. **Services**: `docker-compose up -d`
3. **Workflow**: Import `Discrete_workflow.json`
4. **Validation**: Run test scripts

**Debugging Tools**:
- **N8N Execution Logs**: Detailed workflow execution traces
- **Console Logging**: JavaScript console output in code nodes
- **Error Tracking**: Comprehensive error handling with fallbacks

---

## 9. Performance & Reliability

### 9.1 Latency Targets

- **P95 Standard Response**: ≤2.5 seconds
- **P95 With Refinement**: ≤5.0 seconds
- **LLM Call Timeout**: 20 seconds (MVP) / 15 seconds (full)
- **Total Request Timeout**: 30 seconds

### 9.2 Error Handling

**Fallback Strategy**:
- Detection errors → neutral OCEAN vector
- Generation errors → supportive stock response
- System failures → conversation-appropriate fallback with preserved state

**Circuit Breakers**: Exponential backoff for LLM provider failures
**Retry Logic**: Bounded retry mechanisms prevent cascade failures

---

## 10. Evaluation Framework

### 10.1 Performance Metrics

| Metric | Target | Rationale |
|--------|--------|-----------|
| **Stability Time** | ≤5 turns | Achieve stable personality detection |
| **Oscillation Rate** | <10% | Avoid jarring tone shifts |
| **Policy Adherence** | >90% | Directives reliably shape replies |
| **Grounding Violations** | <5% | Maintain dialog-bounded content |
| **P95 Latency** | ≤2.5s | Keep interaction responsive |

### 10.2 Testing Infrastructure

**Automated Testing**:
- Scripted dialog replay for deterministic testing
- Regression testing for prompt version changes
- Personality ground truth comparison
- Automated metric collection

**Evaluation Harness**:
- Conversation simulation
- Behavioral baseline validation
- Continuous system improvement cycles

---

## 11. Security & Compliance

### 11.1 Privacy Protection

- **Dialog-Only Grounding**: No external data dependencies
- **PII Redaction**: Pre-processing hooks before persistence
- **Session Encryption**: Data protection at rest
- **Access Control**: RBAC with configurable retention policies

### 11.2 Healthcare Compliance

- **Audit Logging**: Immutable timestamps for all decisions
- **GDPR/HIPAA Support**: Configurable data retention
- **Regulatory Adherence**: Comprehensive decision trails
- **State Encryption**: Queryable yet protected conversation data

---

## 12. Deployment Architecture

### 12.1 Container Strategy

- **N8N Workflow Engine**: Independent scaling for workflow execution
- **PostgreSQL Database**: Shared state persistence
- **Next.js Frontend**: Client interfaces and supplementary APIs
- **Container Orchestration**: Independent service scaling

### 12.2 Deployment Patterns

- **Blue/Green Deployment**: Zero-downtime prompt updates
- **Canary Releases**: Gradual model rollout with auto-rollback
- **Configuration Management**: Environment-based model/prompt control
- **Validation**: Consistent deployment across environments

---

## 13. Implementation Roadmap

### 13.1 MVP (Current)
- ✅ Discrete OCEAN detection
- ✅ Basic regulation mapping
- ✅ Grounded generation
- ✅ Manual workflow execution

### 13.2 Phase 1 (Next)
- 🔄 EMA smoothing implementation
- 🔄 Verification/refinement pipeline
- 🔄 Database persistence
- 🔄 Webhook API endpoints

### 13.3 Phase 2 (Future)
- ⏳ Advanced observability
- ⏳ A/B testing framework
- ⏳ Performance optimization
- ⏳ Production deployment

---

## Appendix A: Prompt Templates

### Detection Prompt (Discrete)
```
Analyze this conversation turn to infer personality traits. Return JSON only:
{"ocean_disc": {"O": -1|0|1, "C": -1|0|1, "E": -1|0|1, "A": -1|0|1, "N": -1|0|1}}

No prose commentary. Values: -1 (low), 0 (neutral), 1 (high).
```

### Regulation Prompt
```
Given OCEAN traits, generate ≤4 behavioral directives.
Input: {"ocean_disc": {...}}
Output: ["directive1", "directive2", ...]
Target: warmth, directness, assertiveness, pacing, question ratio.
```

### Generation Prompt
```
Generate response following directives. CRITICAL: Only use conversation content.
Policy directives: [...]
User text: "..."
Requirements: Quote/paraphrase dialog only, follow directives, 70-150 words, ≤2 questions.
```

### Verification Prompt
```
Check response for: (1) Policy compliance (2) Dialog grounding
Response: "..."
Policy: [...]
History: [...]
Return: {"pass": bool, "reasons": [...]}
```

---

*This specification provides implementation-ready details for building a personality-adaptive conversational AI system with deterministic behavior, comprehensive audit trails, and healthcare compliance requirements.*
