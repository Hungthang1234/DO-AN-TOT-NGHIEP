"""
Advanced House Price Prediction Pipeline
Trains models on full dataset with temporal and spatial features
Supports prediction for multiple years and regions
"""

import pandas as pd
import numpy as np
import joblib
import time
import argparse
from pathlib import Path
from datetime import datetime
from sklearn.model_selection import train_test_split, cross_val_score, KFold
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.impute import SimpleImputer
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LinearRegression, Ridge, Lasso
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor, ExtraTreesRegressor
from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error
from xgboost import XGBRegressor
from lightgbm import LGBMRegressor

# Configuration
RANDOM_STATE = 42
N_JOBS = -1  # Use all CPU cores
CV_FOLDS = 5  # Cross-validation folds
TEST_SIZE = 0.2
BASE_DIR = Path(r"D:\Do An Tot Nghiep - Du doan gia bat dong san bang ML va DL")
MODELS_DIR = BASE_DIR / "models"
LOGS_DIR = BASE_DIR / "logs"

def load_data(data_path, nrows=None, sample_frac=None):
    """
    Load and prepare data with basic validation.
    
    Args:
        data_path: Path to CSV file
        nrows: Number of rows to load (None = all)
        sample_frac: Fraction of data to sample (None = no sampling)
    
    Returns:
        pandas DataFrame
    """
    print(f"\n{'='*80}")
    print(f"Loading data from: {data_path}")
    print(f"{'='*80}")
    
    if not Path(data_path).exists():
        raise FileNotFoundError(f"Data file not found: {data_path}")
    
    # Load data
    start_time = time.time()
    df = pd.read_csv(data_path, nrows=nrows)
    load_time = time.time() - start_time
    
    print(f"✓ Loaded {len(df):,} rows in {load_time:.2f} seconds")
    
    # Sample if requested
    if sample_frac and 0 < sample_frac < 1:
        original_size = len(df)
        df = df.sample(frac=sample_frac, random_state=RANDOM_STATE)
        print(f"✓ Sampled {len(df):,} rows ({sample_frac*100:.1f}% of {original_size:,})")
    
    # Validate columns
    required_cols = ['country', 'city', 'date', 'price', 'area_m2', 
                     'property_type', 'price_per_m2', 'year', 'month']
    missing_cols = set(required_cols) - set(df.columns)
    if missing_cols:
        raise ValueError(f"Missing required columns: {missing_cols}")
    
    print(f"✓ All required columns present")
    print(f"\nData shape: {df.shape}")
    print(f"Memory usage: {df.memory_usage(deep=True).sum() / 1024**2:.2f} MB")
    
    return df

