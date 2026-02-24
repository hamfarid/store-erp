# ML Model Versioning Rules (v18.0)
# Scope: Model Registry & Lifecycle Management
# Tools: MLflow Model Registry, DVC

## 1. Semantic Versioning for Models

### 1.1 Format: MAJOR.MINOR.PATCH
*   **MAJOR**: Breaking change (e.g., new architecture, incompatible input/output schema).
*   **MINOR**: Significant improvement (e.g., +2% accuracy, new features, backward compatible).
*   **PATCH**: Bug fix or minor retraining (e.g., retraining on new data with same code).

### 1.2 Examples
*   `v1.0.0`: Initial ResNet50 release.
*   `v1.1.0`: Added "Rust" class to detection.
*   `v1.1.1`: Retrained on Q1 2026 data.
*   `v2.0.0`: Switched to EfficientNet-B4 (API change).

## 2. Model Registry Stages

### 2.1 None (Development)
*   **Description**: Initial training runs.
*   **Access**: Data Scientists only.
*   **Retention**: 30 days.

### 2.2 Staging (Pre-Production)
*   **Description**: Candidate models that passed unit tests.
*   **Gate**: Must pass `test_model_schema.py` and `test_inference_latency.py`.
*   **Access**: CI/CD Pipeline, QA Team.
*   **Retention**: Until promoted or rejected.

### 2.3 Production (Live)
*   **Description**: Currently serving traffic.
*   **Gate**: Must pass Canary Deployment (1% traffic) and A/B Test.
*   **Access**: Read-only for Serving API.
*   **Retention**: Indefinite (Archived after replacement).

### 2.4 Archived (Retired)
*   **Description**: Previous production models.
*   **Reason**: Fallback/Rollback capability.
*   **Retention**: 1 year minimum (Regulatory compliance).

## 3. Metadata Requirements

### 3.1 Mandatory Attributes
*   **author**: Email of data scientist.
*   **framework**: PyTorch/TensorFlow version.
*   **dataset_hash**: DVC commit hash.
*   **metrics**: JSON string of final evaluation metrics.
*   **schema_signature**: Input/Output tensor shapes and types.

### 3.2 Description Field
*   Must include a link to the Experiment Run and the Jira Ticket/Issue ID.

## 4. Automation Rules

### 4.1 Auto-Promotion
*   **Rule**: If Staging model beats Production model on *Golden Test Set* by > 1% F1-Score AND Latency < 110% of Production -> Auto-Promote to Canary.

### 4.2 Auto-Rollback
*   **Rule**: If Production model error rate > 5% (5xx responses) OR Latency > 500ms (p99) for 5 mins -> Auto-Rollback to Previous Version.

## 5. Code Example (MLflow Registry)

```python
import mlflow
from mlflow.tracking import MlflowClient

client = MlflowClient()

def promote_to_staging(run_id, model_name):
    # 1. Register Model
    model_uri = f"runs:/{run_id}/model"
    mv = mlflow.register_model(model_uri, model_name)
    
    # 2. Transition to Staging
    client.transition_model_version_stage(
        name=model_name,
        version=mv.version,
        stage="Staging",
        archive_existing_versions=False
    )
    
    # 3. Update Description
    client.update_model_version(
        name=model_name,
        version=mv.version,
        description="Promoted by CI/CD Pipeline #1234"
    )
    print(f"Model {model_name} v{mv.version} promoted to Staging.")
```
