@echo off
title Starting Docker Desktop
color 0A

echo ================================================================
echo                Starting Docker Desktop                         
echo ================================================================
echo.

echo Checking if Docker is installed...
docker --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Docker is not installed
    echo Please install Docker Desktop from: https://www.docker.com/products/docker-desktop
    echo.
    echo After installation, run this script again.
    pause
    exit /b 1
)

echo SUCCESS: Docker is installed
echo.

echo Checking if Docker is running...
docker ps >nul 2>&1
if %errorlevel% equ 0 (
    echo SUCCESS: Docker is already running
    goto docker_ready
)

echo Docker is not running. Starting Docker Desktop...
echo.

REM Try different common paths for Docker Desktop
set DOCKER_PATH=""
if exist "C:\Program Files\Docker\Docker\Docker Desktop.exe" (
    set DOCKER_PATH="C:\Program Files\Docker\Docker\Docker Desktop.exe"
) else if exist "%USERPROFILE%\AppData\Local\Docker\Docker Desktop.exe" (
    set DOCKER_PATH="%USERPROFILE%\AppData\Local\Docker\Docker Desktop.exe"
) else if exist "C:\Users\%USERNAME%\AppData\Local\Docker\Docker Desktop.exe" (
    set DOCKER_PATH="C:\Users\%USERNAME%\AppData\Local\Docker\Docker Desktop.exe"
)

if %DOCKER_PATH%=="" (
    echo ERROR: Could not find Docker Desktop executable
    echo Please start Docker Desktop manually and then run the deployment script
    pause
    exit /b 1
)

echo Starting Docker Desktop from: %DOCKER_PATH%
start "" %DOCKER_PATH%

echo.
echo Waiting for Docker to start...
echo This may take 1-3 minutes depending on your system...
echo.

REM Wait for Docker to be ready
set /a counter=0
:wait_loop
timeout /t 15 /nobreak >nul
docker ps >nul 2>&1
if %errorlevel% equ 0 goto docker_ready

set /a counter+=1
echo Still waiting... (%counter%/12) - Please wait while Docker starts
if %counter% lss 12 goto wait_loop

echo.
echo WARNING: Docker is taking longer than expected to start
echo Please check Docker Desktop manually and ensure it's running
echo Then run the deployment script again
pause
exit /b 1

:docker_ready
echo.
echo ================================================================
echo                   DOCKER IS READY!                            
echo ================================================================
echo.

echo Creating Docker network...
docker network create agri_ai_network 2>nul
if %errorlevel% equ 0 (
    echo SUCCESS: Network created
) else (
    echo INFO: Network already exists or created successfully
)

echo.
echo Docker is now ready for container deployment!
echo.
echo Next steps:
echo 1. Run: start_simple.cmd (for quick start)
echo 2. Run: START_CONTAINERS.cmd (for full menu)
echo 3. Run: deploy_staged.cmd (for staged deployment)
echo.
pause
