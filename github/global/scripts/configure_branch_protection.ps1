# Configure Branch Protection for Store ERP Repository
# Based on docs/github/BRANCH_PROTECTION.md

param(
    [string]$GitHubToken = $env:GITHUB_TOKEN
)

# Configuration
$RepoOwner = "hamfarid"
$RepoName = "Store"

# Check if GitHub token is set
if ([string]::IsNullOrEmpty($GitHubToken)) {
    Write-Host "Error: GITHUB_TOKEN environment variable is not set" -ForegroundColor Red
    Write-Host "Please set it with: `$env:GITHUB_TOKEN = 'your_token_here'" -ForegroundColor Yellow
    exit 1
}

Write-Host "Configuring branch protection for $RepoOwner/$RepoName" -ForegroundColor Green
Write-Host ""

# Function to configure branch protection
function Configure-BranchProtection {
    param(
        [string]$Branch,
        [hashtable]$Config
    )
    
    Write-Host "Configuring protection for branch: $Branch" -ForegroundColor Yellow
    
    $uri = "https://api.github.com/repos/$RepoOwner/$RepoName/branches/$Branch/protection"
    $headers = @{
        "Accept" = "application/vnd.github+json"
        "Authorization" = "Bearer $GitHubToken"
        "X-GitHub-Api-Version" = "2022-11-28"
    }
    
    $body = $Config | ConvertTo-Json -Depth 10
    
    try {
        $response = Invoke-RestMethod -Uri $uri -Method Put -Headers $headers -Body $body -ContentType "application/json"
        Write-Host "✅ Branch protection configured for $Branch" -ForegroundColor Green
    }
    catch {
        Write-Host "❌ Failed to configure branch protection for $Branch" -ForegroundColor Red
        Write-Host "Error: $($_.Exception.Message)" -ForegroundColor Red
    }
    
    Write-Host ""
}

# Main branch protection configuration
$mainBranchConfig = @{
    required_status_checks = @{
        strict = $true
        contexts = @(
            "backend-tests / test",
            "pr-quality-gate / pr-quality-gate"
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

# Development branch protection configuration
$developmentBranchConfig = @{
    required_status_checks = @{
        strict = $false
        contexts = @(
            "backend-tests / test"
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

# Configure main branch
Write-Host "=== Configuring Main Branch ===" -ForegroundColor Green
Configure-BranchProtection -Branch "main" -Config $mainBranchConfig

# Configure development branch (if exists)
Write-Host "=== Configuring Development Branch ===" -ForegroundColor Green
try {
    $branches = Invoke-RestMethod -Uri "https://api.github.com/repos/$RepoOwner/$RepoName/branches" -Headers @{
        "Accept" = "application/vnd.github+json"
        "Authorization" = "Bearer $GitHubToken"
    }
    
    if ($branches | Where-Object { $_.name -eq "development" }) {
        Configure-BranchProtection -Branch "development" -Config $developmentBranchConfig
    }
    else {
        Write-Host "⚠️  Development branch does not exist, skipping" -ForegroundColor Yellow
        Write-Host ""
    }
}
catch {
    Write-Host "⚠️  Could not check for development branch, skipping" -ForegroundColor Yellow
    Write-Host ""
}

Write-Host "=== Branch Protection Configuration Complete ===" -ForegroundColor Green
Write-Host ""
Write-Host "To verify the configuration:"
Write-Host "  1. Go to: https://github.com/$RepoOwner/$RepoName/settings/branches"
Write-Host "  2. Check the protection rules for each branch"
Write-Host ""
Write-Host "Or use GitHub CLI:"
Write-Host "  gh api repos/$RepoOwner/$RepoName/branches/main/protection"

