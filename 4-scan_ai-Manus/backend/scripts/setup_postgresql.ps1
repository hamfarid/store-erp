# ============================================================================
# GAARA AI - PostgreSQL Setup Script (Windows PowerShell)
# ============================================================================
# FILE: backend/scripts/setup_postgresql.ps1
# PURPOSE: Automated PostgreSQL setup for Gaara AI
# OWNER: DevOps Team
# LAST-AUDITED: 2025-11-18
#
# USAGE:
#   .\scripts\setup_postgresql.ps1
# ============================================================================

Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "🐘 Gaara AI - PostgreSQL Setup" -ForegroundColor Cyan
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host ""

# Configuration
$DB_NAME = "gaara_scan_ai"
$DB_USER = "gaara_user"
$DB_PASSWORD = "GaaraSecure2024!@#"
$DB_HOST = "localhost"
$DB_PORT = "5432"

# Check if PostgreSQL is installed
Write-Host "Checking PostgreSQL installation..." -ForegroundColor Yellow

$psqlPath = Get-Command psql -ErrorAction SilentlyContinue

if (-not $psqlPath) {
    Write-Host "❌ PostgreSQL is not installed or not in PATH" -ForegroundColor Red
    Write-Host ""
    Write-Host "Please install PostgreSQL from:" -ForegroundColor Yellow
    Write-Host "https://www.postgresql.org/download/windows/" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "Or use Docker:" -ForegroundColor Yellow
    Write-Host "docker run --name gaara-postgres -e POSTGRES_PASSWORD=postgres -p 5432:5432 -d postgres:15-alpine" -ForegroundColor Cyan
    exit 1
}

Write-Host "✅ PostgreSQL found: $($psqlPath.Source)" -ForegroundColor Green
Write-Host ""

# Check if PostgreSQL service is running
Write-Host "Checking PostgreSQL service..." -ForegroundColor Yellow

$service = Get-Service -Name "postgresql*" -ErrorAction SilentlyContinue | Where-Object { $_.Status -eq "Running" } | Select-Object -First 1

if (-not $service) {
    Write-Host "⚠️  PostgreSQL service is not running" -ForegroundColor Yellow
    Write-Host "Attempting to start PostgreSQL service..." -ForegroundColor Yellow
    
    $allServices = Get-Service -Name "postgresql*" -ErrorAction SilentlyContinue
    if ($allServices) {
        $serviceToStart = $allServices | Select-Object -First 1
        Start-Service $serviceToStart.Name -ErrorAction SilentlyContinue
        Start-Sleep -Seconds 3
        
        $service = Get-Service -Name $serviceToStart.Name
        if ($service.Status -eq "Running") {
            Write-Host "✅ PostgreSQL service started" -ForegroundColor Green
        } else {
            Write-Host "❌ Failed to start PostgreSQL service" -ForegroundColor Red
            Write-Host "Please start it manually from Services (services.msc)" -ForegroundColor Yellow
            exit 1
        }
    } else {
        Write-Host "❌ No PostgreSQL service found" -ForegroundColor Red
        exit 1
    }
} else {
    Write-Host "✅ PostgreSQL service is running: $($service.Name)" -ForegroundColor Green
}

Write-Host ""

# Run SQL setup script
Write-Host "Running database setup script..." -ForegroundColor Yellow
Write-Host ""

$sqlScript = Join-Path $PSScriptRoot "setup_postgresql.sql"

if (-not (Test-Path $sqlScript)) {
    Write-Host "❌ SQL script not found: $sqlScript" -ForegroundColor Red
    exit 1
}

# Execute SQL script
$env:PGPASSWORD = "postgres"  # Default postgres password
& psql -U postgres -f $sqlScript 2>&1 | ForEach-Object {
    if ($_ -match "ERROR") {
        Write-Host $_ -ForegroundColor Red
    } elseif ($_ -match "NOTICE|WARNING") {
        Write-Host $_ -ForegroundColor Yellow
    } else {
        Write-Host $_
    }
}

if ($LASTEXITCODE -ne 0) {
    Write-Host ""
    Write-Host "❌ Database setup failed" -ForegroundColor Red
    Write-Host ""
    Write-Host "Common issues:" -ForegroundColor Yellow
    Write-Host "1. Wrong postgres password - Update the script with correct password" -ForegroundColor White
    Write-Host "2. Database already exists - Drop it first: dropdb -U postgres gaara_scan_ai" -ForegroundColor White
    Write-Host "3. User already exists - Drop it first: dropuser -U postgres gaara_user" -ForegroundColor White
    exit 1
}

Write-Host ""
Write-Host "============================================================" -ForegroundColor Green
Write-Host "✅ PostgreSQL Setup Complete!" -ForegroundColor Green
Write-Host "============================================================" -ForegroundColor Green
Write-Host ""
Write-Host "Database Configuration:" -ForegroundColor Cyan
Write-Host "  Database: $DB_NAME" -ForegroundColor White
Write-Host "  User:     $DB_USER" -ForegroundColor White
Write-Host "  Password: $DB_PASSWORD" -ForegroundColor White
Write-Host "  Host:     $DB_HOST" -ForegroundColor White
Write-Host "  Port:     $DB_PORT" -ForegroundColor White
Write-Host ""
Write-Host "Connection String:" -ForegroundColor Cyan
Write-Host "  postgresql://$DB_USER:$DB_PASSWORD@$DB_HOST:$DB_PORT/$DB_NAME" -ForegroundColor White
Write-Host ""
Write-Host "Next Steps:" -ForegroundColor Yellow
Write-Host "  1. Install psycopg2: pip install psycopg2-binary" -ForegroundColor White
Write-Host "  2. Run migrations: alembic upgrade head" -ForegroundColor White
Write-Host "  3. Create admin user: python scripts/create_default_admin.py" -ForegroundColor White
Write-Host "  4. Start application: python src/main.py" -ForegroundColor White
Write-Host ""
Write-Host "⚠️  IMPORTANT: Change the password in production!" -ForegroundColor Red
Write-Host "============================================================" -ForegroundColor Green

