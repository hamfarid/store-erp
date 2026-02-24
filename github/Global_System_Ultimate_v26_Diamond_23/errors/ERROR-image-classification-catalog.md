# ERROR-image-classification-catalog.md
# Governance: ML/AI Application Framework (Feb 2026)
# Tooling: PyTorch, Cleanlab

## 1. Data Quality (High Severity)
**ID:** `IC-DQ-001`
**Name:** Mislabeling
**Description:** Training data contains incorrect labels (avg 3.4% in benchmarks).
**Detection:** Cleanlab `find_label_issues()`.
**Resolution:** Relabel or remove noisy samples.
**Prevention:** Inter-annotator agreement > 0.8.

**ID:** `IC-DQ-002`
**Name:** Artifact Learning
**Description:** Model learns spurious correlations (e.g., watermark = class).
**Detection:** Grad-CAM visualization (heatmap on background).
**Resolution:** Remove artifacts; Augment data (CutMix).
**Prevention:** Data cleaning; Diverse data sources.

## 2. Preprocessing Errors (Medium Severity)
**ID:** `IC-PE-001`
**Name:** Aspect Ratio Distortion
**Description:** Resizing images without preserving aspect ratio (stretching).
**Detection:** Visual inspection; `PIL.Image.resize` without padding.
**Resolution:** Use `albumentations.Resize(always_apply=True, p=1)` with padding.
**Prevention:** Standardize resizing pipeline.

**ID:** `IC-PE-002`
**Name:** Normalization Mismatch
**Description:** Training on ImageNet stats but inferencing on [0, 255].
**Detection:** Poor performance; `ValueError`.
**Resolution:** Ensure consistent normalization pipeline.
**Prevention:** Encapsulate preprocessing in `torchvision.transforms`.

## 3. Model Architecture (Low Severity)
**ID:** `IC-MA-001`
**Name:** Vanishing Gradients
**Description:** Deep networks fail to learn due to gradients approaching zero.
**Detection:** Gradient monitoring (TensorBoard).
**Resolution:** Use ResNet (skip connections); Batch Normalization.
**Prevention:** Proper initialization (He/Xavier).
