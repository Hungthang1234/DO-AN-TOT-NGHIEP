@echo off
title Switch Active Model
color 0E

echo.
echo ================================================
echo           SWITCH ACTIVE MODEL
echo ================================================
echo.

cd /d "D:\Do An Tot Nghiep - Du doan gia bat dong san bang ML va DL"
call .venv\Scripts\activate.bat

echo Current available models:
echo.
python -c "from scripts.model_manager import ModelManager; m = ModelManager(); models = m.list_available_models(); print('\n'.join([f'  [{i+1}] {model[\"name\"]:30} - R²: {model[\"r2\"]:.4f}, RMSE: ${model[\"rmse\"]:,.0f}' for i, model in enumerate(models)]))"

echo.
echo ================================================
echo.
set /p choice="Enter model number to activate: "

python -c "from scripts.model_manager import ModelManager; m = ModelManager(); models = m.list_available_models(); model_name = models[int('%choice%')-1]['name']; m.set_active_model(model_name)"

echo.
echo ================================================
echo Active model has been switched!
echo Please restart the Flask app for changes to take effect.
echo ================================================
echo.
