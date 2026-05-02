#!/usr/bin/env bash
set -euo pipefail

if ! command -v python3 >/dev/null 2>&1; then
  echo "python3 is not installed; skipping Python syntax checks."
  exit 0
fi

python3 -m py_compile services/asset-context/asset_context.py
python3 -m py_compile services/connection-metrics/connection_metrics.py
python3 -m py_compile services/range-engine/range_engine.py
python3 -m py_compile services/sensor-enrollment/enrollment_service.py
python3 -m py_compile services/soc-portal/soc_portal.py
python3 tests/test-asset-context.py
python3 tests/test-connection-metrics.py
python3 tests/test-soc-portal.py

echo "Python syntax checks passed."
