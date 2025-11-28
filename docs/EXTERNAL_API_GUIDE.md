# External API Data Collection & Model Training Guide

Hướng dẫn sử dụng API bên ngoài để thu thập dữ liệu và train model mới.

## 📚 Tổng quan

System này cho phép bạn:
1. **Fetch data** từ các Real Estate APIs (Zillow, Domain.com.au, Singapore HDB, etc.)
2. **Train model mới** với data đó
3. **Switch giữa các models** khác nhau

---

## 🌐 External APIs Được Hỗ Trợ

### 1. **Singapore HDB (FREE)**
- **API:** data.gov.sg
- **Data:** Singapore HDB resale prices
- **Features:** area_m2, property_type, city, year, month
- **Cost:** FREE, không cần API key
- **Records:** ~1000 records/request

### 2. **Zillow (US) - RapidAPI**
- **API:** https://rapidapi.com/apimaker/api/zillow-com1
- **Data:** US real estate listings
- **Features:** bedrooms, bathrooms, area, price, year_built
- **Cost:** ~$10-50/month (có free tier)
- **Records:** Variable

### 3. **Realty Mole (US)**
- **API:** https://rapidapi.com/realtymole/api/realty-mole-property-api
- **Data:** US property data with tax assessments
- **Features:** bedrooms, bathrooms, squareFootage, assessedValue
- **Cost:** FREE tier available
- **Records:** ~100/request

### 4. **Zoopla (UK)**
- **API:** https://developer.zoopla.co.uk/
- **Data:** UK property listings
- **Features:** bedrooms, bathrooms, property_type, price
- **Cost:** Requires registration
- **Records:** Variable

### 5. **Domain.com.au (Australia)**
- **API:** https://developer.domain.com.au/
- **Data:** Australian property listings
- **Features:** bedrooms, bathrooms, landArea, price
- **Cost:** Requires API key
- **Records:** Variable

---

## 🚀 Quick Start

### Step 1: Fetch Data từ APIs

```python
from scripts.fetch_external_data import RealEstateAPIClient

client = RealEstateAPIClient()

# Option 1: Singapore HDB (FREE, không cần API key)
df = client.fetch_singapore_hdb_data(year=2024, month=6)
print(f"Fetched {len(df)} records")

# Option 2: Multi-source (cần API keys)
apis_config = {
    'singapore': {'year': 2024, 'month': 6},
    'zillow': {
        'api_key': 'YOUR_RAPIDAPI_KEY',
        'location': 'New York, NY',
        'max_results': 100
    },
    'realty_mole': {
        'api_key': 'YOUR_RAPIDAPI_KEY',
        'city': 'Los Angeles',
        'state': 'CA',
        'limit': 100
    }
}

combined_df = client.fetch_multi_source_data(apis_config)
# Saves to: Data/api_combined_YYYYMMDD_HHMMSS.csv
```

### Step 2: Train Model Mới

```python
from scripts.model_manager import ModelManager

manager = ModelManager()

# Train với data vừa fetch
model_data = manager.train_new_model(
    data_file='Data/api_combined_20241125_143022.csv',
    model_name='us_properties_model',
    model_type='lightgbm'  # hoặc 'xgboost'
)
```

### Step 3: Switch Active Model

```python
# Xem tất cả models
models = manager.list_available_models()
for m in models:
    print(f"{m['name']} - R²: {m['r2']:.4f}")

# Set active model
manager.set_active_model('us_properties_model')

# App sẽ tự động dùng model mới
```

---

## 📊 Chi Tiết Các APIs

### Singapore HDB API (Recommended để test)

**Ưu điểm:**
- ✅ FREE, không cần đăng ký
- ✅ Data quality cao
- ✅ ~1000 records/request
- ✅ Cập nhật hàng tháng

**Code:**
```python
client = RealEstateAPIClient()
df = client.fetch_singapore_hdb_data(year=2024, month=6)

# Features: country, city, area_m2, property_type, price, year, month
print(df.head())
```

**Output CSV Example:**
```csv
country,city,area_m2,property_type,price,year,month,date,source
Singapore,ANG MO KIO,67.0,3 ROOM,410000.0,2024,6,2024-06-01,data_gov_sg
Singapore,ANG MO KIO,68.0,3 ROOM,430000.0,2024,6,2024-06-01,data_gov_sg
```

