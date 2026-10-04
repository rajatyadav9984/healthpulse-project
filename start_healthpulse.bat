@echo off
title HealthPulse Launcher
cd /d "%~dp0"

echo ========================================================
echo        HealthPulse Healthcare Operations App
echo ========================================================

echo [1/3] Clearing old processes on Port 5000...
for /f "tokens=5" %%a in ('netstat -aon ^| findstr :5000 ^| findstr LISTENING') do taskkill /F /PID %%a >nul 2>&1

echo [2/3] Starting HealthPulse Server...
start "HealthPulse Server" cmd /k "python backend\app.py"

echo [3/3] Waiting for server startup (1 to 2 seconds)...
powershell -NoProfile -ExecutionPolicy Bypass -Command "$ready=$false; for($i=0; $i -lt 10; $i++) { try { $res = Invoke-WebRequest -Uri 'http://127.0.0.1:5000/health' -UseBasicParsing -TimeoutSec 1 -ErrorAction Stop; if ($res.StatusCode -eq 200) { $ready=$true; break } } catch { Start-Sleep -Milliseconds 500 } }; if ($ready) { Write-Host 'SUCCESS: Server is UP and READY!' -ForegroundColor Green; [Environment]::Exit(0) } else { Write-Host 'ERROR: Server failed to start.' -ForegroundColor Red; [Environment]::Exit(1) }"

if errorlevel 1 goto SERVER_ERROR

echo.
echo Opening Dashboard in your browser...
start http://127.0.0.1:5000/
echo ========================================================
echo HealthPulse App is running!
echo Dashboard URL: http://127.0.0.1:5000/
echo ========================================================
echo (Keep the 'HealthPulse Server' window open while using the app)
echo.
pause
exit /b 0

:SERVER_ERROR
echo.
echo ========================================================
echo FAILED to start HealthPulse Server.
echo Please check the 'HealthPulse Server' window for error logs!
echo ========================================================
echo.
pause
exit /b 1





