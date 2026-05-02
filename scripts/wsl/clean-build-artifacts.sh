#!/usr/bin/env bash
set -euo pipefail

# SentinelMesh NSM
# Purpose: Clean generated build artifacts after confirmation.
# Inputs: ./build directory.
# Outputs: Removed generated build artifacts.
# Safe to re-run: yes, with explicit confirmation.

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
BUILD_DIR="$REPO_ROOT/build"

usage() {
  echo "Usage: scripts/wsl/clean-build-artifacts.sh"
}

if [[ "${1:-}" == "--help" || "${1:-}" == "-h" ]]; then
  usage
  exit 0
fi

if [[ ! -d "$BUILD_DIR" ]]; then
  echo "No build directory exists."
  exit 0
fi

read -r -p "Remove generated build artifacts under $BUILD_DIR? Type yes: " answer
if [[ "$answer" != "yes" ]]; then
  echo "Aborted."
  exit 1
fi

rm -rf "$BUILD_DIR"
echo "Removed $BUILD_DIR"

