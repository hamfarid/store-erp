$projects = @(
    "d:\Ai_Project\1-test_projects\global - V1.3 -13-12-2025",
    "d:\Ai_Project\2-gold-price-predictor",
    "d:\Ai_Project\3-Zakat\Zakat_Clean"
)

foreach ($p in $projects) {
    Write-Host "Recreating Project: $p" -ForegroundColor Cyan
    Set-Location $p
    docker-compose down
    docker-compose up -d --build --force-recreate
}

Write-Host "P1, P2, P3 Restarted. Checking ports..." -ForegroundColor Green
docker ps --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}" | Select-String "global|gold|zakat"
