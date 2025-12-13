#!/usr/bin/env pwsh
<#
.SYNOPSIS
    Store ERP - Complete System Startup Script (PowerShell)
    
.DESCRIPTION
    Starts the complete Store ERP system:
    - Backend (Flask API on port 5002)
    - Frontend (React/Vite on port 5502)
    - Database migrations and initialization
    - Health checks and monitoring
    
.PARAMETER Mode
    Startup mode: 'dev' (development) or 'prod' (production via Docker)
    
.PARAMETER SkipMigration
    Skip database migration check
    
.PARAMETER SkipFrontend
    Skip frontend startup (backend only)
    
.PARAMETER SkipBackend
    Skip backend startup (frontend only)
    
.PARAMETER Clean
    Clean install (delete node_modules and .venv before starting)
    
.PARAMETER OpenBrowser
    Automatically open the application in the default browser
    
.PARAMETER SkipDocker
    Skip Docker services startup (useful if Docker is not needed)
    
.EXAMPLE
    .\start-system.ps1
    Start system in development mode with all services
    
.EXAMPLE
    .\start-system.ps1 -OpenBrowser
    Start system and automatically open browser
    
.EXAMPLE
    .\start-system.ps1 -Mode prod
    Start system in production mode using Docker
    
.EXAMPLE
    .\start-system.ps1 -SkipFrontend
    Start backend only
    
.EXAMPLE
    .\start-system.ps1 -Clean
    Perform clean installation (removes existing dependencies)
    
.EXAMPLE
    .\start-system.ps1 -SkipDocker
    Start without Docker services
#>

param(
    [Parameter(Mandatory=$false)]
    [ValidateSet('dev', 'prod')]
    [string]$Mode = 'dev',
    
    [Parameter(Mandatory=$false)]
    [switch]$SkipMigration,
    
    [Parameter(Mandatory=$false)]
    [switch]$SkipFrontend,
    
    [Parameter(Mandatory=$false)]
    [switch]$SkipBackend,
    
    [Parameter(Mandatory=$false)]
    [switch]$Clean,
    
    [Parameter(Mandatory=$false)]
    [switch]$OpenBrowser,
    
    [Parameter(Mandatory=$false)]
    [switch]$SkipDocker
)

# ============================================================================
# Configuration
# ============================================================================

$ErrorActionPreference = "Continue"
$SCRIPT_DIR = Split-Path -Parent $MyInvocation.MyCommand.Path
$BACKEND_DIR = Join-Path $SCRIPT_DIR "backend"
$FRONTEND_DIR = Join-Path $SCRIPT_DIR "frontend"
$BACKEND_PORT = 5002
$FRONTEND_PORT = 5502
$DOCKER_SERVICES = @("redis", "postgres", "monitoring")  # Docker services to start

# Colors for output
$ColorSuccess = "Green"
$ColorError = "Red"
$ColorWarning = "Yellow"
$ColorInfo = "Cyan"

# ============================================================================
# Helper Functions
# ============================================================================

function Write-Header {
    param([string]$Message)
    Write-Host "`n========================================" -ForegroundColor $ColorInfo
    Write-Host $Message -ForegroundColor $ColorInfo
    Write-Host "========================================`n" -ForegroundColor $ColorInfo
}

function Write-Success {
    param([string]$Message)
    Write-Host "✅ $Message" -ForegroundColor $ColorSuccess
}

function Write-Error-Message {
    param([string]$Message)
    Write-Host "❌ $Message" -ForegroundColor $ColorError
}

function Write-Warning-Message {
    param([string]$Message)
    Write-Host "⚠️  $Message" -ForegroundColor $ColorWarning
}

function Write-Info {
    param([string]$Message)
    Write-Host "ℹ️  $Message" -ForegroundColor $ColorInfo
}

function Test-Command {
    param([string]$Command)
    try {
        Get-Command $Command -ErrorAction Stop | Out-Null
        return $true
    }
    catch {
        return $false
    }
}

