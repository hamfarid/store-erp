# ML Training Workflow (v18.0)
# Scope: Model Development & Experimentation
# Tools: PyTorch, TensorFlow, MLflow, Ray

## 1. Workflow Stages

### 1.1 Data Preparation (Phase 1)
*   **Goal**: Load and preprocess data.
*   **Tool**: DVC / Pandas / Ray Data.
*   **Steps**:
    1.  Load raw data (S3).
    2.  Clean and validate (Pandera).
    3.  Split (Train/Val/Test) - Stratified.
    4.  Augment (Albumentations).

### 1.2 Model Architecture (Phase 2)
*   **Goal**: Define model structure.
*   **Tool**: PyTorch Lightning / Keras.
*   **Strategy**: Transfer Learning (ResNet50/EfficientNet).
*   **Config**: Hydra / YAML.

### 1.3 Training Loop (Phase 3)
*   **Goal**: Optimize model weights.
*   **Tool**: PyTorch Lightning Trainer.
*   **Features**:
    *   Early Stopping (Patience=5).
    *   Model Checkpointing (Top-3 Val Loss).
    *   Gradient Clipping (Norm=1.0).
    *   Mixed Precision (FP16).

### 1.4 Evaluation (Phase 4)
*   **Goal**: Assess model performance.
*   **Tool**: Scikit-learn / TorchMetrics.
*   **Metrics**: Accuracy, F1, AUC, Confusion Matrix.
*   **Report**: MLflow Artifacts.

## 2. Infrastructure (Ray/Kubeflow)

### 2.1 Distributed Training
*   **Strategy**: DDP (Distributed Data Parallel).
*   **Resources**: Multi-GPU (A100 x 4).
*   **Tool**: Ray Train / PyTorch DDP.

### 2.2 Hyperparameter Tuning
*   **Tool**: Ray Tune / Optuna.
*   **Algorithm**: Bayesian Optimization (TPE).
*   **Trials**: 50-100.

## 3. Reproducibility Checklist

### 3.1 Seeding
*   **Rule**: Set global seed (42).
*   **Scope**: Python, Numpy, PyTorch, CUDA.

### 3.2 Environment
*   **Rule**: Docker container with pinned versions.
*   **File**: `requirements.txt` (pip-compile).

### 3.3 Data
*   **Rule**: DVC hash committed to Git.

## 4. Code Example (PyTorch Lightning)

```python
import pytorch_lightning as pl
from pytorch_lightning.callbacks import ModelCheckpoint, EarlyStopping

class PlantDiseaseModel(pl.LightningModule):
    def __init__(self, lr=1e-3):
        super().__init__()
        self.save_hyperparameters()
        self.model = models.resnet50(pretrained=True)
        self.model.fc = nn.Linear(2048, NUM_CLASSES)

    def training_step(self, batch, batch_idx):
        x, y = batch
        y_hat = self.model(x)
        loss = F.cross_entropy(y_hat, y)
        self.log("train_loss", loss)
        return loss

    def configure_optimizers(self):
        return torch.optim.Adam(self.parameters(), lr=self.hparams.lr)

trainer = pl.Trainer(
    max_epochs=50,
    gpus=1,
    precision=16,
    callbacks=[
        EarlyStopping(monitor="val_loss", patience=5),
        ModelCheckpoint(monitor="val_loss", save_top_k=3)
    ]
)
```
