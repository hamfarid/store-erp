# Refresh environment variables and install npm packages
# This script reloads PATH and runs npm install

Write-Host "🔄 Refreshing environment variables..." -ForegroundColor Cyan

# Refresh PATH from registry
$env:Path = [System.Environment]::GetEnvironmentVariable("Path","Machine") + ";" + [System.Environment]::GetEnvironmentVariable("Path","User")

Write-Host "✅ Environment variables refreshed" -ForegroundColor Green

# Check if Node.js is available
Write-Host "`n📦 Checking Node.js installation..." -ForegroundColor Cyan

try {
    $nodeVersion = & node --version 2>&1
    Write-Host "✅ Node.js version: $nodeVersion" -ForegroundColor Green
} catch {
    Write-Host "❌ Node.js not found in PATH" -ForegroundColor Red
    Write-Host "Please close this PowerShell window and open a new one." -ForegroundColor Yellow
    exit 1
}

# Check if npm is available
try {
    $npmVersion = & npm --version 2>&1
    Write-Host "✅ npm version: $npmVersion" -ForegroundColor Green
} catch {
    Write-Host "❌ npm not found in PATH" -ForegroundColor Red
    exit 1
}

# Navigate to frontend directory
Write-Host "`n📁 Navigating to frontend directory..." -ForegroundColor Cyan
Set-Location -Path "D:\APPS_AI\store\store_v1.6\frontend"

# Install npm packages
Write-Host "`n📦 Installing npm packages..." -ForegroundColor Cyan
Write-Host "This may take 2-5 minutes..." -ForegroundColor Yellow

& npm install

if ($LASTEXITCODE -eq 0) {
    Write-Host "`n✅ npm packages installed successfully!" -ForegroundColor Green
    Write-Host "`n🚀 To start the development server, run:" -ForegroundColor Cyan
    Write-Host "   npm run dev" -ForegroundColor White
} else {
    Write-Host "`n❌ npm install failed" -ForegroundColor Red
    Write-Host "Please check the error messages above." -ForegroundColor Yellow
}

