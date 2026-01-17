@echo off
REM =============================================================================
REM Store ERP - Development Mode Startup Script (Windows)
REM =============================================================================

setlocal

echo.
echo ========================================
echo Store ERP - Development Mode
echo ========================================
echo.

REM Check virtual environment
if not exist .venv (
    echo [INFO] Creating virtual environment...
    python -m venv .venv
)

REM Activate virtual environment
call .venv\Scripts\activate.bat

REM Install/upgrade dependencies
echo [INFO] Installing dependencies...
pip install -r backend\requirements.txt --upgrade

REM Check argon2-cffi
python -c "import argon2" 2>nul
if errorlevel 1 (
    echo [INFO] Installing argon2-cffi...
    pip install argon2-cffi==23.1.0
)

echo [OK] Dependencies installed
echo.

REM Kill existing Python processes
taskkill /F /IM python.exe /T 2>nul

REM Start backend
echo [INFO] Starting backend on http://127.0.0.1:5002
cd backend

set FLASK_APP=app:create_app
set FLASK_ENV=development
set FLASK_DEBUG=1

start "Store Backend" python -m flask run --host=0.0.0.0 --port=5002 --debug

cd ..

echo [OK] Backend started
echo.
echo ========================================
echo Development Server Running
echo ========================================
echo.
echo Services:
echo   Backend:  http://127.0.0.1:5002
echo   API Docs: http://127.0.0.1:5002/api
echo   Health:   http://127.0.0.1:5002/health
echo.
echo Press Ctrl+C in the backend window to stop
echo.

endlocal
