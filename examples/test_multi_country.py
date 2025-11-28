"""
Test Multi-Country API Support
Test predictions across 12 countries
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

import requests
import json

# Flask app URL
BASE_URL = "http://localhost:5000"

def test_get_countries():
    """Test getting list of countries"""
    print("\n" + "="*60)
    print("TEST 1: Get All Countries")
    print("="*60)
    
    response = requests.get(f"{BASE_URL}/get_countries")
    data = response.json()
    
    if data['success']:
        countries = data['countries']
        print(f"✅ Success! Found {len(countries)} countries:")
        for i, country in enumerate(countries, 1):
            print(f"  {i:2}. {country}")
        return countries
    else:
        print(f"❌ Failed: {data.get('error')}")
        return []

def test_get_cities(country):
    """Test getting cities for a country"""
    print(f"\n{'='*60}")
    print(f"TEST 2: Get Cities for {country}")
    print(f"{'='*60}")
    
    response = requests.get(f"{BASE_URL}/get_cities/{country}")
    data = response.json()
    
    if data['success']:
        cities = data['cities']
        print(f"✅ Success! Found {len(cities)} cities")
        print(f"  First 10: {', '.join(cities[:10])}")
        return cities
    else:
        print(f"❌ Failed: {data.get('error')}")
        return []

def test_prediction(country, city, **kwargs):
    """Test price prediction"""
    print(f"\n{'='*60}")
    print(f"TEST 3: Predict Price - {country}, {city}")
    print(f"{'='*60}")
    
    # Base payload
    payload = {
        'country': country,
        'city': city,
        'area_m2': kwargs.get('area_m2', 100),
        'year': kwargs.get('year', 2024),
        'month': kwargs.get('month', 11)
    }
    
    # Add optional fields
    if 'property_type' in kwargs:
        payload['property_type'] = kwargs['property_type']
    if 'bedrooms' in kwargs:
        payload['bedrooms'] = kwargs['bedrooms']
    if 'bathrooms' in kwargs:
        payload['bathrooms'] = kwargs['bathrooms']
    if 'year_built' in kwargs:
        payload['year_built'] = kwargs['year_built']
    
    print(f"\nPayload:")
    print(json.dumps(payload, indent=2))
    
    response = requests.post(
        f"{BASE_URL}/predict",
        json=payload,
        headers={'Content-Type': 'application/json'}
    )
    
    data = response.json()
    
    if data['success']:
        print(f"\n✅ Prediction Success!")
        print(f"  Predicted Price: {data.get('formatted_price', data.get('predicted_price'))}")
        if 'confidence' in data:
            print(f"  Confidence: {data['confidence']}")
    else:
        print(f"\n❌ Prediction Failed: {data.get('error')}")
    
    return data

def test_all_countries():
    """Test predictions for all 12 countries"""
    print("\n" + "="*60)
    print("COMPREHENSIVE TEST: All 12 Countries")
    print("="*60)
    
    test_cases = [
        {
            'country': 'Singapore',
            'city': 'PUNGGOL',
            'area_m2': 93,
            'property_type': '4 ROOM'
        },
        {
            'country': 'USA',
            'city': 'New York',
            'area_m2': 120,
            'bedrooms': 3,
            'bathrooms': 2,
            'year_built': 2015
        },
        {
            'country': 'Australia',
            'city': 'Sydney',
            'area_m2': 110,
            'bedrooms': 3,
            'bathrooms': 2
        },
        {
            'country': 'UK',
            'city': 'London',
            'area_m2': 85,
            'bedrooms': 2,
            'bathrooms': 1,
            'property_type': 'Flat'
        },
        {
            'country': 'Canada',
            'city': 'Toronto',
            'area_m2': 95,
            'bedrooms': 2,
            'bathrooms': 2
        },
        {
            'country': 'Germany',
            'city': 'Berlin',
            'area_m2': 80,
            'bedrooms': 2,
            'bathrooms': 1,
            'property_type': 'Apartment'
        },
        {
            'country': 'France',
            'city': 'Paris',
            'area_m2': 70,
            'bedrooms': 2,
            'bathrooms': 1
        },
        {
            'country': 'Japan',
            'city': 'Tokyo',
            'area_m2': 60,
            'bedrooms': 2,
            'bathrooms': 1,
            'property_type': 'Apartment'
        },
        {
            'country': 'China',
            'city': 'Shanghai',
            'area_m2': 90,
            'bedrooms': 3,
            'bathrooms': 2
        },
        {
            'country': 'South Korea',
            'city': 'Seoul',
            'area_m2': 85,
            'bedrooms': 3,
            'bathrooms': 2,
            'property_type': 'Apartment'
        },
        {
            'country': 'India',
            'city': 'Mumbai',
            'area_m2': 75,
            'bedrooms': 2,
            'bathrooms': 2
        },
        {
            'country': 'UAE',
            'city': 'Dubai',
            'area_m2': 120,
            'bedrooms': 3,
            'bathrooms': 2,
            'property_type': 'Apartment'
        }
    ]
    
    results = []
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n[{i}/12] Testing {test_case['country']}...")
        result = test_prediction(**test_case)
        results.append({
            'country': test_case['country'],
            'city': test_case['city'],
            'success': result.get('success', False),
            'price': result.get('predicted_price') if result.get('success') else None
        })
    
    # Summary
    print("\n" + "="*60)
    print("SUMMARY")
    print("="*60)
    
    successful = sum(1 for r in results if r['success'])
    print(f"\nSuccess Rate: {successful}/{len(results)} ({successful/len(results)*100:.1f}%)")
    
    print("\nResults:")
    for r in results:
        status = "✅" if r['success'] else "❌"
        price_str = f"${r['price']:,.0f}" if r['price'] else "N/A"
        print(f"  {status} {r['country']:15} {r['city']:20} {price_str}")

if __name__ == "__main__":
    print("\n" + "="*60)
    print("🌍 MULTI-COUNTRY API TEST SUITE")
    print("="*60)
    print("\nMake sure Flask app is running on http://localhost:5000")
    print("Press Enter to start tests, or Ctrl+C to cancel...")
    input()
    
    try:
        # Test 1: Get countries
        countries = test_get_countries()
        
        if countries:
            # Test 2: Get cities for first 3 countries
            for country in countries[:3]:
                test_get_cities(country)
            
            # Test 3: Single prediction
            print("\n" + "="*60)
            print("QUICK TEST: Single Prediction")
            print("="*60)
            test_prediction(
                country='Singapore',
                city='PUNGGOL',
                area_m2=93,
                property_type='4 ROOM'
            )
            
            # Test 4: All countries
            test_all_countries()
        
        print("\n" + "="*60)
        print("✅ ALL TESTS COMPLETED")
        print("="*60)
        
    except requests.exceptions.ConnectionError:
        print("\n❌ Error: Cannot connect to Flask app")
        print("Make sure the app is running: python app.py")
    except KeyboardInterrupt:
        print("\n\nTests cancelled by user")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
