# 🚀 HƯỚNG DẪN CHẠY WEB KHÔNG CẦN CHAT

## ✅ Cách 1: Sử dụng MENU (ĐƠN GIẢN NHẤT)

### Bước 1: Mở MENU
- Double-click file: **`MENU.bat`**

### Bước 2: Chọn chức năng
```
[1] 🚀 Khởi động Web Application
[2] ⏹️  Dừng Server
[3] 📊 Xem thông tin Model
[4] 📁 Mở thư mục dự án
[5] 🌐 Mở Web Browser
[6] 🔄 Export model metrics
[0] ❌ Thoát
```

---

## ✅ Cách 2: Double-click file BAT

### 📁 Files có sẵn:

#### 1. **START_WEB.bat**
- Double-click để khởi động server
- Tự động mở terminal
- Server chạy tại: http://localhost:5000

#### 2. **STOP_WEB.bat**
- Double-click để dừng server
- Tắt tất cả Python processes

#### 3. **VIEW_MODEL_INFO.bat**
- Double-click để xem thông tin model
- Hiển thị metrics, features, etc.

#### 4. **MENU.bat**
- Menu tổng hợp tất cả chức năng
- Giao diện đẹp, dễ sử dụng

---

## ✅ Cách 3: PowerShell / CMD

### Khởi động server:
```powershell
cd "D:\Do An Tot Nghiep - Du doan gia bat dong san bang ML va DL"
.venv\Scripts\python.exe app.py
```

### Hoặc đơn giản:
```cmd
python app.py
```

---

## 📋 Quy Trình Sử Dụng Hàng Ngày

### ☀️ Bắt đầu làm việc:
1. Double-click **`MENU.bat`**
2. Chọn `[1]` - Khởi động Web
3. Chọn `[5]` - Mở Browser
4. Truy cập: http://localhost:5000

### 🌙 Kết thúc làm việc:
1. Mở **`MENU.bat`** (hoặc đang mở rồi)
2. Chọn `[2]` - Dừng Server
3. Chọn `[0]` - Thoát

---

## 📊 Các Tính Năng Khác

### Xem thông tin Model:
- Double-click **`VIEW_MODEL_INFO.bat`**
- Hoặc qua MENU → `[3]`

### Export metrics mới:
- Qua MENU → `[6]`
- Tạo report JSON + TXT mới

### Mở folder dự án:
- Qua MENU → `[4]`
- Tự động mở Explorer

---

## 🔧 Troubleshooting

### ❌ Server không khởi động:

**Cách 1 - Qua MENU:**
```
1. Mở MENU.bat
2. Chọn [2] - Dừng Server (đảm bảo tắt hết)
3. Chọn [1] - Khởi động lại
```

**Cách 2 - Manual:**
```cmd
taskkill /F /IM python.exe
START_WEB.bat
```

### ❌ Web không mở được:

1. Kiểm tra server đang chạy:
   - Xem terminal có dòng: `Running on http://127.0.0.1:5000`

2. Thử địa chỉ khác:
   - http://localhost:5000
   - http://127.0.0.1:5000

3. Clear browser cache: `Ctrl + Shift + Delete`

### ❌ Port 5000 đã dùng:

Dừng tất cả Python:
```cmd
STOP_WEB.bat
```

Hoặc:
```cmd
taskkill /F /IM python.exe
```

---

## 📱 Shortcut Desktop (Tùy chọn)

### Tạo shortcut MENU lên Desktop:

1. Chuột phải vào **`MENU.bat`**
2. Chọn "Send to" → "Desktop (create shortcut)"
3. Đổi tên: "Dự Đoán Giá Nhà"
4. Chuột phải shortcut → Properties
5. Click "Change Icon" (tùy chọn)

Giờ chỉ cần double-click icon trên Desktop!

---

## 🎯 Tóm Tắt Nhanh

| Cần làm gì? | File nào? |
|-------------|-----------|
| Khởi động web | `START_WEB.bat` hoặc `MENU.bat` → [1] |
| Dừng server | `STOP_WEB.bat` hoặc `MENU.bat` → [2] |
| Xem model info | `VIEW_MODEL_INFO.bat` hoặc `MENU.bat` → [3] |
| Mở browser | `MENU.bat` → [5] |
| Mọi thứ | `MENU.bat` ⭐ (KHUYÊN DÙNG) |

---

## ✨ LƯU Ý QUAN TRỌNG

✅ **Model đã được lưu** - KHÔNG cần train lại  
✅ **Chỉ cần chạy START_WEB.bat** - Web hoạt động ngay  
✅ **Tất cả metrics đã có** - Xem trong MODEL_REFERENCE.txt  
✅ **Logs tự động** - Mọi prediction được ghi lại  

---

## 🎓 Tips & Tricks

### 1. Chạy nhanh từ bất kỳ đâu:
- Pin folder vào Quick Access (Windows Explorer)
- Hoặc tạo shortcut Desktop

### 2. Chạy tự động khi khởi động máy:
- Copy `MENU.bat` vào:
  `C:\Users\[YourName]\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup`

### 3. Check nhanh server có chạy không:
```cmd
netstat -ano | findstr :5000
```

Nếu có output → Server đang chạy  
Nếu không có → Server đã tắt

---

## 📞 Hỗ Trợ

Nếu gặp vấn đề:
1. Xem `logs/errors.log`
2. Check `MODEL_REFERENCE.txt`
3. Chạy `export_model_info.py` để verify

---

**🎉 Giờ bạn có thể tự chạy web mà không cần chat!**

Double-click **MENU.bat** và bắt đầu! 🚀
