# Simple Clean Archive Creator for Complete Inventory System

Write-Host "Creating clean archive..." -ForegroundColor Blue

$ArchiveName = "complete_inventory_system_v1.0.0_clean"
$TempDir = "$env:TEMP\$ArchiveName"

# Clean up existing temp directory
if (Test-Path $TempDir) {
    Remove-Item $TempDir -Recurse -Force
}

# Create temp directory
New-Item -ItemType Directory -Path $TempDir -Force | Out-Null
Write-Host "Created temp directory" -ForegroundColor Green

# Copy main directories (excluding unwanted files)
$Directories = @("backend\src", "frontend\src", "frontend\public", "scripts", "docs")

foreach ($Dir in $Directories) {
    if (Test-Path $Dir) {
        Write-Host "Copying $Dir..." -ForegroundColor Cyan
        $DestPath = Join-Path $TempDir $Dir
        New-Item -ItemType Directory -Path $DestPath -Force -Recurse | Out-Null
        Copy-Item "$Dir\*" $DestPath -Recurse -Force
    }
}

# Copy specific files
$Files = @(
    "README.md",
    "PROJECT_SUMMARY.md",
    "backend\requirements.txt",
    "backend\requirements_final.txt",
    "frontend\package.json",
    "frontend\vite.config.js",
    "frontend\index.html",
    "frontend\tailwind.config.js"
)

foreach ($File in $Files) {
    if (Test-Path $File) {
        Write-Host "Copying $File..." -ForegroundColor Cyan
        $DestPath = Join-Path $TempDir $File
        $DestDir = Split-Path $DestPath -Parent
        New-Item -ItemType Directory -Path $DestDir -Force | Out-Null
        Copy-Item $File $DestPath -Force
    }
}

# Create archive info
$InfoContent = @"
# Complete Inventory Management System - Clean Archive

Version: v1.0.0
Created: $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')

## What's Included:
- Source code (backend & frontend)
- Configuration files
- Installation scripts
- Documentation

## What's Excluded:
- node_modules
- Python virtual environments
- Cache files
- Build outputs
- Log files

## Quick Start:
1. Extract archive
2. Install Python 3.9+ and Node.js 18.0.0+
3. Backend: cd backend, python -m venv venv, venv\Scripts\activate, pip install -r requirements_final.txt
4. Frontend: cd frontend, npm install
5. Run: python backend\src\main.py (Terminal 1), npm run dev (Terminal 2 in frontend)

## Access:
- Frontend: http://localhost:5173
- Backend: http://localhost:8000
"@

$InfoContent | Out-File -FilePath "$TempDir\README_ARCHIVE.txt" -Encoding UTF8

# Create the ZIP archive
Write-Host "Creating ZIP archive..." -ForegroundColor Yellow
$ArchivePath = "..\$ArchiveName.zip"

if (Test-Path $ArchivePath) {
    Remove-Item $ArchivePath -Force
}

Compress-Archive -Path "$TempDir\*" -DestinationPath $ArchivePath -CompressionLevel Optimal

# Get file size
$Size = (Get-Item $ArchivePath).Length / 1MB
$SizeRounded = [math]::Round($Size, 2)

Write-Host "Archive created successfully!" -ForegroundColor Green
Write-Host "File: $ArchiveName.zip" -ForegroundColor Cyan
Write-Host "Size: $SizeRounded MB" -ForegroundColor Cyan
Write-Host "Location: $(Resolve-Path $ArchivePath)" -ForegroundColor Cyan

# Clean up
Remove-Item $TempDir -Recurse -Force
Write-Host "Cleanup completed!" -ForegroundColor Green
