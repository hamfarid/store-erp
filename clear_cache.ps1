# مسح جميع ملفات الكاش - Clear All Cache Files
Write-Host "🧹 بدء مسح ملفات الكاش..." -ForegroundColor Cyan

# Frontend Cache
Write-Host "`n📦 مسح كاش Frontend..." -ForegroundColor Yellow
if (Test-Path "frontend\node_modules\.vite") {
    Remove-Item -Path "frontend\node_modules\.vite" -Recurse -Force
    Write-Host "✅ تم مسح .vite cache" -ForegroundColor Green
}

if (Test-Path "frontend\dist") {
    Remove-Item -Path "frontend\dist" -Recurse -Force
    Write-Host "✅ تم مسح dist folder" -ForegroundColor Green
}

# Backend Cache
Write-Host "`n🐍 مسح كاش Backend..." -ForegroundColor Yellow
if (Test-Path "backend\__pycache__") {
    Remove-Item -Path "backend\__pycache__" -Recurse -Force
    Write-Host "✅ تم مسح backend __pycache__" -ForegroundColor Green
}

if (Test-Path "backend\src\__pycache__") {
    Remove-Item -Path "backend\src\__pycache__" -Recurse -Force
    Write-Host "✅ تم مسح src __pycache__" -ForegroundColor Green
}

if (Test-Path "backend\flask_session") {
    Remove-Item -Path "backend\flask_session" -Recurse -Force
    Write-Host "✅ تم مسح flask_session" -ForegroundColor Green
}

# Root Cache
Write-Host "`n📁 مسح كاش Root..." -ForegroundColor Yellow
if (Test-Path "__pycache__") {
    Remove-Item -Path "__pycache__" -Recurse -Force
    Write-Host "✅ تم مسح root __pycache__" -ForegroundColor Green
}

Write-Host "`n✅ تم مسح جميع ملفات الكاش بنجاح!" -ForegroundColor Green
Write-Host "💡 يمكنك الآن تشغيل السيرفرات من جديد" -ForegroundColor Cyan

