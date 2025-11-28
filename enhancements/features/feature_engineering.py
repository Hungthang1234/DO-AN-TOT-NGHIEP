"""
Feature Engineering - Tạo features nâng cao cho model
Thêm: distance_to_center, nearby_schools, nearby_hospitals, price_growth_rate
"""

import pandas as pd
import numpy as np
from pathlib import Path
from geopy.distance import geodesic
import warnings
warnings.filterwarnings('ignore')


# Static data - Coordinates của trung tâm thành phố
CITY_CENTERS = {
    'Ho Chi Minh City': (10.8231, 106.6297),
    'Hanoi': (21.0285, 105.8542),
    'Da Nang': (16.0544, 108.2022),
    'Can Tho': (10.0452, 105.7469),
    'Hai Phong': (20.8449, 106.6881),
    'Bien Hoa': (10.9500, 106.8167),
    'Nha Trang': (12.2388, 109.1967),
    'Hue': (16.4637, 107.5909),
    'Vung Tau': (10.3460, 107.0843),
    'Buon Ma Thuot': (12.6672, 108.0378),
}

# Static data - Số lượng trường học theo quận (ước tính)
DISTRICT_SCHOOLS = {
    'District 1': 25,
    'District 2': 18,
    'District 3': 22,
    'District 4': 15,
    'District 5': 20,
    'District 6': 16,
    'District 7': 30,
    'District 8': 14,
    'District 9': 20,
    'District 10': 18,
    'District 11': 17,
    'District 12': 22,
    'Binh Thanh': 24,
    'Go Vap': 26,
    'Phu Nhuan': 19,
    'Tan Binh': 28,
    'Tan Phu': 21,
    'Thu Duc': 35,
    'Binh Tan': 23,
    'Binh Chanh': 18,
    'Hoc Mon': 16,
    'Cu Chi': 12,
    'Nha Be': 10,
    'Can Gio': 8,
}

# Static data - Số bệnh viện theo quận
DISTRICT_HOSPITALS = {
    'District 1': 12,
    'District 2': 5,
    'District 3': 8,
    'District 4': 4,
    'District 5': 7,
    'District 6': 5,
    'District 7': 6,
    'District 8': 3,
    'District 9': 4,
    'District 10': 6,
    'District 11': 5,
    'District 12': 4,
    'Binh Thanh': 9,
    'Go Vap': 7,
    'Phu Nhuan': 6,
    'Tan Binh': 8,
    'Tan Phu': 5,
    'Thu Duc': 10,
    'Binh Tan': 4,
    'Binh Chanh': 3,
    'Hoc Mon': 2,
    'Cu Chi': 2,
    'Nha Be': 1,
    'Can Gio': 1,
}


