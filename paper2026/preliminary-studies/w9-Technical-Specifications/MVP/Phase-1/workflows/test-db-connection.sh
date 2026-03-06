#!/bin/bash
echo "╔═══════════════════════════════════════════════════════════════╗"
echo "║  🧪 TESTING POSTGRESQL CONNECTION                            ║"
echo "╚═══════════════════════════════════════════════════════════════╝"
echo ""
echo "Testing connection with credentials you'll use in N8N..."
echo ""
echo "Host: postgres"
echo "Database: personality_chat"
echo "User: n8n_user"
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# Test connection
docker exec mvp-postgres-1 psql -U n8n_user -d personality_chat -c "SELECT 'Connection successful! ✅' as status;" 2>&1 | head -4

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "Testing tables..."
docker exec mvp-postgres-1 psql -U n8n_user -d personality_chat -c "SELECT table_name FROM information_schema.tables WHERE table_schema='public' ORDER BY table_name;" 2>&1 | grep -E "table_name|---|chat_sessions|conversation_turns|personality_states|performance_metrics"

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "Testing helper function..."
docker exec mvp-postgres-1 psql -U n8n_user -d personality_chat -c "SELECT * FROM get_conversation_history('test-session', 5);" 2>&1 | head -4

echo ""
echo "✅ If you see output above with no errors, your database is ready!"
echo "✅ Use these credentials in N8N: see N8N-CREDENTIALS.txt"
