# Multi-View Plant Disease Analysis Governance Rules (v26.0)

> **Scope**: End-to-End Plant Disease Detection Pipeline
> **Compliance**: Global System Ultimate v26 Diamond 2
> **Version**: 26.0.0

## 1. Tool Version Pinning & Licensing
**CRITICAL**: AI agents must generate code against these EXACT versions to prevent silent failures.

| Library | Version | Critical Note |
| :--- | :--- | :--- |
| **PyTorch** | 2.10.0 | Requires Python ≥3.10 |
| **torchvision** | 0.25.0 | Aligned with PyTorch 2.10 |
| **AlbumentationsX** | 2.0.14 | **WARNING**: AGPL-3.0 / Commercial Dual License. Must verify license. |
| **TIMM** | 1.0.24 | Supports DINOv3, NaFlexViT |
| **OpenCV** | 4.13.0.92 | `opencv-python` package |
| **scikit-image** | 0.26.0 | Use `graycomatrix` (NOT `greycomatrix`) |
| **ChromaDB** | 1.5.0 | For dev/prototyping (<500K vectors) |
| **Qdrant** | 1.16.x | For production (<5M vectors) |
| **Milvus** | 2.6.10 | For enterprise (>5M vectors) |
| **SAM2** | 2.1.x | Meta’s Segment Anything Model 2 |
| **Albumentations** | 2.0.14 | Augmentation pipeline |

## 2. Crop Strategy Decision Matrix
Select strategy based on input context:

| Scenario | Strategy | Min Crops | Notes |
| :--- | :--- | :--- | :--- |
| **Lab (Single Leaf)** | TTA (Flip + Rotation) | 2 | Image well-framed |
| **Field (Single Leaf)** | 10-crop + TTA | 10 | Handle positional variance |
| **Whole Plant** | Sliding Window | Dependent | ≥50% overlap |
| **Real-time Mobile** | Center Crop | 1 | Speed priority |
| **Production Eval** | 10-crop + Multi-scale | 10-18 | Maximize accuracy |

## 3. Image Binarization & Thresholding
**Pipeline Order (INVIOLABLE):**
1.  Color Space Conversion (RGB -> HSV/Lab)
2.  Channel Selection
3.  Thresholding
4.  Morphological Cleanup
5.  Connected Component Analysis
6.  Feature Extraction

**Vegetation Indices Preference:**
1.  **ExGR**: `(2*G - R - B) - (1.4*R - G)` (Zero threshold)
2.  **ExG**: `2*G - R - B` (Otsu threshold)
3.  **NGRDI**: `(G-R)/(G+R)`

**HSV Ranges (OpenCV Scale H:0-180, S:0-255, V:0-255):**
*   **Healthy Green**: H=35-85, S=40-255, V=40-255
*   **Chlorosis (Yellowing)**: H=20-35, S=50-255, V=50-255
*   **Necrosis (Brown/Dead)**: H=10-20, S=50-200, V=20-150
*   **Powdery Mildew (White)**: H=0-180, S=0-30, V=200-255
*   **Rust (Orange)**: H=10-25, S=150-255, V=100-255

**SAM2 vs Otsu Decision Tree:**
*   **Use Otsu when**: single leaf on uniform background, lab conditions, speed priority (<5ms).
*   **Use Adaptive Threshold when**: field images, uneven lighting, mixed backgrounds.
*   **Use SAM2 when**: complex scenes, multiple overlapping leaves, accuracy priority, GPU available (~200ms).

## 4. Morphological Operation Limits
**HARD LIMITS (Never Exceed):**
*   **Maximum Kernel Size**: 15×15 pixels. Larger kernels destroy fine lesion details.
*   **Maximum Iterations**: 5 per operation. More iterations merge distinct lesions.
*   **Kernel Shape**: Elliptical (`MORPH_ELLIPSE`) default. Rectangular only for grid patterns.

**Standard Pipeline:**
*   **Opening (noise removal)**: `kernel=(3,3)`, `iterations=1`
*   **Closing (hole filling)**: `kernel=(5,5)`, `iterations=2`

