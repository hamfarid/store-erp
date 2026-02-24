# GUIDE-plant-disease-yolov8-onnx.md
# Governance: ML/AI Application Framework (Feb 2026)

## 1. Architecture: Dual-Model Pipeline

GAARA-AI Plant Doctor uses **two models in sequence**:

```
Image → YOLOv8n (Disease Detection) → DenseNet121 (Nutrient Deficiency)
  │            │                              │
  │     Bounding boxes +               9 nutrient classes
  │     26 disease classes             (N, P, K, Ca, Mg, Fe, Mn, Zn, B)
  │            │                              │
  └────────────┴──────────────────────────────┘
                      │
              LLM Report (Arabic) + Treatment DB
```

## 2. YOLOv8 Disease Detection

### 2.1 Model Selection
| Model | Size | mAP50 | Speed (CPU) | Speed (GPU) | Recommended |
|-------|------|-------|-------------|-------------|-------------|
| YOLOv8n | 6.3 MB | 95.2% | 120ms | 8ms | **✅ Production (CPU)** |
| YOLOv8s | 22.5 MB | 96.8% | 250ms | 12ms | GPU available |
| YOLOv8m | 52 MB | 97.5% | 500ms | 18ms | High accuracy needed |

**YOLOv8n** is the default — smallest, fastest, 95%+ accuracy on PlantVillage.

### 2.2 Dataset: PlantVillage
- **Images:** 54,306 (healthy + diseased)
- **Crops:** 14 (Tomato, Potato, Apple, Grape, Corn, etc.)
- **Diseases:** 26 classes
- **Split:** 70% train / 15% val / 15% test
- **Augmentation:** RandomFlip, RandomRotation(30°), ColorJitter, RandomCrop

### 2.3 Training
```python
from ultralytics import YOLO

model = YOLO("yolov8n.pt")  # Pretrained on COCO
results = model.train(
    data="plantvillage.yaml",
    epochs=100,
    imgsz=640,
    batch=16,
    patience=15,            # Early stopping
    device="0",             # GPU (or "cpu")
    augment=True,
    name="plant_disease_v1",
    project="runs/detect",
)
```

### 2.4 ONNX Export (Critical for CPU Production)
```python
# Export to ONNX — 2-5x faster on CPU than PyTorch
model = YOLO("runs/detect/plant_disease_v1/weights/best.pt")
model.export(
    format="onnx",
    dynamic=True,           # Dynamic batch size
    simplify=True,          # ONNX graph optimization
    opset=17,
    imgsz=640,
)
# Output: best.onnx (smaller + faster)
```

### 2.5 ONNX Inference
```python
import onnxruntime as ort
import numpy as np
import cv2

class PlantDiseaseDetector:
    def __init__(self, model_path="models/plant_disease.onnx"):
        self.session = ort.InferenceSession(
            model_path,
            providers=['CPUExecutionProvider']  # or CUDAExecutionProvider
        )
        self.input_name = self.session.get_inputs()[0].name
        self.classes = [...]  # 26 disease classes

    def preprocess(self, image_path):
        img = cv2.imread(image_path)
        img = cv2.resize(img, (640, 640))
        img = img.astype(np.float32) / 255.0
        img = np.transpose(img, (2, 0, 1))  # HWC → CHW
        return np.expand_dims(img, axis=0)   # Add batch dim

    def detect(self, image_path, confidence=0.5):
        input_tensor = self.preprocess(image_path)
        outputs = self.session.run(None, {self.input_name: input_tensor})

        detections = []
        for detection in self.parse_outputs(outputs[0]):
            if detection['confidence'] >= confidence:
                detections.append({
                    'disease': self.classes[detection['class_id']],
                    'confidence': float(detection['confidence']),
                    'bbox': detection['bbox'],
                })
        return detections
```

## 3. DenseNet121 Nutrient Deficiency

### 3.1 Model
- **Architecture:** DenseNet121 (pretrained ImageNet, fine-tuned)
- **Accuracy:** 98.6% on nutrient deficiency dataset
- **Classes (9):** Nitrogen(N), Phosphorus(P), Potassium(K), Calcium(Ca), Magnesium(Mg), Iron(Fe), Manganese(Mn), Zinc(Zn), Boron(B)
- **Input:** 224×224 RGB
- **Export:** ONNX for CPU inference

### 3.2 Training
```python
import torch
import torchvision.models as models

model = models.densenet121(pretrained=True)
model.classifier = torch.nn.Linear(1024, 9)  # 9 nutrient classes

# Fine-tune with frozen features
for param in model.features.parameters():
    param.requires_grad = False

# Train classifier head, then unfreeze last 2 dense blocks
```

### 3.3 ONNX Export
```python
dummy_input = torch.randn(1, 3, 224, 224)
torch.onnx.export(
    model, dummy_input, "models/nutrient_deficiency.onnx",
    opset_version=17,
    input_names=["image"],
    output_names=["prediction"],
    dynamic_axes={"image": {0: "batch"}, "prediction": {0: "batch"}}
)
```

## 4. Full Diagnosis Workflow

```python
async def diagnose(image_path, crop_type=None):
    # Step 1: Disease Detection (YOLOv8 ONNX)
    diseases = disease_detector.detect(image_path)

    # Step 2: Nutrient Deficiency (DenseNet121 ONNX)
    nutrients = nutrient_detector.predict(image_path)

    # Step 3: Generate Arabic Report (Ollama LLM)
    report = await llm.generate(
        prompt=f"أنت خبير أمراض نباتات. حلل النتائج التالية:\n"
               f"الأمراض: {diseases}\n"
               f"نقص العناصر: {nutrients}\n"
               f"المحصول: {crop_type}\n"
               f"اكتب تقريراً مفصلاً بالعربية مع توصيات العلاج."
    )

    # Step 4: Treatment Lookup
    treatments = treatment_db.lookup(diseases, nutrients, crop_type)

    # Step 5: Annotate Image
    annotated = annotate_image(image_path, diseases)

    return {
        "diseases": diseases,
        "nutrients": nutrients,
        "report_ar": report,
        "treatments": treatments,
        "annotated_image": annotated,
    }
```

## 5. Treatment Database Schema

```sql
CREATE TABLE treatments (
    id SERIAL PRIMARY KEY,
    disease_name VARCHAR(100),
    crop VARCHAR(50),
    severity VARCHAR(20),  -- low, medium, high
    chemical_treatment TEXT,
    organic_treatment TEXT,
    fertilizer_recommendation TEXT,
    prevention TEXT,
    notes_ar TEXT,
    notes_en TEXT
);
```

## 6. Performance Benchmarks (CPU — ONNX)

| Model | PyTorch (CPU) | ONNX (CPU) | Speedup |
|-------|--------------|------------|---------|
| YOLOv8n | 120ms | **45ms** | 2.7x |
| DenseNet121 | 80ms | **25ms** | 3.2x |
| Full Pipeline | 200ms | **70ms** | 2.9x |

**Conclusion:** ONNX export is mandatory for CPU-only deployment. GPU is optional but recommended for batch processing (>50 images).

## 7. Docker Service

```yaml
plant-doctor:
  build: ./services/plant-doctor
  container_name: gaara-plant-doctor
  volumes:
    - plant_data:/app/models
  environment:
    - DISEASE_MODEL=/app/models/plant_disease.onnx
    - NUTRIENT_MODEL=/app/models/nutrient_deficiency.onnx
    - CONFIDENCE_THRESHOLD=0.5
    - DEVICE=cpu  # or cuda
  ports:
    - "8001:8001"
```
