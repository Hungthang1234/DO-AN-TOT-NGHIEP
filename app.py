"""
Flask web application for house price prediction
"""
from flask import Flask, render_template, request, jsonify
from pathlib import Path
import pandas as pd
import joblib
import traceback

app = Flask(__name__)

# Load model at startup
MODEL_PATH = Path("models/best.joblib")
model_data = None

def load_model():
    """Load the trained model"""
    global model_data
    try:
        if MODEL_PATH.exists():
            model_data = joblib.load(MODEL_PATH)
            print(f"✓ Model loaded successfully from {MODEL_PATH}")
            if isinstance(model_data, dict):
                print(f"  Model: {model_data.get('model_name', 'Unknown')}")
                print(f"  Features: {len(model_data.get('feature_names', []))}")
                rmse_val = model_data.get('rmse', None)
                r2_val = model_data.get('r2', None)
                if rmse_val is not None:
                    print(f"  RMSE: {rmse_val:.2f}")
                if r2_val is not None:
                    print(f"  R²: {r2_val:.4f}")
        else:
            print(f"⚠ Model file not found at {MODEL_PATH}")
            print("  Run train_pipeline.py first to create the model")
    except Exception as e:
        print(f"❌ Error loading model: {e}")
        traceback.print_exc()

load_model()


@app.route('/')
def home():
    """Render the main page"""
    feature_names = []
    model_info = {}
    
    if model_data and isinstance(model_data, dict):
        feature_names = model_data.get('feature_names', [])
        model_info = {
            'name': model_data.get('model_name', 'Unknown'),
            'rmse': f"{model_data.get('rmse', 0):,.2f}",
            'r2': f"{model_data.get('r2', 0):.4f}",
            'target': model_data.get('target', 'price')
        }
    
    return render_template('index.html', 
                         feature_names=feature_names,
                         model_info=model_info,
                         model_loaded=model_data is not None)


@app.route('/predict', methods=['POST'])
def predict():
    """Handle prediction request"""
    try:
        if not model_data:
            return jsonify({
                'error': 'Model not loaded. Please train the model first.',
                'success': False
            })
        
        # Get form data
        form_data = request.form.to_dict()
        
        # Get model pipeline and feature names
        if isinstance(model_data, dict):
            pipeline = model_data['pipeline']
            feature_names = model_data['feature_names']
        else:
            pipeline = model_data
            feature_names = None
        
        # Convert form data to DataFrame
        input_data = {}
        for key, value in form_data.items():
            # Try to convert to numeric if possible
            try:
                input_data[key] = float(value)
            except ValueError:
                input_data[key] = value
        
        # Create DataFrame with single row
        df = pd.DataFrame([input_data])
        
        # Align columns if feature_names available
        if feature_names:
            # Add missing columns with NaN
            for col in feature_names:
                if col not in df.columns:
                    df[col] = pd.NA
            
            # Reorder to match training
            df = df[feature_names]
        
        # Make prediction
        prediction = pipeline.predict(df)[0]
        
        return jsonify({
            'success': True,
            'prediction': float(prediction),
            'formatted_prediction': f"{prediction:,.2f}",
            'input_data': input_data
        })
        
    except Exception as e:
        error_msg = str(e)
        traceback.print_exc()
        return jsonify({
            'success': False,
            'error': f'Prediction error: {error_msg}'
        })


@app.route('/predict_batch', methods=['POST'])
def predict_batch():
    """Handle batch prediction from CSV file"""
    try:
        if not model_data:
            return jsonify({
                'error': 'Model not loaded. Please train the model first.',
                'success': False
            })
        
        # Check if file was uploaded
        if 'file' not in request.files:
            return jsonify({
                'success': False,
                'error': 'No file uploaded'
            })
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({
                'success': False,
                'error': 'No file selected'
            })
        
        # Read CSV
        df = pd.read_csv(file)
        
        # Get model pipeline and feature names
        if isinstance(model_data, dict):
            pipeline = model_data['pipeline']
            feature_names = model_data['feature_names']
        else:
            pipeline = model_data
            feature_names = None
        
        # Align columns if feature_names available
        if feature_names:
            # Add missing columns
            for col in feature_names:
                if col not in df.columns:
                    df[col] = pd.NA
            
            # Reorder
            df = df[feature_names]
        
        # Make predictions
        predictions = pipeline.predict(df)
        
        # Prepare results
        results = []
        for idx, pred in enumerate(predictions[:100]):  # Limit to 100 rows for display
            results.append({
                'row': idx + 1,
                'prediction': float(pred),
                'formatted': f"{pred:,.2f}"
            })
        
        return jsonify({
            'success': True,
            'count': len(predictions),
            'predictions': results,
            'statistics': {
                'mean': float(predictions.mean()),
                'min': float(predictions.min()),
                'max': float(predictions.max()),
                'std': float(predictions.std())
            }
        })
        
    except Exception as e:
        error_msg = str(e)
        traceback.print_exc()
        return jsonify({
            'success': False,
            'error': f'Batch prediction error: {error_msg}'
        })


@app.route('/reload_model', methods=['POST'])
def reload_model():
    """Reload the model"""
    try:
        load_model()
        if model_data:
            return jsonify({
                'success': True,
                'message': 'Model reloaded successfully'
            })
        else:
            return jsonify({
                'success': False,
                'error': 'Model file not found'
            })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        })


if __name__ == '__main__':
    print("\n" + "="*60)
    print("House Price Prediction Web Application")
    print("="*60)
    print(f"Model path: {MODEL_PATH}")
    print(f"Model loaded: {model_data is not None}")
    print("\nStarting Flask server...")
    print("Open http://localhost:5000 in your browser")
    print("="*60 + "\n")
    
    app.run(debug=True, host='0.0.0.0', port=5000)
