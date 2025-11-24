@echo off
chcp 65001 >nul
cls
color 0A
echo.
echo ╔════════════════════════════════════════════════════════════════╗
echo ║                                                                ║
echo ║     DỰ ĐOÁN GIÁ BẤT ĐỘNG SẢN - MACHINE LEARNING               ║
echo ║                                                                ║
echo ╚════════════════════════════════════════════════════════════════╝
echo.
echo.
echo    Chọn chức năng:
echo.
echo    [1] 🚀 Khởi động Web Application
echo    [2] ⏹️  Dừng Server
echo    [3] 📊 Xem thông tin Model
echo    [4] 📁 Mở thư mục dự án
echo    [5] 🌐 Mở Web Browser (nếu server đang chạy)
echo    [6] 🔄 Export model metrics
echo    [7] 📝 Xem hướng dẫn sử dụng
echo    [0] ❌ Thoát
echo.
echo ════════════════════════════════════════════════════════════════
echo.

set /p choice="Nhập lựa chọn của bạn: "

if "%choice%"=="1" goto start_web
if "%choice%"=="2" goto stop_web
if "%choice%"=="3" goto view_info
if "%choice%"=="4" goto open_folder
if "%choice%"=="5" goto open_browser
if "%choice%"=="6" goto export_metrics
if "%choice%"=="7" goto view_guide
if "%choice%"=="0" goto exit

echo.
echo ⚠ Lựa chọn không hợp lệ!
timeout /t 2 >nul
goto menu

:start_web
cls
echo.
echo ════════════════════════════════════════════════════════════════
echo    KHỞI ĐỘNG WEB APPLICATION
echo ════════════════════════════════════════════════════════════════
echo.
start "House Price Prediction Server" "%~dp0START_WEB.bat"
echo ✓ Server đang khởi động trong cửa sổ mới...
echo.
echo ℹ️  Sau khi server khởi động xong, truy cập:
echo    👉 http://localhost:5000
echo.
timeout /t 3 >nul
goto menu

:stop_web
cls
echo.
echo ════════════════════════════════════════════════════════════════
echo    DỪNG SERVER
echo ════════════════════════════════════════════════════════════════
echo.
taskkill /F /IM python.exe 2>nul
if %errorlevel% == 0 (
    echo ✓ Đã dừng server thành công!
) else (
    echo ⚠ Không tìm thấy server đang chạy
)
echo.
timeout /t 2 >nul
goto menu

:view_info
cls
call "%~dp0VIEW_MODEL_INFO.bat"
goto menu

:open_folder
explorer "%~dp0"
goto menu

:open_browser
start http://localhost:5000
echo ✓ Đã mở browser...
timeout /t 1 >nul
goto menu

:export_metrics
cls
echo.
echo ════════════════════════════════════════════════════════════════
echo    EXPORT MODEL METRICS
echo ════════════════════════════════════════════════════════════════
echo.
cd /d "%~dp0"
"%~dp0.venv\Scripts\python.exe" export_model_info.py
echo.
pause
goto menu

:view_guide
cls
if exist "HUONG_DAN_SU_DUNG.txt" (
    type "HUONG_DAN_SU_DUNG.txt" | more
) else if exist "MODEL_STORAGE_README.md" (
    type "MODEL_STORAGE_README.md" | more
) else (
    echo ⚠ Không tìm thấy file hướng dẫn
)
echo.
pause
goto menu

:exit
cls
echo.
echo ════════════════════════════════════════════════════════════════
echo.
echo    Cảm ơn bạn đã sử dụng! 👋
echo.
echo ════════════════════════════════════════════════════════════════
echo.
timeout /t 2 >nul
exit

:menu
cls
color 0A
echo.
echo ╔════════════════════════════════════════════════════════════════╗
echo ║                                                                ║
echo ║     DỰ ĐOÁN GIÁ BẤT ĐỘNG SẢN - MACHINE LEARNING               ║
echo ║                                                                ║
echo ╚════════════════════════════════════════════════════════════════╝
echo.
echo.
echo    Chọn chức năng:
echo.
echo    [1] 🚀 Khởi động Web Application
echo    [2] ⏹️  Dừng Server
echo    [3] 📊 Xem thông tin Model
echo    [4] 📁 Mở thư mục dự án
echo    [5] 🌐 Mở Web Browser (nếu server đang chạy)
echo    [6] 🔄 Export model metrics
echo    [7] 📝 Xem hướng dẫn sử dụng
echo    [0] ❌ Thoát
echo.
echo ════════════════════════════════════════════════════════════════
echo.

set /p choice="Nhập lựa chọn của bạn: "

if "%choice%"=="1" goto start_web
if "%choice%"=="2" goto stop_web
if "%choice%"=="3" goto view_info
if "%choice%"=="4" goto open_folder
if "%choice%"=="5" goto open_browser
if "%choice%"=="6" goto export_metrics
if "%choice%"=="7" goto view_guide
if "%choice%"=="0" goto exit

echo.
echo ⚠ Lựa chọn không hợp lệ!
timeout /t 2 >nul
goto menu
