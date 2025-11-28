"""
Advanced Chart API - Real Estate Data Visualization
Provides comprehensive analytics and visualization endpoints
"""
from flask import Blueprint, jsonify, request
import pandas as pd
import numpy as np
from pathlib import Path
from datetime import datetime, timedelta
import json

advanced_charts_bp = Blueprint('advanced_charts', __name__, url_prefix='/api/charts')

# Load dataset
DATA_PATH = Path("Data/cleaned_real_estate.csv")

def load_data():
    """Load and cache dataset"""
    try:
        df = pd.read_csv(DATA_PATH)
        # Convert date column if exists
        if 'date' in df.columns:
            df['date'] = pd.to_datetime(df['date'], errors='coerce')
        return df
    except Exception as e:
        print(f"Error loading data: {e}")
        return None

@advanced_charts_bp.route('/overview', methods=['GET'])
def get_overview():
    """Get overview statistics for dashboard"""
    try:
        df = load_data()
        if df is None:
            return jsonify({'success': False, 'error': 'Data not available'}), 500
        
        # Get parameters
        country = request.args.get('country', 'all')
        year_range = request.args.get('year_range', '10')
        
        # Filter by country
        if country != 'all' and 'country' in df.columns:
            df = df[df['country'] == country]
        
        # Filter by year range
        if 'date' in df.columns and year_range != 'all':
            years = int(year_range)
            cutoff_date = datetime.now() - timedelta(days=years*365)
            df = df[df['date'] >= cutoff_date]
        
        # Calculate statistics
        stats = {
            'success': True,
            'total_records': len(df),
            'avg_price': float(df['price'].mean()) if 'price' in df.columns else 0,
            'median_price': float(df['price'].median()) if 'price' in df.columns else 0,
            'min_price': float(df['price'].min()) if 'price' in df.columns else 0,
            'max_price': float(df['price'].max()) if 'price' in df.columns else 0,
            'std_price': float(df['price'].std()) if 'price' in df.columns else 0,
            'property_types_count': len(df['property_type'].unique()) if 'property_type' in df.columns else 0,
            'cities_count': len(df['city'].unique()) if 'city' in df.columns else 0,
            'countries_count': len(df['country'].unique()) if 'country' in df.columns else 0
        }
        
        # Calculate YoY growth if date available
        if 'date' in df.columns and len(df) > 0:
            df_sorted = df.sort_values('date')
            df_sorted['year'] = df_sorted['date'].dt.year
            yearly_avg = df_sorted.groupby('year')['price'].mean()
            
            if len(yearly_avg) >= 2:
                last_year = yearly_avg.iloc[-1]
                prev_year = yearly_avg.iloc[-2]
                yoy_growth = ((last_year - prev_year) / prev_year) * 100
                stats['yoy_growth'] = round(float(yoy_growth), 2)
            else:
                stats['yoy_growth'] = 0
        else:
            stats['yoy_growth'] = 0
        
        return jsonify(stats)
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@advanced_charts_bp.route('/price-trend', methods=['GET'])
def get_price_trend():
    """Get price trend over time"""
    try:
        df = load_data()
        if df is None or 'date' not in df.columns:
            return jsonify({'success': False, 'error': 'Date data not available'}), 500
        
        country = request.args.get('country', 'all')
        year_range = request.args.get('year_range', '10')
        
        # Filter data
        if country != 'all':
            df = df[df['country'] == country]
        
        if year_range != 'all':
            years = int(year_range)
            cutoff_date = datetime.now() - timedelta(days=years*365)
            df = df[df['date'] >= cutoff_date]
        
        # Group by month
        df['year_month'] = df['date'].dt.to_period('M')
        monthly_data = df.groupby('year_month')['price'].agg(['mean', 'median', 'count']).reset_index()
        monthly_data['year_month'] = monthly_data['year_month'].astype(str)
        
        return jsonify({
            'success': True,
            'labels': monthly_data['year_month'].tolist(),
            'mean': monthly_data['mean'].round(2).tolist(),
            'median': monthly_data['median'].round(2).tolist(),
            'count': monthly_data['count'].tolist()
        })
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@advanced_charts_bp.route('/property-type-distribution', methods=['GET'])
def get_property_type_distribution():
    """Get property type distribution with average prices"""
    try:
        df = load_data()
        if df is None or 'property_type' not in df.columns:
            return jsonify({'success': False, 'error': 'Property type data not available'}), 500
        
        country = request.args.get('country', 'all')
        
        if country != 'all':
            df = df[df['country'] == country]
        
        # Group by property type
        type_data = df.groupby('property_type').agg({
            'price': ['mean', 'median', 'count']
        }).reset_index()
        
        type_data.columns = ['property_type', 'avg_price', 'median_price', 'count']
        type_data = type_data.sort_values('count', ascending=False).head(10)
        
        return jsonify({
            'success': True,
            'labels': type_data['property_type'].tolist(),
            'avg_prices': type_data['avg_price'].round(2).tolist(),
            'median_prices': type_data['median_price'].round(2).tolist(),
            'counts': type_data['count'].tolist()
        })
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@advanced_charts_bp.route('/price-range-distribution', methods=['GET'])
def get_price_range_distribution():
    """Get price range distribution"""
    try:
        df = load_data()
        if df is None or 'price' not in df.columns:
            return jsonify({'success': False, 'error': 'Price data not available'}), 500
        
        country = request.args.get('country', 'all')
        
        if country != 'all':
            df = df[df['country'] == country]
        
        # Define price ranges
        bins = [0, 200000, 400000, 600000, 800000, float('inf')]
        labels = ['<$200K', '$200K-$400K', '$400K-$600K', '$600K-$800K', '>$800K']
        
        df['price_range'] = pd.cut(df['price'], bins=bins, labels=labels)
        range_counts = df['price_range'].value_counts().sort_index()
        
        # Convert to percentage
        total = range_counts.sum()
        percentages = (range_counts / total * 100).round(2)
        
        return jsonify({
            'success': True,
            'labels': labels,
            'values': percentages.tolist(),
            'counts': range_counts.tolist()
        })
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@advanced_charts_bp.route('/area-distribution', methods=['GET'])
def get_area_distribution():
    """Get area size distribution"""
    try:
        df = load_data()
        if df is None:
            return jsonify({'success': False, 'error': 'Data not available'}), 500
        
        # Check for area columns
        area_col = None
        for col in ['floor_area_sqm', 'area_m2', 'area']:
            if col in df.columns:
                area_col = col
                break
        
        if area_col is None:
            return jsonify({'success': False, 'error': 'Area data not available'}), 500
        
        country = request.args.get('country', 'all')
        
        if country != 'all':
            df = df[df['country'] == country]
        
        # Define area ranges
        bins = [0, 50, 100, 150, 200, float('inf')]
        labels = ['<50m²', '50-100m²', '100-150m²', '150-200m²', '>200m²']
        
        df['area_range'] = pd.cut(df[area_col], bins=bins, labels=labels)
        area_counts = df['area_range'].value_counts().sort_index()
        
        # Convert to percentage
        total = area_counts.sum()
        percentages = (area_counts / total * 100).round(2)
        
        return jsonify({
            'success': True,
            'labels': labels,
            'values': percentages.tolist(),
            'counts': area_counts.tolist()
        })
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@advanced_charts_bp.route('/seasonal-patterns', methods=['GET'])
def get_seasonal_patterns():
    """Get seasonal price patterns (by month)"""
    try:
        df = load_data()
        if df is None or 'date' not in df.columns:
            return jsonify({'success': False, 'error': 'Date data not available'}), 500
        
        country = request.args.get('country', 'all')
        
        if country != 'all':
            df = df[df['country'] == country]
        
        # Extract month and calculate average prices
        df['month'] = df['date'].dt.month
        monthly_avg = df.groupby('month')['price'].agg(['mean', 'count']).reset_index()
        
        month_names = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 
                       'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
        
        # Ensure all months are represented
        all_months = pd.DataFrame({'month': range(1, 13)})
        monthly_avg = all_months.merge(monthly_avg, on='month', how='left').fillna(0)
        
        return jsonify({
            'success': True,
            'labels': month_names,
            'avg_prices': monthly_avg['mean'].round(2).tolist(),
            'transaction_counts': monthly_avg['count'].tolist()
        })
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@advanced_charts_bp.route('/top-cities', methods=['GET'])
def get_top_cities():
    """Get top cities by average price"""
    try:
        df = load_data()
        if df is None or 'city' not in df.columns:
            return jsonify({'success': False, 'error': 'City data not available'}), 500
        
        country = request.args.get('country', 'all')
        limit = int(request.args.get('limit', 15))
        
        if country != 'all':
            df = df[df['country'] == country]
        
        # Group by city
        city_data = df.groupby('city').agg({
            'price': ['mean', 'median', 'count']
        }).reset_index()
        
        city_data.columns = ['city', 'avg_price', 'median_price', 'count']
        
        # Filter cities with minimum transactions
        city_data = city_data[city_data['count'] >= 10]
        
        # Sort by average price and get top N
        city_data = city_data.sort_values('avg_price', ascending=False).head(limit)
        
        return jsonify({
            'success': True,
            'labels': city_data['city'].tolist(),
            'avg_prices': city_data['avg_price'].round(2).tolist(),
            'median_prices': city_data['median_price'].round(2).tolist(),
            'counts': city_data['count'].tolist()
        })
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@advanced_charts_bp.route('/price-by-type-trend', methods=['GET'])
def get_price_by_type_trend():
    """Get price trend by property type over time"""
    try:
        df = load_data()
        if df is None or 'date' not in df.columns or 'property_type' not in df.columns:
            return jsonify({'success': False, 'error': 'Required data not available'}), 500
        
        country = request.args.get('country', 'all')
        year_range = request.args.get('year_range', '10')
        
        if country != 'all':
            df = df[df['country'] == country]
        
        if year_range != 'all':
            years = int(year_range)
            cutoff_date = datetime.now() - timedelta(days=years*365)
            df = df[df['date'] >= cutoff_date]
        
        # Get top 5 property types
        top_types = df['property_type'].value_counts().head(5).index.tolist()
        df_filtered = df[df['property_type'].isin(top_types)]
        
        # Group by year and property type
        df_filtered['year'] = df_filtered['date'].dt.year
        trend_data = df_filtered.groupby(['year', 'property_type'])['price'].mean().reset_index()
        
        # Pivot to get one series per property type
        pivot_data = trend_data.pivot(index='year', columns='property_type', values='price').fillna(0)
        
        return jsonify({
            'success': True,
            'labels': [int(year) for year in pivot_data.index.tolist()],
            'datasets': [
                {
                    'label': prop_type,
                    'data': pivot_data[prop_type].round(2).tolist()
                }
                for prop_type in pivot_data.columns
            ]
        })
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@advanced_charts_bp.route('/countries', methods=['GET'])
def get_countries():
    """Get list of available countries"""
    try:
        df = load_data()
        if df is None or 'country' not in df.columns:
            return jsonify({'success': False, 'error': 'Country data not available'}), 500
        
        countries = sorted(df['country'].unique().tolist())
        
        return jsonify({
            'success': True,
            'countries': countries
        })
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@advanced_charts_bp.route('/price-heatmap', methods=['GET'])
def get_price_heatmap():
    """Get price heatmap data (year x property_type)"""
    try:
        df = load_data()
        if df is None or 'date' not in df.columns or 'property_type' not in df.columns:
            return jsonify({'success': False, 'error': 'Required data not available'}), 500
        
        country = request.args.get('country', 'all')
        
        if country != 'all':
            df = df[df['country'] == country]
        
        # Extract year
        df['year'] = df['date'].dt.year
        
        # Get top property types
        top_types = df['property_type'].value_counts().head(8).index.tolist()
        df_filtered = df[df['property_type'].isin(top_types)]
        
        # Create pivot table
        heatmap_data = df_filtered.groupby(['year', 'property_type'])['price'].mean().reset_index()
        pivot = heatmap_data.pivot(index='property_type', columns='year', values='price').fillna(0)
        
        return jsonify({
            'success': True,
            'property_types': pivot.index.tolist(),
            'years': [int(year) for year in pivot.columns.tolist()],
            'values': pivot.values.round(2).tolist()
        })
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500
