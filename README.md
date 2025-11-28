# 🏠 House Price Prediction - ML & DL Application

Ứng dụng web dự đoán giá bất động sản sử dụng Machine Learning và Deep Learning với Flask framework.

## 📁 Cấu Trúc Project

```
├── app.py                      # Flask web application
├── requirements.txt            # Python dependencies
│
├── 📁 bat_files/              # Windows batch launchers (start.bat, MENU.bat)
├── 📁 config/                 # Configuration files (model_metadata.json)
├── 📁 Data/                   # Datasets (cleaned_real_estate.csv - 978K records)
├── 📁 docs/                   # Documentation (QUICK_START.md, guides...)
├── 📁 enhancements/           # API enhancements (advanced_charts_api.py)
├── 📁 examples/               # Example code và demos
├── 📁 launchers/              # Python launcher scripts
├── 📁 logs/                   # Application logs
├── 📁 models/                 # Trained ML models (29+ models)
├── 📁 notebooks/              # Jupyter notebooks
├── 📁 scripts/                # Utility scripts (external_api_predictor.py)
├── 📁 templates/              # HTML templates (index.html)
├── 📁 tests/                  # Test files
└── 📁 utils/                  # Utility functions
```

## 🎯 Tính Năng Chính

- **🏠 Dự đoán giá BĐS** - Sử dụng dataset 978K records với 29+ ML models
- **🌐 External API Mode** - Kết nối Singapore HDB API (FREE)
- **📊 Advanced Charts** - 7 biểu đồ interactive với 10 API endpoints
- **🤖 Model Management** - Switch models, compare performance
- **🔧 Admin Dashboard** - Training logs, model comparison
- **🌍 Multi-country** - 12 quốc gia, 242+ thành phố

## 🚀 Quick Start

### 1. Cài Đặt

```powershell
# Clone repository
git clone https://github.com/Hungthang1234/DO-AN-TOT-NGHIEP.git

# Tạo virtual environment
python -m venv .venv
.\.venv\Scripts\Activate.ps1

# Cài đặt dependencies
pip install -r requirements.txt
```

### 2. Chạy Ứng Dụng

**Cách 1: Sử dụng Batch File (Windows - Khuyến nghị)**
```cmd
cd bat_files
MENU.bat
```

**Cách 2: Quick Start**
```cmd
cd bat_files
start.bat
```

**Cách 3: Chạy trực tiếp**
```powershell
python app.py
```

Sau đó mở: **http://127.0.0.1:5000**

### 3. Sử Dụng Web Interface

1. **Chọn Mode**:
   - Dataset Mode (Option 1) - Dự đoán với dataset 978K records
   - External API Mode (Option 2) - Dùng Singapore HDB API

2. **Nhập thông tin BĐS**:
   - Country, City
   - Area (m²)
   - Property Type
   - Year

3. **Nhận kết quả**:
   - Predicted Price
   - Confidence Interval (95% CI)
   - Market Statistics

### 4. Advanced Charts

1. Click tab **"Advanced Visualization"**
2. Chọn filters:
   - Country: All / Singapore / USA / Australia
   - Year Range: 5 / 10 / 15 / All years
3. Click **"Update Charts"**
4. Xem 7 biểu đồ interactive

## 📊 Advanced Charts Feature

### 10 API Endpoints

```bash
GET /api/charts/overview              # Statistics overview
GET /api/charts/price-trend           # Price trends
GET /api/charts/property-type-distribution
GET /api/charts/price-range-distribution
GET /api/charts/area-distribution
GET /api/charts/seasonal-patterns
GET /api/charts/top-cities
GET /api/charts/price-by-type-trend
GET /api/charts/countries
GET /api/charts/price-heatmap
```

### 7 Interactive Charts

1. **Monthly Price Trend** - Line chart (avg vs median)
2. **Property Price by Type** - Bar chart (top 10 types)
3. **Price Range Distribution** - Doughnut chart (5 ranges)
4. **Area Distribution** - Bar chart (5 ranges)
5. **Seasonal Patterns** - Radar chart (12 months)
6. **Top Cities** - Horizontal bar (top 15 cities)
7. **Price by Type Trend** - Multi-line chart (top 5 types)

## 🧪 Testing

```powershell
# Test dataset
python tests/test_charts_api.py

# Test API endpoints (server phải chạy)
python tests/test_api_direct.py
```

## 📚 Documentation

Xem thư mục **docs/** cho tài liệu chi tiết:

- `QUICK_START.md` - Hướng dẫn bắt đầu
- `ADVANCED_CHARTS_COMPLETE.md` - Advanced Charts guide
- `EXTERNAL_API_COMPLETE.md` - External API guide  
- `MULTI_COUNTRY_COMPLETE.md` - Multi-country support
- `PROJECT_STRUCTURE.md` - Project structure

## 🔧 Configuration

### Model Config (`config/model_metadata.json`)
```json
{
  "model_name": "LightGBM (Full Dataset)",
  "rmse": 49357.73,
  "r2_score": 0.9245
}
```

### Dataset Info
- **File**: `Data/cleaned_real_estate.csv`
- **Records**: 978,768
- **Countries**: 3 (Singapore, USA, Australia)
- **Property Types**: 12
- **Years**: 1990-2025

## 📦 Tech Stack

- **Backend**: Flask 3.1.2, Python 3.14
- **ML**: scikit-learn, LightGBM, XGBoost
- **Data**: pandas 2.3.3, numpy
- **Frontend**: HTML, CSS, JavaScript, Chart.js
- **API**: RESTful APIs with JSON

## 🛠️ Development

### Add New Model
```python
import joblib
joblib.dump(model, 'models/new_model.joblib')
# Update config/model_metadata.json
```

### Add API Endpoint
```python
# Create file in enhancements/
# Register blueprint in app.py
```

## 📝 Notes

- Dataset `Data/cleaned_real_estate.csv` must exist
- Python 3.8+ required
- Works on Windows (tested with PowerShell)
- For large datasets, use sampling for quick tests

## 📧 Contact

- **Repository**: https://github.com/Hungthang1234/DO-AN-TOT-NGHIEP
- **Issues**: https://github.com/Hungthang1234/DO-AN-TOT-NGHIEP/issues

---

**Version**: 2.0 | **Last Updated**: Nov 27, 2025 | **Advanced Charts Release** 🎉
