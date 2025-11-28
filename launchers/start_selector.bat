@echo off
chcp 65001 >nul
title House Price Prediction - Version Selector
color 0D

cls
echo.
echo ═══════════════════════════════════════════════════════════════
echo  🎯 VERSION SELECTOR - HOUSE PRICE PREDICTION
echo ═══════════════════════════════════════════════════════════════
echo.
echo  ✅ Landing Page: Chọn version từ web browser
echo  ✅ URL: http://localhost:5000/select
echo.
echo  Bạn có thể chọn giữa:
echo   • Legacy Version (Dataset cũ)
echo   • API Version (Dataset mới)
echo.
echo  Đang khởi động server...
echo.

cd /d "%~dp0.."
timeout /t 2 >nul
start "" http://localhost:5000/select
"%~dp0..\.venv\Scripts\python.exe" app.py