function Test-Port {
    param([int]$Port)
    try {
        $connection = Test-NetConnection -ComputerName localhost -Port $Port -InformationLevel Quiet -WarningAction SilentlyContinue
        return $connection
    }
    catch {
        return $false
    }
}

function Stop-ProcessOnPort {
    param([int]$Port)
    
    try {
        $process = Get-NetTCPConnection -LocalPort $Port -ErrorAction SilentlyContinue | 
                   Select-Object -ExpandProperty OwningProcess -First 1
        
        if ($process) {
            Write-Warning-Message "Port $Port is in use by process $process. Stopping it..."
            Stop-Process -Id $process -Force -ErrorAction SilentlyContinue
            Start-Sleep -Seconds 2
            Write-Success "Process stopped"
            return $true
        }
    }
    catch {
        Write-Warning-Message "Could not check or stop process on port $Port"
    }
    return $false
}

# ============================================================================
# Pre-flight Checks
# ============================================================================

function Test-Prerequisites {
    Write-Header "System Prerequisites Check"
    
    $allOk = $true
    
    # Check Python
    if (Test-Command "python") {
        $pythonVersion = python --version 2>&1
        Write-Success "Python installed: $pythonVersion"
    }
    else {
        Write-Error-Message "Python is not installed or not in PATH"
        $allOk = $false
    }
    
    # Check Node.js (only if frontend is needed)
    if (-not $SkipFrontend) {
        if (Test-Command "node") {
            $nodeVersion = node --version
            Write-Success "Node.js installed: $nodeVersion"
        }
        else {
            Write-Error-Message "Node.js is not installed or not in PATH"
            $allOk = $false
        }
        
        # Check npm
        if (Test-Command "npm") {
            $npmVersion = npm --version
            Write-Success "npm installed: v$npmVersion"
        }
        else {
            Write-Error-Message "npm is not installed or not in PATH"
            $allOk = $false
        }
    }
    
    # Check Docker (only for production mode)
    # Check Docker (always check in dev mode too for optional services)
    if (Test-Command "docker") {
        $dockerVersion = docker --version
        Write-Success "Docker installed: $dockerVersion"
        
        # Check if Docker daemon is running
        try {
            docker ps 2>&1 | Out-Null
            if ($LASTEXITCODE -eq 0) {
                Write-Success "Docker daemon is running"
            }
            else {
                Write-Warning-Message "Docker is installed but daemon is not running"
            }
        }
        catch {
            Write-Warning-Message "Docker daemon may not be running"
        }
    }
    else {
        if ($Mode -eq 'prod') {
            Write-Error-Message "Docker is not installed or not in PATH"
            $allOk = $false
        }
        else {
            Write-Warning-Message "Docker is not installed (optional for development)"
        }
    }
    
    if (Test-Command "docker-compose") {
        $composeVersion = docker-compose --version
        Write-Success "Docker Compose installed: $composeVersion"
    }
    else {
        if ($Mode -eq 'prod') {
            Write-Error-Message "Docker Compose is not installed"
            $allOk = $false
        }
        else {
            Write-Warning-Message "Docker Compose is not installed (optional for development)"
        }
    }
    
    if (-not $allOk) {
        Write-Error-Message "Prerequisites check failed. Please install missing dependencies."
        exit 1
    }
    
    Write-Success "All prerequisites satisfied"
}

# ============================================================================
# Docker Services
# ============================================================================

function Start-DockerServices {
    Write-Header "Starting Docker Services"
    
    # Check if Docker is available
    if (-not (Test-Command "docker")) {
        Write-Warning-Message "Docker is not installed. Skipping Docker services."
        return $false
    }
    
    # Check if docker-compose.yml exists
    $composeFile = Join-Path $SCRIPT_DIR "docker-compose.yml"
    if (-not (Test-Path $composeFile)) {
        Write-Warning-Message "docker-compose.yml not found. Skipping Docker services."
        return $false
    }
    
    Set-Location $SCRIPT_DIR
    
    try {
        Write-Info "Starting Docker Compose services..."
        
        # Start services in detached mode
        docker-compose up -d
        
        if ($LASTEXITCODE -eq 0) {
            Write-Success "Docker services started successfully"
            
            # Wait for services to be healthy
            Write-Info "Waiting for services to be ready..."
            Start-Sleep -Seconds 10
            
            # Show running containers
            Write-Info "Running Docker containers:"
            docker-compose ps
            
            return $true
        }
        else {
            Write-Warning-Message "Docker Compose returned non-zero exit code"
            return $false
        }
    }
    catch {
        Write-Warning-Message "Failed to start Docker services: $_"
        return $false
    }
}