def create_advanced_features(df):
    """
    Create advanced temporal and spatial features for better predictions.
    NO DATA LEAKAGE - only use features that would be available at prediction time.
    
    Args:
        df: Input DataFrame
    
    Returns:
        DataFrame with additional features
    """
    print(f"\n{'='*80}")
    print("Creating advanced features...")
    print(f"{'='*80}")
    
    df = df.copy()
    
    # 1. TEMPORAL FEATURES
    print("\n1. Creating temporal features...")
    
    # Year-based features
    df['years_since_1990'] = df['year'] - 1990  # Normalize year
    df['year_squared'] = df['year'] ** 2  # Capture non-linear trends
    
    # Seasonality features
    df['quarter'] = (df['month'] - 1) // 3 + 1
    df['is_peak_season'] = df['month'].isin([3, 4, 5, 6]).astype(int)  # Peak buying season
    
    # Cyclical encoding for month (preserves circular nature)
    df['month_sin'] = np.sin(2 * np.pi * df['month'] / 12)
    df['month_cos'] = np.cos(2 * np.pi * df['month'] / 12)
    
    print(f"  - Added: years_since_1990, year_squared, quarter, is_peak_season, month_sin, month_cos")
    
    # 2. INTERACTION FEATURES (no data leakage)
    print("\n2. Creating interaction features...")
    
    # Area interactions
    df['area_squared'] = df['area_m2'] ** 2
    df['area_log'] = np.log1p(df['area_m2'])
    
    # Year-area interaction
    df['year_x_area'] = df['years_since_1990'] * df['area_m2']
    
    # Price per m2 interactions
    df['price_per_m2_squared'] = df['price_per_m2'] ** 2
    df['price_per_m2_log'] = np.log1p(df['price_per_m2'])
    
    print(f"  - Added: area_squared, area_log, year_x_area")
    print(f"  - Added: price_per_m2_squared, price_per_m2_log")
    
    # 3. STATISTICAL FEATURES
    print("\n3. Creating statistical features...")
    
    # Area categories
    df['area_category'] = pd.cut(df['area_m2'], 
                                  bins=[0, 50, 80, 110, 150, float('inf')],
                                  labels=['very_small', 'small', 'medium', 'large', 'very_large'])
    
    # Price per m2 categories
    df['price_per_m2_category'] = pd.qcut(df['price_per_m2'], 
                                           q=5, 
                                           labels=['very_low', 'low', 'medium', 'high', 'very_high'],
                                           duplicates='drop')
    
    print(f"  - Added: area_category, price_per_m2_category")
    
    print(f"\n✓ Feature engineering complete!")
    print(f"  Total features: {len(df.columns)}")
    print(f"  New features: {len(df.columns) - 9}")  # 9 original columns
    
    return df

def build_advanced_preprocessor(df, target='price'):
    """
    Build preprocessing pipeline with advanced feature handling.
    
    Args:
        df: Full DataFrame (needed to identify feature types)
        target: Target column name
    
    Returns:
        ColumnTransformer pipeline
    """
    print(f"\n{'='*80}")
    print("Building advanced preprocessing pipeline...")
    print(f"{'='*80}")
    
    # Separate features from target
    X = df.drop(columns=[target])
    
    # Identify feature types
    numeric_features = X.select_dtypes(include=['int64', 'float64']).columns.tolist()
    categorical_features = X.select_dtypes(include=['object', 'category']).columns.tolist()
    
    # Remove date column from features (not useful as-is)
    if 'date' in numeric_features:
        numeric_features.remove('date')
    if 'date' in categorical_features:
        categorical_features.remove('date')
    
    # Remove 'city' to speed up training (too many categories: 347)
    # Keep country and property_type which have fewer categories
    if 'city' in categorical_features:
        categorical_features.remove('city')
        print(f"  ⚠ Removed 'city' feature (347 categories) to speed up training")
    
    print(f"\nFeature types:")
    print(f"  - Numeric features ({len(numeric_features)}): {numeric_features[:5]}...")
    print(f"  - Categorical features ({len(categorical_features)}): {categorical_features}")
    
    # Numeric pipeline: impute missing + scale
    numeric_transformer = Pipeline(steps=[
        ('imputer', SimpleImputer(strategy='median')),
        ('scaler', StandardScaler())
    ])
    
    # Categorical pipeline: impute missing + one-hot encode
    categorical_transformer = Pipeline(steps=[
        ('imputer', SimpleImputer(strategy='most_frequent')),
        ('onehot', OneHotEncoder(handle_unknown='ignore', sparse_output=False))
    ])
    
    # Combine transformers
    preprocessor = ColumnTransformer(
        transformers=[
            ('num', numeric_transformer, numeric_features),
            ('cat', categorical_transformer, categorical_features)
        ],
        remainder='drop'
    )
    
    print(f"✓ Preprocessor ready")
    
    return preprocessor