---

### Zillow API (RapidAPI)

**Setup:**
1. Đăng ký RapidAPI: https://rapidapi.com/
2. Subscribe to Zillow API: https://rapidapi.com/apimaker/api/zillow-com1
3. Copy API key

**Code:**
```python
df = client.fetch_zillow_data(
    api_key='YOUR_RAPIDAPI_KEY',
    location='New York, NY',
    max_results=100
)

# Features: bedrooms, bathrooms, area_m2, price, year_built, property_type
```

**Pricing:**
- FREE: 100 requests/month
- Basic: $10/month - 1000 requests
- Pro: $50/month - 10000 requests

---

### Realty Mole API

**Setup:**
1. Đăng ký RapidAPI
2. Subscribe to Realty Mole: https://rapidapi.com/realtymole/api/realty-mole-property-api

**Code:**
```python
df = client.fetch_realty_mole_data(
    api_key='YOUR_RAPIDAPI_KEY',
    city='Los Angeles',
    state='CA',
    limit=100
)
```

**Ưu điểm:**
- ✅ FREE tier available
- ✅ Tax assessment data
- ✅ Detailed property info

---

## 🔧 Advanced Usage

### 1. Combine Multiple Sources

```python
apis_config = {
    'singapore': {'year': 2024, 'month': 6},
    'zillow': {
        'api_key': 'xxx',
        'location': 'San Francisco, CA',
        'max_results': 50
    },
    'domain': {
        'api_key': 'yyy',
        'suburb': 'Sydney',
        'state': 'NSW',
        'max_results': 50
    }
}

# Fetch all sources
combined_df = client.fetch_multi_source_data(apis_config)
# Auto saves to Data/api_combined_YYYYMMDD_HHMMSS.csv
```

### 2. Use Cached Data

```python
# Load cached data (if < 7 days old)
cached_df = client.load_cache('singapore_hdb', days_old=7)

if cached_df.empty:
    # Fetch fresh data
    df = client.fetch_singapore_hdb_data(2024, 6)
else:
    df = cached_df
```

### 3. Train với Custom Features

```python
# Specify which features to use
model_data = manager.train_new_model(
    data_file='Data/my_data.csv',
    model_name='custom_model',
    model_type='lightgbm',
    features=['bedrooms', 'bathrooms', 'area_m2', 'year_built', 'city']
)
```

### 4. Compare Models

```python
# Compare all models
comparison = manager.compare_models()
print(comparison)

# Output:
# Model                    Type        R²      RMSE       Features  Date
# us_properties_model      LightGBM    0.8945  $45,230    8         2024-11-25
# singapore_model          LightGBM    0.9245  $49,357    7         2024-11-20
# best_clean               LightGBM    0.9245  $49,357    7         2024-11-15
```

---

## 🎯 Workflows

### Workflow 1: Add New Country/Region Data

```python
# 1. Fetch data for new region
client = RealEstateAPIClient()
df_uk = client.fetch_zoopla_data(
    api_key='your_key',
    area='London',
    max_results=200
)

# 2. Combine with existing data
df_existing = pd.read_csv('Data/cleaned_real_estate.csv')
df_combined = pd.concat([df_existing, df_uk], ignore_index=True)
df_combined.to_csv('Data/multi_country_data.csv', index=False)

# 3. Train new model
manager = ModelManager()
model_data = manager.train_new_model(
    data_file='Data/multi_country_data.csv',
    model_name='multi_country_model',
    model_type='lightgbm'
)

# 4. Switch to new model
manager.set_active_model('multi_country_model')
```

### Workflow 2: Monthly Update

```python
import schedule
import time

def monthly_update():
    # Fetch latest data
    client = RealEstateAPIClient()
    df = client.fetch_singapore_hdb_data(
        year=datetime.now().year,
        month=datetime.now().month
    )
    
    # Append to existing data
    df_existing = pd.read_csv('Data/cleaned_real_estate.csv')
    df_updated = pd.concat([df_existing, df], ignore_index=True)
    df_updated.to_csv('Data/cleaned_real_estate.csv', index=False)
    
    # Retrain model
    manager = ModelManager()
    manager.train_new_model(
        data_file='Data/cleaned_real_estate.csv',
        model_name=f'model_{datetime.now().strftime("%Y%m")}',
        model_type='lightgbm'
    )

# Schedule monthly
schedule.every().month.at("00:00").do(monthly_update)
```

