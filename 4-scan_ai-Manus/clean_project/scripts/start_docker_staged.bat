@echo off
REM Start Docker with Staged Deployment

echo ========================================
echo Starting AI Agricultural System
echo ========================================
echo.

REM Check if Docker is running
docker ps >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Docker is not running. Please start Docker Desktop first.
    pause
    exit /b 1
)

echo Starting Stage 1: Infrastructure Services...
echo ========================================
docker-compose -f docker-compose.stage1.yml up -d

echo.
echo Waiting for databases to be ready...
timeout /t 30 /nobreak >nul

echo.
echo Starting Stage 2: Main Application...
echo ========================================
docker-compose -f docker-compose.stage2.yml up -d

echo.
echo Waiting for application to start...
timeout /t 30 /nobreak >nul

echo.
echo Starting Stage 3: Optional Services...
echo ========================================
docker-compose -f docker-compose.stage3.yml up -d

echo.
echo ========================================
echo Deployment Complete!
echo ========================================
echo.
echo Application URL: http://localhost:8031
echo RabbitMQ Management: http://localhost:15672
echo MinIO Console: http://localhost:9001
echo.
echo To check status: docker ps
echo To view logs: docker logs agri_ai_app -f
echo.
pause 