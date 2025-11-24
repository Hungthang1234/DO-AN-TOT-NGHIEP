# KẾT QUẢ TRÁNH OVERFITTING

## Ngày: 24/11/2024

## VẤN ĐỀ BAN ĐẦU

Model cũ (best.joblib):
- ✅ R² = 0.9319 (cao)
- ✅ RMSE = 46,958
- ⚠️ **KHÔNG kiểm tra overfitting** (không có train/test gap)
- ⚠️ Train trên dataset có **price_per_m2** → nghi ngờ data leakage

Model train ban đầu (train_all_models.py):
- ❌ Random Forest R² = 0.9998 (quá cao, không thực tế!)
- ❌ XGBoost R² = 0.9995
- ❌ Decision Tree R² = 0.9994
- **Nguyên nhân**: Feature `price_per_m2 = price / area_m2` 
  → Model chỉ cần nhân 2 số → Học "shortcut" không học pattern thật

## GIẢI PHÁP

### 1. Loại bỏ Data Leakage
```python
# Xóa feature price_per_m2
if 'price_per_m2' in df.columns:
    df = df.drop(columns=['price_per_m2'])
```

### 2. Anti-Overfitting Parameters

**Decision Tree:**
```python
max_depth=10           # Giới hạn độ sâu cây
min_samples_split=100  # Tối thiểu 100 mẫu để split
min_samples_leaf=50    # Tối thiểu 50 mẫu ở leaf
```

**Random Forest:**
```python
max_depth=15
min_samples_split=50
min_samples_leaf=20
max_features='sqrt'    # Chỉ dùng sqrt(n_features) cho mỗi split
```

**XGBoost:**
```python
max_depth=6
reg_alpha=1.0         # L1 regularization
reg_lambda=1.0        # L2 regularization
subsample=0.8         # 80% samples mỗi tree
colsample_bytree=0.8  # 80% features mỗi tree
```

**LightGBM:**
```python
max_depth=10
reg_alpha=0.5
reg_lambda=0.5
subsample=0.8
colsample_bytree=0.8
```

### 3. Overfitting Detection
```python
r2_gap = train_r2 - test_r2

if r2_gap > 0.05:
    status = "⚠️ OVERFIT"    # Gap > 5% → Overfit
elif r2_gap < 0.02:
    status = "✅ Good"        # Gap < 2% → Good
else:
    status = "⚙️ OK"          # Gap 2-5% → OK
```

## KẾT QUẢ MODELS CLEAN

| Model          | Test R² | Train R² | R² Gap | RMSE      | MAE       | Status   |
|----------------|---------|----------|--------|-----------|-----------|----------|
| **LightGBM** ✨ | 0.8987  | 0.9016   | 0.0029 | 44,344.56 | 31,024.98 | ✅ Good  |
| XGBoost        | 0.8908  | 0.8957   | 0.0049 | 46,046.08 | 32,010.82 | ✅ Good  |
| Decision Tree  | 0.8021  | 0.8019   |-0.0002 | 61,980.54 | 43,191.66 | ✅ Good  |
| Random Forest  | 0.7915  | 0.7933   | 0.0018 | 63,619.35 | 44,790.11 | ✅ Good  |
| Linear Reg     | 0.8045  | 0.8062   | 0.0017 | 61,570.31 | 44,158.92 | ✅ Good  |
| Ridge          | 0.8044  | 0.8061   | 0.0017 | 61,583.79 | 44,164.79 | ✅ Good  |

**👍 TẤT CẢ MODELS ĐỀU KHÔNG OVERFIT** (Gap < 0.005)

## SO SÁNH MODEL CŨ VS MỚI

### Model Cũ (best.joblib - LightGBM):
- R²: 0.9319
- RMSE: 46,958.14
- ⚠️ Không có train/test gap → Không biết có overfit không
- ⚠️ Có thể đã train trên data có leakage

### Model Mới (best_clean.joblib - LightGBM):
- Test R²: **0.8987**
- Train R²: 0.9016
- R² Gap: **0.0029** ✅
- RMSE: **44,344.56** (thấp hơn!)
- MAE: 31,024.98
- ✅ **Không có data leakage**
- ✅ **Không overfit**
- ✅ **RMSE thấp hơn model cũ**

## KẾT LUẬN

### ✅ Ưu điểm Model Clean:
1. **RMSE thấp hơn** (44,344 vs 46,958) → Dự đoán chính xác hơn
2. **R² gap rất thấp** (0.0029) → Không overfit → Generalize tốt
3. **Không data leakage** → Học pattern thật, không học shortcut
4. **Dự đoán tin cậy** trên dữ liệu mới

### ⚙️ Model cũ có R² cao hơn nhưng:
- Không biết có overfit không (không có gap)
- Có thể đã train trên data có feature gây leakage
- RMSE cao hơn → Dự đoán kém chính xác hơn

### 💡 Khuyến nghị:
**✨ Dùng `best_clean.joblib` cho production**

## CẬP NHẬT

✅ Web app đã được update: `app.py` dùng `models/best_clean.joblib`
✅ Tất cả 6 models clean đã được lưu với suffix `_clean.joblib`
✅ Logs đã được ghi vào `logs/model_training.csv`

## CÁCH CHẠY WEB

```bash
# Cách 1: Double click
START_WEB.bat

# Cách 2: Menu
MENU.bat → Chọn 1

# Cách 3: PowerShell
.venv\Scripts\python.exe app.py
```

Web sẽ chạy tại: http://127.0.0.1:5000

---

**Tóm tắt**: Model clean có **RMSE thấp hơn** và **không overfit**, dự đoán **chính xác và tin cậy hơn** model cũ. ✨
