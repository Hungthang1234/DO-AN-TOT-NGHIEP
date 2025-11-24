"""
Train multiple models and compare performance
Save all models with metrics for easy comparison
"""

import numpy as np
import pandas as pd
import joblib
import time
from pathlib import Path
from datetime import datetime

from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error

# Import models
from sklearn.linear_model import LinearRegression, RidgeCV, LassoCV
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor
from sklearn.neighbors import KNeighborsRegressor
from sklearn.neural_network import MLPRegressor

try:
    from xgboost import XGBRegressor
    XGBOOST_AVAILABLE = True
except ImportError:
    XGBOOST_AVAILABLE = False
    print("⚠ XGBoost not available")

try:
    from lightgbm import LGBMRegressor
    LIGHTGBM_AVAILABLE = True
except ImportError:
    LIGHTGBM_AVAILABLE = False
    print("⚠ LightGBM not available")

# Import logger
from logger_config import ModelLogger

# Paths
DATA_PATH = Path("Data/cleaned_real_estate.csv")
MODELS_DIR = Path("models")
MODELS_DIR.mkdir(exist_ok=True)

print("\n" + "="*80)
print("TRAINING MULTIPLE MODELS - FULL COMPARISON")
print("="*80 + "\n")

# Load data
print("📊 Loading data...")
# Sample 50K rows for faster training (especially for slow models like KNN, MLP)
SAMPLE_SIZE = 50000
df = pd.read_csv(DATA_PATH, nrows=SAMPLE_SIZE)
print(f"✓ Loaded {len(df):,} rows (sampled for faster training), {len(df.columns)} columns")

# Prepare features and target
target_col = 'price'
X = df.drop(columns=[target_col])
y = df[target_col]

print(f"Features: {list(X.columns)}")
print(f"Target: {target_col}")

# Split data
print("\n📂 Splitting data (80/20)...")
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)
print(f"✓ Train: {len(X_train):,} samples")
print(f"✓ Test: {len(X_test):,} samples")

# Build preprocessor
print("\n🔧 Building preprocessor...")
numeric_cols = X.select_dtypes(include=[np.number]).columns.tolist()
categorical_cols = X.select_dtypes(exclude=[np.number]).columns.tolist()

print(f"Numeric features: {len(numeric_cols)}")
print(f"Categorical features: {len(categorical_cols)}")

numeric_pipeline = Pipeline([
    ("imputer", SimpleImputer(strategy="median")),
    ("scaler", StandardScaler()),
])

categorical_pipeline = Pipeline([
    ("imputer", SimpleImputer(strategy="most_frequent")),
    ("onehot", OneHotEncoder(handle_unknown="ignore", sparse_output=False)),
])

preprocessor = ColumnTransformer([
    ("num", numeric_pipeline, numeric_cols),
    ("cat", categorical_pipeline, categorical_cols),
])

# Define models to train
models_to_train = [
    ("Linear Regression", LinearRegression(), {}),
    ("Ridge Regression", RidgeCV(alphas=[0.1, 1.0, 10.0]), {}),
    ("Lasso Regression", LassoCV(max_iter=10000), {}),
    ("Decision Tree", DecisionTreeRegressor(max_depth=20, random_state=42), {}),
    ("Random Forest", RandomForestRegressor(n_estimators=100, max_depth=20, random_state=42, n_jobs=-1), {}),
    ("K-Nearest Neighbors", KNeighborsRegressor(n_neighbors=5, n_jobs=-1), {}),
    ("MLP Neural Network", MLPRegressor(hidden_layer_sizes=(100, 50), max_iter=500, random_state=42, early_stopping=True), {}),
]

if XGBOOST_AVAILABLE:
    models_to_train.append(
        ("XGBoost", XGBRegressor(n_estimators=100, max_depth=10, random_state=42, n_jobs=-1), {})
    )

if LIGHTGBM_AVAILABLE:
    models_to_train.append(
        ("LightGBM", LGBMRegressor(n_estimators=100, max_depth=10, random_state=42, n_jobs=-1, verbose=-1), {})
    )

print(f"\n🚀 Training {len(models_to_train)} models...\n")

results = []

