#!/usr/bin/env bash
set -euo pipefail

# SentinelMesh NSM
# Purpose: Validate Ubuntu autoinstall YAML.
# Inputs: iso/autoinstall/user-data.
# Outputs: Validation result.
# Safe to re-run: yes.

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
LOG_DIR="$REPO_ROOT/build/logs"
LOG_FILE="$LOG_DIR/validate-autoinstall.log"
USER_DATA="$REPO_ROOT/iso/autoinstall/user-data"

usage() {
  echo "Usage: scripts/wsl/validate-autoinstall.sh"
}

if [[ "${1:-}" == "--help" || "${1:-}" == "-h" ]]; then
  usage
  exit 0
fi

mkdir -p "$LOG_DIR"
exec > >(tee -a "$LOG_FILE") 2>&1

python3 - "$USER_DATA" <<'PY'
import sys
import yaml

path = sys.argv[1]
with open(path, "r", encoding="utf-8") as handle:
    data = yaml.safe_load(handle)

if not isinstance(data, dict):
    raise SystemExit("user-data must parse as a YAML mapping")

if "autoinstall" not in data:
    raise SystemExit("user-data must include top-level autoinstall key")

print("Autoinstall YAML validates:", path)
PY

