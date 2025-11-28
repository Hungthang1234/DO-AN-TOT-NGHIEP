# 🚀 Launchers Folder

Thư mục chứa các file `.bat` để khởi động các phiên bản khác nhau của ứng dụng.

## 📁 Files

### `start_legacy.bat` 🔵
Khởi động **Legacy Version**
- Dataset: Cũ (bedrooms, bathrooms, year_built, floor_level)
- Records: ~19,000
- URL: `http://localhost:5000/legacy`

**Chạy:**
```bash
launchers\start_legacy.bat
```

---

### `start_api.bat` 🟢
Khởi động **API Version**
- Dataset: Mới (property_type, Singapore HDB)
- Records: 978,000
- Enhanced APIs: Trend, ROI, SHAP
- URL: `http://localhost:5000/`

**Chạy:**
```bash
launchers\start_api.bat
```

---

### `start_selector.bat` 🎯
Khởi động **Version Selector**
- Landing page để chọn version
- So sánh features
- URL: `http://localhost:5000/select`

**Chạy:**
```bash
launchers\start_selector.bat
```

---

## 💡 Khuyến nghị

### Lần đầu sử dụng:
Chạy `START.bat` (ở thư mục root) → Chọn option từ menu

### Đã biết version:
Chạy trực tiếp file tương ứng trong thư mục này

---

**See also:** `../QUICK_START.md` - Hướng dẫn chi tiết
