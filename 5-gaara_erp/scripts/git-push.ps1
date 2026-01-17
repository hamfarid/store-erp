# =============================================================================
# Gaara ERP - Git Push Script (PowerShell)
# =============================================================================
# Script to add, commit, and push changes to GitHub
# =============================================================================

Write-Host "==========================================" -ForegroundColor Cyan
Write-Host "Gaara ERP - Git Push to GitHub" -ForegroundColor Cyan
Write-Host "==========================================" -ForegroundColor Cyan
Write-Host ""

# Check if git is installed
if (-not (Get-Command git -ErrorAction SilentlyContinue)) {
    Write-Host "✗ Git is not installed" -ForegroundColor Red
    exit 1
}

# Check if git is initialized
if (-not (Test-Path .git)) {
    Write-Host "Git repository not initialized." -ForegroundColor Yellow
    Write-Host "Initializing git repository..." -ForegroundColor Yellow
    git init
    Write-Host "✓ Git repository initialized" -ForegroundColor Green
}

# Show current status
Write-Host "Current status:" -ForegroundColor Cyan
git status --short
Write-Host ""

# Check remote
$remote = git remote get-url origin 2>$null
if ($remote) {
    Write-Host "Remote repository: $remote" -ForegroundColor Green
} else {
    Write-Host "No remote repository configured." -ForegroundColor Yellow
    $githubUrl = Read-Host "Enter GitHub repository URL (or press Enter to skip)"
    if ($githubUrl) {
        git remote add origin $githubUrl
        Write-Host "✓ Remote added" -ForegroundColor Green
    }
}

# Stage all files
Write-Host ""
Write-Host "Staging all files..." -ForegroundColor Cyan
git add .
Write-Host "✓ Files staged" -ForegroundColor Green

# Get commit message
Write-Host ""
$commitMsg = Read-Host "Enter commit message (or press Enter for default)"
if ([string]::IsNullOrWhiteSpace($commitMsg)) {
    $commitMsg = "feat: Add comprehensive backend infrastructure, Docker setup, API documentation, and configuration modules"
}

# Commit
Write-Host ""
Write-Host "Committing changes..." -ForegroundColor Cyan
git commit -m $commitMsg
Write-Host "✓ Changes committed" -ForegroundColor Green

# Get current branch
$branch = git branch --show-current
if ([string]::IsNullOrWhiteSpace($branch)) {
    $branch = "main"
}

# Push
Write-Host ""
$push = Read-Host "Push to GitHub? (y/n)"
if ($push -eq "y" -or $push -eq "Y") {
    Write-Host "Pushing to origin/$branch..." -ForegroundColor Cyan
    try {
        git push -u origin $branch
        Write-Host "✓ Successfully pushed to GitHub" -ForegroundColor Green
    } catch {
        Write-Host "⚠ Push failed. Trying alternative..." -ForegroundColor Yellow
        git push -u origin main 2>$null
        git push -u origin master 2>$null
    }
} else {
    Write-Host "Skipping push. Run 'git push' manually when ready." -ForegroundColor Yellow
}

Write-Host ""
Write-Host "==========================================" -ForegroundColor Cyan
Write-Host "Done!" -ForegroundColor Green
Write-Host "==========================================" -ForegroundColor Cyan
