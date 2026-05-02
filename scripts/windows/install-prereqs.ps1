# SentinelMesh NSM
# Purpose: Print prerequisite installation guidance for Windows.
# Inputs: None.
# Outputs: Human-readable installation steps.
# Safe to re-run: yes.

[CmdletBinding()]
param(
    [switch]$Help
)

if ($Help) {
    Write-Host "Usage: pwsh ./scripts/windows/install-prereqs.ps1"
    exit 0
}

Write-Host "Install these tools before building SentinelMesh:"
Write-Host "- VS Code"
Write-Host "- Git for Windows"
Write-Host "- Docker Desktop with WSL 2 backend"
Write-Host "- Ubuntu WSL distro"
Write-Host "- PowerShell 7"
Write-Host "- HashiCorp Packer"
Write-Host "- QEMU or Hyper-V"
Write-Host ""
Write-Host "After installation, run:"
Write-Host "pwsh ./scripts/windows/check-build-env.ps1"

