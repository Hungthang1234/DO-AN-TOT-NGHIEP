# House Price Prediction — Training Pipeline

This repository contains a training pipeline and interactive notebooks to train regression models for house price prediction using the included cleaned real estate CSV.

Files of interest:
- `train_pipeline.py`: Command-line training script that builds preprocessing pipelines, trains several models, evaluates them, and saves pipelines to `models/`.
- `predict.py`: CLI script to load a saved model pipeline and produce predictions on a CSV file.
- `TrainModel.ipynb`: Windows-friendly interactive notebook with EDA, preprocessing, training, evaluation, and inference examples.
- `TrainPipeline_from_py.ipynb`: Notebook converted from the `train_pipeline.py` and `predict.py` scripts for interactive experimentation.
- `requirements.txt`: Python package list for dependencies.

## Quick start (Windows PowerShell)

1. Create and activate a Python virtual environment:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

2. Install dependencies:

```powershell
pip install -r requirements.txt
```

3. Run the interactive notebook (open in VS Code or Jupyter):

```powershell
code .\TrainModel.ipynb
# or
jupyter notebook TrainModel.ipynb
```

4. Run the CLI training script (example):

```powershell
python .\train_pipeline.py --data "Data\cleaned_real_estate.csv" --target price --out-dir models
```

Quick preview (small subset):

```powershell
python .\train_pipeline.py --data "Data\cleaned_real_estate.csv" --preview --nrows 1000
```

5. Run prediction with a saved model (example):

```powershell
python .\predict.py --model models\RandomForest.joblib --input "Data\sample_features.csv" --output predictions.csv
```

## Notes
- The scripts and notebooks expect `Data\cleaned_real_estate.csv` to be present in the repository. Change paths in the notebook if your data is located elsewhere.
- The pipeline automatically separates numeric and categorical features and applies sensible defaults (imputation, scaling, one-hot encoding).
- If `xgboost` or `lightgbm` are not installed, those models will be skipped; they are optional dependencies listed in `requirements.txt`.
- For large datasets, run training locally (the tooling here cannot read files >50MB). Use sampling flags (`--sample-frac` or `--nrows`) for quick runs.

## Next steps I can help with
- Add hyperparameter tuning (GridSearchCV / RandomizedSearchCV) and automated model selection.
- Add SHAP explanations for feature importance and local explanations.
- Add a PowerShell wrapper to run the training script headlessly and capture logs.
# House Price Prediction — Training Pipeline

This repository contains a simple training pipeline to train multiple regression models for house price prediction using a cleaned real estate CSV.

Files added:
- `train_pipeline.py`: training script that preprocesses data, trains several models and saves them to `models/`.
- `predict.py`: simple inference script to load a saved model and run predictions on a CSV file.
- `requirements.txt`: package list for the main dependencies.

Quick start (Windows PowerShell):

1. Create and activate a Python environment (optional but recommended):

```powershell
python -m venv .venv; .\.venv\Scripts\Activate.ps1
```

2. Install requirements:

```powershell
pip install -r requirements.txt
```

3. Train models (adjust target column name if different):

```powershell
python train_pipeline.py --data "Data/cleaned_real_estate.csv" --target price --out-dir models
```

If your dataset is very large and you want a quick preview run:

```powershell
python train_pipeline.py --data "Data/cleaned_real_estate.csv" --preview --nrows 1000
```

4. Run prediction with a saved model:

```powershell
python predict.py --model models\RandomForest.joblib --input "Data/sample_features.csv" --output predictions.csv
```

Notes:
- The pipeline automatically infers numeric and categorical columns.
- If `xgboost` or `lightgbm` are not installed they will be skipped.
- Adjust `--drop-missing-frac` to drop columns with many missing values before training.