for i, (name, model, params) in enumerate(models_to_train, 1):
    print(f"[{i}/{len(models_to_train)}] Training {name}...")
    
    try:
        start_time = time.time()
        
        # Create pipeline
        pipeline = Pipeline([
            ("preprocessor", preprocessor),
            ("regressor", model)
        ])
        
        # Train
        pipeline.fit(X_train, y_train)
        training_time = time.time() - start_time
        
        # Predict
        y_pred = pipeline.predict(X_test)
        
        # Calculate metrics
        rmse = np.sqrt(mean_squared_error(y_test, y_pred))
        r2 = r2_score(y_test, y_pred)
        mae = mean_absolute_error(y_test, y_pred)
        
        # Store results
        result = {
            'model_name': name,
            'rmse': rmse,
            'r2': r2,
            'mae': mae,
            'training_time': training_time,
            'train_samples': len(X_train),
            'test_samples': len(X_test)
        }
        results.append(result)
        
        # Save model with metadata
        model_data = {
            'model_name': name,
            'pipeline': pipeline,
            'rmse': rmse,
            'r2': r2,
            'mae': mae,
            'feature_names': list(X.columns),
            'train_samples': len(X_train),
            'test_samples': len(X_test),
            'training_time': training_time,
            'trained_date': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        
        # Save to file
        model_filename = name.lower().replace(' ', '_') + '_new.joblib'
        model_path = MODELS_DIR / model_filename
        joblib.dump(model_data, model_path)
        
        # Log to training history
        ModelLogger.log_training(
            model_name=name,
            metrics={
                'mae': mae,
                'rmse': rmse,
                'r2': r2,
                'train_samples': len(X_train),
                'test_samples': len(X_test),
                'training_time': training_time
            },
            hyperparameters=params if params else None,
            notes=f"Trained on {datetime.now().strftime('%Y-%m-%d')}"
        )
        
        print(f"   ✓ RMSE: {rmse:,.2f} | R²: {r2:.4f} | MAE: {mae:,.2f} | Time: {training_time:.1f}s")
        print(f"   💾 Saved to: {model_filename}")
        
    except Exception as e:
        print(f"   ❌ Error: {str(e)}")
        results.append({
            'model_name': name,
            'rmse': None,
            'r2': None,
            'mae': None,
            'training_time': None,
            'error': str(e)
        })
    
    print()

# Results summary
print("\n" + "="*80)
print("RESULTS SUMMARY")
print("="*80 + "\n")

results_df = pd.DataFrame([r for r in results if r['r2'] is not None])
if len(results_df) > 0:
    results_df = results_df.sort_values('r2', ascending=False)
    
    print(f"{'Model':<25} {'RMSE':<15} {'R²':<10} {'MAE':<15} {'Time (s)':<10}")
    print("-"*80)
    
    for idx, row in results_df.iterrows():
        marker = "⭐" if idx == results_df.index[0] else "  "
        print(f"{row['model_name']:<25} {row['rmse']:>13,.2f} {row['r2']:>9.4f} {row['mae']:>13,.2f} {row['training_time']:>9.1f} {marker}")
    
    # Best model
    best = results_df.iloc[0]
    print("\n" + "="*80)
    print("🏆 BEST MODEL")
    print("="*80)
    print(f"Model: {best['model_name']}")
    print(f"RMSE: {best['rmse']:,.2f}")
    print(f"R²: {best['r2']:.4f}")
    print(f"MAE: {best['mae']:,.2f}")
    print(f"Training Time: {best['training_time']:.1f}s")
    
    # Save best model as best_new.joblib
    best_model_name = best['model_name'].lower().replace(' ', '_') + '_new.joblib'
    best_model_path = MODELS_DIR / best_model_name
    
    if best_model_path.exists():
        best_model_data = joblib.load(best_model_path)
        joblib.dump(best_model_data, MODELS_DIR / 'best_new.joblib')
        print(f"\n💾 Best model also saved as: best_new.joblib")

# Failed models
failed = [r for r in results if r['r2'] is None]
if failed:
    print("\n" + "="*80)
    print("❌ FAILED MODELS")
    print("="*80)
    for r in failed:
        print(f"  • {r['model_name']}: {r.get('error', 'Unknown error')}")

print("\n" + "="*80)
print(f"✅ Training completed! Results saved to models/ directory")
print(f"📊 Check logs/model_training.csv for detailed history")
print("="*80 + "\n")
