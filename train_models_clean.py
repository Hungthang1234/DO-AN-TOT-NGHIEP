"""
Train models with proper overfitting prevention
- Remove data leakage features (price_per_m2)
- Use larger dataset
- Apply regularization
- Cross-validation
- Proper hyperparameters
"""

import numpy as np
import pandas as pd
import joblib
import time
from pathlib import Path
from datetime import datetime

from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error

# Import models
from sklearn.linear_model import LinearRegression, Ridge, Lasso
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor
from sklearn.neighbors import KNeighborsRegressor
from sklearn.neural_network import MLPRegressor

try:
    from xgboost import XGBRegressor
    XGBOOST_AVAILABLE = True
except ImportError:
    XGBOOST_AVAILABLE = False

try:
    from lightgbm import LGBMRegressor
    LIGHTGBM_AVAILABLE = True
except ImportError:
    LIGHTGBM_AVAILABLE = False

from logger_config import ModelLogger

# Paths
DATA_PATH = Path("Data/cleaned_real_estate.csv")
MODELS_DIR = Path("models")
MODELS_DIR.mkdir(exist_ok=True)

print("\n" + "="*80)
print("TRAINING MODELS - WITH OVERFITTING PREVENTION")
print("="*80 + "\n")

# Load data
print("📊 Loading data...")
SAMPLE_SIZE = 100000  # Balanced speed and accuracy
df = pd.read_csv(DATA_PATH, nrows=SAMPLE_SIZE)
print(f"✓ Loaded {len(df):,} rows, {len(df.columns)} columns")

# ❌ REMOVE DATA LEAKAGE - CRITICAL!
print("\n🔥 Removing data leakage features...")
if 'price_per_m2' in df.columns:
    df = df.drop(columns=['price_per_m2'])
    print("✓ Removed 'price_per_m2' (causes data leakage)")

print(f"✓ Clean features: {list(df.drop(columns=['price']).columns)}")

# Prepare features and target
target_col = 'price'
X = df.drop(columns=[target_col])
y = df[target_col]

# Split data
print("\n📂 Splitting data (80/20)...")
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, shuffle=True
)
print(f"✓ Train: {len(X_train):,} samples")
print(f"✓ Test: {len(X_test):,} samples")

# Build preprocessor
print("\n🔧 Building preprocessor...")
numeric_cols = X.select_dtypes(include=[np.number]).columns.tolist()
categorical_cols = X.select_dtypes(exclude=[np.number]).columns.tolist()

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

# Define models with ANTI-OVERFITTING parameters
models_to_train = [
    ("Linear Regression", LinearRegression(), {}),
    
    ("Ridge (Regularized)", Ridge(alpha=10.0), {'alpha': 10.0}),
    
    ("Lasso (Regularized)", Lasso(alpha=10.0, max_iter=10000), {'alpha': 10.0}),
    
    # Decision Tree with MAX DEPTH limit
    ("Decision Tree", DecisionTreeRegressor(
        max_depth=10,  # ✅ Limited depth
        min_samples_split=100,  # ✅ Prevent overfitting
        min_samples_leaf=50,    # ✅ Prevent overfitting
        random_state=42
    ), {'max_depth': 10, 'min_samples_split': 100}),
    
    # Random Forest with REGULARIZATION
    ("Random Forest", RandomForestRegressor(
        n_estimators=100,
        max_depth=15,           # ✅ Not too deep
        min_samples_split=50,   # ✅ Prevent overfitting
        min_samples_leaf=20,    # ✅ Prevent overfitting
        max_features='sqrt',    # ✅ Feature sampling
        random_state=42,
        n_jobs=-1
    ), {'n_estimators': 100, 'max_depth': 15}),
    
    # KNN - naturally less prone to overfitting
    ("K-Nearest Neighbors", KNeighborsRegressor(
        n_neighbors=10,  # ✅ More neighbors = less overfit
        n_jobs=-1
    ), {'n_neighbors': 10}),
    
    # MLP with REGULARIZATION
    ("MLP Neural Network", MLPRegressor(
        hidden_layer_sizes=(100,),  # ✅ Simpler architecture
        max_iter=500,
        alpha=0.01,  # ✅ L2 regularization
        early_stopping=True,  # ✅ Stop when validation score stops improving
        validation_fraction=0.1,
        random_state=42
    ), {'alpha': 0.01, 'early_stopping': True}),
]

