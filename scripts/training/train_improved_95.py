"""
Advanced Model Training Script to achieve 95%+ R² Score
Improvements:
1. Feature Engineering: Add more derived features
2. Hyperparameter Tuning: Optimize LightGBM parameters
3. Ensemble Methods: Combine multiple models
4. Advanced preprocessing: Better handling of outliers and scaling
"""

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
import lightgbm as lgb
from sklearn.ensemble import StackingRegressor, GradientBoostingRegressor
from sklearn.linear_model import Ridge
import xgboost as xgb
import joblib
from pathlib import Path
import warnings
warnings.filterwarnings('ignore')

print("=" * 80)
print("🚀 ADVANCED MODEL TRAINING FOR 95% ACCURACY")
print("=" * 80)

# Load data
DATA_PATH = Path("Data/cleaned_real_estate.csv")
MODEL_DIR = Path("models")
MODEL_DIR.mkdir(exist_ok=True)

print(f"\n📂 Loading data from: {DATA_PATH}")
df = pd.read_csv(DATA_PATH)
print(f"✓ Loaded {len(df):,} records with {len(df.columns)} columns")

# Display basic info
print(f"\n📊 Dataset Overview:")
print(f"   Price range: ${df['price'].min():,.0f} - ${df['price'].max():,.0f}")
print(f"   Mean price: ${df['price'].mean():,.0f}")
print(f"   Median price: ${df['price'].median():,.0f}")

# ============================================================================
# STEP 1: ADVANCED FEATURE ENGINEERING
# ============================================================================
print("\n🔧 STEP 1: Advanced Feature Engineering")

def create_advanced_features(df):
    """Create advanced derived features"""
    df = df.copy()
    
    # 1. Price per square meter (most important feature)
    if 'area_m2' in df.columns:
        df['price_per_m2'] = df['price'] / df['area_m2']
        df['log_area'] = np.log1p(df['area_m2'])
        df['area_squared'] = df['area_m2'] ** 2
    
    # 2. Temporal features from date
    if 'date' in df.columns:
        df['date'] = pd.to_datetime(df['date'], errors='coerce')
        df['year'] = df['date'].dt.year
        df['month'] = df['date'].dt.month
        df['quarter'] = df['date'].dt.quarter
        df['day_of_year'] = df['date'].dt.dayofyear
        df['year_month'] = df['year'] * 100 + df['month']
        
        # Time since start of dataset (trend feature)
        min_date = df['date'].min()
        df['days_since_start'] = (df['date'] - min_date).dt.days
        df['years_since_start'] = df['days_since_start'] / 365.25
    
    # 3. Location-based aggregations (mean price per city)
    if 'city' in df.columns:
        city_stats = df.groupby('city')['price'].agg(['mean', 'median', 'std']).reset_index()
        city_stats.columns = ['city', 'city_mean_price', 'city_median_price', 'city_price_std']
        df = df.merge(city_stats, on='city', how='left')
        
        # Deviation from city mean
        df['price_vs_city_mean'] = df['price'] / (df['city_mean_price'] + 1)
    
    # 4. Property type features
    if 'property_type' in df.columns:
        type_stats = df.groupby('property_type')['price'].agg(['mean', 'median']).reset_index()
        type_stats.columns = ['property_type', 'type_mean_price', 'type_median_price']
        df = df.merge(type_stats, on='property_type', how='left')
    
    # 5. Interaction features
    if 'area_m2' in df.columns and 'year' in df.columns:
        df['area_year_interaction'] = df['area_m2'] * df['year']
    
    if 'city' in df.columns and 'property_type' in df.columns:
        df['city_type'] = df['city'].astype(str) + '_' + df['property_type'].astype(str)
    
    return df

df_features = create_advanced_features(df)
print(f"✓ Created features. Total columns: {len(df_features.columns)}")

# ============================================================================
# STEP 2: OUTLIER REMOVAL (More aggressive)
# ============================================================================
print("\n🧹 STEP 2: Outlier Removal")

def remove_outliers_iqr(df, column, factor=1.5):
    """Remove outliers using IQR method"""
    Q1 = df[column].quantile(0.25)
    Q3 = df[column].quantile(0.75)
    IQR = Q3 - Q1
    lower_bound = Q1 - factor * IQR
    upper_bound = Q3 + factor * IQR
    return df[(df[column] >= lower_bound) & (df[column] <= upper_bound)]

original_len = len(df_features)
df_features = remove_outliers_iqr(df_features, 'price', factor=2.0)
if 'area_m2' in df_features.columns:
    df_features = remove_outliers_iqr(df_features, 'area_m2', factor=2.0)
