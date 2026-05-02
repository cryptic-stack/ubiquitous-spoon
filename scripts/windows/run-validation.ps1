# SentinelMesh NSM
# Purpose: Run Windows-friendly validation checks.
# Inputs: Repository files, Docker Desktop, and Windows PowerShell.
# Outputs: Validation results.
# Safe to re-run: yes.

[CmdletBinding()]
param(
    [switch]$Help
)

if ($Help) {
    Write-Host "Usage: powershell -NoProfile -ExecutionPolicy Bypass -File ./scripts/windows/run-validation.ps1"
    exit 0
}

$ErrorActionPreference = "Stop"
$RepoRoot = Resolve-Path (Join-Path $PSScriptRoot "../..")

Write-Host "Parsing PowerShell helper scripts..."
Get-ChildItem (Join-Path $RepoRoot "scripts/windows/*.ps1") | ForEach-Object {
    $errors = $null
    $null = [System.Management.Automation.PSParser]::Tokenize((Get-Content -LiteralPath $_.FullName -Raw), [ref]$errors)
    if ($errors) {
        throw "Parse failed for $($_.Name)"
    }
    Write-Host "Parsed $($_.Name)"
}

Write-Host "Validating Docker Compose profiles..."
& (Join-Path $RepoRoot "scripts/windows/run-compose-tests.ps1")

Write-Host "Running Docker-backed Linux checks..."
& (Join-Path $RepoRoot "scripts/windows/run-linux-checks.ps1")

Write-Host "Windows-friendly validation completed."

