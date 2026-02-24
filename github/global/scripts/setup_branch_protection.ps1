# Setup Branch Protection - Interactive Script
# This script guides you through configuring branch protection

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  Branch Protection Setup" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Check if GITHUB_TOKEN is set
if (-not $env:GITHUB_TOKEN) {
    Write-Host "❌ GITHUB_TOKEN not found!" -ForegroundColor Red
    Write-Host ""
    Write-Host "To configure branch protection, you need a GitHub Personal Access Token." -ForegroundColor Yellow
    Write-Host ""
    Write-Host "Steps to create a token:" -ForegroundColor Cyan
    Write-Host "1. Go to: https://github.com/settings/tokens" -ForegroundColor White
    Write-Host "2. Click 'Generate new token' → 'Generate new token (classic)'" -ForegroundColor White
    Write-Host "3. Give it a name: 'Store Branch Protection'" -ForegroundColor White
    Write-Host "4. Select scopes: ✅ repo (all)" -ForegroundColor White
    Write-Host "5. Click 'Generate token'" -ForegroundColor White
    Write-Host "6. Copy the token (you won't see it again!)" -ForegroundColor White
    Write-Host ""
    Write-Host "Then run:" -ForegroundColor Cyan
    Write-Host '  $env:GITHUB_TOKEN = "your_token_here"' -ForegroundColor Green
    Write-Host '  .\scripts\setup_branch_protection.ps1' -ForegroundColor Green
    Write-Host ""
    exit 1
}

Write-Host "✅ GITHUB_TOKEN found!" -ForegroundColor Green
Write-Host ""

# Repository details
$owner = "hamfarid"
$repo = "Store"
$token = $env:GITHUB_TOKEN

Write-Host "Repository: $owner/$repo" -ForegroundColor Cyan
Write-Host ""

# Test GitHub API access
Write-Host "Testing GitHub API access..." -ForegroundColor Yellow
try {
    $headers = @{
        "Authorization" = "Bearer $token"
        "Accept" = "application/vnd.github+json"
        "X-GitHub-Api-Version" = "2022-11-28"
    }
    
    $testUrl = "https://api.github.com/repos/$owner/$repo"
    $response = Invoke-RestMethod -Uri $testUrl -Headers $headers -Method Get
    Write-Host "✅ API access successful!" -ForegroundColor Green
    Write-Host "   Repository: $($response.full_name)" -ForegroundColor White
    Write-Host "   Default branch: $($response.default_branch)" -ForegroundColor White
    Write-Host ""
} catch {
    Write-Host "❌ API access failed!" -ForegroundColor Red
    Write-Host "   Error: $($_.Exception.Message)" -ForegroundColor Red
    Write-Host ""
    Write-Host "Please check:" -ForegroundColor Yellow
    Write-Host "  1. Token is valid" -ForegroundColor White
    Write-Host "  2. Token has 'repo' scope" -ForegroundColor White
    Write-Host "  3. You have admin access to the repository" -ForegroundColor White
    Write-Host ""
    exit 1
}

# Configure main branch protection
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  Configuring Main Branch Protection" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

$mainBranchConfig = @{
    required_status_checks = @{
        strict = $true
        contexts = @(
            "Python tests and quality gates"
            "pr-quality-gate"
        )
    }
    enforce_admins = $true
    required_pull_request_reviews = @{
        dismiss_stale_reviews = $true
        require_code_owner_reviews = $false
        required_approving_review_count = 1
        require_last_push_approval = $false
    }
    restrictions = $null
    allow_force_pushes = $false
    allow_deletions = $false
    block_creations = $false
    required_conversation_resolution = $true
    lock_branch = $false
    allow_fork_syncing = $false
}

Write-Host "Configuration for 'main' branch:" -ForegroundColor Yellow
Write-Host "  ✅ Required status checks: Python tests, PR quality gate" -ForegroundColor White
Write-Host "  ✅ Required reviews: 1" -ForegroundColor White
Write-Host "  ✅ Enforce for admins: Yes" -ForegroundColor White
Write-Host "  ✅ Force push: Disabled" -ForegroundColor White
Write-Host "  ✅ Deletions: Disabled" -ForegroundColor White
Write-Host "  ✅ Conversation resolution: Required" -ForegroundColor White
Write-Host ""

