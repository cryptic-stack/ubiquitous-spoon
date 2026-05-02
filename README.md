# SentinelMesh NSM

SentinelMesh NSM is a custom network security monitoring image built from one universal Ubuntu Server ISO. The ISO installs a hardened base system, then a first-boot wizard asks which deployment role to activate.

Source repository:

https://github.com/cryptic-stack/ubiquitous-spoon

## Build Principle

Build system:

- Windows workstation
- VS Code
- Codex
- Docker Desktop with WSL 2 backend
- Ubuntu WSL
- HashiCorp Packer
- PowerShell 7

Target system:

- Ubuntu Server 24.04 LTS
- Docker Engine
- Docker Compose plugin
- SentinelMesh files under `/opt/sentinelmesh`

Do not use Ubuntu Desktop as the target image.

## Universal ISO Model

SentinelMesh uses one ISO for all deployment types. Role selection happens after install through:

```bash
sudo sm-setup
```

Supported install types:

1. Standalone NSM
2. Manager / Search Node
3. Sensor Node
4. Cyber Range Node
5. Developer / Lab Node

## Repository Map

- `docs/` contains architecture, decisions, build notes, service maps, and troubleshooting.
- `iso/` contains Ubuntu autoinstall and ISO build helpers.
- `packer/` contains image automation templates.
- `ansible/` prepares the Ubuntu host and installs SentinelMesh files.
- `compose/` contains the profile-based Docker Compose stack.
- `profiles/` contains profile-specific environment files.
- `scripts/windows/` contains PowerShell helpers for the Windows workstation.
- `scripts/wsl/` contains Linux build and validation helpers for Ubuntu WSL.
- `scripts/` will contain appliance scripts copied to `/opt/sentinelmesh/bin`.
- `configs/` contains service configuration.
- `rules/` contains detection content.
- `tests/` contains local validation scripts.

## First Developer Flow

From Windows:

```powershell
pwsh ./scripts/windows/check-build-env.ps1
```

From Ubuntu WSL:

```bash
./scripts/wsl/install-linux-build-deps.sh
./tests/run-all.sh
```

From Windows with Docker Desktop:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File ./scripts/windows/run-validation.ps1
```

## Documentation Rule

Documentation is part of the build. Every meaningful change should update at least one of:

- `docs/architecture.md`
- `docs/design-decisions.md`
- `docs/service-map.md`
- `docs/troubleshooting.md`
- `docs/developer-notes.md`
- `docs/changelog.md`
- `docs/validation.md`
- `docs/asset-context.md`
- `docs/risk-scoring.md`
- `docs/phase-status.md`
- `docs/cyber-range.md`
- `docs/sensor-enrollment.md`
- `docs/operations.md`
- `docs/iso-testing.md`
- `docs/observability.md`
- `docs/security-onion-gap-analysis.md`
- `docs/next-steps.md`

Codex-specific implementation guidance lives in:

- `docs/codex-build-instructions.md`
