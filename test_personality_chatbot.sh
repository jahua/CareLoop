#!/bin/bash

echo "🤖 PERSONALITY AI CHATBOT - COMPREHENSIVE TEST SUITE"
echo "=================================================="

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m'

# Test webhook availability
echo -e "${BLUE}🔍 Checking webhook availability...${NC}"
WEBHOOK_STATUS=$(curl -s -o /dev/null -w "%{http_code}" -X POST http://localhost:5678/webhook/chat)

if [ "$WEBHOOK_STATUS" -eq 404 ]; then
    echo -e "${RED}❌ Webhook not found - workflow may not be active${NC}"
    echo -e "${YELLOW}💡 Make sure to activate the workflow in N8N first!${NC}"
    exit 1
elif [ "$WEBHOOK_STATUS" -eq 500 ]; then
    echo -e "${YELLOW}⚠️  Webhook found but may have configuration issues${NC}"
elif [ "$WEBHOOK_STATUS" -eq 200 ]; then
    echo -e "${GREEN}✅ Webhook is active and responding${NC}"
else
    echo -e "${YELLOW}⚠️  Webhook status: HTTP $WEBHOOK_STATUS${NC}"
fi

echo ""
echo -e "${CYAN}🧪 Running personality detection tests...${NC}"
echo ""

# Test cases with different personalities
declare -a TEST_CASES=(
    '{"session_id":"test-extrovert","message":"Hi there! I absolutely love meeting new people and going to social events! The more people, the better! Life is so exciting when youre surrounded by friends!"}'
    '{"session_id":"test-introvert","message":"Hello. I much prefer quiet environments where I can think deeply. I usually need time alone to recharge after social interactions. I like to plan things carefully."}'
    '{"session_id":"test-anxious","message":"Im really worried about my job interview tomorrow. I keep thinking about all the things that could go wrong. What if I say something stupid? What if they dont like me?"}'
    '{"session_id":"test-confident","message":"I am super excited about my new project launch! I know its going to be a huge success because Ive prepared everything perfectly. I cant wait to present it to everyone!"}'
    '{"session_id":"test-analytical","message":"I need to carefully analyze this problem step by step. Let me break it down into logical components and evaluate each option systematically before making a decision."}'
)

declare -a TEST_NAMES=(
    "🎉 High Extraversion Test"
    "🤔 High Introversion Test"  
    "😰 High Neuroticism (Anxiety) Test"
    "😊 Low Neuroticism (Confidence) Test"
    "🧠 High Conscientiousness Test"
)

# Run tests
for i in "${!TEST_CASES[@]}"; do
    echo -e "${BLUE}Test $((i+1))/5: ${TEST_NAMES[$i]}${NC}"
    
    # Extract session_id and message for display
    SESSION_ID=$(echo "${TEST_CASES[$i]}" | jq -r '.session_id')
    MESSAGE=$(echo "${TEST_CASES[$i]}" | jq -r '.message')
    
    echo -e "${CYAN}📝 Session: $SESSION_ID${NC}"
    echo -e "${CYAN}💬 Message: ${MESSAGE:0:60}...${NC}"
    
    # Make API call with timeout
    echo -e "${YELLOW}⏳ Calling personality AI...${NC}"
    
    start_time=$(date +%s.%N)
    RESPONSE=$(timeout 45s curl -s -w "HTTPSTATUS:%{http_code}" \
        -X POST http://localhost:5678/webhook/chat \
        -H "Content-Type: application/json" \
        -d "${TEST_CASES[$i]}")
    end_time=$(date +%s.%N)
    
    # Parse response
    HTTP_CODE=$(echo "$RESPONSE" | tr -d '\n' | sed -e 's/.*HTTPSTATUS://')
    RESPONSE_BODY=$(echo "$RESPONSE" | sed -e 's/HTTPSTATUS:.*//')
    
    # Calculate duration
    duration=$(echo "$end_time - $start_time" | bc -l)
    duration_formatted=$(printf "%.2f" $duration)
    
    if [ "$HTTP_CODE" -eq 200 ]; then
        echo -e "${GREEN}✅ Success (${duration_formatted}s) - HTTP $HTTP_CODE${NC}"
        
        if command -v jq >/dev/null 2>&1; then
            echo -e "${CYAN}🧠 Detected OCEAN Traits:${NC}"
            echo "$RESPONSE_BODY" | jq -r '.ocean // {} | to_entries[] | "   \(.key): \(.value)"' 2>/dev/null || echo "   Unable to parse OCEAN traits"
            
            echo -e "${CYAN}🎯 Confidence Levels:${NC}"
            echo "$RESPONSE_BODY" | jq -r '.trait_conf // {} | to_entries[] | "   \(.key): \(.value)"' 2>/dev/null || echo "   Unable to parse confidence levels"
            
            echo -e "${CYAN}🗣️  AI Response:${NC}"
            AI_RESPONSE=$(echo "$RESPONSE_BODY" | jq -r '.final_response // .response // "No response found"' 2>/dev/null)
            echo "$AI_RESPONSE" | fold -w 80 -s | sed 's/^/   /'
            
            echo -e "${CYAN}⚡ Performance:${NC}"
            echo "$RESPONSE_BODY" | jq -r '.timings_ms // {} | to_entries[] | "   \(.key): \(.value)ms"' 2>/dev/null || echo "   Timing: ${duration_formatted}s total"
        else
            echo -e "${CYAN}📄 Response preview:${NC}"
            echo "$RESPONSE_BODY" | head -c 200 | sed 's/^/   /'
            echo "..."
        fi
    else
        echo -e "${RED}❌ Failed (${duration_formatted}s) - HTTP $HTTP_CODE${NC}"
        echo -e "${RED}Error details:${NC}"
        echo "$RESPONSE_BODY" | head -c 300 | sed 's/^/   /'
    fi
    
    echo ""
    echo -e "${BLUE}─────────────────────────────────────────────────${NC}"
    echo ""
    
    # Delay between tests
    sleep 2
done

echo -e "${CYAN}📊 Test Suite Complete!${NC}"
echo -e "${BLUE}🌐 N8N Workflow Editor: http://localhost:5678${NC}"
echo -e "${BLUE}📊 Database: localhost:5432 (n8n_personality_ai)${NC}"
echo ""
echo -e "${CYAN}🔧 Manual Test Command:${NC}"
echo -e '   curl -X POST http://localhost:5678/webhook/chat \'
echo -e '     -H "Content-Type: application/json" \'
echo -e '     -d '"'"'{"session_id":"manual","message":"Your test message here"}'"'"''
















