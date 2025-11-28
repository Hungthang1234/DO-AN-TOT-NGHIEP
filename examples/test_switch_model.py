# Example: Switch between models
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from scripts.model_manager import ModelManager

manager = ModelManager()

# List available models
print("=" * 60)
print("AVAILABLE MODELS")
print("=" * 60)
models = manager.list_available_models()

for i, model in enumerate(models, 1):
    active = " [ACTIVE]" if model['name'] == manager.models_config.get('active_model') else ""
    print(f"{i}. {model['name']:30} - R²: {model['r2']:.4f}, RMSE: ${model['rmse']:,.0f}{active}")

# Switch model
print("\n" + "=" * 60)
print("SWITCH MODEL")
print("=" * 60)

# Example: Activate specific model
model_name = 'best_clean'  # Change this to your model name
success = manager.set_active_model(model_name)

if success:
    print(f"✅ Activated model: {model_name}")
    print("⚠️  Please restart Flask app for changes to take effect")
else:
    print(f"❌ Failed to activate model: {model_name}")
