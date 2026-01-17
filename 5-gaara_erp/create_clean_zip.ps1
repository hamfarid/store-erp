# Create Clean Zip Script for Gaara ERP v12
# Excludes: venv, env, node_modules, __pycache__, .pytest_cache, .git

$ErrorActionPreference = "Stop"

# Configuration
$SourcePath = "D:\Ai_Project\5-gaara_erp"
$OutputPath = "D:\Ai_Project\gaara_erp_v12_clean.zip"
$TempPath = "D:\Ai_Project\_temp_gaara_erp"

# Exclude patterns
$ExcludePatterns = @(
    "venv",
    "env",
    ".venv",
    "node_modules",
    "__pycache__",
    ".pytest_cache",
    ".git",
    ".mypy_cache",
    "*.pyc",
    "*.pyo",
    ".coverage",
    "htmlcov",
    ".tox",
    "*.egg-info",
    "dist",
    "build",
    ".eggs",
    "*.log",
    "*.sqlite3",
    ".env",
    ".env.local",
    ".DS_Store",
    "Thumbs.db",
    "pnpm-lock.yaml",
    "package-lock.json",
    "yarn.lock"
)

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Gaara ERP v12 - Clean Zip Creator" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Remove temp folder if exists
if (Test-Path $TempPath) {
    Write-Host "Cleaning temp folder..." -ForegroundColor Yellow
    Remove-Item -Path $TempPath -Recurse -Force
}

# Remove old zip if exists
if (Test-Path $OutputPath) {
    Write-Host "Removing old zip file..." -ForegroundColor Yellow
    Remove-Item -Path $OutputPath -Force
}

Write-Host "Creating temp folder..." -ForegroundColor Green
New-Item -ItemType Directory -Path $TempPath -Force | Out-Null

Write-Host "Copying files (excluding unwanted directories)..." -ForegroundColor Green

# Copy files using robocopy with exclusions
$RobocopyExcludes = @(
    "/XD", "venv", "env", ".venv", "node_modules", "__pycache__", ".pytest_cache", 
    ".git", ".mypy_cache", "htmlcov", ".tox", "dist", "build", ".eggs"
)
$RobocopyFileExcludes = @(
    "/XF", "*.pyc", "*.pyo", "*.log", "*.sqlite3", ".env", ".env.local", 
    ".DS_Store", "Thumbs.db", "pnpm-lock.yaml", "package-lock.json", "yarn.lock", ".coverage"
)

robocopy $SourcePath $TempPath /E /NFL /NDL /NJH /NJS /nc /ns /np `
    $RobocopyExcludes $RobocopyFileExcludes

Write-Host "Creating zip archive..." -ForegroundColor Green
Compress-Archive -Path "$TempPath\*" -DestinationPath $OutputPath -Force

Write-Host "Cleaning up temp folder..." -ForegroundColor Yellow
Remove-Item -Path $TempPath -Recurse -Force

# Get file size
$ZipSize = (Get-Item $OutputPath).Length / 1MB
Write-Host ""
Write-Host "========================================" -ForegroundColor Green
Write-Host "SUCCESS!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Write-Host "Output: $OutputPath" -ForegroundColor Cyan
Write-Host "Size: $([math]::Round($ZipSize, 2)) MB" -ForegroundColor Cyan
Write-Host ""
