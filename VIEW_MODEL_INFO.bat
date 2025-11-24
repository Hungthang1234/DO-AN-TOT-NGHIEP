@echo off
chcp 65001 >nul
echo.
echo ============================================================
echo    XEM THÔNG TIN MODEL
echo ============================================================
echo.

cd /d "%~dp0"

if exist "MODEL_REFERENCE.txt" (
    type "MODEL_REFERENCE.txt"
) else (
    echo ⚠ File MODEL_REFERENCE.txt không tồn tại
    echo Đang tạo...
    "%~dp0.venv\Scripts\python.exe" export_model_info.py
)

echo.
echo.
pause
