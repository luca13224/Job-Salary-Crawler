@echo off
REM Job Salary Analytics - Demo Runner
REM This script starts both Backend and Frontend servers

echo ========================================
echo  Job Salary Dashboard - Demo Launcher
echo ========================================
echo.

echo [1/2] Starting Backend (FastAPI on port 8000)...
start "Backend" cmd /k "cd /d %~dp0 && set PYTHONPATH=%CD% && python -m uvicorn backend.main:app --port 8000 --host 127.0.0.1"

echo.
echo [2/2] Starting Frontend (Vite on port 5173)...
start "Frontend" cmd /k "cd /d %~dp0\frontend && npm run dev"

echo.
echo ========================================
echo Servers starting... Please wait 5 seconds
echo ========================================
timeout /t 5 /nobreak

echo.
echo Opening dashboard in browser...
timeout /t 2 /nobreak

REM Try to open in default browser
start http://localhost:5173

echo.
echo ========================================
echo DEMO RUNNING!
echo ========================================
echo.
echo Backend:  http://127.0.0.1:8000
echo Frontend: http://localhost:5173
echo.
echo Login with: admin / demo123
echo.
echo Close this window to stop.
pause
