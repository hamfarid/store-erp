# Service Status Checker
# Checks the status of all services in the Store Management System

$services = @{
    "Frontend" = @{
        "Port" = 5505
        "URL" = "http://localhost:5505"
        "Process" = "node"
    }
    "Backend" = @{
        "Port" = 5506
        "URL" = "http://localhost:5506"
        "Process" = "python"
    }
    "PostgreSQL" = @{
        "Port" = 5432
        "URL" = "localhost:5432"
        "Process" = "postgres"
    }
    "Redis" = @{
        "Port" = 6379
        "URL" = "localhost:6379"
        "Process" = "redis"
    }
    "Prometheus" = @{
        "Port" = 9323
        "URL" = "http://localhost:9323"
        "Process" = "node"
    }
}

Write-Host "`n========================================" -ForegroundColor Cyan
Write-Host "  Store Management System - Services Status" -ForegroundColor Cyan
Write-Host "========================================`n" -ForegroundColor Cyan

$allRunning = $true

foreach ($serviceName in $services.Keys) {
    $service = $services[$serviceName]
    $port = $service.Port
    $url = $service.URL
    
    # Check if port is in use
    $portCheck = netstat -ano | Select-String ":$port" | Select-String "LISTENING"
    
    if ($portCheck) {
        $processId = ($portCheck -split '\s+')[-1]
        $procInfo = Get-Process -Id $processId -ErrorAction SilentlyContinue
        
        Write-Host "[✓] $serviceName" -ForegroundColor Green -NoNewline
        Write-Host " - Port $port - PID: $processId" -ForegroundColor Gray
        
        # Try to check if service is responding
        try {
            $response = Invoke-WebRequest -Uri $url -TimeoutSec 2 -UseBasicParsing -ErrorAction SilentlyContinue
            if ($response.StatusCode -eq 200) {
                Write-Host "     Status: Running and responding" -ForegroundColor Green
            }
        } catch {
            Write-Host "     Status: Port open but not responding" -ForegroundColor Yellow
        }
    } else {
        Write-Host "[✗] $serviceName" -ForegroundColor Red -NoNewline
        Write-Host " - Port $port - Not running" -ForegroundColor Gray
        $allRunning = $false
    }
}

Write-Host "`n========================================" -ForegroundColor Cyan

if ($allRunning) {
    Write-Host "All services are running! ✓" -ForegroundColor Green
} else {
    Write-Host "Some services are not running. Check above for details." -ForegroundColor Yellow
}

Write-Host "`nTo start services:" -ForegroundColor Cyan
Write-Host "  Frontend:  cd frontend && npm run dev" -ForegroundColor White
Write-Host "  Backend:   cd backend && python main.py" -ForegroundColor White
Write-Host "`n"

