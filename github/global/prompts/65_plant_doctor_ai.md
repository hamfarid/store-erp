# Prompt 65: Plant Doctor AI — Disease Detection & Nutrient Analysis

> **Scope**: Plant disease detection (YOLOv8) + nutrient deficiency (DenseNet121)
> **Container**: gaara-plant-doctor (port 8001)

## Dual Model Architecture

### Model 1: Disease Detection — YOLOv8n
- **Task**: Detect plant diseases with bounding boxes
- **Input**: Plant leaf/stem image
- **Output**: Disease name, confidence, bounding box, severity
- **Format**: ONNX (CPU-first, 2-5x faster than PyTorch)
- **Training Data**: PlantVillage (54,306 images, 14 crops, 26 diseases)

### Model 2: Nutrient Deficiency — DenseNet121
- **Task**: Classify nutrient deficiency status
- **Input**: Plant leaf image
- **Output**: Status per nutrient (N, P, K, Ca, Mg, Fe, Mn, Zn)
- **Format**: ONNX
- **Training Data**: Banana Nutrient (Mendeley), Rice Nutrient (Roboflow), Coffee Leaf (CoLeaf)

## Diagnosis Pipeline
```
Upload Image
  → OpenCV preprocessing (resize 640x640, normalize)
  → YOLOv8n ONNX (disease detection + bounding boxes)
  + DenseNet121 ONNX (nutrient classification)
  → Treatment DB lookup (treatment + fertilizer + dosage)
  → Ollama LLM (generate human-readable diagnosis in Arabic)
  → Save to Django ERP (AIDiagnosis model)
  → Return annotated image + full report
```

## Service Structure
```
services/plant-doctor/
├── Dockerfile
├── requirements.txt
├── main.py                  # FastAPI app
├── doctor.py                # GAARAPlantDoctor main class
├── disease_detector.py      # YOLOv8 engine
├── nutrient_analyzer.py     # DenseNet121 engine
├── treatment_db.py          # Treatment + fertilizer DB
├── preprocessing.py         # Image preprocessing
└── models/                  # Pre-trained ONNX weights
```

## Rules
- Always use ONNX Runtime for inference (`onnxruntime.InferenceSession`)
- Image preprocessing: resize to 640x640, normalize 0-1
- Batch diagnosis via Celery task (not blocking API)
- Treatment recommendations must include dosage + application method
- All diagnoses saved to PostgreSQL for drift detection
