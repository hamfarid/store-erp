# ============================================================
# بدء Backend Server
# Start Backend Server
# ============================================================

Write-Host "`n🔧 بدء Backend Server..." -ForegroundColor Cyan

# تفعيل البيئة الافتراضية
if (Test-Path ".venv\Scripts\Activate.ps1") {
    & ".venv\Scripts\Activate.ps1"
} else {
    Write-Host "⚠️  البيئة الافتراضية غير موجودة" -ForegroundColor Yellow
}

# الانتقال إلى مجلد Backend
Set-Location backend

# التحقق من قاعدة البيانات
if (-not (Test-Path "instance\inventory.db")) {
    Write-Host "📊 تهيئة قاعدة البيانات..." -ForegroundColor Yellow
    python init_db.py
}

# بدء الخادم
Write-Host "🚀 بدء Backend على المنفذ 5506..." -ForegroundColor Green
Write-Host "📍 http://localhost:5506" -ForegroundColor Cyan
Write-Host "🔗 Health: http://localhost:5506/api/health`n" -ForegroundColor Cyan

python -m src.main
