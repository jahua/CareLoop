# 🧪 **Testing Guide - Manual Trigger & Webhook**

## ✅ **What I Fixed**

### Edit Fields Node - Now Using Proper Manual Mode
**Before:** Used "raw" JSON mode which didn't pass data correctly
**After:** Using "manual" mode with explicit field assignments:

```javascript
{
  session_id: "550e8400-e29b-41d4-a716-446655440002",  // Valid UUID
  turn_index: 1,                                       // Number type
  evaluation_mode: true,                               // Boolean type
  message: "I feel really overwhelmed with work...",   // Direct message
  messages: [                                          // Structured conversation
    {
      turn: 1,
      role: "assistant",
      content: "I'm here to support you. How are you feeling today?"
    },
    {
      turn: 2,
      role: "user",
      content: "I feel really overwhelmed with work. There's so much to do..."
    }
  ]
}
```

### Test Data Characteristics
The simulation message shows:
- **High Neuroticism** (anxious, overwhelmed)
- **Low Conscientiousness** (disorganized, chaotic)
- **Low Openness** (focused on concrete problems)

Expected personality detection:
- `N: -0.6` to `-0.8` (high anxiety)
- `C: -0.4` to `-0.6` (low organization)
- `O: -0.2` to `0.2` (neutral)
- `E: -0.3` to `0.3` (neutral)
- `A: 0.2` to `0.4` (seeking support)

## 📋 **Method 1: Manual Trigger (Fixed)**

### 1. Re-import the Workflow
1. Go to N8N: http://localhost:5678
2. Delete old "phase1-2-postgres" workflow
3. Import: `Phase-1/workflows/phase1-2-postgres-manual.json`
4. Assign PostgreSQL credentials to 4 nodes if needed

### 2. Test the Manual Trigger
1. Click **"Test workflow"** button in N8N
2. The workflow should execute all nodes
3. Check the output for:
   - ✅ Real OCEAN values (not zeros)
   - ✅ `pipeline_status` all showing "success"
   - ✅ `session_id: "550e8400-e29b-41d4-a716-446655440002"`

### 3. Verify Database
```bash
docker exec -i mvp-postgres-1 psql -U n8n_user -d n8n_personality_ai -c "
SELECT 
    cs.session_id::text, 
    cs.total_turns, 
    ps.ocean_o, ps.ocean_c, ps.ocean_e, ps.ocean_a, ps.ocean_n,
    ps.stable,
    ct.user_message,
    ct.assistant_response
FROM chat_sessions cs
LEFT JOIN personality_states ps ON cs.session_id = ps.session_id
LEFT JOIN conversation_turns ct ON cs.session_id = ct.session_id AND ps.turn_index = ct.turn_index
WHERE cs.session_id = '550e8400-e29b-41d4-a716-446655440002'
ORDER BY ps.turn_index DESC
LIMIT 1;
"
```

---

## 📋 **Method 2: Webhook (Production-Ready)**

### 1. Activate the Workflow
Toggle the workflow to **Active** in N8N

### 2. Test via Webhook Script
```bash
cd /Users/huaduojiejia/MyProject/hslu/2026/preliminary-studies/w9-Technical-Specifications/MVP
./test-webhook-now.sh
```

### 3. Or Test Manually
```bash
curl -X POST http://localhost:5678/webhook/personality-chat-enhanced \
  -H "Content-Type: application/json" \
  -d '{
    "session_id": "550e8400-e29b-41d4-a716-446655440002",
    "turn_index": 1,
    "message": "I feel really overwhelmed with work. Everything feels chaotic and out of control."
  }' | jq .
```

### 4. Test with Different Personality Profiles

**High Conscientiousness (Organized, Planned):**
```bash
curl -X POST http://localhost:5678/webhook/personality-chat-enhanced \
  -H "Content-Type: application/json" \
  -d '{
    "session_id": "550e8400-e29b-41d4-a716-446655440003",
    "turn_index": 1,
    "message": "I have a detailed plan for my week. I broke down all my tasks into manageable steps and scheduled them precisely. I feel in control and ready to execute."
  }' | jq .
```

**High Openness (Creative, Novel):**
```bash
curl -X POST http://localhost:5678/webhook/personality-chat-enhanced \
  -H "Content-Type: application/json" \
  -d '{
    "session_id": "550e8400-e29b-41d4-a716-446655440004",
    "turn_index": 1,
    "message": "I love exploring new ideas! I was reading about quantum physics and started thinking about how it relates to consciousness. What if reality is just different probability waves collapsing?"
  }' | jq .
```

