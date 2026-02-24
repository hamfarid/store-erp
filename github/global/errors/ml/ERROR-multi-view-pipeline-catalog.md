# Multi-View Pipeline Error Catalog (v26.0)

> **Scope**: All Errors in the Plant Disease Multi-View Pipeline
> **Compliance**: Global System v26 Diamond 32 v26 Diamond 9
> **Referenced by**: `errors/DONT_MAKE_THESE_ERRORS_AGAIN.md`, all `rules/ml/` files

## 1. Image Quality Errors

### ERR-IMG-001: Resolution Below Minimum
-   **Severity**: High
-   **Symptoms**: Image accepted but feature extraction produces poor-quality embeddings.
-   **Cause**: Input image resolution below 1280×960 minimum.
-   **Resolution**: Reject image at ingestion with clear error message. Request re-capture at higher resolution.
-   **Prevention**: Validate resolution at pipeline entry point before any processing. Log rejection with image metadata.

### ERR-IMG-002: Blur Threshold Exceeded
-   **Severity**: High
-   **Symptoms**: Model predictions are low-confidence or incorrect. GradCAM shows diffuse activation.
-   **Cause**: Laplacian variance < 100.0 indicating motion blur or out-of-focus capture.
-   **Resolution**: Reject image. Instruct user to stabilize camera, clean lens, and retake.
-   **Prevention**: Calculate Laplacian variance at ingestion. Block images with variance < 100.0 from entering pipeline.

### ERR-IMG-003: Glare Detected
-   **Severity**: Medium
-   **Symptoms**: Binarization produces artifacts. GradCAM highlights glare spots instead of disease regions.
-   **Cause**: High intensity pixel clusters (V > 250 in HSV) covering > 10% of image area. Direct flash or sunlight reflection.
-   **Resolution**: Reject or flag image. Suggest adjusting lighting angle or using polarizing filter.
-   **Prevention**: Check V-channel histogram at ingestion. Flag images where pixels with V > 250 exceed 10% of total area.

## 2. Crop & Augmentation Errors

### ERR-CROP-001: Crop Strategy Mismatch
-   **Severity**: Critical
-   **Symptoms**: Training accuracy high but inference accuracy significantly lower. TTA provides no benefit.
-   **Cause**: Using random crop at inference time instead of deterministic 10-crop strategy. Or using center crop during training but multi-crop during inference.
-   **Resolution**: Apply consistent crop strategy: random resized crop for training, deterministic 10-crop + horizontal flip (TTA) for inference. Follow `rules/ml/RULES-multi-crop-augmentation.md` Section 4 Decision Matrix.
-   **Prevention**: Validate crop strategy in inference pipeline config matches the expected strategy for the deployment scenario. Add assertion that inference receives exactly 10 crops when TTA is enabled.

### ERR-CROP-002: Color Augmentation Exceeds Disease-Safe Limits
-   **Severity**: High
-   **Symptoms**: Model confuses similar diseases (e.g., early blight vs rust). Color-dependent features are unreliable.
-   **Cause**: Hue jitter > 0.1 or saturation jitter > 0.4 during training, destroying disease color signals.
-   **Resolution**: Reduce augmentation to disease-safe limits per `rules/ml/RULES-multi-crop-augmentation.md` Section 2.
-   **Prevention**: Augmentation config must be reviewed by Data Scientist before training. Hard-code maximum limits in augmentation pipeline.

### ERR-CROP-003: Crop Size Below Minimum
-   **Severity**: Medium
-   **Symptoms**: Model sees insufficient context in crop. Predictions on edge crops are random.
-   **Cause**: Random resized crop scale set below 0.08, producing crops that are < 5% of image area.
-   **Resolution**: Set minimum scale to 0.08 per governance rules.
-   **Prevention**: Validate augmentation config parameters before training launch.

## 3. Binarization & Segmentation Errors

