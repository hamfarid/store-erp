@echo off
REM =============================================================================
REM Store ERP - System Startup Wrapper (Batch to PowerShell)
REM =============================================================================
REM This batch file launches the PowerShell startup script with proper execution
REM policy settings.
REM =============================================================================

echo.
echo ========================================
echo Store ERP - System Startup
echo ========================================
echo.

REM Check if PowerShell is available
where pwsh >nul 2>nul
if %ERRORLEVEL% EQU 0 (
    echo Using PowerShell Core (pwsh)
    pwsh -ExecutionPolicy Bypass -File "%~dp0start-system.ps1" %*
) else (
    where powershell >nul 2>nul
    if %ERRORLEVEL% EQU 0 (
        echo Using Windows PowerShell
        powershell -ExecutionPolicy Bypass -File "%~dp0start-system.ps1" %*
    ) else (
        echo [ERROR] PowerShell is not installed
        echo Please install PowerShell to use this script
        pause
        exit /b 1
    )
)

if %ERRORLEVEL% NEQ 0 (
    echo.
    echo [ERROR] Startup script failed with exit code %ERRORLEVEL%
    pause
)