## 5. Quality Gates (Binary Mask Validation)
| Metric | Min | Max | Action on Failure |
| :--- | :--- | :--- | :--- |
| **Foreground Ratio** | 5% | 60% | Reject image (empty or occluded) |
| **Contour Count** | 1 | 50 | Reject (noisy segmentation) |
| **Min Contour Area** | 100 px² | — | Filter out noise contours |
| **Aspect Ratio** | 0.2 | 5.0 | Flag unusual leaf shape |

## 6. Feature Extraction Standards
*   **GradCAM**: Target last convolutional layer. Validation: ≥70% of top activations must overlap with leaf region (see `rules/ml/RULES-gradcam-heatmap.md`).
*   **ROAD Metric**: Remove top 20% activated pixels → re-classify. Confidence must drop ≥50%. ROAD score ≥0.3 required.
*   **TIMM**: Use `features_only=True`. Extract from at least 3 scales (early, mid, late).
*   **Texture (GLCM)**: `distances=[1, 3, 5]`, `angles=[0, π/4, π/2, 3π/4]`.
*   **Texture (LBP)**: `radius=3`, `n_points=24`, `method='uniform'`.

## 7. Embedding & Vector DB Governance
*   **Primary Model**: DINOv2 ViT-B/14 (768d).
*   **Normalization**: L2-normalize ALL embeddings before storage.
*   **Distance Metric**: Cosine Similarity.

**Similarity Thresholds:**
*   **Same-disease match**: cosine similarity > 0.85
*   **Different-disease separation**: cosine similarity < 0.70
*   **Drift alert**: centroid shift > 0.05 over 30-day window

**Database Selection:**
*   **ChromaDB**: < 500K vectors (dev/prototyping).
*   **Qdrant**: < 5M vectors (Filtered HNSW, production).
*   **Milvus**: > 5M vectors (IVF_RABITQ, enterprise).

## 8. Dual-Head Architecture Rules
When using classification + similarity simultaneously:
*   **Classification Head**: Softmax output for disease prediction. Temperature scaling τ=1.5 for calibration.
*   **Embedding Head**: L2-normalized feature vector for similarity search.
*   **Loss Function**: Joint loss = CrossEntropy + 0.5 × TripletMarginLoss(margin=0.3).
*   **Training**: Freeze backbone for first 5 epochs, then fine-tune with lr=1e-5.

## 9. Few-Shot Learning Benchmarks
For new/rare diseases with limited samples:
*   **Minimum samples**: 5 per class (5-shot learning).
*   **Method**: Prototypical Networks with DINOv2 backbone.
*   **Expected accuracy**: ≥75% with 5-shot, ≥85% with 20-shot.
*   **Fallback**: If <5 samples, use embedding similarity search only (no classification).

## 10. Processing Budget Constraints
| Stage | Time Budget (GPU) | Time Budget (CPU) | Memory Budget |
| :--- | :--- | :--- | :--- |
| **Image Loading** | 5ms | 10ms | 5-12 MB/image |
| **Binarization** | 3ms | 15ms | 2× image size |
| **Multi-Crop (10)** | 20ms | 100ms | 10× crop size |
| **Feature Extraction** | 50ms | 500ms | Model-dependent |
| **Embedding Generation** | 30ms | 300ms | 768d × float32 |
| **Total Pipeline** | **80-150ms** | **800-1500ms** | **≤500MB GPU** |

## 11. Cross-References
*   **Binarization Details**: `rules/ml/RULES-image-binarization.md`
*   **Embedding Storage**: `rules/ml/RULES-embedding-storage.md`
*   **GradCAM Validation**: `rules/ml/RULES-gradcam-heatmap.md`
*   **Crop Augmentation**: `rules/ml/RULES-multi-crop-augmentation.md`
*   **Error Catalog**: `errors/ml/ERROR-multi-view-pipeline-catalog.md`
*   **Workflow**: `workflows/ml/ML_MULTI_VIEW_WORKFLOW.md`
*   **Example**: `examples/ml/EXAMPLE-multi-view-plant-disease.md`
