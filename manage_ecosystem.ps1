<#
.SYNOPSIS
    Speckit Ecosystem Manager
.DESCRIPTION
    Manages the lifecycle of the Global Nginx Proxy and the 6 Projects.
#>

function Show-Menu {
    Clear-Host
    Write-Host "============================" -ForegroundColor Cyan
    Write-Host "   Speckit Ecosystem Hub    " -ForegroundColor Cyan
    Write-Host "============================" -ForegroundColor Cyan
    Write-Host "1. Start Global Proxy (Nginx)"
    Write-Host "2. Stop Global Proxy"
    Write-Host "----------------------------"
    Write-Host "3. Start Project 1 (Global)"
    Write-Host "4. Start Project 2 (Gold)"
    Write-Host "5. Start Project 3 (Zakat)"
    Write-Host "6. Start Project 4 (ScanAI)"
    Write-Host "7. Start Project 5 (Gaara)"
    Write-Host "8. Start Project 6 (Store)"
    Write-Host "----------------------------"
    Write-Host "9. Stop ALL Projects"
    Write-Host "0. Exit"
    Write-Host "============================"
}

function Start-Proxy {
    Write-Host "Starting Global Nginx Proxy..." -ForegroundColor Green
    docker-compose -f "d:\Ai_Project\docker-compose.global.yml" up -d
    Write-Host "Proxy launched at http://localhost" -ForegroundColor Yellow
}

function Stop-Proxy {
    Write-Host "Stopping Global Nginx Proxy..." -ForegroundColor Yellow
    docker-compose -f "d:\Ai_Project\docker-compose.global.yml" down
}

function Start-Project {
    param($path, $name)
    Write-Host "Starting $name..." -ForegroundColor Green
    Set-Location $path
    docker-compose up -d
    Write-Host "$name started." -ForegroundColor Yellow
}

function Stop-All {
    Write-Host "Stopping ALL Projects and Proxy..." -ForegroundColor Red
    
    # List of paths
    $paths = @(
        "d:\Ai_Project\1-test_projects\global - V1.3 -13-12-2025",
        "d:\Ai_Project\2-gold-price-predictor",
        "d:\Ai_Project\3-Zakat\Zakat_Clean",
        "d:\Ai_Project\4-scan_ai-Manus",
        "d:\Ai_Project\5-gaara_erp",
        "d:\Ai_Project\6-store",
        "d:\Ai_Project" # For global proxy
    )

    foreach ($p in $paths) {
        if (Test-Path "$p\docker-compose.yml" -PathType Leaf) {
            Write-Host "Stopping in $p..."
            Set-Location $p
            docker-compose down
        }
        elseif (Test-Path "$p\docker-compose.global.yml" -PathType Leaf) {
            Write-Host "Stopping Global Proxy..."
            Set-Location $p
            docker-compose -f docker-compose.global.yml down
        }
    }
}

# Main Loop
do {
    Show-Menu
    $userChoice = Read-Host "Select an option"
    switch ($userChoice) {
        '1' { Start-Proxy }
        '2' { Stop-Proxy }
        '3' { Start-Project "d:\Ai_Project\1-test_projects\global - V1.3 -13-12-2025" "Project 1" }
        '4' { Start-Project "d:\Ai_Project\2-gold-price-predictor" "Project 2" }
        '5' { Start-Project "d:\Ai_Project\3-Zakat\Zakat_Clean" "Project 3" }
        '6' { Start-Project "d:\Ai_Project\4-scan_ai-Manus" "Project 4" }
        '7' { Start-Project "d:\Ai_Project\5-gaara_erp" "Project 5" }
        '8' { Start-Project "d:\Ai_Project\6-store" "Project 6" }
        '9' { Stop-All }
        '0' { Write-Host "Exiting..."; break }
        default { Write-Host "Invalid option" -ForegroundColor Red }
    }
    Pause
} while ($true)
