"""Quick test to verify Advanced Charts is working"""
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def test_advanced_charts():
    """Test if Advanced Charts API endpoints exist"""
    try:
        from enhancements.advanced_charts_api import advanced_charts_bp
        print("✓ Advanced Charts Blueprint imported successfully")
        print(f"  Blueprint name: {advanced_charts_bp.name}")
        print(f"  URL prefix: {advanced_charts_bp.url_prefix}")
        
        # Check routes
        routes = [rule.rule for rule in advanced_charts_bp.url_map.iter_rules() if 'charts' in rule.rule]
        if routes:
            print(f"\n✓ Found {len(routes)} chart routes")
        else:
            print("\n⚠ No routes found in blueprint")
        
        return True
    except Exception as e:
        print(f"✗ Error: {e}")
        return False

def test_dataset():
    """Test if dataset exists"""
    import pandas as pd
    try:
        df = pd.read_csv('Data/cleaned_real_estate.csv')
        print(f"\n✓ Dataset loaded: {len(df):,} records")
        print(f"  Countries: {df['country'].nunique()}")
        print(f"  Property types: {df['property_type'].nunique()}")
        return True
    except Exception as e:
        print(f"\n✗ Dataset error: {e}")
        return False

def test_template():
    """Check if template has visualization tab"""
    try:
        with open('templates/index.html', 'r', encoding='utf-8') as f:
            content = f.read()
            
        checks = {
            'visualization-tab': 'visualization-tab' in content,
            'loadVisualization': 'loadVisualization()' in content,
            'vizContent': 'vizContent' in content,
            'switchTab': "'visualization'" in content
        }
        
        print("\n✓ Template checks:")
        for name, result in checks.items():
            status = "✓" if result else "✗"
            print(f"  {status} {name}: {result}")
        
        return all(checks.values())
    except Exception as e:
        print(f"\n✗ Template error: {e}")
        return False

if __name__ == "__main__":
    print("="*50)
    print("ADVANCED CHARTS VERIFICATION")
    print("="*50)
    
    results = []
    results.append(("Blueprint", test_advanced_charts()))
    results.append(("Dataset", test_dataset()))
    results.append(("Template", test_template()))
    
    print("\n" + "="*50)
    print("SUMMARY")
    print("="*50)
    
    for name, result in results:
        status = "✓" if result else "✗"
        print(f"{status} {name}: {'PASS' if result else 'FAIL'}")
    
    if all(r[1] for r in results):
        print("\n✓ All checks passed! Advanced Charts should work.")
        print("\nTo test in browser:")
        print("1. Start app: python app.py")
        print("2. Open: http://127.0.0.1:5000")
        print("3. Click 'Advanced Charts' tab")
        print("4. Charts should auto-load")
        sys.exit(0)
    else:
        print("\n✗ Some checks failed. See errors above.")
        sys.exit(1)
