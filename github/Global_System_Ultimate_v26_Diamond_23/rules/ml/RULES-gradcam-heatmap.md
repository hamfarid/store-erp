# Grad-CAM Heatmap Rules (v26.0)

> **Scope**: Model Explainability (XAI)
> **Compliance**: Multi-View Plant Disease Detection
> **Status**: Production-Ready
> **Version**: v26.0.0 (Diamond 5)

## 1. Target Layer Selection

### 1.1 Architecture-Specific Targets

| Architecture | Target Layer | Method | Output Dims |
| :--- | :--- | :--- | :--- |
| **ResNet50** | `layer4[-1]` | Standard GradCAM | 7×7 |
| **ResNet101/152** | `layer4[-1]` | Standard GradCAM | 7×7 |
| **EfficientNet-B0** | `_conv_head` | Standard GradCAM | 7×7 |
| **EfficientNet-B4** | Last MBConvBlock | Standard GradCAM | 7×7 |
| **DINOv2 ViT-B/14** | Last transformer block | Attention Rollout | 16×16 |
| **ViT-B/16** | Last Self-Attention | Attention Rollout | 14×14 |
| **ConvNeXt** | `stages[-1]` | Standard GradCAM | 7×7 |

### 1.2 Selection Rules
*   **CNNs**: Always use the **LAST convolutional layer** before global pooling.
*   **ViTs/DINOv2**: Use **Attention Rollout** on CLS token, NOT standard GradCAM.
*   **Hybrid models**: Use GradCAM on the convolutional stem if spatial resolution > 7×7.
*   **Constraint**: **NEVER** target intermediate layers unless debugging specific feature activation issues.

## 2. Validation Strategy

### 2.1 ROAD (Remove And Debias) — Primary Metric
*   **Process**: Mask top 20% activated pixels → Re-classify with debiased input.
*   **Success Criteria**: Classification confidence drops > 50%.
*   **Failure Indication**: Confidence remains high → model relies on background features.
*   **Minimum ROAD Score**: **≥ 0.3** for production deployment.
*   **Calculation**: `ROAD = 1 - (confidence_after_removal / confidence_before_removal)`

### 2.2 Pointing Game — Secondary Metric
*   **Metric**: Hit Rate across validation set.
*   **Process**: Check if maximum activation point falls inside ground-truth bounding box.
*   **Minimum Hit Rate**: **70%** across validation set.
*   **Per-class minimum**: 60% for any individual disease class.

### 2.3 Overlap Validation (Plant Disease Specific)
*   **Metric**: GradCAM-Leaf Overlap Ratio (GLOR).
*   **Formula**: `GLOR = Sum(Heatmap × Leaf_Mask) / Sum(Heatmap)`
*   **Minimum**: **≥ 70%** of top activations must overlap with leaf region.
*   **Action if < 70%**: Flag model for background bias → retrain with CutMix augmentation.
*   **Monitoring**: Track GLOR weekly per disease class. Alert if 30-day trend is declining.

## 3. Background Activation Limits

### 3.1 Background Activation Ratio (BAR)
*   **Formula**: `BAR = Sum(Heatmap × (1 - Leaf_Mask)) / Sum(Heatmap)`
*   **Hard Limit**: **BAR < 0.30 (30%)**.
*   **Warning Threshold**: BAR > 0.20 triggers investigation.
*   **Action if BAR > 0.30**: Block deployment → retrain with:
    *   CutMix augmentation (mix leaves with diverse backgrounds).
    *   Background randomization (paste leaves on varied backgrounds).
    *   Foreground-focused loss weighting.

### 3.2 Per-Disease BAR Targets

| Disease | Expected BAR | Notes |
| :--- | :--- | :--- |
| **Early Blight** | < 0.15 | Distinct concentric rings, easy to localize |
| **Late Blight** | < 0.25 | Large irregular lesions, some edge spill |
| **Powdery Mildew** | < 0.20 | Surface-level, well-defined |
| **Rust** | < 0.15 | Small discrete pustules |
| **Healthy** | < 0.30 | Uniform activation expected, higher BAR acceptable |

## 4. Visualization Standards

### 4.1 Colormap & Overlay
*   **Colormap**: `cv2.COLORMAP_JET` (Blue=Low, Red=High).
*   **Overlay Blend**: `0.4 × Heatmap + 0.6 × Original Image`.
*   **Resolution**: Upsample heatmap to original image resolution using bilinear interpolation.

