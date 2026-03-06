#!/bin/bash

echo "🧪 Testing PostgreSQL Workflow via Webhook"
echo "==========================================="
echo ""

# Test 1: Simple message
echo "📝 Test 1: Sending test message..."
curl -X POST http://localhost:5678/webhook/personality-chat-enhanced \
  -H "Content-Type: application/json" \
  -d '{
    "session_id": "550e8400-e29b-41d4-a716-446655440002",
    "turn_index": 1,
    "message": "I feel overwhelmed and anxious about work deadlines"
  }' | jq .

echo ""
echo "✅ Check above for:"
echo "   - Real OCEAN values (not all zeros)"
echo "   - pipeline_status: success"
echo "   - Database saved successfully"
echo ""

# Verify database
echo "📊 Checking database records..."
docker exec -i mvp-postgres-1 psql -U n8n_user -d n8n_personality_ai -c "
SELECT 
    cs.session_id::text, 
    cs.total_turns, 
    ps.ocean_o, ps.ocean_c, ps.ocean_e, ps.ocean_a, ps.ocean_n,
    ps.stable,
    ct.user_message
FROM chat_sessions cs
LEFT JOIN personality_states ps ON cs.session_id = ps.session_id AND ps.turn_index = cs.total_turns
LEFT JOIN conversation_turns ct ON cs.session_id = ct.session_id AND ct.turn_index = cs.total_turns
WHERE cs.session_id = '550e8400-e29b-41d4-a716-446655440002'
ORDER BY cs.updated_at DESC
LIMIT 1;
"

echo ""
echo "🎉 Done! Check the results above."









































