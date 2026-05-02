#!/usr/bin/env bash
set -euo pipefail

if ! command -v docker >/dev/null 2>&1; then
  echo "docker is not installed; skipping Docker Compose validation."
  exit 0
fi

./scripts/wsl/test-compose.sh
