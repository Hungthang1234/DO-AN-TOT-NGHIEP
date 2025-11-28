# 🌍 Multi-Country Support - 12 Countries

API hiện hỗ trợ dự đoán giá bất động sản cho **12 quốc gia**:

## 🌏 Supported Countries

### 1. **Singapore** 🇸🇬
- **Cities**: 26 HDB towns
- **Examples**: ANG MO KIO, BEDOK, TAMPINES, PUNGGOL
- **Data Source**: Singapore HDB dataset (978K records)
- **Property Types**: 1 ROOM, 2 ROOM, 3 ROOM, 4 ROOM, 5 ROOM, EXECUTIVE, MULTI-GENERATION

### 2. **USA** 🇺🇸
- **Cities**: 25 major cities
- **Examples**: New York, Los Angeles, Chicago, San Francisco, Boston
- **Features**: bedrooms, bathrooms, area_m2, year_built
- **Data Source**: Zillow, Realty Mole APIs

### 3. **Australia** 🇦🇺
- **Cities**: 19 major cities
- **Examples**: Sydney, Melbourne, Brisbane, Perth, Adelaide
- **Data Source**: Domain.com.au API

### 4. **UK** 🇬🇧
- **Cities**: 20 major cities
- **Examples**: London, Manchester, Birmingham, Edinburgh, Cardiff
- **Data Source**: Zoopla API

### 5. **Canada** 🇨🇦
- **Cities**: 20 major cities
- **Examples**: Toronto, Montreal, Vancouver, Calgary, Ottawa

### 6. **Germany** 🇩🇪
- **Cities**: 20 major cities
- **Examples**: Berlin, Hamburg, Munich, Frankfurt, Cologne

### 7. **France** 🇫🇷
- **Cities**: 20 major cities
- **Examples**: Paris, Marseille, Lyon, Toulouse, Nice

### 8. **Japan** 🇯🇵
- **Cities**: 20 major cities
- **Examples**: Tokyo, Osaka, Yokohama, Kyoto, Fukuoka

### 9. **China** 🇨🇳
- **Cities**: 20 major cities
- **Examples**: Beijing, Shanghai, Guangzhou, Shenzhen, Hangzhou

### 10. **South Korea** 🇰🇷
- **Cities**: 20 major cities
- **Examples**: Seoul, Busan, Incheon, Daegu, Gwangju

### 11. **India** 🇮🇳
- **Cities**: 20 major cities
- **Examples**: Mumbai, Delhi, Bangalore, Hyderabad, Chennai

### 12. **UAE** 🇦🇪
- **Cities**: 12 major cities
- **Examples**: Dubai, Abu Dhabi, Sharjah, Ajman

---

## 📊 Total Coverage

- **12 Countries**
- **242+ Cities**
- **All major metropolitan areas**

---

## 🔌 API Usage

### Get All Countries

```http
GET /get_countries
```

**Response:**
```json
{
  "success": true,
  "countries": [
    "Singapore", "USA", "Australia", "UK", "Canada",
    "Germany", "France", "Japan", "China", "South Korea",
    "India", "UAE"
  ]
}
```

### Get Cities for Country

```http
GET /get_cities/USA
```

**Response:**
```json
{
  "success": true,
  "cities": [
    "New York", "Los Angeles", "Chicago", "Houston",
    "Phoenix", "Philadelphia", "San Antonio", "San Diego",
    "Dallas", "San Jose", "Austin", "Jacksonville",
    "Fort Worth", "Columbus", "San Francisco", "Charlotte",
    "Indianapolis", "Seattle", "Denver", "Boston",
    "Washington DC", "Nashville", "Las Vegas", "Portland", "Miami"
  ]
}
```

### Make Prediction

```http
POST /predict
Content-Type: application/json

{
  "country": "USA",
  "city": "New York",
  "area_m2": 100,
  "year": 2024,
  "month": 11,
  "bedrooms": 3,
  "bathrooms": 2,
  "year_built": 2015,
  "property_type": "Apartment"
}
```

**Response:**
```json
{
  "success": true,
  "predicted_price": 850000,
  "formatted_price": "$850,000",
  "input_data": {...}
}
```

---

## 🧪 Test Examples

### Test 1: Singapore HDB

```bash
curl -X POST http://localhost:5000/predict \
  -H "Content-Type: application/json" \
  -d '{
    "country": "Singapore",
    "city": "PUNGGOL",
    "area_m2": 93,
    "property_type": "4 ROOM",
    "year": 2024,
    "month": 11
  }'
```

### Test 2: USA Property

