# Multi-Crop Augmentation Rules (v26.0)

> **Scope**: Computer Vision Training & Inference
> **Compliance**: Multi-View Plant Disease Detection
> **Status**: Production-Ready
> **Version**: v26.0.2 (Diamond 32)

## 1. Crop Strategy (Training)

### 1.1 Random Resized Crop (Standard Training)
*   **Scale**: `(0.08, 1.0)` — Covers 8% to 100% of image area.
*   **Ratio**: `(3/4, 4/3)` — Aspect ratio variation.
*   **Output Size**: `224×224` (ImageNet standard) or `384×384` (high-resolution mode).
*   **Why**: Forces model to learn both local features (lesion spots) and global structure (leaf shape).
*   **Constraint**: **Never crop below 8%** — too small a crop loses all disease context.

### 1.2 Five-Crop (Deterministic Validation)
*   **Method**: Top-Left, Top-Right, Bottom-Left, Bottom-Right, Center.
*   **Size**: `224×224` from `256×256` resized input.
*   **Why**: Deterministic evaluation ensures reproducible metrics across runs.

### 1.3 Ten-Crop (Production Evaluation)
*   **Method**: Five-Crop + Horizontal Flip of each = 10 views.
*   **Aggregation**: Mean of Softmax Probabilities across all 10 views.
*   **Benefit**: +1-2% accuracy over single center crop.

## 2. Color Augmentation Limits (Disease-Safe)

### 2.1 Hard Limits
Plant diseases are diagnosed by color. Excessive color augmentation destroys diagnostic signals.

| Parameter | Maximum | Reason |
| :--- | :--- | :--- |
| **Hue Jitter** | ±0.1 (10%) | Yellow vs brown vs green are disease indicators |
| **Saturation** | ±0.4 (40%) | Simulates sunny vs cloudy lighting |
| **Brightness** | ±0.4 (40%) | Simulates direct vs diffuse light |
| **Contrast** | ±0.4 (40%) | Handles camera variation |

### 2.2 Disease-Specific Augmentation Restrictions

| Disease | Hue Limit | Special Notes |
| :--- | :--- | :--- |
| **Early Blight** | ±0.05 | Brown ring patterns are hue-critical |
| **Chlorosis** | ±0.05 | Yellow-green transition is diagnostic |
| **Rust** | ±0.08 | Orange pustule color is distinctive |
| **Powdery Mildew** | ±0.1 (standard) | White color is brightness-dependent, not hue |
| **Healthy** | ±0.1 (standard) | Green range is broad enough |

## 3. Geometric Augmentation

### 3.1 Allowed Transformations
*   **Rotation**: ±180 degrees (p=0.5). Leaves can be in any orientation.
*   **Horizontal Flip**: p=0.5. Always allowed for plant images.
*   **Vertical Flip**: p=0.5. Always allowed for plant images.
*   **Affine**: scale=(0.9, 1.1), translate=(-0.1, 0.1), shear=(-5°, 5°).

### 3.2 Restricted Transformations
*   **Elastic Transform**: Use sparingly (p=0.1, α<50, σ<5). Can distort lesion shape.
*   **GridDistortion**: **Avoid** for plant disease — changes lesion geometry unnaturally.
*   **Perspective**: Light use only (p=0.2, scale<0.05). Simulates slight camera angle.

### 3.3 Spatial Resolution Rules
*   **Minimum output size**: `224×224`. Never downsample below this.
*   **Interpolation**: `INTER_LINEAR` for downscale, `INTER_CUBIC` for upscale.
*   **Anti-aliasing**: Always enable when downsampling > 2×.

## 4. Crop Strategy Decision Matrix

| Scenario | Strategy | Min Crops | Time Budget | Accuracy Gain |
| :--- | :--- | :--- | :--- | :--- |
| **Lab (Single Leaf)** | TTA (Flip + Rotation) | 2 | 40ms | +0.5% |
| **Field (Single Leaf)** | 10-crop + TTA | 10 | 200ms | +1.5% |
| **Sliding Window** | ≥50% overlap | Variable | 500ms+ | +2.0% |
| **Real-time Mobile** | Center Crop only | 1 | 20ms | Baseline |
| **Production Eval** | 10-crop + Multi-scale | 10-18 | 300ms | +2.5% |
| **Research/Benchmark** | 10-crop + TTA + 3 scales | 30-54 | 1000ms+ | +3.0% |

## 5. Test-Time Augmentation (TTA) Pipeline

