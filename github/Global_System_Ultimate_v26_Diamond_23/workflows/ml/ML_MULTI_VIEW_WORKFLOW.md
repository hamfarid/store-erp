# Multi-View Plant Disease Diagnosis Workflow (v26.0)
# Scope: End-to-End Pipeline Orchestration
# Compliance: Global System Ultimate v26 Diamond 2

---

## 1. Introduction
This workflow orchestrates the end-to-end process of diagnosing plant diseases using multiple camera views. It integrates strict quality gates, advanced segmentation, explainable AI, and similarity search through a governed pipeline with clear error handling and monitoring.

## 2. Pipeline Architecture

```
Image Capture → Gate-1 (Quality) → Binarization (5 Views) → Gate-2 (Mask Quality)
  → Multi-Crop (10 Views) → Feature Extraction → Embedding Generation
  → Gate-3 (Embedding Quality) → Classification → GradCAM → Gate-4 (Explainability)
  → Similarity Search → Report Generation → Storage & Monitoring
```

## 3. Workflow Steps

### Step 1: Image Acquisition & Validation
**Input:** 1-3 images per plant (Top, Side, Close-up preferred).
**Validation Checks:**
*   Resolution ≥ 1280×960 pixels (reject ERR-IMG-001 if below).
*   File format: JPEG (quality ≥ 85), PNG, or TIFF.
*   File size: 50KB - 20MB (reject if outside range).
*   Metadata extraction: GPS, timestamp, camera model (if available).
**Output:** Validated raw images with metadata record.

### Step 2: Quality Gate 1 — Image Quality
**Rules Reference:** `rules/ml/RULES-plant-disease-analysis.md` Section 3.
**Checks:**
*   Blur detection: Laplacian variance ≥ 100.0 (reject ERR-IMG-002).
*   Glare detection: V > 250 pixels ≤ 10% of area (flag ERR-IMG-003).
*   Color space validity: Image is 3-channel RGB.
**Fail Action:** Return error to user with specific failure code and re-capture guidance.
**Pass Action:** Forward to Step 3.

### Step 3: Binarization & Segmentation (5 Binary Views)
**Rules Reference:** `rules/ml/RULES-image-binarization.md`.
**Process:**
1.  Convert RGB → HSV.
2.  Generate 5 binary views: Green Mask, Disease Mask, Edge Binary, Texture Binary, Saturation Binary.
3.  Apply morphological cleanup: Opening(3,3) + Closing(5,5) within hard limits (max kernel 15×15, max 5 iterations).
4.  Segmentation method selection via decision tree: SAM2 (complex/GPU) → Adaptive Threshold (field) → Otsu (lab/fast).
**Output:** 5 binary masks per input image.

### Step 4: Quality Gate 2 — Mask Quality
**Checks:**
*   Foreground ratio: 5-60% (reject ERR-BIN-001 if outside).
*   Contour count: 1-50 (reject if noisy).
*   Minimum contour area: 100 px².
**Fail Action:** Log error, attempt fallback method (Otsu → Adaptive → SAM2). If all fail, reject image.
**Pass Action:** Forward to Step 5.

### Step 5: Multi-Crop Augmentation (10+ Views)
**Rules Reference:** `rules/ml/RULES-multi-crop-augmentation.md`.
**Process:**
1.  Resize image to 256×256.
2.  Generate 5 crops: Top-Left, Top-Right, Bottom-Left, Bottom-Right, Center (224×224).
3.  Apply horizontal flip to each crop → 10 views total.
4.  For high-accuracy mode: add 3-scale processing (224, 256, 384) → up to 30 views.
**Output:** 10-30 crop tensors per input image.
**Memory Budget:** ≤ 200MB GPU for 10-crop, ≤ 500MB for 30-crop.

### Step 6: Feature Extraction & Embedding Generation
**Rules Reference:** `rules/ml/RULES-embedding-storage.md`, `rules/ml/RULES-plant-disease-analysis.md` Section 6.
**Process:**
1.  Forward all crops through DINOv2 ViT-B/14 backbone.
2.  Extract 768-dimensional embedding per crop.
3.  L2-normalize ALL embeddings (mandatory: `assert abs(norm - 1.0) < 1e-6`).
4.  Average embeddings across crops for final image embedding.
5.  Extract texture features: GLCM (distances=[1,3,5]), LBP (radius=3, n_points=24).
**Output:** 768d normalized embedding + texture feature vector per image.
**Time Budget:** 30ms (GPU) / 300ms (CPU) per image.

