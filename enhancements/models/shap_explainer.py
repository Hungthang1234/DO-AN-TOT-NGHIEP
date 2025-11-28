"""
SHAP Explainability - Giải thích dự đoán của model
Shows which features contribute most to the prediction
"""

import pandas as pd
import numpy as np
import joblib
import shap
import matplotlib.pyplot as plt
from pathlib import Path
import warnings
warnings.filterwarnings('ignore')


class SHAPExplainer:
    """SHAP explainability for model predictions"""
    
    def __init__(self, model_path):
        """Load model"""
        print(f"📂 Loading model from: {model_path}")
        self.model_data = joblib.load(model_path)
        
        # Extract model based on structure
        if isinstance(self.model_data, dict):
            if 'model' in self.model_data:
                self.model = self.model_data['model']
            elif 'base_models' in self.model_data:
                # Ensemble model - use first base model for SHAP
                self.model = self.model_data['base_models'][0][1]
            else:
                raise ValueError("Unknown model structure")
            
            self.feature_names = self.model_data.get('feature_names', [])
        else:
            self.model = self.model_data
            self.feature_names = []
        
        self.explainer = None
        self.shap_values = None
    
    def create_explainer(self, X_background, max_samples=100):
        """
        Create SHAP explainer with background data
        
        Args:
            X_background: Training data sample for background distribution
            max_samples: Max samples to use (for speed)
        """
        print(f"🔧 Creating SHAP explainer...")
        
        # Use subset for speed
        if len(X_background) > max_samples:
            X_background = X_background.sample(n=max_samples, random_state=42)
        
        try:
            # Try TreeExplainer first (faster for tree models)
            self.explainer = shap.TreeExplainer(self.model)
            print("   ✅ Using TreeExplainer (optimized for tree models)")
        except:
            # Fallback to KernelExplainer
            self.explainer = shap.KernelExplainer(
                self.model.predict, 
                X_background
            )
            print("   ✅ Using KernelExplainer (universal)")
    
    def explain_prediction(self, X_input, feature_names=None):
        """
        Explain a single prediction
        
        Args:
            X_input: Single row DataFrame or dict
            feature_names: List of feature names
            
        Returns:
            dict with explanation
        """
        if self.explainer is None:
            raise ValueError("Call create_explainer() first")
        
        # Convert to DataFrame if needed
        if isinstance(X_input, dict):
            X_input = pd.DataFrame([X_input])
        
        # Get SHAP values
        shap_values = self.explainer.shap_values(X_input)
        
        # Get prediction
        prediction = self.model.predict(X_input)[0]
        
        # Create explanation dict
        if feature_names is None:
            feature_names = self.feature_names if self.feature_names else X_input.columns
        
        explanation = {
            'prediction': float(prediction),
            'base_value': float(self.explainer.expected_value) if hasattr(self.explainer, 'expected_value') else None,
            'features': []
        }
        
        # Add feature contributions
        for i, feature in enumerate(feature_names):
            contribution = float(shap_values[0][i]) if isinstance(shap_values, np.ndarray) else float(shap_values[i])
            
            explanation['features'].append({
                'name': feature,
                'value': float(X_input.iloc[0][i]),
                'contribution': contribution,
                'abs_contribution': abs(contribution)
            })
        
        # Sort by absolute contribution
        explanation['features'] = sorted(
            explanation['features'], 
            key=lambda x: x['abs_contribution'], 
            reverse=True
        )
        
        return explanation
    
    def plot_waterfall(self, X_input, save_path=None):
        """
        Create waterfall plot showing feature contributions
        
        Args:
            X_input: Single row to explain
            save_path: Path to save plot image
        """
        if self.explainer is None:
            raise ValueError("Call create_explainer() first")
        
        # Get SHAP values
        shap_values = self.explainer.shap_values(X_input)
        
        # Create waterfall plot
        plt.figure(figsize=(10, 6))
        shap.waterfall_plot(
            shap.Explanation(
                values=shap_values[0],
                base_values=self.explainer.expected_value,
                data=X_input.iloc[0],
                feature_names=X_input.columns
            )
        )
        
        if save_path:
            plt.savefig(save_path, bbox_inches='tight', dpi=150)
            print(f"✅ Waterfall plot saved to: {save_path}")
        else:
            plt.show()
        
        plt.close()
    
    def plot_force(self, X_input, save_path=None):
        """
        Create force plot showing feature contributions
        
        Args:
            X_input: Single row to explain
            save_path: Path to save plot HTML
        """
        if self.explainer is None:
            raise ValueError("Call create_explainer() first")
        
        # Get SHAP values
        shap_values = self.explainer.shap_values(X_input)
        
        # Create force plot
        force_plot = shap.force_plot(
            self.explainer.expected_value,
            shap_values[0],
            X_input.iloc[0],
            feature_names=X_input.columns
        )
        
        if save_path:
            shap.save_html(save_path, force_plot)
            print(f"✅ Force plot saved to: {save_path}")
        else:
            return force_plot
    
    def get_feature_importance(self, X_sample):
        """
        Get overall feature importance from SHAP values
        
        Args:
            X_sample: Sample data to calculate importance
            
        Returns:
            DataFrame with feature importance
        """
        if self.explainer is None:
            raise ValueError("Call create_explainer() first")
        
        # Calculate SHAP values for sample
        shap_values = self.explainer.shap_values(X_sample)
        
        # Calculate mean absolute SHAP value per feature
        importance = np.abs(shap_values).mean(axis=0)
        
        # Create DataFrame
        importance_df = pd.DataFrame({
            'feature': X_sample.columns,
            'importance': importance
        }).sort_values('importance', ascending=False)
        
        return importance_df


def explain_single_prediction(model_path, X_input, X_background=None):
    """
    Explain a single prediction with SHAP
    
    Args:
        model_path: Path to model file
        X_input: Single prediction input (dict or DataFrame)
        X_background: Background data for explainer
        
    Returns:
        Explanation dict
    """
    explainer = SHAPExplainer(model_path)
    
    if X_background is not None:
        explainer.create_explainer(X_background)
    else:
        # Use X_input as background (not ideal but works)
        if isinstance(X_input, dict):
            X_bg = pd.DataFrame([X_input])
        else:
            X_bg = X_input
        explainer.create_explainer(X_bg)
    
    explanation = explainer.explain_prediction(X_input)
    
    return explanation


if __name__ == '__main__':
    # Example usage
    model_path = Path(__file__).parent.parent.parent / 'models' / 'lightgbm_full_dataset.joblib'
    
    if not model_path.exists():
        print(f"❌ Model file not found: {model_path}")
        exit(1)
    
    # Example input
    sample_input = {
        'country': 'Vietnam',
        'city': 'Ho Chi Minh City',
        'area_m2': 100,
        'property_type': 'Apartment',
        'year': 2024,
        'month': 11
    }
    
    print("🔍 Explaining prediction...")
    explanation = explain_single_prediction(model_path, sample_input)
    
    print("\n" + "=" * 80)
    print("📊 SHAP EXPLANATION")
    print("=" * 80)
    print(f"Predicted Price: ${explanation['prediction']:,.2f}")
    print(f"\nTop 5 Contributing Features:")
    print("-" * 80)
    
    for i, feat in enumerate(explanation['features'][:5], 1):
        impact = "↑" if feat['contribution'] > 0 else "↓"
        print(f"{i}. {feat['name']}: {feat['value']} {impact} ${abs(feat['contribution']):,.2f}")
    
    print("=" * 80)
