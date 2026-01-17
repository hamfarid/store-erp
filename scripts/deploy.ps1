# =============================================================================
# Store ERP v2.0.0 - Deployment Script (PowerShell)
# =============================================================================
# Usage: .\scripts\deploy.ps1 -Environment [dev|staging|production]
# =============================================================================

param(
    [Parameter(Mandatory=$false)]
    [ValidateSet("dev", "staging", "production")]
    [string]$Environment = "dev",
    
    [switch]$Force,
    [switch]$NoBackup,
    [switch]$DockerOnly
)

$ErrorActionPreference = "Stop"
$ProjectRoot = Split-Path -Parent $PSScriptRoot

Write-Host ""
Write-Host "╔═══════════════════════════════════════════════════════════════════╗" -ForegroundColor Cyan
Write-Host "║           Store ERP v2.0.0 - Deployment                           ║" -ForegroundColor Cyan
Write-Host "║           Environment: $($Environment.ToUpper().PadRight(40))    ║" -ForegroundColor Cyan
Write-Host "╚═══════════════════════════════════════════════════════════════════╝" -ForegroundColor Cyan
Write-Host ""

# Validate environment
if ($Environment -eq "production" -and -not $Force) {
    Write-Host "[WARNING] You are deploying to PRODUCTION!" -ForegroundColor Red
    Write-Host "Use -Force flag to confirm." -ForegroundColor Yellow
    exit 1
}

# Step 1: Create Backup
if (-not $NoBackup) {
    Write-Host "[1/6] Creating Backup..." -ForegroundColor Yellow
    $BackupDir = "$ProjectRoot\backups"
    $Timestamp = Get-Date -Format "yyyy-MM-dd_HH-mm-ss"
    $BackupPath = "$BackupDir\backup_$Timestamp"
    
    if (-not (Test-Path $BackupDir)) {
        New-Item -ItemType Directory -Path $BackupDir | Out-Null
    }
    
    # Backup database
    if (Test-Path "$ProjectRoot\backend\instance\store.db") {
        Copy-Item "$ProjectRoot\backend\instance\store.db" "$BackupPath.db"
        Write-Host "  ✓ Database backed up" -ForegroundColor Green
    }
    
    # Backup config
    if (Test-Path "$ProjectRoot\backend\.env") {
        Copy-Item "$ProjectRoot\backend\.env" "$BackupPath.env"
        Write-Host "  ✓ Config backed up" -ForegroundColor Green
    }
} else {
    Write-Host "[1/6] Skipping Backup (--NoBackup)" -ForegroundColor Yellow
}

# Step 2: Pull Latest Code (if git repo)
Write-Host "[2/6] Checking for Updates..." -ForegroundColor Yellow
Push-Location $ProjectRoot
if (Test-Path ".git") {
    $GitStatus = git status --porcelain
    if ($GitStatus -and -not $Force) {
        Write-Host "  ✗ Uncommitted changes detected!" -ForegroundColor Red
        Write-Host "  Commit or stash changes first, or use -Force" -ForegroundColor Yellow
        exit 1
    }
    Write-Host "  ✓ Repository clean" -ForegroundColor Green
} else {
    Write-Host "  → Not a git repository" -ForegroundColor Gray
}
Pop-Location

# Step 3: Install Dependencies
Write-Host "[3/6] Installing Dependencies..." -ForegroundColor Yellow

# Backend
Push-Location "$ProjectRoot\backend"
if (Test-Path "venv\Scripts\pip.exe") {
    Write-Host "  → Backend dependencies" -ForegroundColor Gray
    .\venv\Scripts\pip.exe install -r requirements.txt -q 2>&1 | Out-Null
    Write-Host "  ✓ Backend dependencies installed" -ForegroundColor Green
}
Pop-Location

# Frontend
Push-Location "$ProjectRoot\frontend"
Write-Host "  → Frontend dependencies" -ForegroundColor Gray
npm ci --silent 2>&1 | Out-Null
Write-Host "  ✓ Frontend dependencies installed" -ForegroundColor Green
Pop-Location

# Step 4: Run Migrations
Write-Host "[4/6] Running Database Migrations..." -ForegroundColor Yellow
Push-Location "$ProjectRoot\backend"
if (Test-Path "venv\Scripts\flask.exe") {
    .\venv\Scripts\flask.exe db upgrade 2>&1 | Out-Null
    Write-Host "  ✓ Migrations applied" -ForegroundColor Green
} else {
    Write-Host "  → Skipping (flask not in venv)" -ForegroundColor Gray
}
Pop-Location

# Step 5: Build Frontend (for staging/production)
if ($Environment -ne "dev") {
    Write-Host "[5/6] Building Frontend..." -ForegroundColor Yellow
    Push-Location "$ProjectRoot\frontend"
    
    $env:NODE_ENV = "production"
    npm run build 2>&1 | Out-Null
    
    Write-Host "  ✓ Frontend built" -ForegroundColor Green
    Pop-Location
} else {
    Write-Host "[5/6] Skipping Frontend Build (dev mode)" -ForegroundColor Yellow
}

# Step 6: Start Services
Write-Host "[6/6] Starting Services..." -ForegroundColor Yellow

if ($DockerOnly) {
    # Docker deployment
    Push-Location $ProjectRoot
    docker network create Ai_project 2>$null
    docker-compose up -d
    Write-Host "  ✓ Docker services started" -ForegroundColor Green
    Pop-Location
} else {
    # Direct deployment
    Write-Host "  → Use start-dev.ps1 for local or docker-start.ps1 for Docker" -ForegroundColor Gray
}

# Summary
Write-Host ""
Write-Host "═══════════════════════════════════════════════════════════════════" -ForegroundColor Green
Write-Host ""
Write-Host "  ✅ Deployment Complete!" -ForegroundColor Green
Write-Host ""
Write-Host "  Environment:     $Environment" -ForegroundColor White
Write-Host "  Status:          Ready" -ForegroundColor Green
Write-Host ""

switch ($Environment) {
    "dev" {
        Write-Host "  URLs:" -ForegroundColor White
        Write-Host "  • Frontend: http://localhost:6501" -ForegroundColor Yellow
        Write-Host "  • Backend:  http://localhost:6001" -ForegroundColor Yellow
    }
    "staging" {
        Write-Host "  URLs:" -ForegroundColor White
        Write-Host "  • Frontend: http://staging.store-erp.local" -ForegroundColor Yellow
        Write-Host "  • Backend:  http://api.staging.store-erp.local" -ForegroundColor Yellow
    }
    "production" {
        Write-Host "  URLs:" -ForegroundColor White
        Write-Host "  • Frontend: https://store-erp.com" -ForegroundColor Yellow
        Write-Host "  • Backend:  https://api.store-erp.com" -ForegroundColor Yellow
    }
}

Write-Host ""
Write-Host "═══════════════════════════════════════════════════════════════════" -ForegroundColor Green
Write-Host ""
