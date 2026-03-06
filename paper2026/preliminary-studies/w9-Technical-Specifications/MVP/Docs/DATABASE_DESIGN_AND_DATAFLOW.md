# Database Design & Data Flow Documentation

**Personality-Adaptive AI Chatbot with EMA Smoothing**  
**Version:** Phase 1 - PostgreSQL Enhanced  
**Last Updated:** October 1, 2025

---

## Table of Contents

1. [Overview](#overview)
2. [Database Schema](#database-schema)
3. [Data Flow Architecture](#data-flow-architecture)
4. [Design Decisions](#design-decisions)
5. [Entity Relationship Diagram](#entity-relationship-diagram)
6. [Helper Functions & Views](#helper-functions--views)
7. [Indexes & Performance](#indexes--performance)
8. [Integration with N8N Workflow](#integration-with-n8n-workflow)
9. [EMA Smoothing Integration](#ema-smoothing-integration)
10. [Usage Examples](#usage-examples)
11. [Maintenance & Optimization](#maintenance--optimization)

---

## Overview

### Purpose

This database stores and manages:
- **Chat sessions** with unique identifiers
- **Conversation history** (turn-by-turn user/assistant exchanges)
- **Personality states** with OCEAN trait values and confidence scores
- **Performance metrics** for monitoring and evaluation
- **EMA smoothing** continuity across conversation turns

### Technology Stack

- **Database:** PostgreSQL 12+
- **Schema Version:** 1.0
- **N8N Integration:** 4 PostgreSQL nodes (1 read, 3 write)
- **Data Types:** UUID, JSONB, FLOAT, TEXT, TIMESTAMP

### Key Features

✅ **Session Management:** Track multi-turn conversations  
✅ **Personality Evolution:** Store personality state snapshots per turn  
✅ **EMA Continuity:** Enable exponential moving average across sessions  
✅ **Verification Tracking:** Record response quality and adherence  
✅ **Performance Monitoring:** Track pipeline execution status  
✅ **Cascade Deletion:** Automatic cleanup when sessions are deleted  
✅ **ACID Compliance:** Reliable transactional operations

---

## Database Schema

### 1. `chat_sessions` Table

**Purpose:** Master table for chat sessions, storing session-level metadata.

```sql
CREATE TABLE chat_sessions (
    session_id UUID PRIMARY KEY,
    total_turns INTEGER DEFAULT 0,
    evaluation_mode BOOLEAN DEFAULT FALSE,
    baseline_comparison BOOLEAN DEFAULT FALSE,
    status VARCHAR(20) DEFAULT 'active',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

#### Column Descriptions

| Column | Type | Description | Default | Constraints |
|--------|------|-------------|---------|-------------|
| `session_id` | UUID | Unique session identifier | - | PRIMARY KEY |
| `total_turns` | INTEGER | Total conversation turns | 0 | - |
| `evaluation_mode` | BOOLEAN | Is this an evaluation session? | FALSE | - |
| `baseline_comparison` | BOOLEAN | Compare with baseline? | FALSE | - |
| `status` | VARCHAR(20) | Session status (active/inactive) | 'active' | - |
| `created_at` | TIMESTAMP | Session creation time | CURRENT_TIMESTAMP | - |
| `updated_at` | TIMESTAMP | Last update time | CURRENT_TIMESTAMP | Auto-updated |

#### Indexes

```sql
CREATE INDEX idx_sessions_created ON chat_sessions(created_at);
CREATE INDEX idx_sessions_status ON chat_sessions(status);
```

#### Usage in Workflow

- **Node:** "Save Session (PostgreSQL)"
- **Operation:** `INSERT ... ON CONFLICT ... DO UPDATE`
- **Frequency:** Once per conversation turn
- **Updates:** `total_turns` increments, `updated_at` refreshed

---

### 2. `conversation_turns` Table

**Purpose:** Stores turn-by-turn conversation history with verification metadata.

```sql
CREATE TABLE conversation_turns (
    id SERIAL PRIMARY KEY,
    session_id UUID REFERENCES chat_sessions(session_id) ON DELETE CASCADE,
    turn_index INTEGER NOT NULL,
    user_message TEXT,
    assistant_response TEXT,
    directives_applied JSONB DEFAULT '[]',
    verification_status VARCHAR(20),
    adherence_score FLOAT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(session_id, turn_index)
);
```

#### Column Descriptions

| Column | Type | Description | Default | Constraints |
|--------|------|-------------|---------|-------------|
| `id` | SERIAL | Auto-incrementing primary key | - | PRIMARY KEY |
| `session_id` | UUID | Foreign key to chat_sessions | - | REFERENCES chat_sessions |
| `turn_index` | INTEGER | Turn number within session | - | NOT NULL |
| `user_message` | TEXT | User's input message | - | - |
| `assistant_response` | TEXT | Bot's verified response | - | - |
| `directives_applied` | JSONB | Personality directives used | '[]' | JSON array |
| `verification_status` | VARCHAR(20) | verified/refined/failed | - | - |
| `adherence_score` | FLOAT | Quality score (0.0-1.0) | - | - |
| `created_at` | TIMESTAMP | Turn creation time | CURRENT_TIMESTAMP | - |

#### Composite Key

```sql
UNIQUE(session_id, turn_index)
```

This ensures each turn number is unique within a session, preventing duplicate turns.

#### Indexes

```sql
CREATE INDEX idx_turns_session ON conversation_turns(session_id);
CREATE INDEX idx_turns_created ON conversation_turns(created_at);
```

#### JSONB Field: `directives_applied`

**Example:**
```json
[
  "Focus on familiar topics; reduce novelty",
  "Keep the demeanour flexible, relaxed, and spontaneous",
  "Adopt a calm, low-key style with reflective space",
  "Offer extra comfort; acknowledge anxieties"
]
```

This allows querying which personality directives were used:
```sql
SELECT * FROM conversation_turns 
WHERE directives_applied @> '["Offer extra comfort; acknowledge anxieties"]'::jsonb;
```

#### Usage in Workflow

- **Node:** "Save Conversation Turn (PostgreSQL)"
- **Operation:** `INSERT ... ON CONFLICT ... DO UPDATE`
- **Frequency:** Once per conversation turn
- **Data Source:** Combines user input + verifier output

---

### 3. `personality_states` Table

**Purpose:** Stores OCEAN personality trait snapshots per turn for EMA continuity.

```sql
CREATE TABLE personality_states (
    id SERIAL PRIMARY KEY,
    session_id UUID REFERENCES chat_sessions(session_id) ON DELETE CASCADE,
    turn_index INTEGER NOT NULL,
    ocean_o FLOAT,
    ocean_c FLOAT,
    ocean_e FLOAT,
    ocean_a FLOAT,
    ocean_n FLOAT,
    confidence_o FLOAT,
    confidence_c FLOAT,
    confidence_e FLOAT,
    confidence_a FLOAT,
    confidence_n FLOAT,
    stable BOOLEAN DEFAULT FALSE,
    ema_applied BOOLEAN DEFAULT FALSE,
    emotional_state VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(session_id, turn_index)
);
```

#### Column Descriptions

| Column | Type | Description | Range | Purpose |
|--------|------|-------------|-------|---------|
| `id` | SERIAL | Auto-incrementing ID | - | PRIMARY KEY |
| `session_id` | UUID | Foreign key | - | Links to session |
| `turn_index` | INTEGER | Turn number | 1+ | Identifies turn |
| `ocean_o` | FLOAT | Openness trait value | -1.0 to 1.0 | Personality dimension |
| `ocean_c` | FLOAT | Conscientiousness | -1.0 to 1.0 | Personality dimension |
| `ocean_e` | FLOAT | Extraversion | -1.0 to 1.0 | Personality dimension |
| `ocean_a` | FLOAT | Agreeableness | -1.0 to 1.0 | Personality dimension |
| `ocean_n` | FLOAT | Neuroticism | -1.0 to 1.0 | Personality dimension |
| `confidence_o` | FLOAT | Openness confidence | 0.0 to 1.0 | Detection certainty |
| `confidence_c` | FLOAT | Conscientiousness conf | 0.0 to 1.0 | Detection certainty |
| `confidence_e` | FLOAT | Extraversion conf | 0.0 to 1.0 | Detection certainty |
| `confidence_a` | FLOAT | Agreeableness conf | 0.0 to 1.0 | Detection certainty |
| `confidence_n` | FLOAT | Neuroticism conf | 0.0 to 1.0 | Detection certainty |
| `stable` | BOOLEAN | Is personality stable? | - | EMA stability flag |
| `ema_applied` | BOOLEAN | Was EMA used? | - | Tracking flag |
| `emotional_state` | VARCHAR(50) | Detected emotion | - | Optional metadata |
| `created_at` | TIMESTAMP | Creation time | - | Timestamp |

#### Composite Key

```sql
UNIQUE(session_id, turn_index)
```

#### Indexes

```sql
CREATE INDEX idx_personality_session ON personality_states(session_id);
CREATE INDEX idx_personality_stable ON personality_states(stable);
CREATE INDEX idx_personality_created ON personality_states(created_at);
```

#### Usage in Workflow

- **Read Node:** "Load Previous State (PostgreSQL)"
  - Uses `get_latest_personality_state(session_id)` function
  - Retrieves previous turn's OCEAN values for EMA smoothing
  
- **Write Node:** "Save Personality State (PostgreSQL)"
  - Stores current turn's smoothed OCEAN values
  - Updates `stable` flag when personality stabilizes

#### EMA Integration

**Turn 1:**
```sql
ocean_o = detected_value  -- No smoothing
ema_applied = FALSE
stable = FALSE
```

**Turn 2+:**
```sql
ocean_o = 0.3 * detected_value + 0.7 * previous_ocean_o  -- EMA smoothing
ema_applied = TRUE
stable = (turn_index >= 5 AND all_confidence >= 0.6)
```

---

### 4. `performance_metrics` Table

**Purpose:** Tracks pipeline execution status and performance (Phase 1: Not fully implemented).

```sql
CREATE TABLE performance_metrics (
    id SERIAL PRIMARY KEY,
    session_id UUID REFERENCES chat_sessions(session_id) ON DELETE CASCADE,
    turn_index INTEGER NOT NULL,
    detector_status VARCHAR(20),
    regulator_status VARCHAR(20),
    generator_status VARCHAR(20),
    verifier_status VARCHAR(20),
    database_status VARCHAR(20),
    total_processing_time_ms INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(session_id, turn_index)
);
```

#### Column Descriptions

| Column | Type | Description | Values |
|--------|------|-------------|--------|
| `id` | SERIAL | Auto-incrementing ID | - |
| `session_id` | UUID | Foreign key | - |
| `turn_index` | INTEGER | Turn number | 1+ |
| `detector_status` | VARCHAR(20) | Personality detection status | success/error/pending |
| `regulator_status` | VARCHAR(20) | Regulation status | success/error/pending |
| `generator_status` | VARCHAR(20) | Generation status | success/error/pending |
| `verifier_status` | VARCHAR(20) | Verification status | verified/refined/failed |
| `database_status` | VARCHAR(20) | DB save status | success/error |
| `total_processing_time_ms` | INTEGER | Total pipeline time (ms) | 0+ |
| `created_at` | TIMESTAMP | Creation time | - |

#### Indexes

```sql
CREATE INDEX idx_metrics_session ON performance_metrics(session_id);
CREATE INDEX idx_metrics_created ON performance_metrics(created_at);
```

#### Future Implementation

**Planned for Phase 2:**
- Automatic population from N8N execution data
- Performance dashboard
- Anomaly detection
- A/B testing support

---

## Data Flow Architecture

### High-Level Flow

```
┌─────────────────────────────────────────────────────────────────────┐
│                         N8N WORKFLOW                                 │
├─────────────────────────────────────────────────────────────────────┤
│                                                                      │
│  1. Webhook Trigger (User Input)                                    │
│          ↓                                                           │
│  2. Enhanced Ingest (Extract session_id, clean_msg)                 │
│          ↓                                                           │
│  ┌──────────────────────────────────────────────┐                   │
│  │ 3. Load Previous State (PostgreSQL) ← READ  │                   │
│  │    SELECT * FROM get_latest_personality_state()                  │
│  │    Returns: previous OCEAN + confidence                          │
│  └──────────────────────────────────────────────┘                   │
│          ↓                                                           │
│  4. Combine Inputs (Merge Node)                                     │
│          ↓                                                           │
│  5. Merge Previous State (Attach previous_state to data)            │
│          ↓                                                           │
│  6. Zurich Model Detection (EMA)                                    │
│     - Uses previous_state for EMA smoothing                         │
│     - Calculates smoothed OCEAN values                              │
│          ↓                                                           │
│  7. Enhanced Regulation (Generate directives)                       │
│          ↓                                                           │
│  8. Enhanced Generation (Create response)                           │
│          ↓                                                           │
│  9. Verification & Refinement (Check quality)                       │
│          ↓                                                           │
│  ┌──────────────────────────────────────────────┐                   │
│  │ 10. PARALLEL SAVES (3 PostgreSQL Nodes)     │                   │
│  │                                              │                   │
│  │  ├─> Save Session ← WRITE                   │                   │
│  │  │   INSERT INTO chat_sessions              │                   │
│  │  │                                           │                   │
│  │  ├─> Save Conversation Turn ← WRITE         │                   │
│  │  │   INSERT INTO conversation_turns         │                   │
│  │  │                                           │                   │
│  │  └─> Save Personality State ← WRITE         │                   │
│  │      INSERT INTO personality_states          │                   │
│  └──────────────────────────────────────────────┘                   │
│          ↓                                                           │
│  11. Merge DB Results (Confirm saves)                               │
│          ↓                                                           │
│  12. Phase 1 Enhanced Output (Format response)                      │
│          ↓                                                           │
│  13. Return API Response                                            │
│                                                                      │
└─────────────────────────────────────────────────────────────────────┘
```

---

### Detailed Data Flow: Turn-by-Turn

#### **Turn 1: First Message**

```
User sends message → Webhook
    ↓
Enhanced Ingest creates session_id (if not provided)
    ↓
Load Previous State (PostgreSQL)
    Query: get_latest_personality_state(session_id)
    Result: EMPTY (no previous state)
    ↓
Merge Previous State
    previous_state = {
      ocean: {O:0, C:0, E:0, A:0, N:0},
      confidence: {O:0.5, C:0.5, E:0.5, A:0.5, N:0.5},
      turn_index: 0,
      stable: false,
      loaded_from_db: false
    }
    ↓
Zurich Model Detection (EMA)
    Raw detection: ocean_detected = {O:0.3, C:-0.5, E:0.7, A:0.2, N:-0.3}
    EMA calculation: smoothed_ocean = ocean_detected (no smoothing on turn 1)
    ↓
... (regulation, generation, verification) ...
    ↓
Save Personality State (PostgreSQL)
    INSERT INTO personality_states:
      session_id: abc-123-def
      turn_index: 1
      ocean_o: 0.3
      ocean_c: -0.5
      ocean_e: 0.7
      ocean_a: 0.2
      ocean_n: -0.3
      confidence_o: 0.8
      ... (etc)
      stable: false
      ema_applied: false
```

#### **Turn 2: Second Message (EMA Applied)**

```
User sends message → Webhook
    ↓
Enhanced Ingest (same session_id)
    ↓
Load Previous State (PostgreSQL)
    Query: get_latest_personality_state(session_id)
    Result: {
      ocean_o: 0.3, ocean_c: -0.5, ocean_e: 0.7, ocean_a: 0.2, ocean_n: -0.3,
      confidence_o: 0.8, ...,
      turn_index: 1,
      stable: false
    }
    ↓
Merge Previous State
    previous_state = {
      ocean: {O:0.3, C:-0.5, E:0.7, A:0.2, N:-0.3},  ← From DB!
      confidence: {O:0.8, C:0.7, E:0.9, A:0.6, N:0.5},
      turn_index: 1,
      stable: false,
      loaded_from_db: true  ← Important!
    }
    ↓
Zurich Model Detection (EMA)
    Raw detection: ocean_detected = {O:0.5, C:-0.3, E:0.6, A:0.4, N:-0.2}
    EMA calculation (α=0.3):
      smoothed_ocean.O = 0.3 * 0.5 + 0.7 * 0.3 = 0.36
      smoothed_ocean.C = 0.3 * (-0.3) + 0.7 * (-0.5) = -0.44
      ... (etc for all traits)
    ↓
... (regulation, generation, verification) ...
    ↓
Save Personality State (PostgreSQL)
    INSERT INTO personality_states:
      session_id: abc-123-def
      turn_index: 2
      ocean_o: 0.36  ← EMA smoothed!
      ocean_c: -0.44
      ... (etc)
      stable: false
      ema_applied: true  ← EMA was applied
```

#### **Turn 5+: Stable Personality**

```
... (same flow) ...
    ↓
Zurich Model Detection (EMA)
    turn_index: 5
    All confidence values >= 0.6
    
    personality_stable = true  ← Stability achieved!
    ↓
Save Personality State (PostgreSQL)
    stable: true  ← Marked as stable
```

---

### Database Read Operations

#### 1. **Load Previous State**

**N8N Node:** "Load Previous State (PostgreSQL)"

**Query:**
```sql
SELECT * FROM get_latest_personality_state('{{ $json.session_id }}')
```

**Function Definition:**
```sql
CREATE OR REPLACE FUNCTION get_latest_personality_state(p_session_id UUID)
RETURNS TABLE(
    ocean_o FLOAT,
    ocean_c FLOAT,
    ocean_e FLOAT,
    ocean_a FLOAT,
    ocean_n FLOAT,
    confidence_o FLOAT,
    confidence_c FLOAT,
    confidence_e FLOAT,
    confidence_a FLOAT,
    confidence_n FLOAT,
    stable BOOLEAN,
    turn_index INTEGER
) AS $$
BEGIN
    RETURN QUERY
    SELECT 
        ps.ocean_o, ps.ocean_c, ps.ocean_e, ps.ocean_a, ps.ocean_n,
        ps.confidence_o, ps.confidence_c, ps.confidence_e, 
        ps.confidence_a, ps.confidence_n,
        ps.stable,
        ps.turn_index
    FROM personality_states ps
    WHERE ps.session_id = p_session_id
    ORDER BY ps.turn_index DESC
    LIMIT 1;
END;
$$ LANGUAGE plpgsql;
```

**Returns:**
- Latest personality state for the session
- Empty result if no previous state exists (turn 1)

**Performance:** O(log n) due to index on (session_id, turn_index)

---

### Database Write Operations

#### 2. **Save Session**

**N8N Node:** "Save Session (PostgreSQL)"

**Query:**
```sql
INSERT INTO chat_sessions (session_id, total_turns, evaluation_mode, status)
VALUES ('{{ $json.session_id }}', {{ $json.turn_index || 1 }}, {{ $json.evaluation_mode ? 'true' : 'false' }}, 'active')
ON CONFLICT (session_id) 
DO UPDATE SET 
  total_turns = GREATEST(chat_sessions.total_turns, EXCLUDED.total_turns),
  updated_at = CURRENT_TIMESTAMP
```

**Behavior:**
- **First turn:** Creates new session record
- **Subsequent turns:** Updates `total_turns` if higher, refreshes `updated_at`
- **UPSERT operation:** Safe for concurrent requests

---

#### 3. **Save Conversation Turn**

**N8N Node:** "Save Conversation Turn (PostgreSQL)"

**Query:**
```sql
INSERT INTO conversation_turns (
  session_id, turn_index, user_message, assistant_response,
  directives_applied, verification_status, adherence_score
) VALUES (
  '{{ $json.session_id }}',
  {{ $json.turn_index || 1 }},
  $${{ $json.clean_msg || "" }}$$,
  $${{ $json.verifier?.verified_response || $json.generator?.raw_content || "" }}$$,
  '{{ JSON.stringify($json.directives || []) }}'::jsonb,
  '{{ $json.verifier?.verification_status || "unknown" }}',
  {{ $json.verifier?.adherence_score || 0 }}
)
ON CONFLICT (session_id, turn_index) DO UPDATE SET
  assistant_response = EXCLUDED.assistant_response,
  directives_applied = EXCLUDED.directives_applied,
  verification_status = EXCLUDED.verification_status,
  adherence_score = EXCLUDED.adherence_score
```

**Data Sources:**
- `user_message` ← from `clean_msg` (Enhanced Ingest)
- `assistant_response` ← from `verifier.verified_response` (Verification node)
- `directives_applied` ← from `directives` array (Regulation node)
- `verification_status` ← from `verifier.verification_status`
- `adherence_score` ← from `verifier.adherence_score`

**Dollar Quoting:** `$$..$$` used for TEXT fields to handle quotes in messages

---

#### 4. **Save Personality State**

**N8N Node:** "Save Personality State (PostgreSQL)"

**Query:**
```sql
INSERT INTO personality_states (
  session_id, turn_index,
  ocean_o, ocean_c, ocean_e, ocean_a, ocean_n,
  confidence_o, confidence_c, confidence_e, confidence_a, confidence_n,
  stable, ema_applied
) VALUES (
  '{{ $json.session_id }}',
  {{ $json.turn_index || 1 }},
  {{ $json.detector?.smoothed_ocean?.O || 0 }},
  {{ $json.detector?.smoothed_ocean?.C || 0 }},
  {{ $json.detector?.smoothed_ocean?.E || 0 }},
  {{ $json.detector?.smoothed_ocean?.A || 0 }},
  {{ $json.detector?.smoothed_ocean?.N || 0 }},
  {{ $json.detector?.smoothed_confidence?.O || 0.5 }},
  {{ $json.detector?.smoothed_confidence?.C || 0.5 }},
  {{ $json.detector?.smoothed_confidence?.E || 0.5 }},
  {{ $json.detector?.smoothed_confidence?.A || 0.5 }},
  {{ $json.detector?.smoothed_confidence?.N || 0.5 }},
  {{ $json.detector?.personality_stable ? 'true' : 'false' }},
  {{ $json.detector?.ema_applied ? 'true' : 'false' }}
)
ON CONFLICT (session_id, turn_index) DO UPDATE SET
  ocean_o = EXCLUDED.ocean_o,
  ocean_c = EXCLUDED.ocean_c,
  ocean_e = EXCLUDED.ocean_e,
  ocean_a = EXCLUDED.ocean_a,
  ocean_n = EXCLUDED.ocean_n,
  stable = EXCLUDED.stable
```

**Data Source:** All from `detector` object (Zurich Model Detection node)

**Critical Fields:**
- `smoothed_ocean.*` ← EMA-smoothed values (not raw detection)
- `smoothed_confidence.*` ← EMA-smoothed confidence
- `stable` ← Calculated from turn_index and confidence thresholds
- `ema_applied` ← TRUE if turn > 1 and previous state existed

---

## Design Decisions

### 1. **Why 4 Separate Tables?**

**Separation of Concerns:**
- `chat_sessions` → Session metadata
- `conversation_turns` → Conversation history
- `personality_states` → Personality snapshots
- `performance_metrics` → Pipeline monitoring

**Benefits:**
- Clear domain boundaries
- Easier to query specific data
- Independent schema evolution
- Optimized indexing per table
- Parallel write operations

**Alternative Rejected:**
- ❌ Single denormalized table → Data duplication, harder to query
- ❌ Document store (MongoDB) → Lacks ACID guarantees for EMA continuity

---

### 2. **Why UUID for session_id?**

**Advantages:**
- **Globally unique:** No collision risk across distributed systems
- **Security:** Not sequential, harder to guess other sessions
- **Scalability:** Can be generated client-side
- **Database-agnostic:** Portable across PostgreSQL, MySQL, etc.

**Trade-off:**
- Larger storage (16 bytes vs 4 bytes for INT)
- Slightly slower indexes

**Verdict:** Benefits outweigh costs for multi-client chatbot system

---

### 3. **Why JSONB for directives_applied?**

**Use Case:** Personality directives are variable-length arrays:
```json
["Directive 1", "Directive 2", "Directive 3"]
```

**JSONB Advantages:**
- **Flexible:** Array length varies (1-5 directives typically)
- **Queryable:** Can search for specific directives
- **Indexable:** GIN indexes for fast JSON queries
- **Schema evolution:** Add metadata without migration

**Example Query:**
```sql
-- Find turns that used "calm, low-key" directive
SELECT session_id, turn_index, user_message
FROM conversation_turns
WHERE directives_applied @> '["Adopt a calm, low-key style with reflective space"]'::jsonb;
```

---

### 4. **Why Separate OCEAN Columns Instead of JSON?**

**Choice:** 5 separate columns (`ocean_o`, `ocean_c`, etc.) vs 1 JSON column

**Reasons for Separate Columns:**
- **Math operations:** Can calculate averages, std dev, ranges
- **Indexing:** Can index individual traits
- **Type safety:** PostgreSQL enforces FLOAT type
- **Performance:** Faster numerical queries
- **SQL analytics:** Easy to aggregate and analyze

**Example Queries Enabled:**
```sql
-- Average Openness across all sessions
SELECT AVG(ocean_o) FROM personality_states WHERE stable = true;

-- Find highly extraverted users
SELECT session_id FROM personality_states 
WHERE ocean_e > 0.7 AND stable = true
GROUP BY session_id;

-- Personality stability over turns
SELECT turn_index, AVG(ocean_o), AVG(ocean_c), AVG(ocean_e), AVG(ocean_a), AVG(ocean_n)
FROM personality_states
WHERE session_id = 'some-uuid'
GROUP BY turn_index
ORDER BY turn_index;
```

---

### 5. **Why ON CONFLICT DO UPDATE (UPSERT)?**

**Problem:** N8N workflow might execute twice due to:
- Network retries
- Manual re-execution
- Debugging/testing

**Solution:** UPSERT pattern prevents duplicate key errors:

```sql
INSERT INTO personality_states (session_id, turn_index, ...)
VALUES (...)
ON CONFLICT (session_id, turn_index) DO UPDATE SET ...
```

**Behavior:**
- **First execution:** Creates new row
- **Retry/re-execution:** Updates existing row
- **Idempotent:** Safe to run multiple times

---

### 6. **Why CASCADE DELETE?**

**Foreign Key Constraints:**
```sql
session_id UUID REFERENCES chat_sessions(session_id) ON DELETE CASCADE
```

**Benefit:** When a session is deleted, all related data is automatically removed:

```sql
DELETE FROM chat_sessions WHERE session_id = 'abc-123';
-- Automatically deletes:
--   - All conversation_turns for this session
--   - All personality_states for this session
--   - All performance_metrics for this session
```

**Use Case:** GDPR compliance, user data deletion, cleanup

---

## Entity Relationship Diagram

```
┌─────────────────────────────────────┐
│        chat_sessions                │
│─────────────────────────────────────│
│ PK  session_id (UUID)               │
│     total_turns                     │
│     evaluation_mode                 │
│     baseline_comparison             │
│     status                          │
│     created_at                      │
│     updated_at                      │
└──────────┬──────────────────────────┘
           │
           │ 1:N (one session has many turns/states/metrics)
           │
     ┌─────┴──────┬──────────────┬─────────────────┐
     │            │              │                 │
     ▼            ▼              ▼                 ▼
┌────────┐  ┌────────────┐  ┌───────────┐  ┌──────────┐
│conv    │  │personality │  │performance│  │(future   │
│_turns  │  │_states     │  │_metrics   │  │tables)   │
└────────┘  └────────────┘  └───────────┘  └──────────┘
   │            │                │
   │ FK         │ FK             │ FK
   │ session_id │ session_id     │ session_id
   │            │                │
   │ UNIQUE     │ UNIQUE         │ UNIQUE
   │ (session_id, turn_index)    │ (session_id, turn_index)
   │            │                │
   └────────────┴────────────────┘
        Composite Key Pattern
```

### Relationship Details

**chat_sessions (Parent Table)**
- Primary Key: `session_id` (UUID)
- Child Tables: 3 (conversation_turns, personality_states, performance_metrics)

**conversation_turns (Child Table)**
- Foreign Key: `session_id` → `chat_sessions.session_id`
- Composite Unique: `(session_id, turn_index)`
- Cascade Delete: YES

**personality_states (Child Table)**
- Foreign Key: `session_id` → `chat_sessions.session_id`
- Composite Unique: `(session_id, turn_index)`
- Cascade Delete: YES
- Special: Used for EMA smoothing (read previous state)

**performance_metrics (Child Table)**
- Foreign Key: `session_id` → `chat_sessions.session_id`
- Composite Unique: `(session_id, turn_index)`
- Cascade Delete: YES
- Status: Placeholder for Phase 2

---

## Helper Functions & Views

### 1. `get_latest_personality_state()` Function

**Purpose:** Retrieves the most recent personality state for EMA smoothing.

**Function:**
```sql
CREATE OR REPLACE FUNCTION get_latest_personality_state(p_session_id UUID)
RETURNS TABLE(
    ocean_o FLOAT, ocean_c FLOAT, ocean_e FLOAT, ocean_a FLOAT, ocean_n FLOAT,
    confidence_o FLOAT, confidence_c FLOAT, confidence_e FLOAT, 
    confidence_a FLOAT, confidence_n FLOAT,
    stable BOOLEAN,
    turn_index INTEGER
) AS $$
BEGIN
    RETURN QUERY
    SELECT 
        ps.ocean_o, ps.ocean_c, ps.ocean_e, ps.ocean_a, ps.ocean_n,
        ps.confidence_o, ps.confidence_c, ps.confidence_e, 
        ps.confidence_a, ps.confidence_n,
        ps.stable,
        ps.turn_index
    FROM personality_states ps
    WHERE ps.session_id = p_session_id
    ORDER BY ps.turn_index DESC
    LIMIT 1;
END;
$$ LANGUAGE plpgsql;
```

**Usage in N8N:**
```sql
SELECT * FROM get_latest_personality_state('abc-123-def-456');
```

**Returns:**
- Latest turn's OCEAN values and confidence
- Empty if no previous state (turn 1)

**Performance:** O(log n) with index on (session_id, turn_index)

---

### 2. `get_conversation_history()` Function

**Purpose:** Retrieves recent conversation turns for context.

**Function:**
```sql
CREATE OR REPLACE FUNCTION get_conversation_history(
    p_session_id UUID, 
    p_limit INTEGER DEFAULT 10
)
RETURNS TABLE(
    turn_index INTEGER,
    user_message TEXT,
    assistant_response TEXT,
    created_at TIMESTAMP
) AS $$
BEGIN
    RETURN QUERY
    SELECT 
        ct.turn_index,
        ct.user_message,
        ct.assistant_response,
        ct.created_at
    FROM conversation_turns ct
    WHERE ct.session_id = p_session_id
    ORDER BY ct.turn_index DESC
    LIMIT p_limit;
END;
$$ LANGUAGE plpgsql;
```

**Usage:**
```sql
-- Get last 5 turns
SELECT * FROM get_conversation_history('abc-123', 5);

-- Get all turns
SELECT * FROM get_conversation_history('abc-123', 1000);
```

**Use Case:** Context-aware generation (future enhancement)

---

### 3. `session_summary` View

**Purpose:** Quick overview of active sessions with latest personality state.

**View:**
```sql
CREATE OR REPLACE VIEW session_summary AS
SELECT 
    cs.session_id,
    cs.total_turns,
    cs.evaluation_mode,
    cs.status,
    ps.stable as personality_stable,
    ps.ocean_o, ps.ocean_c, ps.ocean_e, ps.ocean_a, ps.ocean_n,
    cs.created_at,
    cs.updated_at
FROM chat_sessions cs
LEFT JOIN LATERAL (
    SELECT * FROM personality_states 
    WHERE session_id = cs.session_id 
    ORDER BY turn_index DESC 
    LIMIT 1
) ps ON true;
```

**Query:**
```sql
-- All active sessions
SELECT * FROM session_summary WHERE status = 'active';

-- Stable personalities
SELECT * FROM session_summary WHERE personality_stable = true;

-- Long conversations
SELECT * FROM session_summary WHERE total_turns >= 10 ORDER BY total_turns DESC;
```

---

### 4. Trigger: `update_session_timestamp()`

**Purpose:** Auto-update `chat_sessions.updated_at` when new turn is added.

**Function:**
```sql
CREATE OR REPLACE FUNCTION update_session_timestamp()
RETURNS TRIGGER AS $$
BEGIN
    UPDATE chat_sessions 
    SET updated_at = CURRENT_TIMESTAMP 
    WHERE session_id = NEW.session_id;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;
```

**Trigger:**
```sql
CREATE TRIGGER update_session_on_turn
AFTER INSERT ON conversation_turns
FOR EACH ROW
EXECUTE FUNCTION update_session_timestamp();
```

**Behavior:**
- Every time a turn is inserted into `conversation_turns`
- The parent session's `updated_at` timestamp is refreshed
- Keeps session metadata current

---

## Indexes & Performance

### Index Strategy

#### 1. **Primary Keys (Automatic Indexes)**
```sql
-- Automatically created with PRIMARY KEY constraint
chat_sessions.session_id
conversation_turns.id
personality_states.id
performance_metrics.id
```

#### 2. **Foreign Key Indexes**
```sql
-- Speed up JOIN operations
CREATE INDEX idx_turns_session ON conversation_turns(session_id);
CREATE INDEX idx_personality_session ON personality_states(session_id);
CREATE INDEX idx_metrics_session ON performance_metrics(session_id);
```

#### 3. **Composite Unique Indexes**
```sql
-- Automatically created with UNIQUE constraint
UNIQUE(session_id, turn_index) -- on conversation_turns
UNIQUE(session_id, turn_index) -- on personality_states
UNIQUE(session_id, turn_index) -- on performance_metrics
```

#### 4. **Timestamp Indexes**
```sql
-- Enable time-range queries
CREATE INDEX idx_sessions_created ON chat_sessions(created_at);
CREATE INDEX idx_turns_created ON conversation_turns(created_at);
CREATE INDEX idx_personality_created ON personality_states(created_at);
CREATE INDEX idx_metrics_created ON performance_metrics(created_at);
```

#### 5. **Status Indexes**
```sql
-- Filter by session status
CREATE INDEX idx_sessions_status ON chat_sessions(status);

-- Filter by personality stability
CREATE INDEX idx_personality_stable ON personality_states(stable);
```

---

### Query Performance

#### Typical Query Patterns

**1. Load Previous State (Most Frequent)**
```sql
SELECT * FROM get_latest_personality_state('session-uuid');
```
**Complexity:** O(log n)  
**Index Used:** `idx_personality_session` + composite unique index  
**Typical Time:** < 5ms

**2. Save Turn (Frequent)**
```sql
INSERT INTO conversation_turns (...) ON CONFLICT (...) DO UPDATE;
```
**Complexity:** O(log n) for conflict check  
**Index Used:** Composite unique index on (session_id, turn_index)  
**Typical Time:** < 10ms

**3. Session Summary (Dashboard)**
```sql
SELECT * FROM session_summary WHERE status = 'active';
```
**Complexity:** O(n) for session scan, O(log n) per session for latest personality  
**Index Used:** `idx_sessions_status`, `idx_personality_session`  
**Typical Time:** < 50ms for 1000 sessions

---

### Optimization Strategies

#### 1. **Partitioning (Future)**

For high-volume production:
```sql
-- Partition conversation_turns by month
CREATE TABLE conversation_turns_2025_10 PARTITION OF conversation_turns
FOR VALUES FROM ('2025-10-01') TO ('2025-11-01');
```

#### 2. **Materialized Views**

For analytics:
```sql
CREATE MATERIALIZED VIEW daily_personality_stats AS
SELECT 
    DATE(created_at) as date,
    COUNT(DISTINCT session_id) as unique_sessions,
    AVG(ocean_o) as avg_openness,
    AVG(ocean_c) as avg_conscientiousness,
    COUNT(*) FILTER (WHERE stable = true) as stable_count
FROM personality_states
GROUP BY DATE(created_at);

-- Refresh daily
REFRESH MATERIALIZED VIEW daily_personality_stats;
```

#### 3. **Connection Pooling**

N8N PostgreSQL nodes should use connection pooling:
- Max connections: 20-50
- Idle timeout: 30 seconds
- Reuse connections across workflow executions

---

## Integration with N8N Workflow

### Node Mapping

| N8N Node | Table | Operation | Timing |
|----------|-------|-----------|--------|
| Load Previous State (PostgreSQL) | `personality_states` | SELECT (via function) | Early (turn start) |
| Save Session (PostgreSQL) | `chat_sessions` | INSERT/UPDATE | Late (after verification) |
| Save Conversation Turn (PostgreSQL) | `conversation_turns` | INSERT/UPDATE | Late (parallel) |
| Save Personality State (PostgreSQL) | `personality_states` | INSERT/UPDATE | Late (parallel) |

### Execution Order

```
1. Enhanced Ingest → Extract session_id
2. Load Previous State → READ from personality_states
3. Combine Inputs → Merge DB data with workflow data
4. Merge Previous State → Attach previous_state to payload
5. Zurich Model Detection → Use previous_state for EMA
6. ... (regulation, generation, verification) ...
7. PARALLEL WRITES:
   ├─ Save Session
   ├─ Save Conversation Turn
   └─ Save Personality State
8. Merge DB Results → Confirm all saves succeeded
```

### Data Dependencies

**Save Session depends on:**
- `session_id` (from Enhanced Ingest)
- `turn_index` (from Enhanced Ingest)
- `evaluation_mode` (from input)

**Save Conversation Turn depends on:**
- `session_id` (from Enhanced Ingest)
- `turn_index` (from Enhanced Ingest)
- `clean_msg` (from Enhanced Ingest)
- `verifier.verified_response` (from Verification node)
- `directives` (from Regulation node)
- `verifier.verification_status` (from Verification node)
- `verifier.adherence_score` (from Verification node)

**Save Personality State depends on:**
- `session_id` (from Enhanced Ingest)
- `turn_index` (from Enhanced Ingest)
- `detector.smoothed_ocean.*` (from Detection node)
- `detector.smoothed_confidence.*` (from Detection node)
- `detector.personality_stable` (from Detection node)
- `detector.ema_applied` (from Detection node)

---

## EMA Smoothing Integration

### Database Role in EMA

The database is **critical** for EMA (Exponential Moving Average) smoothing because:

1. **Persistence:** Stores previous OCEAN values across sessions
2. **Continuity:** Enables multi-turn conversations with state
3. **Retrieval:** Provides `get_latest_personality_state()` function
4. **History:** Tracks personality evolution over time

### EMA Flow with Database

```
Turn N:
  1. Load Previous State → DB READ
     get_latest_personality_state(session_id)
     Returns: Turn N-1 OCEAN values
  
  2. Zurich Model Detection
     Raw detection: {O: 0.5, C: -0.3, ...}
     Previous state: {O: 0.3, C: -0.5, ...}
     
     EMA formula: smoothed = α * current + (1-α) * previous
     
     smoothed.O = 0.3 * 0.5 + 0.7 * 0.3 = 0.36
     smoothed.C = 0.3 * (-0.3) + 0.7 * (-0.5) = -0.44
  
  3. Save Personality State → DB WRITE
     INSERT turn N with smoothed values
     Next turn will use these as "previous"
```

### Stability Tracking

```sql
-- Check if personality has stabilized
SELECT 
    session_id,
    turn_index,
    stable,
    ocean_o, ocean_c, ocean_e, ocean_a, ocean_n
FROM personality_states
WHERE session_id = 'some-uuid'
ORDER BY turn_index;

-- Result shows progression:
-- turn_index | stable | ocean_o | ocean_c | ...
-- -----------|--------|---------|---------|
--     1      | false  |  0.30   |  -0.50  |
--     2      | false  |  0.36   |  -0.44  | <- EMA applied
--     3      | false  |  0.39   |  -0.41  |
--     4      | false  |  0.42   |  -0.38  |
--     5      | true   |  0.44   |  -0.35  | <- Stable!
```

**Stability Criteria:**
- `turn_index >= 5`
- All confidence scores >= 0.6
- Marked with `stable = true` in database

---

## Usage Examples

### Example 1: Create New Session

```sql
-- Initial session creation (handled by N8N workflow)
INSERT INTO chat_sessions (session_id, total_turns, evaluation_mode, status)
VALUES ('550e8400-e29b-41d4-a716-446655440000', 1, false, 'active')
ON CONFLICT (session_id) DO UPDATE SET total_turns = 1;

-- Save first turn
INSERT INTO conversation_turns (
    session_id, turn_index, user_message, assistant_response,
    directives_applied, verification_status, adherence_score
) VALUES (
    '550e8400-e29b-41d4-a716-446655440000',
    1,
    'I feel overwhelmed with work.',
    'I understand you''re feeling overwhelmed. Let''s break this down together.',
    '["Offer extra comfort; acknowledge anxieties"]'::jsonb,
    'verified',
    0.85
);

-- Save first personality state
INSERT INTO personality_states (
    session_id, turn_index,
    ocean_o, ocean_c, ocean_e, ocean_a, ocean_n,
    confidence_o, confidence_c, confidence_e, confidence_a, confidence_n,
    stable, ema_applied
) VALUES (
    '550e8400-e29b-41d4-a716-446655440000',
    1,
    0.3, -0.5, 0.7, 0.2, -0.3,  -- OCEAN values
    0.8, 0.7, 0.9, 0.6, 0.5,    -- Confidence values
    false, false  -- Not stable yet, no EMA on turn 1
);
```

---

### Example 2: Query Session History

```sql
-- Get full conversation
SELECT 
    turn_index,
    user_message,
    assistant_response,
    directives_applied,
    verification_status
FROM conversation_turns
WHERE session_id = '550e8400-e29b-41d4-a716-446655440000'
ORDER BY turn_index ASC;

-- Get personality evolution
SELECT 
    turn_index,
    ocean_o AS openness,
    ocean_c AS conscientiousness,
    ocean_e AS extraversion,
    ocean_a AS agreeableness,
    ocean_n AS neuroticism,
    stable,
    ema_applied
FROM personality_states
WHERE session_id = '550e8400-e29b-41d4-a716-446655440000'
ORDER BY turn_index ASC;
```

---

### Example 3: Analytics Queries

```sql
-- Average personality traits across all stable sessions
SELECT 
    AVG(ocean_o) as avg_openness,
    AVG(ocean_c) as avg_conscientiousness,
    AVG(ocean_e) as avg_extraversion,
    AVG(ocean_a) as avg_agreeableness,
    AVG(ocean_n) as avg_neuroticism
FROM personality_states
WHERE stable = true;

-- Sessions that reached stability
SELECT 
    session_id,
    MIN(turn_index) as first_stable_turn
FROM personality_states
WHERE stable = true
GROUP BY session_id
ORDER BY first_stable_turn ASC;

-- Most common directives used
SELECT 
    directive,
    COUNT(*) as usage_count
FROM conversation_turns,
     jsonb_array_elements_text(directives_applied) as directive
GROUP BY directive
ORDER BY usage_count DESC
LIMIT 10;

-- Average adherence scores over time
SELECT 
    DATE(created_at) as date,
    AVG(adherence_score) as avg_score,
    COUNT(*) as turn_count
FROM conversation_turns
WHERE verification_status = 'verified'
GROUP BY DATE(created_at)
ORDER BY date DESC;
```

---

### Example 4: Session Cleanup

```sql
-- Delete old inactive sessions (GDPR compliance)
DELETE FROM chat_sessions
WHERE status = 'inactive' 
  AND updated_at < NOW() - INTERVAL '90 days';
-- This CASCADE deletes all related turns, personality states, and metrics

-- Archive old sessions (before deleting)
INSERT INTO chat_sessions_archive
SELECT * FROM chat_sessions
WHERE updated_at < NOW() - INTERVAL '90 days';
```

---

## Maintenance & Optimization

### Regular Maintenance Tasks

#### 1. **VACUUM and ANALYZE**

```sql
-- Weekly: Reclaim space and update statistics
VACUUM ANALYZE chat_sessions;
VACUUM ANALYZE conversation_turns;
VACUUM ANALYZE personality_states;
VACUUM ANALYZE performance_metrics;
```

#### 2. **Reindex**

```sql
-- Monthly: Rebuild indexes for optimal performance
REINDEX TABLE conversation_turns;
REINDEX TABLE personality_states;
```

#### 3. **Statistics**

```sql
-- Check table sizes
SELECT 
    schemaname,
    tablename,
    pg_size_pretty(pg_total_relation_size(schemaname||'.'||tablename)) AS size
FROM pg_tables
WHERE schemaname = 'public'
ORDER BY pg_total_relation_size(schemaname||'.'||tablename) DESC;

-- Check index usage
SELECT 
    schemaname,
    tablename,
    indexname,
    idx_scan as index_scans,
    idx_tup_read as tuples_read,
    idx_tup_fetch as tuples_fetched
FROM pg_stat_user_indexes
WHERE schemaname = 'public'
ORDER BY idx_scan DESC;
```

---

### Backup Strategy

```bash
# Daily backup
pg_dump -h localhost -U postgres -d personality_chat_db \
  -F c -b -v -f "backup_$(date +%Y%m%d).dump"

# Backup schema only
pg_dump -h localhost -U postgres -d personality_chat_db \
  --schema-only -f schema_backup.sql

# Restore from backup
pg_restore -h localhost -U postgres -d personality_chat_db \
  -v backup_20251001.dump
```

---

### Monitoring Queries

```sql
-- Active sessions in last 24 hours
SELECT COUNT(DISTINCT session_id) as active_sessions
FROM chat_sessions
WHERE updated_at > NOW() - INTERVAL '24 hours';

-- Total turns processed today
SELECT COUNT(*) as turns_today
FROM conversation_turns
WHERE created_at::date = CURRENT_DATE;

-- Average turns per session
SELECT AVG(total_turns) as avg_turns_per_session
FROM chat_sessions
WHERE status = 'active';

-- Stable personality percentage
SELECT 
    COUNT(*) FILTER (WHERE stable = true) * 100.0 / COUNT(*) as stable_percentage
FROM (
    SELECT DISTINCT ON (session_id) stable
    FROM personality_states
    ORDER BY session_id, turn_index DESC
) latest_states;
```

---

## Summary

### Key Takeaways

1. **4 Tables, 4 Concerns:**
   - `chat_sessions` → Session metadata
   - `conversation_turns` → Conversation history
   - `personality_states` → EMA smoothing continuity ⭐
   - `performance_metrics` → Pipeline monitoring (Phase 2)

2. **EMA Database Integration:**
   - Read previous state at turn start
   - Calculate smoothed values in N8N
   - Save smoothed state for next turn
   - Database enables multi-turn continuity

3. **N8N Integration:**
   - 1 read node (Load Previous State)
   - 3 write nodes (Save Session, Turn, Personality State)
   - Parallel writes for performance
   - UPSERT pattern for idempotency

4. **Design Principles:**
   - **Normalization:** Separate tables for separate concerns
   - **ACID Compliance:** Reliable transactional operations
   - **Cascade Deletes:** Automatic cleanup
   - **Optimized Indexes:** Fast queries on common patterns
   - **Helper Functions:** Abstraction for complex queries

5. **Performance:**
   - Indexed foreign keys for fast JOINs
   - Composite unique constraints for data integrity
   - Materialized views for analytics (future)
   - Connection pooling for scalability

---

## Next Steps

**Phase 2 Enhancements:**
- [ ] Populate `performance_metrics` automatically
- [ ] Add `emotional_state` detection and storage
- [ ] Implement table partitioning for high volume
- [ ] Create analytics dashboard queries
- [ ] Add A/B testing support tables
- [ ] Implement audit logging

**Documentation:**
- [x] Database Schema ✅
- [x] Data Flow ✅
- [x] EMA Integration ✅
- [ ] Performance Tuning Guide (future)
- [ ] Migration Scripts (future)

---

**Document Version:** 1.0  
**Last Updated:** October 1, 2025  
**Maintained By:** Phase 1 Development Team









































