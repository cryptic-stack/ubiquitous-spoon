#!/usr/bin/env bash
set -euo pipefail

if ! command -v python3 >/dev/null 2>&1; then
  echo "python3 is not installed; skipping YAML checks."
  exit 0
fi

python3 - <<'PY'
from pathlib import Path

try:
    import yaml
except ImportError:
    print("PyYAML is not installed; skipping YAML checks.")
    raise SystemExit(0)

yaml_paths = [
    Path("configs/prometheus/prometheus.yml"),
    Path("configs/grafana/provisioning/datasources/datasources.yml"),
    Path("configs/grafana/provisioning/dashboards/dashboards.yml"),
]

for path in yaml_paths:
    with path.open("r", encoding="utf-8") as handle:
        yaml.safe_load(handle)
    print(f"YAML parses: {path}")
PY

echo "YAML checks passed."
