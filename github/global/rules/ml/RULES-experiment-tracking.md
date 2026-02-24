# ML Experiment Tracking Rules (v18.0)
# Scope: All ML Training & Evaluation
# Tools: MLflow, DVC, Weights & Biases

## 1. Mandatory Tracking Metrics

### 1.1 Classification Models
*   **Metrics**: Accuracy, Precision, Recall, F1-Score (Macro & Weighted), AUC-ROC.
*   **Confusion Matrix**: Must be logged as an artifact (PNG/JSON).
*   **Thresholds**: Log metrics at 0.5, optimized F1 threshold, and 95% precision threshold.

### 1.2 Regression Models
*   **Metrics**: MSE, RMSE, MAE, R2 Score.
*   **Residual Plots**: Must be logged as artifacts.

### 1.3 Resource Metrics
*   **System**: CPU Usage (%), GPU Usage (%), Memory (GB), Training Time (s).
*   **Carbon Footprint**: Estimated CO2 emissions (using CodeCarbon).

## 2. MLflow Standards

### 2.1 Naming Convention
*   **Experiment Name**: `{project_name}/{model_type}/{version}` (e.g., `plant-disease/resnet50/v1`).
*   **Run Name**: `{timestamp}-{git_commit_short}-{strategy}` (e.g., `20260216-a1b2c3d-transfer_learning`).

### 2.2 Tags
*   **Required Tags**:
    *   `git_commit`: Full SHA.
    *   `triggered_by`: User or CI/CD pipeline ID.
    *   `dataset_version`: DVC hash.
    *   `model_class`: Python class name (e.g., `ResNet50`).

### 2.3 Artifacts
*   **Model**: Logged in `models/` directory.
*   **Config**: `config.yaml` used for training.
*   **Requirements**: `requirements.txt` or `conda.yaml`.
*   **Plots**: Loss curves, PR curves, SHAP summary plots.

## 3. DVC Integration

### 3.1 Data Versioning
*   **Rule**: NEVER train on uncommitted data.
*   **Command**: `dvc repro` must be used to trigger training pipelines.
*   **Storage**: Remote S3 bucket (`s3://gaara-ml-data/`).

### 3.2 Pipeline Stages
*   **dvc.yaml**: Must define `prepare`, `train`, `evaluate` stages.
*   **Dependencies**: Explicitly list all input data and code files.
*   **Outputs**: Explicitly list all metrics and model files.

## 4. Code Example (MLflow + PyTorch)

```python
import mlflow
import mlflow.pytorch
from codecarbon import EmissionsTracker

def train(model, loader, optimizer, epoch):
    tracker = EmissionsTracker()
    tracker.start()
    
    mlflow.set_experiment("plant-disease/resnet50/v1")
    
    with mlflow.start_run(run_name="20260216-auto-v1"):
        # Log Params
        mlflow.log_param("learning_rate", 0.001)
        mlflow.log_param("batch_size", 32)
        
        # Training Loop...
        # ...
        
        # Log Metrics
        mlflow.log_metric("train_loss", 0.15, step=epoch)
        mlflow.log_metric("val_accuracy", 0.92, step=epoch)
        
        # Log Artifacts
        mlflow.pytorch.log_model(model, "model")
        
        emissions = tracker.stop()
        mlflow.log_metric("co2_emissions_kg", emissions)
```
