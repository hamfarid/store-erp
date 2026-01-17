@echo off
REM =============================================================================
REM Gaara ERP - Push to GitHub (Windows Batch)
REM =============================================================================

echo ==========================================
echo Gaara ERP - Push to GitHub
echo ==========================================
echo.

REM Check if git is installed
git --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Git is not installed!
    pause
    exit /b 1
)

REM Check if git is initialized
if not exist .git (
    echo [INFO] Initializing git repository...
    git init
    echo [OK] Git repository initialized
    echo.
)

REM Show status
echo Current git status:
git status --short
echo.

REM Stage all files
echo [INFO] Staging all files...
git add .
echo [OK] Files staged
echo.

REM Get commit message
set /p COMMIT_MSG="Enter commit message (or press Enter for default): "
if "%COMMIT_MSG%"=="" (
    set COMMIT_MSG=feat: Add comprehensive backend infrastructure, Docker setup, API documentation, and configuration modules
)

REM Commit
echo [INFO] Committing changes...
git commit -m "%COMMIT_MSG%"
if errorlevel 1 (
    echo [WARNING] Nothing to commit or commit failed
) else (
    echo [OK] Changes committed
)
echo.

REM Check remote
git remote get-url origin >nul 2>&1
if errorlevel 1 (
    echo [INFO] No remote repository configured.
    set /p GITHUB_URL="Enter GitHub repository URL: "
    if not "%GITHUB_URL%"=="" (
        git remote add origin "%GITHUB_URL%"
        echo [OK] Remote added
    )
)

REM Get current branch
for /f "tokens=*" %%i in ('git branch --show-current 2^>nul') do set BRANCH=%%i
if "%BRANCH%"=="" set BRANCH=main

REM Ask to push
set /p PUSH="Push to GitHub? (y/n): "
if /i "%PUSH%"=="y" (
    echo [INFO] Pushing to origin/%BRANCH%...
    git push -u origin %BRANCH%
    if errorlevel 1 (
        echo [INFO] Trying main branch...
        git push -u origin main
        if errorlevel 1 (
            echo [INFO] Trying master branch...
            git push -u origin master
        )
    )
    echo [OK] Pushed to GitHub
)

echo.
echo ==========================================
echo Done!
echo ==========================================
pause
