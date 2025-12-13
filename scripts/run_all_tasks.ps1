# Run All Tasks - Master Script
# Executes all tasks in order: 1 → 2 → 3 → 4

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  Master Task Execution Script" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "This script will execute all tasks in order:" -ForegroundColor Yellow
Write-Host "  1. Configure branch protection" -ForegroundColor White
Write-Host "  2. Start T21 implementation (Vault setup)" -ForegroundColor White
Write-Host "  3. Review PR #26" -ForegroundColor White
Write-Host "  4. Install K6" -ForegroundColor White
Write-Host ""

$continue = Read-Host "Do you want to continue? (y/n)"
if ($continue -ne "y") {
    Write-Host "Cancelled." -ForegroundColor Yellow
    exit 0
}

Write-Host ""

# Task 1: Configure Branch Protection
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  Task 1: Configure Branch Protection" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

if (-not $env:GITHUB_TOKEN) {
    Write-Host "⚠️  GITHUB_TOKEN not set!" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "To configure branch protection, you need a GitHub token." -ForegroundColor White
    Write-Host "Would you like to:" -ForegroundColor Yellow
    Write-Host "  1. Set token now and continue" -ForegroundColor White
    Write-Host "  2. Skip branch protection for now" -ForegroundColor White
    Write-Host ""
    
    $choice = Read-Host "Enter choice (1-2)"
    
    if ($choice -eq "1") {
        Write-Host ""
        $token = Read-Host "Enter your GitHub token" -AsSecureString
        $env:GITHUB_TOKEN = [Runtime.InteropServices.Marshal]::PtrToStringAuto([Runtime.InteropServices.Marshal]::SecureStringToBSTR($token))
        Write-Host "✅ Token set!" -ForegroundColor Green
        Write-Host ""
    } else {
        Write-Host "⏭️  Skipping branch protection" -ForegroundColor Cyan
        Write-Host ""
        Write-Host "You can run it later with:" -ForegroundColor Yellow
        Write-Host "  .\scripts\setup_branch_protection.ps1" -ForegroundColor Green
        Write-Host ""
        Start-Sleep -Seconds 2
        goto Task2
    }
}

Write-Host "Running branch protection setup..." -ForegroundColor Yellow
Write-Host ""
& .\scripts\setup_branch_protection.ps1

Write-Host ""
Write-Host "Press any key to continue to Task 2..." -ForegroundColor Cyan
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
Write-Host ""

# Task 2: Start T21 Implementation
:Task2
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  Task 2: Start T21 Implementation" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

Write-Host "This will set up HashiCorp Vault for secret management." -ForegroundColor Yellow
Write-Host ""
$runVault = Read-Host "Do you want to set up Vault now? (y/n)"

if ($runVault -eq "y") {
    Write-Host ""
    Write-Host "Running Vault setup..." -ForegroundColor Yellow
    Write-Host ""
    & .\scripts\setup_vault.ps1
} else {
    Write-Host "⏭️  Skipping Vault setup" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "You can run it later with:" -ForegroundColor Yellow
    Write-Host "  .\scripts\setup_vault.ps1" -ForegroundColor Green
    Write-Host ""
}

Write-Host ""
Write-Host "Press any key to continue to Task 3..." -ForegroundColor Cyan
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
Write-Host ""

# Task 3: Review PR #26
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  Task 3: Review PR #26" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

Write-Host "Running PR review..." -ForegroundColor Yellow
Write-Host ""
& .\scripts\review_pr26.ps1

Write-Host ""
Write-Host "Press any key to continue to Task 4..." -ForegroundColor Cyan
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
Write-Host ""

# Task 4: Install K6
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  Task 4: Install K6" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

Write-Host "This will install K6 performance testing tool." -ForegroundColor Yellow
Write-Host ""
$installK6 = Read-Host "Do you want to install K6 now? (y/n)"

if ($installK6 -eq "y") {
    Write-Host ""
    Write-Host "Running K6 installation..." -ForegroundColor Yellow
    Write-Host ""
    & .\scripts\install_k6.ps1
} else {
    Write-Host "⏭️  Skipping K6 installation" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "You can run it later with:" -ForegroundColor Yellow
    Write-Host "  .\scripts\install_k6.ps1" -ForegroundColor Green
    Write-Host ""
}

# Summary
Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  All Tasks Complete!" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

Write-Host "Summary:" -ForegroundColor Green
Write-Host "  ✅ Task 1: Branch protection" -ForegroundColor White
Write-Host "  ✅ Task 2: Vault setup" -ForegroundColor White
Write-Host "  ✅ Task 3: PR review" -ForegroundColor White
Write-Host "  ✅ Task 4: K6 installation" -ForegroundColor White
Write-Host ""

Write-Host "Next Steps:" -ForegroundColor Cyan
Write-Host "  1. Verify branch protection in GitHub" -ForegroundColor White
Write-Host "  2. Test Vault access" -ForegroundColor White
Write-Host "  3. Review PR #26 workflow logs" -ForegroundColor White
Write-Host "  4. Run K6 performance tests" -ForegroundColor White
Write-Host ""

Write-Host "Documentation:" -ForegroundColor Cyan
Write-Host "  - docs/github/BRANCH_PROTECTION.md" -ForegroundColor White
Write-Host "  - docs/security/T21_KMS_VAULT_PLAN.md" -ForegroundColor White
Write-Host "  - docs/github/CI_CD_TESTING_RESULTS.md" -ForegroundColor White
Write-Host "  - docs/performance/K6_TESTING.md" -ForegroundColor White
Write-Host "  - docs/PROGRESS_SUMMARY.md" -ForegroundColor White
Write-Host ""

Write-Host "Done! 🎉" -ForegroundColor Green
Write-Host ""

