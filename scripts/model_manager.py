"""
Model Manager - Switch between different trained models
Train new models with external API data
"""

import joblib
import pandas as pd
import numpy as np
from pathlib import Path
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error
import lightgbm as lgb
import xgboost as xgb
from datetime import datetime
import json

class ModelManager:
    """Manage multiple models and switch between them"""
    
    def __init__(self, models_dir='models'):
        self.models_dir = Path(models_dir)
        self.models_dir.mkdir(exist_ok=True)
        
        self.config_file = self.models_dir / 'models_config.json'
        self.models_config = self.load_config()
    
    def load_config(self):
        """Load models configuration"""
        if self.config_file.exists():
            with open(self.config_file, 'r') as f:
                return json.load(f)
        return {'models': [], 'active_model': None}
    
    def save_config(self):
        """Save models configuration"""
        with open(self.config_file, 'w') as f:
            json.dump(self.models_config, f, indent=2)
    
    def list_available_models(self):
        """List all available models"""
        models = []
        for model_file in self.models_dir.glob('*.joblib'):
            try:
                model_data = joblib.load(model_file)
                if isinstance(model_data, dict):
                    models.append({
                        'name': model_file.stem,
                        'file': model_file.name,
                        'type': model_data.get('model_name', 'Unknown'),
                        'features': len(model_data.get('feature_names', [])),
                        'r2': model_data.get('r2', 0),
                        'rmse': model_data.get('rmse', 0),
                        'trained_date': model_data.get('trained_date', 'Unknown')
                    })
            except:
                pass
        
        return sorted(models, key=lambda x: x['r2'], reverse=True)
    
    def train_new_model(self, data_file, model_name, model_type='lightgbm', features=None):
        """
        Train a new model with external API data
        
        Args:
            data_file: Path to CSV file with data
            model_name: Name for the new model
            model_type: 'lightgbm', 'xgboost', or 'random_forest'
            features: List of feature columns to use (auto-detect if None)
        """
        print(f"\n{'='*60}")
        print(f"Training new {model_type.upper()} model: {model_name}")
        print(f"{'='*60}\n")
        
        # Load data
        df = pd.read_csv(data_file)
        print(f"Loaded {len(df)} records from {data_file}")
        print(f"Columns: {list(df.columns)}")
        
        # Auto-detect features if not provided
        if features is None:
            features = [col for col in df.columns if col not in ['price', 'source', 'date']]
        
        print(f"\nUsing features: {features}")
        
        # Prepare data
        X = df[features].copy()
        y = df['price'].copy()
        
        # Encode categorical features
        label_encoders = {}
        for col in X.select_dtypes(include=['object']).columns:
            le = LabelEncoder()
            X[col] = le.fit_transform(X[col].astype(str))
            label_encoders[col] = le
        
        # Handle missing values
        X = X.fillna(X.median())
        
        # Split data
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42
        )
        
        print(f"\nTrain size: {len(X_train)}, Test size: {len(X_test)}")
        
        # Train model based on type
        if model_type == 'lightgbm':
            model = self._train_lightgbm(X_train, y_train, X_test, y_test)
        elif model_type == 'xgboost':
            model = self._train_xgboost(X_train, y_train, X_test, y_test)
        else:
            raise ValueError(f"Unknown model type: {model_type}")
        
        # Evaluate
        train_pred = model.predict(X_train)
        test_pred = model.predict(X_test)
        
        train_r2 = r2_score(y_train, train_pred)
        test_r2 = r2_score(y_test, test_pred)
        train_rmse = np.sqrt(mean_squared_error(y_train, train_pred))
        test_rmse = np.sqrt(mean_squared_error(y_test, test_pred))
        test_mae = mean_absolute_error(y_test, test_pred)
        
        print(f"\n{'='*60}")
        print("Model Performance:")
        print(f"{'='*60}")
        print(f"Train R²:  {train_r2:.4f}")
        print(f"Test R²:   {test_r2:.4f}")
        print(f"Train RMSE: ${train_rmse:,.2f}")
        print(f"Test RMSE:  ${test_rmse:,.2f}")
        print(f"Test MAE:   ${test_mae:,.2f}")
        print(f"{'='*60}\n")
        
        # Save model
        model_data = {
            'model': model,
            'model_name': f'{model_type.upper()} ({model_name})',
            'feature_names': features,
            'label_encoders': label_encoders,
            'r2': test_r2,
            'rmse': test_rmse,
            'mae': test_mae,
            'train_r2': train_r2,
            'train_rmse': train_rmse,
            'train_samples': len(X_train),
            'test_samples': len(X_test),
            'trained_date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'data_source': str(data_file),
            'target': 'price'
        }
        
        output_file = self.models_dir / f'{model_name}.joblib'
        joblib.dump(model_data, output_file)
        print(f"✅ Model saved to: {output_file}")
        
        # Update config
        self.models_config['models'].append({
            'name': model_name,
            'type': model_type,
            'r2': test_r2,
            'rmse': test_rmse,
            'created': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        })
        self.save_config()
        
        return model_data
    
    def _train_lightgbm(self, X_train, y_train, X_test, y_test):
        """Train LightGBM model"""
        print("\nTraining LightGBM...")
        
        model = lgb.LGBMRegressor(
            n_estimators=1000,
            learning_rate=0.05,
            max_depth=10,
            num_leaves=31,
            min_child_samples=20,
            subsample=0.8,
            colsample_bytree=0.8,
            random_state=42,
            n_jobs=-1,
            verbose=-1
        )
        
        model.fit(
            X_train, y_train,
            eval_set=[(X_test, y_test)],
            eval_metric='rmse',
            callbacks=[lgb.early_stopping(50), lgb.log_evaluation(100)]
        )
        
        return model
    
    def _train_xgboost(self, X_train, y_train, X_test, y_test):
        """Train XGBoost model"""
        print("\nTraining XGBoost...")
        
        model = xgb.XGBRegressor(
            n_estimators=1000,
            learning_rate=0.05,
            max_depth=10,
            subsample=0.8,
            colsample_bytree=0.8,
            random_state=42,
            n_jobs=-1
        )
        
        model.fit(
            X_train, y_train,
            eval_set=[(X_test, y_test)],
            early_stopping_rounds=50,
            verbose=100
        )
        
        return model
    
    def set_active_model(self, model_name):
        """Set a model as active"""
        model_file = self.models_dir / f'{model_name}.joblib'
        
        if not model_file.exists():
            print(f"❌ Model not found: {model_name}")
            return False
        
        # Copy to best_clean.joblib (active model)
        import shutil
        active_model = self.models_dir / 'best_clean.joblib'
        
        # Skip if already active (same file)
        if model_file.resolve() == active_model.resolve():
            print(f"ℹ️  Model '{model_name}' is already active")
            return True
        
        shutil.copy(model_file, active_model)
        
        self.models_config['active_model'] = model_name
        self.save_config()
        
        print(f"✅ Set active model to: {model_name}")
        return True
    
    def compare_models(self, model_names=None):
        """Compare multiple models"""
        if model_names is None:
            # Compare all models
            model_names = [m['name'] for m in self.list_available_models()]
        
        results = []
        for name in model_names:
            model_file = self.models_dir / f'{name}.joblib'
            if model_file.exists():
                try:
                    model_data = joblib.load(model_file)
                    results.append({
                        'Model': name,
                        'Type': model_data.get('model_name', 'Unknown'),
                        'R²': f"{model_data.get('r2', 0):.4f}",
                        'RMSE': f"${model_data.get('rmse', 0):,.2f}",
                        'Features': len(model_data.get('feature_names', [])),
                        'Date': model_data.get('trained_date', 'Unknown')
                    })
                except:
                    pass
        
        return pd.DataFrame(results)


# ==================== EXAMPLE USAGE ====================
if __name__ == "__main__":
    manager = ModelManager()
    
    # Example 1: List available models
    print("\n=== Available Models ===")
    models = manager.list_available_models()
    for model in models:
        print(f"{model['name']:30} - R²: {model['r2']:.4f}, RMSE: ${model['rmse']:,.2f}")
    
    # Example 2: Train new model with external data
    # Uncomment to train
    """
    data_file = 'Data/api_combined_20241125.csv'
    model_name = 'external_api_model'
    
    model_data = manager.train_new_model(
        data_file=data_file,
        model_name=model_name,
        model_type='lightgbm'
    )
    """
    
    # Example 3: Set active model
    # manager.set_active_model('external_api_model')
    
    # Example 4: Compare models
    print("\n=== Model Comparison ===")
    comparison = manager.compare_models()
    print(comparison.to_string(index=False))
