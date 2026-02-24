@echo off
REM =============================================================================
REM Store ERP - Complete System Startup Script (Windows)
REM =============================================================================
REM This script starts the complete system:
REM - Docker services (Redis, PostgreSQL, Monitoring)
REM - Backend API (Flask on port 5002)
REM - Frontend (React on port 5502)
REM - Database initialization and migrations
REM
REM Usage: start-all.bat [OPTIONS]
REM Options:
REM   --browser          Open browser automatically
REM   --no-docker        Skip Docker services
REM   --clean            Clean install (remove dependencies)
REM   --backend-only     Start backend only
REM   --frontend-only    Start frontend only
REM   --help             Show this help message
REM =============================================================================

setlocal enabledelayedexpansion

REM Configuration
set "PS_ARGS="
set "SHOW_HELP=false"

REM Parse arguments
:parse_args
if "%~1"=="" goto start
if /i "%~1"=="--browser" (
    set "PS_ARGS=%PS_ARGS% -OpenBrowser"
    shift
    goto parse_args
)
if /i "%~1"=="--no-docker" (
    set "PS_ARGS=%PS_ARGS% -SkipDocker"
    shift
    goto parse_args
)
if /i "%~1"=="--clean" (
    set "PS_ARGS=%PS_ARGS% -Clean"
    shift
    goto parse_args
)
if /i "%~1"=="--backend-only" (
    set "PS_ARGS=%PS_ARGS% -SkipFrontend"
    shift
    goto parse_args
)
if /i "%~1"=="--frontend-only" (
    set "PS_ARGS=%PS_ARGS% -SkipBackend"
    shift
    goto parse_args
)
if /i "%~1"=="--help" (
    set "SHOW_HELP=true"
    goto show_help
)
echo Unknown option: %~1
echo Use --help to see available options
exit /b 1

:show_help
echo.
echo Store ERP - Complete System Startup
echo.
echo Usage: start-all.bat [OPTIONS]
echo.
echo Options:
echo   --browser          Open browser automatically after startup
echo   --no-docker        Skip Docker services startup
echo   --clean            Clean install (remove existing dependencies)
echo   --backend-only     Start backend API only
echo   --frontend-only    Start frontend only
echo   --help             Show this help message
echo.
echo Examples:
echo   start-all.bat                    Start everything
echo   start-all.bat --browser          Start and open browser
echo   start-all.bat --no-docker        Start without Docker
echo   start-all.bat --clean            Clean install and start
echo.
exit /b 0

:start
echo.
echo ╔════════════════════════════════════════════════════════════════╗
echo ║                                                                ║
echo ║              Store ERP - Complete System Startup               ║
echo ║                                                                ║
echo ╚════════════════════════════════════════════════════════════════╝
echo.

REM Detect PowerShell
set "PWSH_CMD="
where pwsh >nul 2>nul
if %ERRORLEVEL% EQU 0 (
    set "PWSH_CMD=pwsh"
    echo [✓] Found PowerShell Core (pwsh)
) else (
    where powershell >nul 2>nul
    if %ERRORLEVEL% EQU 0 (
        set "PWSH_CMD=powershell"
        echo [✓] Found Windows PowerShell
    ) else (
        echo [✗] PowerShell not found!
        echo.
        echo PowerShell is required to run this script.
        echo Please install PowerShell from: https://aka.ms/powershell
        echo.
        pause
        exit /b 1
    )
)

echo.
echo Starting system with PowerShell script...
echo Arguments: %PS_ARGS%
echo.

REM Execute PowerShell startup script
%PWSH_CMD% -ExecutionPolicy Bypass -File "%~dp0start-system.ps1" %PS_ARGS%

REM Check exit code
if %ERRORLEVEL% NEQ 0 (
    echo.
    echo ╔════════════════════════════════════════════════════════════════╗
    echo ║                                                                ║
    echo ║  [✗] System startup failed with error code: %ERRORLEVEL%      ║
    echo ║                                                                ║
    echo ╚════════════════════════════════════════════════════════════════╝
    echo.
    echo Check the logs above for details.
    echo.
    pause
    exit /b %ERRORLEVEL%
)

echo.
echo ╔════════════════════════════════════════════════════════════════╗
echo ║                                                                ║
echo ║  [✓] System startup completed successfully!                   ║
echo ║                                                                ║
echo ╚════════════════════════════════════════════════════════════════╝
echo.
echo The system is now running. Press any key to exit this window.
echo Backend and frontend will continue running in separate windows.
echo.
pause

endlocal
