Param()
$ErrorActionPreference = 'Stop'
$ts = Get-Date -Format 'yyyyMMdd-HHmmss'
Set-Location -Path (Get-Location)
$backupDir = 'artifacts'
New-Item -ItemType Directory -Force -Path $backupDir | Out-Null
$zip = Join-Path $backupDir ("store_backup_$ts.zip")
if (Test-Path 'store') {
    Compress-Archive -Path 'store' -DestinationPath $zip -CompressionLevel Optimal -Force
    New-Item -ItemType Directory -Force -Path 'unneeded' | Out-Null
    $removed = Join-Path 'unneeded' ("store.removed.$ts")
    if (Test-Path $removed) { Remove-Item -Recurse -Force $removed }
    Move-Item -Path 'store' -Destination $removed
    Write-Output ("BACKUP_ZIP:" + $zip)
    Write-Output ("MOVED_TO:" + $removed)
} else {
    Write-Output 'NO_STORE_DIR'
}

