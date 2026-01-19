# Nginx Configuration Restore Script
# Run this after starting a project's containers to enable Nginx proxy for that project

param(
    [Parameter(Mandatory=$true)]
    [ValidateSet('test_projects','gold_price_predictor','zakat','scan_ai_manus','gaara_erp','store','all')]
    [string]$Project
)

function Restore-NginxConfig {
    param([string]$ConfigName)
    
    $source = ".\nginx\conf.d.backup\$ConfigName.conf"
    $dest = ".\nginx\conf.d\$ConfigName.conf"
    
    if (Test-Path $source) {
        Copy-Item $source $dest -Force
        Write-Host "✓ Restored $ConfigName.conf" -ForegroundColor Green
        return $true
    } else {
        Write-Host "✗ Config file not found: $ConfigName.conf" -ForegroundColor Red
        return $false
    }
}

function Reload-Nginx {
    Write-Host "`nReloading Nginx..." -ForegroundColor Cyan
    docker exec nginx-proxy nginx -t
    if ($LASTEXITCODE -eq 0) {
        docker exec nginx-proxy nginx -s reload
        Write-Host "✓ Nginx reloaded successfully" -ForegroundColor Green
    } else {
        Write-Host "✗ Nginx configuration test failed" -ForegroundColor Red
        exit 1
    }
}

Write-Host "Starting Nginx configuration restore..." -ForegroundColor Cyan
Write-Host "Project: $Project`n" -ForegroundColor Yellow

if ($Project -eq 'all') {
    $configs = @('test_projects', 'gold_price_predictor', 'zakat', 'scan_ai_manus', 'gaara_erp', 'store')
    foreach ($config in $configs) {
        Restore-NginxConfig $config
    }
} else {
    Restore-NginxConfig $Project
}

Reload-Nginx

Write-Host "`n✓ Configuration restore complete!" -ForegroundColor Green
