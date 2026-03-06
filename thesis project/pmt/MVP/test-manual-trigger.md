# Testing Manual Trigger - PostgreSQL Workflow

## ✅ **Database Setup Complete**

The following tables have been created successfully:
- ✅ `chat_sessions` - Session management
- ✅ `conversation_turns` - Message history
- ✅ `personality_states` - OCEAN personality tracking
- ✅ `performance_metrics` - Pipeline performance data

## 📋 **Next Steps**

### 1. Import the Fixed Workflow
1. Go to N8N: http://localhost:5678
2. Click **Import from File**
3. Select: `Phase-1/workflows/phase1-2-postgres-manual.json`
4. Click **Import**

### 2. Configure PostgreSQL Credentials
1. In the workflow, find the 4 PostgreSQL nodes:
   - **Load Previous State (PostgreSQL)**
   - **Save Session (PostgreSQL)**
   - **Save Conversation Turn (PostgreSQL)**
   - **Save Personality State (PostgreSQL)**

2. For each node, configure the credential:
   - **Host**: `mvp-postgres-1`
   - **Port**: `5432`
   - **Database**: `n8n_personality_ai`
   - **User**: `n8n_user`
   - **Password**: `n8n_password`
   - **Credential Name**: `personality-chat-db`

### 3. Test the Manual Trigger
1. Click **Test workflow** button in N8N
2. The workflow should execute successfully
3. Check for:
   - ✅ Real OCEAN values (not all zeros)
   - ✅ `pipeline_status` showing "success" for all components
   - ✅ Database records created

### 4. Verify Database Records
Run this command to check if data was saved:

```bash
docker exec -i mvp-postgres-1 psql -U n8n_user -d n8n_personality_ai -c "
SELECT 
    cs.session_id, 
    cs.total_turns, 
    ps.stable,
    ps.ocean_o, ps.ocean_c, ps.ocean_e, ps.ocean_a, ps.ocean_n
FROM chat_sessions cs
LEFT JOIN personality_states ps ON cs.session_id = ps.session_id
ORDER BY cs.created_at DESC
LIMIT 5;"
```

### 5. Activate for Webhook Testing
1. Toggle the workflow to **Active**
2. Test via webhook:

```bash
curl -X POST http://localhost:5678/webhook/personality-chat-enhanced \
  -H "Content-Type: application/json" \
  -d '{"message":"I feel overwhelmed and anxious about work deadlines"}'
```

## 🎯 **Expected Results**

The workflow should:
1. ✅ Load previous state from PostgreSQL (or start fresh)
2. ✅ Detect personality traits from the message
3. ✅ Apply EMA smoothing if previous state exists
4. ✅ Generate personalized response
5. ✅ Save all data to PostgreSQL tables
6. ✅ Return JSON with real OCEAN values and pipeline statuses

## 🔍 **Troubleshooting**

If you still see errors:
1. **Credential errors**: Double-check the PostgreSQL credentials match exactly
2. **Connection errors**: Ensure Docker containers are all running (`docker ps`)
3. **Empty OCEAN values**: Check that the OpenAI API key is configured in N8N
4. **Database errors**: Verify schema exists (`\dt` in psql)









































