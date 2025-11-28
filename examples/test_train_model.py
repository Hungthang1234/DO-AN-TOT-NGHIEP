# Example: Train model with external data
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from scripts.model_manager import ModelManager
from scripts.fetch_external_data import RealEstateAPIClient

# Step 1: Fetch data
print("=" * 60)
print("STEP 1: Fetch Data from Singapore HDB API")
print("=" * 60)
client = RealEstateAPIClient()
df = client.fetch_singapore_hdb_data(year=2024, month=6)
print(f"✅ Fetched {len(df)} records")

# Save data
data_file = 'Data/singapore_june_2024.csv'
df.to_csv(data_file, index=False)
print(f"✅ Saved to {data_file}")

# Step 2: Train model
print("\n" + "=" * 60)
print("STEP 2: Train New Model")
print("=" * 60)
manager = ModelManager()
model_data = manager.train_new_model(
    data_file=data_file,
    model_name='singapore_june_model',
    model_type='lightgbm'
)

# Step 3: List all models
print("\n" + "=" * 60)
print("STEP 3: Available Models")
print("=" * 60)
models = manager.list_available_models()
for i, model in enumerate(models, 1):
    print(f"{i}. {model['name']:30} - R²: {model['r2']:.4f}, RMSE: ${model['rmse']:,.0f}")

# Step 4: Compare models
print("\n" + "=" * 60)
print("STEP 4: Model Comparison")
print("=" * 60)
comparison = manager.compare_models()
print(comparison.to_string(index=False))

# Step 5: Activate new model (optional)
print("\n" + "=" * 60)
print("STEP 5: Activate Model")
print("=" * 60)
# Uncomment to activate:
# manager.set_active_model('singapore_june_model')
print("To activate: manager.set_active_model('singapore_june_model')")