function Stop-DockerServices {
    Write-Header "Stopping Docker Services"
    
    if (-not (Test-Command "docker-compose")) {
        return
    }
    
    $composeFile = Join-Path $SCRIPT_DIR "docker-compose.yml"
    if (-not (Test-Path $composeFile)) {
        return
    }
    
    Set-Location $SCRIPT_DIR
    
    try {
        Write-Info "Stopping Docker Compose services..."
        docker-compose down
        Write-Success "Docker services stopped"
    }
    catch {
        Write-Warning-Message "Failed to stop Docker services: $_"
    }
}

# ============================================================================
# Backend Setup
# ============================================================================

function Initialize-Backend {
    Write-Header "Backend Setup"
    
    Set-Location $BACKEND_DIR
    
    # Clean install if requested
    if ($Clean) {
        Write-Info "Performing clean install..."
        if (Test-Path ".venv") {
            Remove-Item -Recurse -Force ".venv"
            Write-Success "Removed .venv directory"
        }
    }
    
    # Create virtual environment if it doesn't exist
    if (-not (Test-Path ".venv")) {
        Write-Info "Creating Python virtual environment..."
        python -m venv .venv
        
        if ($LASTEXITCODE -ne 0) {
            Write-Error-Message "Failed to create virtual environment"
            return $false
        }
        Write-Success "Virtual environment created"
    }
    
    # Activate virtual environment
    Write-Info "Activating virtual environment..."
    $activateScript = Join-Path $BACKEND_DIR ".venv\Scripts\Activate.ps1"
    
    if (Test-Path $activateScript) {
        . $activateScript
        Write-Success "Virtual environment activated"
    }
    else {
        Write-Error-Message "Could not find activation script"
        return $false
    }
    
    # Install/upgrade dependencies
    Write-Info "Installing backend dependencies..."
    python -m pip install --upgrade pip -q
    pip install -r requirements.txt -q
    
    if ($LASTEXITCODE -ne 0) {
        Write-Warning-Message "Some dependencies may have failed to install"
    }
    else {
        Write-Success "Backend dependencies installed"
    }
    
    return $true
}