def get_advanced_models():
    """
    Get dictionary of advanced models with optimized hyperparameters.
    
    Returns:
        Dictionary of model name -> model instance
    """
    models = {
        'LinearRegression': LinearRegression(n_jobs=N_JOBS),
        
        'Ridge': Ridge(alpha=10.0, random_state=RANDOM_STATE),
        
        'Lasso': Lasso(alpha=10.0, random_state=RANDOM_STATE, max_iter=2000),
        
        'RandomForest': RandomForestRegressor(
            n_estimators=200,
            max_depth=25,
            min_samples_split=5,
            min_samples_leaf=2,
            max_features='sqrt',
            random_state=RANDOM_STATE,
            n_jobs=N_JOBS,
            verbose=0
        ),
        
        'ExtraTrees': ExtraTreesRegressor(
            n_estimators=200,
            max_depth=25,
            min_samples_split=5,
            min_samples_leaf=2,
            max_features='sqrt',
            random_state=RANDOM_STATE,
            n_jobs=N_JOBS,
            verbose=0
        ),
        
        'GradientBoosting': GradientBoostingRegressor(
            n_estimators=200,
            max_depth=7,
            learning_rate=0.05,
            min_samples_split=5,
            min_samples_leaf=2,
            subsample=0.8,
            random_state=RANDOM_STATE,
            verbose=0
        ),
        
        'XGBoost': XGBRegressor(
            n_estimators=200,
            max_depth=7,
            learning_rate=0.05,
            min_child_weight=3,
            subsample=0.8,
            colsample_bytree=0.8,
            gamma=0.1,
            random_state=RANDOM_STATE,
            n_jobs=N_JOBS,
            verbosity=0
        ),
        
        'LightGBM': LGBMRegressor(
            n_estimators=200,
            max_depth=7,
            learning_rate=0.05,
            num_leaves=31,
            min_child_samples=20,
            subsample=0.8,
            colsample_bytree=0.8,
            random_state=RANDOM_STATE,
            n_jobs=N_JOBS,
            verbose=-1
        )
    }
    
    return models

def evaluate_with_cross_validation(model, X, y, cv=CV_FOLDS):
    """
    Evaluate model using cross-validation.
    
    Args:
        model: Scikit-learn model or pipeline
        X: Feature matrix
        y: Target vector
        cv: Number of cross-validation folds
    
    Returns:
        dict with cv scores
    """
    kfold = KFold(n_splits=cv, shuffle=True, random_state=RANDOM_STATE)
    
    # Negative MSE (sklearn convention)
    cv_mse = -cross_val_score(model, X, y, cv=kfold, 
                               scoring='neg_mean_squared_error', n_jobs=N_JOBS)
    cv_rmse = np.sqrt(cv_mse)
    
    # R2 score
    cv_r2 = cross_val_score(model, X, y, cv=kfold, 
                            scoring='r2', n_jobs=N_JOBS)
    
    # MAE
    cv_mae = -cross_val_score(model, X, y, cv=kfold,
                              scoring='neg_mean_absolute_error', n_jobs=N_JOBS)
    
    return {
        'cv_rmse_mean': cv_rmse.mean(),
        'cv_rmse_std': cv_rmse.std(),
        'cv_r2_mean': cv_r2.mean(),
        'cv_r2_std': cv_r2.std(),
        'cv_mae_mean': cv_mae.mean(),
        'cv_mae_std': cv_mae.std()
    }

