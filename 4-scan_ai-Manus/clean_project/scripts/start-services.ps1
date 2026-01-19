# Simple script to start services and run the application

Write-Host "Starting Docker services..." -ForegroundColor Green
docker-compose -f docker-compose.services-only.yml up -d

Write-Host "`nWaiting for services to start..." -ForegroundColor Yellow
Start-Sleep -Seconds 10

# Set environment variables
$env:DB_HOST = "localhost"
$env:DB_PORT = "5432"
$env:DB_NAME = "agri_ai_db"
$env:DB_USER = "postgres"
$env:DB_PASSWORD = "postgres"
$env:REDIS_HOST = "localhost"
$env:REDIS_PORT = "6379"
$env:SECRET_KEY = "Gaara_AI_Super_Secret_Key_2024_Agricultural_System!"
$env:DEBUG = "true"
$env:LOG_LEVEL = "DEBUG"
$env:API_HOST = "0.0.0.0"
$env:API_PORT = "8031"

Write-Host "`nEnvironment variables set." -ForegroundColor Green
Write-Host "`nStarting the application..." -ForegroundColor Green
Write-Host "Press Ctrl+C to stop`n" -ForegroundColor Yellow

python run_app.py 