---

## 🛠️ Command Line Tools

### Fetch Data

```powershell
# Singapore HDB
python -c "from scripts.fetch_external_data import RealEstateAPIClient; c = RealEstateAPIClient(); c.fetch_singapore_hdb_data(2024, 6)"

# Zillow
python -c "from scripts.fetch_external_data import RealEstateAPIClient; c = RealEstateAPIClient(); c.fetch_zillow_data('API_KEY', 'New York, NY')"
```

### Train Model

```powershell
python -c "from scripts.model_manager import ModelManager; m = ModelManager(); m.train_new_model('Data/api_combined.csv', 'new_model', 'lightgbm')"
```

### Switch Model

```powershell
python -c "from scripts.model_manager import ModelManager; m = ModelManager(); m.set_active_model('new_model')"
```

### List Models

```powershell
python -c "from scripts.model_manager import ModelManager; m = ModelManager(); print(m.compare_models())"
```

---

## 📝 Data Format Requirements

Khi train model mới, data cần có các columns sau (minimum):

**Required:**
- `price` - Target variable (giá)

**Recommended:**
- `country` - Quốc gia
- `city` - Thành phố
- `area_m2` - Diện tích (m²)
- `property_type` hoặc `bedrooms` - Loại nhà/số phòng ngủ

**Optional:**
- `bathrooms` - Số phòng tắm
- `year_built` - Năm xây dựng
- `floor_level` - Tầng
- `year`, `month` - Thời gian
- `district` - Quận/Huyện

---

## ⚠️ Important Notes

### API Keys Security

**NEVER** commit API keys to git:

```python
# ❌ BAD
api_key = 'abc123def456'

# ✅ GOOD - Use environment variables
import os
api_key = os.getenv('RAPIDAPI_KEY')

# ✅ GOOD - Use config file (add to .gitignore)
with open('config/api_keys.json') as f:
    config = json.load(f)
    api_key = config['rapidapi_key']
```

### Rate Limits

Mỗi API có rate limits khác nhau:
- Singapore: Unlimited (public API)
- Zillow (Free): 100 req/month
- Realty Mole (Free): 500 req/month

**Tip:** Use caching để tránh duplicate requests.

### Data Quality

Luôn validate data sau khi fetch:

```python
# Check missing values
print(df.isnull().sum())

# Check data types
print(df.dtypes)

# Check price range
print(df['price'].describe())

# Remove outliers
df = df[(df['price'] > df['price'].quantile(0.01)) & 
        (df['price'] < df['price'].quantile(0.99))]
```

---

## 🔍 Troubleshooting

### Issue: API returns empty data

**Solution:**
- Check API key validity
- Check internet connection
- Verify API endpoint is still active
- Check rate limits

### Issue: Training fails with "KeyError"

**Solution:**
- Ensure all required columns exist
- Check for missing values
- Verify data types are correct

### Issue: Model performance is poor

**Solution:**
- Check data quality (outliers, missing values)
- Increase training data size
- Try different model_type ('lightgbm' vs 'xgboost')
- Tune hyperparameters

---

## 📊 Model Comparison Dashboard

Access model comparison at: `/admin/models`

```python
# Add to app.py
@app.route('/admin/models')
def models_admin():
    manager = ModelManager()
    models = manager.list_available_models()
    comparison = manager.compare_models()
    
    return render_template('admin_models.html',
                          models=models,
                          comparison=comparison.to_html())
```

---

## 🎓 Best Practices

1. **Start with Singapore HDB** (free, reliable)
2. **Cache API responses** to save costs
3. **Validate data** before training
4. **Keep old models** for rollback
5. **Monitor model performance** over time
6. **Update monthly** with fresh data
7. **Compare models** before switching
8. **Use environment variables** for API keys

---

## 📞 Support

Questions? Check:
- Singapore HDB API: https://data.gov.sg/
- RapidAPI Hub: https://rapidapi.com/hub
- GitHub Issues: [Your repo URL]

---

**Created:** 2024-11-25  
**Updated:** 2024-11-25  
**Version:** 1.0
