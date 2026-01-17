# FILE: bootstrap_windows.ps1 | PURPOSE: تنزيل وإعداد مستودع global بالكامل على Windows | OWNER: DevOps | LAST-AUDITED: 2025-10-21

<#
.SYNOPSIS
    تنزيل وإعداد مستودع global من GitHub

.DESCRIPTION
    يقوم هذا السكريبت بتنزيل مستودع global بالكامل من GitHub وإعداده للاستخدام على Windows

.PARAMETER Branch
    الفرع أو Tag المراد تنزيله (افتراضي: main)

.PARAMETER Destination
    مجلد الوجهة (افتراضي: .\global)

.PARAMETER Token
    رمز GitHub للمستودعات الخاصة (اختياري)

.EXAMPLE
    .\bootstrap_windows.ps1

.EXAMPLE
    .\bootstrap_windows.ps1 -Branch main -Destination "C:\Projects\global"

.EXAMPLE
    .\bootstrap_windows.ps1 -Token "ghp_xxxxx"
#>

param(
    [string]$Branch = "main",
    [string]$Destination = ".\global",
    [string]$Token = $env:GITHUB_TOKEN
)

# ========================================
# المتغيرات الأساسية
# ========================================
$RepoOwner = "hamfarid"
$RepoName = "global"
$RepoUrl = "https://github.com/$RepoOwner/$RepoName.git"

# ========================================
# الدوال المساعدة
# ========================================
function Write-ColorOutput {
    param(
        [string]$Message,
        [string]$Type = "Info"
    )
    
    $timestamp = Get-Date -Format "HH:mm:ss"
    
    switch ($Type) {
        "Info"    { Write-Host "[$timestamp] [INFO] " -ForegroundColor Blue -NoNewline; Write-Host $Message }
        "Success" { Write-Host "[$timestamp] [✓] " -ForegroundColor Green -NoNewline; Write-Host $Message }
        "Warning" { Write-Host "[$timestamp] [!] " -ForegroundColor Yellow -NoNewline; Write-Host $Message }
        "Error"   { Write-Host "[$timestamp] [✗] " -ForegroundColor Red -NoNewline; Write-Host $Message }
    }
}

# ========================================
# البداية
# ========================================
Write-Host ""
Write-ColorOutput "==========================================" "Info"
Write-ColorOutput "تنزيل وإعداد مستودع Global" "Info"
Write-ColorOutput "==========================================" "Info"
Write-Host ""
Write-ColorOutput "المستودع: $RepoOwner/$RepoName" "Info"
Write-ColorOutput "الفرع   : $Branch" "Info"
Write-ColorOutput "الوجهة  : $Destination" "Info"
Write-Host ""

# ========================================
# إنشاء مجلد الوجهة
# ========================================
if (-not (Test-Path $Destination)) {
    New-Item -ItemType Directory -Path $Destination -Force | Out-Null
}
$Destination = (Resolve-Path $Destination).Path

# ========================================
# التحقق من وجود git
# ========================================
$UseGit = $false
try {
    $gitVersion = git --version 2>$null
    if ($gitVersion) {
        Write-ColorOutput "تم العثور على git: $gitVersion" "Success"
        $UseGit = $true
    }
} catch {
    Write-ColorOutput "لم يتم العثور على git - سيتم استخدام التنزيل المباشر" "Warning"
}

# ========================================
# التنزيل
# ========================================
$TempDir = Join-Path $env:TEMP "global-download-$(Get-Random)"
New-Item -ItemType Directory -Path $TempDir -Force | Out-Null

try {
    Write-ColorOutput "جاري التنزيل..." "Info"
    
    if ($UseGit) {
        # استخدام git clone
        $CloneUrl = if ($Token) {
            "https://${Token}@github.com/$RepoOwner/$RepoName.git"
        } else {
            $RepoUrl
        }
        
        try {
            git clone --depth 1 --branch $Branch $CloneUrl $Destination 2>&1 | Out-Null
            if ($LASTEXITCODE -eq 0) {
                Write-ColorOutput "تم التنزيل باستخدام git" "Success"
            } else {
                throw "فشل git clone"
            }
        } catch {
            Write-ColorOutput "فشل git clone - محاولة التنزيل المباشر..." "Warning"
            $UseGit = $false
        }
    }
    
    if (-not $UseGit) {
        # التنزيل المباشر
        $ZipUrl = "https://api.github.com/repos/$RepoOwner/$RepoName/zipball/$Branch"
        $ZipPath = Join-Path $TempDir "repo.zip"
        
        $headers = @{}
        if ($Token) {
            $headers["Authorization"] = "token $Token"
        }
        
        try {
            Invoke-WebRequest -Uri $ZipUrl -OutFile $ZipPath -Headers $headers -UseBasicParsing
            Write-ColorOutput "تم التنزيل" "Success"
            
            Write-ColorOutput "جاري فك الضغط..." "Info"
            Expand-Archive -Path $ZipPath -DestinationPath $TempDir -Force
            
            # نقل الملفات
            $ExtractedDir = Get-ChildItem -Path $TempDir -Directory | Select-Object -First 1
            if ($ExtractedDir) {
                Copy-Item -Path "$($ExtractedDir.FullName)\*" -Destination $Destination -Recurse -Force
                Write-ColorOutput "تم فك الضغط والنقل" "Success"
            }
        } catch {
            Write-ColorOutput "فشل التنزيل: $_" "Error"
            exit 1
        }
    }
    
} finally {
    # تنظيف الملفات المؤقتة
    if (Test-Path $TempDir) {
        Remove-Item -Path $TempDir -Recurse -Force -ErrorAction SilentlyContinue
    }
}

