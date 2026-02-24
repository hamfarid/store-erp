# 🏪 Complete Inventory Management System - Clean Archive Creator
# Creates a compressed archive without unnecessary files

Write-Host "🗜️ Creating clean archive for Complete Inventory System..." -ForegroundColor Blue

# Configuration
$ProjectName = "complete_inventory_system"
$Version = "v1.0.0"
$Date = Get-Date -Format "yyyyMMdd_HHmmss"
$ArchiveName = "${ProjectName}_${Version}_clean"
$TempDir = "$env:TEMP\$ArchiveName"
$SourceDir = "."

# Files and directories to exclude
$ExcludePatterns = @(
    "node_modules",
    "__pycache__",
    ".pytest_cache",
    "venv",
    "env",
    ".env",
    "instance",
    "logs",
    "dist",
    "build",
    ".next",
    ".vscode",
    ".idea",
    ".DS_Store",
    "*.pyc",
    "*.pyo",
    "*.tmp",
    "*.temp",
    "*~",
    ".git",
    "unneeded",
    "create_clean_archive.ps1"
)

# Function to check if path should be excluded
function Should-Exclude {
    param($Path)
    
    $BaseName = Split-Path $Path -Leaf
    
    foreach ($Pattern in $ExcludePatterns) {
        if ($Pattern.Contains("*")) {
            if ($BaseName -like $Pattern) {
                return $true
            }
        } else {
            if ($BaseName -eq $Pattern) {
                return $true
            }
        }
    }
    return $false
}

# Function to copy files with exclusions
function Copy-WithExclusions {
    param($Source, $Destination)
    
    if (Should-Exclude $Source) {
        return
    }
    
    if (Test-Path $Source -PathType Container) {
        # It's a directory
        if (!(Test-Path $Destination)) {
            New-Item -ItemType Directory -Path $Destination -Force | Out-Null
        }
        
        Get-ChildItem $Source | ForEach-Object {
            Copy-WithExclusions $_.FullName (Join-Path $Destination $_.Name)
        }
    } else {
        # It's a file
        $DestDir = Split-Path $Destination -Parent
        if (!(Test-Path $DestDir)) {
            New-Item -ItemType Directory -Path $DestDir -Force | Out-Null
        }
        Copy-Item $Source $Destination -Force
    }
}

try {
    # Clean up any existing temp directory
    if (Test-Path $TempDir) {
        Remove-Item $TempDir -Recurse -Force
    }
    
    # Create temp directory
    New-Item -ItemType Directory -Path $TempDir -Force | Out-Null
    Write-Host "✓ Created temp directory: $TempDir" -ForegroundColor Green
    
    # Copy project files
    Write-Host "📂 Copying project files..." -ForegroundColor Yellow
    
    # Copy main directories
    $MainDirs = @("backend", "frontend", "scripts", "docs")
    foreach ($Dir in $MainDirs) {
        if (Test-Path $Dir) {
            Write-Host "  - Copying $Dir..." -ForegroundColor Cyan
            Copy-WithExclusions (Join-Path $SourceDir $Dir) (Join-Path $TempDir $Dir)
        }
    }
    
    # Copy root files
    Write-Host "  - Copying root files..." -ForegroundColor Cyan
    $RootFiles = @("README.md", "PROJECT_SUMMARY.md", ".gitignore")
    foreach ($File in $RootFiles) {
        if (Test-Path $File) {
            Copy-Item $File (Join-Path $TempDir $File) -Force
        }
    }
    
    # Create archive info
    Write-Host "📄 Creating archive info..." -ForegroundColor Yellow
    $ArchiveInfo = @"
# 🏪 Complete Inventory Management System - Clean Archive

## Archive Information
- Name: $ArchiveName
- Version: $Version
- Created: $(Get-Date -Format "yyyy-MM-dd HH:mm:ss")
- Type: Clean (no dependencies, cache, or build files)

## What's Included
✅ Source code (backend & frontend)
✅ Configuration files
✅ Scripts for installation and deployment
✅ Documentation
✅ Requirements files

## What's Excluded
❌ node_modules (will be installed by npm install)
❌ Python virtual environments (will be created by install script)
❌ Cache files (__pycache__, .pytest_cache)
❌ Build outputs (dist, build)
❌ Log files
❌ IDE files (.vscode, .idea)
❌ Environment files (.env)
❌ Database files (instance/)

## Quick Start
1. Extract the archive
2. cd $ArchiveName
3. Follow INSTALL.md instructions

## Requirements
- Python 3.9+
- Node.js 18.0.0+
- npm 9.0.0+
- 4GB RAM (8GB recommended)
- 2GB free disk space

## Access URLs
- Frontend: http://localhost:5173
- Backend: http://localhost:8000
- API Docs: http://localhost:8000/api

Created by: Automated Clean Archive Script
"@
    
    $ArchiveInfo | Out-File -FilePath (Join-Path $TempDir "ARCHIVE_INFO.md") -Encoding UTF8
    
    # Create installation guide
    Write-Host "📋 Creating installation guide..." -ForegroundColor Yellow
    $InstallGuide = @"
# Installation Guide

## Prerequisites
* Python 3.9+
* Node.js 18.0.0+
* npm 9.0.0+

## Windows Installation

### Backend Setup
```powershell
cd backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements_final.txt
```

### Frontend Setup
```powershell
cd frontend
npm install
```

### Running the System
```powershell
# Terminal 1 - Backend
cd backend
venv\Scripts\activate
python src/main.py

# Terminal 2 - Frontend
cd frontend
npm run dev
```

## Linux/Mac Installation

### Quick Installation
```bash
chmod +x scripts/*.sh
./scripts/install.sh
./scripts/start.sh
```

## Access URLs
* Frontend: http://localhost:5173
* Backend: http://localhost:8000
"@
    
    $InstallGuide | Out-File -FilePath (Join-Path $TempDir "INSTALL.md") -Encoding UTF8
    
    # Create the archive
    Write-Host "🗜️ Creating ZIP archive..." -ForegroundColor Yellow
    $ArchivePath = "..\$ArchiveName.zip"
    
    # Remove existing archive if it exists
    if (Test-Path $ArchivePath) {
        Remove-Item $ArchivePath -Force
    }
    
    # Create the archive
    Compress-Archive -Path "$TempDir\*" -DestinationPath $ArchivePath -CompressionLevel Optimal
    
    # Get archive size
    $ArchiveSize = (Get-Item $ArchivePath).Length
    $ArchiveSizeMB = [math]::Round($ArchiveSize / 1MB, 2)
    
    Write-Host "✅ Archive created successfully!" -ForegroundColor Green
    Write-Host "📦 Archive: $ArchiveName.zip" -ForegroundColor Cyan
    Write-Host "📏 Size: $ArchiveSizeMB MB" -ForegroundColor Cyan
    Write-Host "📍 Location: $(Resolve-Path $ArchivePath)" -ForegroundColor Cyan
    
    # Clean up temp directory
    Write-Host "🧹 Cleaning up..." -ForegroundColor Yellow
    Remove-Item $TempDir -Recurse -Force
    
    Write-Host "🎉 Clean archive creation completed!" -ForegroundColor Green
    
} catch {
    Write-Host "❌ Error creating archive: $($_.Exception.Message)" -ForegroundColor Red
    exit 1
}
