"""
Test script for enhanced API endpoints
Tests: predict_trend, compare_areas, calculate_roi
"""

import requests
import json

BASE_URL = "http://localhost:5000/api"


def test_predict_trend():
    """Test price trend prediction"""
    print("\n" + "="*80)
    print("TEST 1: PREDICT TREND")
    print("="*80)
    
    payload = {
        "country": "Vietnam",
        "city": "Ho Chi Minh City",
        "area_m2": 100,
        "property_type": "Apartment",
        "start_year": 2024,
        "years_ahead": 5
    }
    
    try:
        response = requests.post(f"{BASE_URL}/predict_trend", json=payload)
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Success!")
            print(f"\nPeriod: {result['period']}")
            print(f"Average Growth Rate: {result['growth_rate']}% per year")
            print(f"Total Growth: {result['total_growth']}%")
            print("\nYearly Predictions:")
            for item in result['trend']:
                print(f"  {item['year']}: ${item['predicted_price']:,.2f}")
        else:
            print(f"❌ Error: {response.status_code}")
            print(response.json())
    except Exception as e:
        print(f"❌ Exception: {e}")


def test_compare_areas():
    """Test area comparison"""
    print("\n" + "="*80)
    print("TEST 2: COMPARE AREAS")
    print("="*80)
    
    payload = {
        "base_features": {
            "country": "Vietnam",
            "area_m2": 100,
            "property_type": "Apartment",
            "year": 2024
        },
        "cities": ["Ho Chi Minh City", "Hanoi", "Da Nang"]
    }
    
    try:
        response = requests.post(f"{BASE_URL}/compare_areas", json=payload)
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Success!")
            print("\nPrice Comparison:")
            for comp in result['comparisons']:
                print(f"  #{comp['rank']} {comp['city']}: ${comp['price']:,.2f}")
            
            print(f"\nMost Expensive: {result['most_expensive']['city']} - ${result['most_expensive']['price']:,.2f}")
            print(f"Cheapest: {result['cheapest']['city']} - ${result['cheapest']['price']:,.2f}")
            print(f"Price Difference: ${result['price_range']['difference']:,.2f} ({result['price_range']['difference_percent']:.1f}%)")
        else:
            print(f"❌ Error: {response.status_code}")
            print(response.json())
    except Exception as e:
        print(f"❌ Exception: {e}")


def test_calculate_roi():
    """Test ROI calculation"""
    print("\n" + "="*80)
    print("TEST 3: CALCULATE ROI")
    print("="*80)
    
    payload = {
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
    }
    
    try:
        response = requests.post(f"{BASE_URL}/calculate_roi", json=payload)
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Success!")
            print(f"\nInvestment Analysis:")
            print(f"  Purchase Price: ${result['purchase_price']:,.2f}")
            print(f"  Predicted Sell Price: ${result['predicted_sell_price']:,.2f}")
            print(f"  Capital Gain: ${result['capital_gain']:,.2f}")
            print(f"  Total Rental Income: ${result['total_rental_income']:,.2f}")
            print(f"  Total Costs: ${result['total_costs']:,.2f}")
            print(f"\nReturns:")
            print(f"  Net Profit: ${result['net_profit']:,.2f}")
            print(f"  ROI: {result['roi_percent']:.2f}%")
            print(f"  Annualized Return: {result['annualized_return']:.2f}%")
            print(f"  Holding Period: {result['holding_period_years']} years")
            print(f"\n  Recommendation: {result['recommendation']}")
        else:
            print(f"❌ Error: {response.status_code}")
            print(response.json())
    except Exception as e:
        print(f"❌ Exception: {e}")


def test_health():
    """Test health endpoint"""
    print("\n" + "="*80)
    print("TEST 0: HEALTH CHECK")
    print("="*80)
    
    try:
        response = requests.get(f"{BASE_URL}/health")
        
        if response.status_code == 200:
            result = response.json()
            print("✅ API is healthy!")
            print(f"  Status: {result['status']}")
            print(f"  Model Loaded: {result['model_loaded']}")
            print(f"  SHAP Available: {result['shap_available']}")
        else:
            print(f"❌ Error: {response.status_code}")
    except Exception as e:
        print(f"❌ Cannot connect to server. Is it running?")
        print(f"   Start server: .venv\\Scripts\\python.exe app.py")


if __name__ == '__main__':
    print("🧪 TESTING ENHANCED API ENDPOINTS")
    print("Make sure Flask server is running on http://localhost:5000")
    print("-" * 80)
    
    # Run tests
    test_health()
    test_predict_trend()
    test_compare_areas()
    test_calculate_roi()
    
    print("\n" + "="*80)
    print("✅ ALL TESTS COMPLETED")
    print("="*80)
