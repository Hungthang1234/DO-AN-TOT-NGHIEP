"""
View all models information regardless of sklearn version
"""
import joblib
import pandas as pd
from pathlib import Path
import warnings
warnings.filterwarnings('ignore')

models_dir = Path('models')

print("\n" + "="*80)
print("TOÀN BỘ MODELS ĐÃ HUẤN LUYỆN")
print("="*80 + "\n")

models_info = []

for model_file in sorted(models_dir.glob('*.joblib')):
    try:
        print(f"📦 {model_file.name}")
        
        # Try to load
        model_data = joblib.load(model_file)
        
        if isinstance(model_data, dict):
            # New format with metrics
            info = {
                'file': model_file.name,
                'name': model_data.get('model_name', 'Unknown'),
                'rmse': model_data.get('rmse', 'N/A'),
                'r2': model_data.get('r2', 'N/A'),
                'mae': model_data.get('mae', 'N/A'),
                'features': len(model_data.get('feature_names', [])),
                'status': '✅ With Metrics'
            }
            models_info.append(info)
            print(f"   Model: {info['name']}")
            print(f"   RMSE: {info['rmse']}")
            print(f"   R²: {info['r2']}")
            print(f"   Features: {info['features']}")
            print(f"   {info['status']}")
        else:
            # Old format - just the model object
            model_name = type(model_data).__name__
            if hasattr(model_data, 'named_steps'):
                # It's a pipeline
                if 'regressor' in model_data.named_steps:
                    model_name = type(model_data.named_steps['regressor']).__name__
            
            info = {
                'file': model_file.name,
                'name': model_name,
                'rmse': 'Not stored',
                'r2': 'Not stored',
                'mae': 'Not stored',
                'features': 'Unknown',
                'status': '⚠️ Old Format (No Metrics)'
            }
            models_info.append(info)
            print(f"   Model: {info['name']}")
            print(f"   {info['status']}")
        
        print()
        
    except Exception as e:
        print(f"   ❌ Error: {str(e)[:100]}")
        print()

# Summary table
print("\n" + "="*80)
print("BẢNG TỔNG KẾT")
print("="*80)

if models_info:
    df = pd.DataFrame(models_info)
    print(f"\n{'File':<25} {'Model':<20} {'RMSE':<15} {'R²':<10} {'Status':<25}")
    print("-"*100)
    
    for _, row in df.iterrows():
        rmse_str = f"{row['rmse']:,.2f}" if isinstance(row['rmse'], (int, float)) else str(row['rmse'])
        r2_str = f"{row['r2']:.4f}" if isinstance(row['r2'], (int, float)) else str(row['r2'])
        print(f"{row['file']:<25} {row['name']:<20} {rmse_str:<15} {r2_str:<10} {row['status']:<25}")

print("\n" + "="*80)
print(f"Tổng số models: {len(models_info)}")
print(f"Models có metrics: {sum(1 for m in models_info if 'With Metrics' in m['status'])}")
print(f"Models không có metrics: {sum(1 for m in models_info if 'Old Format' in m['status'])}")
print("="*80 + "\n")

# Best model
best_models = [m for m in models_info if isinstance(m['r2'], (int, float))]
if best_models:
    best = max(best_models, key=lambda x: x['r2'])
    print("🏆 BEST MODEL:")
    print(f"   File: {best['file']}")
    print(f"   Model: {best['name']}")
    print(f"   RMSE: {best['rmse']:,.2f}")
    print(f"   R²: {best['r2']:.4f}")
    print()
