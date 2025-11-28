"""Simple test to check if enhancement APIs work"""
import sys
from pathlib import Path

print("Testing API imports...")

try:
    sys.path.insert(0, str(Path(__file__).parent))
    from api.endpoints import api_bp
    print("✅ API blueprint imported successfully")
    print(f"   Routes: {[r.rule for r in api_bp.url_map._rules if 'api' in r.rule][:5]}")
except Exception as e:
    print(f"❌ Error importing API: {e}")
    import traceback
    traceback.print_exc()
