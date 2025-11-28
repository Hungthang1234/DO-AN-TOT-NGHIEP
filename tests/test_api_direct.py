"""Test Advanced Charts API directly"""
import sys
import time

def test_api():
    """Test all Advanced Charts API endpoints"""
    import requests
    
    base_url = "http://127.0.0.1:5000"
    endpoints = [
        "/api/charts/countries",
        "/api/charts/overview",
        "/api/charts/price-trend",
        "/api/charts/property-type-distribution",
        "/api/charts/price-range-distribution",
        "/api/charts/area-distribution",
        "/api/charts/seasonal-patterns",
        "/api/charts/top-cities",
        "/api/charts/price-by-type-trend",
        "/api/charts/price-heatmap"
    ]
    
    print("Testing Advanced Charts API Endpoints\n" + "="*50)
    
    passed = 0
    failed = 0
    
    for endpoint in endpoints:
        try:
            response = requests.get(f"{base_url}{endpoint}", timeout=10)
            data = response.json()
            
            if data.get('success'):
                print(f"✓ {endpoint}")
                # Show sample data for first endpoint
                try:
                    if endpoint == "/api/charts/countries" and 'data' in data:
                        countries = data['data'].get('countries', [])
                        print(f"  Countries: {countries[:5] if len(countries) > 5 else countries}")
                    elif endpoint == "/api/charts/overview" and 'data' in data:
                        print(f"  Total records: {data['data'].get('total_records', 0):,}")
                        print(f"  Avg price: ${data['data'].get('avg_price', 0):,.0f}")
                except Exception as e:
                    pass  # Just skip sample data if structure is different
                passed += 1
            else:
                print(f"✗ {endpoint}: {data.get('error', 'Unknown error')}")
                failed += 1
        except Exception as e:
            print(f"✗ {endpoint}: {str(e)}")
            failed += 1
    
    print(f"\n{'='*50}")
    print(f"Results: {passed}/{len(endpoints)} passed, {failed} failed")
    
    if failed == 0:
        print("\n✓ All Advanced Charts API endpoints working!")
        return True
    else:
        print(f"\n✗ {failed} endpoints failed")
        return False

if __name__ == "__main__":
    # Wait for server to be ready
    print("Waiting for server...")
    time.sleep(2)
    
    success = test_api()
    sys.exit(0 if success else 1)
