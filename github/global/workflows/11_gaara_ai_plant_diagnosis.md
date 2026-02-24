# Workflow 11: Plant Doctor Diagnosis Pipeline

> **Trigger**: User uploads plant image via API or Django Plant Doctor page
> **Modules Involved**: API Gateway → Plant Doctor → LLM → Treatment DB → Django ERP

## Steps

### Step 1: Image Upload & Preprocessing
- Gateway receives image (max 10MB, JPEG/PNG)
- Validate format and dimensions
- Send to Plant Doctor service as Celery task (plant_diagnosis queue)

### Step 2: Disease Detection (YOLOv8n ONNX)
- Preprocess: resize 640x640, normalize 0-1
- Run YOLOv8n inference via ONNX Runtime
- Output: disease name, confidence %, bounding box coordinates, severity level

### Step 3: Nutrient Deficiency Analysis (DenseNet121 ONNX)
- Run DenseNet121 inference on same image
- Output: nutrient status per element (N, P, K, Ca, Mg, Fe, Mn, Zn)
- Classification: normal / mild deficiency / severe deficiency

### Step 4: Treatment Lookup
- Query treatment database with detected disease
- Return: recommended treatment, fertilizer, dosage, application method

### Step 5: Arabic Diagnosis Generation
- Send all results to Ollama LLM (Qwen2.5:7b):
  - "Generate a professional Arabic diagnosis report for: {disease}, {nutrients}"
- LLM returns human-readable Arabic report

### Step 6: Save & Respond
- Annotate original image with bounding boxes (OpenCV)
- Save to Django ERP (AIDiagnosis model: image, diagnosis, treatment, date)
- Return: annotated image + diagnosis report + treatment plan
- Optional: trigger Avatar service to present results as video

## Drift Monitoring
- Every diagnosis is logged with prediction distribution
- Daily at 2 AM: Evidently AI compares recent predictions vs training baseline
- Alert if drift score > 0.3
