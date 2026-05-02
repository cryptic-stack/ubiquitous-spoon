#!/usr/bin/env bash
set -euo pipefail

for script in scripts/sm-* scripts/wsl/*.sh iso/*.sh tests/*.sh; do
  bash -n "$script"
done

echo "Script syntax checks passed."