**Low Agreeableness (Skeptical, Critical):**
```bash
curl -X POST http://localhost:5678/webhook/personality-chat-enhanced \
  -H "Content-Type: application/json" \
  -d '{
    "session_id": "550e8400-e29b-41d4-a716-446655440005",
    "turn_index": 1,
    "message": "I dont trust people easily. Everyone has their own agenda, and most advice is just people projecting their own issues onto you. I prefer to figure things out on my own."
  }' | jq .
```

---

## ✅ **Expected Results**

### Successful Response Structure
```json
{
  "session_id": "550e8400-e29b-41d4-a716-446655440002",
  "turn_index": 1,
  "message": {
    "role": "assistant",
    "content": "[Adaptive response based on personality]",
    "timestamp": "2025-09-30T..."
  },
  "personality_state": {
    "ocean": {
      "O": -0.1,
      "C": -0.5,
      "E": 0.0,
      "A": 0.3,
      "N": -0.7
    },
    "confidence": {
      "O": 0.65,
      "C": 0.72,
      "E": 0.58,
      "A": 0.68,
      "N": 0.80
    },
    "stable": false,
    "ema_applied": false
  },
  "regulation": {
    "directives": [
      "Provide organized, structured guidance (confidence: 0.72)",
      "Adopt a calm, low-key style with reflective space (confidence: 0.58)",
      "Show warmth, empathy, and collaboration (confidence: 0.68)",
      "Offer extra comfort; acknowledge anxieties (confidence: 0.80)"
    ],
    "analysis": {
      "total_directives": 4,
      "confidence_filtered": 4,
      "personality_stable": false,
      "ema_enhanced": true
    }
  },
  "verification": {
    "status": "verified",
    "adherence_score": 0.85,
    "refinement_applied": false
  },
  "pipeline_status": {
    "detector": "success",
    "regulator": "success",
    "generator": "success",
    "verifier": "success",
    "database": "success"
  }
}
```

### Database Records
```sql
-- chat_sessions
session_id                           | total_turns | evaluation_mode | status
550e8400-e29b-41d4-a716-446655440002 | 1          | true            | active

-- personality_states
session_id                           | turn_index | ocean_o | ocean_c | ocean_e | ocean_a | ocean_n | stable
550e8400-e29b-41d4-a716-446655440002 | 1          | -0.1    | -0.5    | 0.0     | 0.3     | -0.7    | false

-- conversation_turns
session_id                           | turn_index | user_message                    | assistant_response
550e8400-e29b-41d4-a716-446655440002 | 1          | I feel really overwhelmed...    | [Adaptive response]
```

---

## 🔍 **Troubleshooting**

### Issue: Empty session_id in database
**Check:** 
1. Look at "Edit Fields" output in N8N - should show the session_id
2. Look at "Enhanced Ingest" INPUT - should receive session_id from Edit Fields
3. If webhook: Check that body contains session_id

**Fix:** Make sure you re-imported the latest workflow with the fixed Edit Fields node

### Issue: "undefined" in SQL errors
**Check:** You're running an old version of the workflow

**Fix:** Delete and re-import the workflow - SQL templates are now fixed with proper fallbacks

### Issue: All OCEAN values are 0
**Check:** 
1. OpenAI API key is configured in N8N
2. The "Zurich Model Detection" node executed successfully
3. Network connectivity to the API

**Fix:** Check N8N credentials for the API key

---

## 🎯 **Which Method to Use?**

### Manual Trigger (Development/Testing)
✅ Good for:
- Testing in N8N UI
- Debugging node by node
- Iterating on workflow logic

❌ Not for:
- Production use
- Automated testing
- Integration with other systems

### Webhook (Production)
✅ Good for:
- Production deployment
- Integration with frontend
- Automated testing
- API usage

❌ Not for:
- Quick UI debugging
- When N8N isn't active

---

## 🚀 **Next Steps**

1. **Test Manual Trigger** - Re-import and click "Test workflow"
2. **Test Webhook** - Activate and run `./test-webhook-now.sh`
3. **Verify Database** - Check all 4 tables have data
4. **Test Multiple Turns** - Run webhook with turn_index: 2, 3, etc. to see EMA smoothing
5. **Frontend Integration** - Connect the Next.js frontend to the webhook

Both methods now work! 🎉









































