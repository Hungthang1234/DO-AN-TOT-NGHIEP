import argparse
import os
import joblib
import numpy as np
import pandas as pd
from pathlib import Path

from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.linear_model import LinearRegression, RidgeCV, LassoCV
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score

try:
    from xgboost import XGBRegressor
except ImportError:
    XGBRegressor = None

try:
    from lightgbm import LGBMRegressor
except ImportError:
    LGBMRegressor = None


def load_data(path, sample_frac=None, nrows=None):
    # allow reading with a fraction or fixed nrows for large files
    if sample_frac is not None and sample_frac < 1.0:
        df = pd.read_csv(path, nrows=nrows)
        return df.sample(frac=sample_frac, random_state=42)
    return pd.read_csv(path, nrows=nrows)


def build_preprocessor(df, target_col):
    X = df.drop(columns=[target_col])
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

    return preprocessor


def evaluate_and_report(model, X_test, y_test, name):
    preds = model.predict(X_test)
    # use np.sqrt of MSE for compatibility with this scikit-learn version
    rmse = np.sqrt(mean_squared_error(y_test, preds))
    r2 = r2_score(y_test, preds)
    print(f"{name} -> RMSE: {rmse:.4f}, R2: {r2:.4f}")
    return {"name": name, "rmse": rmse, "r2": r2}


def main(args):
    data_path = Path(args.data)
    if not data_path.exists():
        raise FileNotFoundError(f"Data file not found: {data_path}")
    
    if not data_path.suffix.lower() == '.csv':
        raise ValueError(f"Expected CSV file, got: {data_path.suffix}")

    print(f"Loading data from: {data_path}")
    if args.nrows:
        print(f"  Reading first {args.nrows} rows...")
    if args.sample_frac < 1.0:
        print(f"  Will sample {args.sample_frac*100:.0f}% of rows")
    
    df = load_data(data_path, sample_frac=args.sample_frac, nrows=args.nrows)
    print(f"Loaded {len(df)} rows, {len(df.columns)} columns")

    if args.preview:
        print(df.head().to_string())
        print(df.info())
        return

    if args.target not in df.columns:
        available_cols = ', '.join(df.columns[:10])
        raise ValueError(
            f"Target column '{args.target}' not found.\n"
            f"Available columns: {available_cols}{'...' if len(df.columns) > 10 else ''}"
        )

    # Check target column type
    if not pd.api.types.is_numeric_dtype(df[args.target]):
        raise ValueError(f"Target column '{args.target}' must be numeric, got {df[args.target].dtype}")
    
    initial_rows = len(df)
    df = df.dropna(axis=0, subset=[args.target])
    if len(df) < initial_rows:
        print(f"Dropped {initial_rows - len(df)} rows with missing target values")

    # optionally drop columns with too many missing values
    thresh = args.drop_missing_frac
    if thresh > 0:
        keep_cols = [c for c in df.columns if df[c].isna().mean() <= thresh]
        removed = set(df.columns) - set(keep_cols)
        if removed:
            print(f"Dropping columns with >{thresh*100:.0f}% missing: {sorted(list(removed))}")
        df = df[keep_cols]

    X = df.drop(columns=[args.target])
    y = df[args.target]

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=args.test_size, random_state=42)

    # Build preprocessor from the original dataframe so the target column is available
    preprocessor = build_preprocessor(df, args.target)

    models = []
    # Linear models (fast, interpretable baselines)
    models.append(("LinearRegression", Pipeline([("pre", preprocessor), ("est", LinearRegression())])))
    models.append(("RidgeCV", Pipeline([("pre", preprocessor), ("est", RidgeCV(alphas=[0.1, 1.0, 10.0], cv=3))])))
    models.append(("LassoCV", Pipeline([("pre", preprocessor), ("est", LassoCV(cv=3, max_iter=2000, random_state=42))])))

    # Tree-based models (better for non-linear patterns)
    n_jobs = min(os.cpu_count() or 1, 4)  # Limit parallelism to avoid overloading
    models.append(("RandomForest", Pipeline([("pre", preprocessor), ("est", RandomForestRegressor(
        n_estimators=100, 
        max_depth=15,
        min_samples_split=10,
        random_state=42, 
        n_jobs=n_jobs
    ))])))

    if XGBRegressor is not None:
        models.append(("XGBoost", Pipeline([("pre", preprocessor), ("est", XGBRegressor(
            n_estimators=200,
            max_depth=6,
            learning_rate=0.1,
            random_state=42,
            n_jobs=n_jobs,
            verbosity=0
        ))])))
    else:
        print("⚠ xgboost not installed — skipping XGBoost model")

    if LGBMRegressor is not None:
        models.append(("LightGBM", Pipeline([("pre", preprocessor), ("est", LGBMRegressor(
            n_estimators=200,
            max_depth=10,
            learning_rate=0.1,
            random_state=42,
            n_jobs=n_jobs,
            verbose=-1
        ))])))
    else:
        print("⚠ lightgbm not installed — skipping LightGBM model")

    results = []
    os.makedirs(args.out_dir, exist_ok=True)
    
    print(f"\nTraining {len(models)} models...")
    print(f"Train set: {len(X_train)} samples, Test set: {len(X_test)} samples\n")

    import time
    for idx, (name, pipeline) in enumerate(models, 1):
        print(f"[{idx}/{len(models)}] Training {name}...")
        start_time = time.time()
        pipeline.fit(X_train, y_train)
        train_time = time.time() - start_time
        
        res = evaluate_and_report(pipeline, X_test, y_test, name)
        res['train_time'] = train_time
        results.append(res)
        
        # save each model
        model_path = Path(args.out_dir) / f"{name}.joblib"
        joblib.dump(pipeline, model_path)
        size_mb = model_path.stat().st_size / (1024 * 1024)
        print(f"  Saved to {model_path} ({size_mb:.2f} MB, trained in {train_time:.1f}s)\n")

    # sort by rmse ascending
    results = sorted(results, key=lambda r: r["rmse"])
    print("Summary (best first):")
    for r in results:
        print(f"- {r['name']}: RMSE={r['rmse']:.4f}, R2={r['r2']:.4f}")

    # Save the best model in a feature-name-safe format
    if results:
        best_name = results[0]["name"]
        best_model = None
        for n, p in models:
            if n == best_name:
                best_model = p
                break
        if best_model is not None:
            best_path = Path(args.out_dir) / "best.joblib"
            # save a dict containing the pipeline and the training feature names
            feature_names = list(X.columns)
            joblib.dump({"pipeline": best_model, "feature_names": feature_names}, best_path)
            print(f"Saved best model '{best_name}' with feature names to {best_path}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Train house price models on cleaned real estate CSV")
    parser.add_argument("--data", type=str, default="Data/cleaned_real_estate.csv", help="Path to dataset CSV")
    parser.add_argument("--target", type=str, default="price", help="Target column name for house price")
    parser.add_argument("--out-dir", type=str, default="models", help="Directory to save trained models")
    parser.add_argument("--test-size", type=float, default=0.2, help="Test split fraction")
    parser.add_argument("--sample-frac", type=float, default=1.0, help="If <1.0, sample this fraction of the CSV after reading nrows")
    parser.add_argument("--nrows", type=int, default=None, help="If set, read only this many rows (useful for preview)")
    parser.add_argument("--preview", action="store_true", help="Show head and info then exit")
    parser.add_argument("--drop-missing-frac", dest="drop_missing_frac", type=float, default=0.5, help="Drop columns with missing fraction greater than this")
    args = parser.parse_args()
    main(args)
