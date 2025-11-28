"""
External API Integration for Data Collection
Fetch real estate data from external APIs to train models
"""

import requests
import pandas as pd
import json
from datetime import datetime
from pathlib import Path
import time

class RealEstateAPIClient:
    """Client to fetch data from various real estate APIs"""
    
    def __init__(self):
        self.cache_dir = Path('Data/api_cache')
        self.cache_dir.mkdir(exist_ok=True, parents=True)
    
    # ==================== Zillow API (US) ====================
    def fetch_zillow_data(self, api_key, location, max_results=100):
        """
        Fetch data from Zillow API
        
        Zillow API: https://www.zillow.com/howto/api/APIOverview.htm
        RapidAPI Zillow: https://rapidapi.com/apimaker/api/zillow-com1
        """
        url = "https://zillow-com1.p.rapidapi.com/propertyExtendedSearch"
        
        headers = {
            "X-RapidAPI-Key": api_key,
            "X-RapidAPI-Host": "zillow-com1.p.rapidapi.com"
        }
        
        querystring = {
            "location": location,
            "status_type": "ForSale",
            "home_type": "Houses"
        }
        
        try:
            response = requests.get(url, headers=headers, params=querystring)
            response.raise_for_status()
            data = response.json()
            
            # Parse and normalize
            properties = []
            for prop in data.get('props', [])[:max_results]:
                properties.append({
                    'country': 'USA',
                    'city': prop.get('address', {}).get('city'),
                    'area_m2': prop.get('livingArea', 0) * 0.092903,  # sqft to m2
                    'bedrooms': prop.get('bedrooms'),
                    'bathrooms': prop.get('bathrooms'),
                    'price': prop.get('price'),
                    'year_built': prop.get('yearBuilt'),
                    'property_type': prop.get('homeType'),
                    'date': datetime.now().strftime('%Y-%m-%d'),
                    'source': 'zillow'
                })
            
            df = pd.DataFrame(properties)
            self._save_cache(df, f'zillow_{location}_{datetime.now().strftime("%Y%m%d")}')
            return df
            
        except Exception as e:
            print(f"Error fetching Zillow data: {e}")
            return pd.DataFrame()
    
    # ==================== Realty Mole API (US) ====================
    def fetch_realty_mole_data(self, api_key, city, state, limit=100):
        """
        Fetch data from Realty Mole Property API
        
        API: https://rapidapi.com/realtymole/api/realty-mole-property-api
        """
        url = "https://realty-mole-property-api.p.rapidapi.com/properties"
        
        headers = {
            "X-RapidAPI-Key": api_key,
            "X-RapidAPI-Host": "realty-mole-property-api.p.rapidapi.com"
        }
        
        querystring = {"city": city, "state": state, "limit": str(limit)}
        
        try:
            response = requests.get(url, headers=headers, params=querystring)
            response.raise_for_status()
            data = response.json()
            
            properties = []
            for prop in data:
                properties.append({
                    'country': 'USA',
                    'city': city,
                    'area_m2': prop.get('squareFootage', 0) * 0.092903,
                    'bedrooms': prop.get('bedrooms'),
                    'bathrooms': prop.get('bathrooms'),
                    'price': prop.get('assessedValue'),
                    'year_built': prop.get('yearBuilt'),
                    'property_type': prop.get('propertyType'),
                    'date': datetime.now().strftime('%Y-%m-%d'),
                    'source': 'realty_mole'
                })
            
            df = pd.DataFrame(properties)
            self._save_cache(df, f'realty_mole_{city}_{datetime.now().strftime("%Y%m%d")}')
            return df
            
        except Exception as e:
            print(f"Error fetching Realty Mole data: {e}")
            return pd.DataFrame()
    
    # ==================== Zoopla API (UK) ====================
    def fetch_zoopla_data(self, api_key, area, max_results=100):
        """
        Fetch data from Zoopla API
        
        API: https://developer.zoopla.co.uk/docs/
        """
        url = "https://api.zoopla.co.uk/api/v1/property_listings.json"
        
        params = {
            'api_key': api_key,
            'area': area,
            'listing_status': 'sale',
            'page_size': max_results
        }
        
        try:
            response = requests.get(url, params=params)
            response.raise_for_status()
            data = response.json()
            
            properties = []
            for prop in data.get('listing', []):
                properties.append({
                    'country': 'UK',
                    'city': prop.get('county'),
                    'area_m2': prop.get('num_floors', 0) * 50,  # estimate
                    'bedrooms': prop.get('num_bedrooms'),
                    'bathrooms': prop.get('num_bathrooms'),
                    'price': prop.get('price'),
                    'property_type': prop.get('property_type'),
                    'date': datetime.now().strftime('%Y-%m-%d'),
                    'source': 'zoopla'
                })
            
            df = pd.DataFrame(properties)
            self._save_cache(df, f'zoopla_{area}_{datetime.now().strftime("%Y%m%d")}')
            return df
            
        except Exception as e:
            print(f"Error fetching Zoopla data: {e}")
            return pd.DataFrame()
    
    # ==================== Domain.com.au API (Australia) ====================
    def fetch_domain_data(self, api_key, suburb, state='NSW', max_results=100):
        """
        Fetch data from Domain.com.au API
        
        API: https://developer.domain.com.au/
        """
        url = f"https://api.domain.com.au/v1/listings/residential/_search"
        
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "listingType": "Sale",
            "locations": [{"state": state, "suburb": suburb}],
            "pageSize": max_results
        }
        
        try:
            response = requests.post(url, headers=headers, json=payload)
            response.raise_for_status()
            data = response.json()
            
            properties = []
            for prop in data:
                properties.append({
                    'country': 'Australia',
                    'city': suburb,
                    'area_m2': prop.get('propertyDetails', {}).get('landArea'),
                    'bedrooms': prop.get('propertyDetails', {}).get('bedrooms'),
                    'bathrooms': prop.get('propertyDetails', {}).get('bathrooms'),
                    'price': prop.get('priceDetails', {}).get('price'),
                    'property_type': prop.get('propertyDetails', {}).get('propertyType'),
                    'date': datetime.now().strftime('%Y-%m-%d'),
                    'source': 'domain_au'
                })
            
            df = pd.DataFrame(properties)
            self._save_cache(df, f'domain_{suburb}_{datetime.now().strftime("%Y%m%d")}')
            return df
            
        except Exception as e:
            print(f"Error fetching Domain data: {e}")
            return pd.DataFrame()
    
    # ==================== Open Data APIs ====================
    def fetch_singapore_hdb_data(self, year=2024, month=None):
        """
        Fetch Singapore HDB resale data from data.gov.sg
        
        API: https://data.gov.sg/
        """
        url = "https://data.gov.sg/api/action/datastore_search"
        
        params = {
            'resource_id': 'f1765b54-a209-4718-8d38-a39237f502b3',  # HDB resale prices
            'limit': 1000
        }
        
        if month:
            params['filters'] = json.dumps({'month': f'{year}-{month:02d}'})
        
        try:
            response = requests.get(url, params=params)
            response.raise_for_status()
            data = response.json()
            
            properties = []
            for record in data.get('result', {}).get('records', []):
                properties.append({
                    'country': 'Singapore',
                    'city': record.get('town'),
                    'area_m2': float(record.get('floor_area_sqm', 0)),
                    'property_type': record.get('flat_type'),
                    'price': float(record.get('resale_price', 0)),
                    'year': int(record.get('month', '2024-01').split('-')[0]),
                    'month': int(record.get('month', '2024-01').split('-')[1]),
                    'date': record.get('month') + '-01',
                    'source': 'data_gov_sg'
                })
            
            df = pd.DataFrame(properties)
            self._save_cache(df, f'singapore_hdb_{year}_{datetime.now().strftime("%Y%m%d")}')
            return df
            
        except Exception as e:
            print(f"Error fetching Singapore HDB data: {e}")
            return pd.DataFrame()
    
    # ==================== Combine Multiple Sources ====================
    def fetch_multi_source_data(self, apis_config):
        """
        Fetch data from multiple APIs and combine
        
        apis_config example:
        {
            'zillow': {'api_key': 'xxx', 'location': 'New York, NY'},
            'singapore': {'year': 2024, 'month': 6},
            'domain': {'api_key': 'yyy', 'suburb': 'Melbourne'}
        }
        """
        all_data = []
        
        if 'zillow' in apis_config:
            print("Fetching Zillow data...")
            df = self.fetch_zillow_data(**apis_config['zillow'])
            if not df.empty:
                all_data.append(df)
                print(f"  ✓ Got {len(df)} properties from Zillow")
        
        if 'realty_mole' in apis_config:
            print("Fetching Realty Mole data...")
            df = self.fetch_realty_mole_data(**apis_config['realty_mole'])
            if not df.empty:
                all_data.append(df)
                print(f"  ✓ Got {len(df)} properties from Realty Mole")
        
        if 'zoopla' in apis_config:
            print("Fetching Zoopla data...")
            df = self.fetch_zoopla_data(**apis_config['zoopla'])
            if not df.empty:
                all_data.append(df)
                print(f"  ✓ Got {len(df)} properties from Zoopla")
        
        if 'domain' in apis_config:
            print("Fetching Domain.com.au data...")
            df = self.fetch_domain_data(**apis_config['domain'])
            if not df.empty:
                all_data.append(df)
                print(f"  ✓ Got {len(df)} properties from Domain")
        
        if 'singapore' in apis_config:
            print("Fetching Singapore HDB data...")
            df = self.fetch_singapore_hdb_data(**apis_config['singapore'])
            if not df.empty:
                all_data.append(df)
                print(f"  ✓ Got {len(df)} properties from data.gov.sg")
        
        if not all_data:
            print("⚠️  No data fetched from any source")
            return pd.DataFrame()
        
        # Combine all dataframes
        combined_df = pd.concat(all_data, ignore_index=True)
        
        # Save combined data
        output_file = f'Data/api_combined_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv'
        combined_df.to_csv(output_file, index=False)
        print(f"\n✅ Combined {len(combined_df)} properties from {len(all_data)} sources")
        print(f"   Saved to: {output_file}")
        
        return combined_df
    
    # ==================== Cache Management ====================
    def _save_cache(self, df, filename):
        """Save fetched data to cache"""
        if not df.empty:
            cache_file = self.cache_dir / f'{filename}.csv'
            df.to_csv(cache_file, index=False)
            print(f"  💾 Cached to: {cache_file}")
    
    def load_cache(self, source, days_old=7):
        """Load cached data if available and recent"""
        import glob
        from datetime import timedelta
        
        pattern = str(self.cache_dir / f'{source}_*.csv')
        files = glob.glob(pattern)
        
        if not files:
            return pd.DataFrame()
        
        # Get most recent file
        latest_file = max(files, key=lambda x: Path(x).stat().st_mtime)
        file_time = datetime.fromtimestamp(Path(latest_file).stat().st_mtime)
        
        # Check if recent enough
        if datetime.now() - file_time < timedelta(days=days_old):
            print(f"📦 Loading cached data from: {latest_file}")
            return pd.read_csv(latest_file)
        
        return pd.DataFrame()


# ==================== EXAMPLE USAGE ====================
if __name__ == "__main__":
    client = RealEstateAPIClient()
    
    # Example 1: Singapore HDB data (free, no API key needed)
    print("\n=== Fetching Singapore HDB Data ===")
    singapore_df = client.fetch_singapore_hdb_data(year=2024, month=6)
    
    if not singapore_df.empty:
        print(f"\nSample data:")
        print(singapore_df.head())
        print(f"\nShape: {singapore_df.shape}")
    
    # Example 2: Multi-source (requires API keys)
    # Uncomment and add your API keys
    """
    apis_config = {
        'singapore': {'year': 2024, 'month': 6},
        'zillow': {
            'api_key': 'YOUR_RAPIDAPI_KEY',
            'location': 'New York, NY',
            'max_results': 50
        },
        'domain': {
            'api_key': 'YOUR_DOMAIN_API_KEY',
            'suburb': 'Melbourne',
            'state': 'VIC'
        }
    }
    
    combined_df = client.fetch_multi_source_data(apis_config)
    """
