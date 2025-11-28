@echo off
title Train New Model with External API Data
color 0B

echo.
echo ================================================
echo       TRAIN NEW MODEL - EXTERNAL API DATA
echo ================================================
echo.
echo Select data source:
echo.
echo [1] Singapore HDB (FREE, no API key needed)
echo [2] Multi-source (requires API keys)
echo [3] Use existing CSV file
echo [4] Back to main menu
echo.

set /p choice="Enter your choice (1-4): "

if "%choice%"=="1" goto singapore
if "%choice%"=="2" goto multisource
if "%choice%"=="3" goto existing
if "%choice%"=="4" goto end

echo Invalid choice!
timeout /t 2 >nul
goto end

:singapore
echo.
echo ================================================
echo    Fetching Singapore HDB Data...
echo ================================================
cd /d "D:\Do An Tot Nghiep - Du doan gia bat dong san bang ML va DL"
call .venv\Scripts\activate.bat
python -c "from scripts.fetch_external_data import RealEstateAPIClient; from datetime import datetime; c = RealEstateAPIClient(); df = c.fetch_singapore_hdb_data(datetime.now().year, datetime.now().month); print(f'\nFetched {len(df)} records'); df.to_csv('Data/singapore_latest.csv', index=False); print('Saved to Data/singapore_latest.csv')"

echo.
echo ================================================
echo    Training Model...
echo ================================================
python -c "from scripts.model_manager import ModelManager; m = ModelManager(); m.train_new_model('Data/singapore_latest.csv', 'singapore_hdb_model', 'lightgbm')"

echo.
echo Press any key to return to menu...
pause >nul
goto end

:multisource
echo.
echo ================================================
echo    Multi-Source Data Collection
echo ================================================
echo.
echo NOTE: You need API keys configured in config/api_keys.json
echo.
echo Press Enter to continue or Ctrl+C to cancel...
pause >nul

cd /d "D:\Do An Tot Nghiep - Du doan gia bat dong san bang ML va DL"
call .venv\Scripts\activate.bat
python -c "from scripts.fetch_external_data import RealEstateAPIClient; import json; c = RealEstateAPIClient(); config = json.load(open('config/api_keys.json')); apis = {'singapore': {'year': 2024, 'month': 11}}; df = c.fetch_multi_source_data(apis); print(f'\nTotal records: {len(df)}')"

echo.
echo Press any key to continue...
pause >nul
goto end

:existing
echo.
echo ================================================
echo    Train Model from Existing CSV
echo ================================================
echo.
set /p csvfile="Enter CSV file path (relative to Data/): "
set /p modelname="Enter model name: "
set /p modeltype="Enter model type (lightgbm/xgboost): "

cd /d "D:\Do An Tot Nghiep - Du doan gia bat dong san bang ML va DL"
call .venv\Scripts\activate.bat
python -c "from scripts.model_manager import ModelManager; m = ModelManager(); m.train_new_model('Data/%csvfile%', '%modelname%', '%modeltype%')"

echo.
goto end

:end
