#!/bin/bash

# Quick test script to verify the workflow is working

echo "🧪 Testing N8N Workflow..."
echo "=========================="
echo ""

# Test message
MESSAGE="I feel anxious and stressed about everything"

# Send request
RESPONSE=$(curl -s -X POST http://localhost:3001/api/chat/message \
  -H "Content-Type: application/json" \
  -d "{
    \"session_id\": \"test-$(date +%s)\",
    \"message\": \"$MESSAGE\"
  }")

echo "📝 Test Message:"
echo "   \"$MESSAGE\""
echo ""

# Check if response has real values
echo "📊 Response:"
echo "$RESPONSE" | jq '.'
echo ""

# Extract OCEAN values
OCEAN_O=$(echo "$RESPONSE" | jq -r '.personality_state.ocean.O // 0')
OCEAN_C=$(echo "$RESPONSE" | jq -r '.personality_state.ocean.C // 0')
OCEAN_E=$(echo "$RESPONSE" | jq -r '.personality_state.ocean.E // 0')
OCEAN_A=$(echo "$RESPONSE" | jq -r '.personality_state.ocean.A // 0')
OCEAN_N=$(echo "$RESPONSE" | jq -r '.personality_state.ocean.N // 0')

echo "🧠 OCEAN Values:"
echo "   O (Openness):        $OCEAN_O"
echo "   C (Conscientiousness): $OCEAN_C"
echo "   E (Extraversion):    $OCEAN_E"
echo "   A (Agreeableness):   $OCEAN_A"
echo "   N (Neuroticism):     $OCEAN_N"
echo ""

# Check if all are zero (indicates broken workflow)
if [ "$OCEAN_O" == "0" ] && [ "$OCEAN_C" == "0" ] && [ "$OCEAN_E" == "0" ] && [ "$OCEAN_A" == "0" ] && [ "$OCEAN_N" == "0" ]; then
    echo "❌ WORKFLOW STILL BROKEN!"
    echo "   All OCEAN values are 0"
    echo ""
    echo "🔧 Make sure you:"
    echo "   1. Imported Phase1_Enhanced_Workflow_LATEST.json"
    echo "   2. Deactivated 'phase1-2' workflow"
    echo "   3. Activated new 'Phase1-Enhanced-Personality-Chat-LATEST' workflow"
    exit 1
else
    echo "✅ WORKFLOW IS WORKING!"
    echo "   Got real personality values"
    echo ""
    echo "🎉 Success! The workflow is properly detecting personality traits."
    exit 0
fi











