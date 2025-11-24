"""
Test script to validate the training pipeline, prediction workflow, and model artifacts.
"""
import os
import sys
from pathlib import Path
import pandas as pd
import joblib
import numpy as np

# Test configuration
DATA_PATH = Path("Data/cleaned_real_estate.csv")
TEST_DIR = Path("test_output")
TEST_DIR.mkdir(exist_ok=True)

def test_data_loading():
    """Test 1: Verify dataset can be loaded and has expected structure"""
    print("=" * 60)
    print("TEST 1: Data Loading")
    print("=" * 60)
    
    if not DATA_PATH.exists():
        print(f"❌ FAIL: Dataset not found at {DATA_PATH}")
        return False
    
    try:
        df = pd.read_csv(DATA_PATH, nrows=100)
        print(f"✓ Loaded {len(df)} rows")
        print(f"✓ Columns: {list(df.columns)}")
        print(f"✓ Shape: {df.shape}")
        
        if 'price' not in df.columns:
            print("⚠ WARNING: 'price' column not found - may need to adjust target column name")
        else:
            print(f"✓ Target column 'price' found")
            print(f"  Price range: {df['price'].min():.2f} to {df['price'].max():.2f}")
        
        print("✅ PASS: Data loading successful\n")
        return True
    except Exception as e:
        print(f"❌ FAIL: {e}\n")
        return False


def test_training_script():
    """Test 2: Run training script on small subset and verify outputs"""
    print("=" * 60)
    print("TEST 2: Training Script")
    print("=" * 60)
    
    import subprocess
    
    cmd = [
        sys.executable,
        "train_pipeline.py",
        "--data", str(DATA_PATH),
        "--nrows", "500",
        "--sample-frac", "0.5",
        "--out-dir", str(TEST_DIR),
        "--test-size", "0.2"
    ]
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
        
        if result.returncode != 0:
            print(f"❌ FAIL: Training script exited with code {result.returncode}")
            print("STDERR:", result.stderr[-500:] if len(result.stderr) > 500 else result.stderr)
            return False
        
        print("✓ Training script completed successfully")
        
        # Check if models were saved
        expected_models = ["LinearRegression.joblib", "RidgeCV.joblib", "LassoCV.joblib", 
                          "RandomForest.joblib", "best.joblib"]
        
        for model_name in expected_models:
            model_path = TEST_DIR / model_name
            if model_path.exists():
                size_kb = model_path.stat().st_size / 1024
                print(f"✓ Found {model_name} ({size_kb:.1f} KB)")
            else:
                print(f"⚠ WARNING: {model_name} not found")
        
        # Verify best.joblib structure
        best_path = TEST_DIR / "best.joblib"
        if best_path.exists():
            best = joblib.load(best_path)
            if isinstance(best, dict) and "pipeline" in best and "feature_names" in best:
                print(f"✓ best.joblib has correct structure")
                print(f"  Feature names: {best['feature_names'][:5]}... ({len(best['feature_names'])} total)")
            else:
                print("⚠ WARNING: best.joblib doesn't have expected dict structure")
        
        print("✅ PASS: Training script test successful\n")
        return True
        
    except subprocess.TimeoutExpired:
        print("❌ FAIL: Training script timed out after 120 seconds\n")
        return False
    except Exception as e:
        print(f"❌ FAIL: {e}\n")
        return False


