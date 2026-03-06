#!/bin/bash

echo "=========================================="
echo "Testing N8N Webhook Activation"
echo "=========================================="
echo ""

echo "Testing: http://localhost:5678/webhook/personality-chat-enhanced"
echo ""

RESPONSE=$(curl -s -w "\n%{http_code}" -X POST http://localhost:5678/webhook/personality-chat-enhanced \
  -H "Content-Type: application/json" \
  -d '{"session_id":"test-activation","turn_index":1,"message":"test"}')

HTTP_CODE=$(echo "$RESPONSE" | tail -n1)
BODY=$(echo "$RESPONSE" | sed '$d')

echo "HTTP Status Code: $HTTP_CODE"
echo ""

if [ -z "$BODY" ]; then
  echo "❌ Response Body: EMPTY (0 bytes)"
  echo ""
  echo "PROBLEM: N8N returned nothing!"
  echo ""
  echo "This means the workflow is NOT ACTIVE."
  echo ""
  echo "ACTION REQUIRED:"
  echo "1. Go to http://localhost:5678"
  echo "2. Open your workflow"
  echo "3. Look at TOP-RIGHT corner"
  echo "4. Click the toggle to make it GREEN (Active)"
  echo ""
else
  echo "✅ Response Body: (first 200 chars)"
  echo "$BODY" | head -c 200
  echo ""
  echo ""
  if echo "$BODY" | grep -q '"reply"'; then
    echo "✅ SUCCESS! Webhook is working!"
    echo "The workflow is ACTIVE and responding correctly."
    echo ""
    echo "Now restart the frontend:"
    echo "  pkill -f 'next dev'"
    echo "  cd frontend && npm run dev > /tmp/frontend.log 2>&1 &"
    echo ""
    echo "Then refresh browser and test chat!"
  elif echo "$BODY" | grep -q '"code":404'; then
    echo "❌ WEBHOOK NOT REGISTERED"
    echo "The workflow needs to be activated in N8N."
  else
    echo "⚠️  Unexpected response format"
  fi
fi

echo "=========================================="









































