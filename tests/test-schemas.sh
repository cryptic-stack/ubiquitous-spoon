#!/usr/bin/env bash
set -euo pipefail

if ! command -v python3 >/dev/null 2>&1; then
  echo "python3 is not installed; skipping schema checks."
  exit 0
fi

python3 - <<'PY'
import json
from pathlib import Path

json_paths = list(Path("schemas").glob("*.json"))
json_paths.extend(Path("configs/grafana/dashboards").glob("*.json"))
json_paths.extend(Path("configs/opensearch/index-templates").glob("*.json"))
json_paths.extend(Path("examples").glob("**/*.json"))

for path in json_paths:
    with path.open("r", encoding="utf-8") as handle:
        json.load(handle)
    print(f"JSON parses: {path}")
PY

echo "Schema checks passed."
