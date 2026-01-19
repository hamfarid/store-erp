# ==========================================
# سكريبت رفع المشروع إلى GitHub
# Push to GitHub Script
# ==========================================

Write-Host "🚀 سكريبت رفع المشروع إلى GitHub" -ForegroundColor Cyan
Write-Host "=================================" -ForegroundColor Cyan
Write-Host ""

# التحقق من وجود Git
if (-not (Get-Command git -ErrorAction SilentlyContinue)) {
    Write-Host "❌ Git غير مثبت!" -ForegroundColor Red
    Write-Host "يرجى تثبيت Git أولاً من: https://git-scm.com/download/win" -ForegroundColor Yellow
    exit 1
}

# الانتقال إلى مجلد المشروع
$projectPath = Split-Path -Parent $PSScriptRoot
Set-Location $projectPath

Write-Host "📁 مجلد المشروع: $projectPath" -ForegroundColor Green
Write-Host ""

# التحقق من وجود remote
$remote = git remote -v
if ($remote) {
    Write-Host "✅ تم العثور على remote:" -ForegroundColor Green
    Write-Host $remote
    Write-Host ""
    
    $push = Read-Host "هل تريد رفع الملفات الآن؟ (y/n)"
    if ($push -eq "y" -or $push -eq "Y") {
        Write-Host ""
        Write-Host "⬆️  جاري رفع الملفات..." -ForegroundColor Yellow
        
        # التحقق من اسم الفرع
        $branch = git branch --show-current
        Write-Host "📌 الفرع الحالي: $branch" -ForegroundColor Cyan
        
        # رفع الملفات
        git push -u origin $branch
        
        if ($LASTEXITCODE -eq 0) {
            Write-Host ""
            Write-Host "✅ تم رفع الملفات بنجاح!" -ForegroundColor Green
        } else {
            Write-Host ""
            Write-Host "❌ فشل رفع الملفات!" -ForegroundColor Red
            Write-Host "يرجى التحقق من:" -ForegroundColor Yellow
            Write-Host "  1. اسم المستخدم وكلمة المرور/Token" -ForegroundColor Yellow
            Write-Host "  2. صلاحيات المستودع" -ForegroundColor Yellow
            Write-Host "  3. اتصال الإنترنت" -ForegroundColor Yellow
        }
    }
} else {
    Write-Host "⚠️  لم يتم العثور على remote" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "يرجى إضافة remote أولاً:" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "git remote add origin https://github.com/YOUR_USERNAME/REPO_NAME.git" -ForegroundColor White
    Write-Host ""
    Write-Host "أو:" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "git remote add origin git@github.com:YOUR_USERNAME/REPO_NAME.git" -ForegroundColor White
    Write-Host ""
    
    $addRemote = Read-Host "هل تريد إضافة remote الآن؟ (y/n)"
    if ($addRemote -eq "y" -or $addRemote -eq "Y") {
        $repoUrl = Read-Host "أدخل رابط المستودع (مثال: https://github.com/username/repo.git)"
        if ($repoUrl) {
            git remote add origin $repoUrl
            Write-Host "✅ تم إضافة remote بنجاح!" -ForegroundColor Green
            Write-Host ""
            
            $pushNow = Read-Host "هل تريد رفع الملفات الآن؟ (y/n)"
            if ($pushNow -eq "y" -or $pushNow -eq "Y") {
                $branch = git branch --show-current
                Write-Host ""
                Write-Host "⬆️  جاري رفع الملفات..." -ForegroundColor Yellow
                git push -u origin $branch
            }
        }
    }
}

Write-Host ""
Write-Host "✨ انتهى!" -ForegroundColor Cyan

