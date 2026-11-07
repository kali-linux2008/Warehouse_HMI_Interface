@echo off
setlocal
cd /d "%~dp0"
title Siemens OPC UA - One Click Setup

echo.
echo ==============================================
echo   SIEMENS OPC UA - ONE CLICK SETUP
echo ==============================================
echo.

powershell.exe -NoProfile -ExecutionPolicy Bypass -File "%~dp0install.ps1"
if errorlevel 1 (
  echo.
  echo INSTALLATION FAILED. See the error above.
  pause
  exit /b 1
)

powershell.exe -NoProfile -ExecutionPolicy Bypass -File "%~dp0first-run.ps1"
if errorlevel 1 (
  echo.
  echo SETUP DID NOT COMPLETE. See the error above.
  pause
  exit /b 1
)

echo.
echo All available automatic steps have finished.
pause
