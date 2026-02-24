# Deep Learning Error Catalog

> **Scope**: Deep Learning, Neural Networks, Training Convergence
> **Owner**: ML Engineer

## ML-DL-001: Model Convergence Failure
- **Description**: Loss function fails to decrease or oscillates wildly.
- **Severity**: Critical
- **Cause**: Learning rate too high, bad initialization, or vanishing gradients.
- **Solution**:
    1. Reduce learning rate (LR scheduler).
    2. Check gradient clipping.
    3. Verify data normalization.

## ML-DL-002: CUDA OOM (Out of Memory)
- **Description**: GPU memory exhausted during training.
- **Severity**: Critical
- **Cause**: Batch size too large or model too deep.
- **Solution**:
    1. Reduce batch size.
    2. Use Gradient Accumulation.
    3. Enable Mixed Precision (AMP).
