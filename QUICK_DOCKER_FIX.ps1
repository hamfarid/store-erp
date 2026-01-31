# Quick Docker Desktop Fix Script
# Run this script in PowerShell (as Administrator if needed)

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Docker Desktop Troubleshooting Script" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Step 1: Check if Docker Desktop is running
Write-Host "[1/5] Checking Docker Desktop status..." -ForegroundColor Yellow
try {
    $dockerVersion = docker version 2>&1
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✅ Docker Desktop is running!" -ForegroundColor Green
    } else {
        Write-Host "❌ Docker Desktop is not responding" -ForegroundColor Red
        Write-Host "   Error: $dockerVersion" -ForegroundColor Red
    }
} catch {
    Write-Host "❌ Docker Desktop is not running" -ForegroundColor Red
}

Write-Host ""

# Step 2: Check Docker Desktop process
Write-Host "[2/5] Checking Docker Desktop process..." -ForegroundColor Yellow
$dockerProcess = Get-Process -Name "Docker Desktop" -ErrorAction SilentlyContinue
if ($dockerProcess) {
    Write-Host "✅ Docker Desktop process found (PID: $($dockerProcess.Id))" -ForegroundColor Green
} else {
    Write-Host "❌ Docker Desktop process not found" -ForegroundColor Red
    Write-Host "   Please start Docker Desktop manually" -ForegroundColor Yellow
}

Write-Host ""

# Step 3: Try to restart Docker Desktop
Write-Host "[3/5] Attempting to restart Docker Desktop..." -ForegroundColor Yellow
try {
    # Stop Docker Desktop
    Stop-Process -Name "Docker Desktop" -Force -ErrorAction SilentlyContinue
    Write-Host "   Stopped Docker Desktop..." -ForegroundColor Yellow
    Start-Sleep -Seconds 5
    
    # Start Docker Desktop
    $dockerPath = "C:\Program Files\Docker\Docker\Docker Desktop.exe"
    if (Test-Path $dockerPath) {
        Start-Process $dockerPath
        Write-Host "   Started Docker Desktop..." -ForegroundColor Yellow
        Write-Host "   Waiting for Docker Desktop to initialize (30 seconds)..." -ForegroundColor Yellow
        Start-Sleep -Seconds 30
    } else {
        Write-Host "   ⚠️  Docker Desktop not found at default path" -ForegroundColor Yellow
        Write-Host "   Please start Docker Desktop manually" -ForegroundColor Yellow
    }
} catch {
    Write-Host "   ⚠️  Could not restart Docker Desktop automatically" -ForegroundColor Yellow
    Write-Host "   Please restart Docker Desktop manually" -ForegroundColor Yellow
}

Write-Host ""

# Step 4: Verify Docker is working
Write-Host "[4/5] Verifying Docker is working..." -ForegroundColor Yellow
Start-Sleep -Seconds 5
try {
    $dockerPs = docker ps 2>&1
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✅ Docker is working!" -ForegroundColor Green
    } else {
        Write-Host "❌ Docker is still not responding" -ForegroundColor Red
        Write-Host "   Error: $dockerPs" -ForegroundColor Red
    }
} catch {
    Write-Host "❌ Docker is still not responding" -ForegroundColor Red
}

Write-Host ""

# Step 5: Final instructions
Write-Host "[5/5] Final Instructions" -ForegroundColor Yellow
Write-Host ""
Write-Host "If Docker is still not working, try:" -ForegroundColor Cyan
Write-Host "  1. Restart your computer" -ForegroundColor White
Write-Host "  2. Update Docker Desktop to the latest version" -ForegroundColor White
Write-Host "  3. Check Windows Updates" -ForegroundColor White
Write-Host "  4. Reinstall Docker Desktop if necessary" -ForegroundColor White
Write-Host ""
Write-Host "Once Docker is working, run:" -ForegroundColor Cyan
Write-Host "  cd D:\Ai_Project\4-scan_ai-Manus" -ForegroundColor White
Write-Host "  docker-compose build ml_service" -ForegroundColor White
Write-Host "  docker-compose up -d ml_service" -ForegroundColor White
Write-Host ""
