@echo off
chcp 65001 >nul
title External API Predictor - No Dataset Mode

cd /d "%~dp0.."

echo.
echo ═══════════════════════════════════════════════════════════════
echo 🌐 EXTERNAL API PREDICTOR
echo ═══════════════════════════════════════════════════════════════
echo.
echo This mode uses ONLY external APIs - no local dataset needed!
echo.
echo Available APIs:
echo   ✓ Singapore HDB API (FREE - data.gov.sg)
echo   ⚠ USA Zillow API (Requires RapidAPI key)
echo.
echo ═══════════════════════════════════════════════════════════════
echo.

"%~dp0..\.venv\Scripts\python.exe" scripts/external_api_predictor.py