### 4.2 Normalization
*   **Range**: Min-Max Normalize to `[0, 1]` per image.
*   **Noise Floor**: Set activations < 0.2 to zero (suppress noise).
*   **Clipping**: Cap activations > 0.95 at 0.95 to prevent single-pixel dominance.

### 4.3 Multi-View Heatmap Composition
When generating heatmaps for multiple crop views of the same image:
1.  Generate per-crop heatmaps independently.
2.  Map each crop heatmap back to original image coordinates.
3.  Average all aligned heatmaps.
4.  Highlight consensus regions (activated in ≥ 3 out of 10 crops).
5.  Store both individual and composite heatmaps for audit trail.

## 5. Quality Gate Summary

| Metric | Threshold | Action on Failure | Priority |
| :--- | :--- | :--- | :--- |
| **ROAD Score** | ≥ 0.3 | Block deployment | **Critical** |
| **Pointing Game Hit Rate** | ≥ 70% | Investigate model focus | High |
| **GradCAM-Leaf Overlap (GLOR)** | ≥ 70% | Flag background bias | High |
| **BAR** | < 30% | Retrain with CutMix | **Critical** |
| **Activation Noise** | < 20% area | Filter low activations below 0.2 | Medium |
| **Per-class ROAD variance** | σ < 0.15 | Investigate inconsistent classes | Medium |

## 6. GradCAM for Disease-Specific Diagnosis
Use heatmap patterns to validate disease identification:

| Disease | Expected Heatmap Pattern | Red Flag |
| :--- | :--- | :--- |
| **Early Blight** | Concentric ring activation on lesion center | Diffuse uniform activation |
| **Late Blight** | Irregular patch activation on water-soaked areas | Activation on leaf margins only |
| **Powdery Mildew** | Surface-distributed activation | Deep tissue activation |
| **Rust** | Discrete punctate activations on pustules | Single large blob |
| **Bacterial Spot** | Angular activations bounded by leaf veins | Circular activations |
| **Healthy** | Low uniform activation across leaf | Strong focal activation |

## 7. Code Example (PyTorch Grad-CAM)

```python
from pytorch_grad_cam import GradCAM
from pytorch_grad_cam.utils.image import show_cam_on_image
import numpy as np
import cv2
import torch

def generate_and_validate_gradcam(model, input_tensor, rgb_img, leaf_mask):
    """Generate GradCAM heatmap with full quality validation."""
    
    # Select target layer (ResNet example)
    target_layers = [model.layer4[-1]]
    cam = GradCAM(model=model, target_layers=target_layers)
    
    # Generate heatmap
    grayscale_cam = cam(input_tensor=input_tensor, targets=None)
    heatmap = grayscale_cam[0, :]
    
    # Suppress noise (activations < 0.2)
    heatmap[heatmap < 0.2] = 0.0
    
    # Validate: GradCAM-Leaf Overlap (GLOR)
    leaf_binary = (leaf_mask > 0).astype(float)
    glor = np.sum(heatmap * leaf_binary) / (np.sum(heatmap) + 1e-8)
    
    if glor < 0.70:
        print(f"WARNING: GLOR {glor:.2%} below 70% — background bias detected")
        
    # Validate: Background Activation Ratio (BAR)
    bar = np.sum(heatmap * (1 - leaf_binary)) / (np.sum(heatmap) + 1e-8)
    
    if bar >= 0.30:
        raise ValueError(f"BAR {bar:.2%} exceeds 30% limit - Model Rejected")
        
    # Visualize
    visualization = show_cam_on_image(rgb_img, heatmap, use_rgb=True)
    return visualization, {"glor": glor, "bar": bar}
```

## 8. Monitoring & Alerting
*   Track **ROAD score**, **GLOR**, and **BAR** per model version in MLflow/W&B.
*   **Alert** if any metric degrades > 10% between model versions.
*   **Weekly automated report** comparing heatmap quality across disease classes.
*   **Store heatmap samples** (10 per disease class per model version) for visual audit.

## 9. Cross-References
*   **Master Rules**: `rules/ml/RULES-plant-disease-analysis.md` → Section 6
*   **Binarization (leaf mask generation)**: `rules/ml/RULES-image-binarization.md`
*   **Error Catalog**: `errors/ml/ERROR-multi-view-pipeline-catalog.md` → ERR-HEAT-001
*   **Workflow**: `workflows/ml/ML_MULTI_VIEW_WORKFLOW.md` → Step 4 (Explainability)
