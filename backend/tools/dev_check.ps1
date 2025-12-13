#Requires -Version 5.0
$ErrorActionPreference = "Stop"
Set-StrictMode -Version Latest

# Move to repo backend root no matter where this script is called from
$scriptDir = Split-Path -Path $MyInvocation.MyCommand.Path -Parent
$backendRoot = Split-Path -Path $scriptDir -Parent
Set-Location $backendRoot

function Resolve-Python {
  if ($env:VIRTUAL_ENV) {
    $candidate = Join-Path $env:VIRTUAL_ENV "Scripts/python.exe"
    if (Test-Path $candidate) { return $candidate }
  }
  $py = (Get-Command python -ErrorAction SilentlyContinue)
  if ($py) { return "python" }
  throw "Python interpreter not found. Activate your venv or ensure 'python' is on PATH."
}

$PY = Resolve-Python

Write-Host "==> Regenerating tools/requirements_autogen.txt with pipreqs" -ForegroundColor Cyan
& $PY -m pipreqs --encoding utf-8 --savepath tools/requirements_autogen.txt --ignore venv,.venv,__pycache__,migrations,tests --mode compat .
if ($LASTEXITCODE -ne 0) { throw "pipreqs failed with exit code $LASTEXITCODE" }

Write-Host "==> Diff curated vs auto" -ForegroundColor Cyan
& $PY tools/diff_requirements.py
if ($LASTEXITCODE -ne 0) { throw "diff script failed with exit code $LASTEXITCODE" }

Write-Host "==> Running tests (SKIP_BLUEPRINTS=1)" -ForegroundColor Cyan
$env:SKIP_BLUEPRINTS = "1"
& $PY -m pytest -q
exit $LASTEXITCODE

