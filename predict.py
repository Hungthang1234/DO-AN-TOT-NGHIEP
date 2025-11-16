import argparse
import pandas as pd
import joblib
from pathlib import Path


def main(args):
    model_path = Path(args.model)
    if not model_path.exists():
        raise FileNotFoundError(
            f"Model not found: {model_path}\n"
            f"Make sure you've run train_pipeline.py first to create models."
        )
    
    print(f"Loading model from: {model_path}")
    loaded = joblib.load(model_path)

    # Support both raw pipeline objects and the feature-name-safe dict saved by train_pipeline
    if isinstance(loaded, dict) and "pipeline" in loaded:
        pipeline = loaded["pipeline"]
        feature_names = loaded.get("feature_names", None)
    else:
        pipeline = loaded
        feature_names = None

    df = pd.read_csv(args.input)
    if args.sample and args.sample < 1.0:
        df = df.sample(frac=args.sample, random_state=42)

    # If the saved artifact includes feature names, align columns (add missing columns with NaN)
    if feature_names is not None:
        missing = [c for c in feature_names if c not in df.columns]
        extra = [c for c in df.columns if c not in feature_names]
        
        if missing:
            print(f"⚠ Adding {len(missing)} missing columns (will be imputed): {missing[:3]}{'...' if len(missing) > 3 else ''}")
            for c in missing:
                df[c] = pd.NA
        
        if extra:
            print(f"⚠ Ignoring {len(extra)} extra columns not used during training: {extra[:3]}{'...' if len(extra) > 3 else ''}")
        
        # Reorder columns to match training order
        df = df[feature_names]

    print(f"\nMaking predictions for {len(df)} rows...")
    preds = pipeline.predict(df)
    
    # Add prediction statistics
    print(f"\nPrediction Summary:")
    print(f"  Count: {len(preds)}")
    print(f"  Mean:  {preds.mean():,.2f}")
    print(f"  Min:   {preds.min():,.2f}")
    print(f"  Max:   {preds.max():,.2f}")
    print(f"  Std:   {preds.std():,.2f}")
    
    out = pd.DataFrame({"prediction": preds})
    if args.output:
        out.to_csv(args.output, index=False)
        print(f"\n✓ Saved {len(out)} predictions to {args.output}")
    else:
        print(f"\nFirst {min(10, len(out))} predictions:")
        print(out.head(10).to_string(index=False))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Load a saved model and predict on CSV")
    parser.add_argument("--model", required=True, help="Path to saved model joblib")
    parser.add_argument("--input", required=True, help="CSV file with features (same columns used during training)")
    parser.add_argument("--output", help="CSV file to write predictions")
    parser.add_argument("--sample", type=float, default=1.0, help="If <1.0, sample fraction of input for quick checks")
    args = parser.parse_args()
    main(args)
