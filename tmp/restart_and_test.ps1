# Restart backend and test login endpoint (PowerShell)
# 1) Clear __pycache__
Get-ChildItem -Path 'backend' -Recurse -Directory -Filter '__pycache__' -ErrorAction SilentlyContinue | Remove-Item -Recurse -Force -ErrorAction SilentlyContinue

# 2) Kill listeners on port 5001 (if any)
$pids = Get-NetTCPConnection -LocalPort 5001 -State Listen -ErrorAction SilentlyContinue | Select-Object -ExpandProperty OwningProcess -Unique
foreach ($procId in $pids) {
  try {
    Stop-Process -Id $procId -Force -ErrorAction Stop
    Write-Output ("Killed PID " + $procId)
  } catch {
    Write-Output ("Failed to kill PID " + $procId + ': ' + $_.Exception.Message)
  }
}

# 3) Start backend
$env:PORT = "5001"
$python = ".\.venv311\Scripts\python.exe"
if (!(Test-Path $python)) { $python = "python" }
$backend = Start-Process -FilePath $python -ArgumentList 'backend\app.py' -WindowStyle Hidden -PassThru
Start-Sleep -Seconds 6

# 4) Prepare temp folder
New-Item -ItemType Directory -Force -Path 'tmp' | Out-Null

# 5) Call login endpoint with wrong creds to capture headers/body
$bodyObj = @{ email = "wrong@example.com"; password = "nope" }
$bodyJson = ($bodyObj | ConvertTo-Json -Compress)
try {
  $resp = Invoke-WebRequest -UseBasicParsing -Uri 'http://127.0.0.1:5001/api/auth/login' -Method Post -ContentType 'application/json' -Body $bodyJson -ErrorAction Stop
} catch {
  $resp = $_.Exception.Response
}

$headersPath = 'tmp\login_headers.txt'
$bodyPath = 'tmp\login_body.json'

# 6) Write headers
$lines = @()
if ($resp -and $resp.StatusCode) {
  $statusDesc = if ($resp.StatusDescription) { $resp.StatusDescription } else { "" }
  $lines += ('HTTP/1.1 ' + $resp.StatusCode + ' ' + $statusDesc)
}
if ($resp -and $resp.Headers) {
  foreach ($key in $resp.Headers.Keys) { $lines += ($key + ': ' + $resp.Headers[$key]) }
}
Set-Content -Path $headersPath -Value $lines -Encoding UTF8

# 7) Write body
if ($resp -and $resp.Content) {
  Set-Content -Path $bodyPath -Value $resp.Content -Encoding UTF8
}

# 8) Print to console
Get-Content $headersPath
Get-Content $bodyPath

# 9) Stop backend process (cleanup)
if ($backend -and -not $backend.HasExited) {
  try { Stop-Process -Id $backend.Id -Force -ErrorAction Stop } catch {}
}
