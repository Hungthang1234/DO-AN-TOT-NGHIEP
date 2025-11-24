"""
Logging Configuration for House Price Prediction Application
Provides centralized logging for model training, predictions, and analytics
"""

import logging
import pandas as pd
from pathlib import Path
from datetime import datetime
import json

# Paths
BASE_DIR = Path(__file__).parent
LOGS_DIR = BASE_DIR / "logs"
LOGS_DIR.mkdir(exist_ok=True)

# Log files
MODEL_TRAINING_LOG = LOGS_DIR / "model_training.csv"
PREDICTION_LOG = LOGS_DIR / "predictions.csv"
ANALYTICS_LOG = LOGS_DIR / "analytics.csv"
ERROR_LOG = LOGS_DIR / "errors.log"

# Setup file logger
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(ERROR_LOG),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)


class ModelLogger:
    """Logger for model training and evaluation"""
    
    @staticmethod
    def log_training(model_name, metrics, hyperparameters=None, notes=""):
        """
        Log model training results
        
        Args:
            model_name: Name of the model
            metrics: Dict with MAE, RMSE, R2, etc.
            hyperparameters: Dict of hyperparameters used
            notes: Additional notes
        """
        log_entry = {
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'model_name': model_name,
            'mae': metrics.get('mae', 0),
            'rmse': metrics.get('rmse', 0),
            'r2': metrics.get('r2', 0),
            'train_samples': metrics.get('train_samples', 0),
            'test_samples': metrics.get('test_samples', 0),
            'training_time_seconds': metrics.get('training_time', 0),
            'hyperparameters': json.dumps(hyperparameters) if hyperparameters else "",
            'notes': notes
        }
        
        df = pd.DataFrame([log_entry])
        
        if MODEL_TRAINING_LOG.exists():
            existing = pd.read_csv(MODEL_TRAINING_LOG)
            df = pd.concat([existing, df], ignore_index=True)
        
        df.to_csv(MODEL_TRAINING_LOG, index=False)
        logger.info(f"Logged training for {model_name}: RMSE={metrics.get('rmse'):.2f}, R²={metrics.get('r2'):.4f}")
    
    @staticmethod
    def get_best_model():
        """Get best model from training history"""
        if not MODEL_TRAINING_LOG.exists():
            return None
        
        df = pd.read_csv(MODEL_TRAINING_LOG)
        if len(df) == 0:
            return None
        
        # Best model = highest R2
        best_idx = df['r2'].idxmax()
        return df.loc[best_idx].to_dict()
    
    @staticmethod
    def get_training_history(model_name=None, limit=10):
        """Get training history, optionally filtered by model name"""
        if not MODEL_TRAINING_LOG.exists():
            return pd.DataFrame()
        
        df = pd.read_csv(MODEL_TRAINING_LOG)
        
        if model_name:
            df = df[df['model_name'] == model_name]
        
        return df.tail(limit)


class PredictionLogger:
    """Logger for predictions made by the application"""
    
    @staticmethod
    def log_prediction(input_data, prediction, prediction_type='single'):
        """
        Log a prediction
        
        Args:
            input_data: Dict of input features
            prediction: Predicted price
            prediction_type: 'single' or 'batch'
        """
        log_entry = {
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'prediction_type': prediction_type,
            'country': input_data.get('country', ''),
            'city': input_data.get('city', ''),
            'year': input_data.get('year', 0),
            'month': input_data.get('month', 0),
            'area_m2': input_data.get('area_m2', 0),
            'property_type': input_data.get('property_type', ''),
            'predicted_price': float(prediction),
            'input_json': json.dumps(input_data)
        }
        
        df = pd.DataFrame([log_entry])
        
        if PREDICTION_LOG.exists():
            existing = pd.read_csv(PREDICTION_LOG)
            # Keep only last 10000 predictions to avoid huge file
            if len(existing) > 10000:
                existing = existing.tail(9000)
            df = pd.concat([existing, df], ignore_index=True)
        
        df.to_csv(PREDICTION_LOG, index=False)
    
    @staticmethod
    def log_batch_prediction(batch_size, avg_price, min_price, max_price):
        """Log batch prediction statistics"""
        log_entry = {
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'prediction_type': 'batch',
            'batch_size': batch_size,
            'avg_predicted_price': float(avg_price),
            'min_predicted_price': float(min_price),
            'max_predicted_price': float(max_price)
        }
        
        df = pd.DataFrame([log_entry])
        
        batch_log = LOGS_DIR / "batch_predictions.csv"
        if batch_log.exists():
            existing = pd.read_csv(batch_log)
            df = pd.concat([existing, df], ignore_index=True)
        
        df.to_csv(batch_log, index=False)
    
    @staticmethod
    def get_recent_predictions(limit=100):
        """Get recent predictions"""
        if not PREDICTION_LOG.exists():
            return pd.DataFrame()
        
        df = pd.read_csv(PREDICTION_LOG)
        return df.tail(limit)
    
    @staticmethod
    def get_prediction_stats():
        """Get prediction statistics"""
        if not PREDICTION_LOG.exists():
            return {}
        
        df = pd.read_csv(PREDICTION_LOG)
        
        stats = {
            'total_predictions': len(df),
            'avg_predicted_price': df['predicted_price'].mean(),
            'median_predicted_price': df['predicted_price'].median(),
            'min_predicted_price': df['predicted_price'].min(),
            'max_predicted_price': df['predicted_price'].max(),
            'most_common_city': df['city'].mode()[0] if len(df) > 0 else 'N/A',
            'most_common_country': df['country'].mode()[0] if len(df) > 0 else 'N/A',
            'predictions_by_type': df['prediction_type'].value_counts().to_dict()
        }
        
        return stats


