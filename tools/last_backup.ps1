Param()
if (Test-Path 'artifacts') {
  $f = Get-ChildItem artifacts -Filter 'store_backup_*.zip' | Sort-Object LastWriteTime -Descending | Select-Object -First 1
  if ($f) { Write-Output $f.FullName } else { Write-Output 'NO_BACKUPS' }
} else {
  Write-Output 'NO_ARTIFACTS_DIR'
}