def train_and_evaluate_model(name, model, X_train, X_test, y_train, y_test, use_cv=True):
    """
    Train and evaluate a single model with optional cross-validation.
    
    Args:
        name: Model name
        model: Model instance or pipeline
        X_train, X_test, y_train, y_test: Train/test splits
        use_cv: Whether to use cross-validation
    
    Returns:
        dict with evaluation metrics
    """
    print(f"\n{'-'*80}")
    print(f"Training: {name}")
    print(f"{'-'*80}")
    
    # Training
    start_time = time.time()
    model.fit(X_train, y_train)
    train_time = time.time() - start_time
    
    # Predictions
    train_pred = model.predict(X_train)
    test_pred = model.predict(X_test)
    
    # Metrics
    train_rmse = np.sqrt(mean_squared_error(y_train, train_pred))
    test_rmse = np.sqrt(mean_squared_error(y_test, test_pred))
    train_r2 = r2_score(y_train, train_pred)
    test_r2 = r2_score(y_test, test_pred)
    test_mae = mean_absolute_error(y_test, test_pred)
    
    results = {
        'model_name': name,
        'train_rmse': train_rmse,
        'test_rmse': test_rmse,
        'train_r2': train_r2,
        'test_r2': test_r2,
        'test_mae': test_mae,
        'train_time': train_time
    }
    
    # Cross-validation
    if use_cv:
        print(f"  Running {CV_FOLDS}-fold cross-validation...")
        cv_results = evaluate_with_cross_validation(model, X_train, y_train, cv=CV_FOLDS)
        results.update(cv_results)
    
    # Display results
    print(f"\n  Results:")
    print(f"    Train RMSE: {train_rmse:,.2f}")
    print(f"    Test RMSE:  {test_rmse:,.2f}")
    print(f"    Train R²:   {train_r2:.4f}")
    print(f"    Test R²:    {test_r2:.4f}")
    print(f"    Test MAE:   {test_mae:,.2f}")
    if use_cv:
        print(f"    CV RMSE:    {results['cv_rmse_mean']:,.2f} ± {results['cv_rmse_std']:,.2f}")
        print(f"    CV R²:      {results['cv_r2_mean']:.4f} ± {results['cv_r2_std']:.4f}")
    print(f"    Train time: {train_time:.2f}s")
    
    return results, model