function Initialize-Database {
    param([bool]$Force = $false)
    
    Write-Header "Database Initialization"
    
    Set-Location $BACKEND_DIR
    
    # Ensure instance directory exists
    $instanceDir = Join-Path $BACKEND_DIR "instance"
    if (-not (Test-Path $instanceDir)) {
        New-Item -ItemType Directory -Path $instanceDir | Out-Null
        Write-Success "Created instance directory"
    }
    
    # Check if database exists
    $dbPath = Join-Path $BACKEND_DIR "instance\inventory.db"
    $dbExists = Test-Path $dbPath
    
    if ($dbExists -and -not $Force) {
        Write-Info "Database already exists at: $dbPath"
        
        # Run migration check
        Write-Info "Checking for pending migrations..."
        
        try {
            # Check if Alembic migrations exist
            $migrationsDir = Join-Path $BACKEND_DIR "migrations\versions"
            
            if (Test-Path $migrationsDir) {
                Write-Info "Running database migrations..."
                
                # Set environment variables for Flask
                $env:FLASK_APP = "app.py"
                
                python -m flask db upgrade
                
                if ($LASTEXITCODE -eq 0) {
                    Write-Success "Database migrations applied successfully"
                }
                else {
                    Write-Warning-Message "Migration command returned non-zero exit code"
                }
            }
            else {
                Write-Info "No migrations directory found, initializing..."
                
                # Initialize Alembic
                $env:FLASK_APP = "app.py"
                python -m flask db init
                
                if ($LASTEXITCODE -eq 0) {
                    Write-Success "Migrations initialized"
                }
            }
        }
        catch {
            Write-Warning-Message "Could not run migrations: $_"
        }
        
        # Verify database integrity
        Write-Info "Verifying database integrity..."
        $checkScript = Join-Path $BACKEND_DIR "check_tables.py"
        if (Test-Path $checkScript) {
            python $checkScript
        }
    }
    else {
        Write-Info "Initializing new database..."
        
        # Initialize database using database_setup.py if available
        $setupScript = Join-Path $BACKEND_DIR "database_setup.py"
        
        if (Test-Path $setupScript) {
            Write-Info "Running comprehensive database setup..."
            python $setupScript
            
            if ($LASTEXITCODE -eq 0) {
                Write-Success "Database initialized successfully"
            }
            else {
                Write-Warning-Message "Database setup script returned warnings"
            }
        }
        else {
            # Fallback to Flask db init
            Write-Info "Initializing database with Flask-Migrate..."
            
            $env:FLASK_APP = "app.py"
            
            if (-not (Test-Path "migrations")) {
                python -m flask db init
            }
            
            python -m flask db migrate -m "Initial migration"
            python -m flask db upgrade
            
            Write-Success "Database created via Flask-Migrate"
            
            # Create admin user if available
            $adminScript = Join-Path $BACKEND_DIR "create_admin_user.py"
            if (Test-Path $adminScript) {
                Write-Info "Creating admin user..."
                python $adminScript
            }
        }
    }
    
    # Ensure default data exists
    Write-Info "Ensuring default data exists..."
    try {
        # Try to run default data creation if script exists
        $defaultDataScript = Join-Path $BACKEND_DIR "ensure_tables.py"
        if (Test-Path $defaultDataScript) {
            python $defaultDataScript
        }
    }
    catch {
        Write-Warning-Message "Could not ensure default data: $_"
    }
    
    Write-Success "Database ready"
    return $true
}

function Start-Backend {
    Write-Header "Starting Backend Server"
    
    Set-Location $BACKEND_DIR
    
    # Check if port is in use
    if (Test-Port $BACKEND_PORT) {
        Write-Warning-Message "Backend port $BACKEND_PORT is already in use"
        $response = Read-Host "Stop existing process? (Y/n)"
        
        if ($response -eq '' -or $response -match '^[Yy]') {
            Stop-ProcessOnPort $BACKEND_PORT
        }
        else {
            Write-Error-Message "Cannot start backend - port is in use"
            return $false
        }
    }
    
    Write-Info "Starting Flask development server on port $BACKEND_PORT..."
    
    # Set environment variables
    $env:FLASK_APP = "app.py"
    $env:FLASK_ENV = "development"
    $env:FLASK_DEBUG = "1"
    
    # Start backend in a new window
    $backendCmd = "cd '$BACKEND_DIR'; .\.venv\Scripts\Activate.ps1; python app.py"
    
    Start-Process pwsh -ArgumentList "-NoExit", "-Command", $backendCmd -WindowStyle Normal
    
    # Wait for backend to be ready
    Write-Info "Waiting for backend to start..."
    $maxAttempts = 30
    $attempt = 0
    
    while ($attempt -lt $maxAttempts) {
        Start-Sleep -Seconds 1
        
        if (Test-Port $BACKEND_PORT) {
            Write-Success "Backend server is running on http://localhost:$BACKEND_PORT"
            return $true
        }
        
        $attempt++
        Write-Host "." -NoNewline
    }
    
    Write-Host ""
    Write-Warning-Message "Backend may still be starting. Check the backend window for details."
    return $true
}

# ============================================================================
# Frontend Setup
# ============================================================================

