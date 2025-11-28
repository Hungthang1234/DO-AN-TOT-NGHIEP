# 🚀 Quick Start - External APIs & Model Training

Hướng dẫn nhanh để fetch data từ external APIs và train model mới.

---

## 📋 TL;DR (Too Long; Didn't Read)

```powershell
# 1. Test fetch data (Singapore HDB - FREE)
python examples/test_fetch_data.py

# 2. Train new model
python examples/test_train_model.py

# 3. Switch active model
python examples/test_switch_model.py

# 4. Or use menu
START.bat
# Choose option [6] Train Model or [7] Switch Model
```

---

## 🎯 Method 1: Use START.bat Menu (Easiest)

1. **Run START.bat**
   ```
   START.bat
   ```

2. **Choose option [6] - TRAIN NEW MODEL**
   - Option 1: Singapore HDB (FREE, no API key)
   - Option 2: Multi-source (requires API keys)
   - Option 3: Use existing CSV

3. **Choose option [7] - SWITCH MODEL**
   - Select model from list
   - Restart Flask app

4. **Choose option [8] - ADMIN DASHBOARD**
   - Web-based model management
   - View/compare/switch models
   - Fetch data & train directly from browser

---

## 🎯 Method 2: Python Scripts

### Test 1: Fetch Data (Singapore HDB - FREE)

```python
# examples/test_fetch_data.py
from scripts.fetch_external_data import RealEstateAPIClient

client = RealEstateAPIClient()
df = client.fetch_singapore_hdb_data(year=2024, month=6)

print(f"Fetched {len(df)} records")
df.to_csv('Data/singapore_test.csv', index=False)
```

**Run:**
```powershell
python examples/test_fetch_data.py
```

**Output:**
```
Fetching Singapore HDB data for June 2024...
Fetched 1000 records
✅ Saved to Data/singapore_test.csv
```

---

### Test 2: Train Model

```python
# examples/test_train_model.py
from scripts.model_manager import ModelManager

manager = ModelManager()
model_data = manager.train_new_model(
    data_file='Data/singapore_test.csv',
    model_name='my_new_model',
    model_type='lightgbm'
)
```

**Run:**
```powershell
python examples/test_train_model.py
```

**Output:**
```
===========================================================
Training new LIGHTGBM model: my_new_model
===========================================================
Loaded 1000 records
Using features: ['country', 'city', 'area_m2', ...]

Train size: 800, Test size: 200

Training LightGBM...
[100] valid_0's rmse: 45230.5

===========================================================
Model Performance:
===========================================================
Train R²:  0.9312
Test R²:   0.8945
Train RMSE: $43,125.23
Test RMSE:  $45,230.50
Test MAE:   $32,145.67
===========================================================

✅ Model saved to: models/my_new_model.joblib
```

---

### Test 3: Switch Model

```python
# examples/test_switch_model.py
from scripts.model_manager import ModelManager

manager = ModelManager()

# List models
models = manager.list_available_models()
for model in models:
    print(f"{model['name']} - R²: {model['r2']:.4f}")

# Switch to new model
manager.set_active_model('my_new_model')
```

**Run:**
```powershell
python examples/test_switch_model.py
```

---

## 🌐 Method 3: Admin Dashboard (Web UI)

1. **Start app with admin dashboard:**
   ```powershell
   START.bat
   # Choose [8] ADMIN DASHBOARD
   ```

2. **Opens:** `http://localhost:5000/admin/models`

3. **Features:**
   - 📊 View all models with metrics
   - 🌐 Fetch external data (Singapore, Zillow, etc.)
   - 🔧 Train new model
   - ✓ Activate model
   - 📄 View detailed model info

---

## 📚 Available APIs

### 1. **Singapore HDB** (Recommended - FREE)
- **Source:** data.gov.sg
- **Cost:** FREE, no API key needed
- **Data:** ~1000 records/month
- **Features:** area_m2, property_type, city, year, month

