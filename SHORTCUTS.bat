@echo off
chcp 65001 >nul
color 0B
cls
echo.
echo ╔════════════════════════════════════════════════════════════════╗
echo ║                                                                ║
echo ║     🚀 SHORTCUTS - Truy cập nhanh                             ║
echo ║                                                                ║
echo ╚════════════════════════════════════════════════════════════════╝
echo.
echo.
echo    📁 THƯ MỤC QUAN TRỌNG:
echo.
echo    [1] 📂 bat_files/        - BAT files (MENU, START, STOP)
echo    [2] 📂 scripts/          - Python scripts
echo    [3] 📂 models/           - Trained models
echo    [4] 📂 logs/             - Training và prediction logs
echo    [5] 📂 docs/             - Documentation
echo    [6] 📂 Data/             - Datasets
echo.
echo    🚀 CHẠY NHANH:
echo.
echo    [7] ▶️  Khởi động web    - bat_files/START_WEB.bat
echo    [8] 📋 Menu chính        - bat_files/MENU.bat
echo    [9] 📊 Xem model info    - bat_files/VIEW_MODEL_INFO.bat
echo.
echo    📄 ĐỌC DOCS:
echo.
echo    [A] 📖 Cấu trúc dự án   - PROJECT_STRUCTURE.md
echo    [B] 📖 Kết quả training - docs/KETQUA_TRANH_OVERFITTING.md
echo    [C] 📖 Quick start      - docs/README_QUICKSTART.md
echo    [D] 📖 Model reference  - docs/MODEL_REFERENCE.txt
echo.
echo    [0] ❌ Thoát
echo.
echo ════════════════════════════════════════════════════════════════
echo.

set /p choice="Nhập lựa chọn: "

if "%choice%"=="1" start explorer "%~dp0bat_files" & goto menu
if "%choice%"=="2" start explorer "%~dp0scripts" & goto menu
if "%choice%"=="3" start explorer "%~dp0models" & goto menu
if "%choice%"=="4" start explorer "%~dp0logs" & goto menu
if "%choice%"=="5" start explorer "%~dp0docs" & goto menu
if "%choice%"=="6" start explorer "%~dp0Data" & goto menu

if "%choice%"=="7" start "" "%~dp0bat_files\START_WEB.bat" & goto menu
if "%choice%"=="8" start "" "%~dp0bat_files\MENU.bat" & goto menu
if "%choice%"=="9" start "" "%~dp0bat_files\VIEW_MODEL_INFO.bat" & goto menu

if /i "%choice%"=="A" start notepad "%~dp0PROJECT_STRUCTURE.md" & goto menu
if /i "%choice%"=="B" start notepad "%~dp0docs\KETQUA_TRANH_OVERFITTING.md" & goto menu
if /i "%choice%"=="C" start notepad "%~dp0docs\README_QUICKSTART.md" & goto menu
if /i "%choice%"=="D" start notepad "%~dp0docs\MODEL_REFERENCE.txt" & goto menu

if "%choice%"=="0" exit

echo.
echo ⚠ Lựa chọn không hợp lệ!
timeout /t 2 >nul

:menu
cls
color 0B
echo.
echo ╔════════════════════════════════════════════════════════════════╗
echo ║                                                                ║
echo ║     🚀 SHORTCUTS - Truy cập nhanh                             ║
echo ║                                                                ║
echo ╚════════════════════════════════════════════════════════════════╝
echo.
echo.
echo    📁 THƯ MỤC QUAN TRỌNG:
echo.
echo    [1] 📂 bat_files/        - BAT files (MENU, START, STOP)
echo    [2] 📂 scripts/          - Python scripts
echo    [3] 📂 models/           - Trained models
echo    [4] 📂 logs/             - Training và prediction logs
echo    [5] 📂 docs/             - Documentation
echo    [6] 📂 Data/             - Datasets
echo.
echo    🚀 CHẠY NHANH:
echo.
echo    [7] ▶️  Khởi động web    - bat_files/START_WEB.bat
echo    [8] 📋 Menu chính        - bat_files/MENU.bat
echo    [9] 📊 Xem model info    - bat_files/VIEW_MODEL_INFO.bat
echo.
echo    📄 ĐỌC DOCS:
echo.
echo    [A] 📖 Cấu trúc dự án   - PROJECT_STRUCTURE.md
echo    [B] 📖 Kết quả training - docs/KETQUA_TRANH_OVERFITTING.md
echo    [C] 📖 Quick start      - docs/README_QUICKSTART.md
echo    [D] 📖 Model reference  - docs/MODEL_REFERENCE.txt
echo.
echo    [0] ❌ Thoát
echo.
echo ════════════════════════════════════════════════════════════════
echo.

set /p choice="Nhập lựa chọn: "

if "%choice%"=="1" start explorer "%~dp0bat_files" & goto menu
if "%choice%"=="2" start explorer "%~dp0scripts" & goto menu
if "%choice%"=="3" start explorer "%~dp0models" & goto menu
if "%choice%"=="4" start explorer "%~dp0logs" & goto menu
if "%choice%"=="5" start explorer "%~dp0docs" & goto menu
if "%choice%"=="6" start explorer "%~dp0Data" & goto menu

if "%choice%"=="7" start "" "%~dp0bat_files\START_WEB.bat" & goto menu
if "%choice%"=="8" start "" "%~dp0bat_files\MENU.bat" & goto menu
if "%choice%"=="9" start "" "%~dp0bat_files\VIEW_MODEL_INFO.bat" & goto menu

if /i "%choice%"=="A" start notepad "%~dp0PROJECT_STRUCTURE.md" & goto menu
if /i "%choice%"=="B" start notepad "%~dp0docs\KETQUA_TRANH_OVERFITTING.md" & goto menu
if /i "%choice%"=="C" start notepad "%~dp0docs\README_QUICKSTART.md" & goto menu
if /i "%choice%"=="D" start notepad "%~dp0docs\MODEL_REFERENCE.txt" & goto menu

if "%choice%"=="0" exit

echo.
echo ⚠ Lựa chọn không hợp lệ!
timeout /t 2 >nul
goto menu
