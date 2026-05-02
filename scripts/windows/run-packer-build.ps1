# SentinelMesh NSM
# Purpose: Run a Packer build from Windows.
# Inputs: Ubuntu ISO path and checksum.
# Outputs: Packer build artifacts.
# Safe to re-run: yes, but existing Packer output may need cleanup.

[CmdletBinding()]
param(
    [string]$UbuntuIsoPath,
    [string]$UbuntuIsoChecksum = "none",
    [switch]$Help
)

if ($Help -or -not $UbuntuIsoPath) {
    Write-Host "Usage: pwsh ./scripts/windows/run-packer-build.ps1 -UbuntuIsoPath C:\path\ubuntu.iso [-UbuntuIsoChecksum sha256:...]"
    exit 0
}

$ErrorActionPreference = "Stop"
$RepoRoot = Resolve-Path (Join-Path $PSScriptRoot "../..")
$Template = Join-Path $RepoRoot "packer/sentinelmesh-ubuntu-24.04.pkr.hcl"

packer init $Template
packer validate -var "ubuntu_iso_path=$UbuntuIsoPath" -var "ubuntu_iso_checksum=$UbuntuIsoChecksum" $Template
packer build -var "ubuntu_iso_path=$UbuntuIsoPath" -var "ubuntu_iso_checksum=$UbuntuIsoChecksum" $Template

