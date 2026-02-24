# Experiment Tracking Template
# Tooling: MLflow, Weights & Biases

## Experiment Details
*   **Experiment Name:** [e.g., `finbert-sentiment-v1`]
*   **Date:** [YYYY-MM-DD]
*   **Author:** [Your Name]
*   **Goal:** [e.g., Improve F1-score on minority class.]
*   **Hypothesis:** [e.g., Focal Loss will handle class imbalance better than CrossEntropy.]

## Configuration
*   **Base Model:** [e.g., `bert-base-uncased`]
*   **Dataset Version:** [e.g., `v2.1.0` (Hash: `a1b2c3d`)]
*   **Hyperparameters:**
    *   `learning_rate`: [e.g., 2e-5]
    *   `batch_size`: [e.g., 32]
    *   `epochs`: [e.g., 5]
    *   `optimizer`: [e.g., AdamW]
    *   `scheduler`: [e.g., Linear Warmup]
    *   `loss_function`: [e.g., Focal Loss (gamma=2.0)]

## Results
*   **Training Time:** [e.g., 2h 15m on A100]
*   **Best Epoch:** [e.g., 3]
*   **Metrics (Validation):**
    *   `accuracy`: [Value]
    *   `f1_macro`: [Value]
    *   `precision`: [Value]
    *   `recall`: [Value]
    *   `auc`: [Value]

## Analysis
*   **Observations:** [e.g., Model converged faster but overfitted slightly.]
*   **Comparison:** [e.g., +2% F1-score compared to baseline.]
*   **Issues:** [e.g., High variance in validation loss.]

## Artifacts
*   **Model Path:** [e.g., `s3://mlflow/artifacts/12345/model`]
*   **Logs:** [e.g., TensorBoard link]
*   **Code Commit:** [Git Hash]

## Next Steps
*   **Action:** [e.g., Tune `gamma` parameter for Focal Loss.]
*   **Decision:** [e.g., Promote to Staging for further testing.]
