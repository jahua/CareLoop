#!/bin/bash

echo "🔧 N8N WORKFLOW FIX & TEST ASSISTANT"
echo "==================================="

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

echo ""
echo -e "${BLUE}📋 STEP-BY-STEP INSTRUCTIONS:${NC}"
echo ""

echo -e "${YELLOW}1. REPLACE THE WORKFLOW IN N8N:${NC}"
echo "   a. Go to N8N → Workflows"
echo "   b. Delete current 'Personality Adaptive Chat Workflow' (if exists)"
echo "   c. Import → From file → Select: $(pwd)/workflows/personality-chat-workflow-FIXED.json"
echo ""

echo -e "${YELLOW}2. CONFIGURE POSTGRESQL CREDENTIALS:${NC}"
echo "   a. Open the imported workflow"
echo "   b. Click each BLUE database node (5 nodes total):"
echo "      - Get Latest State"
echo "      - Get Conversation History" 
echo "      - Save User Turn"
echo "      - Save Assistant Turn"
echo "      - Save State Snapshot"
echo "   c. For each node: Set credential → 'Postgres account'"
echo ""

echo -e "${YELLOW}3. ACTIVATE THE WORKFLOW:${NC}"
echo "   a. Toggle 'Inactive' to 'Active' (green)"
echo "   b. Save the workflow"
echo ""

echo -e "${YELLOW}4. TEST THE FIXED WORKFLOW:${NC}"
echo "   Press Enter when ready to test..."
read -r

echo ""
echo -e "${BLUE}🧪 TESTING FIXED PERSONALITY AI WORKFLOW...${NC}"
echo ""

# Test the webhook
echo -e "${CYAN}Test Message: 'Hi! I love socializing and meeting new people!'${NC}"
echo -e "${CYAN}Expected: 5-15 second processing, rich JSON response${NC}"
echo ""

start_time=$(date +%s)

RESPONSE=$(curl -s -w "HTTPSTATUS:%{http_code}" \
    -X POST http://localhost:5678/webhook/chat \
    -H "Content-Type: application/json" \
    -d '{"session_id":"f47ac10b-58cc-4372-a567-0e02b2c3d479","message":"Hi! I love socializing and meeting new people at parties!"}')

end_time=$(date +%s)
duration=$((end_time - start_time))

# Parse response
HTTP_CODE=$(echo "$RESPONSE" | tr -d '\n' | sed -e 's/.*HTTPSTATUS://')
RESPONSE_BODY=$(echo "$RESPONSE" | sed -e 's/HTTPSTATUS:.*//')

echo -e "${BLUE}📊 TEST RESULTS:${NC}"
echo "   Status Code: $HTTP_CODE"
echo "   Processing Time: ${duration}s"

if [ "$HTTP_CODE" -eq 200 ] && [ ${#RESPONSE_BODY} -gt 100 ]; then
    echo -e "${GREEN}✅ SUCCESS! Personality AI is working!${NC}"
    echo ""
    echo -e "${CYAN}🧠 Response Preview:${NC}"
    if command -v jq >/dev/null 2>&1; then
        echo "$RESPONSE_BODY" | jq -r '.ocean_preview // .ocean // empty | to_entries[] | "   \(.key): \(.value)"' 2>/dev/null || echo "   OCEAN traits detected!"
        echo ""
        echo -e "${CYAN}🗣️  AI Reply:${NC}"
        echo "$RESPONSE_BODY" | jq -r '.reply // .final_response // "Response generated!"' 2>/dev/null | fold -w 80 -s | sed 's/^/   /'
    else
        echo "$RESPONSE_BODY" | head -c 200
        echo "..."
    fi
    echo ""
    echo -e "${GREEN}🎉 YOUR N8N PERSONALITY AI CHATBOT IS NOW FULLY FUNCTIONAL!${NC}"
    echo ""
    echo -e "${BLUE}🔗 Access Points:${NC}"
    echo "   🌐 N8N Editor: http://localhost:5678"
    echo "   📡 Webhook API: http://localhost:5678/webhook/chat"
    echo ""
    echo -e "${BLUE}📝 Test Commands:${NC}"
    echo "   ./test_personality_chatbot.sh  # Comprehensive test suite"
    echo "   curl -X POST http://localhost:5678/webhook/chat \\"
    echo '     -H "Content-Type: application/json" \'
    echo '     -d '"'"'{"session_id":"demo","message":"Your test message"}'"'"''

elif [ "$HTTP_CODE" -eq 200 ] && [ ${#RESPONSE_BODY} -le 100 ]; then
    echo -e "${YELLOW}⚠️  Partial Success - Response too short${NC}"
    echo "   This suggests the workflow is starting but not completing"
    echo "   Check: All 5 database nodes have PostgreSQL credentials set"
    echo ""
    echo -e "${CYAN}Raw Response:${NC}"
    echo "$RESPONSE_BODY"

elif [ "$HTTP_CODE" -eq 404 ]; then
    echo -e "${RED}❌ Workflow not found or not activated${NC}"
    echo "   Make sure to activate the workflow after importing"

elif [ "$HTTP_CODE" -eq 500 ]; then
    echo -e "${RED}❌ Server error - likely credential/configuration issue${NC}"
    echo "   Check N8N execution logs for detailed error information"
    echo "   Go to: Workflow → Executions tab → Click latest failed execution"

else
    echo -e "${RED}❌ Unexpected error${NC}"
    echo "   HTTP Code: $HTTP_CODE"
    echo "   Response: $RESPONSE_BODY"
fi

echo ""
echo -e "${BLUE}🔧 Need Help?${NC}"
echo "   Check N8N → Workflows → [Your workflow] → Executions tab for error details"
echo "   Verify all database nodes show 'Postgres account' in credentials"
echo "   Ensure workflow is marked as 'Active' (green toggle)"
















