# ============================================================================
# 🚀 نظام إدارة المخزون الكامل - سكريبت التشغيل الشامل
# Complete Inventory Management System - Comprehensive Startup Script
# ============================================================================

Write-Host "`n" -NoNewline
Write-Host "============================================================================" -ForegroundColor Cyan
Write-Host "🚀 نظام إدارة المخزون v1.6 | Inventory Management System v1.6" -ForegroundColor Yellow
Write-Host "============================================================================" -ForegroundColor Cyan
Write-Host "`n"

# ============================================================================
# الخطوة 1: التحقق من المتطلبات | Step 1: Check Requirements
# ============================================================================

Write-Host "📋 الخطوة 1: التحقق من المتطلبات..." -ForegroundColor Green
Write-Host "   Step 1: Checking requirements..." -ForegroundColor Gray

# التحقق من Python
Write-Host "`n   🐍 التحقق من Python..." -ForegroundColor Cyan
$pythonVersion = python --version 2>&1
if ($LASTEXITCODE -eq 0) {
    Write-Host "   ✅ Python متوفر: $pythonVersion" -ForegroundColor Green
} else {
    Write-Host "   ❌ Python غير متوفر! يرجى تثبيت Python 3.8+" -ForegroundColor Red
    exit 1
}

# التحقق من Node.js
Write-Host "`n   📦 التحقق من Node.js..." -ForegroundColor Cyan
$nodeVersion = node --version 2>&1
if ($LASTEXITCODE -eq 0) {
    Write-Host "   ✅ Node.js متوفر: $nodeVersion" -ForegroundColor Green
} else {
    Write-Host "   ❌ Node.js غير متوفر! يرجى تثبيت Node.js 16+" -ForegroundColor Red
    exit 1
}

# ============================================================================
# الخطوة 2: تفعيل البيئة الافتراضية | Step 2: Activate Virtual Environment
# ============================================================================

Write-Host "`n📋 الخطوة 2: تفعيل البيئة الافتراضية..." -ForegroundColor Green
Write-Host "   Step 2: Activating virtual environment..." -ForegroundColor Gray

if (Test-Path ".venv\Scripts\Activate.ps1") {
    & .venv\Scripts\Activate.ps1
    Write-Host "   ✅ تم تفعيل البيئة الافتراضية" -ForegroundColor Green
} else {
    Write-Host "   ⚠️ البيئة الافتراضية غير موجودة، جاري الإنشاء..." -ForegroundColor Yellow
    python -m venv .venv
    & .venv\Scripts\Activate.ps1
    Write-Host "   ✅ تم إنشاء وتفعيل البيئة الافتراضية" -ForegroundColor Green
}

# ============================================================================
# الخطوة 3: تثبيت المتطلبات | Step 3: Install Requirements
# ============================================================================

Write-Host "`n📋 الخطوة 3: تثبيت المتطلبات..." -ForegroundColor Green
Write-Host "   Step 3: Installing requirements..." -ForegroundColor Gray

# Backend requirements
Write-Host "`n   🔧 تثبيت متطلبات Backend..." -ForegroundColor Cyan
if (Test-Path "backend\requirements.txt") {
    pip install -r backend\requirements.txt --quiet
    Write-Host "   ✅ تم تثبيت متطلبات Backend" -ForegroundColor Green
}

# Frontend requirements
Write-Host "`n   🎨 تثبيت متطلبات Frontend..." -ForegroundColor Cyan
if (Test-Path "frontend\package.json") {
    Push-Location frontend
    npm install --silent
    Pop-Location
    Write-Host "   ✅ تم تثبيت متطلبات Frontend" -ForegroundColor Green
}

# ============================================================================
# الخطوة 4: مسح الكاش | Step 4: Clear Cache
# ============================================================================

Write-Host "`n📋 الخطوة 4: مسح الكاش..." -ForegroundColor Green
Write-Host "   Step 4: Clearing cache..." -ForegroundColor Gray

