# Don’t Make These Errors Again

> **Purpose**: Track all errors to prevent repeating the same mistakes.
> **Law 8**: Trust is good, Automation is better.
> **Version**: v26.0.0 (Diamond 2)
> **Last Updated**: Feb 16, 2026
> **Status**: Active

## How to Use This File

### When Error Occurs:
1.  **Log immediately** - Don’t wait
2.  **Be specific** - Include context
3.  **Document solution** - How you fixed it
4.  **Add prevention** - How to avoid it (e.g., add to Sentinel)

### Before Implementing:
1.  **Search this file** - Check if error is known
2.  **Read prevention tips** - Follow them
3.  **Update if needed** - Add new insights

## Critical Errors (System-Breaking)

### Error #C001: Committing Secrets
*   **Severity**: Critical
*   **Context**: Developer committed `.env` file or hardcoded API key.
*   **Solution**: Remove file from git history (`git filter-branch`). Rotate keys immediately.
*   **Prevention (Global System Ultimate)**:
    *   **Sentinel Tool**: `sentinel.py` now blocks commits with secrets.
    *   **Pre-commit Hook**: Ensure `speckit verify` is run before push.

### Error #C002: Committing TODOs
*   **Severity**: Critical
*   **Context**: Developer left `TODO` or `FIXME` in the code and deployed.
*   **Solution**: Finish the task or move it to a ticket system.
*   **Prevention (Global System Ultimate)**:
    *   **Sentinel Tool**: `sentinel.py` blocks commits with `TODO` in source code.

### Error #C003: Hallucinated Imports
*   **Severity**: Critical
*   **Context**: AI imported a library that doesn’t exist in `requirements.txt`.
*   **Solution**: Run `pip install` and update `requirements.txt`.
*   **Prevention (Global System Ultimate)**:
    *   **Speckit Analyze**: Always map dependencies before coding.
    *   **Law 2**: Uncertainty is a failure state. Check before you import.

## High Priority Errors (Functionality Impact)

### Error #H001: Losing Context
*   **Severity**: High
*   **Context**: AI forgot the file structure or previous decisions.
*   **Solution**: Re-read `system_log.md` and `memory-bank/code_structure.json`.
*   **Prevention (Global System Ultimate)**:
    *   **Speckit Analyze**: Automatically recalls memory before every task.
    *   **Law 1**: Mandatory Refresh every 10 minutes.

### Error #H002: Breaking Existing Features
*   **Severity**: High
*   **Context**: New feature caused regression in old feature.
*   **Solution**: Revert changes and add regression tests.
*   **Prevention (Global System Ultimate)**:
    *   **Speckit Verify**: Runs `coderabbit_reviewer.py` to check for regressions.
    *   **E2E Testing**: Use `prompts/42_e2e_testing.md`.

## Medium Priority Errors (UX/Performance)

### Error #M001: UI Glitches
*   **Severity**: Medium
*   **Context**: Button misalignment or bad contrast.
*   **Solution**: Fix CSS and verify with screenshot.
*   **Prevention (Global System Ultimate)**:
    *   **UI/UX Testing**: Use `prompts/43_ui_ux_testing.md`.
    *   **Visual Regression**: Use Playwright to compare screenshots.

## Error Resolution Workflow (Global System Ultimate)
1.  Error Occurs
2.  Log Error (this file)
3.  Investigate Root Cause
4.  Implement Solution
5.  Automate Prevention (Add to Sentinel/Speckit)
6.  Verify Fix (Speckit Verify)

## ML & AI Errors (Governance)

### Error #ML001: Data Leakage
*   **Severity**: Critical
*   **Context**: Training data included in validation set.
*   **Solution**: Use strict time-based splitting for time-series. Verify no overlap in `patient_id` or `user_id`.
*   **Prevention**: Use `rules/ml/POLICY-feature-store-governance.yaml`.