class FeatureEngineer:
    """Feature engineering utilities"""
    
    def __init__(self):
        self.fitted = False
        self.yearly_growth_rate = {}
        
    def add_distance_to_center(self, df):
        """
        Thêm feature: khoảng cách đến trung tâm thành phố
        Nếu không có coordinates, dùng district-based estimate
        """
        df = df.copy()
        
        # Check if coordinates exist
        if 'latitude' in df.columns and 'longitude' in df.columns:
            df['distance_to_center_km'] = df.apply(
                lambda row: self._calc_distance(
                    row['city'], row['latitude'], row['longitude']
                ) if pd.notna(row['latitude']) else self._estimate_distance(row['city'], row.get('district')),
                axis=1
            )
        else:
            # Estimate based on city and district
            df['distance_to_center_km'] = df.apply(
                lambda row: self._estimate_distance(row['city'], row.get('district')),
                axis=1
            )
        
        return df
    
    def _calc_distance(self, city, lat, lon):
        """Calculate actual distance using coordinates"""
        if city in CITY_CENTERS:
            center = CITY_CENTERS[city]
            try:
                dist = geodesic(center, (lat, lon)).kilometers
                return round(dist, 2)
            except:
                return self._estimate_distance(city, None)
        return 10.0  # default
    
    def _estimate_distance(self, city, district):
        """Estimate distance based on district name"""
        # District 1 = center = 0km, outer districts = farther
        if pd.isna(district):
            return 10.0
        
        district_str = str(district).lower()
        
        # Central districts
        if any(x in district_str for x in ['district 1', 'quan 1', 'center', 'downtown']):
            return 0.5
        elif any(x in district_str for x in ['district 2', 'district 3', 'district 4', 'district 5', 
                                               'binh thanh', 'phu nhuan', 'tan binh']):
            return 5.0
        elif any(x in district_str for x in ['district 7', 'district 9', 'thu duc', 'go vap']):
            return 10.0
        else:
            return 15.0  # Outer districts
    
    def add_poi_features(self, df):
        """
        Thêm features: nearby schools và hospitals
        POI = Points of Interest
        """
        df = df.copy()
        
        # Nearby schools
        if 'district' in df.columns:
            df['nearby_schools'] = df['district'].map(DISTRICT_SCHOOLS).fillna(10)
        else:
            df['nearby_schools'] = 10  # default
        
        # Nearby hospitals
        if 'district' in df.columns:
            df['nearby_hospitals'] = df['district'].map(DISTRICT_HOSPITALS).fillna(3)
        else:
            df['nearby_hospitals'] = 3  # default
        
        return df
    
    def add_property_age(self, df):
        """Thêm tuổi nhà (nếu có year_built)"""
        df = df.copy()
        
        if 'year_built' in df.columns and 'year' in df.columns:
            df['property_age'] = df['year'] - df['year_built']
            df['property_age'] = df['property_age'].clip(lower=0)  # không âm
        elif 'year_built' in df.columns:
            current_year = pd.Timestamp.now().year
            df['property_age'] = current_year - df['year_built']
            df['property_age'] = df['property_age'].clip(lower=0)
        
        return df
    
    def add_price_growth_rate(self, df, fit=False):
        """
        Thêm tỷ lệ tăng trưởng giá theo thời gian (yearly)
        Chỉ dùng khi training (có cột price)
        """
        df = df.copy()
        
        if 'price' not in df.columns or 'year' not in df.columns:
            return df
        
        if fit:
            # Calculate yearly average price
            yearly_avg = df.groupby('year')['price'].mean().sort_index()
            
            # Calculate growth rate
            for i in range(1, len(yearly_avg)):
                year = yearly_avg.index[i]
                prev_price = yearly_avg.iloc[i-1]
                curr_price = yearly_avg.iloc[i]
                growth = (curr_price - prev_price) / prev_price * 100
                self.yearly_growth_rate[year] = growth
            
            self.fitted = True
        
        # Add growth rate as feature
        if self.fitted:
            df['price_growth_rate'] = df['year'].map(self.yearly_growth_rate).fillna(0)
        
        return df
    
    def add_area_per_room(self, df):
        """Thêm diện tích trung bình mỗi phòng"""
        df = df.copy()
        
        if 'area_m2' in df.columns and 'bedrooms' in df.columns:
            df['area_per_room'] = df['area_m2'] / (df['bedrooms'] + 1)  # +1 to avoid division by 0
        
        return df
    
    def add_luxury_score(self, df):
        """
        Thêm điểm sang trọng dựa trên:
        - Area, bathrooms, floor_level
        """
        df = df.copy()
        
        luxury_score = 0
        
        if 'area_m2' in df.columns:
            luxury_score += (df['area_m2'] / 100) * 2  # Large area
        
        if 'bathrooms' in df.columns:
            luxury_score += df['bathrooms'] * 1.5  # Multiple bathrooms
        
        if 'floor_level' in df.columns:
            luxury_score += (df['floor_level'] / 10) * 1  # High floor
        
        df['luxury_score'] = luxury_score
        
        return df
    
    def engineer_all_features(self, df, fit=False):
        """Apply all feature engineering"""
        print("🔧 Engineering features...")
        
        df = self.add_distance_to_center(df)
        print("   ✅ Added: distance_to_center_km")
        
        df = self.add_poi_features(df)
        print("   ✅ Added: nearby_schools, nearby_hospitals")
        
        df = self.add_property_age(df)
        print("   ✅ Added: property_age")
        
        df = self.add_price_growth_rate(df, fit=fit)
        if fit:
            print("   ✅ Added: price_growth_rate")
        
        df = self.add_area_per_room(df)
        print("   ✅ Added: area_per_room")
        
        df = self.add_luxury_score(df)
        print("   ✅ Added: luxury_score")
        
        return df


def apply_feature_engineering(data_path, output_path=None):
    """
    Apply feature engineering to dataset
    
    Args:
        data_path: Path to cleaned_real_estate.csv
        output_path: Path to save enhanced dataset
    """
    print("📂 Loading dataset...")
    df = pd.read_csv(data_path)
    print(f"   Original: {len(df):,} rows, {len(df.columns)} columns")
    
    # Apply feature engineering
    engineer = FeatureEngineer()
    df_enhanced = engineer.engineer_all_features(df, fit=True)
    
    print(f"   Enhanced: {len(df_enhanced):,} rows, {len(df_enhanced.columns)} columns")
    print(f"   New features: {len(df_enhanced.columns) - len(df.columns)}")
    
    # Save
    if output_path is None:
        output_path = Path(data_path).parent / 'cleaned_real_estate_enhanced.csv'
    
    df_enhanced.to_csv(output_path, index=False)
    print(f"✅ Enhanced dataset saved to: {output_path}")
    
    return df_enhanced


if __name__ == '__main__':
    # Apply feature engineering
    data_path = Path(__file__).parent.parent.parent / 'Data' / 'cleaned_real_estate.csv'
    
    if not data_path.exists():
        print(f"❌ Data file not found: {data_path}")
        exit(1)
    
    df_enhanced = apply_feature_engineering(data_path)
    print("\n✅ Feature engineering completed!")
    print(f"   New columns: {list(df_enhanced.columns[-6:])}")  # Show last 6 new columns