### ERR-BIN-001: Binarization Threshold Drift
-   **Severity**: High
-   **Symptoms**: Binary mask is all black (no foreground) or all white (no background separation). Foreground ratio outside 5-60% range.
-   **Cause**: Fixed Otsu threshold fails on field images with uneven lighting. Or HSV ranges misconfigured for the specific disease type.
-   **Resolution**: Switch from Otsu to adaptive thresholding (block_size=11, C=2) for field conditions. Verify HSV ranges per `rules/ml/RULES-image-binarization.md` Section 4.
-   **Prevention**: Quality gate check on foreground ratio (5-60%) after binarization. Automatic fallback from Otsu to adaptive if foreground ratio is out of range.

### ERR-BIN-002: Morphological Kernel Exceeds Limits
-   **Severity**: Medium
-   **Symptoms**: Fine lesion details destroyed. Distinct lesions merged into single large blob.
-   **Cause**: Kernel size > 15×15 or iterations > 5, violating hard limits in `rules/ml/RULES-image-binarization.md` Section 2.
-   **Resolution**: Reduce kernel size and iterations to within governance limits.
-   **Prevention**: Assert kernel size ≤ 15 and iterations ≤ 5 in preprocessing code. Code review must verify morphological parameters.

### ERR-SAM-001: SAM2 Oversegmentation
-   **Severity**: Medium
-   **Symptoms**: SAM2 produces too many small segments on heavily diseased leaves. Hundreds of tiny masks instead of coherent leaf/lesion regions.
-   **Cause**: Default SAM2 parameters too sensitive for plant disease images. Complex texture confuses the model.
-   **Resolution**: Apply connected component filtering with min_area threshold (100 px²). Merge adjacent small segments. Alternatively, fall back to Otsu+morphology pipeline.
-   **Prevention**: Post-process all SAM2 output with contour count check (< 50 contours). If exceeded, trigger fallback pipeline.

## 4. Embedding & Vector DB Errors

### ERR-EMB-001: Embedding Dimension Mismatch
-   **Severity**: Critical
-   **Symptoms**: Vector DB insertion fails with dimension error. Or queries return nonsensical similarity scores.
-   **Cause**: Model outputs different dimensions (e.g., ResNet50 2048d) than vector DB collection expects (e.g., DINOv2 768d). Often occurs after model version upgrade without re-indexing.
-   **Resolution**: Verify model output dimensionality matches collection schema before any insertion. If model changed, create new collection and re-index all embeddings.
-   **Prevention**: Store embedding model version in collection metadata. Pre-deployment check: assert `model.output_dim == collection.dimension`. See `errors/ml/ERROR-drift-detection-catalog.md` → ERR-DRIFT-004.

### ERR-EMB-002: Missing L2 Normalization
-   **Severity**: High
-   **Symptoms**: Cosine similarity scores are not in [0, 1] range. Similar images return low similarity scores.
-   **Cause**: Embeddings stored without L2 normalization. Cosine similarity on unnormalized vectors produces unreliable results.
-   **Resolution**: Re-normalize all stored embeddings: `embedding = embedding / np.linalg.norm(embedding)`. Re-index collection.
-   **Prevention**: Assert `abs(np.linalg.norm(embedding) - 1.0) < 1e-6` before every insertion. Mandatory per `rules/ml/RULES-embedding-storage.md` Section 2.3.

### ERR-DB-001: Vector DB Connection Failed
-   **Severity**: Critical
-   **Symptoms**: Pipeline halts at embedding storage/query step. Timeout errors in logs.
-   **Cause**: Vector DB service (Milvus/Qdrant/ChromaDB) is down, overloaded, or network issue.
-   **Resolution**: Check service health endpoint. Restart service if needed. If persistent, check resource allocation (RAM, disk).
-   **Prevention**: Health check endpoint monitored every 60 seconds. Automatic failover to read-only cache for query operations. Circuit breaker pattern: after 3 consecutive failures, queue embeddings for later insertion.

## 5. GradCAM & Explainability Errors

