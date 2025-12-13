# Setup HashiCorp Vault - T21 Implementation
# This script sets up Vault and migrates secrets

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  HashiCorp Vault Setup (T21)" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Check if Docker is installed
Write-Host "Checking prerequisites..." -ForegroundColor Yellow
try {
    $dockerVersion = docker --version
    Write-Host "✅ Docker installed: $dockerVersion" -ForegroundColor Green
} catch {
    Write-Host "❌ Docker not found!" -ForegroundColor Red
    Write-Host "   Please install Docker Desktop: https://www.docker.com/products/docker-desktop" -ForegroundColor Yellow
    Write-Host ""
    exit 1
}

Write-Host ""

# Start Vault container
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  Starting Vault Container" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

Write-Host "Starting Vault with Docker Compose..." -ForegroundColor Yellow
try {
    docker-compose -f docker-compose.vault.yml up -d
    Write-Host "✅ Vault container started!" -ForegroundColor Green
} catch {
    Write-Host "❌ Failed to start Vault!" -ForegroundColor Red
    Write-Host "   Error: $($_.Exception.Message)" -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "Waiting for Vault to be ready..." -ForegroundColor Yellow
Start-Sleep -Seconds 5

# Check Vault status
Write-Host ""
Write-Host "Checking Vault status..." -ForegroundColor Yellow

$env:VAULT_ADDR = "http://127.0.0.1:8200"
$env:VAULT_TOKEN = "dev-root-token-change-me"

try {
    $vaultStatus = docker exec store-vault vault status
    Write-Host "✅ Vault is running!" -ForegroundColor Green
    Write-Host ""
    Write-Host $vaultStatus
} catch {
    Write-Host "⚠️  Vault might not be ready yet" -ForegroundColor Yellow
    Write-Host "   Waiting 10 more seconds..." -ForegroundColor Yellow
    Start-Sleep -Seconds 10
}

Write-Host ""

# Enable KV secrets engine
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  Configuring Vault" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

Write-Host "Enabling KV secrets engine..." -ForegroundColor Yellow
try {
    docker exec store-vault vault secrets enable -version=2 -path=secret kv 2>$null
    Write-Host "✅ KV secrets engine enabled!" -ForegroundColor Green
} catch {
    Write-Host "ℹ️  KV secrets engine might already be enabled" -ForegroundColor Cyan
}

Write-Host ""

# Create secret structure
Write-Host "Creating secret structure..." -ForegroundColor Yellow
Write-Host ""

# Development secrets
Write-Host "  Creating development secrets..." -ForegroundColor White

# Generate secure random secrets
$flaskSecret = -join ((65..90) + (97..122) + (48..57) | Get-Random -Count 32 | ForEach-Object {[char]$_})
$jwtSecret = -join ((65..90) + (97..122) + (48..57) | Get-Random -Count 32 | ForEach-Object {[char]$_})

docker exec store-vault vault kv put secret/store-erp/development/flask secret_key="$flaskSecret"
docker exec store-vault vault kv put secret/store-erp/development/jwt secret_key="$jwtSecret"
docker exec store-vault vault kv put secret/store-erp/development/database url="sqlite:///store.db" password=""

Write-Host "  ✅ Development secrets created" -ForegroundColor Green
Write-Host ""

# Production secrets (placeholders)
Write-Host "  Creating production secret placeholders..." -ForegroundColor White

$prodFlaskSecret = -join ((65..90) + (97..122) + (48..57) | Get-Random -Count 64 | ForEach-Object {[char]$_})
$prodJwtSecret = -join ((65..90) + (97..122) + (48..57) | Get-Random -Count 64 | ForEach-Object {[char]$_})

docker exec store-vault vault kv put secret/store-erp/production/flask secret_key="$prodFlaskSecret"
docker exec store-vault vault kv put secret/store-erp/production/jwt secret_key="$prodJwtSecret"
docker exec store-vault vault kv put secret/store-erp/production/database url="postgresql://user:pass@localhost/store" password="CHANGE_ME"

Write-Host "  ✅ Production secret placeholders created" -ForegroundColor Green
Write-Host ""

# Verify secrets
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  Verifying Secrets" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

Write-Host "Reading development Flask secret..." -ForegroundColor Yellow
$flaskSecretRead = docker exec store-vault vault kv get -field=secret_key secret/store-erp/development/flask
if ($flaskSecretRead) {
    Write-Host "✅ Flask secret verified (length: $($flaskSecretRead.Length))" -ForegroundColor Green
} else {
    Write-Host "❌ Failed to read Flask secret!" -ForegroundColor Red
}

Write-Host ""
Write-Host "Reading development JWT secret..." -ForegroundColor Yellow
$jwtSecretRead = docker exec store-vault vault kv get -field=secret_key secret/store-erp/development/jwt
if ($jwtSecretRead) {
    Write-Host "✅ JWT secret verified (length: $($jwtSecretRead.Length))" -ForegroundColor Green
} else {
    Write-Host "❌ Failed to read JWT secret!" -ForegroundColor Red
}

Write-Host ""

# Create Vault policy
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  Creating Vault Policy" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

$policyContent = @"
# Policy for Store ERP application
path "secret/data/store-erp/development/*" {
  capabilities = ["read"]
}

path "secret/data/store-erp/production/*" {
  capabilities = ["read"]
}
"@

# Write policy to temp file
$policyPath = "vault-app-policy.hcl"
$policyContent | Out-File -FilePath $policyPath -Encoding UTF8

# Copy policy to container and apply
docker cp $policyPath store-vault:/tmp/app-policy.hcl
docker exec store-vault vault policy write app-policy /tmp/app-policy.hcl

Remove-Item $policyPath

Write-Host "✅ Vault policy created!" -ForegroundColor Green
Write-Host ""

# Summary
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  Setup Complete!" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

Write-Host "Vault is now running and configured!" -ForegroundColor Green
Write-Host ""
Write-Host "Access Information:" -ForegroundColor Cyan
Write-Host "  URL: http://127.0.0.1:8200" -ForegroundColor White
Write-Host "  Token: dev-root-token-change-me" -ForegroundColor White
Write-Host ""
Write-Host "Environment Variables:" -ForegroundColor Cyan
Write-Host '  $env:VAULT_ADDR = "http://127.0.0.1:8200"' -ForegroundColor Green
Write-Host '  $env:VAULT_TOKEN = "dev-root-token-change-me"' -ForegroundColor Green
Write-Host ""
Write-Host "Secrets Created:" -ForegroundColor Cyan
Write-Host "  ✅ secret/store-erp/development/flask" -ForegroundColor White
Write-Host "  ✅ secret/store-erp/development/jwt" -ForegroundColor White
Write-Host "  ✅ secret/store-erp/development/database" -ForegroundColor White
Write-Host "  ✅ secret/store-erp/production/flask (placeholder)" -ForegroundColor White
Write-Host "  ✅ secret/store-erp/production/jwt (placeholder)" -ForegroundColor White
Write-Host "  ✅ secret/store-erp/production/database (placeholder)" -ForegroundColor White
Write-Host ""
Write-Host "Next Steps:" -ForegroundColor Cyan
Write-Host "  1. Install Python Vault client:" -ForegroundColor White
Write-Host "     pip install hvac" -ForegroundColor Green
Write-Host ""
Write-Host "  2. Test Vault access:" -ForegroundColor White
Write-Host "     docker exec store-vault vault kv get secret/store-erp/development/flask" -ForegroundColor Green
Write-Host ""
Write-Host "  3. Update application code to use Vault" -ForegroundColor White
Write-Host "     See: docs/security/T21_KMS_VAULT_PLAN.md" -ForegroundColor Green
Write-Host ""
Write-Host "  4. Access Vault UI:" -ForegroundColor White
Write-Host "     http://127.0.0.1:8200/ui" -ForegroundColor Green
Write-Host "     Token: dev-root-token-change-me" -ForegroundColor Green
Write-Host ""
Write-Host "Done! 🎉" -ForegroundColor Green
Write-Host ""

