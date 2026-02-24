# ============================================================
# نظام إدارة المخزون - تهيئة شاملة
# Store Management System - Complete Initialization
# ============================================================

Write-Host "`n========================================" -ForegroundColor Cyan
Write-Host "🚀 تهيئة نظام إدارة المخزون" -ForegroundColor Green
Write-Host "Store Management System Initialization" -ForegroundColor Green
Write-Host "========================================`n" -ForegroundColor Cyan

# التحقق من البيئة الافتراضية
$venvPath = ".venv"
if (-not (Test-Path $venvPath)) {
    Write-Host "⚠️  البيئة الافتراضية غير موجودة. جاري الإنشاء..." -ForegroundColor Yellow
    python -m venv $venvPath
    Write-Host "✅ تم إنشاء البيئة الافتراضية" -ForegroundColor Green
}

# تفعيل البيئة الافتراضية
Write-Host "`n📦 تفعيل البيئة الافتراضية..." -ForegroundColor Cyan
& "$venvPath\Scripts\Activate.ps1"

# ============================================================
# 1. تهيئة قاعدة البيانات
# ============================================================
Write-Host "`n📊 [1/3] تهيئة قاعدة البيانات..." -ForegroundColor Cyan

$dbPath = "backend\instance\inventory.db"
$dbDir = "backend\instance"

# إنشاء مجلد instance إذا لم يكن موجوداً
if (-not (Test-Path $dbDir)) {
    New-Item -ItemType Directory -Path $dbDir -Force | Out-Null
    Write-Host "✅ تم إنشاء مجلد قاعدة البيانات" -ForegroundColor Green
}

# التحقق من وجود قاعدة البيانات
if (Test-Path $dbPath) {
    Write-Host "✅ قاعدة البيانات موجودة: $dbPath" -ForegroundColor Green
} else {
    Write-Host "⚠️  قاعدة البيانات غير موجودة. جاري التهيئة..." -ForegroundColor Yellow
    
    # تشغيل سكريبت تهيئة قاعدة البيانات
    Set-Location backend
    python init_db.py
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✅ تم تهيئة قاعدة البيانات بنجاح" -ForegroundColor Green
    } else {
        Write-Host "❌ فشل تهيئة قاعدة البيانات" -ForegroundColor Red
        Set-Location ..
        exit 1
    }
    Set-Location ..
}

# ============================================================
# 2. التحقق من تثبيت المتطلبات
# ============================================================
Write-Host "`n📦 [2/3] التحقق من المتطلبات..." -ForegroundColor Cyan

# متطلبات Backend
Write-Host "   جاري التحقق من متطلبات Backend..." -ForegroundColor Gray
if (Test-Path "backend\requirements.txt") {
    $backendInstalled = python -c "import flask" 2>$null
    if (-not $backendInstalled) {
        Write-Host "   ⚠️  تثبيت متطلبات Backend..." -ForegroundColor Yellow
        Set-Location backend
        pip install -r requirements.txt
        Set-Location ..
        Write-Host "   ✅ تم تثبيت متطلبات Backend" -ForegroundColor Green
    } else {
        Write-Host "   ✅ متطلبات Backend مثبتة" -ForegroundColor Green
    }
} else {
    Write-Host "   ⚠️  ملف requirements.txt غير موجود" -ForegroundColor Yellow
}

# متطلبات Frontend
Write-Host "   جاري التحقق من متطلبات Frontend..." -ForegroundColor Gray
if (Test-Path "frontend\node_modules") {
    Write-Host "   ✅ متطلبات Frontend مثبتة" -ForegroundColor Green
} else {
    Write-Host "   ⚠️  تثبيت متطلبات Frontend..." -ForegroundColor Yellow
    Set-Location frontend
    npm install
    Set-Location ..
    Write-Host "   ✅ تم تثبيت متطلبات Frontend" -ForegroundColor Green
}

# ============================================================
# 3. بدء الخوادم
# ============================================================
Write-Host "`n🚀 [3/3] بدء الخوادم..." -ForegroundColor Cyan

# بدء Backend في نافذة منفصلة
Write-Host "`n   🔧 بدء Backend Server (Port 5506)..." -ForegroundColor Yellow
$backendScript = @"
cd backend
python -m src.main
"@

Start-Process powershell -ArgumentList "-NoExit", "-Command", $backendScript -WindowStyle Normal
Start-Sleep -Seconds 3

# بدء Frontend في نافذة منفصلة
Write-Host "   🎨 بدء Frontend Server (Port 5505)..." -ForegroundColor Yellow
$frontendScript = @"
cd frontend
npm run dev
"@

Start-Process powershell -ArgumentList "-NoExit", "-Command", $frontendScript -WindowStyle Normal
Start-Sleep -Seconds 3

# ============================================================
# ملخص
# ============================================================
Write-Host "`n========================================" -ForegroundColor Cyan
Write-Host "✅ تم التهيئة بنجاح!" -ForegroundColor Green
Write-Host "========================================`n" -ForegroundColor Cyan

Write-Host "📍 الروابط:" -ForegroundColor Yellow
Write-Host "   Frontend:  http://localhost:5505" -ForegroundColor White
Write-Host "   Backend:   http://localhost:5506" -ForegroundColor White
Write-Host "   Health:    http://localhost:5506/api/health" -ForegroundColor White

Write-Host "`n📝 ملاحظات:" -ForegroundColor Yellow
Write-Host "   - تم فتح نافذتين منفصلتين للخوادم" -ForegroundColor Gray
Write-Host "   - يمكنك إغلاق هذه النافذة بأمان" -ForegroundColor Gray
Write-Host "   - لإيقاف الخوادم، أغلق النوافذ المفتوحة" -ForegroundColor Gray

Write-Host "`n✨ جاهز للاستخدام!" -ForegroundColor Green
Write-Host ""