### Error #ML002: Silent Model Failure
*   **Severity**: Critical
*   **Context**: Model returns predictions but accuracy has degraded (Drift).
*   **Solution**: Retrain model on recent data.
*   **Prevention**: Implement Drift Detection (EvidentlyAI). Use `rules/ml/POLICY-retraining-triggers.yaml`.

### Error #ML003: Training-Serving Skew
*   **Severity**: High
*   **Context**: Feature calculation logic differs between training (Spark) and inference (Python).
*   **Solution**: Unify logic using a Feature Store (Feast).
*   **Prevention**: Adhere to `rules/ml/POLICY-feature-store-governance.yaml`.

## Multi-View Plant Disease Pipeline Errors
> **Reference Catalog**: `errors/ml/ERROR-multi-view-pipeline-catalog.md`

### Error #ERR-CROP-001: Crop Strategy Mismatch
*   **Severity**: Critical
*   **Context**: Using random crop at inference time instead of deterministic 10-crop.
*   **Solution**: Apply TTA (Test-Time Augmentation) with 5-crop + horizontal flip = 10 views.
*   **Prevention**: See `errors/ml/ERROR-multi-view-pipeline-catalog.md` → ERR-CROP-001.

### Error #ERR-BIN-001: Binarization Threshold Drift
*   **Severity**: High
*   **Context**: Fixed Otsu threshold fails on field images with uneven lighting.
*   **Solution**: Switch to adaptive thresholding (block_size=11, C=2) for field conditions.
*   **Prevention**: See `errors/ml/ERROR-multi-view-pipeline-catalog.md` → ERR-BIN-001.

### Error #ERR-EMB-001: Embedding Dimension Mismatch
*   **Severity**: Critical
*   **Context**: Model outputs 2048-dim (ResNet50) but vector DB expects 768-dim (DINOv2).
*   **Solution**: Verify model output dimensionality matches collection schema before insertion.
*   **Prevention**: See `errors/ml/ERROR-multi-view-pipeline-catalog.md` → ERR-EMB-001.

### Error #ERR-HEAT-001: GradCAM Background Activation
*   **Severity**: High
*   **Context**: GradCAM heatmap highlights soil/background instead of leaf lesion.
*   **Solution**: Validate BAR (Background Activation Ratio) < 0.3. If exceeded, retrain with CutMix augmentation.
*   **Prevention**: See `errors/ml/ERROR-multi-view-pipeline-catalog.md` → ERR-HEAT-001.

### Error #ERR-SAM-001: SAM2 Oversegmentation
*   **Severity**: Medium
*   **Context**: SAM2 produces too many small segments on heavily diseased leaves.
*   **Solution**: Apply connected component filtering with `min_area` threshold.
*   **Prevention**: See `errors/ml/ERROR-multi-view-pipeline-catalog.md` → ERR-SAM-001.

### Error #ERR-MEM-001: GPU Memory Overflow in Multi-View
*   **Severity**: Critical
*   **Context**: Processing 10 crops × 3 views × full-resolution causes OOM on 8GB GPU.
*   **Solution**: Batch views in groups of 4, clear intermediate tensors with `torch.cuda.empty_cache()`.
*   **Prevention**: See `errors/ml/ERROR-multi-view-pipeline-catalog.md` → ERR-MEM-001.

### Error #ML-DL-001: Deep Learning Catalog
*   **Severity**: Critical
*   **Context**: General deep learning training failures (NaN loss, gradient explosion, learning rate issues).
*   **Prevention**: See `errors/ml/ERROR-deep-learning-training-catalog.md`.

### Error #FD-TZ-001: Drift Detection Failures
*   **Severity**: High
*   **Context**: Embedding centroid shift exceeds threshold but no alert fires.
*   **Prevention**: See `errors/ml/ERROR-drift-detection-catalog.md`.

### Error #WS-RL-001: Web Scraping Rate Limits
*   **Severity**: Medium
*   **Context**: Image scraping pipeline blocked by rate limiting.
*   **Prevention**: See `errors/ERROR-web-scraping-catalog.md`.
