@echo off
chcp 65001 >nul
cls
color 0B

:menu
cls
echo.
echo ╔══════════════════════════════════════════════════════════════╗
echo ║                                                              ║
echo ║     🏠 DỰ ĐOÁN GIÁ BẤT ĐỘNG SẢN - ML & DL                   ║
echo ║                                                              ║
echo ╚══════════════════════════════════════════════════════════════╝
echo.
echo  📊 MAIN MENU
echo.
echo    [1] 🚀 Start Web Application
echo    [2] ⏹️  Stop Server
echo    [3] 🌐 Open in Browser (http://127.0.0.1:5000)
echo    [4] 📊 View Model Info
echo    [5] 📁 Open Project Folder
echo    [6] 📚 View Documentation
echo    [7] 🧪 Run Tests
echo    [0] ❌ Exit
echo.
echo ══════════════════════════════════════════════════════════════
echo.

set /p choice="Choose option: "

if "%choice%"=="1" goto start_web
if "%choice%"=="2" goto stop_web
if "%choice%"=="3" goto open_browser
if "%choice%"=="4" goto view_info
if "%choice%"=="5" goto open_folder
if "%choice%"=="6" goto view_docs
if "%choice%"=="7" goto run_tests
if "%choice%"=="0" goto exit

echo.
echo ⚠️ Invalid choice!
timeout /t 2 >nul
goto menu

:start_web
cls
echo.
echo ══════════════════════════════════════════════════════════════
echo  🚀 STARTING WEB APPLICATION
echo ══════════════════════════════════════════════════════════════
echo.
cd /d "%~dp0.."
start "House Price Prediction" cmd /k ""%~dp0..\\.venv\\Scripts\\python.exe" app.py"
echo.
echo ✓ Server is starting...
echo ✓ URL: http://127.0.0.1:5000
echo.
echo  Opening browser in 3 seconds...
timeout /t 3 >nul
start http://127.0.0.1:5000
echo.
pause
goto menu

:stop_web
cls
echo.
echo ══════════════════════════════════════════════════════════════
echo  ⏹️ STOPPING SERVER
echo ══════════════════════════════════════════════════════════════
echo.
taskkill /F /IM python.exe 2>nul
if %errorlevel% == 0 (
    echo ✓ Server stopped successfully!
) else (
    echo ⚠️ No server running
)
echo.
pause
goto menu

:open_browser
start http://127.0.0.1:5000
echo ✓ Opening browser...
timeout /t 1 >nul
goto menu

:view_info
cls
call "%~dp0VIEW_MODEL_INFO.bat"
goto menu

:open_folder
explorer "%~dp0.."
goto menu

:view_docs
cls
echo.
echo ══════════════════════════════════════════════════════════════
echo  📚 DOCUMENTATION
echo ══════════════════════════════════════════════════════════════
echo.
echo    [1] Quick Start Guide
echo    [2] Advanced Charts Complete
echo    [3] External API Guide
echo    [4] Multi-Country Support
echo    [5] Project Structure
echo    [6] Open docs/ folder
echo    [0] Back
echo.
set /p doc="Choose: "
if "%doc%"=="1" start notepad "%~dp0..\\docs\\QUICK_START.md"
if "%doc%"=="2" start notepad "%~dp0..\\docs\\ADVANCED_CHARTS_COMPLETE.md"
if "%doc%"=="3" start notepad "%~dp0..\\docs\\EXTERNAL_API_COMPLETE.md"
if "%doc%"=="4" start notepad "%~dp0..\\docs\\MULTI_COUNTRY_COMPLETE.md"
if "%doc%"=="5" start notepad "%~dp0..\\docs\\PROJECT_STRUCTURE.md"
if "%doc%"=="6" explorer "%~dp0..\\docs"
if "%doc%"=="0" goto menu
timeout /t 1 >nul
goto view_docs

:run_tests
cls
echo.
echo ══════════════════════════════════════════════════════════════
echo  🧪 RUNNING TESTS
echo ══════════════════════════════════════════════════════════════
echo.
cd /d "%~dp0.."
echo Running test_charts_api.py...
"%~dp0..\\.venv\\Scripts\\python.exe" tests\\test_charts_api.py
echo.
echo.
pause
goto menu

:exit
cls
echo.
echo ══════════════════════════════════════════════════════════════
echo.
echo    👋 Thanks for using! Goodbye!
echo.
echo ══════════════════════════════════════════════════════════════
echo.
timeout /t 2 >nul
exit
