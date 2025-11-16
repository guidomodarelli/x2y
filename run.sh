#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
COMPOSE_FILE="$SCRIPT_DIR/docker/docker-compose.yml"
SERVICE=free-media-converter

printf "Building Docker image for %s...\n" "$SERVICE"
docker compose -f "$COMPOSE_FILE" build --pull "$SERVICE"

printf "Running %s inside container with %d argument(s)...\n" "$SERVICE" "$#"
docker compose -f "$COMPOSE_FILE" run --rm "$SERVICE" "$@"
