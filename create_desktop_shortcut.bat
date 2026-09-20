@echo off
title Create HealthPulse Desktop Shortcut
cd /d "%~dp0"

echo Creating Desktop Shortcut for HealthPulse...

set "TARGET_BAT=%~dp0start_healthpulse.bat"
set "WORK_DIR=%~dp0"
set "SHORTCUT_PATH=%USERPROFILE%\Desktop\HealthPulse.lnk"

powershell -NoProfile -ExecutionPolicy Bypass -Command "$s=(New-Object -COM WScript.Shell).CreateShortcut('%SHORTCUT_PATH%'); $s.TargetPath='%TARGET_BAT%'; $s.WorkingDirectory='%WORK_DIR%'; $s.IconLocation='shell32.dll,13'; $s.Save()"

if exist "%SHORTCUT_PATH%" (
    echo ========================================================
    echo SUCCESS: 'HealthPulse' shortcut created on your Desktop!
    echo Now you can double-click 'HealthPulse' icon on Desktop
    echo to start backend, frontend, and open browser in 1 CLICK!
    echo ========================================================
) else (
    echo Failed to create desktop shortcut.
)

pause
