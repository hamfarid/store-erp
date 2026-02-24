# EXAMPLE-plant-disease-classification.md
# Governance: ML/AI Application Framework (Feb 2026)
# Reference: PlantVillage Dataset (54,303 images, 38 classes)

## 1. Project Structure
```
plant-disease-classification/
├── configs/
│   ├── config.yaml          # Hyperparameters, paths
│   └── logging.yaml         # Logging configuration
├── data/
│   ├── raw/                 # Immutable raw data (PlantVillage)
│   ├── processed/           # Resized and normalized images
│   └── splits/              # Train/Val/Test splits (stratified)
├── src/
│   ├── data/                # Data loading and preprocessing scripts
│   ├── models/              # Model definition (EfficientNet-B4)
│   ├── training/            # Training loop and evaluation
│   └── serving/             # FastAPI serving code
├── notebooks/               # EDA and experimentation notebooks
├── tests/                   # Unit and integration tests
├── Dockerfile               # Multi-stage build
├── requirements.txt         # Pinned dependencies
└── README.md                # Project documentation
```

## 2. Preprocessing Rules
*   **Resize:** 380x380 pixels (EfficientNet-B4 default).
*   **Normalization:** ImageNet stats (mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]).
*   **Augmentation:**
    *   RandomHorizontalFlip (p=0.5).
    *   RandomRotation (degrees=15).
    *   ColorJitter (brightness=0.2, contrast=0.2).

## 3. Model Architecture
*   **Base Model:** EfficientNet-B4 (Pretrained on ImageNet).
*   **Task:** Multi-class Classification (38 classes).
*   **Loss Function:** CrossEntropyLoss.
*   **Optimizer:** AdamW (learning rate: 1e-4).

## 4. Evaluation Requirements
*   **Primary Metric:** Accuracy (> 99%).
*   **Secondary Metrics:** Precision, Recall, F1-Score per class.
*   **Generalization Check:** Validate on PlantDoc dataset (real-world images).
*   **Confusion Matrix:** Analyze misclassifications between similar diseases.

## 5. Governance Checkpoints
*   **Data Validation:** Check for corrupted images, valid labels (0-37).
*   **Drift Detection:** Monitor input image distribution (embedding drift).
*   **Model Card:** Document model limitations (e.g., lab vs. field conditions).
