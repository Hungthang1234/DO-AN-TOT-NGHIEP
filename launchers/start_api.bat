@echo off
chcp 65001 >nul
title House Price Prediction - External API Version
color 0A

cls
echo.
echo ═══════════════════════════════════════════════════════════════
echo  🟢 EXTERNAL API VERSION
echo ═══════════════════════════════════════════════════════════════
echo.
echo  ✅ Data source: Singapore HDB API (FREE - data.gov.sg)
echo  ✅ Real-time: Fetch data from external APIs
echo  ✅ Dataset: KHÔNG dùng dataset local
echo  ✅ URL: http://localhost:5000/external_api
echo.
echo  Đang khởi động server...
echo.

cd /d "%~dp0.."
timeout /t 2 >nul
start "" http://localhost:5000/external_api
"%~dp0..\.venv\Scripts\python.exe" app.py
