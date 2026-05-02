# ISO Build

The SentinelMesh ISO build must produce one universal Ubuntu Server 24.04 LTS installer.

## Current Status

The ISO build script now implements a first remaster workflow:

- Validate required inputs.
- Check for `7z`, `xorriso`, and `sed`.
- Extract the Ubuntu Server ISO.
- Inject NoCloud autoinstall files under `/nocloud`.
- Copy the SentinelMesh source payload into `/sentinelmesh/payload` on the ISO.
- Patch GRUB entries with `autoinstall ds=nocloud;s=/cdrom/nocloud/`.
- Rebuild the ISO with `xorriso`.

This still requires VM boot testing before it should be considered release-ready.

## Intended Flow

1. Download or locate the Ubuntu Server 24.04 LTS ISO.
2. Inject SentinelMesh autoinstall data.
3. Include host preparation and firstboot assets.
4. Build a bootable ISO artifact.
5. Boot-test the ISO in Hyper-V, QEMU, or VMware.
6. Record test findings in `docs/developer-notes.md` and `docs/changelog.md`.

## Validation

Run:

```bash
./scripts/wsl/validate-autoinstall.sh
```

The validator checks that the autoinstall file parses as YAML and includes the expected top-level `autoinstall` key.

## Build Command

From Ubuntu WSL:

```bash
./iso/build-iso.sh \
  --ubuntu-iso /path/to/ubuntu-24.04-live-server-amd64.iso \
  --output build/SentinelMesh-NSM.iso
```

Keep extracted build files for troubleshooting:

```bash
./iso/build-iso.sh \
  --ubuntu-iso /path/to/ubuntu-24.04-live-server-amd64.iso \
  --output build/SentinelMesh-NSM.iso \
  --no-clean
```

## Payload Install

The autoinstall `late-commands` copy the ISO payload into:

```text
/opt/sentinelmesh/source
```

Then the installer runs:

```bash
ANSIBLE_CONFIG=ansible/ansible.cfg ansible-playbook -i ansible/inventory.ini ansible/site.yml
```

The Ansible playbook installs runtime files into `/opt/sentinelmesh`, links commands into `/usr/local/bin`, installs Docker Engine, and enables firstboot reminders.

## Known Risk

Ubuntu ISO boot layouts can change between point releases. If the script cannot find the expected BIOS or UEFI boot images, it stops and preserves the extracted tree for inspection.
