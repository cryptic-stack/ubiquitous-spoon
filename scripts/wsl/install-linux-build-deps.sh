#!/usr/bin/env bash
set -euo pipefail

# SentinelMesh NSM
# Purpose: Install Linux-side build dependencies inside Ubuntu WSL.
# Inputs: apt repositories.
# Outputs: Installed validation and build tools.
# Safe to re-run: yes.

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
LOG_DIR="$REPO_ROOT/build/logs"
LOG_FILE="$LOG_DIR/install-linux-build-deps.log"

usage() {
  echo "Usage: scripts/wsl/install-linux-build-deps.sh"
}

if [[ "${1:-}" == "--help" || "${1:-}" == "-h" ]]; then
  usage
  exit 0
fi

mkdir -p "$LOG_DIR"
exec > >(tee -a "$LOG_FILE") 2>&1

sudo apt-get update
sudo apt-get install -y python3 python3-yaml shellcheck xorriso p7zip-full qemu-utils

echo "Linux build dependencies installed."

