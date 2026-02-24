# Error Catalog: ML Training (v2026.2)

## 1. Gradient Explosion/Vanishing
-   **Symptom:** Loss becomes `NaN` or `0.0` quickly.
-   **Cause:** Learning rate too high, deep network without normalization.
-   **Fix:**
    -   Use Gradient Clipping (`torch.nn.utils.clip_grad_norm_`).
    -   Add Batch Normalization layers.
    -   Reduce Learning Rate.

## 2. Overfitting
-   **Symptom:** Training loss decreases, Validation loss increases.
-   **Cause:** Model too complex, insufficient data.
-   **Fix:**
    -   Add Dropout layers.
    -   Use L1/L2 Regularization (Weight Decay).
    -   Increase dataset size (Augmentation).
    -   Implement Early Stopping.

## 3. Data Leakage
-   **Symptom:** Model performs perfectly (99%+) on validation but fails in production.
-   **Cause:** Target variable leaked into features (e.g., future data).
-   **Fix:**
    -   Review feature engineering pipeline.
    -   Ensure time-based splitting for time-series data.
    -   Remove ID columns or direct proxies of the target.

## 4. CUDA Out of Memory (OOM)
-   **Symptom:** `RuntimeError: CUDA out of memory`.
-   **Cause:** Batch size too large, model too big for GPU VRAM.
-   **Fix:**
    -   Reduce Batch Size.
    -   Use Gradient Accumulation.
    -   Use Mixed Precision Training (`fp16`).
    -   Clear cache (`torch.cuda.empty_cache()`).
