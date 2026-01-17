# =============================================================================
# Store ERP v2.0.0 - Docker Start Script (PowerShell)
# =============================================================================
# Usage: .\scripts\docker-start.ps1 [up|down|logs|build|restart]
# =============================================================================

param(
    [string]$Action = "up"
)

$ProjectRoot = Split-Path -Parent $PSScriptRoot

Write-Host ""
Write-Host "╔═══════════════════════════════════════════════════════════════════╗" -ForegroundColor Cyan
Write-Host "║           Store ERP v2.0.0 - Docker Management                    ║" -ForegroundColor Cyan
Write-Host "╚═══════════════════════════════════════════════════════════════════╝" -ForegroundColor Cyan
Write-Host ""

Push-Location $ProjectRoot

# Create network if not exists
$networkExists = docker network ls --format "{{.Name}}" | Where-Object { $_ -eq "Ai_project" }
if (-Not $networkExists) {
    Write-Host "[INFO] Creating Docker network 'Ai_project'..." -ForegroundColor Yellow
    docker network create Ai_project
}

switch ($Action.ToLower()) {
    "up" {
        Write-Host "[INFO] Starting all services..." -ForegroundColor Green
        docker-compose up -d
        Write-Host ""
        Write-Host "[INFO] Services started. Checking health..." -ForegroundColor Green
        Start-Sleep -Seconds 5
        docker-compose ps
    }
    "down" {
        Write-Host "[INFO] Stopping all services..." -ForegroundColor Yellow
        docker-compose down
    }
    "logs" {
        Write-Host "[INFO] Showing logs (Ctrl+C to exit)..." -ForegroundColor Cyan
        docker-compose logs -f
    }
    "build" {
        Write-Host "[INFO] Building images..." -ForegroundColor Green
        docker-compose build --no-cache
    }
    "restart" {
        Write-Host "[INFO] Restarting all services..." -ForegroundColor Yellow
        docker-compose restart
    }
    "status" {
        docker-compose ps
    }
    default {
        Write-Host "Usage: .\docker-start.ps1 [up|down|logs|build|restart|status]" -ForegroundColor Yellow
    }
}

Pop-Location

Write-Host ""
Write-Host "═══════════════════════════════════════════════════════════════════" -ForegroundColor Green
Write-Host ""
Write-Host "  Service URLs:" -ForegroundColor White
Write-Host "  • Main App:     http://localhost" -ForegroundColor Yellow
Write-Host "  • Backend API:  http://localhost:6001/api" -ForegroundColor Yellow
Write-Host "  • Frontend:     http://localhost:6501" -ForegroundColor Yellow
Write-Host ""
Write-Host "═══════════════════════════════════════════════════════════════════" -ForegroundColor Green
Write-Host ""
