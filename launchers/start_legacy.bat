@echo off
chcp 65001 >nul
title House Price Prediction - Legacy Version
color 0E

cls
echo.
echo ═══════════════════════════════════════════════════════════════
echo  🔵 LEGACY VERSION - HOUSE PRICE PREDICTION
echo ═══════════════════════════════════════════════════════════════
echo.
echo  ✅ Dataset: Cũ (bedrooms, bathrooms, year_built, floor_level)
echo  ✅ Records: ~19,000
echo  ✅ Features: Chi tiết đầy đủ
echo  ✅ URL: http://localhost:5000/legacy
echo.
echo  Đang khởi động server...
echo.

cd /d "%~dp0.."
timeout /t 2 >nul
start "" http://localhost:5000/legacy
"%~dp0..\.venv\Scripts\python.exe" app.py
