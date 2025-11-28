@echo off
chcp 65001 >nul
title House Price Prediction - Version Selector
color 0B

:menu
cls
echo.
echo ╔═══════════════════════════════════════════════════════════════╗
echo ║         🏠 HOUSE PRICE PREDICTION - VERSION SELECTOR         ║
echo ╚═══════════════════════════════════════════════════════════════╝
echo.
echo  Chọn phiên bản bạn muốn sử dụng:
echo.
echo  ┌─────────────────────────────────────────────────────────────┐
echo  │  [1] 🔵 LEGACY VERSION - Dataset Cũ                         │
echo  │      • Bedrooms, Bathrooms, Year Built, Floor Level         │
echo  │      • ~19,000 records                                      │
echo  │      • Chi tiết, đầy đủ features                            │
echo  │      • Backup an toàn                                       │
echo  └─────────────────────────────────────────────────────────────┘
echo.
echo  ┌─────────────────────────────────────────────────────────────┐
echo  │  [2] 🟢 API VERSION - Dataset Mới (Singapore HDB)           │
echo  │      • Property Type system                                 │
echo  │      • 978,000 records (Big Data)                           │
echo  │      • Enhanced APIs (Trend, ROI, SHAP)                     │
echo  │      • Multi-country                                        │
echo  └─────────────────────────────────────────────────────────────┘
echo.
echo  ┌─────────────────────────────────────────────────────────────┐
echo  │  [3] 🎯 VERSION SELECTOR - Chọn từ Web                      │
echo  │      • Mở landing page để chọn version                      │
echo  └─────────────────────────────────────────────────────────────┘
echo.
echo  [0] ❌ Thoát
echo.
echo ═══════════════════════════════════════════════════════════════
echo.

set /p choice="  Nhập lựa chọn của bạn (0-3): "

if "%choice%"=="1" goto legacy
if "%choice%"=="2" goto api
if "%choice%"=="3" goto selector
if "%choice%"=="0" goto exit
echo.
echo  ⚠️  Lựa chọn không hợp lệ! Vui lòng chọn 0-3.
timeout /t 2 >nul
goto menu

:legacy
cls
echo.
echo ═══════════════════════════════════════════════════════════════
echo  🔵 LEGACY VERSION
echo ═══════════════════════════════════════════════════════════════
echo.
echo  Đang khởi động server với Legacy Version...
echo  • Dataset: Cũ (bedrooms, bathrooms, year_built, floor_level)
echo  • URL: http://localhost:5000/legacy
echo.
echo  ⏳ Vui lòng đợi server khởi động...
echo.

set DEFAULT_PAGE=/legacy
start "" http://localhost:5000/legacy
.venv\Scripts\python.exe app.py
goto end

:api
cls
echo.
echo ═══════════════════════════════════════════════════════════════
echo  🟢 API VERSION
echo ═══════════════════════════════════════════════════════════════
echo.
echo  Đang khởi động server với API Version...
echo  • Dataset: Mới (property_type, 978K records)
echo  • URL: http://localhost:5000/
echo.
echo  ⏳ Vui lòng đợi server khởi động...
echo.

set DEFAULT_PAGE=/
start "" http://localhost:5000/
.venv\Scripts\python.exe app.py
goto end

:selector
cls
echo.
echo ═══════════════════════════════════════════════════════════════
echo  🎯 VERSION SELECTOR
echo ═══════════════════════════════════════════════════════════════
echo.
echo  Đang khởi động server với Landing Page...
echo  • URL: http://localhost:5000/select
echo  • Bạn có thể chọn version từ web browser
echo.
echo  ⏳ Vui lòng đợi server khởi động...
echo.

set DEFAULT_PAGE=/select
start "" http://localhost:5000/select
.venv\Scripts\python.exe app.py
goto end

:exit
cls
echo.
echo  👋 Tạm biệt! Cảm ơn bạn đã sử dụng House Price Prediction.
echo.
timeout /t 2 >nul
exit

:end
echo.
echo.
echo ═══════════════════════════════════════════════════════════════
echo  Server đã dừng.
echo ═══════════════════════════════════════════════════════════════
echo.
pause
goto menu
