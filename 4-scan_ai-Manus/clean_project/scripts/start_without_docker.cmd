@echo off
title Smart Agricultural System - Local Development
color 0A

echo ================================================================
echo            Smart Agricultural System                           
echo               Local Development Mode                           
echo ================================================================
echo.

echo This will start the system without Docker containers
echo Useful for development and testing
echo.

echo Checking Python...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.11+ and try again
    pause
    exit /b 1
)

echo SUCCESS: Python is available
echo.

echo Installing/updating required packages...
python -m pip install --upgrade pip
python -m pip install -r requirements-basic.txt

echo.
echo Creating required directories...
if not exist "logs" mkdir logs
if not exist "uploads" mkdir uploads
if not exist "backups" mkdir backups
if not exist "data" mkdir data
if not exist "media" mkdir media
if not exist "static" mkdir static

echo.
echo Starting the application...
echo.
echo The application will be available at:
echo - Main Application: http://localhost:8031
echo - Login Page: http://localhost:8031/login
echo - API Documentation: http://localhost:8031/docs
echo.
echo Default credentials: admin / admin123
echo.
echo Press Ctrl+C to stop the application
echo.

cd src
python main.py