function Initialize-Frontend {
    Write-Header "Frontend Setup"
    
    Set-Location $FRONTEND_DIR
    
    # Clean install if requested
    if ($Clean) {
        Write-Info "Performing clean install..."
        if (Test-Path "node_modules") {
            Remove-Item -Recurse -Force "node_modules"
            Write-Success "Removed node_modules directory"
        }
        if (Test-Path "package-lock.json") {
            Remove-Item -Force "package-lock.json"
            Write-Success "Removed package-lock.json"
        }
    }
    
    # Install dependencies
    if (-not (Test-Path "node_modules") -or $Clean) {
        Write-Info "Installing frontend dependencies..."
        npm install
        
        if ($LASTEXITCODE -ne 0) {
            Write-Error-Message "Failed to install frontend dependencies"
            return $false
        }
        Write-Success "Frontend dependencies installed"
    }
    else {
        Write-Info "Frontend dependencies already installed"
    }
    
    return $true
}

function Start-Frontend {
    Write-Header "Starting Frontend Server"
    
    Set-Location $FRONTEND_DIR
    
    # Check if port is in use
    if (Test-Port $FRONTEND_PORT) {
        Write-Warning-Message "Frontend port $FRONTEND_PORT is already in use"
        $response = Read-Host "Stop existing process? (Y/n)"
        
        if ($response -eq '' -or $response -match '^[Yy]') {
            Stop-ProcessOnPort $FRONTEND_PORT
        }
        else {
            Write-Error-Message "Cannot start frontend - port is in use"
            return $false
        }
    }
    
    Write-Info "Starting Vite development server on port $FRONTEND_PORT..."
    
    # Start frontend in a new window
    $frontendCmd = "cd '$FRONTEND_DIR'; npm run dev"
    
    Start-Process pwsh -ArgumentList "-NoExit", "-Command", $frontendCmd -WindowStyle Normal
    
    # Wait for frontend to be ready
    Write-Info "Waiting for frontend to start..."
    $maxAttempts = 30
    $attempt = 0
    
    while ($attempt -lt $maxAttempts) {
        Start-Sleep -Seconds 1
        
        if (Test-Port $FRONTEND_PORT) {
            Write-Success "Frontend server is running on http://localhost:$FRONTEND_PORT"
            return $true
        }
        
        $attempt++
        Write-Host "." -NoNewline
    }
    
    Write-Host ""
    Write-Warning-Message "Frontend may still be starting. Check the frontend window for details."
    return $true
}

# ============================================================================
# Production Mode (Docker)
# ============================================================================

function Start-Production {
    Write-Header "Starting Production Environment"
    
    Set-Location $SCRIPT_DIR
    
    # Check for .env file
    if (-not (Test-Path ".env")) {
        Write-Warning-Message ".env file not found"
        
        if (Test-Path ".env.example") {
            Write-Info "Creating .env from .env.example..."
            Copy-Item ".env.example" ".env"
            Write-Success "Created .env file. Please review and update configuration."
            
            $response = Read-Host "Continue with default configuration? (Y/n)"
            if ($response -match '^[Nn]') {
                Write-Info "Please edit .env file and run this script again"
                exit 0
            }
        }
        else {
            Write-Error-Message ".env.example not found"
            exit 1
        }
    }
    
    Write-Info "Starting Docker Compose production stack..."
    
    # Stop existing containers
    docker-compose -f docker-compose.prod.yml down 2>$null
    
    # Start production stack
    docker-compose -f docker-compose.prod.yml up -d --build
    
    if ($LASTEXITCODE -eq 0) {
        Write-Success "Production stack started successfully"
        
        Write-Info "Waiting for services to be ready..."
        Start-Sleep -Seconds 10
        
        Write-Header "Production Services"
        Write-Host "Frontend:    http://localhost:80" -ForegroundColor $ColorSuccess
        Write-Host "Backend API: http://localhost:5001/api" -ForegroundColor $ColorSuccess
        Write-Host "Health:      http://localhost:5001/health" -ForegroundColor $ColorSuccess
        
        Write-Host "`nUseful commands:" -ForegroundColor $ColorInfo
        Write-Host "  View logs:    docker-compose -f docker-compose.prod.yml logs -f" -ForegroundColor $ColorInfo
        Write-Host "  Stop all:     docker-compose -f docker-compose.prod.yml down" -ForegroundColor $ColorInfo
        Write-Host "  Restart:      docker-compose -f docker-compose.prod.yml restart" -ForegroundColor $ColorInfo
        
        return $true
    }
    else {
        Write-Error-Message "Failed to start production stack"
        return $false
    }
}

