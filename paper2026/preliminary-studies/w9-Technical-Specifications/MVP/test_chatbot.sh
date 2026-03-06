#!/bin/bash

echo "🤖 N8N Personality AI Chatbot Tester"
echo "==================================="

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Test cases with different personality profiles
declare -a TEST_MESSAGES=(
    '{"session_id":"extrovert-test","message":"Hi! I love meeting new people and going to parties. What adventure should we plan together?"}'
    '{"session_id":"introvert-test","message":"Hello. I prefer quiet environments and like to think things through carefully before acting. Can you help me plan something?"}'
    '{"session_id":"anxious-test","message":"I am feeling really worried about my presentation tomorrow. I keep thinking about all the things that could go wrong."}'
    '{"session_id":"confident-test","message":"I am excited about my new project! I know it will be successful and I cant wait to share it with everyone."}'
    '{"session_id":"analytical-test","message":"I need to analyze this problem systematically. Can you help me break it down into logical components and evaluate each option?"}'
)

declare -a TEST_LABELS=(
    "🎉 Extroverted & Adventurous"
    "🤔 Introverted & Cautious" 
    "😟 High Neuroticism (Anxious)"
    "😊 Low Neuroticism (Confident)"
    "🧠 High Conscientiousness (Analytical)"
)

echo -e "${BLUE}🔍 Testing N8N Personality AI Chatbot...${NC}"
echo ""

# Check if webhook is available
WEBHOOK_STATUS=$(curl -s -o /dev/null -w "%{http_code}" -X GET http://localhost:5678/webhook/personality-chat-enhanced)
if [ "$WEBHOOK_STATUS" -ne 404 ]; then
    echo -e "${GREEN}✅ Webhook endpoint appears to be available${NC}"
else
    echo -e "${YELLOW}⚠️  Webhook endpoint not found - make sure workflow is imported and active${NC}"
    echo -e "${BLUE}💡 Run ./import_workflow.sh if you haven't imported the workflow yet${NC}"
    echo ""
fi

echo -e "${CYAN}🧪 Running personality detection tests...${NC}"
echo ""

# Run test cases
for i in "${!TEST_MESSAGES[@]}"; do
    echo -e "${BLUE}Test $((i+1))/5: ${TEST_LABELS[$i]}${NC}"
    echo -e "${CYAN}Message: ${NC}$(echo "${TEST_MESSAGES[$i]}" | jq -r '.message')"
    
    # Make the API call
    RESPONSE=$(curl -s -w "HTTPSTATUS:%{http_code}" \
        -X POST http://localhost:5678/webhook/personality-chat-enhanced \
        -H "Content-Type: application/json" \
        -d "${TEST_MESSAGES[$i]}")
    
    # Parse response
    HTTP_CODE=$(echo "$RESPONSE" | tr -d '\n' | sed -e 's/.*HTTPSTATUS://')
    RESPONSE_BODY=$(echo "$RESPONSE" | sed -e 's/HTTPSTATUS:.*//')
    
    if [ "$HTTP_CODE" -eq 200 ]; then
        echo -e "${GREEN}✅ Status: $HTTP_CODE${NC}"
        
        # Try to parse and display key information
        if command -v jq >/dev/null 2>&1; then
            echo -e "${CYAN}🧠 OCEAN Traits:${NC}"
            echo "$RESPONSE_BODY" | jq -r '.ocean // empty | to_entries[] | "   \(.key): \(.value)"' 2>/dev/null || echo "   Unable to parse OCEAN traits"
            
            echo -e "${CYAN}📝 AI Response:${NC}"
            echo "$RESPONSE_BODY" | jq -r '.final_response // .response // empty' 2>/dev/null | fold -w 80 -s | sed 's/^/   /' || echo "   Unable to parse AI response"
            
            echo -e "${CYAN}⚡ Processing Time:${NC}"
            echo "$RESPONSE_BODY" | jq -r '.timings_ms.total // empty | "   Total: \(.)ms"' 2>/dev/null || echo "   Timing info not available"
        else
            echo -e "${CYAN}📄 Raw Response:${NC}"
            echo "$RESPONSE_BODY" | head -c 200
            echo "..."
        fi
    else
        echo -e "${RED}❌ Status: $HTTP_CODE${NC}"
        echo -e "${RED}Error: $RESPONSE_BODY${NC}"
    fi
    
    echo ""
    echo -e "${BLUE}─────────────────────────────────────${NC}"
    echo ""
    
    # Small delay between tests
    sleep 1
done

# Summary
echo -e "${CYAN}📊 Test Summary${NC}"
echo -e "${CYAN}===============${NC}"
echo -e "${BLUE}🔗 Webhook URL: http://localhost:5678/webhook/personality-chat-enhanced${NC}"
echo -e "${BLUE}🌐 N8N Editor: http://localhost:5678 (admin@personality-ai.local/admin123)${NC}"
echo -e "${BLUE}📊 Database: localhost:5432 (n8n_personality_ai)${NC}"
echo ""
echo -e "${BLUE}📝 Manual Test Command:${NC}"
echo -e '   curl -X POST http://localhost:5678/webhook/personality-chat-enhanced \'
echo -e '     -H "Content-Type: application/json" \'
echo -e '     -d '\''{"session_id":"manual-test","message":"Your message here"}'\'''
echo ""
echo -e "${BLUE}📚 For more details, check README.md${NC}"
