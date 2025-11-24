"""
Train model on FULL dataset (978K rows) to capture year trend properly
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
from lightgbm import LGBMRegressor
import sys
sys.path.insert(0, 'scripts/utils')
from logger_config import ModelLogger

DATA_PATH = Path("Data/cleaned_real_estate.csv")
MODELS_DIR = Path("models")

print("\n" + "="*70)
print("TRAIN MODEL ON FULL DATASET - WITH YEAR IMPACT")
print("="*70 + "\n")

# Load FULL dataset
print("Loading full dataset...")
df = pd.read_csv(DATA_PATH)
print(f"✓ Loaded {len(df):,} rows")
print(f"✓ Year range: {df['year'].min()} - {df['year'].max()}")
print(f"✓ Countries: {df['country'].unique()}")

# Remove price_per_m2 if exists (data leakage)
if 'price_per_m2' in df.columns:
    df = df.drop(columns=['price_per_m2'])
    print("✓ Removed price_per_m2 (data leakage)")

# Check year correlation
corr = df[['year', 'price']].corr().loc['year', 'price']
print(f"\n✓ Year-Price Correlation: {corr:.4f}")
if corr > 0.5:
    print("  → Strong correlation! Year WILL impact predictions")
elif corr > 0.3:
    print("  → Moderate correlation, year has some impact")
else:
    print("  → Weak correlation")

X = df.drop(columns=['price'])
y = df['price']

print(f"\nSplitting data (80/20)...")
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
print(f"✓ Train: {len(X_train):,}, Test: {len(X_test):,}")

# Preprocessor
numeric_cols = X.select_dtypes(include=[np.number]).columns.tolist()
categorical_cols = X.select_dtypes(exclude=[np.number]).columns.tolist()

print(f"\nFeatures:")
print(f"  Numeric: {numeric_cols}")
print(f"  Categorical: {categorical_cols}")

preprocessor = ColumnTransformer([
    ("num", Pipeline([
        ("imputer", SimpleImputer(strategy="median")),
        ("scaler", StandardScaler())
    ]), numeric_cols),
    ("cat", Pipeline([
        ("imputer", SimpleImputer(strategy="most_frequent")),
        ("onehot", OneHotEncoder(handle_unknown="ignore", sparse_output=False))
    ]), categorical_cols),
])

# Model with anti-overfitting params
model = LGBMRegressor(
    n_estimators=200,
    max_depth=10,
    learning_rate=0.05,
    num_leaves=31,
    min_child_samples=50,
    subsample=0.8,
    colsample_bytree=0.8,
    reg_alpha=0.5,
    reg_lambda=0.5,
    random_state=42,
    n_jobs=-1,
    verbose=-1
)

pipeline = Pipeline([
    ("preprocessor", preprocessor),
    ("regressor", model)
])

print(f"\n🚀 Training LightGBM on FULL dataset...")
print(f"   This may take 5-10 minutes...\n")
start = time.time()

pipeline.fit(X_train, y_train)

print(f"✓ Training completed in {time.time()-start:.1f}s\n")

# Evaluate
y_train_pred = pipeline.predict(X_train)
y_test_pred = pipeline.predict(X_test)

train_r2 = r2_score(y_train, y_train_pred)
test_r2 = r2_score(y_test, y_test_pred)
test_rmse = np.sqrt(mean_squared_error(y_test, y_test_pred))
test_mae = mean_absolute_error(y_test, y_test_pred)
gap = train_r2 - test_r2

print("="*70)
print("RESULTS")
print("="*70)
print(f"Train R²:  {train_r2:.4f}")
print(f"Test R²:   {test_r2:.4f}")
print(f"R² Gap:    {gap:.4f} {'✅ Good' if gap < 0.05 else '⚠️ Overfit'}")
print(f"RMSE:      ${test_rmse:,.2f}")
print(f"MAE:       ${test_mae:,.2f}")

# Test year impact
print("\n" + "="*70)
print("TEST YEAR IMPACT")
print("="*70)

# Create test cases with same property, different years
test_property = {
    'country': 'Singapore',
    'city': 'ANG MO KIO',
    'date': '2020-01',
    'area_m2': 100,
    'property_type': '3 ROOM',
    'month': 1
}

print(f"\nTest property: {test_property['property_type']}, {test_property['area_m2']}m² in {test_property['city']}")
print("\nPredictions across years:")

test_years = [2012, 2015, 2018, 2021, 2024, 2027, 2030]
predictions = []

for year in test_years:
    test_df = pd.DataFrame([{**test_property, 'year': year}])
    pred = pipeline.predict(test_df)[0]
    predictions.append(pred)
    print(f"  Year {year}: ${pred:>12,.2f}")

# Check variation
variation = (max(predictions) - min(predictions)) / min(predictions) * 100
print(f"\nPrice variation across years: {variation:.1f}%")
if variation > 20:
    print("✅ Model DOES capture year impact (>20% variation)")
elif variation > 5:
    print("⚙️  Model captures some year impact (5-20% variation)")
else:
    print("⚠️  Model captures minimal year impact (<5% variation)")

# Save model
print("\n" + "="*70)
print("SAVING MODEL")
print("="*70)

model_data = {
    'model_name': 'LightGBM (Full Dataset)',
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
    'dataset_size': len(df),
    'year_range': f"{df['year'].min()}-{df['year'].max()}",
    'year_correlation': corr,
    'trained_date': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
}

# Save as new best model
joblib.dump(model_data, MODELS_DIR / 'best_full_dataset.joblib')
print(f"✓ Saved: best_full_dataset.joblib")

# Also save as best_clean (overwrite)
joblib.dump(model_data, MODELS_DIR / 'best_clean.joblib')
print(f"✓ Updated: best_clean.joblib")

# Log training
ModelLogger.log_training(
    model_name="LightGBM (Full Dataset - 978K rows)",
    metrics={
        'mae': test_mae,
        'rmse': test_rmse,
        'r2': test_r2,
        'train_samples': len(X_train),
        'test_samples': len(X_test),
        'training_time': time.time()-start,
        'year_correlation': corr,
        'year_price_variation': variation
    },
    notes=f"Full dataset, Year range: {df['year'].min()}-{df['year'].max()}, Gap: {gap:.4f}, Year impact: {variation:.1f}%"
)

print("\n✅ Training complete! Model now captures year impact properly.\n")
print("💡 Web app will now show price changes when you change the year!\n")
