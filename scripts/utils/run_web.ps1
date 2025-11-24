# PowerShell script to run the web application
Write-Host "==============================================================" -ForegroundColor Cyan
Write-Host "    House Price Prediction Web Application" -ForegroundColor Cyan
Write-Host "==============================================================" -ForegroundColor Cyan
Write-Host ""

# Check if virtual environment exists
if (-Not (Test-Path ".\.venv")) {
    Write-Host "Virtual environment not found. Creating..." -ForegroundColor Yellow
    python -m venv .venv
}

# Activate virtual environment
Write-Host "Activating virtual environment..." -ForegroundColor Green
.\.venv\Scripts\Activate.ps1

# Install/upgrade dependencies
Write-Host "Installing dependencies..." -ForegroundColor Green
.\.venv\Scripts\python.exe -m pip install --upgrade pip -q
.\.venv\Scripts\python.exe -m pip install -r requirements.txt -q

# Check if model exists
if (-Not (Test-Path ".\models\best.joblib")) {
    Write-Host ""
    Write-Host "WARNING: Model file not found!" -ForegroundColor Red
    Write-Host "Please run training first:" -ForegroundColor Yellow
    Write-Host "  python train_pipeline.py --data 'Data\cleaned_real_estate.csv'" -ForegroundColor White
    Write-Host ""
    $response = Read-Host "Do you want to run training now? (y/n)"
    if ($response -eq 'y' -or $response -eq 'Y') {
        Write-Host "Running training..." -ForegroundColor Green
        .\.venv\Scripts\python.exe .\train_pipeline.py --data "Data\cleaned_real_estate.csv" --nrows 1000 --sample-frac 0.2
    }
}

# Run Flask app
Write-Host ""
Write-Host "==============================================================" -ForegroundColor Cyan
Write-Host "Starting Flask web server..." -ForegroundColor Green
Write-Host "Open your browser and navigate to: http://localhost:5000" -ForegroundColor White
Write-Host "Press Ctrl+C to stop the server" -ForegroundColor Yellow
Write-Host "==============================================================" -ForegroundColor Cyan
Write-Host ""

.\.venv\Scripts\python.exe app.py
