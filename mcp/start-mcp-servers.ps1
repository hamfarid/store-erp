# ===========================================
# MCP Servers Startup Script
# ===========================================
# This script starts all MCP servers
# ===========================================

Write-Host "🚀 Starting MCP Servers..." -ForegroundColor Cyan
Write-Host ""

# Check if Docker is running
$dockerRunning = docker info 2>&1
if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Docker is not running. Please start Docker Desktop first." -ForegroundColor Red
    exit 1
}

# Navigate to MCP directory
Set-Location -Path "$PSScriptRoot"

# Check for .env file
if (Test-Path ".env") {
    Write-Host "✅ Found .env file with API keys" -ForegroundColor Green
    $hasEnv = $true
} else {
    Write-Host "⚠️  No .env file found. Only starting servers without API keys." -ForegroundColor Yellow
    Write-Host "   Copy env-template.txt to .env and add your API keys to enable more servers." -ForegroundColor Yellow
    $hasEnv = $false
}

Write-Host ""
Write-Host "Starting servers..." -ForegroundColor Cyan

if ($hasEnv) {
    # Start all servers including those with API keys
    docker-compose --profile with-api-keys up -d
} else {
    # Start only servers without API keys
    docker-compose up -d
}

Write-Host ""
Write-Host "📊 MCP Server Status:" -ForegroundColor Cyan
docker ps --filter "label=mcp.server" --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"

Write-Host ""
Write-Host "✅ MCP Servers started successfully!" -ForegroundColor Green
Write-Host ""
Write-Host "Available Commands:" -ForegroundColor Yellow
Write-Host "  - View logs:    docker-compose logs -f" -ForegroundColor White
Write-Host "  - Stop all:     docker-compose down" -ForegroundColor White
Write-Host "  - Restart:      docker-compose restart" -ForegroundColor White