class AnalyticsLogger:
    """Logger for analytics queries"""
    
    @staticmethod
    def log_analytics_query(filters, record_count, response_time):
        """Log analytics query for performance monitoring"""
        log_entry = {
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'filters': json.dumps(filters),
            'record_count': record_count,
            'response_time_ms': response_time,
        }
        
        df = pd.DataFrame([log_entry])
        
        if ANALYTICS_LOG.exists():
            existing = pd.read_csv(ANALYTICS_LOG)
            # Keep only last 1000 queries
            if len(existing) > 1000:
                existing = existing.tail(900)
            df = pd.concat([existing, df], ignore_index=True)
        
        df.to_csv(ANALYTICS_LOG, index=False)


def generate_summary_report():
    """Generate a summary report of all logs"""
    report = {
        'generated_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'model_training': {},
        'predictions': {},
        'analytics': {}
    }
    
    # Model Training Summary
    if MODEL_TRAINING_LOG.exists():
        df = pd.read_csv(MODEL_TRAINING_LOG)
        if len(df) > 0:
            report['model_training'] = {
                'total_trainings': len(df),
                'models_trained': df['model_name'].unique().tolist(),
                'best_model': {
                    'name': df.loc[df['r2'].idxmax(), 'model_name'],
                    'r2': float(df['r2'].max()),
                    'rmse': float(df.loc[df['r2'].idxmax(), 'rmse'])
                },
                'latest_training': df.iloc[-1]['timestamp']
            }
    
    # Predictions Summary
    if PREDICTION_LOG.exists():
        df = pd.read_csv(PREDICTION_LOG)
        if len(df) > 0:
            report['predictions'] = {
                'total_predictions': len(df),
                'avg_price': float(df['predicted_price'].mean()),
                'latest_prediction': df.iloc[-1]['timestamp'],
                'top_cities': df['city'].value_counts().head(5).to_dict()
            }
    
    # Analytics Summary
    if ANALYTICS_LOG.exists():
        df = pd.read_csv(ANALYTICS_LOG)
        if len(df) > 0:
            report['analytics'] = {
                'total_queries': len(df),
                'avg_response_time_ms': float(df['response_time_ms'].mean()),
                'latest_query': df.iloc[-1]['timestamp']
            }
    
    # Save report
    report_path = LOGS_DIR / f"summary_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(report_path, 'w', encoding='utf-8') as f:
        json.dump(report, f, indent=2, ensure_ascii=False)
    
    logger.info(f"Summary report generated: {report_path}")
    return report


if __name__ == "__main__":
    # Test logging
    print("Testing Logger Configuration...")
    
    # Test model logging
    ModelLogger.log_training(
        model_name="Test Model",
        metrics={'mae': 50000, 'rmse': 60000, 'r2': 0.85, 'training_time': 120},
        hyperparameters={'n_estimators': 100, 'max_depth': 10},
        notes="Test log entry"
    )
    
    # Test prediction logging
    PredictionLogger.log_prediction(
        input_data={'country': 'Singapore', 'city': 'Test', 'year': 2024, 'month': 1, 'area_m2': 100, 'property_type': '3 ROOM'},
        prediction=450000,
        prediction_type='single'
    )
    
    # Generate summary
    report = generate_summary_report()
    print("\n=== Summary Report ===")
    print(json.dumps(report, indent=2))
    
    print("\n✓ Logger configuration tested successfully!")
