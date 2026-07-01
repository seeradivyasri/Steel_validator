@echo off
echo ==============================================
echo   Starting Steel Validation Command Center...
echo ==============================================
echo.
echo Please keep the black server window open in the background!
echo Opening dashboard in your web browser...

:: Change directory to where this script is located
cd /d "%~dp0"

:: Start the Python backend server in a separate minimized command window
start "Steel Validator Background Engine" /min cmd /c "python backend/main.py"

:: Wait 3 seconds to ensure the server has time to wake up and load the AI
timeout /t 3 /nobreak >nul

:: Automatically open the default web browser to the dashboard
start http://localhost:8000/app