### 5.1 Standard TTA (Production)
1.  Input Image (1)
2.  Resize to `256×256`
3.  5 Crops (TL, TR, BL, BR, Center) × `224×224`
4.  Horizontal Flip of each (×2)
5.  **10 views total**
6.  Model inference on each
7.  Mean of Softmax Probabilities
8.  Final Prediction

### 5.2 Multi-Scale TTA (High-Accuracy)
1.  Input Image (1)
2.  Resize to `[224, 256, 384]` (3 scales)
3.  Per scale: 5 Crops + Flips = 10 views
4.  **30 views total**
5.  Model inference on each
6.  Weighted Mean: `scale_224 × 0.2` + `scale_256 × 0.3` + `scale_384 × 0.5`
7.  Final Prediction

### 5.3 TTA Aggregation Rules
*   **Default**: Arithmetic mean of softmax probabilities.
*   **Alternative**: Geometric mean (slightly better for calibrated models).
*   **Confidence threshold**: If max probability < 0.6 after TTA, flag for human review.
*   **Disagreement threshold**: If top-2 crops disagree on class, flag for investigation.

## 6. Sliding Window (Whole Plant / Canopy)

### 6.1 Parameters
*   **Window Size**: `224×224` (match model input).
*   **Stride**: `112×112` (50% overlap minimum).
*   **Overlap**: ≥50% required to avoid missing lesions at boundaries.
*   **Aggregation**: Max activation per spatial location across overlapping windows.

### 6.2 Boundary Handling
*   **Pad image** with reflection padding (not zero padding).
*   **Discard predictions** from windows where > 50% is padding.

## 7. Processing Budget

| Stage | GPU Time | CPU Time | Memory |
| :--- | :--- | :--- | :--- |
| **Single crop inference** | 5ms | 50ms | 50MB |
| **10-crop TTA** | 20ms | 200ms | 200MB |
| **30-crop Multi-scale TTA** | 60ms | 600ms | 500MB |
| **Sliding window (1000×1000)** | 100ms | 1000ms | 300MB |

## 8. Code Example (Albumentations + TTA)

```python
import albumentations as A
from albumentations.pytorch import ToTensorV2
import torch
import numpy as np
import cv2

# Training Transform (with disease-safe limits)
train_transform = A.Compose([
    A.RandomResizedCrop(height=224, width=224, scale=(0.08, 1.0)),
    A.HorizontalFlip(p=0.5),
    A.VerticalFlip(p=0.5),
    A.Rotate(limit=180, p=0.5),
    A.ColorJitter(brightness=0.4, contrast=0.4, saturation=0.4, hue=0.1, p=0.5),
    A.Normalize(mean=(0.485, 0.456, 0.406), std=(0.229, 0.224, 0.225)),
    ToTensorV2(),
])

# Validation Transform (deterministic)
val_transform = A.Compose([
    A.Resize(256, 256),
    A.CenterCrop(224, 224),
    A.Normalize(mean=(0.485, 0.456, 0.406), std=(0.229, 0.224, 0.225)),
    ToTensorV2(),
])

def tta_predict(model, image, n_crops=10):
    """10-crop TTA: 5 crops × 2 (with horizontal flip)."""
    img = cv2.resize(image, (256, 256))
    crops = [
        img[0:224, 0:224],       # Top-Left
        img[0:224, 32:256],      # Top-Right
        img[32:256, 0:224],      # Bottom-Left
        img[32:256, 32:256],     # Bottom-Right
        img[16:240, 16:240],     # Center
    ]
    
    # Add horizontal flips
    crops += [cv2.flip(c, 1) for c in crops]
    
    # Inference on all crops
    predictions = []
    for crop in crops:
        # Note: In real code, batch these!
        tensor = val_transform(image=crop)["image"].unsqueeze(0)
        with torch.no_grad():
            pred = torch.softmax(model(tensor), dim=1)
        predictions.append(pred)
        
    # Aggregate: mean of softmax
    mean_pred = torch.stack(predictions).mean(dim=0)
    return mean_pred
```

## 9. Cross-References
*   **Master Rules**: `rules/ml/RULES-plant-disease-analysis.md` → Section 2
*   **Binarization (binary view generation)**: `rules/ml/RULES-image-binarization.md` → Section 5
*   **Error Catalog**: `errors/ml/ERROR-multi-view-pipeline-catalog.md` → ERR-CROP-001
*   **Workflow**: `workflows/ml/ML_MULTI_VIEW_WORKFLOW.md` → Step 2 (Multi-Crop)
