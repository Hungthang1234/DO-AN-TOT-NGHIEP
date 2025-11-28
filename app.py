"""
Flask web application for house price prediction
"""
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from pathlib import Path
import pandas as pd
import numpy as np
import joblib
import traceback
import time
import json
import sys
from datetime import datetime
from pathlib import Path

# Add scripts/utils to path for imports
sys.path.insert(0, str(Path(__file__).parent / 'scripts' / 'utils'))

from logger_config import ModelLogger, PredictionLogger, AnalyticsLogger

app = Flask(__name__)

# Enable CORS for all routes
CORS(app)

# Register enhancement APIs
try:
    sys.path.insert(0, str(Path(__file__).parent / 'enhancements'))
    from api.endpoints import api_bp
    app.register_blueprint(api_bp)
    print("✓ Enhancement APIs registered successfully")
except Exception as e:
    print(f"⚠ Could not load enhancement APIs: {e}")

# Register admin routes
try:
    from enhancements.admin_routes import admin_bp
    app.register_blueprint(admin_bp)
    print("✓ Admin routes registered successfully")
except Exception as e:
    print(f"⚠ Could not load admin routes: {e}")

# Initialize External API Predictor
try:
    sys.path.insert(0, str(Path(__file__).parent / 'scripts'))
    from external_api_predictor import ExternalAPIPredictor
    external_predictor = ExternalAPIPredictor()
    print("✓ External API Predictor initialized")
except Exception as e:
    external_predictor = None
    print(f"⚠ Could not load External API Predictor: {e}")

# Register Advanced Charts API
try:
    from enhancements.advanced_charts_api import advanced_charts_bp
    app.register_blueprint(advanced_charts_bp)
    print("✓ Advanced Charts API registered successfully")
except Exception as e:
    print(f"⚠ Could not load Advanced Charts API: {e}")

# Load model at startup - Using clean model without overfitting
MODEL_PATH = Path("models/best_clean.joblib")
METADATA_PATH = Path("config/model_metadata.json")
model_data = None
model_metadata = None

def save_model_metadata():
    """Save model metadata to JSON file"""
    global model_data, model_metadata
    try:
        if model_data and isinstance(model_data, dict):
            metadata = {
                'model_name': model_data.get('model_name', 'Unknown'),
                'version': '1.0.0',
                'trained_date': datetime.now().strftime('%Y-%m-%d'),
                'metrics': {
                    'rmse': float(model_data.get('rmse', 0)),
                    'r2': float(model_data.get('r2', 0)),
                    'mae': float(model_data.get('mae', 0))
                },
                'features': model_data.get('feature_names', []),
                'feature_count': len(model_data.get('feature_names', [])),
                'training_info': {
                    'dataset': 'cleaned_real_estate.csv',
                    'total_samples': model_data.get('train_samples', 0) + model_data.get('test_samples', 0),
                    'train_test_split': 0.2
                },
                'model_path': str(MODEL_PATH),
                'last_updated': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            }
            
            with open(METADATA_PATH, 'w', encoding='utf-8') as f:
                json.dump(metadata, f, indent=2, ensure_ascii=False)
            
            model_metadata = metadata
            print(f"✓ Model metadata saved to {METADATA_PATH}")
            return True
    except Exception as e:
        print(f"⚠ Error saving metadata: {e}")
    return False

def load_model_metadata():
    """Load model metadata from JSON file"""
    global model_metadata
    try:
        if METADATA_PATH.exists():
            with open(METADATA_PATH, 'r', encoding='utf-8') as f:
                model_metadata = json.load(f)
            print(f"✓ Model metadata loaded from {METADATA_PATH}")
            return True
    except Exception as e:
        print(f"⚠ Error loading metadata: {e}")
    return False

