# Workflow: Multi-View Plant Disease Detection (v2026.2)

## 1. Overview
This workflow defines the end-to-end process for capturing, analyzing, and diagnosing plant diseases using multi-view imagery. It combines computer vision, vector search, and explainability.

### 1.1 Phases
1.  **Capture:** Acquire images from multiple angles (Top, Side, Leaf).
2.  **Preprocess:** Clean, crop, and segment the leaf.
3.  **Analyze:** Extract features and classify disease.
4.  **Retrieve:** Find similar historical cases.
5.  **Explain:** Generate heatmaps for validation.

## 2. Phase 1: Capture & Ingestion
**Goal:** High-quality input data.

### 2.1 Image Requirements
-   **Resolution:** > 1024x1024 (High Res).
-   **Format:** JPEG (Quality > 90) or PNG.
-   **Metadata:** GPS, Timestamp, Plant ID.

### 2.2 Validation Gate
-   **Check:** Is the image blurry? (Laplacian Variance < 100).
-   **Check:** Is the leaf visible? (Green pixel ratio > 10%).
-   **Action:** Reject upload if checks fail.

## 3. Phase 2: Preprocessing & Segmentation
**Goal:** Isolate the region of interest (ROI).

### 3.1 Binarization
-   **Method:** Otsu's Thresholding + HSV Masking.
-   **Output:** Binary Mask (0=Background, 1=Leaf).

### 3.2 Cropping
-   **Method:** Bounding Box of the largest contour.
-   **Padding:** Add 10% padding around the leaf.
-   **Resize:** Standardize to 224x224 pixels.

## 4. Phase 3: Analysis (Inference)
**Goal:** Detect disease type and severity.

### 4.1 Feature Extraction
-   **Model:** ResNet50 (Backbone).
-   **Output:** 2048-dimensional vector.

### 4.2 Classification
-   **Head:** Fully Connected Layer (2048 -> Num Classes).
-   **Output:** Probability distribution (Softmax).
-   **Threshold:** Confidence > 0.8 required for definitive diagnosis.

## 5. Phase 4: Retrieval (RAG for Images)
**Goal:** Provide context from historical data.

### 5.1 Vector Search
-   **Query:** Extracted feature vector.
-   **Database:** ChromaDB / Qdrant.
-   **Metric:** Cosine Similarity.
-   **Top-K:** Retrieve 5 most similar images.

### 5.2 Contextualization
-   **Output:** "This looks like Early Blight (95% match with Case #123 from 2024)."

## 6. Phase 5: Explanation & Reporting
**Goal:** Build trust with the agronomist.

### 6.1 Heatmap Generation
-   **Method:** Grad-CAM on the last convolutional layer.
-   **Overlay:** Superimpose heatmap on original image.
-   **Check:** Does the heatmap highlight the lesion?

### 6.2 Report Generation
-   **Format:** PDF / JSON.
-   **Content:** Diagnosis, Confidence, Similar Cases, Heatmap, Treatment Recommendation.

## 7. Operational Monitoring
**Goal:** Ensure system health.

### 7.1 Metrics
-   **Latency:** End-to-end processing time (< 2s).
-   **Accuracy:** Feedback loop from expert agronomists.
-   **Drift:** Monitor embedding distribution shift.

### 7.2 Alerts
-   **P1:** Inference failure rate > 1%.
-   **P2:** Average confidence score < 0.6 (Model unsure).
