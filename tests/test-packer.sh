#!/usr/bin/env bash
set -euo pipefail

if ! command -v packer >/dev/null 2>&1; then
  echo "packer is not installed; skipping Packer validation."
  exit 0
fi

packer init packer/sentinelmesh-ubuntu-24.04.pkr.hcl
packer validate \
  -var "ubuntu_iso_path=/tmp/ubuntu.iso" \
  -var "ubuntu_iso_checksum=none" \
  packer/sentinelmesh-ubuntu-24.04.pkr.hcl

echo "Packer validation passed."
