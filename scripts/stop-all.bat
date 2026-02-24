@echo off
REM =============================================================================
REM Store ERP - Stop All Services Script (Windows)
REM =============================================================================

echo.
echo ========================================
echo Store ERP - Stopping All Services
echo ========================================
echo.

docker-compose -f docker-compose.yml down 2>nul
docker-compose -f docker-compose.prod.yml down 2>nul
docker-compose -f docker-compose.monitoring.yml down 2>nul

echo [OK] All services stopped
echo.

set /p "REMOVE_VOLUMES=Remove all volumes? (y/N): "
if /i "%REMOVE_VOLUMES%"=="y" (
    docker-compose -f docker-compose.prod.yml down -v
    echo [OK] Volumes removed
)

echo.