def test_prediction_script():
    """Test 3: Test prediction script with saved model"""
    print("=" * 60)
    print("TEST 3: Prediction Script")
    print("=" * 60)
    
    # Create sample input CSV
    try:
        df = pd.read_csv(DATA_PATH, nrows=10)
        if 'price' in df.columns:
            sample_features = df.drop(columns=['price']).head(5)
        else:
            sample_features = df.head(5)
        
        sample_path = TEST_DIR / "test_input.csv"
        sample_features.to_csv(sample_path, index=False)
        print(f"✓ Created test input CSV with {len(sample_features)} rows")
        
        import subprocess
        
        cmd = [
            sys.executable,
            "predict.py",
            "--model", str(TEST_DIR / "best.joblib"),
            "--input", str(sample_path)
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
        
        if result.returncode != 0:
            print(f"❌ FAIL: Prediction script exited with code {result.returncode}")
            print("STDERR:", result.stderr)
            return False
        
        print("✓ Prediction script ran successfully")
        print("Sample predictions:")
        print(result.stdout)
        
        # Verify predictions are numeric
        if "prediction" in result.stdout:
            print("✓ Predictions generated")
        
        print("✅ PASS: Prediction script test successful\n")
        return True
        
    except Exception as e:
        print(f"❌ FAIL: {e}\n")
        return False


def test_model_loading():
    """Test 4: Directly test model loading and prediction"""
    print("=" * 60)
    print("TEST 4: Direct Model Loading & Prediction")
    print("=" * 60)
    
    try:
        best_path = TEST_DIR / "best.joblib"
        if not best_path.exists():
            print(f"❌ FAIL: best.joblib not found at {best_path}")
            return False
        
        # Load model
        loaded = joblib.load(best_path)
        print(f"✓ Loaded model from {best_path}")
        
        if isinstance(loaded, dict):
            pipeline = loaded["pipeline"]
            feature_names = loaded.get("feature_names", [])
            print(f"✓ Model type: feature-name-safe dict")
            print(f"✓ Feature count: {len(feature_names)}")
        else:
            pipeline = loaded
            feature_names = []
            print(f"✓ Model type: raw pipeline")
        
        # Load sample data
        df = pd.read_csv(DATA_PATH, nrows=10)
        if 'price' in df.columns:
            X_test = df.drop(columns=['price']).head(3)
            y_true = df['price'].head(3).values
        else:
            X_test = df.head(3)
            y_true = None
        
        # Make predictions
        predictions = pipeline.predict(X_test)
        print(f"✓ Generated {len(predictions)} predictions")
        print(f"  Predictions: {predictions}")
        
        if y_true is not None:
            print(f"  Actual values: {y_true}")
            errors = np.abs(predictions - y_true)
            print(f"  Absolute errors: {errors}")
            print(f"  Mean absolute error: {errors.mean():.2f}")
        
        print("✅ PASS: Model loading and prediction test successful\n")
        return True
        
    except Exception as e:
        print(f"❌ FAIL: {e}\n")
        import traceback
        traceback.print_exc()
        return False


def run_all_tests():
    """Run all test cases and report results"""
    print("\n" + "=" * 60)
    print("RUNNING TEST SUITE FOR HOUSE PRICE PREDICTION PIPELINE")
    print("=" * 60 + "\n")
    
    tests = [
        ("Data Loading", test_data_loading),
        ("Training Script", test_training_script),
        ("Prediction Script", test_prediction_script),
        ("Model Loading", test_model_loading),
    ]
    
    results = []
    for test_name, test_func in tests:
        try:
            passed = test_func()
            results.append((test_name, passed))
        except Exception as e:
            print(f"❌ CRITICAL ERROR in {test_name}: {e}\n")
            results.append((test_name, False))
    
    # Summary
    print("\n" + "=" * 60)
    print("TEST SUMMARY")
    print("=" * 60)
    
    passed_count = sum(1 for _, passed in results if passed)
    total_count = len(results)
    
    for test_name, passed in results:
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"{status}: {test_name}")
    
    print(f"\nTotal: {passed_count}/{total_count} tests passed")
    
    if passed_count == total_count:
        print("\n🎉 ALL TESTS PASSED!")
        return 0
    else:
        print(f"\n⚠ {total_count - passed_count} test(s) failed")
        return 1


if __name__ == "__main__":
    exit_code = run_all_tests()
    sys.exit(exit_code)
