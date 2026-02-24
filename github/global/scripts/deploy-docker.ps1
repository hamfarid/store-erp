# ============================================================
# Store ERP v2.0.0 - Docker Deployment Script (Windows)
# ============================================================

param(
    [string]$Environment = "production",
    [switch]$Build,
    [switch]$Down,
    [switch]$Logs,
    [switch]$Status
)

$ErrorActionPreference = "Stop"
$ProjectRoot = Split-Path -Parent $PSScriptRoot

Write-Host "============================================" -ForegroundColor Cyan
Write-Host "  Store ERP v2.0.0 - Docker Deployment" -ForegroundColor Cyan
Write-Host "============================================" -ForegroundColor Cyan
Write-Host ""

# Check Docker
if (-not (Get-Command docker -ErrorAction SilentlyContinue)) {
    Write-Host "Error: Docker is not installed or not in PATH" -ForegroundColor Red
    exit 1
}

# Check if Docker daemon is running
try {
    docker info | Out-Null
} catch {
    Write-Host "Error: Docker daemon is not running" -ForegroundColor Red
    exit 1
}

Set-Location $ProjectRoot

# Handle different commands
if ($Down) {
    Write-Host "Stopping containers..." -ForegroundColor Yellow
    docker-compose -f docker-compose.yml down
    Write-Host "Containers stopped!" -ForegroundColor Green
    exit 0
}

if ($Logs) {
    Write-Host "Showing logs..." -ForegroundColor Yellow
    docker-compose -f docker-compose.yml logs -f --tail=100
    exit 0
}

if ($Status) {
    Write-Host "Container Status:" -ForegroundColor Yellow
    docker-compose -f docker-compose.yml ps
    Write-Host ""
    Write-Host "Resource Usage:" -ForegroundColor Yellow
    docker stats --no-stream --format "table {{.Name}}\t{{.CPUPerc}}\t{{.MemUsage}}"
    exit 0
}

# Build and deploy
Write-Host "Environment: $Environment" -ForegroundColor Cyan
Write-Host ""

# Check for .env file
if (-not (Test-Path ".env")) {
    Write-Host "Warning: .env file not found. Creating from example..." -ForegroundColor Yellow
    if (Test-Path "backend\env.example.txt") {
        Copy-Item "backend\env.example.txt" ".env"
        Write-Host "Created .env file. Please update with your configuration." -ForegroundColor Yellow
    }
}

# Build images
if ($Build) {
    Write-Host "Building Docker images..." -ForegroundColor Yellow
    docker-compose -f docker-compose.yml build --no-cache
}

# Start containers
Write-Host "Starting containers..." -ForegroundColor Yellow
docker-compose -f docker-compose.yml up -d

# Wait for services to be healthy
Write-Host ""
Write-Host "Waiting for services to be ready..." -ForegroundColor Yellow
$maxRetries = 30
$retryCount = 0

do {
    Start-Sleep -Seconds 2
    $backendHealth = docker-compose -f docker-compose.yml exec -T backend curl -s http://localhost:6001/api/health 2>$null
    $retryCount++
    Write-Host "." -NoNewline
} while (-not $backendHealth -and $retryCount -lt $maxRetries)

Write-Host ""

if ($backendHealth) {
    Write-Host ""
    Write-Host "============================================" -ForegroundColor Green
    Write-Host "  Deployment Complete!" -ForegroundColor Green
    Write-Host "============================================" -ForegroundColor Green
    Write-Host ""
    Write-Host "Services running:" -ForegroundColor Cyan
    Write-Host "  - Frontend:  http://localhost:6501" -ForegroundColor White
    Write-Host "  - Backend:   http://localhost:6001" -ForegroundColor White
    Write-Host "  - API Docs:  http://localhost:6001/api/docs" -ForegroundColor White
    Write-Host ""
    Write-Host "Useful commands:" -ForegroundColor Cyan
    Write-Host "  - View logs:    .\scripts\deploy-docker.ps1 -Logs" -ForegroundColor White
    Write-Host "  - Stop all:     .\scripts\deploy-docker.ps1 -Down" -ForegroundColor White
    Write-Host "  - Check status: .\scripts\deploy-docker.ps1 -Status" -ForegroundColor White
} else {
    Write-Host "Warning: Services may not be fully ready. Check logs with:" -ForegroundColor Yellow
    Write-Host "  docker-compose logs -f" -ForegroundColor White
}

Write-Host ""
docker-compose -f docker-compose.yml ps
