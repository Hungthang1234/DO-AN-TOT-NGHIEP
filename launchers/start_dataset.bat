@echo off
chcp 65001 >nul
title House Price Prediction - Dataset Version

cd /d "%~dp0.."

cls
echo.
echo ═══════════════════════════════════════════════════════════════
echo  📊 DATASET VERSION - Singapore HDB
echo ═══════════════════════════════════════════════════════════════
echo.
echo  ✅ Dataset: Singapore HDB (property_type system)
echo  ✅ Records: 978,000 (Big Data)
echo  ✅ Features: Enhanced APIs (Trend, ROI, SHAP)
echo  ✅ URL: http://localhost:5000/
echo.
echo  Đang khởi động server...
echo.

timeout /t 2 >nul
start "" http://localhost:5000/
"%~dp0..\.venv\Scripts\python.exe" app.py
