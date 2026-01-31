$projects = @(
    "d:\Ai_Project\1-test_projects\global - V1.3 -13-12-2025",
    "d:\Ai_Project\2-gold-price-predictor",
    "d:\Ai_Project\3-Zakat\Zakat_Clean",
    "d:\Ai_Project\4-scan_ai-Manus",
    "d:\Ai_Project\5-gaara_erp",
    "d:\Ai_Project\6-store"
)

Write-Host "Starting Global Nginx..." -ForegroundColor Cyan
Set-Location "d:\Ai_Project"
docker-compose -f docker-compose.global.yml up -d

foreach ($p in $projects) {
    Write-Host "Starting Project: $p" -ForegroundColor Cyan
    Set-Location $p
    docker-compose up -d
}

Write-Host "All projects started. Checking stats..." -ForegroundColor Green
docker ps --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"
docker stats --no-stream
