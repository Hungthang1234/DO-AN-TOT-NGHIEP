"""
API Endpoints cho các tính năng nâng cao
- /predict_trend: Dự đoán xu hướng giá 5-10 năm
- /compare_areas: So sánh giá nhiều khu vực
- /calculate_roi: Tính lợi nhuận đầu tư
- /explain_prediction: SHAP explanation
"""

from flask import Blueprint, request, jsonify
import pandas as pd
import numpy as np
import joblib
from pathlib import Path
import sys

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

# Import custom modules
try:
    from models.shap_explainer import SHAPExplainer
except:
    SHAPExplainer = None

# Create blueprint
api_bp = Blueprint('enhancements', __name__, url_prefix='/api')

# Load model globally - try multiple paths
MODEL_PATHS = [
    Path(__file__).parent.parent.parent / 'models' / 'lightgbm_full_dataset.joblib',
    Path(__file__).parent.parent.parent / 'models' / 'best_clean.joblib'
]

model_data = None
MODEL_PATH = None

for path in MODEL_PATHS:
    if path.exists():
        try:
            model_data = joblib.load(path)
            MODEL_PATH = path
            print(f"✓ API loaded model from: {path.name}")
            break
        except:
            continue


@api_bp.route('/predict_trend', methods=['POST'])
def predict_trend():
    """
    Dự đoán xu hướng giá trong 5-10 năm tới
    
    Input JSON:
    {
        "country": "Vietnam",
        "city": "Ho Chi Minh City",
        "area_m2": 100,
        "property_type": "Apartment",
        "start_year": 2024,
        "years_ahead": 5
    }
    
    Output:
    {
        "trend": [
            {"year": 2024, "predicted_price": 500000},
            {"year": 2025, "predicted_price": 520000},
            ...
        ],
        "growth_rate": 4.2,  // % per year
        "total_growth": 21.0  // % over period
    }
    """
    try:
        data = request.json
        
        # Validate input
        required_fields = ['country', 'city', 'area_m2', 'property_type']
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'Missing field: {field}'}), 400
        
        start_year = data.get('start_year', 2024)
        years_ahead = min(data.get('years_ahead', 5), 10)  # Max 10 years
        
        # Prepare base features
        base_features = {
            'country': data['country'],
            'city': data['city'],
            'area_m2': data['area_m2'],
            'property_type': data['property_type'],
            'month': data.get('month', 6)  # Default June
        }
        
        # Predict for each year
        trend = []
        for year_offset in range(years_ahead + 1):
            year = start_year + year_offset
            
            # Create features for this year
            features = base_features.copy()
            features['year'] = year
            
            # Convert to DataFrame
            X = pd.DataFrame([features])
            
            # Encode categorical features if needed
            if 'label_encoders' in model_data:
                for col, le in model_data['label_encoders'].items():
                    if col in X.columns:
                        X[col] = X[col].map(lambda x: le.transform([x])[0] if x in le.classes_ else -1)
            
            # Predict
            model = model_data['model']
            predicted_price = float(model.predict(X)[0])
            
            trend.append({
                'year': year,
                'predicted_price': round(predicted_price, 2)
            })
        
        # Calculate growth metrics
        first_price = trend[0]['predicted_price']
        last_price = trend[-1]['predicted_price']
        
        total_growth = ((last_price - first_price) / first_price) * 100
        avg_growth_rate = total_growth / years_ahead
        
        return jsonify({
            'trend': trend,
            'growth_rate': round(avg_growth_rate, 2),
            'total_growth': round(total_growth, 2),
            'period': f'{start_year}-{start_year + years_ahead}'
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@api_bp.route('/compare_areas', methods=['POST'])
def compare_areas():
    """
    So sánh giá giữa nhiều khu vực
    
    Input JSON:
    {
        "base_features": {
            "country": "Vietnam",
            "area_m2": 100,
            "property_type": "Apartment",
            "year": 2024
        },
        "cities": ["Ho Chi Minh City", "Hanoi", "Da Nang"]
    }
    
    Output:
    {
        "comparisons": [
            {"city": "Ho Chi Minh City", "price": 500000, "rank": 1},
            {"city": "Hanoi", "price": 450000, "rank": 2},
            ...
        ],
        "cheapest": {"city": "Da Nang", "price": 350000},
        "most_expensive": {"city": "Ho Chi Minh City", "price": 500000},
        "price_range": {"min": 350000, "max": 500000, "difference": 150000}
    }
    """
    try:
        data = request.json
        
        base_features = data.get('base_features', {})
        cities = data.get('cities', [])
        
        if not cities:
            return jsonify({'error': 'No cities provided'}), 400
        
        comparisons = []
        
        for city in cities:
            # Create features for this city
            features = base_features.copy()
            features['city'] = city
            features['month'] = features.get('month', 6)
            
            # Convert to DataFrame
            X = pd.DataFrame([features])
            
            # Encode categorical features if needed
            if 'label_encoders' in model_data:
                for col, le in model_data['label_encoders'].items():
                    if col in X.columns:
                        X[col] = X[col].map(lambda x: le.transform([x])[0] if x in le.classes_ else -1)
            
            # Predict
            model = model_data['model']
            predicted_price = float(model.predict(X)[0])
            
            comparisons.append({
                'city': city,
                'price': round(predicted_price, 2)
            })
        
        # Sort by price
        comparisons_sorted = sorted(comparisons, key=lambda x: x['price'], reverse=True)
        
        # Add rank
        for i, comp in enumerate(comparisons_sorted, 1):
            comp['rank'] = i
        
        # Calculate statistics
        prices = [c['price'] for c in comparisons]
        
        return jsonify({
            'comparisons': comparisons_sorted,
            'cheapest': min(comparisons, key=lambda x: x['price']),
            'most_expensive': max(comparisons, key=lambda x: x['price']),
            'price_range': {
                'min': round(min(prices), 2),
                'max': round(max(prices), 2),
                'difference': round(max(prices) - min(prices), 2),
                'difference_percent': round(((max(prices) - min(prices)) / min(prices)) * 100, 2)
            }
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@api_bp.route('/calculate_roi', methods=['POST'])
def calculate_roi():
    """
    Tính toán lợi nhuận đầu tư bất động sản
    
    Input JSON:
    {
        "purchase_price": 500000,
        "purchase_year": 2024,
        "sell_year": 2029,
        "features": {
            "country": "Vietnam",
            "city": "Ho Chi Minh City",
            "area_m2": 100,
            "property_type": "Apartment"
        },
        "additional_costs": 50000,  // Renovation, etc
        "rental_income_per_year": 30000  // Optional
    }
    
    Output:
    {
        "purchase_price": 500000,
        "predicted_sell_price": 625000,
        "capital_gain": 125000,
        "total_rental_income": 150000,
        "total_costs": 50000,
        "net_profit": 225000,
        "roi_percent": 45.0,
        "annualized_return": 9.0,
        "holding_period_years": 5
    }
    """
    try:
        data = request.json
        
        purchase_price = data.get('purchase_price', 0)
        purchase_year = data.get('purchase_year')
        sell_year = data.get('sell_year')
        features = data.get('features', {})
        additional_costs = data.get('additional_costs', 0)
        rental_income_per_year = data.get('rental_income_per_year', 0)
        
        if not all([purchase_price, purchase_year, sell_year, features]):
            return jsonify({'error': 'Missing required fields'}), 400
        
        holding_period = sell_year - purchase_year
        
        if holding_period <= 0:
            return jsonify({'error': 'Sell year must be after purchase year'}), 400
        
        # Predict sell price
        sell_features = features.copy()
        sell_features['year'] = sell_year
        sell_features['month'] = sell_features.get('month', 6)
        
        X = pd.DataFrame([sell_features])
        
        # Encode categorical features if needed
        if 'label_encoders' in model_data:
            for col, le in model_data['label_encoders'].items():
                if col in X.columns:
                    X[col] = X[col].map(lambda x: le.transform([x])[0] if x in le.classes_ else -1)
        
        model = model_data['model']
        predicted_sell_price = float(model.predict(X)[0])
        
        # Calculate ROI
        capital_gain = predicted_sell_price - purchase_price
        total_rental_income = rental_income_per_year * holding_period
        net_profit = capital_gain + total_rental_income - additional_costs
        
        total_investment = purchase_price + additional_costs
        roi_percent = (net_profit / total_investment) * 100
        annualized_return = roi_percent / holding_period
        
        return jsonify({
            'purchase_price': round(purchase_price, 2),
            'predicted_sell_price': round(predicted_sell_price, 2),
            'capital_gain': round(capital_gain, 2),
            'total_rental_income': round(total_rental_income, 2),
            'total_costs': round(additional_costs, 2),
            'net_profit': round(net_profit, 2),
            'roi_percent': round(roi_percent, 2),
            'annualized_return': round(annualized_return, 2),
            'holding_period_years': holding_period,
            'recommendation': 'Good investment' if roi_percent > 50 else 'Moderate investment' if roi_percent > 20 else 'Low return'
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@api_bp.route('/explain_prediction', methods=['POST'])
def explain_prediction():
    """
    Giải thích dự đoán bằng SHAP
    
    Input JSON:
    {
        "country": "Vietnam",
        "city": "Ho Chi Minh City",
        "area_m2": 100,
        "property_type": "Apartment",
        "year": 2024
    }
    
    Output:
    {
        "prediction": 500000,
        "base_value": 450000,
        "features": [
            {"name": "city", "value": "Ho Chi Minh City", "contribution": 80000},
            {"name": "area_m2", "value": 100, "contribution": 50000},
            ...
        ]
    }
    """
    try:
        if SHAPExplainer is None:
            return jsonify({'error': 'SHAP not available'}), 500
        
        data = request.json
        
        # Create explainer
        explainer = SHAPExplainer(MODEL_PATH)
        
        # Load background data (sample from training)
        data_path = Path(__file__).parent.parent.parent / 'Data' / 'cleaned_real_estate.csv'
        df = pd.read_csv(data_path)
        
        if 'price' in df.columns:
            X_bg = df.drop(columns=['price', 'price_per_m2'], errors='ignore').sample(n=100, random_state=42)
        else:
            X_bg = df.sample(n=100, random_state=42)
        
        explainer.create_explainer(X_bg)
        
        # Explain prediction
        explanation = explainer.explain_prediction(data)
        
        return jsonify(explanation)
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# Health check
@api_bp.route('/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'model_loaded': model_data is not None,
        'shap_available': SHAPExplainer is not None
    })
