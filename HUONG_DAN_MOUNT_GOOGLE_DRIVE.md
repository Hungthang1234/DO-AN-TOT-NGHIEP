# 🔗 Hướng Dẫn Mount Google Drive Thành Ổ G: Trên Windows

## Phương pháp 1: Sử dụng Google Drive Desktop (Khuyên dùng - Dễ nhất)

### Bước 1: Cài đặt Google Drive Desktop
1. Download từ: https://www.google.com/drive/download/
2. Cài đặt và đăng nhập bằng tài khoản Google của bạn
3. Chọn "Mirror files" hoặc "Stream files"

### Bước 2: Thay đổi Drive Letter thành G:
1. Mở File Explorer
2. Click phải vào Google Drive (thường là ổ G: hoặc khác)
3. Nếu không phải G:, làm theo:
   - Mở **Disk Management** (Win + X → Disk Management)
   - Tìm ổ Google Drive
   - Click phải → **Change Drive Letter and Paths**
   - Click **Change** → Chọn **G:** → OK

### Bước 3: Sử dụng trong code
Sau khi mount, đường dẫn sẽ là:
```
G:\My Drive\DO-AN-TOT-NGHIEP\cleaned_real_estate.csv
```

---

## Phương pháp 2: Sử dụng rclone (Nâng cao - Linh hoạt hơn)

### Bước 1: Chạy script tự động
```powershell
# Mở PowerShell as Administrator
cd "D:\Do An Tot Nghiep - Du doan gia bat dong san bang ML va DL"
.\mount_google_drive.ps1
```

Script sẽ tự động:
- ✅ Cài đặt rclone nếu chưa có
- ✅ Hướng dẫn cấu hình Google Drive
- ✅ Mount thành ổ G:

### Bước 2: Cấu hình lần đầu
Khi chạy lần đầu, làm theo hướng dẫn:
```
1. Chọn 'n' (new remote)
2. Đặt tên: gdrive
3. Chọn Google Drive (thường là số 15)
4. Để trống client_id và client_secret
5. Chọn scope: 1 (Full access)
6. Để trống root_folder_id
7. Chọn 'n' cho advanced config
8. Chọn 'y' để auto config → Trình duyệt sẽ mở
9. Đăng nhập Google và cho phép truy cập
10. Xác nhận và thoát
```

### Bước 3: Mount (chạy mỗi khi khởi động máy)
```powershell
rclone mount gdrive: G: --vfs-cache-mode writes --vfs-cache-max-age 100h
```

### Bước 4: Unmount
```powershell
Stop-Process -Name rclone -Force
```

---

## Phương pháp 3: Sử dụng subst (Temporary - Nhanh nhất nếu đã có Google Drive Desktop)

Nếu Google Drive Desktop đã cài và mount vào ổ khác (ví dụ: C:\Users\...\Google Drive):

```powershell
# Map folder thành ổ G:
subst G: "C:\Users\ADMIN\Google Drive\My Drive"

# Kiểm tra
dir G:

# Xóa mapping
subst G: /D
```

---

## Cập nhật code để sử dụng ổ G:

### Trong train_pipeline_advanced.py:
```python
BASE_DIR = Path(r"G:\My Drive\DO-AN-TOT-NGHIEP")
DATA_PATH = BASE_DIR / "cleaned_real_estate.csv"
MODELS_DIR = BASE_DIR / "models"
LOGS_DIR = BASE_DIR / "logs"
```

### Chạy training:
```powershell
python train_pipeline_advanced.py --data "G:\My Drive\DO-AN-TOT-NGHIEP\cleaned_real_estate.csv" --sample-frac 0.1
```

---

## ⚠️ Lưu ý:

1. **Phương pháp 1 (Google Drive Desktop)**: 
   - Ưu điểm: Dễ cài đặt, tự động sync
   - Nhược điểm: Tốn dung lượng local cache (có thể chọn Stream mode để giảm)

2. **Phương pháp 2 (rclone)**:
   - Ưu điểm: Linh hoạt, không tốn dung lượng
   - Nhược điểm: Cần cấu hình lần đầu, phải chạy lại sau mỗi lần restart

3. **Phương pháp 3 (subst)**:
   - Ưu điểm: Nhanh nhất nếu đã có Google Drive Desktop
   - Nhược điểm: Temporary, mất sau khi restart

---

## Kiểm tra mount thành công:

```powershell
# Kiểm tra ổ G: có tồn tại không
Test-Path G:\

# List files
dir G:\

# Kiểm tra dung lượng
Get-PSDrive G
```

---

## Troubleshooting:

### Lỗi: "G: already exists"
```powershell
# Unmount ổ G: cũ
Stop-Process -Name rclone -Force
# Hoặc
subst G: /D
```

### Lỗi: "Access denied"
```powershell
# Chạy PowerShell as Administrator
```

### Lỗi: "rclone not found"
```powershell
# Cài rclone thủ công:
# Download: https://rclone.org/downloads/
# Extract và thêm vào PATH
```

---

## Bạn muốn tôi giúp gì tiếp theo?
- Cập nhật code để sử dụng ổ G:?
- Tạo script tự động mount khi khởi động Windows?
- Hướng dẫn sync data từ ổ D lên Google Drive?
