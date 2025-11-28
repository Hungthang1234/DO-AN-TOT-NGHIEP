"""
Ensemble Stacking Model - Kết hợp nhiều models để tăng độ chính xác
Combines LightGBM + XGBoost + CatBoost with Ridge meta-learner
Target: R² from 0.9245 → 0.94+
"""

import pandas as pd
import numpy as np
import joblib
from pathlib import Path
from datetime import datetime
from sklearn.model_selection import train_test_split, KFold
from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error
from sklearn.linear_model import Ridge
from sklearn.preprocessing import LabelEncoder
import lightgbm as lgb
import xgboost as xgb

try:
    import catboost as cb
    CATBOOST_AVAILABLE = True
except ImportError:
    CATBOOST_AVAILABLE = False
    print("⚠️  CatBoost not installed. Using LightGBM + XGBoost only")

import warnings
warnings.filterwarnings('ignore')


class EnsembleStackingModel:
    """Stacking ensemble with cross-validation"""
    
    def __init__(self, n_folds=5):
        self.n_folds = n_folds
        self.base_models = []
        self.meta_model = None
        self.feature_names = None
        self.label_encoders = {}
        
    def _get_base_models(self):
        """Define base models"""
        models = [
            ('lightgbm', lgb.LGBMRegressor(
                n_estimators=2000,
                learning_rate=0.02,
                max_depth=8,
                num_leaves=50,
                subsample=0.8,
                colsample_bytree=0.8,
                min_child_samples=20,
                reg_alpha=0.1,
                reg_lambda=0.1,
                random_state=42,
                verbose=-1
            )),
            ('xgboost', xgb.XGBRegressor(
                n_estimators=2000,
                learning_rate=0.02,
                max_depth=8,
                subsample=0.8,
                colsample_bytree=0.8,
                min_child_weight=3,
                gamma=0.1,
                reg_alpha=0.1,
                reg_lambda=0.1,
                random_state=42,
                tree_method='hist'
            ))
        ]
        
        if CATBOOST_AVAILABLE:
            models.append((
                'catboost', cb.CatBoostRegressor(
                    iterations=2000,
                    learning_rate=0.02,
                    depth=8,
                    subsample=0.8,
                    colsample_bylevel=0.8,
                    min_data_in_leaf=20,
                    l2_leaf_reg=3,
                    random_state=42,
                    verbose=False
                )
            ))
        
        return models
    
    def _prepare_features(self, df, fit=False):
        """Encode categorical features"""
        df = df.copy()
        categorical_cols = df.select_dtypes(include=['object']).columns
        
        for col in categorical_cols:
            if fit:
                le = LabelEncoder()
                df[col] = le.fit_transform(df[col].astype(str))
                self.label_encoders[col] = le
            else:
                if col in self.label_encoders:
                    # Handle unseen labels
                    le = self.label_encoders[col]
                    df[col] = df[col].astype(str).map(
                        lambda x: le.transform([x])[0] if x in le.classes_ else -1
                    )
        
        return df
    
    def fit(self, X, y):
        """Train stacking ensemble with cross-validation"""
        print("=" * 80)
        print("🚀 TRAINING ENSEMBLE STACKING MODEL")
        print("=" * 80)
        
        self.feature_names = list(X.columns)
        X_encoded = self._prepare_features(X, fit=True)
        
        # Prepare meta-features
        meta_features = np.zeros((X_encoded.shape[0], len(self._get_base_models())))
        
        # K-Fold cross-validation
        kf = KFold(n_splits=self.n_folds, shuffle=True, random_state=42)
        
        base_models_list = self._get_base_models()
        
        print(f"\n📊 Training {len(base_models_list)} base models with {self.n_folds}-fold CV...")
        
        for model_idx, (model_name, model) in enumerate(base_models_list):
            print(f"\n  [{model_idx + 1}/{len(base_models_list)}] Training {model_name.upper()}...")
            
            fold_predictions = []
            
            for fold_idx, (train_idx, val_idx) in enumerate(kf.split(X_encoded)):
                X_train_fold, X_val_fold = X_encoded.iloc[train_idx], X_encoded.iloc[val_idx]
                y_train_fold, y_val_fold = y.iloc[train_idx], y.iloc[val_idx]
                
                # Train model on fold
                model_clone = model.__class__(**model.get_params())
                model_clone.fit(X_train_fold, y_train_fold)
                
                # Predict on validation fold
                val_preds = model_clone.predict(X_val_fold)
                meta_features[val_idx, model_idx] = val_preds
                
                # Calculate fold metrics
                fold_r2 = r2_score(y_val_fold, val_preds)
                fold_rmse = np.sqrt(mean_squared_error(y_val_fold, val_preds))
                
                print(f"      Fold {fold_idx + 1}/{self.n_folds}: R² = {fold_r2:.4f}, RMSE = {fold_rmse:,.0f}")
            
            # Train final base model on full data
            final_model = model.__class__(**model.get_params())
            final_model.fit(X_encoded, y)
            self.base_models.append((model_name, final_model))
            
            # Overall base model performance
            overall_preds = meta_features[:, model_idx]
            overall_r2 = r2_score(y, overall_preds)
            overall_rmse = np.sqrt(mean_squared_error(y, overall_preds))
            print(f"      ✅ {model_name.upper()} Overall: R² = {overall_r2:.4f}, RMSE = {overall_rmse:,.0f}")
        
        # Train meta-model (Ridge regression)
        print(f"\n🎯 Training meta-model (Ridge)...")
        self.meta_model = Ridge(alpha=1.0)
        self.meta_model.fit(meta_features, y)
        
        # Final ensemble predictions
        final_preds = self.meta_model.predict(meta_features)
        final_r2 = r2_score(y, final_preds)
        final_rmse = np.sqrt(mean_squared_error(y, final_preds))
        final_mae = mean_absolute_error(y, final_preds)
        
        print("\n" + "=" * 80)
        print("🏆 ENSEMBLE STACKING RESULTS")
        print("=" * 80)
        print(f"  R² Score:  {final_r2:.4f}")
        print(f"  RMSE:      {final_rmse:,.2f}")
        print(f"  MAE:       {final_mae:,.2f}")
        print("=" * 80)
        
        return self
    
    def predict(self, X):
        """Make predictions using stacking ensemble"""
        X_encoded = self._prepare_features(X, fit=False)
        
        # Get predictions from base models
        base_predictions = np.column_stack([
            model.predict(X_encoded) for _, model in self.base_models
        ])
        
        # Meta-model prediction
        final_predictions = self.meta_model.predict(base_predictions)
        
        return final_predictions
    
    def save(self, filepath):
        """Save ensemble model"""
        model_data = {
            'base_models': self.base_models,
            'meta_model': self.meta_model,
            'feature_names': self.feature_names,
            'label_encoders': self.label_encoders,
            'n_folds': self.n_folds,
            'model_name': 'Ensemble Stacking',
            'trained_date': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        joblib.dump(model_data, filepath)
        print(f"✅ Model saved to: {filepath}")
    
    @classmethod
    def load(cls, filepath):
        """Load ensemble model"""
        model_data = joblib.load(filepath)
        
        instance = cls(n_folds=model_data['n_folds'])
        instance.base_models = model_data['base_models']
        instance.meta_model = model_data['meta_model']
        instance.feature_names = model_data['feature_names']
        instance.label_encoders = model_data['label_encoders']
        
        return instance


def train_ensemble_model(data_path, output_path=None, test_size=0.2):
    """
    Train ensemble stacking model
    
    Args:
        data_path: Path to cleaned_real_estate.csv
        output_path: Path to save model (default: models/ensemble_stacking.joblib)
        test_size: Test set ratio
    """
    print("\n📂 Loading dataset...")
    df = pd.read_csv(data_path)
    print(f"   Dataset: {len(df):,} rows")
    
    # Drop price_per_m2 to avoid leakage
    if 'price_per_m2' in df.columns:
        df = df.drop(columns=['price_per_m2'])
    
    # Prepare features and target
    if 'price' in df.columns:
        X = df.drop(columns=['price'])
        y = df['price']
    else:
        raise ValueError("Dataset must contain 'price' column")
    
    # Train-test split
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=test_size, random_state=42
    )
    
    print(f"   Train: {len(X_train):,} | Test: {len(X_test):,}")
    
    # Train ensemble
    ensemble = EnsembleStackingModel(n_folds=5)
    ensemble.fit(X_train, y_train)
    
    # Evaluate on test set
    print("\n" + "=" * 80)
    print("📊 TEST SET EVALUATION")
    print("=" * 80)
    
    y_pred = ensemble.predict(X_test)
    test_r2 = r2_score(y_test, y_pred)
    test_rmse = np.sqrt(mean_squared_error(y_test, y_pred))
    test_mae = mean_absolute_error(y_test, y_pred)
    
    print(f"  Test R²:   {test_r2:.4f}")
    print(f"  Test RMSE: {test_rmse:,.2f}")
    print(f"  Test MAE:  {test_mae:,.2f}")
    print("=" * 80)
    
    # Save model
    if output_path is None:
        output_path = Path(__file__).parent.parent.parent / 'models' / 'ensemble_stacking.joblib'
    
    ensemble.save(output_path)
    
    return ensemble, test_r2, test_rmse


if __name__ == '__main__':
    # Train model
    data_path = Path(__file__).parent.parent.parent / 'Data' / 'cleaned_real_estate.csv'
    
    if not data_path.exists():
        print(f"❌ Data file not found: {data_path}")
        exit(1)
    
    ensemble, test_r2, test_rmse = train_ensemble_model(data_path)
    
    print(f"\n✅ Training completed!")
    print(f"   Test R²: {test_r2:.4f}")
    print(f"   Test RMSE: {test_rmse:,.2f}")
