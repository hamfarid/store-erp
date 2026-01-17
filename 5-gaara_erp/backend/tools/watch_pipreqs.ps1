# Simple file watcher to run pipreqs + diff on source changes
param(
  [string]$Python = "python"
)
$ErrorActionPreference = "Stop"
Set-StrictMode -Version Latest

$root = Split-Path -Path $PSScriptRoot -Parent
Set-Location $root

$fsw = New-Object System.IO.FileSystemWatcher
$fsw.Path = (Get-Location).Path
$fsw.IncludeSubdirectories = $true
$fsw.Filter = "*.py"
$fsw.EnableRaisingEvents = $true

Write-Host "Watching for Python changes under $((Get-Location).Path) ... Press Ctrl+C to stop." -ForegroundColor Yellow

$action = {
  try {
    Write-Host "[watch] Change detected. Running pipreqs + diff..." -ForegroundColor Cyan
    & $using:Python -m pipreqs --encoding utf-8 --savepath tools/requirements_autogen.txt --ignore venv,.venv,__pycache__,migrations,tests --mode compat .
    & $using:Python tools/diff_requirements.py
  } catch {
    Write-Host "[watch] Error: $_" -ForegroundColor Red
  }
}

Register-ObjectEvent $fsw Changed -Action $action | Out-Null
Register-ObjectEvent $fsw Created -Action $action | Out-Null
Register-ObjectEvent $fsw Deleted -Action $action | Out-Null
Register-ObjectEvent $fsw Renamed -Action $action | Out-Null

# Keep the script alive
while ($true) { Start-Sleep -Seconds 1 }

