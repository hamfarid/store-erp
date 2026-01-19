@echo off
title Smart Agricultural System - Quick Start
color 0A

echo ================================================================
echo                Smart Agricultural System
echo                      Quick Start
echo ================================================================
echo.

echo Checking Docker...
docker --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Docker is not installed
    echo Please install Docker Desktop first
    pause
    exit /b 1
)

docker ps >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Docker is not running
    echo Please start Docker Desktop and try again
    pause
    exit /b 1
)

echo SUCCESS: Docker is ready
echo.

echo Creating required directories...
if not exist "logs" mkdir logs
if not exist "uploads" mkdir uploads
if not exist "backups" mkdir backups
if not exist "data" mkdir data
if not exist "media" mkdir media
if not exist "static" mkdir static
if not exist "models" mkdir models
echo SUCCESS: Directories created
echo.

echo Creating network...
docker network create agri_ai_network 2>nul
echo.

echo Starting Stage 1: Databases...
docker-compose -f docker-compose.stage1-databases.yml up -d
if %errorlevel% neq 0 (
    echo ERROR: Failed to start databases
    pause
    exit /b 1
)

echo Waiting for databases to be ready...
timeout /t 30 /nobreak >nul

echo Starting Stage 2: Core Application...
docker-compose -f docker-compose.stage2-simple.yml up -d --build
if %errorlevel% neq 0 (
    echo ERROR: Failed to start core application
    pause
    exit /b 1
)

echo Waiting for application to be ready...
timeout /t 45 /nobreak >nul

echo.
echo ================================================================
echo                    DEPLOYMENT SUCCESSFUL!
echo ================================================================
echo.
echo Available Services:
echo   Main Application:     http://localhost:8031
echo   Frontend:            http://localhost:80
echo   Login Page:          http://localhost/login
echo   API Documentation:   http://localhost:8031/docs
echo   Health Check:        http://localhost:8031/health
echo.
echo Default Login Credentials:
echo   Username: admin
echo   Password: admin123
echo.
echo Container Status:
docker ps --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"
echo.
echo To add AI services, run: deploy_staged.cmd and choose option 3
echo To add monitoring, run: deploy_staged.cmd and choose option 4
echo To stop system, run: stop_system.cmd
echo.
pause
