# =============================================================================
# Gaara ERP - Development Startup Script
# سكريبت بدء التطوير
#
# Author: Global v35.0 Singularity
# Created: 2026-01-17
#
# Usage: .\scripts\start-dev.ps1
# =============================================================================

param(
    [switch]$Backend,
    [switch]$Frontend,
    [switch]$Both,
    [switch]$Docker,
    [switch]$Help
)

$ErrorActionPreference = "Stop"

# Colors for output
function Write-ColorOutput($ForegroundColor) {
    $fc = $host.UI.RawUI.ForegroundColor
    $host.UI.RawUI.ForegroundColor = $ForegroundColor
    if ($args) {
        Write-Output $args
    }
    $host.UI.RawUI.ForegroundColor = $fc
}

function Show-Banner {
    Write-Host ""
    Write-Host "  ╔═══════════════════════════════════════════════╗" -ForegroundColor Cyan
    Write-Host "  ║                                               ║" -ForegroundColor Cyan
    Write-Host "  ║        🏢 GAARA ERP v12 - Development        ║" -ForegroundColor Cyan
    Write-Host "  ║                                               ║" -ForegroundColor Cyan
    Write-Host "  ╚═══════════════════════════════════════════════╝" -ForegroundColor Cyan
    Write-Host ""
}

function Show-Help {
    Show-Banner
    Write-Host "Usage: .\start-dev.ps1 [options]" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "Options:" -ForegroundColor Green
    Write-Host "  -Backend     Start backend server only"
    Write-Host "  -Frontend    Start frontend development server only"
    Write-Host "  -Both        Start both backend and frontend (default)"
    Write-Host "  -Docker      Start using Docker Compose"
    Write-Host "  -Help        Show this help message"
    Write-Host ""
    Write-Host "Examples:" -ForegroundColor Green
    Write-Host "  .\start-dev.ps1 -Both"
    Write-Host "  .\start-dev.ps1 -Backend"
    Write-Host "  .\start-dev.ps1 -Docker"
    Write-Host ""
}

function Start-Backend {
    Write-Host "🐍 Starting Backend Server..." -ForegroundColor Green
    
    $backendPath = Join-Path $PSScriptRoot "..\backend"
    
    if (-not (Test-Path $backendPath)) {
        Write-Host "❌ Backend directory not found!" -ForegroundColor Red
        return
    }
    
    Push-Location $backendPath
    
    # Check for virtual environment
    if (Test-Path "venv\Scripts\Activate.ps1") {
        Write-Host "  📦 Activating virtual environment..." -ForegroundColor Cyan
        & "venv\Scripts\Activate.ps1"
    }
    
    # Check for requirements
    if (Test-Path "requirements.txt") {
        Write-Host "  📥 Installing dependencies..." -ForegroundColor Cyan
        pip install -r requirements.txt -q
    }
    
    # Set environment variables
    $env:FLASK_ENV = "development"
    $env:FLASK_DEBUG = "1"
    
    Write-Host "  🚀 Starting Flask server on http://localhost:5000" -ForegroundColor Yellow
    
    # Start the server
    Start-Process -NoNewWindow -FilePath "python" -ArgumentList "src/main.py"
    
    Pop-Location
}

function Start-Frontend {
    Write-Host "⚛️  Starting Frontend Development Server..." -ForegroundColor Green
    
    $frontendPath = Join-Path $PSScriptRoot "..\gaara-erp-frontend"
    
    if (-not (Test-Path $frontendPath)) {
        Write-Host "❌ Frontend directory not found!" -ForegroundColor Red
        return
    }
    
    Push-Location $frontendPath
    
    # Check if pnpm is available
    $pnpmExists = Get-Command pnpm -ErrorAction SilentlyContinue
    
    if ($pnpmExists) {
        Write-Host "  📦 Installing dependencies with pnpm..." -ForegroundColor Cyan
        pnpm install
        
        Write-Host "  🚀 Starting Vite dev server on http://localhost:5173" -ForegroundColor Yellow
        Start-Process -NoNewWindow -FilePath "pnpm" -ArgumentList "run", "dev"
    } else {
        Write-Host "  📦 Installing dependencies with npm..." -ForegroundColor Cyan
        npm install
        
        Write-Host "  🚀 Starting Vite dev server on http://localhost:5173" -ForegroundColor Yellow
        Start-Process -NoNewWindow -FilePath "npm" -ArgumentList "run", "dev"
    }
    
    Pop-Location
}

function Start-WithDocker {
    Write-Host "🐳 Starting with Docker Compose..." -ForegroundColor Green
    
    $rootPath = Join-Path $PSScriptRoot ".."
    Push-Location $rootPath
    
    # Check for docker-compose
    $dockerComposeExists = Get-Command docker-compose -ErrorAction SilentlyContinue
    
    if (-not $dockerComposeExists) {
        Write-Host "❌ Docker Compose not found! Please install Docker." -ForegroundColor Red
        Pop-Location
        return
    }
    
    Write-Host "  🏗️  Building and starting containers..." -ForegroundColor Cyan
    docker-compose up -d --build
    
    Write-Host ""
    Write-Host "  ✅ Services started:" -ForegroundColor Green
    Write-Host "     - Backend:  http://localhost:5000" -ForegroundColor White
    Write-Host "     - Frontend: http://localhost:3000" -ForegroundColor White
    Write-Host "     - API Docs: http://localhost:5000/api/docs" -ForegroundColor White
    Write-Host ""
    
    Pop-Location
}

# Main execution
if ($Help) {
    Show-Help
    exit 0
}

Show-Banner

if ($Docker) {
    Start-WithDocker
} elseif ($Backend) {
    Start-Backend
} elseif ($Frontend) {
    Start-Frontend
} else {
    # Default: start both
    Start-Backend
    Start-Sleep -Seconds 3
    Start-Frontend
}

Write-Host ""
Write-Host "✨ Development environment started!" -ForegroundColor Green
Write-Host ""
Write-Host "Press Ctrl+C to stop servers" -ForegroundColor Yellow
Write-Host ""
