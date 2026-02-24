@echo off
echo ============================================================
echo Starting Backend Server...
echo ============================================================
cd /d "%~dp0"
cd ..
call .venv\Scripts\activate.bat
cd backend
python minimal_server.py
pause

