@echo off
chcp 65001 >nul
echo.
echo ============================================================
echo    DỪNG SERVER
echo ============================================================
echo.
echo Đang dừng tất cả Python processes...
echo.

taskkill /F /IM python.exe 2>nul

if %errorlevel% == 0 (
    echo ✓ Đã dừng server thành công!
) else (
    echo ⚠ Không tìm thấy server đang chạy
)

echo.
pause
