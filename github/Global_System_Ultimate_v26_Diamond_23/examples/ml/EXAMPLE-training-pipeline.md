# EXAMPLE-training-pipeline.md
# Governance: ML/AI Application Framework (Feb 2026)
# Tooling: PyTorch, MLflow, Optuna

## 1. Project Structure
```
training-pipeline/
├── configs/
│   ├── config.yaml          # Hyperparameters, paths
│   └── logging.yaml         # Logging configuration
├── data/
│   ├── raw/                 # Immutable raw data
│   ├── processed/           # Cleaned and tokenized data
│   └── splits/              # Train/Val/Test splits (stratified)
├── src/
│   ├── data/                # Data loading and preprocessing scripts
│   ├── models/              # Model definition
│   ├── training/            # Training loop and evaluation
│   └── optimization/        # Hyperparameter tuning (Optuna)
├── notebooks/               # EDA and experimentation notebooks
├── tests/                   # Unit and integration tests
├── Dockerfile               # Multi-stage build
├── requirements.txt         # Pinned dependencies
└── README.md                # Project documentation
```

## 2. Training Loop Governance
*   **Seed:** Set random seed (42) for reproducibility.
*   **Logging:** Log metrics (loss, accuracy) to MLflow every epoch.
*   **Checkpointing:** Save model weights every epoch (or best validation loss).
*   **Early Stopping:** Stop training if validation loss doesn't improve for 5 epochs.

## 3. Hyperparameter Optimization
*   **Tool:** Optuna (Bayesian Optimization).
*   **Objective:** Minimize validation loss.
*   **Trials:** Run at least 50 trials.
*   **Pruning:** Use MedianPruner to stop unpromising trials early.

## 4. Evaluation Requirements
*   **Metrics:** Accuracy, Precision, Recall, F1-Score, AUC.
*   **Confusion Matrix:** Analyze misclassifications.
*   **Bias Check:** Verify performance across different subgroups.
*   **Drift Check:** Compare validation set distribution with training set.

## 5. Model Registry
*   **Tool:** MLflow Model Registry.
*   **Tags:** `training_data_hash`, `git_commit`, `hyperparameters`.
*   **Version:** Semantic Versioning (`v1.0.0`).
*   **Stage:** `Staging` -> `Production` (after approval).
