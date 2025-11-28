# 🔧 API Configuration & Testing Guide

## 📊 Enhanced APIs Available

### 1️⃣ Health Check
**Endpoint:** `GET /api/health`

**Response:**
```json
{
  "status": "healthy",
  "model_loaded": true,
  "shap_available": false
}
```

---

### 2️⃣ Predict Trend
**Endpoint:** `POST /api/predict_trend`

**Input:**
```json
{
  "country": "Australia",
  "city": "Avondale Heights",
  "area_m2": 95,
  "property_type": "4 ROOM",
  "start_year": 2024,
  "years_ahead": 5
}
```

**Output:**
```json
{
  "trend": [
    {"year": 2024, "predicted_price": 340000},
    {"year": 2025, "predicted_price": 354200},
    {"year": 2026, "predicted_price": 368736}
  ],
  "growth_rate": 4.2,
  "total_growth": 21.0,
  "period": "2024-2029"
}
```

---

### 3️⃣ Compare Areas
**Endpoint:** `POST /api/compare_areas`

**Input:**
```json
{
  "base_features": {
    "country": "Australia",
    "area_m2": 95,
    "property_type": "4 ROOM",
    "year": 2024,
    "month": 6
  },
  "cities": ["Avondale Heights", "Melbourne", "Sydney"]
}
```

**Output:**
```json
{
  "comparisons": [
    {"city": "Sydney", "predicted_price": 450000},
    {"city": "Melbourne", "predicted_price": 380000},
    {"city": "Avondale Heights", "predicted_price": 340000}
  ],
  "cheapest": {"city": "Avondale Heights", "price": 340000},
  "most_expensive": {"city": "Sydney", "price": 450000},
  "price_range": 110000
}
```

---

### 4️⃣ Calculate ROI
**Endpoint:** `POST /api/calculate_roi`

**Input:**
```json
{
  "purchase_price": 300000,
  "purchase_year": 2020,
  "sell_year": 2025,
  "features": {
    "country": "Australia",
    "city": "Avondale Heights",
    "area_m2": 95,
    "property_type": "4 ROOM"
  },
  "additional_costs": 20000,
  "rental_income": 5000
}
```

**Output:**
```json
{
  "predicted_sell_price": 380000,
  "purchase_price": 300000,
  "net_profit": 85000,
  "roi_percent": 28.33,
  "annualized_return": 5.67,
  "holding_period_years": 5,
  "recommendation": "Good investment with 5.67% annual return"
}
```

---

### 5️⃣ Explain Prediction (SHAP)
**Endpoint:** `POST /api/explain_prediction`

**Input:**
```json
{
  "country": "Australia",
  "city": "Avondale Heights",
  "area_m2": 95,
  "property_type": "4 ROOM",
  "year": 2024,
  "month": 6
}
```

**Output:**
```json
{
  "prediction": 340000,
  "base_value": 320000,
  "contributions": {
    "area_m2": 15000,
    "city": 8000,
    "property_type": -3000,
    "year": 2000
  }
}
```

**Note:** Requires background data initialization

---

## 🧪 Testing Guide

### Method 1: Test Page (Browser)
```
1. Start server: START.bat → [2] API Version
2. Open: enhancements/test_page.html
3. Click test buttons
```

### Method 2: PowerShell (Command Line)
```powershell
# Health Check
Invoke-RestMethod -Uri http://localhost:5000/api/health -Method GET

# Predict Trend
$body = @{
    country = "Australia"
    city = "Avondale Heights"
    area_m2 = 95
    property_type = "4 ROOM"
    start_year = 2024
    years_ahead = 5
} | ConvertTo-Json

Invoke-RestMethod -Uri http://localhost:5000/api/predict_trend `
    -Method POST `
    -ContentType "application/json" `
    -Body $body

# Compare Areas
$body = @{
    base_features = @{
        country = "Australia"
        area_m2 = 95
        property_type = "4 ROOM"
        year = 2024
        month = 6
    }
    cities = @("Avondale Heights", "Melbourne")
} | ConvertTo-Json

Invoke-RestMethod -Uri http://localhost:5000/api/compare_areas `
    -Method POST `
    -ContentType "application/json" `
    -Body $body
```

### Method 3: Python Script
```python
import requests

# Health Check
response = requests.get('http://localhost:5000/api/health')
print(response.json())

# Predict Trend
data = {
    "country": "Australia",
    "city": "Avondale Heights",
    "area_m2": 95,
    "property_type": "4 ROOM",
    "start_year": 2024,
    "years_ahead": 5
}
response = requests.post('http://localhost:5000/api/predict_trend', json=data)
print(response.json())
```

---

## 🚨 Common Issues

### Issue 1: CORS Error
**Error:** `Failed to fetch`

**Solution:** 
- Flask-CORS đã được enable trong `app.py`
- Nếu vẫn lỗi, restart server

### Issue 2: Model Not Found
**Error:** `Model not loaded`

**Solution:**
- Kiểm tra `models/best_clean.joblib` exists
- Check console logs khi start server

### Issue 3: Invalid Features
**Error:** `Missing field: xxx`

**Solution:**
- Đảm bảo gửi đủ required fields
- Check API documentation trên

---

## 🎯 Feature Compatibility

| API Endpoint | Legacy Version | API Version |
|--------------|----------------|-------------|
| `/predict` | ✅ | ✅ |
| `/predict_batch` | ✅ | ✅ |
| `/api/health` | ❌ | ✅ |
| `/api/predict_trend` | ❌ | ✅ |
| `/api/compare_areas` | ❌ | ✅ |
| `/api/calculate_roi` | ❌ | ✅ |
| `/api/explain_prediction` | ❌ | ✅ |

**Enhanced APIs chỉ available trong API Version!**

---

## 📝 Integration Examples

### React/Vue Frontend
```javascript
// Predict Trend
async function predictTrend() {
  const response = await fetch('http://localhost:5000/api/predict_trend', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      country: 'Australia',
      city: 'Avondale Heights',
      area_m2: 95,
      property_type: '4 ROOM',
      start_year: 2024,
      years_ahead: 5
    })
  });
  
  const data = await response.json();
  console.log(data.trend);
}
```

### Mobile App (Flutter/React Native)
```dart
// Dart example
Future<void> compareAreas() async {
  final response = await http.post(
    Uri.parse('http://localhost:5000/api/compare_areas'),
    headers: {'Content-Type': 'application/json'},
    body: jsonEncode({
      'base_features': {
        'country': 'Australia',
        'area_m2': 95,
        'property_type': '4 ROOM',
      },
      'cities': ['Avondale Heights', 'Melbourne']
    }),
  );
  
  final data = jsonDecode(response.body);
  print(data['comparisons']);
}
```

---

## 🔐 Security Notes

### Current State:
- ❌ No authentication
- ❌ No rate limiting
- ❌ No input validation beyond basic checks

### Production Recommendations:
1. Add API keys
2. Implement rate limiting
3. Add input sanitization
4. Use HTTPS
5. Add request logging
6. Implement CORS whitelist

---

## 📊 Performance

### Response Times (Approximate):
- Health Check: ~5ms
- Predict Trend (5 years): ~50-100ms
- Compare Areas (3 cities): ~30-80ms
- Calculate ROI: ~20-40ms
- Explain Prediction: ~100-200ms (SHAP intensive)

### Optimization Tips:
1. Cache model loading
2. Use batch predictions when possible
3. Implement Redis for caching
4. Use async/await for parallel requests

---

**Last Updated:** 2025-11-25  
**Version:** 1.0.0
