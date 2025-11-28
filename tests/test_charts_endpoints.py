"""Quick test for Advanced Charts API endpoints"""
import requests
import json

BASE_URL = "http://127.0.0.1:5000"

def test_endpoint(endpoint, params=None):
    """Test a single API endpoint"""
    try:
        url = f"{BASE_URL}{endpoint}"
        response = requests.get(url, params=params, timeout=10)
        data = response.json()
        
        if data.get('success'):
            print(f"✓ {endpoint}")
            return True
        else:
            print(f"✗ {endpoint}: {data.get('error', 'Unknown error')}")
            return False
    except Exception as e:
        print(f"✗ {endpoint}: {str(e)}")
        return False

def main():
    print("Testing Advanced Charts API Endpoints...\n")
    
    endpoints = [
        "/api/charts/overview",
        "/api/charts/price-trend",
        "/api/charts/property-type-distribution",
        "/api/charts/price-range-distribution",
        "/api/charts/area-distribution",
        "/api/charts/seasonal-patterns",
        "/api/charts/top-cities",
        "/api/charts/price-by-type-trend",
        "/api/charts/countries",
        "/api/charts/price-heatmap"
    ]
    
    results = []
    for endpoint in endpoints:
        results.append(test_endpoint(endpoint))
    
    print(f"\n{'='*50}")
    print(f"Results: {sum(results)}/{len(results)} endpoints working")
    
    # Test with filters
    print(f"\n{'='*50}")
    print("Testing with filters:")
    test_endpoint("/api/charts/overview", {"country": "Singapore", "year_range": "5"})
    test_endpoint("/api/charts/price-trend", {"year_range": "10"})

if __name__ == "__main__":
    main()
