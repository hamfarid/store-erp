# API Testing Script for Store Management System
# This script tests authentication and accounting endpoints

$baseUrl = "http://127.0.0.1:5002"

Write-Host "==================================" -ForegroundColor Cyan
Write-Host "Store API Testing Script" -ForegroundColor Cyan
Write-Host "==================================" -ForegroundColor Cyan

# Test 1: Login
Write-Host "`n[Test 1] Testing Login..." -ForegroundColor Yellow
$loginBody = @{
    username = "admin"
    password = "admin123"
} | ConvertTo-Json

try {
    $loginResponse = Invoke-RestMethod -Uri "$baseUrl/api/auth/login" -Method POST -Body $loginBody -ContentType "application/json"
    $token = $loginResponse.data.access_token
    Write-Host "✓ Login successful!" -ForegroundColor Green
    Write-Host "  Token: $($token.Substring(0, 50))..." -ForegroundColor Gray
} catch {
    Write-Host "✗ Login failed: $_" -ForegroundColor Red
    exit 1
}

# Test 2: Get Currencies
Write-Host "`n[Test 2] Testing Get Currencies..." -ForegroundColor Yellow
$headers = @{
    Authorization = "Bearer $token"
}

try {
    $currenciesResponse = Invoke-RestMethod -Uri "$baseUrl/api/accounting/currencies" -Method GET -Headers $headers
    Write-Host "✓ Get currencies successful!" -ForegroundColor Green
    Write-Host "  Total currencies: $($currenciesResponse.data.Count)" -ForegroundColor Gray
    if ($currenciesResponse.data.Count -gt 0) {
        Write-Host "  Sample: $($currenciesResponse.data[0].code) - $($currenciesResponse.data[0].name)" -ForegroundColor Gray
    }
} catch {
    Write-Host "✗ Get currencies failed: $_" -ForegroundColor Red
}

# Test 3: Create Currency
Write-Host "`n[Test 3] Testing Create Currency..." -ForegroundColor Yellow
$createCurrencyBody = @{
    code = "USD"
    name = "US Dollar"
    symbol = "$"
    exchange_rate = 1.0
    is_active = $true
    is_default = $false
} | ConvertTo-Json

try {
    $createResponse = Invoke-RestMethod -Uri "$baseUrl/api/accounting/currencies" -Method POST -Body $createCurrencyBody -ContentType "application/json" -Headers $headers
    Write-Host "✓ Create currency successful!" -ForegroundColor Green
    Write-Host "  Currency ID: $($createResponse.data.id)" -ForegroundColor Gray
    $currencyId = $createResponse.data.id
} catch {
    Write-Host "! Currency might already exist, trying to get existing..." -ForegroundColor Yellow
    try {
        $existingResponse = Invoke-RestMethod -Uri "$baseUrl/api/accounting/currencies" -Method GET -Headers $headers
        $usdCurrency = $existingResponse.data | Where-Object { $_.code -eq "USD" }
        if ($usdCurrency) {
            $currencyId = $usdCurrency.id
            Write-Host "  Found existing USD currency with ID: $currencyId" -ForegroundColor Gray
        }
    } catch {
        Write-Host "✗ Failed to get existing currencies: $_" -ForegroundColor Red
    }
}

# Test 4: Get Cash Boxes (Treasuries)
Write-Host "`n[Test 4] Testing Get Cash Boxes..." -ForegroundColor Yellow
try {
    $cashBoxesResponse = Invoke-RestMethod -Uri "$baseUrl/api/accounting/cash-boxes" -Method GET -Headers $headers
    Write-Host "✓ Get cash boxes successful!" -ForegroundColor Green
    Write-Host "  Total cash boxes: $($cashBoxesResponse.data.Count)" -ForegroundColor Gray
} catch {
    Write-Host "✗ Get cash boxes failed: $_" -ForegroundColor Red
}

# Test 5: Create Cash Box
Write-Host "`n[Test 5] Testing Create Cash Box..." -ForegroundColor Yellow
$createCashBoxBody = @{
    name = "Main Cash Box"
    description = "Main treasury for daily operations"
    type = "main"
    is_active = $true
    opening_balance = 1000.0
} | ConvertTo-Json