def load_model():
    """Load the trained model and metadata"""
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
                
                # Load or create metadata
                if not load_model_metadata():
                    save_model_metadata()
            else:
                print(f"⚠ Model loaded but not in expected format")
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
    """Load and cache city data from CSV + Extended country support"""
    global CITY_CACHE
    
    # Extended country-city mapping for 10+ countries
    EXTENDED_CITIES = {
        'Singapore': ['ANG MO KIO', 'BEDOK', 'BISHAN', 'BUKIT BATOK', 'BUKIT MERAH', 
                      'BUKIT PANJANG', 'BUKIT TIMAH', 'CENTRAL AREA', 'CHOA CHU KANG',
                      'CLEMENTI', 'GEYLANG', 'HOUGANG', 'JURONG EAST', 'JURONG WEST',
                      'KALLANG/WHAMPOA', 'MARINE PARADE', 'PASIR RIS', 'PUNGGOL',
                      'QUEENSTOWN', 'SEMBAWANG', 'SENGKANG', 'SERANGOON', 'TAMPINES',
                      'TOA PAYOH', 'WOODLANDS', 'YISHUN'],
        'USA': ['New York', 'Los Angeles', 'Chicago', 'Houston', 'Phoenix', 
                'Philadelphia', 'San Antonio', 'San Diego', 'Dallas', 'San Jose',
                'Austin', 'Jacksonville', 'Fort Worth', 'Columbus', 'San Francisco',
                'Charlotte', 'Indianapolis', 'Seattle', 'Denver', 'Boston',
                'Washington DC', 'Nashville', 'Las Vegas', 'Portland', 'Miami'],
        'Australia': ['Sydney', 'Melbourne', 'Brisbane', 'Perth', 'Adelaide',
                      'Gold Coast', 'Newcastle', 'Canberra', 'Sunshine Coast',
                      'Wollongong', 'Hobart', 'Geelong', 'Townsville', 'Cairns',
                      'Darwin', 'Toowoomba', 'Ballarat', 'Bendigo', 'Launceston'],
        'UK': ['London', 'Birmingham', 'Manchester', 'Leeds', 'Liverpool',
               'Sheffield', 'Bristol', 'Newcastle', 'Nottingham', 'Leicester',
               'Coventry', 'Bradford', 'Edinburgh', 'Cardiff', 'Belfast',
               'Glasgow', 'Southampton', 'Portsmouth', 'Brighton', 'Oxford'],
        'Canada': ['Toronto', 'Montreal', 'Vancouver', 'Calgary', 'Edmonton',
                   'Ottawa', 'Winnipeg', 'Quebec City', 'Hamilton', 'Kitchener',
                   'London', 'Victoria', 'Halifax', 'Oshawa', 'Windsor',
                   'Saskatoon', 'Regina', 'St. John\'s', 'Kelowna', 'Barrie'],
        'Germany': ['Berlin', 'Hamburg', 'Munich', 'Cologne', 'Frankfurt',
                    'Stuttgart', 'Dusseldorf', 'Dortmund', 'Essen', 'Leipzig',
                    'Bremen', 'Dresden', 'Hanover', 'Nuremberg', 'Duisburg',
                    'Bochum', 'Wuppertal', 'Bonn', 'Bielefeld', 'Mannheim'],
        'France': ['Paris', 'Marseille', 'Lyon', 'Toulouse', 'Nice',
                   'Nantes', 'Strasbourg', 'Montpellier', 'Bordeaux', 'Lille',
                   'Rennes', 'Reims', 'Le Havre', 'Saint-Étienne', 'Toulon',
                   'Grenoble', 'Dijon', 'Angers', 'Nîmes', 'Villeurbanne'],
        'Japan': ['Tokyo', 'Yokohama', 'Osaka', 'Nagoya', 'Sapporo',
                  'Kobe', 'Kyoto', 'Fukuoka', 'Kawasaki', 'Saitama',
                  'Hiroshima', 'Sendai', 'Chiba', 'Kitakyushu', 'Sakai',
                  'Niigata', 'Hamamatsu', 'Kumamoto', 'Okayama', 'Shizuoka'],
        'China': ['Beijing', 'Shanghai', 'Guangzhou', 'Shenzhen', 'Chengdu',
                  'Hangzhou', 'Wuhan', 'Xi\'an', 'Chongqing', 'Tianjin',
                  'Nanjing', 'Suzhou', 'Dongguan', 'Shenyang', 'Qingdao',
                  'Zhengzhou', 'Foshan', 'Jinan', 'Changsha', 'Dalian'],
        'South Korea': ['Seoul', 'Busan', 'Incheon', 'Daegu', 'Daejeon',
                        'Gwangju', 'Suwon', 'Ulsan', 'Changwon', 'Seongnam',
                        'Goyang', 'Yongin', 'Bucheon', 'Ansan', 'Cheongju',
                        'Jeonju', 'Anyang', 'Pohang', 'Gimhae', 'Jeju'],
        'India': ['Mumbai', 'Delhi', 'Bangalore', 'Hyderabad', 'Chennai',
                  'Kolkata', 'Pune', 'Ahmedabad', 'Jaipur', 'Surat',
                  'Lucknow', 'Kanpur', 'Nagpur', 'Indore', 'Thane',
                  'Bhopal', 'Visakhapatnam', 'Pimpri-Chinchwad', 'Patna', 'Vadodara'],
        'UAE': ['Dubai', 'Abu Dhabi', 'Sharjah', 'Ajman', 'Ras Al Khaimah',
                'Fujairah', 'Umm Al Quwain', 'Al Ain', 'Kalba', 'Khor Fakkan']
    }
    
    try:
        # First try to load from CSV
        data_path = Path("Data/cleaned_real_estate.csv")
        if data_path.exists():
            print("Loading city data from CSV...")
            df = pd.read_csv(data_path, usecols=['country', 'city'])
            
            # Load cities from CSV
            for country in df['country'].unique():
                cities = df[df['country'] == country]['city'].unique().tolist()
                cities.sort()
                CITY_CACHE[country] = cities
            
            print(f"✓ Loaded cities for {len(CITY_CACHE)} countries from CSV")
        
        # Merge with extended cities (add countries not in CSV)
        for country, cities in EXTENDED_CITIES.items():
            if country not in CITY_CACHE:
                CITY_CACHE[country] = sorted(cities)
                print(f"  + Added {country} with {len(cities)} cities")
        
        print(f"✓ Total: {len(CITY_CACHE)} countries with city data available")
        print(f"  Countries: {', '.join(sorted(CITY_CACHE.keys()))}")
        
    except Exception as e:
        # Fallback to extended cities only
        print(f"⚠ Error loading CSV, using extended cities only: {e}")
        CITY_CACHE.update(EXTENDED_CITIES)
        print(f"✓ Loaded {len(CITY_CACHE)} countries from extended database")

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
    """Render the main page - API Version (New)"""
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


