# Install K6 Performance Testing Tool
# This script installs K6 on Windows

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  K6 Installation" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Check if running as administrator
$isAdmin = ([Security.Principal.WindowsPrincipal] [Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)

if (-not $isAdmin) {
    Write-Host "⚠️  Not running as Administrator" -ForegroundColor Yellow
    Write-Host "   Some installation methods require admin privileges" -ForegroundColor Yellow
    Write-Host ""
}

# Check if K6 is already installed
Write-Host "Checking if K6 is already installed..." -ForegroundColor Yellow
try {
    $k6Version = k6 version 2>$null
    if ($k6Version) {
        Write-Host "✅ K6 is already installed!" -ForegroundColor Green
        Write-Host "   Version: $k6Version" -ForegroundColor White
        Write-Host ""
        Write-Host "To update K6, uninstall first and run this script again." -ForegroundColor Cyan
        Write-Host ""
        exit 0
    }
} catch {
    Write-Host "ℹ️  K6 not found - proceeding with installation" -ForegroundColor Cyan
    Write-Host ""
}

# Installation options
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  Installation Options" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Choose an installation method:" -ForegroundColor Yellow
Write-Host ""
Write-Host "1. Chocolatey (Recommended - requires admin)" -ForegroundColor White
Write-Host "2. Scoop (No admin required)" -ForegroundColor White
Write-Host "3. Manual download (No package manager)" -ForegroundColor White
Write-Host "4. Exit" -ForegroundColor White
Write-Host ""

$choice = Read-Host "Enter your choice (1-4)"

switch ($choice) {
    "1" {
        # Chocolatey installation
        Write-Host ""
        Write-Host "========================================" -ForegroundColor Cyan
        Write-Host "  Installing via Chocolatey" -ForegroundColor Cyan
        Write-Host "========================================" -ForegroundColor Cyan
        Write-Host ""
        
        # Check if Chocolatey is installed
        try {
            $chocoVersion = choco --version 2>$null
            Write-Host "✅ Chocolatey found: $chocoVersion" -ForegroundColor Green
            Write-Host ""
        } catch {
            Write-Host "❌ Chocolatey not found!" -ForegroundColor Red
            Write-Host ""
            Write-Host "Installing Chocolatey..." -ForegroundColor Yellow
            Write-Host "This requires administrator privileges." -ForegroundColor Yellow
            Write-Host ""
            
            if (-not $isAdmin) {
                Write-Host "❌ Please run this script as Administrator!" -ForegroundColor Red
                Write-Host ""
                Write-Host "Right-click PowerShell and select 'Run as Administrator'" -ForegroundColor Yellow
                Write-Host ""
                exit 1
            }
            
            try {
                Set-ExecutionPolicy Bypass -Scope Process -Force
                [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072
                Invoke-Expression ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))
                Write-Host "✅ Chocolatey installed!" -ForegroundColor Green
                Write-Host ""
            } catch {
                Write-Host "❌ Failed to install Chocolatey!" -ForegroundColor Red
                Write-Host "   Error: $($_.Exception.Message)" -ForegroundColor Red
                Write-Host ""
                Write-Host "Please install Chocolatey manually:" -ForegroundColor Yellow
                Write-Host "   https://chocolatey.org/install" -ForegroundColor Cyan
                Write-Host ""
                exit 1
            }
        }
        
        # Install K6
        Write-Host "Installing K6..." -ForegroundColor Yellow
        try {
            choco install k6 -y
            Write-Host "✅ K6 installed successfully!" -ForegroundColor Green
            Write-Host ""
        } catch {
            Write-Host "❌ Failed to install K6!" -ForegroundColor Red
            Write-Host "   Error: $($_.Exception.Message)" -ForegroundColor Red
            Write-Host ""
            exit 1
        }
    }
    
    "2" {
        # Scoop installation
        Write-Host ""
        Write-Host "========================================" -ForegroundColor Cyan
        Write-Host "  Installing via Scoop" -ForegroundColor Cyan
        Write-Host "========================================" -ForegroundColor Cyan
        Write-Host ""
        
        # Check if Scoop is installed
        try {
            $scoopVersion = scoop --version 2>$null
            Write-Host "✅ Scoop found: $scoopVersion" -ForegroundColor Green
            Write-Host ""
        } catch {
            Write-Host "❌ Scoop not found!" -ForegroundColor Red
            Write-Host ""
            Write-Host "Installing Scoop..." -ForegroundColor Yellow
            Write-Host ""
            
            try {
                Set-ExecutionPolicy RemoteSigned -Scope CurrentUser -Force
                Invoke-RestMethod get.scoop.sh | Invoke-Expression
                Write-Host "✅ Scoop installed!" -ForegroundColor Green
                Write-Host ""
            } catch {
                Write-Host "❌ Failed to install Scoop!" -ForegroundColor Red
                Write-Host "   Error: $($_.Exception.Message)" -ForegroundColor Red
                Write-Host ""
                Write-Host "Please install Scoop manually:" -ForegroundColor Yellow
                Write-Host "   https://scoop.sh" -ForegroundColor Cyan
                Write-Host ""
                exit 1
            }
        }
        
        # Install K6
        Write-Host "Installing K6..." -ForegroundColor Yellow
        try {
            scoop install k6
            Write-Host "✅ K6 installed successfully!" -ForegroundColor Green
            Write-Host ""
        } catch {
            Write-Host "❌ Failed to install K6!" -ForegroundColor Red
            Write-Host "   Error: $($_.Exception.Message)" -ForegroundColor Red
            Write-Host ""
            exit 1
        }
    }
    
    "3" {
        # Manual download
        Write-Host ""
        Write-Host "========================================" -ForegroundColor Cyan
        Write-Host "  Manual Download" -ForegroundColor Cyan
        Write-Host "========================================" -ForegroundColor Cyan
        Write-Host ""
        
        Write-Host "To install K6 manually:" -ForegroundColor Yellow
        Write-Host ""
        Write-Host "1. Go to: https://github.com/grafana/k6/releases/latest" -ForegroundColor White
        Write-Host "2. Download: k6-v*-windows-amd64.zip" -ForegroundColor White
        Write-Host "3. Extract the ZIP file" -ForegroundColor White
        Write-Host "4. Move k6.exe to a folder in your PATH" -ForegroundColor White
        Write-Host "   (e.g., C:\Windows\System32 or C:\Program Files\k6)" -ForegroundColor White
        Write-Host "5. Verify installation: k6 version" -ForegroundColor White
        Write-Host ""
        Write-Host "Opening download page in browser..." -ForegroundColor Cyan
        Start-Process "https://github.com/grafana/k6/releases/latest"
        Write-Host ""
        exit 0
    }
    
    "4" {
        Write-Host ""
        Write-Host "Installation cancelled." -ForegroundColor Yellow
        Write-Host ""
        exit 0
    }
    
    default {
        Write-Host ""
        Write-Host "❌ Invalid choice!" -ForegroundColor Red
        Write-Host ""
        exit 1
    }
}

