"""
Flask web application for house price prediction
"""
from flask import Flask, render_template, request, jsonify
from pathlib import Path
import pandas as pd
import numpy as np
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

# Cache for city data
CITY_CACHE = {}

def load_cities_data():
    """Load and cache city data from CSV"""
    global CITY_CACHE
    try:
        data_path = Path("Data/cleaned_real_estate.csv")
        if not data_path.exists():
            print("⚠ Data file not found for city lookup")
            return
        
        print("Loading city data...")
        # Read only necessary columns
        df = pd.read_csv(data_path, usecols=['country', 'city'])
        
        # Group by country and get unique cities
        for country in df['country'].unique():
            cities = df[df['country'] == country]['city'].unique().tolist()
            cities.sort()
            CITY_CACHE[country] = cities
        
        print(f"✓ Loaded cities for {len(CITY_CACHE)} countries")
    except Exception as e:
        print(f"❌ Error loading city data: {e}")

# Load cities data at startup
load_cities_data()


@app.route('/get_countries')
def get_countries():
    """Get list of all available countries"""
    try:
        countries = list(CITY_CACHE.keys())
        return jsonify({'success': True, 'countries': countries})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})


@app.route('/get_cities/<country>')
def get_cities(country):
    """Get list of cities for a specific country"""
    try:
        if country not in CITY_CACHE:
            return jsonify({'success': False, 'error': f'No cities found for {country}'})
        
        return jsonify({'success': True, 'cities': CITY_CACHE[country]})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})


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
        
        # Get data from JSON body (not form data)
        form_data = request.get_json() or {}
        
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
            # Skip empty values
            if not value or str(value).strip() == '':
                continue
            # Try to convert to numeric if possible
            try:
                input_data[key] = float(value)
            except (ValueError, TypeError):
                input_data[key] = value
        
        # Create DataFrame with single row
        df = pd.DataFrame([input_data])
        
        # Create date column from year and month if not present
        if 'date' not in df.columns and 'year' in df.columns and 'month' in df.columns:
            # Create date string in YYYY-MM-DD format
            year = int(df['year'].iloc[0]) if not pd.isna(df['year'].iloc[0]) else 2024
            month = int(df['month'].iloc[0]) if not pd.isna(df['month'].iloc[0]) else 1
            df['date'] = f"{year}-{month:02d}-01"
        
        # Debug: print received data
        print(f"DEBUG - Received data: {input_data}")
        print(f"DEBUG - DataFrame columns: {list(df.columns)}")
        print(f"DEBUG - DataFrame values:\n{df}")
        
        # Align columns if feature_names available
        if feature_names:
            print(f"DEBUG - Expected features: {feature_names}")
            # Add missing columns - use median/mode from training data instead of 0
            for col in feature_names:
                if col not in df.columns:
                    # For missing columns, we should not fill with 0 as it affects prediction
                    # Instead, let the pipeline's imputer handle it
                    df[col] = np.nan
            
            # Reorder to match training
            df = df[feature_names]
        
        # Don't convert to numeric here - let the pipeline handle it
        print(f"DEBUG - Final DataFrame before prediction:\n{df}")
        
        # Make prediction - ensure DataFrame has proper feature names for LGBMRegressor
        # Convert to numpy and back to DataFrame to ensure clean column names
        df_clean = pd.DataFrame(df.values, columns=feature_names)
        prediction = pipeline.predict(df_clean)[0]
        
        # Ensure prediction is not negative
        prediction = max(0, prediction)
        
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
        
        # Make predictions - ensure DataFrame has proper feature names for LGBMRegressor
        # Convert to clean DataFrame to avoid NAType and feature name warnings
        df_clean = pd.DataFrame(df.values, columns=feature_names if feature_names else df.columns)
        predictions = pipeline.predict(df_clean)
        
        # Ensure all predictions are non-negative
        predictions = np.maximum(0, predictions)
        
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

