@echo off
title HealthPulse Launcher
cd /d "%~dp0"

echo ========================================================
echo        HealthPulse Healthcare Operations App
echo ========================================================

echo [1/2] Starting HealthPulse Server (Port 5000)...
start "HealthPulse Server" cmd /k "python backend\app.py"


echo [2/2] Waiting for server to start...
ping 127.0.0.1 -n 4 >nul

echo Opening Dashboard in your browser...
start http://127.0.0.1:5000/

echo ========================================================
echo HealthPulse App is now running!
echo Dashboard URL: http://127.0.0.1:5000/
echo ========================================================
echo (Keep the 'HealthPulse Server' window open while using the app)
echo.
pause