@app.route('/select')
def version_selector():
    """Show version selector page"""
    return render_template('version_selector.html')


@app.route('/legacy')
def legacy_home():
    """Render legacy version page with old dataset"""
    return render_template('legacy.html', 
                         model_loaded=model_data is not None)


@app.route('/external_api')
def external_api_page():
    """Render External API mode page - No dataset used"""
    return render_template('external_api_mode.html')


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
        
        # Log prediction
        PredictionLogger.log_prediction(input_data, prediction, prediction_type='single')
        
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


@app.route('/predict_external_api', methods=['POST'])
def predict_external_api():
    """
    Predict using ONLY external APIs - NO local dataset
    Supports: Singapore (FREE), USA (API key required)
    """
    try:
        if not external_predictor:
            return jsonify({
                'success': False,
                'error': 'External API Predictor not initialized'
            })
        
        data = request.json
        country = data.get('country', '').lower()
        
        if country == 'singapore':
            result = external_predictor.predict_singapore_property(
                town=data.get('town'),
                flat_type=data.get('flat_type'),
                floor_area_sqm=data.get('floor_area_sqm'),
                lease_commence_date=data.get('lease_commence_date'),
                storey_range=data.get('storey_range', '04 TO 06')
            )
        elif country == 'usa':
            result = external_predictor.predict_usa_property(
                city=data.get('city'),
                state=data.get('state'),
                bedrooms=data.get('bedrooms'),
                bathrooms=data.get('bathrooms'),
                living_area_sqft=data.get('living_area_sqft'),
                lot_size_sqft=data.get('lot_size_sqft'),
                year_built=data.get('year_built'),
                api_key=data.get('api_key')
            )
        else:
            result = {
                'success': False,
                'error': f'Country {country} not supported for external API predictions'
            }
        
        return jsonify(result)
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'External API prediction error: {str(e)}'
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
        
        # Log batch prediction
        PredictionLogger.log_batch_prediction(
            batch_size=len(predictions),
            avg_price=float(predictions.mean()),
            min_price=float(predictions.min()),
            max_price=float(predictions.max())
        )
        
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
    start_time = time.time()
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
        
        # Log analytics query
        response_time = (time.time() - start_time) * 1000  # Convert to ms
        AnalyticsLogger.log_analytics_query(
            filters={
                'countries': selected_countries,
                'year_from': year_from,
                'year_to': year_to,
                'property_types': selected_property_types,
                'price_min': price_min,
                'price_max': price_max
            },
            record_count=len(df),
            response_time=response_time
        )
        
        return jsonify(analytics_data)
        
    except Exception as e:
        print(f"ERROR in analytics endpoint: {str(e)}")
        traceback.print_exc()
        return jsonify({
            'success': False,
            'error': f'Error loading analytics: {str(e)}',
            'traceback': traceback.format_exc()
        }), 500


@app.route('/logs', methods=['GET'])
def view_logs():
    """View system logs"""
    try:
        from logger_config import generate_summary_report
        
        log_type = request.args.get('type', 'summary')
        
        if log_type == 'summary':
            report = generate_summary_report()
            return jsonify({'success': True, 'data': report})
        
        elif log_type == 'training':
            history = ModelLogger.get_training_history(limit=50)
            return jsonify({
                'success': True,
                'data': history.to_dict(orient='records') if not history.empty else []
            })
        
        elif log_type == 'predictions':
            recent = PredictionLogger.get_recent_predictions(limit=100)
            stats = PredictionLogger.get_prediction_stats()
            return jsonify({
                'success': True,
                'recent_predictions': recent.to_dict(orient='records') if not recent.empty else [],
                'statistics': stats
            })
        
        elif log_type == 'best':
            best = ModelLogger.get_best_model()
            return jsonify({
                'success': True,
                'best_model': best if best else {}
            })
        
        else:
            return jsonify({'success': False, 'error': 'Invalid log type'})
            
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})


@app.route('/model_info', methods=['GET'])
def model_info():
    """Get current model information and metadata"""
    try:
        global model_metadata
        
        if model_metadata:
            return jsonify({
                'success': True,
                'metadata': model_metadata,
                'model_loaded': model_data is not None,
                'model_path': str(MODEL_PATH)
            })
        else:
            # Try to load metadata if not loaded
            if load_model_metadata():
                return jsonify({
                    'success': True,
                    'metadata': model_metadata,
                    'model_loaded': model_data is not None,
                    'model_path': str(MODEL_PATH)
                })
            else:
                return jsonify({
                    'success': False,
                    'error': 'Model metadata not found',
                    'model_loaded': model_data is not None
                })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})


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