Write-Host "Applying configuration..." -ForegroundColor Yellow

try {
    $url = "https://api.github.com/repos/$owner/$repo/branches/main/protection"
    $body = $mainBranchConfig | ConvertTo-Json -Depth 10
    
    $response = Invoke-RestMethod -Uri $url -Headers $headers -Method Put -Body $body -ContentType "application/json"
    
    Write-Host "✅ Main branch protection configured successfully!" -ForegroundColor Green
    Write-Host ""
} catch {
    Write-Host "❌ Failed to configure main branch protection!" -ForegroundColor Red
    Write-Host "   Error: $($_.Exception.Message)" -ForegroundColor Red
    Write-Host ""
    
    # Check if it's a 404 (branch doesn't exist)
    if ($_.Exception.Response.StatusCode -eq 404) {
        Write-Host "   The 'main' branch might not exist yet." -ForegroundColor Yellow
        Write-Host "   Please create the branch first or check the branch name." -ForegroundColor Yellow
    }
    Write-Host ""
}

# Check if development branch exists
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  Checking Development Branch" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

try {
    $devUrl = "https://api.github.com/repos/$owner/$repo/branches/development"
    $devResponse = Invoke-RestMethod -Uri $devUrl -Headers $headers -Method Get
    
    Write-Host "✅ Development branch found!" -ForegroundColor Green
    Write-Host ""
    
    # Configure development branch protection
    Write-Host "Configuring development branch protection..." -ForegroundColor Yellow
    
    $devBranchConfig = @{
        required_status_checks = @{
            strict = $false
            contexts = @(
                "Python tests and quality gates"
            )
        }
        enforce_admins = $false
        required_pull_request_reviews = @{
            dismiss_stale_reviews = $false
            require_code_owner_reviews = $false
            required_approving_review_count = 1
            require_last_push_approval = $false
        }
        restrictions = $null
        allow_force_pushes = $false
        allow_deletions = $false
        block_creations = $false
        required_conversation_resolution = $false
        lock_branch = $false
        allow_fork_syncing = $false
    }
    
    $devProtectionUrl = "https://api.github.com/repos/$owner/$repo/branches/development/protection"
    $devBody = $devBranchConfig | ConvertTo-Json -Depth 10
    
    $devProtectionResponse = Invoke-RestMethod -Uri $devProtectionUrl -Headers $headers -Method Put -Body $devBody -ContentType "application/json"
    
    Write-Host "✅ Development branch protection configured successfully!" -ForegroundColor Green
    Write-Host ""
} catch {
    if ($_.Exception.Response.StatusCode -eq 404) {
        Write-Host "ℹ️  Development branch not found (this is OK)" -ForegroundColor Cyan
        Write-Host "   You can create it later if needed." -ForegroundColor White
        Write-Host ""
    } else {
        Write-Host "⚠️  Could not configure development branch" -ForegroundColor Yellow
        Write-Host "   Error: $($_.Exception.Message)" -ForegroundColor Yellow
        Write-Host ""
    }
}

# Summary
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  Summary" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Branch protection configuration complete!" -ForegroundColor Green
Write-Host ""
Write-Host "Next steps:" -ForegroundColor Cyan
Write-Host "  1. Verify configuration at:" -ForegroundColor White
Write-Host "     https://github.com/$owner/$repo/settings/branches" -ForegroundColor Green
Write-Host ""
Write-Host "  2. Test with PR #26:" -ForegroundColor White
Write-Host "     https://github.com/$owner/$repo/pull/26" -ForegroundColor Green
Write-Host ""
Write-Host "  3. Try to merge without approvals (should be blocked)" -ForegroundColor White
Write-Host ""
Write-Host "Done! 🎉" -ForegroundColor Green
Write-Host ""

