# Deep Learning Training Error Catalog (v26.0)

> **Scope**: Neural Network Training Failures
> **Compliance**: Multi-View Plant Disease Detection
> **Referenced by**: `errors/DONT_MAKE_THESE_ERRORS_AGAIN.md` → ML-DL-001
> **Version**: v26.0.0 (Diamond 6)

## Purpose

This catalog documents common deep learning training errors encountered in the plant disease detection pipeline. Each entry includes symptoms, root cause, resolution, and automated prevention measures.

-----

## ERR-DL-001: NaN Loss During Training

**Severity:** 🔴 Critical
**Symptoms:** Loss becomes `NaN` after N epochs, model outputs garbage predictions.
**Root Cause:** Learning rate too high, causing gradient explosion. Alternatively, division by zero in custom loss function, or corrupted input data (NaN pixels).
**Resolution:**

- Reduce learning rate by 10× (e.g., 1e-3 → 1e-4).
- Add gradient clipping: `torch.nn.utils.clip_grad_norm_(model.parameters(), max_norm=1.0)`.
- Validate input data: `assert not torch.isnan(batch).any()` before forward pass.
- Use `torch.autograd.detect_anomaly()` during debugging to locate exact operation.

**Prevention:**
- Always start with lr=1e-4 for fine-tuning pre-trained models.
- Use learning rate warmup (linear warmup over first 5% of training steps).
- Add NaN check hook: terminate training immediately if loss is NaN for 3 consecutive steps.

## ERR-DL-002: Gradient Explosion

**Severity:** 🔴 Critical
**Symptoms:** Loss spikes suddenly, weights become extremely large, model diverges.
**Root Cause:** Uncontrolled gradient magnitudes, often caused by deep networks without residual connections, or batch normalization layer in eval mode during training.
**Resolution:**

- Apply gradient clipping: `max_norm=1.0` (default) or `max_norm=5.0` for RNNs.
- Verify all BatchNorm layers are in `.train()` mode during training.
- Switch optimizer from SGD to AdamW (more robust to gradient magnitude).

**Prevention:**
- Mandatory gradient clipping in all training configs.
- Log gradient norms per layer every 100 steps. Alert if any layer > 100.

## ERR-DL-003: Gradient Vanishing

**Severity:** 🟠 High
**Symptoms:** Model trains but loss plateaus early, deeper layers show near-zero gradients.
**Root Cause:** Sigmoid/Tanh activations in deep networks, improper weight initialization.
**Resolution:**

- Switch activations to ReLU/GELU/SiLU.
- Use He initialization for ReLU networks, Xavier for Tanh.
- Add residual/skip connections.

**Prevention:**
- Default activation: GELU for transformer-based, ReLU for CNN-based.
- Monitor per-layer gradient statistics during first epoch.

## ERR-DL-004: Overfitting (Train/Val Gap > 15%)

**Severity:** 🟠 High
**Symptoms:** Training accuracy > 95% but validation accuracy < 80%.
**Root Cause:** Model memorizing training data. Insufficient regularization. Insufficient data diversity. Data leakage between train/val splits.
**Resolution:**

- Add dropout (p=0.3 for FC layers, p=0.1 for CNN).
- Increase augmentation strength (within disease-safe limits per RULES-multi-crop-augmentation.md).
- Add weight decay (AdamW default: 0.01).
- Verify no data leakage: same plant image must NOT appear in both train and val.

**Prevention:**
- Split by plant specimen ID (not by image) to prevent leakage.
- Early stopping with patience=10 epochs on validation loss.
- Log train/val gap every epoch. Alert if gap > 15%.

## ERR-DL-005: Learning Rate Too High / Too Low

**Severity:** 🟡 Medium
**Symptoms:**

- Too high: Loss oscillates wildly, never converges.
- Too low: Training converges extremely slowly, stuck in local minimum.

**Root Cause:** LR not tuned for the specific model/dataset combination.
**Resolution:**
- Run LR range test (Leslie Smith method) before training.
- Use OneCycleLR scheduler with max_lr found from range test.
- Fine-tuning pre-trained models: use 10-100× lower LR than training from scratch.

**Prevention:**
- Standard LRs: scratch training = 1e-3, fine-tuning = 1e-4 to 1e-5.
- Always use LR scheduler (CosineAnnealingLR or OneCycleLR).

## ERR-DL-006: Class Imbalance (Rare Disease Underperformance)

**Severity:** 🟠 High
**Symptoms:** High overall accuracy but < 50% recall on rare disease classes.
**Root Cause:** Training set has severe class imbalance (e.g., 10000 healthy vs 50 rust images).
**Resolution:**

- Weighted CrossEntropy: `weight = 1.0 / class_counts`, normalized.
- Oversampling minority classes with augmentation.
- Focal Loss (γ=2.0) for hard example mining.

**Prevention:**
- Log per-class F1 score, not just overall accuracy.
- Set minimum per-class recall threshold: 60% for any class.
- Use stratified sampling in DataLoader.

## ERR-DL-007: Batch Size Mismatch with BatchNorm

**Severity:** 🟡 Medium
**Symptoms:** Model performs well during training, poorly during single-image inference.
**Root Cause:** BatchNorm statistics are noisy with batch_size=1 during inference.
**Resolution:**

- Always call `model.eval()` before inference (uses running statistics).
- For very small batches (< 8), consider GroupNorm or LayerNorm instead.

**Prevention:**
- Training batch size minimum: 16 (for reliable BatchNorm statistics).
- Validation batch size: match training batch size or use `model.eval()`.

## ERR-DL-008: Mixed Precision Training Failure

**Severity:** 🟡 Medium
**Symptoms:** Loss becomes `inf` or model produces zero outputs with AMP enabled.
**Root Cause:** Certain operations (log, exp, division) underflow/overflow in float16.
**Resolution:**

- Use `torch.amp.GradScaler` with dynamic loss scaling.
- Keep loss computation in float32: `with torch.amp.autocast(enabled=False): loss = criterion(...)`.

**Prevention:**
- Default: Use BFloat16 instead of Float16 (wider dynamic range, no GradScaler needed).
- Test AMP on 1 epoch before full training run.

-----

## Quick Reference: Training Config Defaults

|Parameter            |Default Value       |Notes                   |
|:--------------------|:-------------------|:-----------------------|
|**Optimizer**        |AdamW               |weight_decay=0.01       |
|**Learning Rate**    |1e-4 (fine-tune)    |1e-3 for scratch        |
|**LR Scheduler**     |CosineAnnealingLR   |T_max = total_epochs    |
|**Warmup**           |5% of steps         |Linear warmup           |
|**Gradient Clipping**|max_norm=1.0        |Always enabled          |
|**Batch Size**       |32 (GPU) / 16 (min) |Minimum 16 for BatchNorm|
|**Precision**        |BFloat16            |Float32 fallback        |
|**Early Stopping**   |patience=10         |Monitor val_loss        |
|**Dropout**          |0.3 (FC) / 0.1 (CNN)|After last pooling layer|

## Cross-References

- **Master Rules**: `rules/ml/RULES-plant-disease-analysis.md`
- **Augmentation Limits**: `rules/ml/RULES-multi-crop-augmentation.md` → Section 2
- **Parent Error File**: `errors/DONT_MAKE_THESE_ERRORS_AGAIN.md` → ML-DL-001
