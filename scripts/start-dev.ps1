# =============================================================================
# Store ERP v2.0.0 - Development Start Script (PowerShell)
# =============================================================================
# Usage: .\scripts\start-dev.ps1
# =============================================================================

Write-Host ""
Write-Host "╔═══════════════════════════════════════════════════════════════════╗" -ForegroundColor Cyan
Write-Host "║           Store ERP v2.0.0 - Development Mode                     ║" -ForegroundColor Cyan
Write-Host "╚═══════════════════════════════════════════════════════════════════╝" -ForegroundColor Cyan
Write-Host ""

# Get project root directory
$ProjectRoot = Split-Path -Parent $PSScriptRoot

# Check if backend virtual environment exists
$VenvPath = Join-Path $ProjectRoot "backend\venv"
if (-Not (Test-Path $VenvPath)) {
    Write-Host "[!] Virtual environment not found. Creating..." -ForegroundColor Yellow
    Push-Location (Join-Path $ProjectRoot "backend")
    python -m venv venv
    .\venv\Scripts\Activate.ps1
    pip install -r requirements.txt
    Pop-Location
}

# Check if frontend node_modules exists
$NodeModulesPath = Join-Path $ProjectRoot "frontend\node_modules"
if (-Not (Test-Path $NodeModulesPath)) {
    Write-Host "[!] Node modules not found. Installing..." -ForegroundColor Yellow
    Push-Location (Join-Path $ProjectRoot "frontend")
    npm install
    Pop-Location
}

Write-Host ""
Write-Host "[INFO] Starting services..." -ForegroundColor Green
Write-Host ""

# Start backend in a new PowerShell window
Write-Host "[1/2] Starting Backend (Port 6001)..." -ForegroundColor Cyan
$BackendPath = Join-Path $ProjectRoot "backend"
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$BackendPath'; .\venv\Scripts\Activate.ps1; python app.py"

# Wait a moment for backend to start
Start-Sleep -Seconds 3

# Start frontend in a new PowerShell window
Write-Host "[2/2] Starting Frontend (Port 6501)..." -ForegroundColor Cyan
$FrontendPath = Join-Path $ProjectRoot "frontend"
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$FrontendPath'; npm run dev"

Write-Host ""
Write-Host "═══════════════════════════════════════════════════════════════════" -ForegroundColor Green
Write-Host ""
Write-Host "  Services Starting:" -ForegroundColor White
Write-Host "  • Backend API:  http://localhost:6001" -ForegroundColor Yellow
Write-Host "  • Frontend App: http://localhost:6501" -ForegroundColor Yellow
Write-Host ""
Write-Host "  Default Login:" -ForegroundColor White
Write-Host "  • Username: admin" -ForegroundColor Yellow
Write-Host "  • Password: admin123" -ForegroundColor Yellow
Write-Host ""
Write-Host "═══════════════════════════════════════════════════════════════════" -ForegroundColor Green
Write-Host ""