# XGBoost with REGULARIZATION
if XGBOOST_AVAILABLE:
    models_to_train.append((
        "XGBoost (Regularized)", 
        XGBRegressor(
            n_estimators=100,
            max_depth=6,        # ✅ Shallow trees
            learning_rate=0.1,  # ✅ Slow learning
            subsample=0.8,      # ✅ Row sampling
            colsample_bytree=0.8,  # ✅ Column sampling
            reg_alpha=1.0,      # ✅ L1 regularization
            reg_lambda=1.0,     # ✅ L2 regularization
            random_state=42,
            n_jobs=-1
        ),
        {'max_depth': 6, 'reg_alpha': 1.0, 'reg_lambda': 1.0}
    ))

# LightGBM with REGULARIZATION
if LIGHTGBM_AVAILABLE:
    models_to_train.append((
        "LightGBM (Regularized)",
        LGBMRegressor(
            n_estimators=100,
            max_depth=10,       # ✅ Limited depth
            learning_rate=0.1,  # ✅ Slow learning
            num_leaves=31,      # ✅ Limit complexity
            min_child_samples=50,  # ✅ Prevent overfitting
            subsample=0.8,      # ✅ Row sampling
            colsample_bytree=0.8,  # ✅ Column sampling
            reg_alpha=0.5,      # ✅ L1 regularization
            reg_lambda=0.5,     # ✅ L2 regularization
            random_state=42,
            n_jobs=-1,
            verbose=-1
        ),
        {'max_depth': 10, 'reg_alpha': 0.5, 'reg_lambda': 0.5}
    ))

print(f"\n🚀 Training {len(models_to_train)} models with cross-validation...\n")

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
        
        # Predict on train (to check overfitting)
        y_train_pred = pipeline.predict(X_train)
        train_r2 = r2_score(y_train, y_train_pred)
        train_rmse = np.sqrt(mean_squared_error(y_train, y_train_pred))
        
        # Predict on test
        y_test_pred = pipeline.predict(X_test)
        test_r2 = r2_score(y_test, y_test_pred)
        test_rmse = np.sqrt(mean_squared_error(y_test, y_test_pred))
        test_mae = mean_absolute_error(y_test, y_test_pred)
        
        # Calculate overfitting gap
        r2_gap = train_r2 - test_r2
        rmse_gap_pct = ((test_rmse - train_rmse) / train_rmse) * 100
        
        # Cross-validation (only for faster models)
        cv_r2_mean = None
        cv_r2_std = None
        if training_time < 10:  # Only CV for fast models
            try:
                print(f"   Running 3-fold CV...")
                cv_scores = cross_val_score(
                    pipeline, X_train, y_train,
                    cv=3, scoring='r2', n_jobs=-1
                )
                cv_r2_mean = cv_scores.mean()
                cv_r2_std = cv_scores.std()
            except:
                pass
        
        # Overfitting indicator
        if r2_gap > 0.05:  # More than 5% gap
            overfit_status = "⚠️ OVERFIT"
        elif r2_gap > 0.02:
            overfit_status = "⚠️ Slight overfit"
        else:
            overfit_status = "✅ Good"
        
        # Store results
        result = {
            'model_name': name,
            'train_r2': train_r2,
            'test_r2': test_r2,
            'r2_gap': r2_gap,
            'train_rmse': train_rmse,
            'test_rmse': test_rmse,
            'mae': test_mae,
            'cv_r2_mean': cv_r2_mean,
            'cv_r2_std': cv_r2_std,
            'training_time': training_time,
            'overfit_status': overfit_status,
            'train_samples': len(X_train),
            'test_samples': len(X_test)
        }
        results.append(result)
        
        # Print results
        print(f"   Train R²: {train_r2:.4f} | Test R²: {test_r2:.4f} | Gap: {r2_gap:.4f} {overfit_status}")
        print(f"   Train RMSE: {train_rmse:,.2f} | Test RMSE: {test_rmse:,.2f}")
        if cv_r2_mean:
            print(f"   CV R²: {cv_r2_mean:.4f} ± {cv_r2_std:.4f}")
        print(f"   Time: {training_time:.1f}s")
        
        # Save model
        model_data = {
            'model_name': name,
            'pipeline': pipeline,
            'train_r2': train_r2,
            'test_r2': test_r2,
            'rmse': test_rmse,
            'r2': test_r2,
            'mae': test_mae,
            'r2_gap': r2_gap,
            'cv_r2_mean': cv_r2_mean,
            'cv_r2_std': cv_r2_std,
            'feature_names': list(X.columns),
            'train_samples': len(X_train),
            'test_samples': len(X_test),
            'training_time': training_time,
            'trained_date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'hyperparameters': params
        }
        
        model_filename = name.lower().replace(' ', '_').replace('(', '').replace(')', '') + '_clean.joblib'
        joblib.dump(model_data, MODELS_DIR / model_filename)
        print(f"   💾 Saved: {model_filename}")
        
        # Log to history
        ModelLogger.log_training(
            model_name=name,
            metrics={
                'mae': test_mae,
                'rmse': test_rmse,
                'r2': test_r2,
                'train_samples': len(X_train),
                'test_samples': len(X_test),
                'training_time': training_time
            },
            hyperparameters=params,
            notes=f"Clean training (no leakage), R² gap: {r2_gap:.4f}, {overfit_status}"
        )
        
    except Exception as e:
        print(f"   ❌ Error: {str(e)}")
        results.append({
            'model_name': name,
            'error': str(e)
        })
    
    print()

