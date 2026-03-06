# ✅ **PostgreSQL SQL Template Fixes**

## 🐛 **Issues Fixed**

### Problem
N8N template expressions like `{{ $json.turn_index }}` were outputting the literal string `"undefined"` when the field was missing, causing PostgreSQL syntax errors:
- `column "undefined" does not exist`
- `invalid input syntax for type uuid: "eval-002"`

### Root Cause
N8N's template engine doesn't convert JavaScript `undefined` to SQL `NULL`. It outputs "undefined" as a literal string.

## 🔧 **Solutions Applied**

### 1. Save Session (PostgreSQL) Node
**Before:**
```sql
VALUES ('{{ $json.session_id }}', {{ $json.turn_index }}, {{ $json.evaluation_mode || false }}, 'active')
```

**After:**
```sql
VALUES ('{{ $json.session_id }}', {{ $json.turn_index || 1 }}, {{ $json.evaluation_mode ? 'true' : 'false' }}, 'active')
```

**Changes:**
- `{{ $json.turn_index || 1 }}` - Defaults to 1 if undefined
- `{{ $json.evaluation_mode ? 'true' : 'false' }}` - Outputs proper boolean literals

---

### 2. Save Conversation Turn (PostgreSQL) Node
**Before:**
```sql
VALUES (
  '{{ $json.session_id }}',
  {{ $json.turn_index }},
  {{ $json.clean_msg ? JSON.stringify($json.clean_msg) : '\\'\\'' }},
  {{ $json.verifier?.verified_response ? JSON.stringify($json.verifier.verified_response) : '\\'\\'' }},
  ...
)
```

**After:**
```sql
VALUES (
  '{{ $json.session_id }}',
  {{ $json.turn_index || 1 }},
  '{{ $json.clean_msg || "" }}',
  '{{ $json.verifier?.verified_response || $json.generator?.raw_content || "" }}',
  ...
)
```

**Changes:**
- `{{ $json.turn_index || 1 }}` - Defaults to 1
- `'{{ $json.clean_msg || "" }}'` - Simplified string handling with default
- `'{{ $json.verifier?.verified_response || $json.generator?.raw_content || "" }}'` - Fallback chain for response content

---

### 3. Save Personality State (PostgreSQL) Node
**Before:**
```sql
INSERT INTO personality_states (
  session_id, turn_index,
  ocean_o, ocean_c, ocean_e, ocean_a, ocean_n,
  raw_ocean_o, raw_ocean_c, raw_ocean_e, raw_ocean_a, raw_ocean_n,
  confidence_o, confidence_c, confidence_e, confidence_a, confidence_n,
  personality_stable, ema_applied, ema_alpha,
  evidence_quotes, detection_confidence
) VALUES (
  '{{ $json.session_id }}',
  {{ $json.turn_index }},
  {{ $json.detector?.smoothed_ocean?.O || 0 }},
  ...
  {{ $json.detector?.personality_stable || false }},
  {{ $json.detector?.ema_applied || false }},
  ...
)
```

**After:**
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
  ...
  {{ $json.detector?.personality_stable ? 'true' : 'false' }},
  {{ $json.detector?.ema_applied ? 'true' : 'false' }}
)
```

**Changes:**
- Removed non-existent columns (`raw_ocean_*`, `ema_alpha`, `evidence_quotes`, `detection_confidence`)
- Used correct column names from schema (`stable` instead of `personality_stable`)
- `{{ $json.turn_index || 1 }}` - Defaults to 1
- `{{ ... ? 'true' : 'false' }}` - Proper boolean literals

---

### 4. Load Previous State (PostgreSQL) Node
**Added:**
```json
{
  "alwaysOutputData": true,
  "executeOnce": false
}
```

**Purpose:**
- Ensures workflow continues even when query returns 0 rows (new sessions)
- Critical for handling first-time users without previous personality state

---

### 5. Edit Fields (Manual Trigger Input)
**Before:**
```json
{
  "session_id": "eval-002",
  ...
}
```

**After:**
```json
{
  "session_id": "550e8400-e29b-41d4-a716-446655440002",
  ...
}
```

**Changes:**
- Valid UUID format required for PostgreSQL UUID column type

---

## 📊 **Database Schema Match**

The fixes now properly match the actual PostgreSQL schema:

```sql
CREATE TABLE chat_sessions (
    session_id UUID PRIMARY KEY,
    total_turns INTEGER DEFAULT 0,
    evaluation_mode BOOLEAN DEFAULT FALSE,
    status VARCHAR(20) DEFAULT 'active',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE conversation_turns (
    id SERIAL PRIMARY KEY,
    session_id UUID REFERENCES chat_sessions(session_id),
    turn_index INTEGER NOT NULL,
    user_message TEXT,
    assistant_response TEXT,
    directives_applied JSONB DEFAULT '[]',
    verification_status VARCHAR(20),
    adherence_score FLOAT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(session_id, turn_index)
);

CREATE TABLE personality_states (
    id SERIAL PRIMARY KEY,
    session_id UUID REFERENCES chat_sessions(session_id),
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

---

## ✅ **Testing the Fixes**

### 1. Re-import the Workflow
```bash
# In N8N UI:
# 1. Delete old "phase1-2-postgres" workflow
# 2. Import Phase-1/workflows/phase1-2-postgres-manual.json
# 3. Credentials should auto-assign if saved
```

### 2. Test Manual Trigger
Click **"Test workflow"** in N8N - should now complete successfully!

### 3. Verify Database Records
```bash
docker exec -i mvp-postgres-1 psql -U n8n_user -d n8n_personality_ai -c "
SELECT 
    cs.session_id::text, 
    cs.total_turns, 
    cs.evaluation_mode,
    ps.ocean_o, ps.ocean_c, ps.ocean_e, ps.ocean_a, ps.ocean_n,
    ps.stable,
    ps.ema_applied,
    ct.user_message,
    ct.assistant_response
FROM chat_sessions cs
LEFT JOIN personality_states ps ON cs.session_id = ps.session_id
LEFT JOIN conversation_turns ct ON cs.session_id = ct.session_id AND ps.turn_index = ct.turn_index
WHERE cs.session_id = '550e8400-e29b-41d4-a716-446655440002'
ORDER BY ps.turn_index DESC
LIMIT 1;"
```

Expected output:
- ✅ Valid UUID in `session_id`
- ✅ Integer in `total_turns` (not "undefined")
- ✅ Boolean in `evaluation_mode` (true/false, not "undefined")
- ✅ Float values in OCEAN columns
- ✅ Text content in messages

---

## 🎯 **Key Lessons**

1. **Always use fallback values** in N8N templates: `{{ $json.field || defaultValue }}`
2. **Use ternary for booleans**: `{{ $json.field ? 'true' : 'false' }}` instead of `{{ $json.field || false }}`
3. **Match SQL columns exactly** to the actual database schema
4. **Use `alwaysOutputData: true`** for optional database lookups
5. **Test with empty/new sessions** to catch missing field errors early

---

## 🚀 **Status**

All PostgreSQL SQL template errors are now fixed! The workflow should run end-to-end successfully.









































