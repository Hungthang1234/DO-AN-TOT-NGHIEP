@echo off
chcp 65001 >nul
color 0B
echo.
echo ════════════════════════════════════════════════════════════
echo    📊 MODEL INFO - Thông tin Model hiện tại
echo ════════════════════════════════════════════════════════════
echo.

cd /d "%~dp0.."

echo 📋 Reading model metadata...
echo.

if exist "config\model_metadata.json" (
    echo ✓ Model Metadata (config/model_metadata.json):
    echo.
    type "config\model_metadata.json"
    echo.
    echo.
) else (
    echo ⚠ model_metadata.json not found in config/
)

if exist "docs\MODEL_REFERENCE.txt" (
    echo ✓ Model Reference Documentation:
    echo.
    type "docs\MODEL_REFERENCE.txt"
) else (
    echo 📄 MODEL_REFERENCE.txt not found in docs/
)

echo.
echo ════════════════════════════════════════════════════════════
echo  Press any key to exit...
pause >nul
