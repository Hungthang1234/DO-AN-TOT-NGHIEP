# API Testing Script
# Chạy sau khi start server với: START.bat → [2] API Version

Write-Host "🧪 TESTING ENHANCED APIs" -ForegroundColor Cyan
Write-Host "=" * 60
Write-Host ""

# Wait for user confirmation
Write-Host "⚠️  Đảm bảo server đang chạy (START.bat → [2] API Version)" -ForegroundColor Yellow
Write-Host "Press Enter to continue..."
$null = Read-Host

$baseUrl = "http://localhost:5000"

# Test 1: Health Check
Write-Host "`n1️⃣  Testing Health Check..." -ForegroundColor Green
try {
    $health = Invoke-RestMethod -Uri "$baseUrl/api/health" -Method GET
    Write-Host "✅ Health Check OK" -ForegroundColor Green
    $health | ConvertTo-Json | Write-Host
} catch {
    Write-Host "❌ Health Check Failed: $_" -ForegroundColor Red
}

Write-Host "`nPress Enter for next test..."
$null = Read-Host

# Test 2: Predict Trend
Write-Host "`n2️⃣  Testing Predict Trend (5 years)..." -ForegroundColor Green
$trendData = @{
    country = "Australia"
    city = "Avondale Heights"
    area_m2 = 95
    property_type = "4 ROOM"
    start_year = 2024
    years_ahead = 5
} | ConvertTo-Json

try {
    $trend = Invoke-RestMethod -Uri "$baseUrl/api/predict_trend" `
        -Method POST `
        -ContentType "application/json" `
        -Body $trendData
    
    Write-Host "✅ Predict Trend OK" -ForegroundColor Green
    Write-Host "`nGrowth Rate: $($trend.growth_rate)% per year" -ForegroundColor Cyan
    Write-Host "Total Growth: $($trend.total_growth)%" -ForegroundColor Cyan
    Write-Host "`nTrend Data:"
    $trend.trend | Format-Table -AutoSize
} catch {
    Write-Host "❌ Predict Trend Failed: $_" -ForegroundColor Red
}

Write-Host "`nPress Enter for next test..."
$null = Read-Host

# Test 3: Compare Areas
Write-Host "`n3️⃣  Testing Compare Areas..." -ForegroundColor Green
$compareData = @{
    base_features = @{
        country = "Australia"
        area_m2 = 95
        property_type = "4 ROOM"
        year = 2024
        month = 6
    }
    cities = @("Avondale Heights", "Melbourne", "Sydney")
} | ConvertTo-Json -Depth 3

try {
    $compare = Invoke-RestMethod -Uri "$baseUrl/api/compare_areas" `
        -Method POST `
        -ContentType "application/json" `
        -Body $compareData
    
    Write-Host "✅ Compare Areas OK" -ForegroundColor Green
    Write-Host "`nComparisons:"
    $compare.comparisons | Format-Table -AutoSize
    Write-Host "`nCheapest: $($compare.cheapest.city) - `$$($compare.cheapest.price)" -ForegroundColor Green
    Write-Host "Most Expensive: $($compare.most_expensive.city) - `$$($compare.most_expensive.price)" -ForegroundColor Yellow
    Write-Host "Price Range: `$$($compare.price_range)" -ForegroundColor Cyan
} catch {
    Write-Host "❌ Compare Areas Failed: $_" -ForegroundColor Red
}

Write-Host "`nPress Enter for next test..."
$null = Read-Host

# Test 4: Calculate ROI
Write-Host "`n4️⃣  Testing Calculate ROI..." -ForegroundColor Green
$roiData = @{
    purchase_price = 300000
    purchase_year = 2020
    sell_year = 2025
    features = @{
        country = "Australia"
        city = "Avondale Heights"
        area_m2 = 95
        property_type = "4 ROOM"
    }
    additional_costs = 20000
    rental_income = 25000
} | ConvertTo-Json -Depth 3

try {
    $roi = Invoke-RestMethod -Uri "$baseUrl/api/calculate_roi" `
        -Method POST `
        -ContentType "application/json" `
        -Body $roiData
    
    Write-Host "✅ Calculate ROI OK" -ForegroundColor Green
    Write-Host "`nInvestment Analysis:" -ForegroundColor Cyan
    Write-Host "  Purchase Price: `$$($roi.purchase_price)"
    Write-Host "  Predicted Sell Price: `$$($roi.predicted_sell_price)"
    Write-Host "  Net Profit: `$$($roi.net_profit)" -ForegroundColor Green
    Write-Host "  ROI: $($roi.roi_percent)%" -ForegroundColor Yellow
    Write-Host "  Annualized Return: $($roi.annualized_return)%" -ForegroundColor Yellow
    Write-Host "  Holding Period: $($roi.holding_period_years) years"
    Write-Host "`n📊 Recommendation: $($roi.recommendation)" -ForegroundColor Cyan
} catch {
    Write-Host "❌ Calculate ROI Failed: $_" -ForegroundColor Red
}

Write-Host "`n" + "=" * 60
Write-Host "✅ All tests completed!" -ForegroundColor Green
Write-Host ""
Write-Host "📚 Xem thêm: enhancements\API_GUIDE.md"
Write-Host ""
