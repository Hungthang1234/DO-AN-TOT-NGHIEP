# 🚀 Hướng Dẫn Sử Dụng File .BAT

## 📋 Danh Sách Files

Có **4 file .bat** để khởi động ứng dụng:

### 1️⃣ `start.bat` - **MENU CHÍNH** ⭐ (Khuyên dùng)

```
Double-click start.bat
```

**Chức năng:**
- Menu interactive với 3 lựa chọn
- Chọn version trước khi khởi động
- Có thể quay lại menu sau khi dừng server

**Menu hiển thị:**
```
[1] 🔵 LEGACY VERSION - Dataset Cũ
[2] 🟢 API VERSION - Dataset Mới  
[3] 🎯 VERSION SELECTOR - Chọn từ Web
[0] ❌ Thoát
```

---

### 2️⃣ `start_legacy.bat` - LEGACY VERSION

```
Double-click start_legacy.bat
```

**Tự động:**
- ✅ Khởi động Flask server
- ✅ Mở browser tại `http://localhost:5000/legacy`
- ✅ Load Legacy Version với dataset cũ

**Dataset:**
- Bedrooms, Bathrooms, Year Built, Floor Level
- ~19,000 records
- Chi tiết đầy đủ

---

### 3️⃣ `start_api.bat` - API VERSION

```
Double-click start_api.bat
```

**Tự động:**
- ✅ Khởi động Flask server
- ✅ Mở browser tại `http://localhost:5000/`
- ✅ Load API Version với dataset mới

**Dataset:**
- Property Type (Singapore HDB)
- 978,000 records
- Enhanced APIs (Trend, ROI, SHAP)

---

### 4️⃣ `start_selector.bat` - VERSION SELECTOR

```
Double-click start_selector.bat
```

**Tự động:**
- ✅ Khởi động Flask server
- ✅ Mở browser tại `http://localhost:5000/select`
- ✅ Hiển thị landing page để chọn version

**Landing Page:**
- 2 cards đẹp để chọn Legacy hoặc API
- So sánh chi tiết features
- Bảng comparison

---

## 🎯 Workflow Khuyên Dùng

### Cách 1: Menu Interactive (Tốt nhất)
```
1. Double-click start.bat
2. Chọn [1], [2], hoặc [3]
3. Server khởi động + browser mở tự động
4. Sử dụng ứng dụng
5. Ctrl+C để dừng server
6. Menu hiện lại → chọn version khác hoặc [0] thoát
```

### Cách 2: Direct Launch
```
• start_legacy.bat → Legacy Version ngay
• start_api.bat → API Version ngay
• start_selector.bat → Landing page ngay
```

---

## 📊 So Sánh Files

| File | Tự động mở URL | Menu | Version |
|------|---------------|------|---------|
| `start.bat` | ✅ (tùy chọn) | ✅ | Chọn trong menu |
| `start_legacy.bat` | ✅ /legacy | ❌ | Legacy fixed |
| `start_api.bat` | ✅ / | ❌ | API fixed |
| `start_selector.bat` | ✅ /select | ❌ | Selector fixed |

---

## 🔧 Customization

### Thay đổi cổng (port):

Mặc định: `5000`

Để đổi sang port `8080`, edit `app.py`:
```python
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=False)
```

Và đổi trong file .bat:
```batch
start "" http://localhost:8080/legacy
```

### Thay đổi màu sắc terminal:

Trong file .bat, dòng `color XX`:
```batch
color 0A  → Xanh lá
color 0B  → Xanh dương
color 0E  → Vàng
color 0D  → Hồng
```

---

## ⚠️ Troubleshooting

### Lỗi: "python not found"
**Nguyên nhân:** Virtual environment chưa activate  
**Giải pháp:** Files .bat đã include `.venv\Scripts\python.exe`

### Lỗi: "Port 5000 already in use"
**Nguyên nhân:** Server đang chạy rồi  
**Giải pháp:**
1. Tìm terminal có server đang chạy → Ctrl+C
2. Hoặc chạy: `netstat -ano | findstr :5000` → kill process

### Browser không tự động mở
**Nguyên nhân:** `start` command bị block  
**Giải pháp:** Tự mở browser và vào:
- Legacy: `http://localhost:5000/legacy`
- API: `http://localhost:5000/`
- Selector: `http://localhost:5000/select`

### Không hiển thị tiếng Việt đúng
**Nguyên nhân:** Encoding issue  
**Giải pháp:** Files đã include `chcp 65001` để support UTF-8

---

## 🎨 Features của Menu (start.bat)

### ✅ Màu sắc:
- 🔵 Legacy = Màu vàng (0E)
- 🟢 API = Màu xanh lá (0A)
- 🎯 Selector = Màu hồng (0D)
- Menu = Màu xanh dương (0B)

### ✅ Unicode support:
- ✅ ❌ 🔵 🟢 🎯 🏠
- Box drawing: ═ ║ ╔ ╗ ╚ ╝ ┌ ┐ └ ┘

### ✅ Loop back to menu:
- Sau khi dừng server (Ctrl+C)
- Tự động quay về menu
- Chọn version khác hoặc thoát

---

## 📝 Quick Reference

| Muốn | Chạy file | URL tự động |
|------|-----------|-------------|
| Chọn trong menu | `start.bat` | Tùy chọn |
| Legacy ngay | `start_legacy.bat` | /legacy |
| API ngay | `start_api.bat` | / |
| Landing page | `start_selector.bat` | /select |

---

## 🚀 One-Click Start

**Khuyên dùng cho người mới:**
1. Double-click `start.bat`
2. Nhấn `1` (Legacy) hoặc `2` (API)
3. Enter
4. Xong! Browser tự mở ✅

**Khuyên dùng cho dev:**
1. Double-click file tương ứng với version cần test
2. Server start ngay
3. Không cần chọn menu

---

**Tạo bởi:** GitHub Copilot  
**Ngày:** 25/11/2025  
**Version:** 1.0.0