@app.route('/analytics', methods=['GET'])
def analytics():
    """Get analytics data for visualization with advanced filters"""
    try:
        # Get filters from query parameters
        selected_countries = request.args.getlist('countries')
        year_from = request.args.get('year_from', type=int)
        year_to = request.args.get('year_to', type=int)
        selected_property_types = request.args.getlist('property_types')
        price_min = request.args.get('price_min', type=float)
        price_max = request.args.get('price_max', type=float)
        
        # Load sample data for analysis
        data_path = Path('Data/cleaned_real_estate.csv')
        if not data_path.exists():
            return jsonify({
                'success': False,
                'error': 'Data file not found. Please ensure cleaned_real_estate.csv exists in Data folder.'
            }), 404
        
        # Load sample of data (limit to 15000 rows for better analysis)
        df = pd.read_csv(data_path, nrows=15000)
        
        # Apply filters
        if selected_countries and len(selected_countries) > 0:
            df = df[df['country'].isin(selected_countries)]
        
        if year_from is not None:
            df = df[df['year'] >= year_from]
        
        if year_to is not None:
            df = df[df['year'] <= year_to]
        
        if selected_property_types and len(selected_property_types) > 0:
            df = df[df['property_type'].isin(selected_property_types)]
        
        if price_min is not None:
            df = df[df['price'] >= price_min]
        
        if price_max is not None:
            df = df[df['price'] <= price_max]
        
        # Price distribution by year
        price_by_year = df.groupby('year')['price'].agg(['mean', 'median', 'count']).reset_index()
        # Filter to recent years if data available, otherwise show all
        if len(price_by_year) > 10:
            price_by_year = price_by_year.nlargest(10, 'year')
        price_by_year = price_by_year.sort_values('year')
        
        # Price distribution by country
        price_by_country = df.groupby('country')['price'].agg(['mean', 'median', 'count']).reset_index()
        
        # Top 10 cities by average price
        top_cities = df.groupby('city')['price'].mean().nlargest(10).reset_index()
        
        # Property type distribution
        property_types = df['property_type'].value_counts().head(10).reset_index()
        property_types.columns = ['property_type', 'count']
        
        # Price distribution histogram
        price_hist, price_bins = np.histogram(df['price'], bins=20)
        price_bins_centers = [(price_bins[i] + price_bins[i+1])/2 for i in range(len(price_bins)-1)]
        
        # Area vs Price correlation
        area_price = df[['area_m2', 'price']].dropna().sample(min(1000, len(df)))
        
        # Monthly trends (group by year-month)
        try:
            if 'month' in df.columns:
                df_monthly = df[df['month'].notna() & df['year'].notna()].copy()
                if len(df_monthly) > 0:
                    df_monthly['year_month'] = df_monthly['year'].astype(int).astype(str) + '-' + df_monthly['month'].astype(int).astype(str).str.zfill(2)
                    monthly_trends = df_monthly.groupby('year_month')['price'].mean().tail(24).reset_index()
                    monthly_trends = monthly_trends.sort_values('year_month')
                else:
                    monthly_trends = pd.DataFrame({'year_month': [], 'price': []})
            else:
                monthly_trends = pd.DataFrame({'year_month': [], 'price': []})
        except Exception as e:
            print(f"Warning: Error processing monthly trends: {e}")
            monthly_trends = pd.DataFrame({'year_month': [], 'price': []})
        
        # City heatmap (top 15 cities with price levels)
        city_heatmap = df.groupby('city')['price'].agg(['mean', 'count']).reset_index()
        city_heatmap = city_heatmap[city_heatmap['count'] >= 5].nlargest(15, 'mean')
        
        # Cumulative growth (year-over-year)
        try:
            if len(price_by_year) > 1:
                growth_data = price_by_year.copy()
                growth_data['growth'] = growth_data['mean'].pct_change() * 100
                growth_data['cumulative'] = (1 + growth_data['mean'].pct_change()).cumprod() * 100
                # Replace NaN with 0 for first row
                growth_data['growth'] = growth_data['growth'].fillna(0)
                growth_data['cumulative'] = growth_data['cumulative'].fillna(100)
            else:
                growth_data = pd.DataFrame({'year': [], 'mean': [], 'growth': [], 'cumulative': []})
        except Exception as e:
            print(f"Warning: Error processing cumulative growth: {e}")
            growth_data = pd.DataFrame({'year': [], 'mean': [], 'growth': [], 'cumulative': []})
        
        # Additional statistics
        try:
            avg_area = float(df['area_m2'].mean()) if 'area_m2' in df.columns and df['area_m2'].notna().any() else 0
            price_std = float(df['price'].std()) if df['price'].notna().any() else 0
            property_type_count = int(df['property_type'].nunique()) if 'property_type' in df.columns else 0
        except Exception as e:
            print(f"Warning: Error calculating additional statistics: {e}")
            avg_area = 0
            price_std = 0
            property_type_count = 0
        
        analytics_data = {
            'success': True,
            'data': {
                'price_by_year': {
                    'labels': price_by_year['year'].tolist(),
                    'mean': price_by_year['mean'].round(2).tolist(),
                    'median': price_by_year['median'].round(2).tolist(),
                    'count': price_by_year['count'].tolist()
                },
                'price_by_country': {
                    'labels': price_by_country['country'].tolist(),
                    'mean': price_by_country['mean'].round(2).tolist(),
                    'count': price_by_country['count'].tolist()
                },
                'top_cities': {
                    'labels': top_cities['city'].tolist(),
                    'values': top_cities['price'].round(2).tolist()
                },
                'property_types': {
                    'labels': property_types['property_type'].tolist(),
                    'values': property_types['count'].tolist()
                },
                'price_distribution': {
                    'labels': [f'{int(x):,}' for x in price_bins_centers],
                    'values': price_hist.tolist()
                },
                'area_price_scatter': {
                    'area': area_price['area_m2'].tolist(),
                    'price': area_price['price'].tolist()
                },
                'monthly_trends': {
                    'labels': monthly_trends['year_month'].tolist() if len(monthly_trends) > 0 else [],
                    'values': monthly_trends['price'].round(2).tolist() if len(monthly_trends) > 0 else []
                },
                'city_heatmap': {
                    'labels': city_heatmap['city'].tolist() if len(city_heatmap) > 0 else [],
                    'values': city_heatmap['mean'].round(2).tolist() if len(city_heatmap) > 0 else [],
                    'counts': city_heatmap['count'].tolist() if len(city_heatmap) > 0 else []
                },
                'cumulative_growth': {
                    'labels': [int(x) for x in growth_data['year'].tolist()] if len(growth_data) > 0 else [],
                    'mean': [float(x) for x in growth_data['mean'].round(2).tolist()] if len(growth_data) > 0 else [],
                    'growth': [float(x) for x in growth_data['growth'].round(2).tolist()] if len(growth_data) > 0 else [],
                    'cumulative': [float(x) for x in growth_data['cumulative'].round(2).tolist()] if len(growth_data) > 0 else []
                },
                'statistics': {
                    'total_records': int(len(df)),
                    'avg_price': float(df['price'].mean()) if len(df) > 0 else 0.0,
                    'median_price': float(df['price'].median()) if len(df) > 0 else 0.0,
                    'min_price': float(df['price'].min()) if len(df) > 0 else 0.0,
                    'max_price': float(df['price'].max()) if len(df) > 0 else 0.0,
                    'total_cities': int(df['city'].nunique()) if len(df) > 0 else 0,
                    'total_countries': int(df['country'].nunique()) if len(df) > 0 else 0,
                    'year_range': f"{int(df['year'].min())} - {int(df['year'].max())}" if len(df) > 0 and df['year'].notna().any() else "N/A",
                    'avg_area': float(avg_area),
                    'price_std': float(price_std),
                    'property_type_count': int(property_type_count)
                }
            }
        }
        
        return jsonify(analytics_data)
        
    except Exception as e:
        print(f"ERROR in analytics endpoint: {str(e)}")
        traceback.print_exc()
        return jsonify({
            'success': False,
            'error': f'Error loading analytics: {str(e)}',
            'traceback': traceback.format_exc()
        }), 500


if __name__ == '__main__':
    print("\n" + "="*60)
    print("House Price Prediction Web Application")
    print("="*60)
    print(f"Model path: {MODEL_PATH}")
    print(f"Model loaded: {model_data is not None}")
    print("\nStarting Flask server...")
    print("Open http://localhost:5000 in your browser")
    print("="*60 + "\n")
    
    app.run(debug=False, host='0.0.0.0', port=5000)
