"""
Analyze year impact on price predictions
"""
import pandas as pd
import numpy as np
from pathlib import Path

print("\n" + "="*70)
print("PHÂN TÍCH ẢNH HƯỞNG CỦA YEAR ĐẾN GIÁ")
print("="*70 + "\n")

# Load dataset
df = pd.read_csv('Data/cleaned_real_estate.csv', nrows=50000)

print(f"✓ Loaded {len(df):,} rows\n")
print("Columns:", list(df.columns))
print("\nYear range:", df['year'].min(), "-", df['year'].max())
print("Number of years:", df['year'].nunique())

# Analyze price by year
print("\n" + "="*70)
print("GIÁ TRUNG BÌNH THEO NĂM")
print("="*70)

yearly_stats = df.groupby('year')['price'].agg(['mean', 'median', 'std', 'count']).round(2)
yearly_stats = yearly_stats.sort_index()

print(yearly_stats.to_string())

# Check correlation
print("\n" + "="*70)
print("CORRELATION ANALYSIS")
print("="*70)

corr = df[['year', 'price', 'area_m2']].corr()
print("\n", corr)

print(f"\n📊 Correlation year vs price: {corr.loc['year', 'price']:.4f}")

if abs(corr.loc['year', 'price']) < 0.1:
    print("⚠️  CẢNH BÁO: Correlation rất thấp (<0.1) → Year hầu như KHÔNG ảnh hưởng đến giá!")
    print("   Lý do:")
    print("   1. Dataset gộp nhiều quốc gia khác nhau")
    print("   2. Có nhiều yếu tố khác quan trọng hơn (city, area_m2, property_type)")
    print("   3. Model không học được mối quan hệ year-price rõ ràng")
elif abs(corr.loc['year', 'price']) < 0.3:
    print("⚠️  Correlation thấp (0.1-0.3) → Year có ảnh hưởng NHỎ đến giá")
else:
    print("✅ Correlation OK (>0.3) → Year có ảnh hưởng đến giá")

# Check by country
print("\n" + "="*70)
print("CORRELATION THEO TỪNG QUỐC GIA")
print("="*70 + "\n")

for country in df['country'].unique():
    country_df = df[df['country'] == country]
    corr_country = country_df[['year', 'price']].corr().loc['year', 'price']
    print(f"{country:20} → Correlation: {corr_country:6.4f}")

# Sample predictions across years
print("\n" + "="*70)
print("TEST: CÙNG PROPERTY KHÁC YEAR")
print("="*70 + "\n")

# Take a sample property and change year
sample = df.iloc[0].copy()
print("Sample property:")
print(f"  Country: {sample['country']}")
print(f"  City: {sample['city']}")
print(f"  Area: {sample['area_m2']} m²")
print(f"  Property Type: {sample['property_type']}")
print(f"  Original Year: {sample['year']}, Price: ${sample['price']:,.2f}")

print("\nPrice changes over years (same property, different years):")
for year in range(2020, 2031):
    same_props = df[
        (df['city'] == sample['city']) &
        (df['area_m2'].between(sample['area_m2'] - 5, sample['area_m2'] + 5)) &
        (df['property_type'] == sample['property_type']) &
        (df['year'] == year)
    ]
    if len(same_props) > 0:
        avg_price = same_props['price'].mean()
        print(f"  Year {year}: ${avg_price:>12,.2f} ({len(same_props)} properties)")
    else:
        print(f"  Year {year}: {'No data':>12}")

# Recommendation
print("\n" + "="*70)
print("💡 KẾT LUẬN VÀ KHUYẾN NGHỊ")
print("="*70 + "\n")

if abs(df[['year', 'price']].corr().loc['year', 'price']) < 0.15:
    print("🔴 YEAR KHÔNG ẢNH HƯỞNG NHIỀU ĐẾN GIÁ trong dataset này!")
    print()
    print("Giải pháp:")
    print("1. ✅ Chấp nhận: Model dự đoán dựa trên city, area, property_type")
    print("   → Year không ảnh hưởng lớn → Giá không thay đổi nhiều theo năm")
    print()
    print("2. ✅ Thêm features: Nếu muốn year có tác động:")
    print("   - Thêm 'inflation_rate' hoặc 'price_index'")
    print("   - Train model riêng cho từng quốc gia")
    print("   - Thêm 'year_built' hoặc 'renovation_year'")
    print()
    print("3. ⚠️  Lưu ý: Dataset hiện tại year CHỈ là thông tin thời gian")
    print("   → Không phản ánh xu hướng tăng giá thực tế")
else:
    print("✅ Year có ảnh hưởng vừa phải đến giá")
    print("   Model có thể học được trend theo năm")

print("\n" + "="*70 + "\n")
