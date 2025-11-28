# 🏠 House Price Prediction - Dual Version System

## 📋 Tổng quan

Hệ thống bây giờ có **2 phiên bản riêng biệt** để bạn lựa chọn:

```
┌─────────────────────────────────────────────────────────────┐
│                     VERSION SELECTOR                         │
│                    /select (Landing Page)                    │
└──────────────┬─────────────────────────────┬────────────────┘
               │                             │
       ┌───────▼────────┐           ┌───────▼────────┐
       │  LEGACY VERSION │           │   API VERSION   │
       │    /legacy      │           │       /         │
       │   (Dataset cũ)  │           │  (Dataset mới)  │
       └─────────────────┘           └─────────────────┘
```

---

## 🔵 Version 1: LEGACY (Dataset Cũ)

### 📍 URL: `http://localhost:5000/legacy`

### 📊 Dataset:
- **Source**: Dataset cũ với features chi tiết
- **Size**: ~19,000 records
- **Market**: Chủ yếu 1 quốc gia

### ✨ Features có:
```python
{
  "country": "Vietnam",
  "city": "Ho Chi Minh City", 
  "district": "District 1",
  "area_m2": 100,
  "bedrooms": 3,          # ✅ CÓ
  "bathrooms": 2,         # ✅ CÓ
  "year_built": 2015,     # ✅ CÓ
  "floor_level": 5        # ✅ CÓ
}
```

### 🎯 Phù hợp cho:
- ✅ Dự đoán chi tiết với nhiều thông tin về BĐS
- ✅ Phân tích theo số phòng ngủ/tắm cụ thể
- ✅ Đánh giá theo tuổi BĐS (year_built)
- ✅ So sánh theo tầng lầu
- ✅ **BACKUP an toàn** - giữ nguyên dataset cũ

### ⚠️ Hạn chế:
- ❌ Dataset nhỏ hơn
- ❌ Ít quốc gia
- ❌ Không có enhanced APIs (trend, ROI, SHAP)

---

## 🟢 Version 2: API (Dataset Mới - Singapore HDB)

### 📍 URL: `http://localhost:5000/`

### 📊 Dataset:
- **Source**: `Data/cleaned_real_estate.csv`
- **Size**: **978,768 records** (50x lớn hơn!)
- **Years**: 1990-2025
- **Market**: 10+ quốc gia (Australia, Singapore, etc.)

### ✨ Features có:
```python
{
  "country": "Australia",
  "city": "Avondale Heights",
  "area_m2": 95,
  "property_type": "4 ROOM",  # ✅ HDB Classification
  "date": "2024-01",
  "year": 2024,
  "month": 1
}
```

### 📋 Property Type System (Singapore HDB):
```
1 ROOM       →  Studio flat       (~30m²)
2 ROOM       →  1BR flat          (~45m²)
3 ROOM       →  2BR flat          (~70m²)      Giá TB: $212K
4 ROOM       →  3BR flat          (~90m²)      Giá TB: $341K
5 ROOM       →  4BR flat          (~110m²)     Giá TB: $440K
EXECUTIVE    →  Luxury 5BR+       (~150m²)     Giá TB: $520K
house        →  Landed property   (varies)     Giá TB: $459K
```

### 🚀 Enhanced APIs:
1. **Trend Prediction** (`/api/predict_trend`)
   - Dự đoán 5-10 năm tương lai
   - Growth rate calculation

2. **Compare Areas** (`/api/compare_areas`)
   - So sánh giá nhiều thành phố
   - Tìm cheapest/most expensive

3. **ROI Calculator** (`/api/calculate_roi`)
   - Tính lợi nhuận đầu tư
   - Annualized return
   - Investment recommendation

4. **SHAP Explainer** (`/api/explain_prediction`)
   - Giải thích dự đoán
   - Feature importance
   - Waterfall charts

### 🎯 Phù hợp cho:
- ✅ Big data analysis (978K records)
- ✅ Multi-country comparison
- ✅ Singapore HDB market
- ✅ Trend forecasting
- ✅ Investment analysis (ROI)
- ✅ Model explainability (SHAP)

### ⚠️ Lưu ý:
- ⚠️ **KHÔNG có** bedrooms/bathrooms riêng
- ⚠️ Property_type ≠ số phòng ngủ (là loại flat)
- ⚠️ Phải chọn property_type PHÙ HỢP với area_m2

