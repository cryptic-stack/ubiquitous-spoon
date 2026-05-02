# SentinelMesh NSM
# Purpose: Run Linux-oriented validation from Windows using Docker.
# Inputs: Repository files mounted into Linux containers.
# Outputs: Bash syntax and autoinstall validation results.
# Safe to re-run: yes.

[CmdletBinding()]
param(
    [switch]$Help
)

if ($Help) {
    Write-Host "Usage: powershell -NoProfile -ExecutionPolicy Bypass -File ./scripts/windows/run-linux-checks.ps1"
    exit 0
}

$ErrorActionPreference = "Stop"
$RepoRoot = Resolve-Path (Join-Path $PSScriptRoot "../..")

Write-Host "Running Bash syntax checks in Docker..."
docker run --rm -v "${RepoRoot}:/repo" -w /repo bash:5.2 bash ./tests/test-scripts.sh

Write-Host "Running Python syntax and schema checks in Docker..."
docker run --rm -v "${RepoRoot}:/repo" -w /repo python:3.12-slim sh -c "./tests/test-python.sh && ./tests/test-schemas.sh"

Write-Host "Running autoinstall YAML validation in Docker..."
docker run --rm -v "${RepoRoot}:/repo" -w /repo python:3.12-alpine sh -c "pip install --quiet pyyaml && python - <<'PY'
import yaml
from pathlib import Path
path = Path('iso/autoinstall/user-data')
data = yaml.safe_load(path.read_text())
assert isinstance(data, dict)
assert 'autoinstall' in data
print('Autoinstall YAML validates')
PY"

Write-Host "Linux-oriented checks completed."
