# Model Deployment Workflow (MLOps)

## 1. Pre-Deployment Checks
*   **Model Card**: Updated with latest metrics?
*   **Performance**: F1-Score > 0.85 (or baseline)?
*   **Bias Check**: Fairness metrics within threshold?
*   **Security**: Checkpoint scanned for malware (Pickle)?

## 2. Packaging
1.  **Containerize**: Build Docker image with `uv` dependencies.
2.  **Optimize**: Convert to ONNX/TensorRT if applicable.
3.  **Register**: Push to MLflow Model Registry (Stage: Staging).

## 3. Deployment Strategy
*   **Canary**: Deploy to 5% of traffic. Monitor error rate.
*   **Shadow**: Deploy alongside vCurrent. Compare outputs (no user impact).
*   **Blue/Green**: Full switchover with instant rollback capability.

## 4. Monitoring (Day 2 Ops)
*   **Drift Detection**: Monitor input distribution (Evidently AI).
*   **Latency**: P99 < 200ms.
*   **Feedback Loop**: Collect user corrections for retraining.
