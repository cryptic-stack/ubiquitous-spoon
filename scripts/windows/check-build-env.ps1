# SentinelMesh NSM
# Purpose: Check Windows workstation build prerequisites.
# Inputs: Installed local tools.
# Outputs: A readiness report.
# Safe to re-run: yes.

[CmdletBinding()]
param(
    [switch]$Help
)

if ($Help) {
    Write-Host "Usage: pwsh ./scripts/windows/check-build-env.ps1"
    exit 0
}

$ErrorActionPreference = "Continue"
$commandStatus = @{}

function Test-Command {
    param(
        [Parameter(Mandatory = $true)][string]$Name,
        [Parameter(Mandatory = $true)][string]$Command
    )

    $found = Get-Command $Command -ErrorAction SilentlyContinue
    if ($found) {
        Write-Host "[OK] $Name ($Command)"
        $script:commandStatus[$Command] = $true
        return $true
    }

    Write-Host "[MISSING] $Name ($Command)"
    $script:commandStatus[$Command] = $false
    return $false
}

$failures = 0

if (-not (Test-Command -Name "Git" -Command "git")) { $failures++ }
if (-not (Test-Command -Name "Docker" -Command "docker")) { $failures++ }
if (-not (Test-Command -Name "WSL" -Command "wsl.exe")) { $failures++ }
if (-not (Test-Command -Name "Packer" -Command "packer")) { $failures++ }
if (-not (Test-Command -Name "PowerShell 7" -Command "pwsh")) { $failures++ }
if (-not (Test-Command -Name "VS Code" -Command "code")) { $failures++ }

Write-Host ""
Write-Host "Version checks:"
if ($commandStatus["git"]) { git --version 2>$null }
if ($commandStatus["docker"]) {
    docker version --format '{{.Client.Version}}' 2>$null
    docker compose version 2>$null
}
if ($commandStatus["wsl.exe"]) { wsl.exe -l -v 2>$null }
if ($commandStatus["packer"]) { packer version 2>$null }
if ($commandStatus["pwsh"]) { pwsh --version 2>$null }

if ($failures -gt 0) {
    Write-Host ""
    Write-Host "Build environment is missing $failures required tool(s). See docs/windows-build-environment.md."
    exit 1
}

Write-Host ""
Write-Host "Build environment command checks passed."