# ============================================================================
# Health Checks
# ============================================================================

function Test-SystemHealth {
    Write-Header "System Health Check"
    
    # Check backend health
    if (-not $SkipBackend) {
        try {
            Write-Info "Checking backend health..."
            $response = Invoke-WebRequest -Uri "http://localhost:$BACKEND_PORT/health" -TimeoutSec 5 -UseBasicParsing
            
            if ($response.StatusCode -eq 200) {
                Write-Success "Backend is healthy"
            }
            else {
                Write-Warning-Message "Backend returned status code: $($response.StatusCode)"
            }
        }
        catch {
            Write-Warning-Message "Backend health check failed: $($_.Exception.Message)"
        }
    }
    
    # Check frontend
    if (-not $SkipFrontend) {
        try {
            Write-Info "Checking frontend..."
            $response = Invoke-WebRequest -Uri "http://localhost:$FRONTEND_PORT" -TimeoutSec 5 -UseBasicParsing
            
            if ($response.StatusCode -eq 200) {
                Write-Success "Frontend is accessible"
            }
            else {
                Write-Warning-Message "Frontend returned status code: $($response.StatusCode)"
            }
        }
        catch {
            Write-Warning-Message "Frontend health check failed: $($_.Exception.Message)"
        }
    }
}

# ============================================================================
# Main Execution
# ============================================================================

