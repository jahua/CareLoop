#!/bin/bash

echo "🧪 Testing PostgreSQL Workflow - Properly Formatted"
echo "===================================================="
echo ""

# Test 1: Simple overwhelmed message
echo "📝 Test 1: Overwhelmed user (High Neuroticism)"
curl -s -X POST http://localhost:5678/webhook/personality-chat-enhanced \
  -H "Content-Type: application/json" \
  -d '{
    "session_id": "550e8400-e29b-41d4-a716-446655440002",
    "turn_index": 1,
    "message": "I feel really overwhelmed with work. Everything feels chaotic and out of control."
  }' | jq '{
    session_id,
    reply,
    personality_state: {
      ocean,
      stable,
      ema_applied
    },
    regulation: {
      directives
    },
    pipeline_status
  }'

echo ""
echo "---"
echo ""

# Test 2: Skeptical/resistant message
echo "📝 Test 2: Skeptical user (Low Agreeableness)"
curl -s -X POST http://localhost:5678/webhook/personality-chat-enhanced \
  -H "Content-Type: application/json" \
  -d '{
    "session_id": "550e8400-e29b-41d4-a716-446655440003",
    "turn_index": 1,
    "message": "I mean, I appreciate you saying that, but I still do not really buy it. Like, everyone says they care or that it is okay to talk, but it always turns into some lecture or fake comfort or worse nothing. Just silence."
  }' | jq '{
    session_id,
    reply,
    personality_state: {
      ocean,
      stable,
      ema_applied
    },
    regulation: {
      directives
    },
    pipeline_status
  }'

echo ""
echo "---"
echo ""

# Check database
echo "📊 Checking database records..."
docker exec -i mvp-postgres-1 psql -U n8n_user -d n8n_personality_ai -c "
SELECT 
    cs.session_id::text, 
    cs.total_turns,
    ps.ocean_o, ps.ocean_c, ps.ocean_e, ps.ocean_a, ps.ocean_n,
    ps.stable,
    ct.user_message
FROM chat_sessions cs
LEFT JOIN personality_states ps ON cs.session_id = ps.session_id
LEFT JOIN conversation_turns ct ON cs.session_id = ct.session_id
WHERE cs.session_id IN ('550e8400-e29b-41d4-a716-446655440002', '550e8400-e29b-41d4-a716-446655440003')
ORDER BY cs.created_at DESC
LIMIT 5;
"

echo ""
echo "✅ Tests complete!"









































