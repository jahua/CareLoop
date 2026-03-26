#!/usr/bin/env bash
# Test PERSONAGE Benchmark webhook on local Docker.
# Prerequisites: docker compose up, workflow imported & activated in N8N at http://localhost:5678

set -e
WEBHOOK_URL="${WEBHOOK_URL:-http://localhost:5678}"
WEBHOOK_PATH="${WEBHOOK_PATH:-big5loop-turn-personage-benchmark}"

echo "=== Testing webhook: $WEBHOOK_URL/webhook/$WEBHOOK_PATH ==="
echo ""

START=$(python3 -c "import time; print(int(time.time()*1000))")
RESP=$(curl -s -X POST "$WEBHOOK_URL/webhook/$WEBHOOK_PATH" \
  -H "Content-Type: application/json" \
  -d "{\"session_id\":\"test-$(date +%s)\",\"turn_index\":1,\"message\":\"I feel overwhelmed caring for my mother\",\"context\":{\"language\":\"en\",\"canton\":\"ZH\"}}")
END=$(python3 -c "import time; print(int(time.time()*1000))")
ELAPSED=$((END - START))

echo "Response time: ${ELAPSED} ms"
echo ""

if echo "$RESP" | grep -q '"session_id"'; then
  echo "SUCCESS: Got valid response"
  echo "$RESP" | python3 -c "
import json,sys
d=json.load(sys.stdin)
if isinstance(d,list): d=d[0]
st=d.get('stage_timings',[])
if st:
    print('Stage timings:')
    for t in st:
        if isinstance(t,dict) and t.get('duration_ms'):
            print(f\"  {t.get('stage','?'):25s} {t['duration_ms']:6.0f} ms\")
" 2>/dev/null || echo "$RESP" | head -c 500
else
  echo "Response:"
  echo "$RESP" | head -c 800
fi