```python
df = client.fetch_singapore_hdb_data(year=2024, month=6)
```

### 2. **Zillow** (US)
- **Source:** RapidAPI
- **Cost:** $10-50/month (free tier available)
- **Data:** US property listings
- **Features:** bedrooms, bathrooms, area, price, year_built

```python
df = client.fetch_zillow_data(
    api_key='YOUR_KEY',
    location='New York, NY',
    max_results=100
)
```

### 3. **Realty Mole** (US)
- **Source:** RapidAPI
- **Cost:** FREE tier available
- **Features:** bedrooms, bathrooms, squareFootage, assessedValue

---

## 🔧 Model Types

### LightGBM (Recommended)
- ✅ Fast training
- ✅ Good performance
- ✅ Handles missing data
- Small file size

### XGBoost
- ✅ High accuracy
- ⚠️ Slower training
- Large file size

---

## 📊 Workflow Examples

### Workflow 1: Quick Test (5 minutes)

```powershell
# 1. Fetch Singapore data
python examples/test_fetch_data.py

# 2. Train model
python examples/test_train_model.py

# 3. Switch to new model
python examples/test_switch_model.py

# 4. Restart Flask
START.bat  # Choose [2] API VERSION
```

### Workflow 2: Production Update (monthly)

```python
from scripts.fetch_external_data import RealEstateAPIClient
from scripts.model_manager import ModelManager
from datetime import datetime

# 1. Fetch latest data
client = RealEstateAPIClient()
df = client.fetch_singapore_hdb_data(
    year=datetime.now().year,
    month=datetime.now().month
)

# 2. Combine with existing data
df_old = pd.read_csv('Data/cleaned_real_estate.csv')
df_combined = pd.concat([df_old, df], ignore_index=True)
df_combined.to_csv('Data/cleaned_real_estate.csv', index=False)

# 3. Retrain model
manager = ModelManager()
model_data = manager.train_new_model(
    data_file='Data/cleaned_real_estate.csv',
    model_name=f'model_{datetime.now().strftime("%Y%m")}',
    model_type='lightgbm'
)

# 4. Activate if better
if model_data['r2'] > 0.92:
    manager.set_active_model(f'model_{datetime.now().strftime("%Y%m")}')
```

---

## ⚠️ Important Notes

### 1. API Keys
Store API keys in `config/api_keys.json` (not in git):
```json
{
  "rapidapi": {
    "key": "YOUR_KEY_HERE"
  }
}
```

### 2. Rate Limits
- Singapore HDB: Unlimited (public API)
- Zillow (Free): 100 requests/month
- Realty Mole (Free): 500 requests/month

### 3. Data Quality
Always validate data before training:
```python
print(df.isnull().sum())  # Check missing values
print(df['price'].describe())  # Check price range
df = df[(df['price'] > 10000) & (df['price'] < 10000000)]  # Remove outliers
```

### 4. Restart Required
After switching models, **restart Flask app** for changes to take effect.

---

## 🐛 Troubleshooting

**Issue:** Empty data from API
- Check internet connection
- Verify API key
- Check rate limits

**Issue:** Training fails
- Check data has 'price' column
- Remove missing values
- Ensure at least 100 records

**Issue:** Poor model performance
- Increase training data size
- Remove outliers
- Try different model_type

---

## 📖 Full Documentation

- **EXTERNAL_API_GUIDE.md** - Detailed API documentation
- **API_GUIDE.md** - Flask API endpoints
- **DUAL_VERSION_GUIDE.md** - Legacy vs API versions

---

## 🎓 Next Steps

1. ✅ Test with Singapore HDB (FREE)
2. ✅ Train first model
3. ✅ Use Admin Dashboard
4. ⏭️ Get RapidAPI key for US data
5. ⏭️ Set up monthly auto-update
6. ⏭️ Create custom data pipeline

---

**Updated:** 2024-11-25  
**Author:** House Price Prediction Team
