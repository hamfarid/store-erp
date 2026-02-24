# Computer Vision Standards (v17.0)
# Scope: Image Processing & Deep Learning
# Compliance: EU AI Act (High-Risk AI)

## 1. Data Augmentation Limits

### 1.1 Geometric Transformations
*   **Rotation**: +/- 30 degrees (unless orientation invariant).
*   **Flip**: Horizontal allowed (p=0.5). Vertical forbidden for upright objects (e.g., pedestrians).
*   **Shear**: Max 10 degrees.
*   **Zoom**: 0.8x to 1.2x.

### 1.2 Color Transformations
*   **Brightness**: +/- 20%.
*   **Contrast**: +/- 20%.
*   **Saturation**: +/- 20%.
*   **Hue**: +/- 5% (Strict limit to preserve semantic color).

### 1.3 Advanced Techniques
*   **MixUp**: Alpha = 0.2.
*   **CutMix**: Probability = 0.5.
*   **Mosaic**: Required for Object Detection (YOLO).

## 2. Model Architecture

### 2.1 Backbones
*   **ResNet50**: Default baseline.
*   **EfficientNet-B0**: Mobile/Edge deployment.
*   **ViT-B/16**: High-accuracy server deployment (Requires > 10M images).
*   **YOLOv8**: Real-time Object Detection.

### 2.2 Input Resolution
*   **Standard**: 224x224 (ImageNet).
*   **High-Res**: 512x512 (Medical/Satellite).
*   **Constraint**: Must be divisible by 32 (Stride).

## 3. Evaluation Metrics

### 3.1 Classification
*   **Accuracy**: Top-1 and Top-5.
*   **F1-Score**: Macro-averaged (for class imbalance).
*   **Confusion Matrix**: Must be logged to MLflow.

### 3.2 Object Detection
*   **mAP@50**: Mean Average Precision at IoU=0.5.
*   **mAP@50-95**: COCO Standard.
*   **IoU**: Intersection over Union.

### 3.3 Segmentation
*   **Dice Coefficient**: Primary metric.
*   **IoU (Jaccard)**: Secondary metric.

## 4. Quality Gates (Production)

| Metric | Threshold | Action |
| :--- | :--- | :--- |
| **Mislabel Rate** | < 1% | Manual Audit of Test Set |
| **Cohen's Kappa** | > 0.8 | Inter-Annotator Agreement |
| **Inference Time** | < 100ms | Latency Check (P99) |
| **Model Size** | < 500MB | Mobile Deployment Constraint |

## 5. Code Example (PyTorch Lightning)

```python
import pytorch_lightning as pl
import torch
from torchmetrics import Accuracy, F1Score

class LitModel(pl.LightningModule):
    def __init__(self, num_classes):
        super().__init__()
        self.model = models.resnet50()
        self.accuracy = Accuracy(task="multiclass", num_classes=num_classes)
        self.f1 = F1Score(task="multiclass", num_classes=num_classes)

    def training_step(self, batch, batch_idx):
        x, y = batch
        logits = self.model(x)
        loss = F.cross_entropy(logits, y)
        self.log("train_loss", loss)
        return loss

    def validation_step(self, batch, batch_idx):
        x, y = batch
        logits = self.model(x)
        preds = torch.argmax(logits, dim=1)
        self.log("val_acc", self.accuracy(preds, y))
        self.log("val_f1", self.f1(preds, y))
```
