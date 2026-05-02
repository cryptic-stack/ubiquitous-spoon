#!/usr/bin/env bash
set -euo pipefail

# SentinelMesh NSM
# Purpose: WSL wrapper for the ISO build script.
# Inputs: Ubuntu ISO path and output ISO path.
# Outputs: SentinelMesh ISO artifact after implementation.
# Safe to re-run: yes.

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"

"$REPO_ROOT/iso/build-iso.sh" "$@"

