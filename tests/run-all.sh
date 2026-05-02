#!/usr/bin/env bash
set -euo pipefail

# SentinelMesh NSM
# Purpose: Run all repository validation checks available in the current environment.
# Inputs: Repository files and local tooling.
# Outputs: Validation results.
# Safe to re-run: yes.

./tests/test-scripts.sh
./tests/test-python.sh
./tests/test-schemas.sh
./tests/test-autoinstall.sh
./tests/test-ansible.sh
./tests/test-packer.sh
./tests/test-compose.sh

echo "All available validation checks passed."
