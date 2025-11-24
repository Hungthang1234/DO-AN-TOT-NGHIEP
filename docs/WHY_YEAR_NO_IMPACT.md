# ⚠️ TẠI SAO GIÁ KHÔNG THAY ĐỔI KHI THAY ĐỔI NĂM?

## 📊 Phân Tích Dữ Liệu

### Vấn Đề
Khi bạn thay đổi năm từ 2021 → 2030 cho cùng một căn nhà, giá dự đoán **KHÔNG thay đổi** hoặc thay đổi rất ít.

### Nguyên Nhân

#### 1. **Dataset Chỉ Có 3 Năm Dữ Liệu** 📅
```
Year Range: 2012 - 2014 (chỉ 3 năm!)
- 2012: 20,010 records
- 2013: 16,097 records  
- 2014: 13,893 records
```

#### 2. **Correlation Rất Thấp** 📉
```
Correlation (year vs price) = -0.0572

Ý nghĩa:
  • < 0.1  → Hầu như KHÔNG có mối quan hệ
  • 0.1-0.3 → Mối quan hệ YẾU
  • > 0.3  → Có mối quan hệ
```

**→ Year correlation = -0.0572 → Gần 0 → KHÔNG có mối quan hệ!**

#### 3. **Year Chỉ Là Thông Tin Thời Gian** ⏰
Dataset này:
- ✅ Year = năm ghi nhận giao dịch
- ❌ Year ≠ năm xây dựng nhà
- ❌ Year ≠ xu hướng tăng giá qua thời gian

**Model học được:**
```
Price = f(city, area_m2, property_type, month)
Year có tác động RẤT NHỎ!
```

## 🎯 Tại Sao Model Không Học Được Trend Theo Năm?

### Dataset Không Phản Ánh Lạm Phát/Tăng Trưởng
```python
# Dataset hiện tại:
| year | city      | area_m2 | property_type | price   |
|------|-----------|---------|---------------|---------|
| 2012 | Singapore | 45      | 2 ROOM       | 250,000 |
| 2013 | Singapore | 45      | 2 ROOM       | 251,000 | ← Chỉ tăng 0.4%
| 2014 | Singapore | 45      | 2 ROOM       | 249,000 | ← Thậm chí GIẢM!
```

**→ Không có xu hướng tăng giá rõ ràng qua các năm!**

### So Sánh Với Dataset Lý Tưởng
```python
# Dataset LÝ TƯỞNG (có trend):
| year | city      | area_m2 | property_type | price   | inflation |
|------|-----------|---------|---------------|---------|-----------|
| 2012 | Singapore | 45      | 2 ROOM       | 250,000 | 2.3%      |
| 2013 | Singapore | 45      | 2 ROOM       | 265,000 | 3.1%      | ← +6%
| 2014 | Singapore | 45      | 2 ROOM       | 280,000 | 2.8%      | ← +5.7%
| 2015 | Singapore | 45      | 2 ROOM       | 295,000 | 2.5%      | ← +5.4%
...
| 2024 | Singapore | 45      | 2 ROOM       | 420,000 | 3.2%      | ← +68%
```

## ✅ Giải Pháp

### Option 1: Chấp Nhận Hiện Trạng ✅ (Khuyến Nghị)
```
✓ Model dự đoán dựa trên:
  - City (quan trọng nhất)
  - Area_m2 (tương quan 0.74!)
  - Property_type
  - Month (có ảnh hưởng nhỏ theo mùa)

✓ Year KHÔNG ảnh hưởng lớn → Giá ổn định theo năm
✓ Đây là hiện thực của dataset, không phải lỗi model
```

### Option 2: Cải Thiện Dataset 📈
Cần thêm features phản ánh time trend:

#### 2.1. Thêm Price Index
```python
# Thêm cột inflation/price index
df['price_index'] = price_indices[df['year']]  # 2012=100, 2013=103, 2014=106...
df['adjusted_price'] = df['price'] * (current_index / df['price_index'])
```

#### 2.2. Thêm Year-Based Features
```python
# Years since reference
df['years_since_2012'] = df['year'] - 2012

# Decade
df['decade'] = (df['year'] // 10) * 10  # 2010, 2020, etc.

# Economic periods
df['pre_covid'] = (df['year'] < 2020).astype(int)
df['covid_era'] = (df['year'] >= 2020) & (df['year'] <= 2022)
df['post_covid'] = (df['year'] > 2022).astype(int)
```

#### 2.3. Train Model Theo Quốc Gia
```python
# Train riêng cho từng country
for country in ['Singapore', 'Australia', 'USA']:
    model_country = train_model(df[df['country'] == country])
    # Model này sẽ học trend tốt hơn cho từng thị trường
```

### Option 3: Sử Dụng Time Series Model 📊
```python
# Thay vì Random Forest/XGBoost, dùng:
from prophet import Prophet
from statsmodels.tsa.arima.model import ARIMA

# Forecast giá based on historical trends
# Có thể dự đoán 2025-2030 dựa trên data 2012-2024
```

## 📝 Thông Báo Cho User

Đã thêm warning trong web app:
```
ℹ️ Training data: 2012-2014. Year has minimal impact on price (correlation: -0.06).
⚠️ Future year predictions are extrapolations and may be less accurate.
```

## 🎯 Kết Luận

### Hiện Tại ✅
```
✓ Model hoạt động ĐÚNG
✓ Giá không đổi theo year vì:
  → Dataset chỉ có 3 năm (2012-2014)
  → Correlation year-price ≈ 0
  → Year không phản ánh trend tăng giá
  
✓ Prediction chính xác cho các feature khác:
  → City: quan trọng
  → Area: correlation 0.74
  → Property_type: quan trọng
```

### Để Cải Thiện 📈
```
□ Thu thập data nhiều năm hơn (2012-2024)
□ Thêm price index/inflation rate
□ Train model riêng cho từng quốc gia
□ Sử dụng time series models
□ Thêm features kinh tế (GDP, interest rate)
```

---

**TÓM TẮT:** Giá không thay đổi theo năm là **ĐÚNG với dataset hiện tại**, không phải lỗi model. Year chỉ là metadata, không phản ánh xu hướng tăng giá thực tế. Model học các yếu tố khác (city, area, type) quan trọng hơn!
