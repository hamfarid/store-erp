# نص موحد لبدء تشغيل خدمات Gaara Scan AI
# هذا الملف يجمع وظائف جميع سكريبتات البدء في ملف واحد
# تاريخ التوحيد: 14 يونيو 2025

param (
    [string]$Action = "start",
    [string]$Environment = "development",
    [switch]$WithoutDocker = $false,
    [switch]$Staged = $false,
    [switch]$Clean = $false
)

# تعريف الألوان للرسائل
$Green = [System.ConsoleColor]::Green
$Red = [System.ConsoleColor]::Red
$Yellow = [System.ConsoleColor]::Yellow
$Cyan = [System.ConsoleColor]::Cyan

# عرض رسالة ترحيب
function Show-Welcome {
    Write-Host "`n=========================================" -ForegroundColor $Cyan
    Write-Host "      Gaara Scan AI - نظام التشغيل الموحد" -ForegroundColor $Cyan
    Write-Host "=========================================" -ForegroundColor $Cyan
    Write-Host "البيئة: $Environment" -ForegroundColor $Cyan
    if ($WithoutDocker) {
        Write-Host "الوضع: بدون Docker" -ForegroundColor $Cyan
    } elseif ($Staged) {
        Write-Host "الوضع: نشر مرحلي" -ForegroundColor $Cyan
    } else {
        Write-Host "الوضع: قياسي" -ForegroundColor $Cyan
    }
    Write-Host "=========================================`n" -ForegroundColor $Cyan
}

# التحقق من متطلبات النظام
function Check-Requirements {
    Write-Host "جاري التحقق من متطلبات النظام..." -ForegroundColor $Yellow
    
    if (-not $WithoutDocker) {
        try {
            $dockerVersion = docker --version
            Write-Host "✓ تم العثور على Docker: $dockerVersion" -ForegroundColor $Green
            
            $dockerComposeVersion = docker-compose --version
            Write-Host "✓ تم العثور على Docker Compose: $dockerComposeVersion" -ForegroundColor $Green
        } catch {
            Write-Host "✗ لم يتم العثور على Docker أو Docker Compose. يرجى تثبيتهما أولاً." -ForegroundColor $Red
            exit 1
        }
    }
    
    # التحقق من وجود ملف .env
    if (-not (Test-Path ".env")) {
        Write-Host "! لم يتم العثور على ملف .env. جاري إنشاء نسخة من .env-example..." -ForegroundColor $Yellow
        Copy-Item ".env-example" ".env"
        Write-Host "✓ تم إنشاء ملف .env" -ForegroundColor $Green
    }
}

# تنظيف البيئة
function Clean-Environment {
    Write-Host "جاري تنظيف البيئة..." -ForegroundColor $Yellow
    
    if (-not $WithoutDocker) {
        docker-compose down -v
        docker system prune -f
    }
    
    # حذف الملفات المؤقتة
    Remove-Item -Path ".\**\__pycache__" -Recurse -Force -ErrorAction SilentlyContinue
    Remove-Item -Path ".\**\.pytest_cache" -Recurse -Force -ErrorAction SilentlyContinue
    
    Write-Host "✓ تم تنظيف البيئة بنجاح" -ForegroundColor $Green
}

# بدء الخدمات
function Start-Services {
    Write-Host "جاري بدء الخدمات..." -ForegroundColor $Yellow
    
    if ($WithoutDocker) {
        # بدء الخدمات بدون Docker
        Start-Process -FilePath "python" -ArgumentList ".\src\main.py" -NoNewWindow
        Write-Host "✓ تم بدء الخدمات بدون Docker" -ForegroundColor $Green
    } elseif ($Staged) {
        # بدء الخدمات بالنشر المرحلي
        if ($Environment -eq "development") {
            docker-compose -f docker-compose.stage1.yml up -d
        } elseif ($Environment -eq "staging") {
            docker-compose -f docker-compose.stage2.yml up -d
        } elseif ($Environment -eq "production") {
            docker-compose -f docker-compose.stage3.yml up -d
        }
        Write-Host "✓ تم بدء الخدمات بالنشر المرحلي للبيئة: $Environment" -ForegroundColor $Green
    } else {
        # بدء الخدمات بشكل قياسي
        docker-compose up -d
        Write-Host "✓ تم بدء الخدمات بنجاح" -ForegroundColor $Green
    }
}

# إيقاف الخدمات
function Stop-Services {
    Write-Host "جاري إيقاف الخدمات..." -ForegroundColor $Yellow
    
    if ($WithoutDocker) {
        # إيقاف الخدمات بدون Docker
        $processes = Get-Process -Name "python" -ErrorAction SilentlyContinue
        if ($processes) {
            $processes | Stop-Process -Force
        }
        Write-Host "✓ تم إيقاف الخدمات بدون Docker" -ForegroundColor $Green
    } elseif ($Staged) {
        # إيقاف الخدمات بالنشر المرحلي
        if ($Environment -eq "development") {
            docker-compose -f docker-compose.stage1.yml down
        } elseif ($Environment -eq "staging") {
            docker-compose -f docker-compose.stage2.yml down
        } elseif ($Environment -eq "production") {
            docker-compose -f docker-compose.stage3.yml down
        }
        Write-Host "✓ تم إيقاف الخدمات بالنشر المرحلي للبيئة: $Environment" -ForegroundColor $Green
    } else {
        # إيقاف الخدمات بشكل قياسي
        docker-compose down
        Write-Host "✓ تم إيقاف الخدمات بنجاح" -ForegroundColor $Green
    }
}

# إعادة تشغيل الخدمات
function Restart-Services {
    Stop-Services
    Start-Services
}

# عرض حالة الخدمات
function Show-Status {
    Write-Host "جاري عرض حالة الخدمات..." -ForegroundColor $Yellow
    
    if ($WithoutDocker) {
        # عرض حالة الخدمات بدون Docker
        $processes = Get-Process -Name "python" -ErrorAction SilentlyContinue
        if ($processes) {
            Write-Host "✓ الخدمات قيد التشغيل بدون Docker" -ForegroundColor $Green
            $processes | Format-Table Id, ProcessName, StartTime
        } else {
            Write-Host "✗ الخدمات غير قيد التشغيل" -ForegroundColor $Red
        }
    } else {
        # عرض حالة الخدمات مع Docker
        docker-compose ps
    }
}

# التنفيذ الرئيسي
Show-Welcome
Check-Requirements

if ($Clean) {
    Clean-Environment
}

switch ($Action) {
    "start" {
        Start-Services
    }
    "stop" {
        Stop-Services
    }
    "restart" {
        Restart-Services
    }
    "status" {
        Show-Status
    }
    default {
        Write-Host "الإجراء غير معروف: $Action" -ForegroundColor $Red
        Write-Host "الإجراءات المتاحة: start, stop, restart, status" -ForegroundColor $Yellow
    }
}

Write-Host "`nاكتمل التنفيذ. شكراً لاستخدام نظام Gaara Scan AI.`n" -ForegroundColor $Cyan