---

## 🎨 Cách sử dụng

### 1️⃣ Khởi động server:
```bash
.venv\Scripts\python.exe app.py
```

### 2️⃣ Truy cập Landing Page:
```
http://localhost:5000/select
```

### 3️⃣ Chọn phiên bản:
- Click **"LEGACY VERSION"** → Dùng dataset cũ với bedrooms/bathrooms
- Click **"API VERSION"** → Dùng dataset mới với property_type

### 4️⃣ Chuyển đổi giữa các version:
- Mỗi page có nút **"Đổi phiên bản"** ở góc trên
- Hoặc truy cập `/select` để chọn lại

---

## 📂 File Structure

```
templates/
├── version_selector.html    # 🎯 Landing page - chọn version
├── index.html               # 🟢 API Version (New)
└── legacy.html              # 🔵 Legacy Version (Old)

app.py
├── @app.route('/select')    # Version selector
├── @app.route('/')          # API version (default)
└── @app.route('/legacy')    # Legacy version

Data/
├── cleaned_real_estate.csv  # 978K records (API version)
└── [old dataset files]      # Legacy data (nếu có)
```

---

## 🔄 Routes Available

| Route | Version | Description |
|-------|---------|-------------|
| `/select` | Selector | Landing page chọn version |
| `/` | API | Default - API version mới |
| `/legacy` | Legacy | Dataset cũ với bedrooms |
| `/predict` | Both | Prediction endpoint |
| `/api/*` | API Only | Enhanced APIs (trend, ROI, etc.) |

---

## 💡 Recommendations

### Dùng LEGACY khi:
- ✅ Cần fields bedrooms/bathrooms/year_built/floor_level
- ✅ Dataset cũ đã train tốt
- ✅ Muốn backup an toàn
- ✅ Không cần features nâng cao

### Dùng API khi:
- ✅ Cần big data (978K records)
- ✅ Multi-country analysis
- ✅ Singapore HDB market
- ✅ Cần trend forecasting
- ✅ ROI calculation
- ✅ Model explainability

---

## 🔧 Technical Details

### Models:
- **Legacy**: Có thể load model khác (tùy config)
- **API**: `models/best_clean.joblib` (LightGBM, R²=0.9245)

### CORS:
- ✅ Enabled cho cả 2 versions
- ✅ Cross-origin requests work

### Enhancement APIs:
- Chỉ available trong **API Version**
- Legacy version không có `/api/*` endpoints

---

## 📊 Comparison Table

| Feature | Legacy | API |
|---------|--------|-----|
| Dataset Size | ~19K | 978K |
| Countries | 1 | 10+ |
| Bedrooms/Bathrooms | ✅ | ❌ |
| Property Type (HDB) | ❌ | ✅ |
| Year Built | ✅ | ❌ |
| Floor Level | ✅ | ❌ |
| Trend Prediction | ❌ | ✅ |
| ROI Calculator | ❌ | ✅ |
| SHAP Explainer | ❌ | ✅ |
| Compare Areas | ❌ | ✅ |

---

## 🚀 Quick Start

```bash
# 1. Start server
.venv\Scripts\python.exe app.py

# 2. Open browser
http://localhost:5000/select

# 3. Chọn version và bắt đầu!
```

---

## ⚙️ Configuration

Để thay đổi default version, edit `app.py`:

```python
@app.route('/')
def home():
    # Current: API version
    return render_template('index.html', ...)

# Để đổi sang Legacy làm default:
# return render_template('legacy.html', ...)
```

---

## 📝 Notes

1. **Banner màu sắc:**
   - 🟢 Xanh lá = API Version
   - 🟠 Cam = Legacy Version

2. **Property Type Guide:**
   - Khi dùng API version, chọn property_type PHÙ HỢP với area_m2
   - VD: 312m² → nên chọn "EXECUTIVE" hoặc "house", KHÔNG phải "4 ROOM"

3. **Backup:**
   - Legacy version = backup an toàn
   - Dataset cũ không bị mất

---

**Tạo bởi:** GitHub Copilot  
**Ngày:** 25/11/2025  
**Version:** 1.0.0
