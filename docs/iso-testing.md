# ISO Testing

SentinelMesh ISO testing should happen in a disposable VM before any physical install.

## QEMU From WSL

Create a test disk and boot the ISO:

```bash
./scripts/wsl/test-iso-qemu.sh \
  --iso build/SentinelMesh-NSM.iso \
  --create-disk
```

Reuse an existing disk:

```bash
./scripts/wsl/test-iso-qemu.sh \
  --iso build/SentinelMesh-NSM.iso \
  --disk build/qemu/sentinelmesh-test.qcow2
```

The QEMU test VM provides two virtual NICs:

- First NIC for management-style traffic.
- Second NIC for monitoring-interface selection tests.

## Packer

Validate the Packer template when Packer is installed:

```bash
./tests/test-packer.sh
```

Run the Windows helper:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File ./scripts/windows/run-packer-build.ps1 -UbuntuIsoPath C:\path\ubuntu.iso
```

## Current Manual Checks

During boot testing, verify:

- Ubuntu Server autoinstall starts.
- SentinelMesh payload copies to `/opt/sentinelmesh/source`.
- Ansible host-prep runs.
- Docker Engine installs.
- `/opt/sentinelmesh/bin` exists.
- `sm-setup` is available in PATH.
- Firstboot reminder appears.