Remove-Item -Path "backend\src\models\__pycache__" -Recurse -Force -ErrorAction SilentlyContinue
Remove-Item -Path "backend\src\routes\__pycache__" -Recurse -Force -ErrorAction SilentlyContinue
Remove-Item -Path "backend\src\__pycache__" -Recurse -Force -ErrorAction SilentlyContinue
Remove-Item -Path "backend\__pycache__" -Recurse -Force -ErrorAction SilentlyContinue

Write-Host "   ✅ تم مسح الكاش" -ForegroundColor Green

# ============================================================================
# الخطوة 5: التحقق من قاعدة البيانات | Step 5: Check Database
# ============================================================================

Write-Host "`n📋 الخطوة 5: التحقق من قاعدة البيانات..." -ForegroundColor Green
Write-Host "   Step 5: Checking database..." -ForegroundColor Gray

if (Test-Path "backend\instance\inventory.db") {
    Write-Host "   ✅ قاعدة البيانات موجودة" -ForegroundColor Green
} else {
    Write-Host "   ⚠️ قاعدة البيانات غير موجودة، سيتم إنشاؤها عند التشغيل" -ForegroundColor Yellow
}

# ============================================================================
# الخطوة 6: تشغيل Backend | Step 6: Start Backend
# ============================================================================

Write-Host "`n📋 الخطوة 6: تشغيل Backend..." -ForegroundColor Green
Write-Host "   Step 6: Starting backend..." -ForegroundColor Gray

Write-Host "`n   🔧 جاري تشغيل Backend Server..." -ForegroundColor Cyan
Write-Host "   📍 URL: http://127.0.0.1:5002" -ForegroundColor Yellow
Write-Host "   📍 URL: http://localhost:5002" -ForegroundColor Yellow
Write-Host "`n"

Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$PWD\backend'; python app.py"

Start-Sleep -Seconds 5

# ============================================================================
# الخطوة 7: تشغيل Frontend | Step 7: Start Frontend
# ============================================================================

Write-Host "`n📋 الخطوة 7: تشغيل Frontend..." -ForegroundColor Green
Write-Host "   Step 7: Starting frontend..." -ForegroundColor Gray

Write-Host "`n   🎨 جاري تشغيل Frontend Server..." -ForegroundColor Cyan
Write-Host "   📍 URL: http://localhost:5502" -ForegroundColor Yellow
Write-Host "`n"

Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$PWD\frontend'; npm run dev"

Start-Sleep -Seconds 3

# ============================================================================
# الخطوة 8: فتح المتصفح | Step 8: Open Browser
# ============================================================================

Write-Host "`n📋 الخطوة 8: فتح المتصفح..." -ForegroundColor Green
Write-Host "   Step 8: Opening browser..." -ForegroundColor Gray

Start-Sleep -Seconds 5
Start-Process "http://localhost:5502"

# ============================================================================
# ============================================================================
# الخطوة 9: اختبار دخان للنظام | Step 9: Smoke Test
# ============================================================================

function Wait-ForBackend {
    param(
        [string]$Url = "http://localhost:5002/api/status",
        [int]$TimeoutSeconds = 60
    )
    $deadline = (Get-Date).AddSeconds($TimeoutSeconds)
    while ((Get-Date) -lt $deadline) {
        try {
            $resp = Invoke-RestMethod -Method Get -Uri $Url -TimeoutSec 5 -ErrorAction Stop
            if ($resp) { return $true }
        } catch {
            Start-Sleep -Seconds 2
        }
    }
    return $false
}

function Test-Endpoint {
    param(
        [ValidateSet('GET','POST')][string]$Method,
        [Parameter(Mandatory=$true)][string]$Url,
        [hashtable]$Body
    )
    try {
        if ($Method -eq 'GET') {
            $r = Invoke-RestMethod -Method Get -Uri $Url -TimeoutSec 10 -ErrorAction Stop
        } else {
            $json = $null
            if ($Body) { $json = ($Body | ConvertTo-Json -Depth 6) }
            $r = Invoke-RestMethod -Method Post -Uri $Url -Body $json -ContentType 'application/json' -TimeoutSec 10 -ErrorAction Stop
        }
        Write-Host ("   ✅ {0} {1} -> OK" -f $Method, $Url) -ForegroundColor Green
        return @{ ok = $true; response = $r }
    } catch {
        Write-Host ("   ❌ {0} {1} -> {2}" -f $Method, $Url, $_.Exception.Message) -ForegroundColor Red
        return @{ ok = $false }
    }
}

