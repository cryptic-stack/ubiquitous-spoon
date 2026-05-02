#!/usr/bin/env bash
set -euo pipefail

# SentinelMesh NSM
# Purpose: Boot-test a SentinelMesh ISO with QEMU.
# Inputs: ISO path and optional disk path.
# Outputs: A QEMU VM boot session.
# Safe to re-run: yes, but the VM disk can be modified by the installer.

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
LOG_DIR="$REPO_ROOT/build/logs"
LOG_FILE="$LOG_DIR/test-iso-qemu.log"

ISO_PATH=""
DISK_PATH="$REPO_ROOT/build/qemu/sentinelmesh-test.qcow2"
MEMORY="8192"
CPUS="4"
CREATE_DISK="false"

usage() {
  cat <<'EOF'
Usage: scripts/wsl/test-iso-qemu.sh --iso PATH [--disk PATH] [--create-disk]

Boots an ISO in QEMU for manual smoke testing.

Options:
  --iso PATH       ISO to boot.
  --disk PATH      qcow2 disk path.
  --create-disk    Create the qcow2 disk if missing.
EOF
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --iso)
      ISO_PATH="${2:-}"
      shift 2
      ;;
    --disk)
      DISK_PATH="${2:-}"
      shift 2
      ;;
    --create-disk)
      CREATE_DISK="true"
      shift
      ;;
    --help|-h)
      usage
      exit 0
      ;;
    *)
      echo "Unknown argument: $1"
      usage
      exit 1
      ;;
  esac
done

mkdir -p "$LOG_DIR" "$(dirname "$DISK_PATH")"
exec > >(tee -a "$LOG_FILE") 2>&1

if [[ -z "$ISO_PATH" || ! -f "$ISO_PATH" ]]; then
  usage
  exit 1
fi

if ! command -v qemu-system-x86_64 >/dev/null 2>&1; then
  echo "qemu-system-x86_64 is required."
  exit 1
fi

if [[ "$CREATE_DISK" == "true" && ! -f "$DISK_PATH" ]]; then
  if ! command -v qemu-img >/dev/null 2>&1; then
    echo "qemu-img is required to create disks."
    exit 1
  fi
  qemu-img create -f qcow2 "$DISK_PATH" 80G
fi

if [[ ! -f "$DISK_PATH" ]]; then
  echo "Disk not found: $DISK_PATH"
  echo "Use --create-disk to create it."
  exit 1
fi

qemu-system-x86_64 \
  -m "$MEMORY" \
  -smp "$CPUS" \
  -enable-kvm \
  -cdrom "$ISO_PATH" \
  -drive "file=$DISK_PATH,format=qcow2" \
  -boot d \
  -netdev user,id=n0 \
  -device virtio-net-pci,netdev=n0 \
  -netdev user,id=n1 \
  -device virtio-net-pci,netdev=n1

