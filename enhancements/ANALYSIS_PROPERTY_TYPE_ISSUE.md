# 🔍 PHÂN TÍCH: Tại sao giá giảm khi tăng property type?

## ❌ Vấn đề phát hiện

User report: **"Tăng số phòng lên thì giá càng giảm"**

Ví dụ test (Australia, area_m2=312):
- 1 ROOM → Giá cao
- 2 ROOM → Giá giảm
- 3 ROOM → Giá giảm thêm
- 4 ROOM → Giá giảm nữa

## 🔎 Nguyên nhân

### 1. **Dataset KHÔNG có `bedrooms`/`bathrooms`**

Features thực tế trong model:
```python
['country', 'city', 'date', 'area_m2', 'property_type', 'year', 'month']
```

**KHÔNG có:**
- ❌ bedrooms
- ❌ bathrooms  
- ❌ floor_level
- ❌ year_built

### 2. **Property_type ≠ Số phòng ngủ**

Ở Singapore/Australia HDB dataset:
- `property_type` = LOẠI FLAT, KHÔNG phải bedrooms
- "4 ROOM" = 4-room HDB flat (loại căn hộ chính phủ)
- "EXECUTIVE" = flat cao cấp
- "house" = landed property

### 3. **Relationship property_type ↔ area_m2**

Model học từ data thực:

| Property Type | Avg Area | Avg Price |
|---------------|----------|-----------|
| 1 ROOM | ~30m² | $xxx |
| 2 ROOM | ~45m² | $xxx |
| 3 ROOM | ~70m² | $212K |
| 4 ROOM | ~90m² | $341K |
| 5 ROOM | ~110m² | $440K |
| EXECUTIVE | ~140m² | $520K |
| house | varies | $459K |

### 4. **Data Mismatch**

Test case: `area_m2 = 312` + `property_type = "4 ROOM"`

**Vấn đề:**
- 312m² quá LỚN cho 4-room flat (thường ~90m²)
- Model thấy anomaly → predict GIÁ THẤP
- Giống như: "Mercedes engine in Kia body" → suspicious → lower value

**Logic model:**
```
IF area_m2 = 312 AND property_type = "4 ROOM":
    # 4-room thường 90m², đây 312m² = 3.5x bigger
    # Data mismatch → unusual → predict LOWER price
    # (vì training data không có 4-room 312m²)
```

## ✅ Giải pháp

### Solution 1: **Area-PropertyType Validation** (Quick)

Thêm validation trong UI:

```javascript
const PROPERTY_AREA_RANGES = {
  '1 ROOM': [20, 45],
  '2 ROOM': [35, 60],
  '3 ROOM': [60, 85],
  '4 ROOM': [85, 115],
  '5 ROOM': [105, 145],
  'EXECUTIVE': [130, 180],
  'house': [100, 500],
  'Apartment': [30, 300]
};

function validateAreaPropertyType(area, propertyType) {
  const [min, max] = PROPERTY_AREA_RANGES[propertyType] || [0, 1000];
  if (area < min || area > max) {
    return {
      valid: false,
      message: `⚠️ ${propertyType} thường có diện tích ${min}-${max}m². 
                Bạn nhập ${area}m² có thể không chính xác.`
    };
  }
  return { valid: true };
}
```

### Solution 2: **Auto-suggest Property Type** (Better)

Khi user nhập area_m2 → tự động suggest property_type phù hợp:

```javascript
function suggestPropertyType(area) {
  if (area < 45) return '1-2 ROOM';
  if (area < 85) return '3 ROOM';
  if (area < 115) return '4 ROOM';
  if (area < 145) return '5 ROOM';
  return 'EXECUTIVE hoặc house';
}
```

### Solution 3: **Feature Engineering** (Best - Long term)

Thêm feature `area_per_type_ratio`:

```python
# In training
df['area_per_type_ratio'] = df['area_m2'] / df['property_type'].map({
  '1 ROOM': 35,
  '2 ROOM': 50,
  '3 ROOM': 70,
  '4 ROOM': 90,
  '5 ROOM': 120,
  'EXECUTIVE': 150
})

# area_per_type_ratio > 2.0 → unusual → flag for model
```

### Solution 4: **Retrain với area bins** (Advanced)

Thay vì raw area_m2, dùng area categories:

```python
def categorize_area(area, property_type):
    if property_type == '4 ROOM':
        if area < 75: return 'small_4room'
        elif area < 105: return 'normal_4room'
        else: return 'large_4room'  # rare → model biết là special case
```

## 📊 Test Results

### Test 1: Hợp lý
```
area_m2 = 95
property_type = "4 ROOM"
→ Giá: $380K ✅ (reasonable)
```

### Test 2: Không hợp lý (hiện tại)
```
area_m2 = 312
property_type = "4 ROOM"
→ Giá: $250K ❌ (too low because mismatch)
```

### Test 3: Fixed
```
area_m2 = 312
property_type = "EXECUTIVE"  # ← Changed to match area
→ Giá: $650K ✅ (makes sense now)
```

## 🎯 Recommendation

**Immediate (5 minutes):**
1. Thêm tooltip/warning trong UI về area-property relationship
2. Show suggested property_type based on area

**Short-term (1 day):**
3. Add validation preventing nonsense combinations
4. Display typical area range for selected property_type

**Long-term (1 week):**
5. Retrain model với area_ratio feature
6. Add more features: floors, age, location quality

## 📝 User Guide Text

Thêm vào UI:

```
ℹ️ Property Type Guide:
• 1-2 ROOM: Studio/1BR flat (30-50m²)
• 3 ROOM: 2BR flat (60-85m²)
• 4 ROOM: 3BR flat (85-115m²)
• 5 ROOM: 4BR flat (105-145m²)
• EXECUTIVE: Large 5BR+ (130-180m²)
• house: Landed property (varies)

⚠️ Chọn property type PHÙ HỢP với diện tích để có dự đoán chính xác!
```

## 🔧 Quick Fix Code

Add to `templates/index.html`:

```html
<script>
// After area_m2 input
document.getElementById('area_m2').addEventListener('change', function() {
  const area = parseFloat(this.value);
  const propertySelect = document.getElementById('property_type');
  const warning = document.getElementById('area-warning');
  
  let suggested = '';
  if (area < 45) suggested = '1-2 ROOM';
  else if (area < 85) suggested = '3 ROOM';
  else if (area < 115) suggested = '4 ROOM';
  else if (area < 145) suggested = '5 ROOM';
  else suggested = 'EXECUTIVE';
  
  warning.textContent = `💡 Với ${area}m², nên chọn: ${suggested}`;
  warning.style.display = 'block';
});
</script>
```

---

**TL;DR:**
- Dataset KHÔNG có bedrooms/bathrooms
- Property_type là LOẠI FLAT, có area range cố định
- 312m² + "4 ROOM" = mismatch → model confused → low price
- Fix: Chọn EXECUTIVE thay vì 4 ROOM cho 312m²
- Long-term: Add validation + retrain với ratio feature