try {
    $createCashBoxResponse = Invoke-RestMethod -Uri "$baseUrl/api/accounting/cash-boxes" -Method POST -Body $createCashBoxBody -ContentType "application/json" -Headers $headers
    Write-Host "✓ Create cash box successful!" -ForegroundColor Green
    Write-Host "  Cash Box ID: $($createCashBoxResponse.data.id)" -ForegroundColor Gray
    $cashBoxId = $createCashBoxResponse.data.id
} catch {
    Write-Host "! Cash box might already exist, trying to get existing..." -ForegroundColor Yellow
    try {
        $existingCashBoxes = Invoke-RestMethod -Uri "$baseUrl/api/accounting/cash-boxes" -Method GET -Headers $headers
        $mainCashBox = $existingCashBoxes.data | Where-Object { $_.name -eq "Main Cash Box" }
        if ($mainCashBox) {
            $cashBoxId = $mainCashBox.id
            Write-Host "  Found existing cash box with ID: $cashBoxId" -ForegroundColor Gray
        } else {
            Write-Host "  No existing Main Cash Box found" -ForegroundColor Gray
        }
    } catch {
        Write-Host "✗ Failed to get existing cash boxes: $_" -ForegroundColor Red
    }
}

# Test 6: Get Vouchers
Write-Host "`n[Test 6] Testing Get Vouchers..." -ForegroundColor Yellow
try {
    $vouchersResponse = Invoke-RestMethod -Uri "$baseUrl/api/accounting/vouchers" -Method GET -Headers $headers
    Write-Host "✓ Get vouchers successful!" -ForegroundColor Green
    Write-Host "  Total vouchers: $($vouchersResponse.data.Count)" -ForegroundColor Gray
} catch {
    Write-Host "✗ Get vouchers failed: $_" -ForegroundColor Red
}

# Test 7: Get Profit/Loss Report
Write-Host "`n[Test 7] Testing Get Profit/Loss Report..." -ForegroundColor Yellow
try {
    $profitLossResponse = Invoke-RestMethod -Uri "$baseUrl/api/accounting/profit-loss?year=2024" -Method GET -Headers $headers
    Write-Host "✓ Get profit/loss report successful!" -ForegroundColor Green
    Write-Host "  Period: $($profitLossResponse.data.period)" -ForegroundColor Gray
    Write-Host "  Total Revenue: $($profitLossResponse.data.total_revenue)" -ForegroundColor Gray
    Write-Host "  Total Expenses: $($profitLossResponse.data.total_expenses)" -ForegroundColor Gray
    Write-Host "  Net Profit: $($profitLossResponse.data.net_profit)" -ForegroundColor Gray
} catch {
    Write-Host "✗ Get profit/loss report failed: $_" -ForegroundColor Red
}

# Test 8: Test Protected Route (Dashboard)
Write-Host "`n[Test 8] Testing Protected Route (Dashboard)..." -ForegroundColor Yellow
try {
    $dashboardResponse = Invoke-RestMethod -Uri "$baseUrl/api/dashboard" -Method GET -Headers $headers
    Write-Host "✓ Dashboard access successful!" -ForegroundColor Green
} catch {
    Write-Host "✗ Dashboard access failed: $_" -ForegroundColor Red
}

# Test 9: Test Unauthorized Access
Write-Host "`n[Test 9] Testing Unauthorized Access..." -ForegroundColor Yellow
try {
    $unauthorizedResponse = Invoke-RestMethod -Uri "$baseUrl/api/dashboard" -Method GET
    Write-Host "✗ Unauthorized access should have failed!" -ForegroundColor Red
} catch {
    if ($_.Exception.Response.StatusCode -eq 401) {
        Write-Host "✓ Unauthorized access correctly blocked (401)!" -ForegroundColor Green
    } else {
        Write-Host "! Unexpected error: $_" -ForegroundColor Yellow
    }
}

Write-Host "`n==================================" -ForegroundColor Cyan
Write-Host "Testing Complete!" -ForegroundColor Cyan
Write-Host "==================================" -ForegroundColor Cyan
