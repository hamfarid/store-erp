<# 
Security scan runner (Windows / PowerShell)

Runs:
- Frontend dependency audit (npm)
- Backend dependency scan (safety) if installed
- Backend static security lint (bandit) if installed
- Optional static analysis (semgrep) if installed

This is designed for "ethical hacking" style hygiene checks (OWASP-ish).
#>

$ErrorActionPreference = "Stop"

function Has-Cmd($name) {
  return $null -ne (Get-Command $name -ErrorAction SilentlyContinue)
}

# Avoid UnicodeEncodeError on Windows consoles (cp1252).
try { [Console]::OutputEncoding = [System.Text.UTF8Encoding]::new() } catch {}

Write-Host "== Gaara Scan AI - Security Scan ==" -ForegroundColor Cyan

# --- Frontend ---
if (Test-Path ".\frontend\package.json") {
  if (Has-Cmd "npm") {
    Write-Host "`n[Frontend] npm audit (omit dev, audit-level=high)" -ForegroundColor Yellow
    Push-Location ".\frontend"
    try {
      npm audit --omit=dev --audit-level=high
    } finally {
      Pop-Location
    }
  } else {
    Write-Host "[Frontend] npm not found; skip npm audit." -ForegroundColor DarkYellow
  }
}

# --- Backend ---
if (Test-Path ".\backend\requirements.txt") {
  if (Has-Cmd "python") {
    # safety
    if (Has-Cmd "safety") {
      Write-Host "`n[Backend] safety check (requirements.txt)" -ForegroundColor Yellow
      Push-Location ".\backend"
      try {
        # NOTE: safety v3 "scan" may prompt for login; use non-interactive deprecated
        # command to keep CI/local automation working.
        safety check -r .\requirements.txt --full-report
      } finally {
        Pop-Location
      }
    } else {
      Write-Host "[Backend] safety not found; install with: pip install -r backend/requirements-test.txt" -ForegroundColor DarkYellow
    }

    # bandit
    if (Has-Cmd "bandit") {
      Write-Host "`n[Backend] bandit scan (backend/src) -> reports/bandit.json" -ForegroundColor Yellow
      New-Item -ItemType Directory -Force -Path ".\reports" | Out-Null
      # Use JSON output to avoid console encoding issues and make results machine-readable.
      bandit -r .\backend\src -ll -f json -o .\reports\bandit.json
      Write-Host "[Backend] bandit report written to reports/bandit.json" -ForegroundColor Green
    } else {
      Write-Host "[Backend] bandit not found; install with: pip install -r backend/requirements-test.txt" -ForegroundColor DarkYellow
    }

    # semgrep (optional)
    if (Has-Cmd "semgrep") {
      Write-Host "`n[Backend] semgrep scan (auto config)" -ForegroundColor Yellow
      semgrep scan --config auto .\backend\src
    } else {
      Write-Host "[Backend] semgrep not found (optional); install with: pip install -r backend/requirements-test.txt" -ForegroundColor DarkYellow
    }
  } else {
    Write-Host "[Backend] python not found; skip backend scans." -ForegroundColor DarkYellow
  }
}

Write-Host "`nDone." -ForegroundColor Green

