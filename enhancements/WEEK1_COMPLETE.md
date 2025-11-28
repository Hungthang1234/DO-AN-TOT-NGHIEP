# 📅 TUẦN 1 HOÀN TẤT - Cải thiện Model ML

## ✅ Đã implement (3 tính năng chính)

### 1. 🤖 Ensemble Stacking Model
**File:** `enhancements/models/ensemble_stacking.py`

**Mô tả:**
- Kết hợp LightGBM + XGBoost với Ridge meta-learner
- K-Fold Cross-Validation (5 folds) để tránh overfitting
- Target: Tăng R² từ 0.9245 → 0.94+

**Cách sử dụng:**
```python
from enhancements.models.ensemble_stacking import train_ensemble_model

# Train ensemble model
ensemble, test_r2, test_rmse = train_ensemble_model(
    data_path='Data/cleaned_real_estate.csv',
    output_path='models/ensemble_stacking.joblib'
)
```

**Chạy trực tiếp:**
```bash
.venv\Scripts\python.exe enhancements\models\ensemble_stacking.py
```

---

### 2. 🔧 Feature Engineering
**File:** `enhancements/features/feature_engineering.py`

**Features mới:**
- `distance_to_center_km` - Khoảng cách đến trung tâm thành phố
- `nearby_schools` - Số trường học gần đó
- `nearby_hospitals` - Số bệnh viện gần đó
- `property_age` - Tuổi nhà
- `price_growth_rate` - Tỷ lệ tăng trưởng giá theo năm
- `area_per_room` - Diện tích trung bình mỗi phòng
- `luxury_score` - Điểm sang trọng

**Cách sử dụng:**
```python
from enhancements.features.feature_engineering import FeatureEngineer

engineer = FeatureEngineer()
df_enhanced = engineer.engineer_all_features(df, fit=True)
```

**Chạy trực tiếp:**
```bash
.venv\Scripts\python.exe enhancements\features\feature_engineering.py
```

---

### 3. 📊 SHAP Explainability
**File:** `enhancements/models/shap_explainer.py`

**Mô tả:**
- Giải thích tại sao model dự đoán giá đó
- Hiển thị contribution của từng feature
- Hỗ trợ waterfall plot & force plot

**Cách sử dụng:**
```python
from enhancements.models.shap_explainer import explain_single_prediction

explanation = explain_single_prediction(
    model_path='models/lightgbm_full_dataset.joblib',
    X_input={
        'country': 'Vietnam',
        'city': 'Ho Chi Minh City',
        'area_m2': 100,
        'property_type': 'Apartment',
        'year': 2024
    }
)

print(f"Predicted: ${explanation['prediction']:,.2f}")
for feat in explanation['features'][:5]:
    print(f"  {feat['name']}: {feat['contribution']:+,.2f}")
```

---

## 🌐 API Endpoints mới

**File:** `enhancements/api/endpoints.py`

### 1. `/api/predict_trend` - Dự đoán xu hướng giá
```bash
POST http://localhost:5000/api/predict_trend

Body:
{
  "country": "Vietnam",
  "city": "Ho Chi Minh City",
  "area_m2": 100,
  "property_type": "Apartment",
  "start_year": 2024,
  "years_ahead": 5
}

Response:
{
  "trend": [
    {"year": 2024, "predicted_price": 500000},
    {"year": 2025, "predicted_price": 520000},
    ...
  ],
  "growth_rate": 4.2,
  "total_growth": 21.0
}
```

### 2. `/api/compare_areas` - So sánh giá nhiều khu vực
```bash
POST http://localhost:5000/api/compare_areas

Body:
{
  "base_features": {
    "country": "Vietnam",
    "area_m2": 100,
    "property_type": "Apartment",
    "year": 2024
  },
  "cities": ["Ho Chi Minh City", "Hanoi", "Da Nang"]
}

Response:
{
  "comparisons": [
    {"city": "Ho Chi Minh City", "price": 500000, "rank": 1},
    {"city": "Hanoi", "price": 450000, "rank": 2},
    {"city": "Da Nang", "price": 350000, "rank": 3}
  ],
  "price_range": {"min": 350000, "max": 500000, "difference": 150000}
}
```

