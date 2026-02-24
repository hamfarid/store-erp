# ============================================================
# Frontend Testing using MCP Playwright
# ============================================================

Write-Host "`n========================================" -ForegroundColor Cyan
Write-Host "🧪 Frontend Testing with MCP Playwright" -ForegroundColor Green
Write-Host "========================================`n" -ForegroundColor Cyan

# Check if frontend is running
Write-Host "📡 Checking if frontend is running..." -ForegroundColor Yellow
$frontendUrl = "http://localhost:5505"
$backendUrl = "http://localhost:5506"

try {
    $response = Invoke-WebRequest -Uri "$frontendUrl" -Method Get -TimeoutSec 5 -UseBasicParsing -ErrorAction Stop
    Write-Host "✅ Frontend is running on $frontendUrl" -ForegroundColor Green
} catch {
    Write-Host "❌ Frontend is not running on $frontendUrl" -ForegroundColor Red
    Write-Host "   Please start the frontend first: npm run dev" -ForegroundColor Yellow
    exit 1
}

try {
    $response = Invoke-WebRequest -Uri "$backendUrl/api/health" -Method Get -TimeoutSec 5 -UseBasicParsing -ErrorAction Stop
    Write-Host "✅ Backend is running on $backendUrl" -ForegroundColor Green
} catch {
    Write-Host "⚠️  Backend is not running on $backendUrl" -ForegroundColor Yellow
    Write-Host "   Some tests may fail without backend" -ForegroundColor Yellow
}

Write-Host "`n🚀 Starting MCP Playwright Tests...`n" -ForegroundColor Cyan

# Navigate to frontend directory
Set-Location frontend

# Run Playwright tests
Write-Host "Running E2E tests..." -ForegroundColor Yellow
npm run test:e2e

if ($LASTEXITCODE -eq 0) {
    Write-Host "`n✅ All tests passed!" -ForegroundColor Green
} else {
    Write-Host "`n❌ Some tests failed. Check the report for details." -ForegroundColor Red
    Write-Host "   Run 'npm run test:e2e:report' to view the HTML report" -ForegroundColor Yellow
}

Set-Location ..

Write-Host "`n========================================" -ForegroundColor Cyan
Write-Host "✨ Testing Complete!" -ForegroundColor Green
Write-Host "========================================`n" -ForegroundColor Cyan

