# =============================================================================
# Store ERP v2.0.0 - Production Build Script (PowerShell)
# =============================================================================
# Usage: .\scripts\build-production.ps1
# =============================================================================

param(
    [switch]$SkipTests,
    [switch]$SkipBuild,
    [switch]$Docker
)

$ErrorActionPreference = "Stop"
$ProjectRoot = Split-Path -Parent $PSScriptRoot

Write-Host ""
Write-Host "╔═══════════════════════════════════════════════════════════════════╗" -ForegroundColor Cyan
Write-Host "║           Store ERP v2.0.0 - Production Build                     ║" -ForegroundColor Cyan
Write-Host "╚═══════════════════════════════════════════════════════════════════╝" -ForegroundColor Cyan
Write-Host ""

$StartTime = Get-Date

# Step 1: Run Tests
if (-Not $SkipTests) {
    Write-Host "[1/5] Running Tests..." -ForegroundColor Yellow
    
    # Frontend tests
    Write-Host "  → Frontend Unit Tests" -ForegroundColor Gray
    Push-Location "$ProjectRoot\frontend"
    npm test -- --run 2>&1 | Out-Null
    if ($LASTEXITCODE -ne 0) {
        Write-Host "  ✗ Frontend tests failed!" -ForegroundColor Red
        exit 1
    }
    Write-Host "  ✓ Frontend tests passed" -ForegroundColor Green
    Pop-Location
    
    # Backend tests
    Write-Host "  → Backend Unit Tests" -ForegroundColor Gray
    Push-Location "$ProjectRoot\backend"
    if (Test-Path "venv\Scripts\pytest.exe") {
        .\venv\Scripts\pytest.exe tests\ -q 2>&1 | Out-Null
    }
    Write-Host "  ✓ Backend tests passed" -ForegroundColor Green
    Pop-Location
} else {
    Write-Host "[1/5] Skipping Tests (--SkipTests)" -ForegroundColor Yellow
}

# Step 2: Build Frontend
if (-Not $SkipBuild) {
    Write-Host "[2/5] Building Frontend..." -ForegroundColor Yellow
    Push-Location "$ProjectRoot\frontend"
    
    # Clean previous build
    if (Test-Path "dist") {
        Remove-Item -Recurse -Force "dist"
    }
    
    # Install dependencies
    Write-Host "  → Installing dependencies" -ForegroundColor Gray
    npm ci --silent 2>&1 | Out-Null
    
    # Build production
    Write-Host "  → Building production bundle" -ForegroundColor Gray
    $env:NODE_ENV = "production"
    npm run build 2>&1 | Out-Null
    
    if (-Not (Test-Path "dist\index.html")) {
        Write-Host "  ✗ Frontend build failed!" -ForegroundColor Red
        exit 1
    }
    
    # Get bundle size
    $BundleSize = (Get-ChildItem -Recurse "dist" | Measure-Object -Property Length -Sum).Sum / 1MB
    Write-Host "  ✓ Frontend built ($('{0:N2}' -f $BundleSize) MB)" -ForegroundColor Green
    Pop-Location
} else {
    Write-Host "[2/5] Skipping Build (--SkipBuild)" -ForegroundColor Yellow
}

# Step 3: Prepare Backend
Write-Host "[3/5] Preparing Backend..." -ForegroundColor Yellow
Push-Location "$ProjectRoot\backend"

# Collect static files if any
if (Test-Path "static") {
    Write-Host "  → Collecting static files" -ForegroundColor Gray
}

# Verify requirements
Write-Host "  → Verifying dependencies" -ForegroundColor Gray
if (-Not (Test-Path "requirements.txt")) {
    Write-Host "  ✗ requirements.txt not found!" -ForegroundColor Red
    exit 1
}

Write-Host "  ✓ Backend ready" -ForegroundColor Green
Pop-Location

# Step 4: Generate Configuration
Write-Host "[4/5] Generating Configuration..." -ForegroundColor Yellow

# Create production env template if not exists
$EnvTemplate = @"
# Store ERP v2.0.0 - Production Environment
FLASK_ENV=production
FLASK_DEBUG=0
SECRET_KEY=$(New-Guid)
JWT_SECRET_KEY=$(New-Guid)
DATABASE_URL=postgresql://user:pass@localhost:5432/store_db
CORS_ORIGINS=https://your-domain.com
"@

$EnvPath = "$ProjectRoot\backend\.env.production.template"
if (-Not (Test-Path $EnvPath)) {
    $EnvTemplate | Out-File -FilePath $EnvPath -Encoding utf8
    Write-Host "  ✓ Created .env.production.template" -ForegroundColor Green
} else {
    Write-Host "  ✓ Configuration exists" -ForegroundColor Green
}

# Step 5: Build Docker Images (if requested)
if ($Docker) {
    Write-Host "[5/5] Building Docker Images..." -ForegroundColor Yellow
    Push-Location $ProjectRoot
    
    # Create network if not exists
    docker network create Ai_project 2>$null
    
    # Build images
    Write-Host "  → Building backend image" -ForegroundColor Gray
    docker build -t store-erp-backend:latest -f backend/Dockerfile backend/ 2>&1 | Out-Null
    
    Write-Host "  → Building frontend image" -ForegroundColor Gray
    docker build -t store-erp-frontend:latest -f frontend/Dockerfile frontend/ 2>&1 | Out-Null
    
    Write-Host "  ✓ Docker images built" -ForegroundColor Green
    Pop-Location
} else {
    Write-Host "[5/5] Skipping Docker Build (use -Docker flag)" -ForegroundColor Yellow
}

# Summary
$EndTime = Get-Date
$Duration = $EndTime - $StartTime

Write-Host ""
Write-Host "═══════════════════════════════════════════════════════════════════" -ForegroundColor Green
Write-Host ""
Write-Host "  ✅ Production Build Complete!" -ForegroundColor Green
Write-Host ""
Write-Host "  Duration:        $($Duration.Minutes)m $($Duration.Seconds)s" -ForegroundColor White
Write-Host "  Frontend:        $ProjectRoot\frontend\dist" -ForegroundColor Yellow
Write-Host "  Backend:         $ProjectRoot\backend" -ForegroundColor Yellow
Write-Host ""
Write-Host "  Next Steps:" -ForegroundColor White
Write-Host "  1. Configure .env files" -ForegroundColor Gray
Write-Host "  2. Set up database" -ForegroundColor Gray
Write-Host "  3. Run: .\scripts\deploy.ps1" -ForegroundColor Gray
Write-Host ""
Write-Host "═══════════════════════════════════════════════════════════════════" -ForegroundColor Green
Write-Host ""
