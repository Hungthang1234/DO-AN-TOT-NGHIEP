# 🚀 Quick Start Guide - House Price Prediction

## 🎯 Cách Khởi Động Nhanh Nhất

### **Double-click `start.bat`** ⭐

```
╔═══════════════════════════════════════════════════════════════╗
║         🏠 HOUSE PRICE PREDICTION - VERSION SELECTOR         ║
╚═══════════════════════════════════════════════════════════════╝

 Chọn phiên bản bạn muốn sử dụng:

 ┌─────────────────────────────────────────────────────────────┐
 │  [1] 🔵 LEGACY VERSION - Dataset Cũ                         │
 │      • Bedrooms, Bathrooms, Year Built, Floor Level         │
 └─────────────────────────────────────────────────────────────┘

 ┌─────────────────────────────────────────────────────────────┐
 │  [2] 🟢 EXTERNAL API VERSION - APIs Bên Ngoài               │
 │      • Singapore HDB API (FREE - data.gov.sg)               │
 │      • Real-time data fetching                              │
 └─────────────────────────────────────────────────────────────┘

 ┌─────────────────────────────────────────────────────────────┐
 │  [3] 🎯 VERSION SELECTOR - Chọn từ Web                      │
 └─────────────────────────────────────────────────────────────┘

 [0] ❌ Thoát

  Nhập lựa chọn của bạn (0-3): _
```

---

## 📁 Tất Cả Files Có Sẵn

| File | Mô tả | Dùng khi |
|------|-------|---------|
| **START.bat** | Menu chọn version (9 options) | Không biết dùng version nào |
| **start_legacy.bat** | Khởi động Legacy trực tiếp | Chắc chắn dùng Legacy |
| **start_api.bat** | Khởi động External API trực tiếp | Dùng APIs bên ngoài |
| **start_dataset.bat** | Khởi động Dataset version | Dùng Singapore HDB dataset |
| **start_selector.bat** | Mở landing page | Muốn xem comparison trước |

---

## 🔵 Option 1: LEGACY VERSION

### Khởi động:
```
Double-click: start_legacy.bat
```
Hoặc từ menu `start.bat` → chọn `[1]`

### Tự động:
- ✅ Start Flask server
- ✅ Mở browser tại: `http://localhost:5000/legacy`

### Dataset:
```python
{
  "country": "Vietnam",
  "city": "Ho Chi Minh City",
  "district": "District 1",
  "area_m2": 100,
  "bedrooms": 3,        # ✅ 
  "bathrooms": 2,       # ✅
  "year_built": 2015,   # ✅
  "floor_level": 5      # ✅
}
```

### Phù hợp:
- ✅ Cần features chi tiết (bedrooms, bathrooms, etc.)
- ✅ Dataset cũ đã train tốt
- ✅ Backup an toàn

---

## 🟢 Option 2: EXTERNAL API VERSION

### Khởi động:
```
Double-click: start_api.bat
```
Hoặc từ menu `START.bat` → chọn `[2]`

### Tự động:
- ✅ Start Flask server
- ✅ Mở browser tại: `http://localhost:5000/external_api`

### Data Source:
```
🌐 Singapore HDB API (FREE - data.gov.sg)
   • Real-time data fetching
   • No API key required
   • 978,000+ records available
   
⚠️ USA Zillow API (Requires RapidAPI key)
   • Coming soon
```

### Example Input:
```python
{
  "country": "Singapore",
  "town": "TAMPINES",
  "flat_type": "4 ROOM",
  "floor_area_sqm": 90,
  "lease_commence_date": 2000,
  "storey_range": "07 TO 09"
}
```

### Phù hợp:
- ✅ KHÔNG muốn dùng dataset local
- ✅ Muốn data real-time từ APIs
- ✅ Singapore HDB predictions (FREE)
- ✅ Dataset local KHÔNG bị ảnh hưởng

---

## 🎯 Option 3: VERSION SELECTOR

### Khởi động:
```
Double-click: start_selector.bat
```
Hoặc từ menu `start.bat` → chọn `[3]`

### Tự động:
- ✅ Start Flask server
- ✅ Mở browser tại: `http://localhost:5000/select`

### Landing Page:
- 🎨 2 cards đẹp để chọn
- 📊 Comparison table
- 🔄 Switch dễ dàng

---

## 📊 Option 9: DATASET VERSION (Singapore HDB)

### Khởi động:
```
Double-click: start_dataset.bat
```
Hoặc từ menu `START.bat` → chọn `[9]`

### Tự động:
- ✅ Start Flask server
- ✅ Mở browser tại: `http://localhost:5000/`