### 3. `/api/calculate_roi` - Tính ROI đầu tư
```bash
POST http://localhost:5000/api/calculate_roi

Body:
{
  "purchase_price": 500000,
  "purchase_year": 2024,
  "sell_year": 2029,
  "features": {
    "country": "Vietnam",
    "city": "Ho Chi Minh City",
    "area_m2": 100,
    "property_type": "Apartment"
  },
  "additional_costs": 50000,
  "rental_income_per_year": 30000
}

Response:
{
  "net_profit": 225000,
  "roi_percent": 45.0,
  "annualized_return": 9.0,
  "recommendation": "Good investment"
}
```

### 4. `/api/explain_prediction` - SHAP explanation
```bash
POST http://localhost:5000/api/explain_prediction

Body:
{
  "country": "Vietnam",
  "city": "Ho Chi Minh City",
  "area_m2": 100,
  "property_type": "Apartment",
  "year": 2024
}

Response:
{
  "prediction": 500000,
  "features": [
    {"name": "city", "value": "Ho Chi Minh City", "contribution": 80000},
    {"name": "area_m2", "value": 100, "contribution": 50000}
  ]
}
```

---

## 🧪 Testing

**Test API endpoints:**
```bash
# Chạy server
.venv\Scripts\python.exe app.py

# Trong terminal khác:
.venv\Scripts\python.exe enhancements\test_api.py
```

---

## 📦 Dependencies mới

Đã cài đặt:
- ✅ `shap` - SHAP explainability
- ✅ `geopy` - Tính khoảng cách địa lý
- ✅ `matplotlib` - Vẽ biểu đồ
- ❌ `catboost` - Bỏ qua (cần Visual Studio)

---

## 📈 Performance

| Model | R² Score | RMSE | Features |
|-------|----------|------|----------|
| LightGBM (single) | 0.9245 | 49,357 | 7 |
| **Ensemble Stacking** | **TBD** | **TBD** | 7+ |

---

## 🚀 Cách chạy

1. **Khởi động server:**
```bash
.venv\Scripts\python.exe app.py
```

2. **Test API mới:**
```bash
.venv\Scripts\python.exe enhancements\test_api.py
```

3. **Train ensemble model:**
```bash
.venv\Scripts\python.exe enhancements\models\ensemble_stacking.py
```

4. **Apply feature engineering:**
```bash
.venv\Scripts\python.exe enhancements\features\feature_engineering.py
```

---

## 📝 Next Steps (Tuần 2-4)

### Tuần 2: Tính năng dự đoán nâng cao
- [ ] Tích hợp API vào UI
- [ ] Thêm biểu đồ Chart.js cho trend
- [ ] Comparison table với sort/filter

### Tuần 3: Mở rộng dữ liệu
- [ ] Web scraping Batdongsan.com.vn
- [ ] External API (GDP, exchange rate)
- [ ] Cron job tự động update data

### Tuần 4: Mở rộng thị trường
- [ ] Multi-language (i18n)
- [ ] Multi-country support
- [ ] Currency conversion

---

## 🎯 KẾT QUẢ TUẦN 1

✅ **3/3 tính năng core hoàn thành**
✅ **4 API endpoints mới**
✅ **Feature engineering framework**
✅ **SHAP explainability**
✅ **Documentation đầy đủ**

**Thời gian:** ~3-4 tiếng
**Code lines:** ~1,500 lines
**Files created:** 7 files

---

## 📧 Contact

Nếu có vấn đề, check:
1. Server đang chạy? `http://localhost:5000/api/health`
2. Model đã load? Check console output
3. Dependencies đã cài? `pip list | findstr shap`

**Happy coding! 🚀**
