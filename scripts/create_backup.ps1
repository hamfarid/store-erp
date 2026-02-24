# Create Backup Script
$timestamp = Get-Date -Format "yyyyMMdd_HHmmss"
$backupDir = "cleanup_backup_$timestamp"

Write-Host "🔄 Creating backup directory..."
New-Item -ItemType Directory -Path $backupDir -Force | Out-Null

Write-Host "📦 Backing up backend..."
Copy-Item -Path "backend" -Destination "$backupDir\backend" -Recurse -Force

Write-Host "📦 Backing up frontend..."
Copy-Item -Path "frontend" -Destination "$backupDir\frontend" -Recurse -Force

Write-Host ""
Write-Host "✅ Backup created successfully: $backupDir"
Write-Host ""
Write-Host "📊 Backup statistics:"
$files = Get-ChildItem $backupDir -Recurse -File
$totalSize = ($files | Measure-Object -Property Length -Sum).Sum
$totalFiles = $files.Count

Write-Host "  Total files: $totalFiles"
Write-Host "  Total size: $([math]::Round($totalSize/1MB,2)) MB"
Write-Host ""
Write-Host "📁 Backup location: $(Resolve-Path $backupDir)"

# Return backup directory name for use in cleanup script
return $backupDir