### Step 7: Quality Gate 3 — Embedding Quality
**Checks:**
*   Embedding norm = 1.0 ± 1e-6 (verify L2 normalization).
*   Embedding values are finite (no NaN or Inf).
*   Embedding dimensionality matches vector DB collection schema.
**Fail Action:** Re-extract embedding. If persistent, log ERR-EMB-001 and skip storage.
**Pass Action:** Store in vector DB and forward to Step 8.

### Step 8: Disease Classification
**Process:**
1.  Forward embedding through classification head (Softmax output).
2.  Apply temperature scaling (τ=1.5) for calibrated confidence scores.
3.  If multi-view (multiple images of same plant): weighted average of predictions (Top: 0.5, Side: 0.3, Close-up: 0.2).
4.  Confidence thresholds: ≥ 0.6 auto-classify, < 0.6 flag for human review.
**Output:** Disease class prediction + calibrated confidence score.

### Step 9: Explainability — GradCAM Generation
**Rules Reference:** `rules/ml/RULES-gradcam-heatmap.md`.
**Process:**
1.  Generate GradCAM heatmap for predicted disease class.
2.  Suppress noise (activations < 0.2 set to zero).
3.  Create overlay visualization (0.4 heatmap + 0.6 original).
**Output:** Heatmap overlay image.

### Step 10: Quality Gate 4 — Explainability Validation
**Checks:**
*   GradCAM-Leaf Overlap (GLOR) ≥ 70%.
*   Background Activation Ratio (BAR) < 30%.
*   ROAD Score ≥ 0.3 (for production models, checked at deployment time).
**Fail Action:** Flag prediction for human review. Log ERR-HEAT-001. Do not suppress the prediction — present it with a quality warning.
**Pass Action:** Forward to Step 11.

### Step 11: Similarity Search
**Process:**
1.  Query vector DB with image embedding.
2.  Retrieve top-5 nearest neighbors with metadata.
3.  Filter by cosine similarity > 0.70 (discard low-quality matches).
4.  Cross-validate: do similar images agree with classification prediction?
**Output:** Top-5 similar historical images with disease labels and similarity scores.

### Step 12: Report Generation
**Output Format:** JSON report + visual summary.
**Contents:**
*   Original image(s).
*   Binary mask (best quality view).
*   GradCAM overlay.
*   Top-3 disease predictions with confidence scores.
*   Top-5 similar historical images.
*   Quality gate results (all pass/fail statuses).
*   Recommended treatment actions (if confidence ≥ 0.6).
*   Metadata: timestamp, model version, pipeline version, processing time.

### Step 13: Storage & Monitoring
**Actions:**
*   Store embedding in vector DB with full metadata.
*   Store report in document storage.
*   Log pipeline execution metrics (latency per step, quality gate results).
*   Feed into drift detection system (weekly centroid monitoring).
**Alerting:** If "Critical" disease detected (e.g., Late Blight), trigger SMS/Email alert.

## 4. Error Handling
*   All errors cataloged in `errors/ml/ERROR-multi-view-pipeline-catalog.md`.
*   Retry logic: max 3 retries for timeout errors, then fail gracefully.
*   Fallback chain: SAM2 → Adaptive Threshold → Otsu → Manual review.
*   Pipeline must never silently swallow errors — all failures must be logged with error code.

## 5. Processing Time Budget (Total Pipeline)

| Mode | Target (GPU) | Target (CPU) |
| :--- | :--- | :--- |
| **Real-time (1 image, center crop)** | 80ms | 800ms |
| **Standard (1 image, 10-crop TTA)** | 150ms | 1500ms |
| **High-accuracy (1 image, 30-crop)** | 400ms | 4000ms |
| **Multi-view (3 images, 10-crop each)** | 450ms | 4500ms |

## 6. Cross-References
*   **Master Rules**: `rules/ml/RULES-plant-disease-analysis.md`
*   **Binarization**: `rules/ml/RULES-image-binarization.md`
*   **Multi-Crop**: `rules/ml/RULES-multi-crop-augmentation.md`
*   **Embeddings**: `rules/ml/RULES-embedding-storage.md`
*   **GradCAM**: `rules/ml/RULES-gradcam-heatmap.md`
*   **Error Catalog**: `errors/ml/ERROR-multi-view-pipeline-catalog.md`
*   **Example**: `examples/ml/EXAMPLE-multi-view-plant-disease.md`
*   **Diagnosis Guide**: `knowledge/ml/GUIDE-plant-disease-diagnosis.md`
