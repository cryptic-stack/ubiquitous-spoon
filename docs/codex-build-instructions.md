# Codex Build Instructions

Use this document as the working instruction set for Codex when building SentinelMesh NSM.

## Mission

Build SentinelMesh NSM: one universal Ubuntu Server 24.04 LTS ISO for network security monitoring.

The ISO installs a hardened base system. After first boot, deployment scripts ask what type of install the operator wants.

Do not create separate ISOs per role.

## Repository

Use:

```text
https://github.com/cryptic-stack/ubiquitous-spoon
```

The local workspace should track:

```text
origin https://github.com/cryptic-stack/ubiquitous-spoon.git
```

## Development Environment

Build system:

- Windows 11
- VS Code
- Codex
- Docker Desktop with WSL 2 backend
- Ubuntu WSL
- HashiCorp Packer
- Git
- PowerShell 7
- QEMU, Hyper-V, or VMware Workstation for ISO testing

Target system:

- Ubuntu Server 24.04 LTS
- Docker Engine
- Docker Compose plugin

Important:

Docker Desktop is only for development and local Compose tests. The final appliance must use Docker Engine and the Docker Compose plugin directly on Ubuntu Server.

## Install Profiles

`sm-setup` must offer:

1. Standalone NSM
2. Manager / Search Node
3. Sensor Node
4. Cyber Range Node
5. Developer / Lab Node
6. Dedicated Manager Node
7. Dedicated Search Node
8. Receiver Node

The selected profile must be saved to:

- `/etc/sentinelmesh/profile`
- `/etc/sentinelmesh/sentinelmesh.yml`

## Core Design

Use:

- One ISO
- One Ubuntu Server base
- One firstboot setup wizard
- One primary config file
- One main Docker Compose file
- Docker Compose profiles for install modes
- Docker containers inside the Ubuntu Server target
- A common Docker bridge network named `smbridge`
- Ansible for host preparation
- Packer for repeatable image automation where practical

## Required Documentation Behavior

Document during the build, not after.

Update these files as changes are made:

- `docs/architecture.md`
- `docs/design-decisions.md`
- `docs/service-map.md`
- `docs/troubleshooting.md`
- `docs/developer-notes.md`
- `docs/changelog.md`
- `docs/windows-build-environment.md`
- `docs/asset-context.md`
- `docs/risk-scoring.md`

Every major design decision belongs in `docs/design-decisions.md`.

Every added service belongs in `docs/service-map.md`.

Every blocked check, environment issue, or operational wrinkle belongs in `docs/troubleshooting.md`.

Every enrichment or scoring change belongs in `docs/asset-context.md` or `docs/risk-scoring.md`.

## Script Standards

Linux scripts must:

- Use Bash.
- Start with `#!/usr/bin/env bash`.
- Use `set -euo pipefail`.
- Support `--help`.
- Log to `/var/log/sentinelmesh/` on the appliance or `./build/logs/` during build.
- Avoid destructive actions unless explicitly confirmed.

PowerShell scripts must:

- Be PowerShell 7 compatible.
- Check whether required tools exist before running them.
- Print clear next steps.
- Avoid destructive actions unless explicitly confirmed.

## Build Phases

Phase 0:

- Create Windows development environment documentation.
- Add prerequisite check scripts.

Phase 1:

- Create repo structure.
- Add docs.
- Add base scripts.

Phase 2:

- Create Docker Compose profile stack.
- Validate locally with Docker Desktop.

Phase 3:

- Create Ubuntu Server autoinstall configuration.

Phase 4:

- Create Packer templates for automated VM and image testing.

Phase 5:

- Create universal ISO build script.

Phase 6:

- Boot-test the ISO in Hyper-V, QEMU, or VMware.
- Document findings.

## Current Validation Commands

Windows:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File ./scripts/windows/check-build-env.ps1
powershell -NoProfile -ExecutionPolicy Bypass -File ./scripts/windows/run-validation.ps1
```

Ubuntu WSL:

```bash
./scripts/wsl/install-linux-build-deps.sh
./tests/run-all.sh
```

## Current Known Local Gaps

- Packer is not installed or not on PATH in the current Windows shell.
- PowerShell 7 is not installed or not on PATH in the current Windows shell.
- WSL currently shows Docker Desktop, but Ubuntu WSL Bash is not available from this shell.
- Python YAML support is not installed in the current Windows Python environment.