# ========================================
# إنشاء المجلدات الأساسية
# ========================================
Write-ColorOutput "إنشاء المجلدات الأساسية..." "Info"

$Folders = @(
    ".github\workflows",
    "scripts",
    "templates",
    "docs",
    "contracts",
    "packages\shared-types",
    "examples"
)

foreach ($folder in $Folders) {
    $folderPath = Join-Path $Destination $folder
    if (-not (Test-Path $folderPath)) {
        New-Item -ItemType Directory -Path $folderPath -Force | Out-Null
    }
}

Write-ColorOutput "تم إنشاء المجلدات" "Success"

# ========================================
# عرض الملفات
# ========================================
Write-ColorOutput "الملفات المتوفرة:" "Info"
Write-Host ""

$Files = @(
    "README.md",
    "GLOBAL_GUIDELINES.txt",
    "GLOBAL_GUIDELINES_v2.1.txt",
    "GLOBAL_GUIDELINES_v2.2.txt",
    "setup_project_structure.sh",
    "validate_project.sh",
    "scripts\backup.sh"
)

foreach ($file in $Files) {
    $filePath = Join-Path $Destination $file
    if (Test-Path $filePath) {
        Write-ColorOutput $file "Success"
    }
}

# ========================================
# إنشاء ملف batch للسكريبتات bash
# ========================================
Write-ColorOutput "إنشاء ملفات مساعدة لـ Windows..." "Info"

# ملف setup_project.bat
$SetupBat = @"
@echo off
REM FILE: setup_project.bat | PURPOSE: Windows wrapper for setup_project_structure.sh
REM يتطلب Git Bash أو WSL

echo ========================================
echo إنشاء مشروع جديد
echo ========================================
echo.

if "%~1"=="" (
    echo الاستخدام: setup_project.bat project_name [destination]
    echo.
    echo أمثلة:
    echo   setup_project.bat my_project
    echo   setup_project.bat my_project C:\Projects\my_project
    exit /b 1
)

REM التحقق من وجود Git Bash
where bash >nul 2>&1
if %ERRORLEVEL% EQU 0 (
    bash setup_project_structure.sh %*
) else (
    echo [!] لم يتم العثور على bash
    echo [!] يرجى تثبيت Git for Windows أو WSL
    echo [!] أو استخدم Git Bash لتشغيل السكريبت
    exit /b 1
)
"@

$SetupBatPath = Join-Path $Destination "setup_project.bat"
Set-Content -Path $SetupBatPath -Value $SetupBat -Encoding ASCII
Write-ColorOutput "setup_project.bat" "Success"

# ملف validate_project.bat
$ValidateBat = @"
@echo off
REM FILE: validate_project.bat | PURPOSE: Windows wrapper for validate_project.sh
REM يتطلب Git Bash أو WSL

echo ========================================
echo التحقق من صحة المشروع
echo ========================================
echo.

if "%~1"=="" (
    echo الاستخدام: validate_project.bat project_path
    echo.
    echo أمثلة:
    echo   validate_project.bat C:\Projects\my_project
    exit /b 1
)

REM التحقق من وجود Git Bash
where bash >nul 2>&1
if %ERRORLEVEL% EQU 0 (
    bash validate_project.sh %*
) else (
    echo [!] لم يتم العثور على bash
    echo [!] يرجى تثبيت Git for Windows أو WSL
    exit /b 1
)
"@

$ValidateBatPath = Join-Path $Destination "validate_project.bat"
Set-Content -Path $ValidateBatPath -Value $ValidateBat -Encoding ASCII
Write-ColorOutput "validate_project.bat" "Success"

# ========================================
# الخلاصة
# ========================================
Write-Host ""
Write-ColorOutput "==========================================" "Info"
Write-ColorOutput "اكتمل التنزيل والإعداد بنجاح!" "Success"
Write-ColorOutput "==========================================" "Info"
Write-Host ""
Write-ColorOutput "المسار: $Destination" "Info"
Write-Host ""
Write-ColorOutput "الخطوات التالية:" "Info"
Write-Host "  1. cd $Destination"
Write-Host "  2. اقرأ README.md للتعليمات"
Write-Host "  3. استخدم setup_project.bat لإنشاء مشروع جديد"
Write-Host ""
Write-ColorOutput "أمثلة الاستخدام:" "Info"
Write-Host "  # إنشاء مشروع جديد (يتطلب Git Bash)"
Write-Host "  .\setup_project.bat my_project C:\Projects\my_project"
Write-Host ""
Write-Host "  # التحقق من مشروع (يتطلب Git Bash)"
Write-Host "  .\validate_project.bat C:\Projects\my_project"
Write-Host ""
Write-ColorOutput "ملاحظة: السكريبتات تتطلب Git Bash أو WSL" "Warning"
Write-Host ""

