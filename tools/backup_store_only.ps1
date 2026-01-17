Param()
$ErrorActionPreference = 'Stop'
$ts = Get-Date -Format 'yyyyMMdd-HHmmss'
$backupDir = 'artifacts'
New-Item -ItemType Directory -Force -Path $backupDir | Out-Null
$zipPath = Join-Path $backupDir ("store_backup_$ts.zip")
if (Test-Path 'store') {
    if (Test-Path $zipPath) { Remove-Item -Force $zipPath }
    Compress-Archive -Path 'store' -DestinationPath $zipPath -CompressionLevel Optimal -Force
    Write-Output ("BACKUP_ZIP:" + $zipPath)
} else {
    Write-Output 'NO_STORE_DIR'
}

