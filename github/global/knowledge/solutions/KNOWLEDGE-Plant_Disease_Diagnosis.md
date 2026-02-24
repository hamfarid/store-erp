# Knowledge: Plant Disease Diagnosis

## Overview
This guide provides best practices for diagnosing plant diseases using computer vision models.

### 1. Data Collection
- Collect high-quality images of healthy and diseased leaves.
- Ensure diverse lighting conditions and backgrounds.

### 2. Preprocessing
- Resize images to a standard resolution (e.g., 224x224).
- Apply data augmentation (rotation, flip, color jitter).

### 3. Model Selection
- Use transfer learning with pre-trained models (e.g., ResNet, EfficientNet).
- Fine-tune the model on the specific dataset.

### 4. Evaluation
- Use confusion matrix and F1-score for evaluation.
- Visualize model predictions using Grad-CAM.
