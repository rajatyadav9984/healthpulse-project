@echo off
title Stop HealthPulse
echo Stopping HealthPulse Servers...

taskkill /FI "WINDOWTITLE eq HealthPulse Server*" /F >nul 2>&1
taskkill /FI "WINDOWTITLE eq HealthPulse Backend*" /F >nul 2>&1
taskkill /FI "WINDOWTITLE eq HealthPulse Frontend*" /F >nul 2>&1


:: Free ports 5000 and 8080 if still occupied
for /f "tokens=5" %%a in ('netstat -aon ^| findstr :5000 ^| findstr LISTENING') do taskkill /F /PID %%a >nul 2>&1
for /f "tokens=5" %%a in ('netstat -aon ^| findstr :8080 ^| findstr LISTENING') do taskkill /F /PID %%a >nul 2>&1

echo HealthPulse servers stopped cleanly.
ping 127.0.0.1 -n 3 >nul