# Verify installation
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  Verifying Installation" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

Write-Host "Verifying K6 installation..." -ForegroundColor Yellow
try {
    $k6Version = k6 version
    Write-Host "✅ K6 installed successfully!" -ForegroundColor Green
    Write-Host "   Version: $k6Version" -ForegroundColor White
    Write-Host ""
} catch {
    Write-Host "❌ K6 installation verification failed!" -ForegroundColor Red
    Write-Host "   Please restart your terminal and try: k6 version" -ForegroundColor Yellow
    Write-Host ""
    exit 1
}

# Next steps
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  Next Steps" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "K6 is now installed! You can run performance tests:" -ForegroundColor Green
Write-Host ""
Write-Host "1. Start the backend server:" -ForegroundColor White
Write-Host "   cd backend" -ForegroundColor Green
Write-Host "   python app.py" -ForegroundColor Green
Write-Host ""
Write-Host "2. Run K6 tests (in another terminal):" -ForegroundColor White
Write-Host "   k6 run scripts/perf/k6_login.js" -ForegroundColor Green
Write-Host "   k6 run scripts/perf/k6_inventory.js" -ForegroundColor Green
Write-Host "   k6 run scripts/perf/k6_invoices.js" -ForegroundColor Green
Write-Host "   k6 run scripts/perf/k6_full_suite.js" -ForegroundColor Green
Write-Host ""
Write-Host "3. View K6 documentation:" -ForegroundColor White
Write-Host "   docs/performance/K6_TESTING.md" -ForegroundColor Green
Write-Host ""
Write-Host "Done! 🎉" -ForegroundColor Green
Write-Host ""

