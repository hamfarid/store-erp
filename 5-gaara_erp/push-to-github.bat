@echo off
REM =============================================================================
REM Gaara ERP - Push to GitHub
REM =============================================================================

echo ==========================================
echo Gaara ERP - Git Push to GitHub
echo ==========================================
echo.

cd /d "%~dp0"

REM Initialize Git if needed
if not exist ".git" (
    echo Initializing Git repository...
    git init
    git checkout -b main
    echo ✓ Git repository initialized
    echo.
)

REM Set remote
echo Setting remote repository...
git remote remove origin 2>nul
git remote add origin https://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N@github.com/hamfarid/gaara-erp.git
echo ✓ Remote configured
echo.

REM Stage files
echo Staging files...
git add .
echo ✓ Files staged
echo.

REM Commit
echo Committing changes...
git commit -m "feat: Complete Gaara ERP project - All modules, Docker, API, tests, and documentation"
echo ✓ Changes committed
echo.

REM Push
echo Pushing to GitHub...
echo Repository: https://github.com/hamfarid/gaara-erp
echo Branch: main
echo.

git push -u origin main --force

if %ERRORLEVEL% EQU 0 (
    echo.
    echo ✓ Successfully pushed to GitHub!
    echo.
    echo View your repository:
    echo https://github.com/hamfarid/gaara-erp
) else (
    echo.
    echo ✗ Error pushing to GitHub
    echo.
    echo Troubleshooting:
    echo 1. Verify token has 'repo' scope
    echo 2. Check repository exists on GitHub
    echo 3. Check network connection
)

echo.
echo ==========================================
echo Done!
echo ==========================================
pause
