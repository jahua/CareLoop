#!/usr/bin/env bash
# Deploy Big5Loop to remote server
# Usage: ./scripts/deploy.sh

set -e

SERVER="root@47.108.85.216"
KEY="$HOME/.ssh/boyig.pem"
REMOTE_DIR="/opt/big5loop/app"
REMOTE_ENV="/opt/big5loop/.env"
COMPOSE_FILE="infra/docker/docker-compose.deploy.yml"
WORKFLOW_FILE="workflows/n8n/big5loop-phase1-2-parallel-v3.json"
WORKFLOW_NAME="Big5Loop Phase1-2 Parallel v3 (Optimised Detection)"

# Ensure we're in Big5Loop root
cd "$(dirname "$0")/.."
ROOT="$(pwd)"

if [[ ! -f "$KEY" ]]; then
  echo "Error: SSH key not found at $KEY"
  exit 1
fi

echo "==> Syncing files to $SERVER..."
rsync -avz --delete \
  -e "ssh -i $KEY -o StrictHostKeyChecking=no" \
  --exclude node_modules \
  --exclude .next \
  --exclude .git \
  --exclude "*.log" \
  --exclude data/venv \
  "$ROOT/" "$SERVER:$REMOTE_DIR/"

echo "==> Starting Docker Compose on server..."
ssh -i "$KEY" "$SERVER" "cd $REMOTE_DIR && docker-compose -f $COMPOSE_FILE --env-file $REMOTE_ENV up --build -d"

echo "==> Importing and activating N8N workflow..."
ssh -i "$KEY" "$SERVER" bash -s -- "$REMOTE_DIR" "$REMOTE_ENV" "$WORKFLOW_FILE" "$WORKFLOW_NAME" <<'REMOTE'
set -euo pipefail

REMOTE_DIR="$1"
REMOTE_ENV="$2"
WORKFLOW_FILE="$3"
WORKFLOW_NAME="$4"
N8N_CONTAINER="docker-n8n-1"

if [[ ! -f "$REMOTE_DIR/$WORKFLOW_FILE" ]]; then
  echo "Error: workflow file not found at $REMOTE_DIR/$WORKFLOW_FILE"
  exit 1
fi

docker cp "$REMOTE_DIR/$WORKFLOW_FILE" "$N8N_CONTAINER:/tmp/workflow-import.json"
docker exec "$N8N_CONTAINER" n8n import:workflow --input=/tmp/workflow-import.json >/tmp/n8n-import.log 2>&1 || {
  echo "Error: n8n workflow import failed"
  cat /tmp/n8n-import.log
  exit 1
}

N8N_USER="$(grep '^N8N_BASIC_AUTH_USER=' "$REMOTE_ENV" | cut -d= -f2- || true)"
N8N_PASS="$(grep '^N8N_BASIC_AUTH_PASSWORD=' "$REMOTE_ENV" | cut -d= -f2- || true)"

if [[ -z "${N8N_USER}" || -z "${N8N_PASS}" ]]; then
  echo "Warning: N8N basic auth credentials not set in $REMOTE_ENV"
  echo "Workflow imported. Activate manually in N8N UI."
  exit 0
fi

curl -s -c /tmp/n8n-cookies.txt -X POST http://localhost:5678/rest/login \
  -H 'Content-Type: application/json' \
  -d "{\"emailOrLdapLoginId\":\"${N8N_USER}\",\"password\":\"${N8N_PASS}\"}" >/tmp/n8n-login.json

WORKFLOW_ID="$(curl -s -b /tmp/n8n-cookies.txt http://localhost:5678/rest/workflows \
  | python3 -c 'import json,sys; d=json.load(sys.stdin).get("data",[]); name=sys.argv[1]; print(next((w["id"] for w in d if w.get("name")==name), ""))' "$WORKFLOW_NAME")"

if [[ -z "${WORKFLOW_ID}" ]]; then
  echo "Error: imported workflow not found by name: $WORKFLOW_NAME"
  exit 1
fi

VERSION_ID="$(curl -s -b /tmp/n8n-cookies.txt "http://localhost:5678/rest/workflows/${WORKFLOW_ID}" \
  | python3 -c 'import json,sys; print(json.load(sys.stdin).get("data",{}).get("versionId",""))')"

if [[ -z "${VERSION_ID}" ]]; then
  echo "Error: could not resolve workflow versionId for activation"
  exit 1
fi

curl -s -b /tmp/n8n-cookies.txt -X POST "http://localhost:5678/rest/workflows/${WORKFLOW_ID}/activate" \
  -H 'Content-Type: application/json' \
  -d "{\"versionId\":\"${VERSION_ID}\"}" \
  | python3 -c 'import json,sys; d=json.load(sys.stdin).get("data",{}); print(f"Workflow active={d.get(\"active\")} id={d.get(\"id\")}")'
REMOTE

echo "==> Deploy complete. App: https://big5loop.boyig.com"
echo "    Health: https://big5loop.boyig.com/api/health"
