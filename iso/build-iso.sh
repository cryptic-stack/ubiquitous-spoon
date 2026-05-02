#!/usr/bin/env bash
set -euo pipefail

# SentinelMesh NSM
# Purpose: Build the universal Ubuntu Server ISO.
# Inputs: Ubuntu Server ISO path and autoinstall files.
# Outputs: A SentinelMesh ISO artifact.
# Safe to re-run: yes, after build artifact cleanup.

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
LOG_DIR="$REPO_ROOT/build/logs"
LOG_FILE="$LOG_DIR/build-iso.log"
WORK_DIR="$REPO_ROOT/build/iso-work"
EXTRACT_DIR="$WORK_DIR/extracted"
NO_CLEAN="false"

mkdir -p "$LOG_DIR"
exec > >(tee -a "$LOG_FILE") 2>&1

usage() {
  cat <<'EOF'
Usage: iso/build-iso.sh --ubuntu-iso PATH --output PATH [--no-clean]

Builds a SentinelMesh universal ISO by:
  1. Extracting an Ubuntu Server ISO.
  2. Injecting NoCloud autoinstall data.
  3. Patching GRUB boot entries for autoinstall.
  4. Rebuilding the ISO with xorriso.

Required tools:
  7z
  rsync
  xorriso
  sed
EOF
}

require_command() {
  local command_name="$1"
  if ! command -v "$command_name" >/dev/null 2>&1; then
    echo "Missing required command: $command_name"
    exit 1
  fi
}

patch_grub_file() {
  local grub_file="$1"

  if [[ ! -f "$grub_file" ]]; then
    return 0
  fi

  if grep -q "ds=nocloud" "$grub_file"; then
    echo "GRUB file already patched: $grub_file"
    return 0
  fi

  echo "Patching GRUB file: $grub_file"
  sed -i \
    's#---# autoinstall ds=nocloud\\;s=/cdrom/nocloud/ ---#g' \
    "$grub_file"
}

UBUNTU_ISO=""
OUTPUT_ISO=""

while [[ $# -gt 0 ]]; do
  case "$1" in
    --ubuntu-iso)
      UBUNTU_ISO="${2:-}"
      shift 2
      ;;
    --output)
      OUTPUT_ISO="${2:-}"
      shift 2
      ;;
    --no-clean)
      NO_CLEAN="true"
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

if [[ -z "$UBUNTU_ISO" || -z "$OUTPUT_ISO" ]]; then
  usage
  exit 1
fi

if [[ ! -f "$UBUNTU_ISO" ]]; then
  echo "Ubuntu ISO not found: $UBUNTU_ISO"
  exit 1
fi

require_command 7z
require_command rsync
require_command xorriso
require_command sed

USER_DATA="$REPO_ROOT/iso/autoinstall/user-data"
META_DATA="$REPO_ROOT/iso/autoinstall/meta-data"

if [[ ! -f "$USER_DATA" || ! -f "$META_DATA" ]]; then
  echo "Autoinstall files are missing."
  exit 1
fi

if [[ "$NO_CLEAN" != "true" ]]; then
  rm -rf "$WORK_DIR"
fi

mkdir -p "$EXTRACT_DIR" "$(dirname "$OUTPUT_ISO")"

echo "Repository: $REPO_ROOT"
echo "Ubuntu ISO: $UBUNTU_ISO"
echo "Output ISO: $OUTPUT_ISO"
echo "Work directory: $WORK_DIR"

echo "Extracting Ubuntu ISO..."
7z x "$UBUNTU_ISO" "-o$EXTRACT_DIR" >/dev/null

echo "Injecting NoCloud autoinstall data..."
mkdir -p "$EXTRACT_DIR/nocloud"
cp "$USER_DATA" "$EXTRACT_DIR/nocloud/user-data"
cp "$META_DATA" "$EXTRACT_DIR/nocloud/meta-data"

echo "Copying SentinelMesh payload into ISO..."
mkdir -p "$EXTRACT_DIR/sentinelmesh/payload"
rsync -a \
  --exclude ".git/" \
  --exclude "build/" \
  --exclude "Context" \
  --exclude "*.iso" \
  --exclude "__pycache__/" \
  "$REPO_ROOT/" "$EXTRACT_DIR/sentinelmesh/payload/"

patch_grub_file "$EXTRACT_DIR/boot/grub/grub.cfg"
patch_grub_file "$EXTRACT_DIR/boot/grub/loopback.cfg"

if [[ ! -f "$EXTRACT_DIR/boot/grub/i386-pc/eltorito.img" ]]; then
  echo "Expected BIOS boot image not found. Ubuntu ISO layout may have changed."
  echo "Leaving extracted tree in: $EXTRACT_DIR"
  exit 1
fi

if [[ ! -f "$EXTRACT_DIR/EFI/boot/bootx64.efi" ]]; then
  echo "Expected UEFI boot image not found. Ubuntu ISO layout may have changed."
  echo "Leaving extracted tree in: $EXTRACT_DIR"
  exit 1
fi

echo "Rebuilding ISO..."
xorriso -as mkisofs \
  -r \
  -V "SentinelMesh-NSM" \
  -o "$OUTPUT_ISO" \
  -J -joliet-long -l \
  -b boot/grub/i386-pc/eltorito.img \
  -c boot.catalog \
  -no-emul-boot \
  -boot-load-size 4 \
  -boot-info-table \
  -eltorito-alt-boot \
  -e EFI/boot/bootx64.efi \
  -no-emul-boot \
  -isohybrid-gpt-basdat \
  "$EXTRACT_DIR"

echo "ISO created: $OUTPUT_ISO"

if [[ "$NO_CLEAN" != "true" ]]; then
  echo "Cleaning work directory."
  rm -rf "$WORK_DIR"
else
  echo "Preserving work directory: $WORK_DIR"
fi
