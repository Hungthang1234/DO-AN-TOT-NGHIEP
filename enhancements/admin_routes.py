"""
Admin Dashboard - Model Management
View, compare, and switch between models
"""

from flask import Blueprint, render_template, jsonify, request
from scripts.model_manager import ModelManager
from pathlib import Path
import joblib
import json

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')
manager = ModelManager()

@admin_bp.route('/models')
def models_dashboard():
    """Model management dashboard"""
    models = manager.list_available_models()
    active_model = manager.models_config.get('active_model', 'best_clean')
    
    return render_template('admin_models.html',
                          models=models,
                          active_model=active_model)

@admin_bp.route('/api/models')
def api_models():
    """API endpoint to list models"""
    models = manager.list_available_models()
    return jsonify({
        'success': True,
        'models': models,
        'active_model': manager.models_config.get('active_model')
    })

@admin_bp.route('/api/models/<model_name>')
def api_model_details(model_name):
    """Get detailed info about a specific model"""
    model_file = Path('models') / f'{model_name}.joblib'
    
    if not model_file.exists():
        return jsonify({'success': False, 'error': 'Model not found'}), 404
    
    try:
        model_data = joblib.load(model_file)
        
        details = {
            'name': model_name,
            'model_name': model_data.get('model_name', 'Unknown'),
            'features': model_data.get('feature_names', []),
            'feature_count': len(model_data.get('feature_names', [])),
            'metrics': {
                'r2': model_data.get('r2', 0),
                'train_r2': model_data.get('train_r2', 0),
                'rmse': model_data.get('rmse', 0),
                'train_rmse': model_data.get('train_rmse', 0),
                'mae': model_data.get('mae', 0)
            },
            'dataset': {
                'train_samples': model_data.get('train_samples', 0),
                'test_samples': model_data.get('test_samples', 0),
                'data_source': model_data.get('data_source', 'Unknown')
            },
            'trained_date': model_data.get('trained_date', 'Unknown'),
            'target': model_data.get('target', 'price')
        }
        
        return jsonify({'success': True, 'model': details})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@admin_bp.route('/api/models/<model_name>/activate', methods=['POST'])
def api_activate_model(model_name):
    """Set a model as active"""
    success = manager.set_active_model(model_name)
    
    if success:
        return jsonify({
            'success': True,
            'message': f'Model {model_name} is now active',
            'active_model': model_name
        })
    else:
        return jsonify({
            'success': False,
            'error': 'Failed to activate model'
        }), 400

@admin_bp.route('/api/models/compare')
def api_compare_models():
    """Compare all models"""
    comparison = manager.compare_models()
    
    return jsonify({
        'success': True,
        'comparison': comparison.to_dict('records')
    })

@admin_bp.route('/api/data/fetch', methods=['POST'])
def api_fetch_data():
    """Fetch data from external APIs"""
    from scripts.fetch_external_data import RealEstateAPIClient
    
    data = request.json
    source = data.get('source')
    
    client = RealEstateAPIClient()
    
    try:
        if source == 'singapore':
            year = data.get('year', 2024)
            month = data.get('month')
            df = client.fetch_singapore_hdb_data(year, month)
            
        elif source == 'zillow':
            df = client.fetch_zillow_data(
                api_key=data.get('api_key'),
                location=data.get('location'),
                max_results=data.get('max_results', 100)
            )
            
        else:
            return jsonify({'success': False, 'error': 'Unknown source'}), 400
        
        if df.empty:
            return jsonify({'success': False, 'error': 'No data fetched'}), 400
        
        # Save data
        from datetime import datetime
        filename = f'Data/api_{source}_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv'
        df.to_csv(filename, index=False)
        
        return jsonify({
            'success': True,
            'records': len(df),
            'filename': filename,
            'columns': list(df.columns)
        })
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@admin_bp.route('/api/models/train', methods=['POST'])
def api_train_model():
    """Train a new model"""
    data = request.json
    
    try:
        model_data = manager.train_new_model(
            data_file=data.get('data_file'),
            model_name=data.get('model_name'),
            model_type=data.get('model_type', 'lightgbm'),
            features=data.get('features')
        )
        
        return jsonify({
            'success': True,
            'model_name': data.get('model_name'),
            'metrics': {
                'r2': model_data.get('r2'),
                'rmse': model_data.get('rmse'),
                'mae': model_data.get('mae')
            }
        })
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500
