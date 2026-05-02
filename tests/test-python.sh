#!/usr/bin/env bash
set -euo pipefail

if ! command -v python3 >/dev/null 2>&1; then
  echo "python3 is not installed; skipping Python syntax checks."
  exit 0
fi

python3 -m py_compile services/asset-context/asset_context.py
python3 -m py_compile services/range-engine/range_engine.py
python3 -m py_compile services/sensor-enrollment/enrollment_service.py
python3 tests/test-asset-context.py

echo "Python syntax checks passed."
