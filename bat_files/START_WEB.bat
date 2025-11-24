@echo off
chcp 65001 >nul
echo.
echo ============================================================
echo    DỰ ĐOÁN GIÁ BẤT ĐỘNG SẢN - WEB APPLICATION
echo ============================================================
echo.
echo Đang khởi động server...
echo.

cd /d "%~dp0.."

REM Start Python server in background
start "Flask Server" /B "%~dp0..\.venv\Scripts\python.exe" app.py

REM Wait for server to start
timeout /t 3 /nobreak >nul

REM Open browser
start http://localhost:5000

echo.
echo ✓ Server started and browser opened!
echo ✓ URL: http://localhost:5000
echo.
echo Press any key to stop server...
pause >nul

REM Kill Python processes when done
taskkill /F /IM python.exe 2>nul
