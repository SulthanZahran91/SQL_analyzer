@echo off
REM Batch script to start both backend and frontend servers

REM Set the base path to the directory where this script is located
set "BASE_PATH=%~dp0"

REM --- Start Backend Server ---
echo Starting Backend Server...
cd /D "%BASE_PATH%SQL_analyzer_backend"
start "Backend Server" cmd /k "uv run python start_backend.py"

REM Give the backend a moment to start up (optional, adjust as needed)
REM timeout /t 5 /nobreak > nul

REM --- Start Frontend Server ---
echo Starting Frontend Server...
cd /D "%BASE_PATH%SQL_analyzer"
start "Frontend Server (Vite)" cmd /k "npm run dev"

echo Both servers are starting in separate windows.

REM Keep this window open for a bit to see messages, then exit
REM timeout /t 10
exit /b 