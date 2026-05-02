# Troubleshooting

This document collects known issues and diagnostic steps.

## Docker Desktop Is Not Running

Symptom:

`docker version` fails on Windows.

Check:

```powershell
docker version
```

Fix:

Start Docker Desktop and confirm the WSL 2 backend is enabled.

## WSL Is Not Version 2

Symptom:

Build scripts run slowly or Docker integration fails.

Check:

```powershell
wsl.exe -l -v
```

Fix:

Convert the Ubuntu distro to WSL 2.

## Compose Profile Does Not Render

Symptom:

`docker compose --profile dev-lab config` fails.

Check:

```bash
./scripts/wsl/test-compose.sh
```

Fix:

Review `compose/compose.yml` and profile-specific environment files.

## Autoinstall Validation Fails

Symptom:

`validate-autoinstall.sh` reports missing YAML support or invalid data.

Check:

```bash
./scripts/wsl/validate-autoinstall.sh
```

Fix:

Install `python3-yaml` in WSL or correct `iso/autoinstall/user-data`.

## PowerShell 7 Is Missing

Symptom:

`pwsh` is not recognized.

Check:

```powershell
pwsh --version
```

Fix:

Install PowerShell 7 and reopen the terminal so PATH is refreshed.

## PowerShell Script Execution Is Disabled

Symptom:

Running a helper script reports that scripts are disabled on this system.

Check:

```powershell
Get-ExecutionPolicy -List
```

Fix:

For the current user, allow locally authored scripts:

```powershell
Set-ExecutionPolicy -Scope CurrentUser RemoteSigned
```

Use a stricter policy again later if your workstation policy requires it.

## WSL Bash Is Missing

Symptom:

Running Bash scripts from Windows reports that `/bin/bash` cannot be found.

Check:

```powershell
wsl.exe -l -v
```

Fix:

Install an Ubuntu WSL distro and ensure it is running as WSL 2.
