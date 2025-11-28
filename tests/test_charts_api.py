"""Test script for Advanced Charts API endpoints"""
import pandas as pd
import sys

def test_dataset():
    """Check dataset structure"""
    try:
        df = pd.read_csv('Data/cleaned_real_estate.csv')
        print(f"✓ Dataset loaded: {len(df):,} records")
        print(f"✓ Columns: {list(df.columns)[:10]}")
        
        if 'year' in df.columns:
            print(f"✓ Year range: {df['year'].min()} - {df['year'].max()}")
        if 'country' in df.columns:
            print(f"✓ Countries: {df['country'].nunique()} unique")
        if 'property_type' in df.columns:
            print(f"✓ Property types: {df['property_type'].nunique()} unique")
        
        return True
    except Exception as e:
        print(f"✗ Error: {e}")
        return False

if __name__ == "__main__":
    print("Testing Advanced Charts API data source...\n")
    if test_dataset():
        print("\n✓ Dataset ready for Advanced Charts API")
        sys.exit(0)
    else:
        print("\n✗ Dataset issues detected")
        sys.exit(1)