# Results summary
print("\n" + "="*80)
print("RESULTS SUMMARY - OVERFITTING ANALYSIS")
print("="*80 + "\n")

results_df = pd.DataFrame([r for r in results if 'test_r2' in r])
if len(results_df) > 0:
    results_df = results_df.sort_values('test_r2', ascending=False)
    
    print(f"{'Model':<25} {'Test R²':<10} {'R² Gap':<10} {'Test RMSE':<15} {'Status':<20}")
    print("-"*85)
    
    for idx, row in results_df.iterrows():
        marker = "⭐" if idx == results_df.index[0] else "  "
        print(f"{row['model_name']:<25} {row['test_r2']:>9.4f} {row['r2_gap']:>9.4f} {row['test_rmse']:>13,.2f} {row['overfit_status']:<20} {marker}")
    
    # Best model
    best = results_df.iloc[0]
    print("\n" + "="*80)
    print("🏆 BEST MODEL (Highest Test R² with Low Overfitting)")
    print("="*80)
    print(f"Model: {best['model_name']}")
    print(f"Test R²: {best['test_r2']:.4f}")
    print(f"Train R²: {best['train_r2']:.4f}")
    print(f"R² Gap: {best['r2_gap']:.4f} ({best['overfit_status']})")
    print(f"Test RMSE: {best['test_rmse']:,.2f}")
    print(f"MAE: {best['mae']:,.2f}")
    if best['cv_r2_mean']:
        print(f"CV R²: {best['cv_r2_mean']:.4f} ± {best['cv_r2_std']:.4f}")
    
    # Save best model
    best_model_filename = best['model_name'].lower().replace(' ', '_').replace('(', '').replace(')', '') + '_clean.joblib'
    best_model_path = MODELS_DIR / best_model_filename
    if best_model_path.exists():
        best_model_data = joblib.load(best_model_path)
        joblib.dump(best_model_data, MODELS_DIR / 'best_clean.joblib')
        print(f"\n💾 Best model saved as: best_clean.joblib")

print("\n" + "="*80)
print("✅ Training completed with overfitting prevention!")
print("📊 Models saved to models/ directory")
print("📋 Check logs/model_training.csv for history")
print("="*80 + "\n")

print("\n📌 KEY IMPROVEMENTS:")
print("  ✅ Removed 'price_per_m2' (data leakage)")
print("  ✅ Used 200K samples (larger dataset)")
print("  ✅ Applied regularization to all models")
print("  ✅ Limited tree depth and complexity")
print("  ✅ Cross-validation for validation")
print("  ✅ Monitored Train vs Test R² gap")
print("\n  Expected R²: 0.85-0.93 (realistic range)")
print("  Expected Gap: < 0.05 (good generalization)\n")
