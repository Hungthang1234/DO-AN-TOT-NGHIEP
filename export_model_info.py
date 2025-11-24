"""
Export all model metrics and information to a comprehensive report
This allows you to quickly reference model performance without retraining
"""

import joblib
import json
import pandas as pd
from pathlib import Path
from datetime import datetime

def export_all_models_info(output_file='model_metrics_report.json'):
    """Export all model information to JSON file"""
    
    models_dir = Path('models')
    report = {
        'generated_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'models': [],
        'best_model': None,
        'summary': {}
    }
    
    if not models_dir.exists():
        print(f"❌ Models directory not found: {models_dir}")
        return
    
    print("\n" + "="*70)
    print("EXPORTING MODEL METRICS REPORT")
    print("="*70 + "\n")
    
    model_files = list(models_dir.glob('*.joblib'))
    
    if not model_files:
        print("⚠ No model files found")
        return
    
    best_r2 = -999999
    
    for model_path in model_files:
        try:
            print(f"Processing: {model_path.name}")
            model_data = joblib.load(model_path)
            
            if isinstance(model_data, dict):
                model_info = {
                    'file_name': model_path.name,
                    'model_name': model_data.get('model_name', 'Unknown'),
                    'metrics': {
                        'rmse': float(model_data.get('rmse', 0)),
                        'r2': float(model_data.get('r2', 0)),
                        'mae': float(model_data.get('mae', 0))
                    },
                    'features': model_data.get('feature_names', []),
                    'feature_count': len(model_data.get('feature_names', [])),
                    'training_samples': model_data.get('train_samples', 0),
                    'test_samples': model_data.get('test_samples', 0)
                }
                
                report['models'].append(model_info)
                
                # Track best model
                r2_score = model_info['metrics']['r2']
                if r2_score > best_r2:
                    best_r2 = r2_score
                    report['best_model'] = model_info
                
                print(f"  ✓ {model_info['model_name']}: R²={r2_score:.4f}, RMSE={model_info['metrics']['rmse']:.2f}")
            else:
                print(f"  ⚠ Skipped (not in expected format)")
                
        except Exception as e:
            print(f"  ❌ Error: {e}")
    
    # Add summary
    if report['models']:
        report['summary'] = {
            'total_models': len(report['models']),
            'model_names': [m['model_name'] for m in report['models']],
            'best_model_name': report['best_model']['model_name'] if report['best_model'] else None,
            'best_r2': best_r2 if best_r2 > -999999 else None
        }
    
    # Save report
    output_path = Path(output_file)
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(report, f, indent=2, ensure_ascii=False)
    
    print(f"\n{'='*70}")
    print(f"✓ Report saved to: {output_path}")
    print(f"{'='*70}\n")
    
    # Print summary
    print("SUMMARY:")
    print(f"  Total models: {report['summary'].get('total_models', 0)}")
    if report['best_model']:
        print(f"  Best model: {report['best_model']['model_name']}")
        print(f"  Best R²: {report['best_model']['metrics']['r2']:.4f}")
        print(f"  Best RMSE: {report['best_model']['metrics']['rmse']:.2f}")
    print("")
    
    return report


def print_model_comparison():
    """Print a comparison table of all models"""
    models_dir = Path('models')
    
    if not models_dir.exists():
        print("❌ Models directory not found")
        return
    
    model_files = list(models_dir.glob('*.joblib'))
    
    if not model_files:
        print("⚠ No model files found")
        return
    
    print("\n" + "="*100)
    print("MODEL COMPARISON TABLE")
    print("="*100)
    print(f"{'Model Name':<25} {'RMSE':<15} {'R²':<10} {'MAE':<15} {'Features':<10}")
    print("-"*100)
    
    models_info = []
    
    for model_path in model_files:
        try:
            model_data = joblib.load(model_path)
            
            if isinstance(model_data, dict):
                name = model_data.get('model_name', 'Unknown')
                rmse = model_data.get('rmse', 0)
                r2 = model_data.get('r2', 0)
                mae = model_data.get('mae', 0)
                features = len(model_data.get('feature_names', []))
                
                models_info.append({
                    'name': name,
                    'rmse': rmse,
                    'r2': r2,
                    'mae': mae,
                    'features': features
                })
                
        except Exception as e:
            pass
    
    # Sort by R² (descending)
    models_info.sort(key=lambda x: x['r2'], reverse=True)
    
    for i, model in enumerate(models_info, 1):
        best_marker = " ⭐" if i == 1 else ""
        print(f"{model['name']:<25} {model['rmse']:<15,.2f} {model['r2']:<10.4f} {model['mae']:<15,.2f} {model['features']:<10}{best_marker}")
    
    print("="*100 + "\n")


def create_quick_reference():
    """Create a quick reference text file"""
    models_dir = Path('models')
    
    if not models_dir.exists():
        return
    
    output = []
    output.append("="*70)
    output.append("HOUSE PRICE PREDICTION - MODEL QUICK REFERENCE")
    output.append("="*70)
    output.append(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    output.append("")
    
    # Find best model
    best_model_path = models_dir / 'best.joblib'
    if best_model_path.exists():
        try:
            model_data = joblib.load(best_model_path)
            if isinstance(model_data, dict):
                output.append("CURRENT BEST MODEL:")
                output.append(f"  Name: {model_data.get('model_name', 'Unknown')}")
                output.append(f"  RMSE: {model_data.get('rmse', 0):,.2f}")
                output.append(f"  R²: {model_data.get('r2', 0):.4f}")
                output.append(f"  MAE: {model_data.get('mae', 0):,.2f}")
                output.append(f"  Features: {len(model_data.get('feature_names', []))}")
                output.append(f"  Feature List: {', '.join(model_data.get('feature_names', []))}")
                output.append("")
        except:
            pass
    
    output.append("AVAILABLE MODELS:")
    
    model_files = list(models_dir.glob('*.joblib'))
    for model_path in sorted(model_files):
        try:
            model_data = joblib.load(model_path)
            if isinstance(model_data, dict):
                output.append(f"\n  • {model_path.name}")
                output.append(f"    Model: {model_data.get('model_name', 'Unknown')}")
                output.append(f"    RMSE: {model_data.get('rmse', 0):,.2f}")
                output.append(f"    R²: {model_data.get('r2', 0):.4f}")
        except:
            pass
    
    output.append("\n" + "="*70)
    output.append("HOW TO USE:")
    output.append("  1. Start web app: python app.py")
    output.append("  2. Open browser: http://localhost:5000")
    output.append("  3. Model loads automatically from models/best.joblib")
    output.append("  4. No need to retrain - all metrics are saved!")
    output.append("="*70)
    
    # Save to file
    with open('MODEL_REFERENCE.txt', 'w', encoding='utf-8') as f:
        f.write('\n'.join(output))
    
    print("✓ Quick reference saved to MODEL_REFERENCE.txt")
    
    # Also print to console
    print('\n'.join(output))


if __name__ == "__main__":
    print("\n🔍 Exporting Model Information...\n")
    
    # 1. Export JSON report
    export_all_models_info()
    
    # 2. Print comparison table
    print_model_comparison()
    
    # 3. Create quick reference
    create_quick_reference()
    
    print("\n✅ All model information exported successfully!")
    print("\nFiles created:")
    print("  • model_metrics_report.json - Complete metrics report")
    print("  • MODEL_REFERENCE.txt - Quick reference guide")
    print("\nYou can now start the web app without retraining!")
    print("Just run: python app.py\n")