### Dataset:
```python
{
  "country": "Singapore",
  "city": "TAMPINES",
  "property_type": "4 ROOM",
  "floor_area_sqm": 90,
  "lease_commence_date": 2000
}
```

### Property Types:
```
3 ROOM    → ~70m²  → $212K
4 ROOM    → ~90m²  → $341K
5 ROOM    → ~110m² → $440K
EXECUTIVE → ~150m² → $520K
```

### Features:
- ✅ Big data (978K records)
- ✅ Multi-country (12 countries)
- ✅ Enhanced APIs (Trend, ROI, SHAP, Compare)
- ✅ Property type system

### Phù hợp:
- ✅ Muốn dùng dataset local (không cần API)
- ✅ Enhanced features (Trend, ROI, SHAP)
- ✅ Multi-country predictions
- ✅ Big data analysis

---

## ⚡ Workflow Thực Tế

### Lần đầu sử dụng:
```
1. Double-click start.bat
2. Nhấn [3] → Version Selector
3. Xem comparison → quyết định
4. Click card để chọn version
5. Sử dụng app
```

### Đã biết dùng version nào:
```
Legacy:       Double-click start_legacy.bat
External API: Double-click start_api.bat
Dataset:      Double-click start_dataset.bat
```

### Muốn thử cả 2:
```
1. Double-click start.bat
2. Chọn [1] → test Legacy
3. Ctrl+C dừng server
4. Menu hiện lại → chọn [2] → test API
5. Ctrl+C → chọn [0] thoát
```

---

## 🛠️ Dừng Server

### Trong terminal:
```
Ctrl + C
```

### Nếu dùng start.bat:
- Sau khi Ctrl+C
- Menu tự động hiện lại
- Chọn version khác hoặc [0] thoát

---

## 📊 So Sánh 2 Versions

| Feature | Legacy | API |
|---------|--------|-----|
| **Dataset Size** | ~19K | 978K |
| **Countries** | 1 | 10+ |
| **Bedrooms** | ✅ | ❌ |
| **Bathrooms** | ✅ | ❌ |
| **Year Built** | ✅ | ❌ |
| **Floor Level** | ✅ | ❌ |
| **Property Type** | ❌ | ✅ |
| **Trend API** | ❌ | ✅ |
| **ROI Calculator** | ❌ | ✅ |
| **SHAP Explainer** | ❌ | ✅ |

---

## 🎨 Visual Guide

### Menu trong start.bat:
```
┌─────────────────────────────┐
│  Double-click start.bat     │
└──────────────┬──────────────┘
               │
     ┌─────────▼─────────┐
     │   MENU CHỌN       │
     │  [1] [2] [3] [0]  │
     └─────────┬─────────┘
               │
       ┌───────┴───────┐
       │               │
   ┌───▼───┐       ┌───▼───┐
   │ LEGACY│       │  API  │
   └───────┘       └───────┘
```

### Direct Launch:
```
start_legacy.bat  →  /legacy  (Legacy Version)
start_api.bat     →  /        (API Version)
start_selector.bat→  /select  (Landing Page)
```

---

## ⚠️ Troubleshooting

### Port đã được sử dụng:
```powershell
# Tìm process
netstat -ano | findstr :5000

# Kill process (thay 1234 bằng PID)
taskkill /PID 1234 /F
```

### Browser không tự mở:
Tự mở browser và truy cập:
- Legacy: `http://localhost:5000/legacy`
- API: `http://localhost:5000/`
- Selector: `http://localhost:5000/select`

---

## 📝 Tips

### Cho người mới:
1. Dùng `start.bat` → chọn [3]
2. Xem comparison trên web
3. Quyết định version phù hợp

### Cho developer:
1. Dùng file direct launch (`start_legacy.bat` hoặc `start_api.bat`)
2. Test nhanh không cần menu

### Cho demo:
1. Dùng `start_selector.bat`
2. Landing page đẹp cho khách hàng xem

---

## 🎯 Recommendation

| Mục đích | Dùng file | Lý do |
|----------|-----------|-------|
| **First time** | `start.bat` → [3] | Xem comparison |
| **Development** | `start_api.bat` | Test features mới |
| **Production** | `start_legacy.bat` | Ổn định |
| **Demo** | `start_selector.bat` | Professional |

---

**Lưu ý:** Tất cả files .bat tự động:
- ✅ Khởi động Flask server
- ✅ Mở browser với URL đúng
- ✅ UTF-8 encoding (tiếng Việt)
- ✅ Màu sắc terminal đẹp

**Chỉ cần:** Double-click và chọn! 🚀
