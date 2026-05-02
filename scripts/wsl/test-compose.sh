#!/usr/bin/env bash
set -euo pipefail

# SentinelMesh NSM
# Purpose: Validate Docker Compose profiles.
# Inputs: compose/compose.yml and profiles/*.env.
# Outputs: Compose config validation result for each profile.
# Safe to re-run: yes.

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
LOG_DIR="$REPO_ROOT/build/logs"
LOG_FILE="$LOG_DIR/test-compose.log"
COMPOSE_FILE="$REPO_ROOT/compose/compose.yml"

usage() {
  echo "Usage: scripts/wsl/test-compose.sh"
}

if [[ "${1:-}" == "--help" || "${1:-}" == "-h" ]]; then
  usage
  exit 0
fi

mkdir -p "$LOG_DIR"
exec > >(tee -a "$LOG_FILE") 2>&1

if ! command -v docker >/dev/null 2>&1; then
  echo "docker is not installed; skipping Docker Compose validation."
  exit 0
fi

profiles=(standalone manager manager-search search sensor receiver cyber-range dev-lab)

for profile in "${profiles[@]}"; do
  env_file="$REPO_ROOT/profiles/$profile.env"
  echo "Validating profile: $profile"
  docker compose --env-file "$env_file" -f "$COMPOSE_FILE" --profile "$profile" config >/dev/null
done

echo "All Compose profiles validated."
