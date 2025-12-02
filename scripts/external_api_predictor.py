"""
External API-Only Prediction System
Use external APIs to fetch real-time property data and make predictions
WITHOUT touching the existing dataset
"""

import requests
import pandas as pd
import numpy as np
from pathlib import Path
import json
from datetime import datetime
import joblib

class ExternalAPIPredictor:
    """Predictor that uses ONLY external APIs - no local dataset needed"""
    
    def __init__(self, model_path='models/lightgbm.joblib'):
        """Initialize with trained model"""
        self.model_data = None
        self.load_model(model_path)
        
        # API configurations
        self.apis = {
            'singapore_hdb': {
                'url': 'https://data.gov.sg/api/action/datastore_search',
                'resource_id': 'd_8b84c4ee58e3cfc0ece0d773c8ca6abc',
                'enabled': True,
                'free': True
            },
            'zillow': {
                'url': 'https://zillow-com1.p.rapidapi.com/propertyExtendedSearch',
                'enabled': False,  # Requires API key
                'free': False
            },
            'realty_mole': {
                'url': 'https://realty-mole-property-api.p.rapidapi.com/properties',
                'enabled': False,  # Requires API key
                'free': False
            }
        }
    
    def load_model(self, model_path):
        """Load trained model"""
        try:
            self.model_data = joblib.load(model_path)
            print(f"[OK] Model loaded: {model_path}")
            return True
        except Exception as e:
            print(f"[ERROR] Error loading model: {e}")
            return False
    
    # ==================== Singapore HDB API (FREE) ====================
    def fetch_singapore_property(self, town=None, flat_type=None):
        """
        Fetch real property data from Singapore HDB API (FREE - No API key needed)
        Returns: DataFrame with real properties
        """
        try:
            params = {
                'resource_id': self.apis['singapore_hdb']['resource_id'],
                'limit': 100
            }
            
            # Add filters if specified
            filters = {}
            if town:
                filters['town'] = town.upper()
            if flat_type:
                filters['flat_type'] = flat_type
            
            if filters:
                params['filters'] = json.dumps(filters)
            
            print(f"[API] Fetching Singapore HDB data from external API...")
            response = requests.get(self.apis['singapore_hdb']['url'], params=params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            records = data.get('result', {}).get('records', [])
            
            if not records:
                return None
            
            # Convert to DataFrame
            df = pd.DataFrame(records)
            print(f"[OK] Fetched {len(df)} properties from Singapore HDB API")
            
            return df
            
        except Exception as e:
            print(f"[ERROR] Error fetching Singapore data: {e}")
            return None
    
    def predict_singapore_property(self, town, flat_type, floor_area_sqm, 
                                   lease_commence_date, storey_range='04 TO 06'):
        """
        Predict Singapore property price using external API data
        WITH data validation and outlier detection
        """
        # Input validation
        try:
            floor_area_sqm = float(floor_area_sqm)
            lease_commence_date = int(lease_commence_date)
            
            # Validate ranges
            if not (30 <= floor_area_sqm <= 300):
                return {'success': False, 'error': 'Floor area must be between 30-300 sqm'}
            if not (1960 <= lease_commence_date <= 2030):
                return {'success': False, 'error': 'Lease year must be between 1960-2030 (future prediction supported)'}
            if town.upper() not in ['ANG MO KIO', 'BEDOK', 'BISHAN', 'BUKIT BATOK', 'BUKIT MERAH',
                                     'BUKIT PANJANG', 'BUKIT TIMAH', 'CENTRAL AREA', 'CHOA CHU KANG',
                                     'CLEMENTI', 'GEYLANG', 'HOUGANG', 'JURONG EAST', 'JURONG WEST',
                                     'KALLANG/WHAMPOA', 'MARINE PARADE', 'PASIR RIS', 'PUNGGOL',
                                     'QUEENSTOWN', 'SEMBAWANG', 'SENGKANG', 'SERANGOON', 'TAMPINES',
                                     'TOA PAYOH', 'WOODLANDS', 'YISHUN']:
                return {'success': False, 'error': f'Invalid town: {town}'}
                
        except (ValueError, TypeError) as e:
            return {'success': False, 'error': f'Invalid input data: {str(e)}'}
        
        # Fetch similar properties from API
        api_data = self.fetch_singapore_property(town=town, flat_type=flat_type)
        
        if api_data is None or len(api_data) == 0:
            return {
                'success': False,
                'error': 'Could not fetch data from external API',
                'predicted_price': None
            }
        
        # Data cleaning and outlier removal
        try:
            # Convert to numeric and remove invalid data
            api_data['resale_price'] = pd.to_numeric(api_data['resale_price'], errors='coerce')
            api_data['floor_area_sqm'] = pd.to_numeric(api_data['floor_area_sqm'], errors='coerce')
            
            # Remove nulls and zeros
            api_data = api_data.dropna(subset=['resale_price', 'floor_area_sqm'])
            api_data = api_data[(api_data['resale_price'] > 0) & (api_data['floor_area_sqm'] > 0)]
            
            if len(api_data) < 10:
                return {'success': False, 'error': 'Insufficient valid data from API (min 10 samples required)'}
            
            # Calculate price per sqm
            api_data['price_per_sqm'] = api_data['resale_price'] / api_data['floor_area_sqm']
            
            # Remove outliers using IQR method
            Q1 = api_data['price_per_sqm'].quantile(0.25)
            Q3 = api_data['price_per_sqm'].quantile(0.75)
            IQR = Q3 - Q1
            lower_bound = Q1 - 1.5 * IQR
            upper_bound = Q3 + 1.5 * IQR
            
            # Filter outliers
            api_data_clean = api_data[
                (api_data['price_per_sqm'] >= lower_bound) & 
                (api_data['price_per_sqm'] <= upper_bound)
            ]
            
            if len(api_data_clean) < 5:
                # If too few samples after cleaning, use original but log warning
                api_data_clean = api_data
                data_quality_warning = 'Warning: Limited data quality'
            else:
                data_quality_warning = None
            
            # Use median for robustness (less affected by outliers than mean)
            avg_price_per_sqm = api_data_clean['price_per_sqm'].median()
            std_price_per_sqm = api_data_clean['price_per_sqm'].std()
            
            # Calculate property age with validation (allow future predictions)
            current_year = datetime.now().year
            property_age = current_year - lease_commence_date
            remaining_lease = max(0, 99 - property_age)  # Ensure non-negative
            
            # For future year predictions, treat as brand new property (age 0)
            if property_age < 0:
                property_age = 0  # Future property, treat as new
                remaining_lease = 99  # Full lease
            if property_age > 99:
                return {'success': False, 'error': 'Property lease expired (>99 years old)'}
            
            # Extract storey info
            storey_mid = self._parse_storey_range(storey_range)
            
            # Prepare features for prediction
            features = {
                'floor_area_sqm': float(floor_area_sqm),
                'lease_commence_date': int(lease_commence_date),
                'property_age': property_age,
                'remaining_lease': remaining_lease,
                'storey_mid': storey_mid,
                'price_per_sqm_area': avg_price_per_sqm,
                'town_encoded': self._encode_town(town),
                'flat_type_encoded': self._encode_flat_type(flat_type)
            }
            
            # Make prediction with model
            if self.model_data and 'model' in self.model_data:
                model = self.model_data['model']
                feature_names = self.model_data.get('feature_names', [])
                
                # Create feature vector in correct order
                X = pd.DataFrame([features])
                
                # Ensure all required features exist
                missing_features = set(feature_names) - set(X.columns)
                if missing_features:
                    for feat in missing_features:
                        X[feat] = 0  # Fill with default
                
                X = X[feature_names]  # Reorder to match training
                
                # Predict
                predicted_price = model.predict(X)[0]
                
                # Sanity check prediction
                if predicted_price <= 0:
                    return {'success': False, 'error': 'Invalid prediction result (negative price)'}
                
                # Calculate confidence interval based on API data variability
                confidence_interval = 1.96 * std_price_per_sqm * floor_area_sqm  # 95% CI
                
                return {
                    'success': True,
                    'predicted_price': float(predicted_price),
                    'confidence_interval': {
                        'lower': max(0, float(predicted_price - confidence_interval)),
                        'upper': float(predicted_price + confidence_interval)
                    },
                    'api_samples': {
                        'total': len(api_data),
                        'after_cleaning': len(api_data_clean),
                        'removed_outliers': len(api_data) - len(api_data_clean)
                    },
                    'market_data': {
                        'avg_price_per_sqm': float(avg_price_per_sqm),
                        'std_price_per_sqm': float(std_price_per_sqm),
                        'min_price': float(api_data_clean['resale_price'].min()),
                        'max_price': float(api_data_clean['resale_price'].max()),
                        'median_price': float(api_data_clean['resale_price'].median())
                    },
                    'property_details': {
                        'town': town,
                        'flat_type': flat_type,
                        'floor_area_sqm': floor_area_sqm,
                        'property_age': property_age,
                        'remaining_lease': remaining_lease
                    },
                    'data_source': 'Singapore HDB External API (data.gov.sg)',
                    'data_quality': data_quality_warning
                }
            else:
                # Fallback: Statistical prediction when model not available
                # Use median price per sqm from API data adjusted by property characteristics
                base_price_per_sqm = avg_price_per_sqm
                
                # Adjust for property age (newer = higher price)
                age_factor = 1.0
                if property_age < 5:
                    age_factor = 1.15  # 15% premium for very new
                elif property_age < 10:
                    age_factor = 1.08  # 8% premium for new
                elif property_age > 30:
                    age_factor = 0.90  # 10% discount for old
                    
                # Adjust for storey (higher = slight premium)
                storey_factor = 1.0
                storey_mid = self._parse_storey_range(storey_range)
                if storey_mid >= 10:
                    storey_factor = 1.05
                elif storey_mid <= 3:
                    storey_factor = 0.97
                    
                # Calculate predicted price
                adjusted_price_per_sqm = base_price_per_sqm * age_factor * storey_factor
                predicted_price = adjusted_price_per_sqm * floor_area_sqm
                
                # Confidence interval
                confidence_interval = 1.96 * std_price_per_sqm * floor_area_sqm
                
                return {
                    'success': True,
                    'predicted_price': float(predicted_price),
                    'confidence_interval': {
                        'lower': max(0, float(predicted_price - confidence_interval)),
                        'upper': float(predicted_price + confidence_interval)
                    },
                    'api_samples': {
                        'total': len(api_data),
                        'after_cleaning': len(api_data_clean),
                        'removed_outliers': len(api_data) - len(api_data_clean)
                    },
                    'market_data': {
                        'avg_price_per_sqm': float(avg_price_per_sqm),
                        'std_price_per_sqm': float(std_price_per_sqm),
                        'min_price': float(api_data_clean['resale_price'].min()),
                        'max_price': float(api_data_clean['resale_price'].max()),
                        'median_price': float(api_data_clean['resale_price'].median())
                    },
                    'property_details': {
                        'town': town,
                        'flat_type': flat_type,
                        'floor_area_sqm': floor_area_sqm,
                        'property_age': property_age,
                        'remaining_lease': remaining_lease
                    },
                    'data_source': 'Singapore HDB API - Statistical Prediction (ML model not loaded)',
                    'data_quality': data_quality_warning or 'Using statistical method: base price × age factor × storey factor'
                }
                
        except Exception as e:
            return {
                'success': False,
                'error': f'Prediction error: {str(e)}'
            }
    
    # ==================== USA Zillow API (Requires API Key) ====================
    def fetch_usa_property(self, city, state, api_key):
        """
        Fetch real property data from Zillow API
        Requires RapidAPI key
        """
        try:
            headers = {
                "X-RapidAPI-Key": api_key,
                "X-RapidAPI-Host": "zillow-com1.p.rapidapi.com"
            }
            
            params = {
                "location": f"{city}, {state}",
                "status_type": "ForSale",
                "home_type": "Houses"
            }
            
            print(f"[API] Fetching USA property data from Zillow API...")
            response = requests.get(self.apis['zillow']['url'], headers=headers, params=params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            properties = data.get('props', [])
            
            if not properties:
                return None
            
            # Convert to DataFrame
            df = pd.DataFrame(properties)
            print(f"[OK] Fetched {len(df)} properties from Zillow API")
            
            return df
            
        except Exception as e:
            print(f"[ERROR] Error fetching USA data: {e}")
            return None
    
    def predict_usa_property(self, city, state, bedrooms, bathrooms, 
                            living_area_sqft, lot_size_sqft, year_built, api_key=None):
        """
        Predict USA property price using Zillow API data
        WITHOUT touching local dataset
        """
        if not api_key:
            return {
                'success': False,
                'error': 'Zillow API key required. Get free trial at https://rapidapi.com/apimaker/api/zillow-com1'
            }
        
        # Fetch similar properties from API
        api_data = self.fetch_usa_property(city, state, api_key)
        
        if api_data is None:
            return {
                'success': False,
                'error': 'Could not fetch data from Zillow API'
            }
        
        # Make prediction based on API data
        # Implementation similar to Singapore but with USA features
        pass
    
    # ==================== Helper Functions ====================
    def _parse_storey_range(self, storey_range):
        """Parse storey range to get midpoint (e.g., '04 TO 06' -> 5)"""
        try:
            parts = storey_range.split(' TO ')
            low = int(parts[0])
            high = int(parts[1])
            return (low + high) / 2
        except:
            return 5  # Default midpoint
    
    def _encode_town(self, town):
        """Simple town encoding (can be improved with proper mapping)"""
        town_map = {
            'ANG MO KIO': 1, 'BEDOK': 2, 'BISHAN': 3, 'BUKIT BATOK': 4,
            'BUKIT MERAH': 5, 'BUKIT PANJANG': 6, 'BUKIT TIMAH': 7,
            'CENTRAL AREA': 8, 'CHOA CHU KANG': 9, 'CLEMENTI': 10,
            'GEYLANG': 11, 'HOUGANG': 12, 'JURONG EAST': 13, 'JURONG WEST': 14,
            'KALLANG/WHAMPOA': 15, 'MARINE PARADE': 16, 'PASIR RIS': 17,
            'PUNGGOL': 18, 'QUEENSTOWN': 19, 'SEMBAWANG': 20, 'SENGKANG': 21,
            'SERANGOON': 22, 'TAMPINES': 23, 'TOA PAYOH': 24, 'WOODLANDS': 25, 'YISHUN': 26
        }
        return town_map.get(town.upper(), 0)
    
    def _encode_flat_type(self, flat_type):
        """Simple flat type encoding"""
        type_map = {
            '1 ROOM': 1, '2 ROOM': 2, '3 ROOM': 3, '4 ROOM': 4,
            '5 ROOM': 5, 'EXECUTIVE': 6, 'MULTI-GENERATION': 7
        }
        return type_map.get(flat_type.upper(), 0)
    
    # ==================== Multi-Country Support ====================
    def predict_any_country(self, country, **kwargs):
        """
        Universal prediction function that routes to correct API
        """
        if country.lower() == 'singapore':
            return self.predict_singapore_property(**kwargs)
        elif country.lower() == 'usa':
            return self.predict_usa_property(**kwargs)
        else:
            return {
                'success': False,
                'error': f'External API not available for {country}. Only Singapore (FREE) and USA (requires API key) supported.'
            }


# ==================== Example Usage ====================
if __name__ == '__main__':
    print("=" * 60)
    print("EXTERNAL API-ONLY PREDICTOR - No Local Dataset Used")
    print("=" * 60)
    
    # Initialize predictor
    predictor = ExternalAPIPredictor('models/lightgbm.joblib')
    
    # Example 1: Singapore prediction using FREE external API
    print("\n📍 Example 1: Singapore Property (FREE API)")
    print("-" * 60)
    
    result = predictor.predict_singapore_property(
        town='TAMPINES',
        flat_type='4 ROOM',
        floor_area_sqm=90,
        lease_commence_date=2000,
        storey_range='07 TO 09'
    )
    
    if result['success']:
        print(f"SUCCESS! Prediction Successful!")
        print(f"  Predicted Price: ${result['predicted_price']:,.2f}")
        print(f"  Data Source: {result['data_source']}")
        print(f"  API Samples Used: {result['api_samples']}")
        print(f"  Avg Price/sqm: ${result['avg_price_per_sqm']:,.2f}")
    else:
        print(f"FAILED: {result['error']}")
    
    # Example 2: USA prediction (requires API key)
    print("\n📍 Example 2: USA Property (Requires RapidAPI Key)")
    print("-" * 60)
    print("To use USA predictions:")
    print("1. Get free API key from: https://rapidapi.com/apimaker/api/zillow-com1")
    print("2. Call: predictor.predict_usa_property(..., api_key='YOUR_KEY')")
    
    print("\n" + "=" * 60)
