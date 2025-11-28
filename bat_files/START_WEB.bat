@echo off
chcp 65001 >nul
title House Price Prediction - Web Server
color 0B

cls
echo.
echo ══════════════════════════════════════════════════════════════
echo    🏠 HOUSE PRICE PREDICTION - WEB APPLICATION
echo ══════════════════════════════════════════════════════════════
echo.
echo Starting server...
echo.

cd /d "%~dp0.."

REM Start Python server
start "Flask Server" /B "%~dp0..\\.venv\\Scripts\\python.exe" app.py

REM Wait for server to start
timeout /t 3 /nobreak >nul

REM Open browser
start http://127.0.0.1:5000

echo.
echo ✓ Server started successfully!
echo ✓ Browser opened at: http://127.0.0.1:5000
echo.
echo ══════════════════════════════════════════════════════════════
echo.
echo Press any key to stop the server...
pause >nul

REM Kill Python processes when done
taskkill /F /IM python.exe 2>nul
echo.
echo ✓ Server stopped
echo.
timeout /t 2 >nul
