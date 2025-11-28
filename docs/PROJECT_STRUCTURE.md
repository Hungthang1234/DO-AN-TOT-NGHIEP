# 📁 CẤU TRÚC DỰ ÁN

## 🎯 Tổ chức thư mục ngăn nắp theo chức năng

```
📦 Do An Tot Nghiep - Du doan gia bat dong san bang ML va DL
│
├── 📱 app.py                          # Flask web application (MAIN)
├── 📄 requirements.txt                # Python dependencies
├── 📄 model_metadata.json             # Model metadata hiện tại
├── 📄 model_metrics_report.json       # Báo cáo metrics tất cả models
├── 📄 README.md                       # README chính
├── 📄 PROJECT_STRUCTURE.md            # File này - Giải thích cấu trúc
│
├── 📂 bat_files/                      # ⭐ BAT FILES - Chạy nhanh
│   ├── MENU.bat                       # Menu tương tác chính
│   ├── START_WEB.bat                  # Khởi động web nhanh
│   ├── STOP_WEB.bat                   # Dừng server
│   └── VIEW_MODEL_INFO.bat            # Xem thông tin model
│
├── 📂 scripts/                        # Python scripts theo chức năng
│   ├── 📂 training/                   # Scripts train models
│   │   ├── train_all_models.py        # Train 9 models (có overfitting)
│   │   ├── train_models_clean.py      # Train với overfitting prevention
│   │   ├── train_quick_clean.py       # ⭐ Train 4 models quan trọng nhất
│   │   ├── train_pipeline.py          # Pipeline training cơ bản
│   │   └── train_pipeline_advanced.py # Pipeline training nâng cao
│   │
│   ├── 📂 utils/                      # Utility scripts
│   │   ├── logger_config.py           # ⭐ Logging system (ModelLogger, PredictionLogger)
│   │   ├── log_current_model.py       # Log existing models
│   │   ├── export_model_info.py       # Export model metrics to JSON/TXT
│   │   ├── view_all_models.py         # Xem tất cả models
│   │   ├── compare_models.py          # So sánh model cũ vs mới
│   │   ├── predict.py                 # Script dự đoán standalone
│   │   ├── CREATE_DESKTOP_SHORTCUT.ps1 # Tạo shortcut desktop
│   │   ├── mount_google_drive.ps1     # Mount Google Drive (Colab)
│   │   └── run_web.ps1                # PowerShell script chạy web
│   │
│   └── 📂 testing/                    # Test scripts
│       ├── test_pipeline.py           # Test training pipeline
│       ├── test_property_type.py      # Test property type feature
│       ├── test_property_type.html    # HTML test page
│       └── test_output/               # Test output files
│
├── 📂 models/                         # ⭐ Trained models (.joblib)
│   ├── best_clean.joblib              # ✨ Model tốt nhất (LightGBM clean)
│   ├── best.joblib                    # Model cũ (tham khảo)
│   ├── linear_regression_clean.joblib
│   ├── ridge_regularized_clean.joblib
│   ├── decision_tree_clean.joblib
│   ├── random_forest_clean.joblib
│   ├── xgboost_clean.joblib
│   ├── lightgbm_clean.joblib
│   └── ... (other models)
│
├── 📂 Data/                           # Datasets
│   ├── cleaned_real_estate.csv        # ⭐ Main dataset (978K rows)
│   ├── kc_house_data.csv
│   ├── melb_data.csv
│   ├── sample_features.csv
│   └── ... (other datasets)
│
├── 📂 logs/                           # ⭐ Logs từ logging system
│   ├── model_training.csv             # Training history
│   ├── predictions.csv                # Prediction logs
│   ├── analytics.csv                  # Analytics queries logs
│   └── model_logs.csv                 # Old format logs
│
├── 📂 docs/                           # 📚 Documentation
│   ├── README_QUICKSTART.md           # Hướng dẫn nhanh
│   ├── MODEL_STORAGE_README.md        # Hướng dẫn model storage
│   ├── MODEL_REFERENCE.txt            # Quick reference - Model info
│   ├── KETQUA_TRANH_OVERFITTING.md    # ⭐ Báo cáo overfitting prevention
│   ├── ANALYTICS_FIXES.md             # Analytics fixes documentation
│   ├── COMMIT_MESSAGE.txt             # Git commit messages
│   ├── model_comparison.xlsx          # Excel comparison
│   └── HUONG_DAN_CHAY_WEB.md          # Hướng dẫn chạy web (nếu có)
│
├── 📂 notebooks/                      # Jupyter Notebooks
│   ├── TrainModel.ipynb               # Training notebook
│   ├── TrainPipeline_from_py.ipynb    # Pipeline training
│   └── Train_on_Colab.ipynb           # Google Colab training
│
├── 📂 templates/                      # HTML templates (Flask)
│   ├── index.html                     # Main page
│   ├── predict.html                   # Prediction page
│   └── analytics.html                 # Analytics page
│
└── 📂 .venv/                          # Virtual environment (Python 3.14)

```

