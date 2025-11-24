"""
Script to log current trained models into the logging system
Run this after training models to maintain complete history
"""

import joblib
from pathlib import Path
from logger_config import ModelLogger
import json

def log_saved_model(model_path, model_name=None):
    """Log a saved model's metrics to the logging system"""
    try:
        # Load model
        model_data = joblib.load(model_path)
        
        if not isinstance(model_data, dict):
            print(f"⚠ Model at {model_path} is not in expected dictionary format")
            return False
        
        # Extract information
        if model_name is None:
            model_name = model_data.get('model_name', model_path.stem)
        
        metrics = {
            'mae': model_data.get('mae', 0),
            'rmse': model_data.get('rmse', 0),
            'r2': model_data.get('r2', 0),
            'train_samples': model_data.get('train_samples', 0),
            'test_samples': model_data.get('test_samples', 0),
            'training_time': 0  # Unknown for already trained models
        }
        
        # Extract hyperparameters if available
        hyperparameters = {}
        if 'pipeline' in model_data:
            pipeline = model_data['pipeline']
            if hasattr(pipeline, 'named_steps') and 'regressor' in pipeline.named_steps:
                regressor = pipeline.named_steps['regressor']
                if hasattr(regressor, 'get_params'):
                    hyperparameters = regressor.get_params()
        
        # Prepare notes
        notes = f"Logged from saved model: {model_path.name}"
        if 'feature_names' in model_data:
            notes += f" | Features: {len(model_data['feature_names'])}"
        
        # Log it
        ModelLogger.log_training(
            model_name=model_name,
            metrics=metrics,
            hyperparameters=hyperparameters,
            notes=notes
        )
        
        print(f"✓ Logged {model_name}: RMSE={metrics['rmse']:.2f}, R²={metrics['r2']:.4f}")
        return True
        
    except Exception as e:
        print(f"❌ Error logging {model_path}: {e}")
        return False


def log_all_models_in_folder(folder_path='models'):
    """Log all .joblib models in a folder"""
    folder = Path(folder_path)
    
    if not folder.exists():
        print(f"❌ Folder {folder_path} not found")
        return
    
    model_files = list(folder.glob('*.joblib'))
    
    if not model_files:
        print(f"⚠ No .joblib files found in {folder_path}")
        return
    
    print(f"\n{'='*60}")
    print(f"Logging models from {folder_path}/")
    print(f"{'='*60}\n")
    
    success_count = 0
    for model_file in model_files:
        if log_saved_model(model_file):
            success_count += 1
    
    print(f"\n{'='*60}")
    print(f"Logged {success_count}/{len(model_files)} models successfully")
    print(f"{'='*60}\n")


def log_best_model():
    """Log the current best.joblib model"""
    best_path = Path('models/best.joblib')
    
    if not best_path.exists():
        print("❌ best.joblib not found. Train a model first.")
        return False
    
    print("\n" + "="*60)
    print("Logging Current Best Model")
    print("="*60 + "\n")
    
    success = log_saved_model(best_path, model_name="Best Model (Current)")
    
    if success:
        # Display best model info
        best = ModelLogger.get_best_model()
        if best:
            print("\n" + "="*60)
            print("Current Best Model in History:")
            print("="*60)
            print(f"  Model: {best['model_name']}")
            print(f"  RMSE: {best['rmse']:.2f}")
            print(f"  R²: {best['r2']:.4f}")
            print(f"  MAE: {best['mae']:.2f}")
            print(f"  Trained: {best['timestamp']}")
            print("="*60 + "\n")
    
    return success


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        if sys.argv[1] == '--all':
            # Log all models
            log_all_models_in_folder()
        elif sys.argv[1] == '--best':
            # Log only best model
            log_best_model()
        else:
            # Log specific model
            model_path = Path(sys.argv[1])
            if model_path.exists():
                log_saved_model(model_path)
            else:
                print(f"❌ Model file not found: {sys.argv[1]}")
    else:
        # Default: log best model
        log_best_model()
        
        # Ask if user wants to log all
        print("\nWould you like to log all models in the models/ folder?")
        response = input("Enter 'y' to log all, or press Enter to skip: ").strip().lower()
        if response == 'y':
            log_all_models_in_folder()
