@echo off
chcp 65001 >nul
echo.
echo ============================================================
echo    DỰ ĐOÁN GIÁ BẤT ĐỘNG SẢN - WEB APPLICATION
echo ============================================================
echo.
echo Đang khởi động server...
echo.

cd /d "%~dp0"

"%~dp0.venv\Scripts\python.exe" app.py

pause
