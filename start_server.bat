@echo off

cd /d "%~dp0"

where python >nul 2>nul
if errorlevel 1 (
    echo Python was not found on PATH.
    echo Install Python from https://www.python.org and tick "Add Python to PATH".
    echo See docs\INSTALLATION.md for help.
    pause
    exit /b 1
)

python server.py
pause