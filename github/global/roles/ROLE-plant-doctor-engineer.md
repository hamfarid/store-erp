# ROLE: Plant Doctor AI Engineer

> **Module**: Plant Doctor (gaara-plant-doctor:8001)
> **Reports To**: ML Engineer

## Responsibilities
- Train and maintain YOLOv8n disease detection model (ONNX)
- Train and maintain DenseNet121 nutrient deficiency model (ONNX)
- Manage treatment database (disease → treatment + fertilizer + dosage)
- Implement OpenCV preprocessing pipeline
- Export all models to ONNX for CPU inference (2-5x speedup)
- Monitor model drift via Evidently AI

## Datasets
- PlantVillage: 54,306 images (14 crops, 26 diseases)
- Banana Nutrient (Mendeley): 8 nutrients
- Rice Nutrient (Roboflow): N, P, K, Fe, Mg
- Coffee Leaf (CoLeaf): nutritional deficiencies

## Standards
- ONNX Runtime for all inference (never raw PyTorch in production)
- Image preprocessing: resize 640x640, normalize 0-1
- Batch diagnosis via Celery task
- All diagnoses saved to PostgreSQL for drift tracking

## Required Knowledge
- `prompts/65_plant_doctor_ai.md`
- `knowledge/ml/GUIDE-plant-disease-yolov8-onnx.md`
- `rules/ml/RULES-plant-disease-analysis.md`
