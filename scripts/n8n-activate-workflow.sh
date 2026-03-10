#!/usr/bin/env bash
# Activate Big5Loop workflow after N8N restart.
# Run: ./scripts/n8n-activate-workflow.sh (from Big5Loop root)
# Or after docker compose up: docker compose -f infra/docker/docker-compose.yml --env-file .env exec n8n n8n update:workflow --id=Qdw2nuaxVGOSSCbi --active=true

set -e
cd "$(dirname "$0")/.."
COMPOSE="docker compose -f infra/docker/docker-compose.yml --env-file .env"
WF_ID="Qdw2nuaxVGOSSCbi"

echo "Stopping n8n..."
$COMPOSE stop n8n 2>/dev/null || true
sleep 2

echo "Importing workflow..."
# Volume name: docker compose prefixes with project dir; try common names
for vol in docker_n8n_data big5loop_n8n_data; do
  docker volume inspect $vol 2>/dev/null && N8N_VOL=$vol && break
done
N8N_VOL=${N8N_VOL:-docker_n8n_data}

$COMPOSE run --rm -v "$(pwd)/workflows/n8n:/workflows:ro" -v ${N8N_VOL}:/home/node/.n8n n8n import:workflow --input=/workflows/big5loop-phase1-2-postgres-mvp.json 2>&1 | grep -E "Success|Deactiv|Error" || true

echo "Activating workflow $WF_ID..."
$COMPOSE run --rm -v ${N8N_VOL}:/home/node/.n8n n8n update:workflow --id=$WF_ID --active=true 2>&1 | grep -E "Activ|Error" || true

echo "Starting n8n..."
$COMPOSE start n8n 2>&1

echo "Done. Workflow should be active. Test: curl -X POST http://localhost:3003/api/gateway/chat -H 'Content-Type: application/json' -d '{\"message\":\"I feel overwhelmed\",\"session_id\":\"00000000-0000-4000-8000-000000000001\",\"user_id\":\"test\",\"context\":{\"language\":\"en\"}}'"
