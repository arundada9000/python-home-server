@echo off
echo ============================================
echo   SajiloCloud with Collaborative Tools
echo ============================================
echo.
echo Starting servers...
echo.

REM Make sure Python is available before starting anything
where python >nul 2>nul
if errorlevel 1 (
    echo.
    echo Python was not found on PATH.
    echo Install Python from https://www.python.org and tick "Add Python to PATH".
    echo See docs\INSTALLATION.md for help.
    pause
    exit /b 1
)

REM Start WebSocket server in a new window
start "WebSocket Server" cmd /k "python websocket_server.py"

REM Wait a moment for WebSocket server to start
timeout /t 2 /nobreak > nul

REM Start main HTTP server
echo Starting HTTP server...
python server.py
