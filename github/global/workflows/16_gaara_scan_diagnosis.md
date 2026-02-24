# Workflow 16: Gaara Scan — Plant Disease Diagnosis Pipeline

> **Trigger**: User uploads plant image
> **System**: Gaara Scan AI (10 Docker services)

## Steps

### Step 1: Image Upload
- User uploads image via React Frontend (Port 1505)
- Frontend → Backend (Port 1005) → ML Service (Port 8000)

### Step 2: Quality Gate 1 — Image Quality
- Check resolution (min 224x224)
- Check blur score (Laplacian variance)
- Check lighting (brightness histogram)
- If fails → return error with improvement suggestions

### Step 3: Quality Gate 2 — YOLO v8 Detection
- Run YOLOv8 inference (GPU or CPU via auto-detect)
- Output: disease name, confidence, bounding box
- If confidence < threshold → flag for review

### Step 4: Quality Gate 3 — CNN Classification
- Run CNN classifier on cropped region
- Output: disease class, top-5 probabilities
- Generate GradCAM visualization (attention map)

### Step 5: Quality Gate 4 — Cross-Validation
- Compare YOLO detection vs CNN classification
- If both agree → high confidence diagnosis
- If disagree → flag for expert review

### Step 6: Treatment Lookup
- Query disease_classes table for treatment
- Include: favorable conditions (temp, humidity ranges)
- Return Arabic + English treatment description

### Step 7: Self-Learning Trigger
- If overall confidence < 70%:
  - Insert into needs_more_data queue
  - Will trigger crawler in next cycle (every 6h)

### Step 8: Response
- Return: annotated image (bounding boxes) + GradCAM
- Diagnosis report + treatment + similar cases
- Processing time tracked in system_metrics
