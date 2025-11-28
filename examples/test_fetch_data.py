# Example: Test Singapore HDB API (FREE)
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from scripts.fetch_external_data import RealEstateAPIClient

client = RealEstateAPIClient()

print("Fetching Singapore HDB data for June 2024...")
df = client.fetch_singapore_hdb_data(year=2024, month=6)

print(f"\nFetched {len(df)} records")
print(f"Columns: {list(df.columns)}")
print("\nFirst 5 records:")
print(df.head())

# Save to CSV
df.to_csv('Data/singapore_test.csv', index=False)
print(f"\n✅ Saved to Data/singapore_test.csv")