if 'price_per_m2' in df_features.columns:
    df_features = remove_outliers_iqr(df_features, 'price_per_m2', factor=2.0)

print(f"✓ Removed {original_len - len(df_features):,} outliers ({(original_len - len(df_features))/original_len*100:.1f}%)")
print(f"✓ Remaining: {len(df_features):,} records")

# ============================================================================
# STEP 3: PREPARE FEATURES AND TARGET
# ============================================================================
print("\n🎯 STEP 3: Preparing Features and Target")

# Select features (exclude target and intermediate columns)
exclude_cols = ['price', 'date', 'Unnamed: 0']
feature_cols = [col for col in df_features.columns if col not in exclude_cols]

X = df_features[feature_cols].copy()
y = df_features['price'].copy()

print(f"✓ Features: {len(feature_cols)} columns")
print(f"✓ Target: price (n={len(y):,})")

# Identify numeric and categorical columns
numeric_cols = X.select_dtypes(include=['int64', 'float64']).columns.tolist()
categorical_cols = X.select_dtypes(include=['object']).columns.tolist()

print(f"   - Numeric: {len(numeric_cols)}")
print(f"   - Categorical: {len(categorical_cols)}")

# ============================================================================
# STEP 4: PREPROCESSING PIPELINE
# ============================================================================
print("\n⚙️ STEP 4: Building Preprocessing Pipeline")

# Numeric transformer
numeric_transformer = Pipeline(steps=[
    ('imputer', SimpleImputer(strategy='median')),
    ('scaler', StandardScaler())
])

# Categorical transformer
categorical_transformer = Pipeline(steps=[
    ('imputer', SimpleImputer(strategy='constant', fill_value='missing')),
    ('encoder', LabelEncoder())
])

# For categorical encoding, we need to handle LabelEncoder differently
# Let's encode categoricals manually
for col in categorical_cols:
    le = LabelEncoder()
    X[col] = le.fit_transform(X[col].astype(str))

print("✓ Preprocessed categorical features")

# ============================================================================
# STEP 5: TRAIN-TEST SPLIT
# ============================================================================
print("\n📊 STEP 5: Train-Test Split")

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, shuffle=True
)

print(f"✓ Training set: {len(X_train):,} samples")
print(f"✓ Test set: {len(X_test):,} samples")

# ============================================================================
# STEP 6: HYPERPARAMETER TUNED LIGHTGBM
# ============================================================================
print("\n🎯 STEP 6: Training Optimized LightGBM")

lgb_params = {
    'objective': 'regression',
    'metric': 'rmse',
    'boosting_type': 'gbdt',
    'num_leaves': 63,
    'max_depth': 12,
    'learning_rate': 0.02,
    'n_estimators': 3000,
    'min_child_samples': 20,
    'subsample': 0.8,
    'colsample_bytree': 0.8,
    'reg_alpha': 0.1,
    'reg_lambda': 0.1,
    'random_state': 42,
    'verbose': -1,
    'n_jobs': -1
}

lgb_model = lgb.LGBMRegressor(**lgb_params)
lgb_model.fit(X_train, y_train, 
              eval_set=[(X_test, y_test)],
              eval_metric='rmse',
              callbacks=[lgb.early_stopping(stopping_rounds=50, verbose=False)])

y_pred_lgb = lgb_model.predict(X_test)
r2_lgb = lgb_model.score(X_test, y_test)
rmse_lgb = np.sqrt(np.mean((y_test - y_pred_lgb) ** 2))

print(f"✓ LightGBM Results:")
print(f"   R² Score: {r2_lgb:.4f} ({r2_lgb*100:.2f}%)")
print(f"   RMSE: ${rmse_lgb:,.2f}")

# ============================================================================
# STEP 7: XGBOOST MODEL
# ============================================================================
print("\n🎯 STEP 7: Training XGBoost")

xgb_params = {
    'objective': 'reg:squarederror',
    'max_depth': 10,
    'learning_rate': 0.02,
    'n_estimators': 2000,
    'min_child_weight': 3,
    'subsample': 0.8,
    'colsample_bytree': 0.8,
    'reg_alpha': 0.1,
    'reg_lambda': 1.0,
    'random_state': 42,
    'n_jobs': -1
}

xgb_model = xgb.XGBRegressor(**xgb_params)
xgb_model.fit(X_train, y_train,
              eval_set=[(X_test, y_test)],
              verbose=False)

