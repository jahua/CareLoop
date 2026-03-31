#!/usr/bin/env bash
# Import a workflow JSON into the local n8n container (same pattern as deploy.sh).
# Usage: ./scripts/import-n8n-workflow.sh [container_name] <path-under-repo>
# Example: ./scripts/import-n8n-workflow.sh docker-n8n-1 workflows/n8n/big5loop-pandora-eval-multiagent-v4.json
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
CONTAINER="${1:-docker-n8n-1}"
REL="${2:-}"
if [[ -z "$REL" ]]; then
  echo "Usage: $0 [container_name] <path-relative-to-big5loop-root>" >&2
  exit 1
fi
IN_CONTAINER="/workflows/$(basename "$REL")"
docker exec "$CONTAINER" n8n import:workflow --input="$IN_CONTAINER"
echo "Imported from $IN_CONTAINER (ensure the file is bind-mounted under /workflows in the container)."