### ERR-HEAT-001: GradCAM Background Activation
-   **Severity**: High
-   **Symptoms**: GradCAM heatmap highlights soil, pot, or background instead of leaf lesion. BAR (Background Activation Ratio) > 30%.
-   **Cause**: Model learned background correlations instead of disease features. Often caused by consistent backgrounds in training data (e.g., all lab images on white board).
-   **Resolution**: Validate BAR < 0.3 and GradCAM-Leaf Overlap ≥ 70%. If failed, retrain with CutMix augmentation and background randomization.
-   **Prevention**: Include GradCAM quality validation in model evaluation pipeline. Block deployment if BAR > 0.30 per `rules/ml/RULES-gradcam-heatmap.md` Section 4.

### ERR-HEAT-002: Zero Gradients in GradCAM
-   **Severity**: Medium
-   **Symptoms**: Heatmap is completely blank (all zeros). No activation visible.
-   **Cause**: Model is in training mode with `torch.no_grad()` context, or target layer selection is incorrect for the architecture.
-   **Resolution**: Ensure model is in `eval()` mode but gradients are enabled for CAM computation. Verify target layer per architecture table in `rules/ml/RULES-gradcam-heatmap.md` Section 1.
-   **Prevention**: Add assertion that heatmap max value > 0.1 after generation.

## 6. System & Memory Errors

### ERR-MEM-001: GPU Memory Overflow in Multi-View
-   **Severity**: Critical
-   **Symptoms**: CUDA OOM error. Process killed during inference on multi-view batch.
-   **Cause**: Processing 10 crops × multiple views × full resolution simultaneously exceeds GPU memory (typically 8GB).
-   **Resolution**: Batch views in groups of 4. Clear intermediate tensors with `torch.cuda.empty_cache()` between batches. Reduce batch size.
-   **Prevention**: Calculate memory budget before processing: `n_crops × image_size × model_memory`. Enforce ≤ 500MB GPU total per pipeline config in `rules/ml/RULES-plant-disease-analysis.md` Section 10.

### ERR-MEM-002: Memory Leak in Long-Running Pipeline
-   **Severity**: High
-   **Symptoms**: Pipeline worker memory grows continuously over hours. Eventually OOM kill.
-   **Cause**: Accumulating tensors on GPU without proper cleanup. Storing references in lists that prevent garbage collection.
-   **Resolution**: Profile memory usage with `torch.cuda.memory_summary()`. Ensure `del` and `torch.cuda.empty_cache()` after each image. Use with `torch.no_grad()` for inference.
-   **Prevention**: Memory monitoring alert if worker RSS exceeds 2× baseline after 1 hour of operation.

## Error Resolution Quick Reference

| Code | Severity | Summary | First Action |
| :--- | :--- | :--- | :--- |
| **ERR-IMG-001** | Low resolution | Reject + re-capture |
| **ERR-IMG-002** | Blurry image | Reject + re-capture |
| **ERR-IMG-003** | Glare detected | Flag + adjust lighting |
| **ERR-CROP-001** | Crop mismatch | Fix inference config |
| **ERR-CROP-002** | Color aug too high | Reduce hue/sat limits |
| **ERR-BIN-001** | Bad binarization | Switch to adaptive |
| **ERR-SAM-001** | Oversegmentation | Filter small contours |
| **ERR-EMB-001** | Dimension mismatch | Re-index collection |
| **ERR-EMB-002** | Missing L2 norm | Re-normalize vectors |
| **ERR-HEAT-001** | Background focus | Retrain with CutMix |
| **ERR-MEM-001** | GPU OOM | Reduce batch/views |
| **ERR-DB-001** | Vector DB down | Check service health |

## Cross-References

-   **Master Rules**: `rules/ml/RULES-plant-disease-analysis.md`
-   **Binarization**: `rules/ml/RULES-image-binarization.md`
-   **GradCAM**: `rules/ml/RULES-gradcam-heatmap.md`
-   **Embeddings**: `rules/ml/RULES-embedding-storage.md`
-   **Multi-Crop**: `rules/ml/RULES-multi-crop-augmentation.md`
-   **Drift Errors**: `errors/ml/ERROR-drift-detection-catalog.md`
-   **DL Training Errors**: `errors/ml/ERROR-deep-learning-training-catalog.md`
-   **Parent File**: `errors/DONT_MAKE_THESE_ERRORS_AGAIN.md`