## 🚀 CÁCH SỬ DỤNG

### ⭐ Khởi động Web nhanh nhất:

**Cách 1: Double click**
```
bat_files/START_WEB.bat
```

**Cách 2: Menu tương tác**
```
bat_files/MENU.bat
→ Chọn [1] Khởi động Web Application
```

**Cách 3: PowerShell**
```powershell
.venv\Scripts\python.exe app.py
```

### 📊 Xem thông tin models:
```
bat_files/VIEW_MODEL_INFO.bat
```
Hoặc:
```
docs/MODEL_REFERENCE.txt
```

### 🔄 Train models mới:
```powershell
# Train 4 models quan trọng nhất (nhanh - 5 phút)
.venv\Scripts\python.exe scripts/training/train_quick_clean.py

# Train tất cả 9 models (lâu - 20 phút)
.venv\Scripts\python.exe scripts/training/train_models_clean.py
```

### 📈 Export model metrics:
```powershell
.venv\Scripts\python.exe scripts/utils/export_model_info.py
```

### 🔍 Xem logs:
```
logs/model_training.csv      # Training history
logs/predictions.csv         # Prediction logs
logs/analytics.csv           # Analytics logs
```

## 📝 FILES QUAN TRỌNG

### Core Application:
- `app.py` - Flask web server (MAIN)
- `models/best_clean.joblib` - Model production (LightGBM R²=0.8987)
- `scripts/utils/logger_config.py` - Logging system

### Documentation:
- `docs/KETQUA_TRANH_OVERFITTING.md` - Báo cáo overfitting prevention chi tiết
- `docs/MODEL_REFERENCE.txt` - Quick reference
- `docs/README_QUICKSTART.md` - Hướng dẫn nhanh

### BAT Files (Windows):
- `bat_files/MENU.bat` - Menu chính
- `bat_files/START_WEB.bat` - Khởi động web
- `bat_files/STOP_WEB.bat` - Dừng server

### Training Scripts:
- `scripts/training/train_quick_clean.py` - ⭐ Train nhanh 4 models
- `scripts/training/train_models_clean.py` - Train đầy đủ với overfitting prevention

## 🎯 MODEL HIỆN TẠI

**Best Model: LightGBM Clean**
- File: `models/best_clean.joblib`
- Test R²: **0.8987**
- Train R²: 0.9016
- R² Gap: **0.0029** ✅ (Không overfit!)
- RMSE: **44,344 VNĐ**
- MAE: 31,024 VNĐ
- Features: 7 features (không có price_per_m2)
- Trained: November 24, 2024

## 📊 DATASET

**Main Dataset:** `Data/cleaned_real_estate.csv`
- Rows: 978,768
- Features: city, district, area_m2, bedrooms, bathrooms, year_built, floor_level
- Target: price (VNĐ)

## 🔧 TECH STACK

- **Python**: 3.14.0
- **Framework**: Flask 3.1.2
- **ML Libraries**: 
  - scikit-learn 1.7.2
  - XGBoost 2.1.3
  - LightGBM 4.5.0
- **Data**: pandas, numpy
- **Logging**: Custom ModelLogger, PredictionLogger, AnalyticsLogger

## 📞 CONTACT

- Repository: https://github.com/Hungthang1234/DO-AN-TOT-NGHIEP
- Branch: master

---

**Last Updated:** November 24, 2024
**Version:** 2.0 (Reorganized Structure + Clean Models)
