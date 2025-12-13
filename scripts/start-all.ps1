# Start All Services Script
# Starts all services for the Store Management System

Write-Host "Starting Store Management System Services..." -ForegroundColor Cyan
Write-Host "========================================`n" -ForegroundColor Cyan

# Check if ports are available
$ports = @(5505, 5506, 5432, 6379, 9323)
$conflicts = @()

foreach ($port in $ports) {
    $check = netstat -ano | Select-String ":$port" | Select-String "LISTENING"
    if ($check) {
        $pid = ($check -split '\s+')[-1]
        $conflicts += @{
            "Port" = $port
            "PID" = $pid
        }
    }
}

if ($conflicts.Count -gt 0) {
    Write-Host "Warning: Some ports are already in use:" -ForegroundColor Yellow
    foreach ($conflict in $conflicts) {
        Write-Host "  Port $($conflict.Port) - PID: $($conflict.PID)" -ForegroundColor Yellow
    }
    Write-Host "`nUse port-manager.ps1 to free ports:" -ForegroundColor Cyan
    foreach ($conflict in $conflicts) {
        Write-Host "  .\scripts\port-manager.ps1 -Port $($conflict.Port) -Kill" -ForegroundColor White
    }
    Write-Host "`n"
    $continue = Read-Host "Continue anyway? (y/n)"
    if ($continue -ne "y") {
        exit
    }
}

# Start services
Write-Host "Starting services...`n" -ForegroundColor Green

# Start Frontend
Write-Host "[1/2] Starting Frontend..." -ForegroundColor Cyan
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd frontend; npm run dev" -WindowStyle Minimized

Start-Sleep -Seconds 3

# Start Backend
Write-Host "[2/2] Starting Backend..." -ForegroundColor Cyan
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd backend; python main.py" -WindowStyle Minimized

Start-Sleep -Seconds 3

Write-Host "`nServices started!" -ForegroundColor Green
Write-Host "Check service status with: .\scripts\check-services.ps1" -ForegroundColor Cyan
Write-Host "`n"

