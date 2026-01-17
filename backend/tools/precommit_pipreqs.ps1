# Pre-commit helper for Windows PowerShell environments
param(
  [string]$Python = "python"
)
$ErrorActionPreference = "Stop"
Set-StrictMode -Version Latest

Push-Location $PSScriptRoot
$backendRoot = Split-Path -Path $PSScriptRoot -Parent
Set-Location $backendRoot

Write-Host "[pre-commit] Regenerating requirements_autogen.txt with pipreqs" -ForegroundColor Cyan
& $Python -m pipreqs --encoding utf-8 --savepath tools/requirements_autogen.txt --ignore venv,.venv,__pycache__,migrations,tests --mode compat .

Write-Host "[pre-commit] Checking diff (strict)" -ForegroundColor Cyan
& $Python tools/diff_requirements.py --strict

Pop-Location