def main(args=None):
    """Main training pipeline."""
    
    print("\n" + "="*80)
    print("ADVANCED HOUSE PRICE PREDICTION - TRAINING PIPELINE")
    print("="*80)
    print(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Random state: {RANDOM_STATE}")
    print(f"Cross-validation folds: {CV_FOLDS}")
    print(f"Test size: {TEST_SIZE}")
    
    # Create directories
    MODELS_DIR.mkdir(exist_ok=True)
    LOGS_DIR.mkdir(exist_ok=True)
    
    # 1. Load data
    if args and args.data:
        data_path = args.data
    else:
        data_path = BASE_DIR / "Data" / "cleaned_real_estate.csv"
    
    # Use command line arguments for sampling
    nrows = args.nrows if args and args.nrows else None
    sample_frac = args.sample_frac if args and args.sample_frac else 0.1
    
    df = load_data(str(data_path), nrows=nrows, sample_frac=sample_frac)
    
    # 2. Create advanced features
    df = create_advanced_features(df)
    
    # 3. Prepare data
    target = 'price'
    print(f"\n{'='*80}")
    print(f"Target variable: {target}")
    print(f"{'='*80}")
    
    if target not in df.columns:
        raise ValueError(f"Target '{target}' not found in data")
    
    print(f"\nTarget statistics:")
    print(f"  Mean:   {df[target].mean():,.2f}")
    print(f"  Median: {df[target].median():,.2f}")
    print(f"  Std:    {df[target].std():,.2f}")
    print(f"  Min:    {df[target].min():,.2f}")
    print(f"  Max:    {df[target].max():,.2f}")
    
    # 4. Build preprocessor
    preprocessor = build_advanced_preprocessor(df, target)
    
    # 5. Split data
    X = df.drop(columns=[target, 'date'])  # Remove target and date
    y = df[target]
    
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=TEST_SIZE, random_state=RANDOM_STATE
    )
    
    print(f"\n{'='*80}")
    print("Data split:")
    print(f"{'='*80}")
    print(f"  Training set: {len(X_train):,} samples")
    print(f"  Test set:     {len(X_test):,} samples")
    
    # 6. Train models
    print(f"\n{'='*80}")
    print("TRAINING MODELS")
    print(f"{'='*80}")
    
    models = get_advanced_models()
    all_results = []
    trained_models = {}
    
    total_start = time.time()
    
    for name, model in models.items():
        # Create pipeline
        pipeline = Pipeline(steps=[
            ('preprocessor', preprocessor),
            ('model', model)
        ])
        
        # Train and evaluate
        results, trained_pipeline = train_and_evaluate_model(
            name, pipeline, X_train, X_test, y_train, y_test, use_cv=True
        )
        
        all_results.append(results)
        trained_models[name] = trained_pipeline
    
    total_time = time.time() - total_start
    
    # 7. Summary
    print(f"\n{'='*80}")
    print("TRAINING SUMMARY")
    print(f"{'='*80}")
    
    results_df = pd.DataFrame(all_results)
    results_df = results_df.sort_values('test_rmse')
    
    print("\nModel Rankings (by Test RMSE):")
    print(results_df[['model_name', 'test_rmse', 'test_r2', 'test_mae', 'cv_rmse_mean', 'train_time']].to_string(index=False))
    
    print(f"\nTotal training time: {total_time:.2f}s")
    
    # 8. Save best model
    best_model_name = results_df.iloc[0]['model_name']
    best_model = trained_models[best_model_name]
    best_results = results_df.iloc[0].to_dict()
    
    # Get feature names after preprocessing
    feature_names = X_train.columns.tolist()
    
    # Save as dict with metadata
    model_data = {
        'pipeline': best_model,
        'feature_names': feature_names,
        'model_name': best_model_name,
        'target': target,
        'test_rmse': best_results['test_rmse'],
        'test_r2': best_results['test_r2'],
        'test_mae': best_results['test_mae'],
        'cv_rmse_mean': best_results.get('cv_rmse_mean'),
        'cv_r2_mean': best_results.get('cv_r2_mean'),
        'train_time': best_results['train_time'],
        'training_date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'training_samples': len(X_train),
        'test_samples': len(X_test),
        'total_features': len(feature_names),
        'random_state': RANDOM_STATE
    }
    
    best_model_path = MODELS_DIR / "best_advanced.joblib"
    joblib.dump(model_data, best_model_path)
    
    print(f"\n{'='*80}")
    print("BEST MODEL SAVED")
    print(f"{'='*80}")
    print(f"  Model: {best_model_name}")
    print(f"  Path: {best_model_path}")
    print(f"  Test RMSE: {best_results['test_rmse']:,.2f}")
    print(f"  Test R²: {best_results['test_r2']:.4f}")
    print(f"  Test MAE: {best_results['test_mae']:,.2f}")
    print(f"  CV RMSE: {best_results.get('cv_rmse_mean', 0):,.2f}")
    print(f"  CV R²: {best_results.get('cv_r2_mean', 0):.4f}")
    
    # 9. Save all models
    print(f"\nSaving all models...")
    for name, model in trained_models.items():
        model_path = MODELS_DIR / f"{name.lower().replace(' ', '_')}_advanced.joblib"
        joblib.dump(model, model_path)
        print(f"  ✓ {name} -> {model_path}")
    
    # 10. Save training log
    log_path = LOGS_DIR / "training_log_advanced.csv"
    results_df['timestamp'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    if log_path.exists():
        existing_log = pd.read_csv(log_path)
        updated_log = pd.concat([existing_log, results_df], ignore_index=True)
    else:
        updated_log = results_df
    
    updated_log.to_csv(log_path, index=False)
    print(f"\n✓ Training log saved to: {log_path}")
    
    print(f"\n{'='*80}")
    print("PIPELINE COMPLETE!")
    print(f"{'='*80}\n")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Advanced House Price Prediction Training Pipeline"
    )
    parser.add_argument(
        "--data",
        type=str,
        default=None,
        help="Path to CSV data file (default: D:/Do An Tot Nghiep.../Data/cleaned_real_estate.csv)"
    )
    parser.add_argument(
        "--nrows",
        type=int,
        default=None,
        help="Number of rows to load (default: None = all rows)"
    )
    parser.add_argument(
        "--sample-frac",
        type=float,
        default=0.1,
        help="Fraction of data to sample (default: 0.1 = 10%%, use 1.0 for full dataset)"
    )
    
    args = parser.parse_args()
    main(args)
