import requests
import json

url = "http://localhost:5000/predict"

# Base test data
base_data = {
    "country": "Singapore",
    "city": "ANG MO KIO",
    "year": "2023",
    "month": "1",
    "area_m2": "100"
}

# Test with different property types
property_types = ["1 ROOM", "2 ROOM", "3 ROOM", "4 ROOM", "5 ROOM", "EXECUTIVE", "MULTI-GENERATION"]

print("Testing predictions with different Property Types:")
print("=" * 80)

for prop_type in property_types:
    test_data = base_data.copy()
    test_data["property_type"] = prop_type
    
    print(f"\nProperty Type: {prop_type}")
    print(f"Request data: {json.dumps(test_data, indent=2)}")
    
    try:
        response = requests.post(
            url,
            json=test_data,
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 200:
            result = response.json()
            print(f"✓ Prediction: ${result['prediction']:,.2f}")
        else:
            print(f"✗ Error: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"✗ Exception: {e}")

print("\n" + "=" * 80)
print("\nSummary: Check if predictions above are different for each Property Type")