```bash
curl -X POST http://localhost:5000/predict \
  -H "Content-Type: application/json" \
  -d '{
    "country": "USA",
    "city": "San Francisco",
    "area_m2": 150,
    "year": 2024,
    "month": 11,
    "bedrooms": 3,
    "bathrooms": 2
  }'
```

### Test 3: UK Property

```bash
curl -X POST http://localhost:5000/predict \
  -H "Content-Type: application/json" \
  -d '{
    "country": "UK",
    "city": "London",
    "area_m2": 85,
    "year": 2024,
    "month": 11,
    "property_type": "Flat"
  }'
```

### Test 4: Japan Property

```bash
curl -X POST http://localhost:5000/predict \
  -H "Content-Type: application/json" \
  -d '{
    "country": "Japan",
    "city": "Tokyo",
    "area_m2": 60,
    "year": 2024,
    "month": 11,
    "property_type": "Apartment"
  }'
```

---

## 🌐 Web UI Support

Dashboard tự động load danh sách countries và cities:

```javascript
// Auto-populate country dropdown
fetch('/get_countries')
  .then(res => res.json())
  .then(data => {
    const select = document.getElementById('country');
    data.countries.forEach(country => {
      const option = document.createElement('option');
      option.value = country;
      option.text = country;
      select.add(option);
    });
  });

// Load cities when country changes
function loadCities(country) {
  fetch(`/get_cities/${country}`)
    .then(res => res.json())
    .then(data => {
      const select = document.getElementById('city');
      select.innerHTML = '';
      data.cities.forEach(city => {
        const option = document.createElement('option');
        option.value = city;
        option.text = city;
        select.add(option);
      });
    });
}
```

---

## 📈 Model Training for New Countries

Để thêm data cho countries mới:

### Method 1: Fetch từ APIs

```python
from scripts.fetch_external_data import RealEstateAPIClient

client = RealEstateAPIClient()

# Fetch UK data from Zoopla
uk_data = client.fetch_zoopla_data(
    api_key='YOUR_KEY',
    area='London',
    max_results=1000
)

# Train model với multi-country data
from scripts.model_manager import ModelManager
manager = ModelManager()

model = manager.train_new_model(
    data_file='Data/multi_country_data.csv',
    model_name='12_country_model',
    model_type='lightgbm'
)
```

### Method 2: Manual CSV Upload

Format CSV:
```csv
country,city,area_m2,price,year,month,property_type
UK,London,85,450000,2024,6,Flat
Germany,Berlin,95,320000,2024,6,Apartment
France,Paris,70,550000,2024,6,Apartment
```

---

## 🎯 Feature Support by Country

| Country | Area | Bedrooms | Bathrooms | Year Built | Property Type |
|---------|------|----------|-----------|------------|---------------|
| Singapore | ✅ | ❌ | ❌ | ❌ | ✅ (HDB Types) |
| USA | ✅ | ✅ | ✅ | ✅ | ✅ |
| Australia | ✅ | ✅ | ✅ | ✅ | ✅ |
| UK | ✅ | ✅ | ✅ | ✅ | ✅ |
| Canada | ✅ | ✅ | ✅ | ✅ | ✅ |
| Germany | ✅ | ✅ | ✅ | ✅ | ✅ |
| France | ✅ | ✅ | ✅ | ✅ | ✅ |
| Japan | ✅ | ✅ | ✅ | ✅ | ✅ |
| China | ✅ | ✅ | ✅ | ✅ | ✅ |
| South Korea | ✅ | ✅ | ✅ | ✅ | ✅ |
| India | ✅ | ✅ | ✅ | ✅ | ✅ |
| UAE | ✅ | ✅ | ✅ | ✅ | ✅ |

**Note:** Model tự động điều chỉnh predictions dựa trên features có sẵn cho mỗi country.

---

## 💡 Usage Tips

1. **Singapore**: Sử dụng property_type thay vì bedrooms
2. **USA/UK/Australia**: Có thể dùng đầy đủ features (bedrooms, bathrooms, year_built)
3. **Asian countries**: Focus vào area_m2 và location
4. **European countries**: Year_built quan trọng (nhiều nhà cũ)

---

## 📚 Documentation

- **API_GUIDE.md** - Complete API documentation
- **EXTERNAL_API_GUIDE.md** - How to fetch data from external APIs
- **QUICK_START_EXTERNAL_API.md** - Quick start guide

---

**Updated:** 2024-11-25  
**Version:** 2.0 - Multi-Country Support  
**Total Countries:** 12  
**Total Cities:** 242+
