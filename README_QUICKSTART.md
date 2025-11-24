# 🏠 DỰ ÁN DỰ ĐOÁN GIÁ BẤT ĐỘNG SẢN

## 🚀 CÁCH CHẠY NHANH NHẤT

### ⚡ Cách 1: Double-click MENU.bat (KHUYÊN DÙNG)
```
1. Double-click file: MENU.bat
2. Chọn [1] - Khởi động Web
3. Chọn [5] - Mở Browser
4. Truy cập: http://localhost:5000
```

### ⚡ Cách 2: Double-click START_WEB.bat
```
1. Double-click: START_WEB.bat
2. Đợi server khởi động
3. Mở browser: http://localhost:5000
```

---

## 📁 CẤU TRÚC THỨ MỤC

### 🔥 Files QUAN TRỌNG (để chạy web):

```
MENU.bat                    ⭐ Menu tổng hợp - CHẠY FILE NÀY
START_WEB.bat              🚀 Khởi động server
STOP_WEB.bat               ⏹️  Dừng server
VIEW_MODEL_INFO.bat        📊 Xem thông tin model

app.py                     🌐 Flask web application
models/best.joblib         🤖 Model đã train (LightGBM)
model_metadata.json        📝 Thông tin model
MODEL_REFERENCE.txt        📄 Tham khảo nhanh

templates/index.html       🎨 Giao diện web
Data/cleaned_real_estate.csv  💾 Dữ liệu
```

### 📚 Files HỖ TRỢ:

```
export_model_info.py       🔄 Export metrics
log_current_model.py       📋 Log model vào hệ thống
logger_config.py           🔧 Logging configuration

logs/                      📊 Thư mục logs
  ├─ model_training.csv    - Training history
  ├─ predictions.csv       - Prediction history
  └─ analytics.csv         - Analytics queries

HUONG_DAN_CHAY_WEB.md     📖 Hướng dẫn chi tiết
MODEL_STORAGE_README.md    📖 Hướng dẫn logging
HUONG_DAN_SU_DUNG.txt     📖 Hướng dẫn người dùng
```

---

## 🎯 TÍNH NĂNG CHÍNH

### 1️⃣ **Single Prediction** (Dự đoán đơn)
- Nhập thông tin: Country, City, Year, Month, Area, Property Type
- Nhận kết quả: Giá dự đoán
- Auto-log prediction

### 2️⃣ **Batch Prediction** (Dự đoán hàng loạt)
- Upload file CSV
- Dự đoán hàng loạt
- Download kết quả

### 3️⃣ **Data Analytics** (Phân tích dữ liệu)
- 9 biểu đồ:
  - Price by Country
  - Price Distribution
  - Property Type Distribution
  - Price Trends Over Time
  - Price by City (Top 15)
  - Area vs Price Scatter
  - Monthly Trends (NEW)
  - City Heatmap (NEW)
  - Cumulative Growth (NEW)

- Advanced Filters:
  - Country filter
  - Year range filter
  - Property type filter
  - Price range filter

- 10 Statistics Cards:
  - Total Records
  - Average Price
  - Median Price
  - Min/Max Price
  - Total Cities/Countries
  - Year Range
  - Average Area
  - Price Std Dev
  - Property Type Count

### 4️⃣ **About** (Thông tin)
- Model information
- Features used
- Performance metrics
- Dataset info

---

## 📊 THÔNG TIN MODEL

**Model:** LightGBM  
**RMSE:** 46,958.14  
**R² Score:** 0.9319  
**MAE:** 0.00  

**Features (7):**
1. country
2. city
3. date
4. area_m2
5. property_type
6. year
7. month

**Dataset:**
- File: cleaned_real_estate.csv
- Records: 978,768
- Countries: 3 (Singapore, USA, Australia)

---

## 🛠️ YÊU CẦU HỆ THỐNG

✅ **Windows 10/11**  
✅ **Python 3.14** (đã cài trong .venv)  
✅ **Đã có sẵn:**
- Flask 3.1.2
- LightGBM
- scikit-learn
- pandas, numpy
- joblib

**Không cần cài thêm gì!** Chỉ cần double-click MENU.bat!

---

## 📖 HƯỚNG DẪN SỬ DỤNG

### 🟢 Khởi động lần đầu:

1. **Mở MENU:**
   ```
   Double-click: MENU.bat
   ```

2. **Khởi động Web:**
   ```
   Chọn [1] - Khởi động Web Application
   ```

3. **Mở Browser:**
   ```
   Chọn [5] - Mở Web Browser
   hoặc truy cập: http://localhost:5000
   ```

4. **Bắt đầu sử dụng!**

### 🔴 Dừng server:

```
MENU → [2] - Dừng Server
hoặc
Double-click: STOP_WEB.bat
```

### 📊 Xem thông tin Model:

```
MENU → [3] - Xem thông tin Model
hoặc
Double-click: VIEW_MODEL_INFO.bat
```

---

## 🎓 TIPS & TRICKS

### ⚡ Chạy nhanh hơn:

**Tạo Shortcut Desktop:**
```powershell
Double-click: CREATE_DESKTOP_SHORTCUT.ps1
```
→ Tạo icon "Dự Đoán Giá Nhà" trên Desktop

### 🔍 Check server đang chạy:

**Cách 1:** Xem terminal có dòng:
```
* Running on http://127.0.0.1:5000
```

**Cách 2:** Chạy lệnh:
```cmd
netstat -ano | findstr :5000
```

### 🔄 Nếu server bị lỗi:

```
1. STOP_WEB.bat (dừng hẳn)
2. START_WEB.bat (khởi động lại)
```

---

## 📦 BACKUP & RESTORE

### Backup (sao lưu):
Copy các folder/files:
```
models/
logs/
model_metadata.json
model_metrics_report.json
Data/cleaned_real_estate.csv
```

### Restore (khôi phục):
1. Copy lại các files trên
2. Double-click MENU.bat
3. Chọn [1] - Khởi động
4. Done!

---

## 🔧 TROUBLESHOOTING

### ❌ "localhost refused to connect"

**Giải pháp:**
```
1. STOP_WEB.bat (đảm bảo tắt hẳn)
2. START_WEB.bat (khởi động lại)
3. Đợi 3-5 giây
4. Refresh browser (F5)
```

### ❌ "Port 5000 already in use"

**Giải pháp:**
```cmd
taskkill /F /IM python.exe
START_WEB.bat
```

### ❌ Model không load

**Giải pháp:**
```
1. Check file models/best.joblib có tồn tại?
2. Check model_metadata.json có tồn tại?
3. Nếu không: python export_model_info.py
```

### ❌ Server tự tắt

**Nguyên nhân:** Exit Code 1 → Có lỗi Python

**Giải pháp:**
```
1. Xem logs/errors.log
2. Check terminal output khi khởi động
3. Đảm bảo .venv/Scripts/python.exe hoạt động
```

---

## 📞 HỖ TRỢ & TÀI LIỆU

### 📖 Đọc thêm:
- **HUONG_DAN_CHAY_WEB.md** - Hướng dẫn chi tiết chạy web
- **MODEL_STORAGE_README.md** - Hướng dẫn hệ thống logging
- **HUONG_DAN_SU_DUNG.txt** - Hướng dẫn người dùng cuối

### 🔍 Files log:
- `logs/errors.log` - Lỗi hệ thống
- `logs/model_training.csv` - Lịch sử training
- `logs/predictions.csv` - Lịch sử predictions
- `logs/analytics.csv` - Lịch sử queries

### 📊 Files thông tin:
- `MODEL_REFERENCE.txt` - Tham khảo nhanh model
- `model_metrics_report.json` - Báo cáo chi tiết
- `model_metadata.json` - Metadata model

---

## 🎯 WORKFLOW HÀNG NGÀY

### ☀️ Bắt đầu ngày:
```
1. Double-click MENU.bat
2. Chọn [1] - Khởi động Web
3. Chọn [5] - Mở Browser
4. Làm việc...
```

### 🌙 Kết thúc ngày:
```
1. Mở MENU.bat (nếu đã đóng)
2. Chọn [2] - Dừng Server
3. Chọn [0] - Thoát
```

---

## 💾 LƯU Ý QUAN TRỌNG

✅ **Model đã được train và lưu** - Không cần train lại  
✅ **Chỉ cần chạy MENU.bat** - Web hoạt động ngay  
✅ **Tất cả metrics đã được lưu** - Xem MODEL_REFERENCE.txt  
✅ **Logging tự động** - Mọi prediction được ghi lại  
✅ **Không cần Internet** - Chạy offline hoàn toàn  

---

## 🏆 THÀNH TÍCH MODEL

| Metric | Value | Ý nghĩa |
|--------|-------|---------|
| **R² Score** | 0.9319 | Model giải thích được 93.19% variance |
| **RMSE** | 46,958.14 | Sai số trung bình ~47K |
| **Features** | 7 | Đơn giản, hiệu quả |
| **Training Data** | 978,768 | Dataset lớn, đa dạng |

---

## 🚀 PHÁT TRIỂN THÊM

### Nếu muốn train lại model:
```bash
python train_pipeline.py
# hoặc
python train_pipeline_advanced.py
```

### Nếu muốn thêm model mới:
```python
# Sau khi train
python log_current_model.py --best
python export_model_info.py
```

### Nếu muốn xem logs chi tiết:
```
Browser: http://localhost:5000/logs?type=summary
```

---

## 📧 LIÊN HỆ

**Dự án:** Dự đoán giá bất động sản  
**Công nghệ:** Machine Learning (LightGBM)  
**Framework:** Flask + JavaScript  
**Repository:** DO-AN-TOT-NGHIEP  

---

## 🎉 BẮT ĐẦU NGAY!

```
Double-click: MENU.bat
Chọn [1]
Enjoy! 🚀
```

**Không cần chat, không cần code, chỉ cần click!** ✨
