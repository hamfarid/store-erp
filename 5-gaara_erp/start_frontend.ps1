# ============================================================
# بدء Frontend Server
# Start Frontend Server
# ============================================================

Write-Host "`n🎨 بدء Frontend Server..." -ForegroundColor Cyan

# الانتقال إلى مجلد Frontend
Set-Location frontend

# التحقق من تثبيت المتطلبات
if (-not (Test-Path "node_modules")) {
    Write-Host "📦 تثبيت المتطلبات..." -ForegroundColor Yellow
    npm install
}

# بدء الخادم
Write-Host "🚀 بدء Frontend على المنفذ 5505..." -ForegroundColor Green
Write-Host "📍 http://localhost:5505`n" -ForegroundColor Cyan

npm run dev