function Start-System {
    Clear-Host
    
    Write-Host @"
╔════════════════════════════════════════════════════════════════╗
║                                                                ║
║              Store ERP - System Startup Script                 ║
║                                                                ║
║  Mode: $($Mode.ToUpper().PadRight(53)) ║
╚════════════════════════════════════════════════════════════════╝
"@ -ForegroundColor $ColorInfo
    
    # Run prerequisite checks
    Test-Prerequisites
    
    # Start Docker services (in both dev and prod mode)
    $dockerStarted = $false
    if (-not $SkipDocker) {
        Write-Info "Starting Docker services (optional)..."
        $dockerStarted = Start-DockerServices
        
        if ($dockerStarted) {
            Write-Success "Docker services are running"
        }
        else {
            Write-Warning-Message "Docker services not started (continuing without them)"
        }
    }
    else {
        Write-Info "Skipping Docker services (--SkipDocker specified)"
    }
    
    # Production mode uses Docker
    if ($Mode -eq 'prod') {
        if (Start-Production) {
            Write-Header "🎉 Production System Started Successfully!"
        }
        else {
            Write-Error-Message "Failed to start production system"
            exit 1
        }
        return
    }
    
    # Development mode - start services individually
    
    # Backend setup
    if (-not $SkipBackend) {
        if (-not (Initialize-Backend)) {
            Write-Error-Message "Backend initialization failed"
            exit 1
        }
        
        if (-not $SkipMigration) {
            if (-not (Initialize-Database)) {
                Write-Error-Message "Database initialization failed"
                exit 1
            }
        }
        
        if (-not (Start-Backend)) {
            Write-Error-Message "Failed to start backend"
            exit 1
        }
    }
    
    # Frontend setup
    if (-not $SkipFrontend) {
        if (-not (Initialize-Frontend)) {
            Write-Error-Message "Frontend initialization failed"
            exit 1
        }
        
        if (-not (Start-Frontend)) {
            Write-Error-Message "Failed to start frontend"
            exit 1
        }
    }
    
    # Health checks
    Start-Sleep -Seconds 5
    Test-SystemHealth
    
    # Final summary
    Write-Header "🎉 Development System Started Successfully!"
    
    if ($dockerStarted) {
        Write-Host "`nDocker Services:" -ForegroundColor $ColorInfo
        Write-Host "  Status: " -NoNewline -ForegroundColor $ColorInfo
        Write-Host "Running" -ForegroundColor $ColorSuccess
        Write-Host "  View:   docker-compose ps" -ForegroundColor $ColorInfo
        Write-Host "  Logs:   docker-compose logs -f" -ForegroundColor $ColorInfo
        Write-Host "  Stop:   docker-compose down" -ForegroundColor $ColorInfo
    }
    
    if (-not $SkipBackend) {
        Write-Host "`nBackend API:" -ForegroundColor $ColorInfo
        Write-Host "  Server:   " -NoNewline -ForegroundColor $ColorInfo
        Write-Host "http://localhost:$BACKEND_PORT" -ForegroundColor $ColorSuccess
        Write-Host "  API Docs: " -NoNewline -ForegroundColor $ColorInfo
        Write-Host "http://localhost:$BACKEND_PORT/api/docs" -ForegroundColor $ColorSuccess
        Write-Host "  Health:   " -NoNewline -ForegroundColor $ColorInfo
        Write-Host "http://localhost:$BACKEND_PORT/health" -ForegroundColor $ColorSuccess
        Write-Host "  Database: " -NoNewline -ForegroundColor $ColorInfo
        Write-Host "SQLite (instance/inventory.db)" -ForegroundColor $ColorSuccess
    }
    
    if (-not $SkipFrontend) {
        Write-Host "`nFrontend App:" -ForegroundColor $ColorInfo
        Write-Host "  Server: " -NoNewline -ForegroundColor $ColorInfo
        Write-Host "http://localhost:$FRONTEND_PORT" -ForegroundColor $ColorSuccess
    }
    
    Write-Host "`n" -NoNewline
    Write-Host "Quick Actions:" -ForegroundColor $ColorInfo
    Write-Host "  Stop backend:     Ctrl+C in backend window" -ForegroundColor $ColorInfo
    Write-Host "  Stop frontend:    Ctrl+C in frontend window" -ForegroundColor $ColorInfo
    Write-Host "  Stop Docker:      docker-compose down" -ForegroundColor $ColorInfo
    Write-Host "  View logs:        Check terminal windows" -ForegroundColor $ColorInfo
    Write-Host "  Restart system:   .\start-system.bat" -ForegroundColor $ColorInfo
    Write-Host "  Clean restart:    .\start-system.bat -Clean" -ForegroundColor $ColorInfo
    
    Write-Host "`n" -NoNewline
    Write-Host "Default Admin Credentials:" -ForegroundColor $ColorWarning
    Write-Host "  Username: admin" -ForegroundColor $ColorWarning
    Write-Host "  Password: admin123" -ForegroundColor $ColorWarning
    Write-Host "  (Change these after first login!)" -ForegroundColor $ColorWarning
    
    Write-Host "`n" -NoNewline
    Write-Host "System Components:" -ForegroundColor $ColorInfo
    Write-Host "  ✅ Python virtual environment" -ForegroundColor $ColorSuccess
    Write-Host "  ✅ Node.js dependencies" -ForegroundColor $ColorSuccess
    Write-Host "  ✅ Database initialized" -ForegroundColor $ColorSuccess
    Write-Host "  ✅ Default data created" -ForegroundColor $ColorSuccess
    if ($dockerStarted) {
        Write-Host "  ✅ Docker services running" -ForegroundColor $ColorSuccess
    }
    else {
        Write-Host "  ⚠️  Docker services not running" -ForegroundColor $ColorWarning
    }
    
    # Open browser if requested
    if ($OpenBrowser) {
        Write-Host "`n" -NoNewline
        Write-Info "Opening browser..."
        Start-Sleep -Seconds 2
        
        if (-not $SkipFrontend) {
            Start-Process "http://localhost:$FRONTEND_PORT"
            Write-Success "Browser opened to frontend"
        }
        elseif (-not $SkipBackend) {
            Start-Process "http://localhost:$BACKEND_PORT"
            Write-Success "Browser opened to backend"
        }
    }
    
    Write-Host "`n"
}

# Run the main function
Start-System
