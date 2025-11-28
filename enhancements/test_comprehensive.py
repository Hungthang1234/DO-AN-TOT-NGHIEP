"""
Comprehensive test suite for enhancement APIs
Tests all endpoints with various scenarios
"""

import json
import time

def test_with_powershell(endpoint, payload, test_name):
    """Test API endpoint using PowerShell Invoke-RestMethod"""
    import subprocess
    
    print(f"\n{'='*80}")
    print(f"TEST: {test_name}")
    print(f"Endpoint: {endpoint}")
    print(f"{'='*80}")
    
    json_payload = json.dumps(payload)
    
    # Escape quotes for PowerShell
    json_payload_escaped = json_payload.replace('"', '`"')
    
    ps_command = f'''
$body = '{json_payload_escaped}'
try {{
    $response = Invoke-RestMethod -Uri http://localhost:5000{endpoint} -Method Post -Body $body -ContentType "application/json"
    $response | ConvertTo-Json -Depth 10
}} catch {{
    Write-Host "Error: $_"
    exit 1
}}
'''
    
    try:
        result = subprocess.run(
            ['powershell', '-Command', ps_command],
            capture_output=True,
            text=True,
            timeout=30
        )
        
        if result.returncode == 0:
            print("✅ SUCCESS")
            print(result.stdout)
            return True
        else:
            print("❌ FAILED")
            print(result.stderr)
            return False
    except subprocess.TimeoutExpired:
        print("❌ TIMEOUT")
        return False
    except Exception as e:
        print(f"❌ ERROR: {e}")
        return False


def test_health_check():
    """Test health endpoint"""
    import subprocess
    
    print(f"\n{'='*80}")
    print("TEST 0: HEALTH CHECK")
    print(f"{'='*80}")
    
    try:
        result = subprocess.run(
            ['powershell', '-Command', 
             'Invoke-RestMethod -Uri http://localhost:5000/api/health -Method Get'],
            capture_output=True,
            text=True,
            timeout=10
        )
        
        if result.returncode == 0:
            print("✅ API is healthy!")
            print(result.stdout)
            return True
        else:
            print("❌ Health check failed")
            print(result.stderr)
            return False
    except Exception as e:
        print(f"❌ Cannot connect to server: {e}")
        print("   Make sure Flask server is running!")
        return False


def main():
    """Run all tests"""
    print("🧪 COMPREHENSIVE API TESTING")
    print("="*80)
    
    # Wait for server
    print("\nWaiting for server to be ready...")
    time.sleep(2)
    
    results = {}
    
    # Test 0: Health check
    results['health'] = test_health_check()
    
    if not results['health']:
        print("\n❌ Server not responding. Tests aborted.")
        return
    
    time.sleep(1)
    
    # Test 1: Predict Trend
    results['predict_trend'] = test_with_powershell(
        '/api/predict_trend',
        {
            "country": "Vietnam",
            "city": "Ho Chi Minh City",
            "area_m2": 100,
            "property_type": "Apartment",
            "start_year": 2024,
            "years_ahead": 5
        },
        "PREDICT TREND - 5 year forecast"
    )
    
    time.sleep(1)
    
    # Test 2: Compare Areas
    results['compare_areas'] = test_with_powershell(
        '/api/compare_areas',
        {
            "base_features": {
                "country": "Vietnam",
                "area_m2": 100,
                "property_type": "Apartment",
                "year": 2024
            },
            "cities": ["Ho Chi Minh City", "Hanoi", "Da Nang"]
        },
        "COMPARE AREAS - 3 cities"
    )
    
    time.sleep(1)
    
    # Test 3: Calculate ROI
    results['calculate_roi'] = test_with_powershell(
        '/api/calculate_roi',
        {
            "purchase_price": 500000,
            "purchase_year": 2024,
            "sell_year": 2029,
            "features": {
                "country": "Vietnam",
                "city": "Ho Chi Minh City",
                "area_m2": 100,
                "property_type": "Apartment"
            },
            "additional_costs": 50000,
            "rental_income_per_year": 30000
        },
        "CALCULATE ROI - 5 year investment"
    )
    
    time.sleep(1)
    
    # Test 4: Predict Trend (10 years)
    results['predict_trend_10y'] = test_with_powershell(
        '/api/predict_trend',
        {
            "country": "Vietnam",
            "city": "Hanoi",
            "area_m2": 150,
            "property_type": "House",
            "start_year": 2025,
            "years_ahead": 10
        },
        "PREDICT TREND - 10 year forecast (Hanoi, House)"
    )
    
    # Summary
    print("\n" + "="*80)
    print("📊 TEST SUMMARY")
    print("="*80)
    
    total = len(results)
    passed = sum(1 for v in results.values() if v)
    failed = total - passed
    
    for test_name, result in results.items():
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"  {status} - {test_name}")
    
    print(f"\n  Total: {total} | Passed: {passed} | Failed: {failed}")
    
    if failed == 0:
        print("\n🎉 ALL TESTS PASSED!")
    else:
        print(f"\n⚠️  {failed} test(s) failed")
    
    print("="*80)


if __name__ == '__main__':
    main()