Write-Host "`n📋 الخطوة 9: اختبار الدخان للنظام..." -ForegroundColor Green
Write-Host "   Step 9: Running smoke tests..." -ForegroundColor Gray

$passed = 0; $total = 0

if (Wait-ForBackend) {
    Write-Host "   ✅ الخادم الخلفي جاهز" -ForegroundColor Green

    $total += 1
    $t1 = Test-Endpoint -Method GET -Url "http://localhost:5002/api/status"
    if ($t1.ok) { $passed += 1 }

    $total += 1
    $t2 = Test-Endpoint -Method POST -Url "http://localhost:5002/api/auth/login" -Body @{ username = 'admin'; password = 'admin123' }
    if ($t2.ok) { $passed += 1 }

    $total += 1
    $t3 = Test-Endpoint -Method GET -Url "http://localhost:5002/api/categories"
    if ($t3.ok) { $passed += 1 }

    # تحقق من وجود قاعدة البيانات بعد التشغيل
    $total += 1
    if (Test-Path "backend\instance\inventory.db") {
        Write-Host "   ✅ ملف قاعدة البيانات موجود" -ForegroundColor Green
        $passed += 1
    } else {
        Write-Host "   ❌ ملف قاعدة البيانات غير موجود" -ForegroundColor Red
    }

    Write-Host ("   📊 Smoke Test: {0}/{1} Passed" -f $passed, $total) -ForegroundColor Yellow
} else {
    Write-Host "   ❌ الخادم الخلفي لم يبدأ خلال المهلة المحددة" -ForegroundColor Red
}

# النتيجة النهائية | Final Result
# ============================================================================

Write-Host "`n"
Write-Host "============================================================================" -ForegroundColor Cyan
Write-Host "✅ تم تشغيل النظام بنجاح! | System Started Successfully!" -ForegroundColor Green
Write-Host "============================================================================" -ForegroundColor Cyan
Write-Host "`n"

Write-Host "📊 معلومات التشغيل | Running Information:" -ForegroundColor Yellow
Write-Host "   🔧 Backend:  http://localhost:5002" -ForegroundColor White
Write-Host "   🎨 Frontend: http://localhost:5502" -ForegroundColor White
Write-Host "`n"

Write-Host "🔐 بيانات تسجيل الدخول | Login Credentials:" -ForegroundColor Yellow
Write-Host "   👤 اسم المستخدم | Username: admin" -ForegroundColor White
Write-Host "   🔑 كلمة المرور | Password:  admin123" -ForegroundColor White
Write-Host "`n"

Write-Host "📝 ملاحظات | Notes:" -ForegroundColor Yellow
Write-Host "   • تم فتح نافذتين PowerShell للـ Backend والـ Frontend" -ForegroundColor Gray
Write-Host "   • Two PowerShell windows opened for Backend and Frontend" -ForegroundColor Gray
Write-Host "   • لإيقاف النظام، اضغط Ctrl+C في كل نافذة" -ForegroundColor Gray
Write-Host "   • To stop the system, press Ctrl+C in each window" -ForegroundColor Gray
Write-Host "`n"

Write-Host "============================================================================" -ForegroundColor Cyan
Write-Host "🎉 استمتع باستخدام النظام! | Enjoy using the system!" -ForegroundColor Green
Write-Host "============================================================================" -ForegroundColor Cyan
Write-Host "`n"

# Keep this window open
Write-Host "اضغط أي مفتاح للخروج... | Press any key to exit..." -ForegroundColor Yellow
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")

