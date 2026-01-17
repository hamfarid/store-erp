# =============================================================================
# Gaara ERP - Secure Git Push Script (PowerShell)
# =============================================================================
# Securely pushes files to GitHub using Personal Access Token
# =============================================================================

param(
    [string]$CommitMessage = "",
    [string]$Branch = "main"
)

$ErrorActionPreference = "Stop"

Write-Host "==========================================" -ForegroundColor Cyan
Write-Host "Gaara ERP - Git Push to GitHub" -ForegroundColor Cyan
Write-Host "==========================================" -ForegroundColor Cyan
Write-Host ""

# Check if git is initialized
if (-not (Test-Path ".git")) {
    Write-Host "Initializing Git repository..." -ForegroundColor Yellow
    git init
    Write-Host "✓ Git repository initialized" -ForegroundColor Green
}

# Get current branch
$currentBranch = git branch --show-current
if (-not $currentBranch) {
    $currentBranch = $Branch
    git checkout -b $currentBranch
}

Write-Host "Current branch: $currentBranch" -ForegroundColor Cyan
Write-Host ""

# Check for remote
$remoteUrl = git remote get-url origin 2>$null
if (-not $remoteUrl) {
    Write-Host "No remote repository found." -ForegroundColor Yellow
    Write-Host ""
    Write-Host "Please provide your GitHub repository URL:" -ForegroundColor Yellow
    Write-Host "Example: https://github.com/hamfarid/gaara-erp.git" -ForegroundColor Gray
    $repoUrl = Read-Host "Repository URL"

    if ($repoUrl) {
        # Extract username and repo name
        if ($repoUrl -match "github\.com[:/]([^/]+)/([^/]+)\.git?$") {
            $username = $Matches[1]
            $repoName = $Matches[2] -replace '\.git$', ''

            # Use token in URL
            Write-Host ""
            Write-Host "Adding remote with authentication..." -ForegroundColor Yellow
            $token = Read-Host "Enter your GitHub Personal Access Token" -AsSecureString
            $BSTR = [System.Runtime.InteropServices.Marshal]::SecureStringToBSTR($token)
            $plainToken = [System.Runtime.InteropServices.Marshal]::PtrToStringAuto($BSTR)

            $authenticatedUrl = "https://$plainToken@github.com/$username/$repoName.git"
            git remote add origin $authenticatedUrl
            Write-Host "✓ Remote added" -ForegroundColor Green
        } else {
            Write-Host "Invalid repository URL format" -ForegroundColor Red
            exit 1
        }
    } else {
        Write-Host "Repository URL is required" -ForegroundColor Red
        exit 1
    }
} else {
    Write-Host "Remote repository: $remoteUrl" -ForegroundColor Cyan
}

Write-Host ""

# Stage all files
Write-Host "Staging files..." -ForegroundColor Yellow
git add .
Write-Host "✓ Files staged" -ForegroundColor Green
Write-Host ""

# Check if there are changes
$status = git status --porcelain
if (-not $status) {
    Write-Host "No changes to commit" -ForegroundColor Yellow
    exit 0
}

# Commit message
if (-not $CommitMessage) {
    Write-Host "Enter commit message:" -ForegroundColor Yellow
    Write-Host "Press Enter to use default message" -ForegroundColor Gray
    $CommitMessage = Read-Host "Commit message"

    if (-not $CommitMessage) {
        $CommitMessage = "feat: Update Gaara ERP project - $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')"
    }
}

Write-Host ""
Write-Host "Committing changes..." -ForegroundColor Yellow
git commit -m $CommitMessage
Write-Host "✓ Changes committed" -ForegroundColor Green
Write-Host ""

# Push to GitHub
Write-Host "Pushing to GitHub..." -ForegroundColor Yellow
try {
    git push -u origin $currentBranch
    Write-Host ""
    Write-Host "✓ Successfully pushed to GitHub!" -ForegroundColor Green
    Write-Host ""
    Write-Host "Repository: $remoteUrl" -ForegroundColor Cyan
    Write-Host "Branch: $currentBranch" -ForegroundColor Cyan
} catch {
    Write-Host ""
    Write-Host "Error pushing to GitHub:" -ForegroundColor Red
    Write-Host $_.Exception.Message -ForegroundColor Red
    Write-Host ""
    Write-Host "Troubleshooting:" -ForegroundColor Yellow
    Write-Host "1. Check your Personal Access Token" -ForegroundColor Gray
    Write-Host "2. Verify repository URL" -ForegroundColor Gray
    Write-Host "3. Check network connection" -ForegroundColor Gray
    exit 1
}

Write-Host ""
Write-Host "==========================================" -ForegroundColor Cyan
Write-Host "Done!" -ForegroundColor Green
Write-Host "==========================================" -ForegroundColor Cyan
