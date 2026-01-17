# =============================================================================
# Gaara ERP - Git Push with Token (PowerShell)
# =============================================================================
# Quick push script with token authentication
# =============================================================================

param(
    [Parameter(Mandatory=$true)]
    [string]$Username,

    [Parameter(Mandatory=$true)]
    [string]$Token,

    [string]$RepoName = "gaara-erp",
    [string]$CommitMessage = "",
    [string]$Branch = "main"
)

$ErrorActionPreference = "Stop"

Write-Host "==========================================" -ForegroundColor Cyan
Write-Host "Gaara ERP - Git Push to GitHub" -ForegroundColor Cyan
Write-Host "==========================================" -ForegroundColor Cyan
Write-Host ""

# Navigate to project directory
$projectRoot = "d:\APPS_AI\gaara_erp\Gaara_erp"
if (Test-Path $projectRoot) {
    Set-Location $projectRoot
} else {
    Write-Host "Project directory not found: $projectRoot" -ForegroundColor Red
    exit 1
}

# Initialize Git if needed
if (-not (Test-Path ".git")) {
    Write-Host "Initializing Git repository..." -ForegroundColor Yellow
    git init
    git checkout -b $Branch
    Write-Host "✓ Git repository initialized" -ForegroundColor Green
}

# Set remote URL with token
$remoteUrl = "https://${Token}@github.com/${Username}/${RepoName}.git"
Write-Host "Setting remote URL..." -ForegroundColor Yellow
git remote remove origin 2>$null
git remote add origin $remoteUrl
Write-Host "✓ Remote configured" -ForegroundColor Green
Write-Host ""

# Stage all files
Write-Host "Staging files..." -ForegroundColor Yellow
git add .
Write-Host "✓ Files staged" -ForegroundColor Green
Write-Host ""

# Check for changes
$status = git status --porcelain
if (-not $status) {
    Write-Host "No changes to commit" -ForegroundColor Yellow
    exit 0
}

# Commit
if (-not $CommitMessage) {
    $CommitMessage = "feat: Complete Gaara ERP project setup - $(Get-Date -Format 'yyyy-MM-dd')"
}

Write-Host "Committing changes..." -ForegroundColor Yellow
Write-Host "Message: $CommitMessage" -ForegroundColor Gray
git commit -m $CommitMessage
Write-Host "✓ Changes committed" -ForegroundColor Green
Write-Host ""

# Get current branch
$currentBranch = git branch --show-current
if (-not $currentBranch) {
    $currentBranch = $Branch
    git checkout -b $currentBranch
}

# Push
Write-Host "Pushing to GitHub..." -ForegroundColor Yellow
Write-Host "Repository: https://github.com/${Username}/${RepoName}" -ForegroundColor Cyan
Write-Host "Branch: $currentBranch" -ForegroundColor Cyan
Write-Host ""

try {
    git push -u origin $currentBranch --force
    Write-Host ""
    Write-Host "✓ Successfully pushed to GitHub!" -ForegroundColor Green
    Write-Host ""
    Write-Host "View your repository:" -ForegroundColor Cyan
    Write-Host "https://github.com/${Username}/${RepoName}" -ForegroundColor Blue
} catch {
    Write-Host ""
    Write-Host "Error: $($_.Exception.Message)" -ForegroundColor Red
    Write-Host ""
    Write-Host "Troubleshooting:" -ForegroundColor Yellow
    Write-Host "1. Verify token has 'repo' scope" -ForegroundColor Gray
    Write-Host "2. Check repository exists or create it on GitHub" -ForegroundColor Gray
    Write-Host "3. Try: git push -u origin $currentBranch" -ForegroundColor Gray
    exit 1
}

Write-Host ""
Write-Host "==========================================" -ForegroundColor Cyan
Write-Host "Done!" -ForegroundColor Green
Write-Host "==========================================" -ForegroundColor Cyan