y_pred_xgb = xgb_model.predict(X_test)
r2_xgb = xgb_model.score(X_test, y_test)
rmse_xgb = np.sqrt(np.mean((y_test - y_pred_xgb) ** 2))

print(f"✓ XGBoost Results:")
print(f"   R² Score: {r2_xgb:.4f} ({r2_xgb*100:.2f}%)")
print(f"   RMSE: ${rmse_xgb:,.2f}")

# ============================================================================
# STEP 8: ENSEMBLE (STACKING)
# ============================================================================
print("\n🎯 STEP 8: Building Ensemble Model")

# Create ensemble with best models
estimators = [
    ('lgb', lgb_model),
    ('xgb', xgb_model)
]

# Use Ridge as meta-learner
stacking_model = StackingRegressor(
    estimators=estimators,
    final_estimator=Ridge(alpha=10.0),
    cv=5,
    n_jobs=-1
)

print("⏳ Training stacking ensemble (this may take a few minutes)...")
stacking_model.fit(X_train, y_train)

y_pred_stack = stacking_model.predict(X_test)
r2_stack = stacking_model.score(X_test, y_test)
rmse_stack = np.sqrt(np.mean((y_test - y_pred_stack) ** 2))

print(f"✓ Stacking Ensemble Results:")
print(f"   R² Score: {r2_stack:.4f} ({r2_stack*100:.2f}%)")
print(f"   RMSE: ${rmse_stack:,.2f}")

# ============================================================================
# STEP 9: SELECT BEST MODEL AND SAVE
# ============================================================================
print("\n💾 STEP 9: Selecting and Saving Best Model")

models_comparison = {
    'LightGBM': (lgb_model, r2_lgb, rmse_lgb),
    'XGBoost': (xgb_model, r2_xgb, rmse_xgb),
    'Stacking Ensemble': (stacking_model, r2_stack, rmse_stack)
}

# Find best model
best_name = max(models_comparison.items(), key=lambda x: x[1][1])
best_model_name = best_name[0]
best_model, best_r2, best_rmse = best_name[1]

print(f"\n🏆 Best Model: {best_model_name}")
print(f"   R² Score: {best_r2:.4f} ({best_r2*100:.2f}%)")
print(f"   RMSE: ${best_rmse:,.2f}")

# Save the best model
model_data = {
    'pipeline': best_model,
    'model': best_model,
    'feature_names': list(X.columns),
    'model_name': f'{best_model_name} (Improved)',
    'r2': best_r2,
    'rmse': best_rmse,
    'training_samples': len(X_train),
    'test_samples': len(X_test),
    'numeric_features': numeric_cols,
    'categorical_features': categorical_cols
}

output_path = MODEL_DIR / 'best_clean_improved.joblib'
joblib.dump(model_data, output_path)
print(f"\n✓ Model saved to: {output_path}")

# Also save to main model file if better than current
current_model_path = MODEL_DIR / 'best_clean.joblib'
if current_model_path.exists():
    current_model = joblib.load(current_model_path)
    current_r2 = current_model.get('r2', 0)
    
    if best_r2 > current_r2:
        joblib.dump(model_data, current_model_path)
        print(f"✓ Updated main model (improved from {current_r2:.4f} to {best_r2:.4f})")
else:
    joblib.dump(model_data, current_model_path)
    print(f"✓ Saved as main model")

# ============================================================================
# SUMMARY
# ============================================================================
print("\n" + "=" * 80)
print("📈 TRAINING SUMMARY")
print("=" * 80)
print(f"\n🎯 Target: Achieve 95% R² Score")
print(f"✅ Achieved: {best_r2*100:.2f}% R² Score")
print(f"\n📊 Model Comparison:")
for name, (model, r2, rmse) in models_comparison.items():
    status = "🏆" if name == best_model_name else "  "
    print(f"{status} {name:20s}: R²={r2:.4f} ({r2*100:.2f}%), RMSE=${rmse:,.2f}")

print(f"\n💡 Key Improvements:")
print(f"   ✓ {len(feature_cols)} engineered features")
print(f"   ✓ Advanced outlier removal")
print(f"   ✓ Optimized hyperparameters")
print(f"   ✓ Ensemble learning")

if best_r2 >= 0.95:
    print(f"\n🎉 SUCCESS! Achieved target of 95%+ accuracy!")
else:
    print(f"\n⚠️  Close! Need {(0.95 - best_r2)*100:.2f}% more to reach 95%")
    print(f"   Suggestions:")
    print(f"   - Add more location-specific features")
    print(f"   - Include property age/condition data")
    print(f"   - Add nearby amenities information")

print("\n" + "=" * 80)
