# Port Manager Script
# Helps manage port conflicts

param(
    [Parameter(Mandatory=$true)]
    [int]$Port,
    
    [Parameter(Mandatory=$false)]
    [switch]$Kill
)

Write-Host "Checking port $Port..." -ForegroundColor Cyan

# Find process using the port
$process = netstat -ano | Select-String ":$Port" | Select-String "LISTENING"

if ($process) {
    $pid = ($process -split '\s+')[-1]
    $procInfo = Get-Process -Id $pid -ErrorAction SilentlyContinue
    
    if ($procInfo) {
        Write-Host "Port $Port is in use by:" -ForegroundColor Yellow
        Write-Host "  PID: $pid" -ForegroundColor Yellow
        Write-Host "  Process: $($procInfo.ProcessName)" -ForegroundColor Yellow
        Write-Host "  Path: $($procInfo.Path)" -ForegroundColor Yellow
        
        if ($Kill) {
            Write-Host "`nKilling process $pid..." -ForegroundColor Red
            Stop-Process -Id $pid -Force
            Write-Host "Process killed. Port $Port is now available." -ForegroundColor Green
        } else {
            Write-Host "`nTo kill this process, run:" -ForegroundColor Cyan
            Write-Host "  .\scripts\port-manager.ps1 -Port $Port -Kill" -ForegroundColor White
        }
    } else {
        Write-Host "Port $Port is in use but process not found." -ForegroundColor Yellow
    }
} else {
    Write-Host "Port $Port is available." -ForegroundColor Green
}

