#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
COMPOSE_FILE="$SCRIPT_DIR/docker/docker-compose.yml"
SERVICE=free-media-converter

printf "Ensuring Docker Compose service '%s' is running...\n" "$SERVICE"
docker compose -f "$COMPOSE_FILE" up --build -d

printf "Running run.py inside '%s' with %d argument(s)...\n" "$SERVICE" "$#"
docker compose -f "$COMPOSE_FILE" exec "$SERVICE" python run.py "$@"
