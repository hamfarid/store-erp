# Start All Servers - Backend + Frontend
# نص تشغيل جميع الخوادم - الواجهة الخلفية + الواجهة الأمامية

Write-Host "🚀 Starting Complete Inventory Management System" -ForegroundColor Cyan
Write-Host "=================================================" -ForegroundColor Cyan

# Add Node.js to PATH
Write-Host "`n📦 Adding Node.js to PATH..." -ForegroundColor Yellow
$env:Path += ";F:\node-v22.20.0-win-x64"
$env:Path += ";F:\jdk1.8.0_461\bin"

# Verify Node.js
Write-Host "✅ Node.js version: " -NoNewline -ForegroundColor Green
node --version

Write-Host "✅ npm version: " -NoNewline -ForegroundColor Green
npm --version

# Start Backend
Write-Host "`n🔧 Starting Backend Server..." -ForegroundColor Yellow
Write-Host "Location: http://127.0.0.1:5002" -ForegroundColor Cyan

Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$PSScriptRoot\backend'; python app.py"

# Wait a bit for backend to start
Start-Sleep -Seconds 3

# Start Frontend
Write-Host "`n🎨 Starting Frontend Server..." -ForegroundColor Yellow
Write-Host "Location: http://localhost:5502" -ForegroundColor Cyan

Start-Process powershell -ArgumentList "-NoExit", "-Command", "`$env:Path += ';F:\node-v22.20.0-win-x64'; cd '$PSScriptRoot\frontend'; npm run dev"

# Wait a bit for frontend to start
Start-Sleep -Seconds 5

# Open browser
Write-Host "`n🌐 Opening browser..." -ForegroundColor Yellow
Start-Process "http://localhost:5502"

Write-Host "`n✅ All servers started successfully!" -ForegroundColor Green
Write-Host "`nBackend:  http://127.0.0.1:5002" -ForegroundColor Cyan
Write-Host "Frontend: http://localhost:5502" -ForegroundColor Cyan
Write-Host "`nLogin credentials:" -ForegroundColor Yellow
Write-Host "  Username: admin" -ForegroundColor White
Write-Host "  Password: admin123" -ForegroundColor White
Write-Host "`nPress any key to exit..." -ForegroundColor Gray
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")

