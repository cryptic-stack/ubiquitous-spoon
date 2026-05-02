# SentinelMesh NSM
# Purpose: Run Docker Compose validation from Windows.
# Inputs: compose/compose.yml and profile env files.
# Outputs: Compose validation result.
# Safe to re-run: yes.

[CmdletBinding()]
param(
    [string]$Profile = "",
    [switch]$Help
)

if ($Help) {
    Write-Host "Usage: powershell -NoProfile -ExecutionPolicy Bypass -File ./scripts/windows/run-compose-tests.ps1 [-Profile dev-lab]"
    exit 0
}

$ErrorActionPreference = "Stop"
$RepoRoot = Resolve-Path (Join-Path $PSScriptRoot "../..")
$ComposeFile = Join-Path $RepoRoot "compose/compose.yml"
$Profiles = @()
if ($Profile) {
    $Profiles = @($Profile)
} else {
    $Profiles = @("standalone", "manager", "manager-search", "search", "sensor", "receiver", "cyber-range", "dev-lab")
}

if (-not (Test-Path $ComposeFile)) {
    throw "Compose file not found: $ComposeFile"
}

foreach ($Item in $Profiles) {
    $EnvFile = Join-Path $RepoRoot "profiles/$Item.env"

    if (-not (Test-Path $EnvFile)) {
        throw "Profile env file not found: $EnvFile"
    }

    Write-Host "Validating Compose profile: $Item"
    docker compose --env-file $EnvFile -f $ComposeFile --profile $Item config *> $null
}

Write-Host "Compose validation passed."
