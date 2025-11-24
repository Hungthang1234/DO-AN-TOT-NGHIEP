"""
Quick train important models with overfitting prevention
Skip slow models (Lasso, MLP)
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
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor
from xgboost import XGBRegressor
from lightgbm import LGBMRegressor
from logger_config import ModelLogger

DATA_PATH = Path("Data/cleaned_real_estate.csv")
MODELS_DIR = Path("models")

print("\n" + "="*70)
print("QUICK TRAIN - IMPORTANT MODELS (NO OVERFITTING)")
print("="*70 + "\n")

# Load
df = pd.read_csv(DATA_PATH, nrows=100000)
if 'price_per_m2' in df.columns:
    df = df.drop(columns=['price_per_m2'])
print(f"✓ Loaded {len(df):,} rows (clean, no leakage)")

X = df.drop(columns=['price'])
y = df['price']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Preprocessor
numeric_cols = X.select_dtypes(include=[np.number]).columns.tolist()
categorical_cols = X.select_dtypes(exclude=[np.number]).columns.tolist()

preprocessor = ColumnTransformer([
    ("num", Pipeline([("imputer", SimpleImputer(strategy="median")), ("scaler", StandardScaler())]), numeric_cols),
    ("cat", Pipeline([("imputer", SimpleImputer(strategy="most_frequent")), 
                      ("onehot", OneHotEncoder(handle_unknown="ignore", sparse_output=False))]), categorical_cols),
])

# Models
models = [
    ("Decision Tree", DecisionTreeRegressor(max_depth=10, min_samples_split=100, min_samples_leaf=50, random_state=42)),
    ("Random Forest", RandomForestRegressor(n_estimators=100, max_depth=15, min_samples_split=50, min_samples_leaf=20, max_features='sqrt', random_state=42, n_jobs=-1)),
    ("XGBoost", XGBRegressor(n_estimators=100, max_depth=6, learning_rate=0.1, subsample=0.8, colsample_bytree=0.8, reg_alpha=1.0, reg_lambda=1.0, random_state=42, n_jobs=-1)),
    ("LightGBM", LGBMRegressor(n_estimators=100, max_depth=10, learning_rate=0.1, num_leaves=31, min_child_samples=50, subsample=0.8, colsample_bytree=0.8, reg_alpha=0.5, reg_lambda=0.5, random_state=42, n_jobs=-1, verbose=-1)),
]

results = []

for name, model in models:
    print(f"\n🚀 {name}...")
    start = time.time()
    
    pipeline = Pipeline([("preprocessor", preprocessor), ("regressor", model)])
    pipeline.fit(X_train, y_train)
    
    y_train_pred = pipeline.predict(X_train)
    y_test_pred = pipeline.predict(X_test)
    
    train_r2 = r2_score(y_train, y_train_pred)
    test_r2 = r2_score(y_test, y_test_pred)
    test_rmse = np.sqrt(mean_squared_error(y_test, y_test_pred))
    test_mae = mean_absolute_error(y_test, y_test_pred)
    gap = train_r2 - test_r2
    
    status = "✅ Good" if gap < 0.05 else "⚠️ Overfit"
    
    print(f"  Train R²: {train_r2:.4f} | Test R²: {test_r2:.4f} | Gap: {gap:.4f} {status}")
    print(f"  RMSE: {test_rmse:,.2f} | MAE: {test_mae:,.2f} | Time: {time.time()-start:.1f}s")
    
    # Save
    model_data = {
        'model_name': name,
        'pipeline': pipeline,
        'train_r2': train_r2,
        'test_r2': test_r2,
        'r2_gap': gap,
        'rmse': test_rmse,
        'r2': test_r2,
        'mae': test_mae,
        'feature_names': list(X.columns),
        'train_samples': len(X_train),
        'test_samples': len(X_test),
        'trained_date': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }
    
    filename = name.lower().replace(' ', '_') + '_clean.joblib'
    joblib.dump(model_data, MODELS_DIR / filename)
    print(f"  💾 {filename}")
    
    ModelLogger.log_training(
        model_name=name + " (Clean)",
        metrics={'mae': test_mae, 'rmse': test_rmse, 'r2': test_r2, 'train_samples': len(X_train), 'test_samples': len(X_test), 'training_time': time.time()-start},
        notes=f"No data leakage, R² gap: {gap:.4f}, {status}"
    )
    
    results.append({'name': name, 'test_r2': test_r2, 'gap': gap, 'rmse': test_rmse, 'status': status})

# Summary
print("\n" + "="*70)
print("SUMMARY")
print("="*70)
df_res = pd.DataFrame(results).sort_values('test_r2', ascending=False)
for _, r in df_res.iterrows():
    print(f"{r['name']:<20} R²: {r['test_r2']:.4f}  Gap: {r['gap']:.4f}  RMSE: {r['rmse']:>10,.2f}  {r['status']}")

best = df_res.iloc[0]
print(f"\n🏆 Best: {best['name']} (R²={best['test_r2']:.4f})")

# Save best
best_file = best['name'].lower().replace(' ', '_') + '_clean.joblib'
joblib.dump(joblib.load(MODELS_DIR / best_file), MODELS_DIR / 'best_clean.joblib')
print(f"💾 Saved as: best_clean.joblib\n")
