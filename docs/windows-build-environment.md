# Windows Build Environment

SentinelMesh is built from a Windows workstation and targets Ubuntu Server 24.04 LTS.

## Required Host Tools

- Windows 11
- VS Code
- Codex
- Git for Windows
- Docker Desktop with WSL 2 backend
- Ubuntu WSL distro
- PowerShell 7
- HashiCorp Packer
- QEMU, Hyper-V, or VMware Workstation for ISO testing

## Recommended Layouts

Windows-mounted repo:

```text
C:\Projects\sentinelmesh-nsm
```

WSL path:

```text
/mnt/c/Projects/sentinelmesh-nsm
```

WSL-native repo for better Linux filesystem performance:

```text
~/projects/sentinelmesh-nsm
```

Both layouts must remain supported. Prefer WSL-native paths for heavy ISO build work.

## Install Checklist

1. Install VS Code.
2. Install Codex support for the development workflow.
3. Install Git for Windows.
4. Install Docker Desktop.
5. Enable the Docker Desktop WSL 2 backend.
6. Install Ubuntu under WSL.
7. Confirm Ubuntu is running as WSL 2.
8. Install PowerShell 7.
9. Install HashiCorp Packer.
10. Install QEMU or enable Hyper-V.
11. Clone `https://github.com/cryptic-stack/ubiquitous-spoon`.
12. Open the repo in VS Code.

## Validation Commands

PowerShell:

```powershell
pwsh ./scripts/windows/check-build-env.ps1
```

Ubuntu WSL:

```bash
./scripts/wsl/install-linux-build-deps.sh
./scripts/wsl/validate-autoinstall.sh
./scripts/wsl/test-compose.sh
```

Docker-backed Linux checks from Windows:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File ./scripts/windows/run-linux-checks.ps1
```

## Docker Desktop Note

Docker Desktop is used for Windows development and local container testing. It is not the final SentinelMesh appliance runtime.

The final Ubuntu Server image must install Docker Engine and the Docker Compose plugin directly on Linux.

## Packer Note

Use HashiCorp Packer for repeatable image automation, test VM image builds, and ISO validation workflows where practical.

## Acceptance Checks

- VS Code opens the repo.
- `git version` works.
- `pwsh --version` works.
- Docker Desktop is running.
- `docker version` works.
- `docker compose version` works.
- `wsl.exe -l -v` shows Ubuntu running as WSL 2.
- `packer version` works.
- Ubuntu WSL can run Bash scripts.
- Compose `dev-lab` profile validates.
- Autoinstall YAML validates.
