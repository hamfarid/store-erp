# Review PR #26 Workflow Logs
# This script helps review the CI/CD workflow results

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  PR #26 Workflow Review" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

$owner = "hamfarid"
$repo = "Store"
$prNumber = 26

Write-Host "Repository: $owner/$repo" -ForegroundColor Cyan
Write-Host "PR: #$prNumber" -ForegroundColor Cyan
Write-Host ""

# PR URL
$prUrl = "https://github.com/$owner/$repo/pull/$prNumber"
Write-Host "PR URL: $prUrl" -ForegroundColor White
Write-Host ""

# Check if GITHUB_TOKEN is set
if ($env:GITHUB_TOKEN) {
    Write-Host "✅ GITHUB_TOKEN found - will fetch detailed information" -ForegroundColor Green
    Write-Host ""
    
    $headers = @{
        "Authorization" = "Bearer $env:GITHUB_TOKEN"
        "Accept" = "application/vnd.github+json"
        "X-GitHub-Api-Version" = "2022-11-28"
    }
    
    # Get PR details
    Write-Host "Fetching PR details..." -ForegroundColor Yellow
    try {
        $prApiUrl = "https://api.github.com/repos/$owner/$repo/pulls/$prNumber"
        $pr = Invoke-RestMethod -Uri $prApiUrl -Headers $headers -Method Get
        
        Write-Host "✅ PR Details:" -ForegroundColor Green
        Write-Host "   Title: $($pr.title)" -ForegroundColor White
        Write-Host "   State: $($pr.state)" -ForegroundColor White
        Write-Host "   Created: $($pr.created_at)" -ForegroundColor White
        Write-Host "   Updated: $($pr.updated_at)" -ForegroundColor White
        Write-Host "   Additions: $($pr.additions)" -ForegroundColor Green
        Write-Host "   Deletions: $($pr.deletions)" -ForegroundColor Red
        Write-Host "   Changed files: $($pr.changed_files)" -ForegroundColor White
        Write-Host ""
        
        # Get check runs
        Write-Host "Fetching check runs..." -ForegroundColor Yellow
        $checkRunsUrl = "https://api.github.com/repos/$owner/$repo/commits/$($pr.head.sha)/check-runs"
        $checkRuns = Invoke-RestMethod -Uri $checkRunsUrl -Headers $headers -Method Get
        
        Write-Host "✅ Check Runs ($($checkRuns.total_count)):" -ForegroundColor Green
        Write-Host ""
        
        foreach ($check in $checkRuns.check_runs) {
            $statusIcon = switch ($check.conclusion) {
                "success" { "✅" }
                "failure" { "❌" }
                "cancelled" { "⚠️" }
                "skipped" { "⏭️" }
                default { "⏳" }
            }
            
            $statusColor = switch ($check.conclusion) {
                "success" { "Green" }
                "failure" { "Red" }
                "cancelled" { "Yellow" }
                "skipped" { "Cyan" }
                default { "White" }
            }
            
            Write-Host "$statusIcon $($check.name)" -ForegroundColor $statusColor
            Write-Host "   Status: $($check.status)" -ForegroundColor White
            Write-Host "   Conclusion: $($check.conclusion)" -ForegroundColor $statusColor
            Write-Host "   Started: $($check.started_at)" -ForegroundColor White
            Write-Host "   Completed: $($check.completed_at)" -ForegroundColor White
            
            if ($check.output.annotations_count -gt 0) {
                Write-Host "   Annotations: $($check.output.annotations_count)" -ForegroundColor Yellow
            }
            
            Write-Host "   URL: $($check.html_url)" -ForegroundColor Cyan
            Write-Host ""
        }
        
        # Summary
        $successCount = ($checkRuns.check_runs | Where-Object { $_.conclusion -eq "success" }).Count
        $failureCount = ($checkRuns.check_runs | Where-Object { $_.conclusion -eq "failure" }).Count
        $otherCount = $checkRuns.total_count - $successCount - $failureCount
        
        Write-Host "========================================" -ForegroundColor Cyan
        Write-Host "  Summary" -ForegroundColor Cyan
        Write-Host "========================================" -ForegroundColor Cyan
        Write-Host ""
        Write-Host "Total Checks: $($checkRuns.total_count)" -ForegroundColor White
        Write-Host "✅ Success: $successCount" -ForegroundColor Green
        Write-Host "❌ Failure: $failureCount" -ForegroundColor Red
        Write-Host "⏳ Other: $otherCount" -ForegroundColor Yellow
        Write-Host ""
        
        if ($failureCount -gt 0) {
            Write-Host "Failed Checks:" -ForegroundColor Red
            foreach ($check in ($checkRuns.check_runs | Where-Object { $_.conclusion -eq "failure" })) {
                Write-Host "  ❌ $($check.name)" -ForegroundColor Red
                Write-Host "     View logs: $($check.html_url)" -ForegroundColor Cyan
            }
            Write-Host ""
        }
        
    } catch {
        Write-Host "❌ Failed to fetch PR details!" -ForegroundColor Red
        Write-Host "   Error: $($_.Exception.Message)" -ForegroundColor Red
        Write-Host ""
    }
    
} else {
    Write-Host "ℹ️  GITHUB_TOKEN not set - showing basic information only" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "To get detailed information, set GITHUB_TOKEN:" -ForegroundColor Yellow
    Write-Host '  $env:GITHUB_TOKEN = "your_token_here"' -ForegroundColor Green
    Write-Host '  .\scripts\review_pr26.ps1' -ForegroundColor Green
    Write-Host ""
}

# Quick links
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  Quick Links" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "PR Page:" -ForegroundColor Cyan
Write-Host "  $prUrl" -ForegroundColor Green
Write-Host ""
Write-Host "Workflow Runs:" -ForegroundColor Cyan
Write-Host "  https://github.com/$owner/$repo/actions" -ForegroundColor Green
Write-Host ""
Write-Host "Files Changed:" -ForegroundColor Cyan
Write-Host "  $prUrl/files" -ForegroundColor Green
Write-Host ""
Write-Host "Checks:" -ForegroundColor Cyan
Write-Host "  $prUrl/checks" -ForegroundColor Green
Write-Host ""

# Recommendations
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  Recommendations" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "1. Review failed checks:" -ForegroundColor White
Write-Host "   - Click on each failed check" -ForegroundColor White
Write-Host "   - Read the error messages" -ForegroundColor White
Write-Host "   - Fix issues in the code" -ForegroundColor White
Write-Host ""
Write-Host "2. Common issues to check:" -ForegroundColor White
Write-Host "   - Missing dependencies" -ForegroundColor White
Write-Host "   - Import errors" -ForegroundColor White
Write-Host "   - Test failures" -ForegroundColor White
Write-Host "   - Linting issues" -ForegroundColor White
Write-Host ""
Write-Host "3. After fixing:" -ForegroundColor White
Write-Host "   - Commit and push changes" -ForegroundColor White
Write-Host "   - Workflows will re-run automatically" -ForegroundColor White
Write-Host "   - Review results again" -ForegroundColor White
Write-Host ""

Write-Host "Done! 🎉" -ForegroundColor Green
Write-Host ""

