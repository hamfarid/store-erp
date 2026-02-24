# Prompt 72: Gaara Scan AI — Plant Disease Self-Learning System

> **Scope**: Autonomous plant disease detection with self-learning pipeline
> **When to Load**: Any Gaara Scan work

## System Architecture

Gaara Scan AI is a standalone plant disease detection system with an autonomous self-learning loop.

### Services (10 Docker containers)
| Service | Port | Role |
|:--------|:-----|:-----|
| ML Service | 8000 | YOLO v8 + CNN + GradCAM inference |
| Image Crawler | 8001 | Google Search + iNaturalist + OpenAI Vision validation |
| FastAPI Backend | 1005 | Main API |
| React Frontend | 1505 | User interface |
| Celery Worker | — | Background training + crawler jobs |
| Celery Beat | — | Scheduled tasks |
| PostgreSQL 16 | 5432 | 14 tables + 4 views |
| Redis 7 | 6379 | Cache + Celery broker |
| Nginx | 80/443 | Reverse proxy |

### Database Schema (14 Tables)
| Table | Purpose |
|:------|:--------|
| images | Image catalog (file_path, disease_class, quality_score) |
| disease_classes | Disease definitions (name, name_ar, treatment, favorable conditions) |
| model_versions | Model artifacts (type, version, mAP50, precision, recall) |
| training_sessions | Training runs (duration, epochs, dataset split) |
| training_metrics | Per-epoch metrics (loss, accuracy, mAP) |
| model_comparison | Model A vs B comparison results |
| crawler_jobs | Crawl job tracking (disease, images found/accepted/rejected) |
| crawler_images | Individual crawled images (url, hash, OpenAI validation) |
| quality_gate_results | 4-gate quality pipeline results |
| diagnosis_results | Diagnosis outputs (YOLO bbox, CNN class, GradCAM path) |
| needs_more_data | Self-learning trigger queue |
| iot_sensor_data | IoT sensor readings (temp, humidity, soil moisture) |
| disease_alerts | Early warning alerts |
| training_schedule | Auto-training configuration |

### Self-Learning Pipeline
```
Low Confidence Diagnosis (<70%)
    → Insert into needs_more_data queue
    → Celery Beat checks every 6 hours
    → Trigger Crawler: search Google + iNaturalist for disease images
    → OpenAI Vision validates each image (is it really this disease?)
    → Accepted images → training data folder
    → When threshold reached (50+ new images per class)
    → Auto-trigger training (YOLO or CNN)
    → Compare new model vs active model
    → If better → promote to active
    → If worse → discard and log
```

### GPU Auto-Detection
```python
detect_device() → CUDA GPU → Apple MPS → CPU (fallback)
# CPU mode: inference ~100-500ms per image (still functional)
# GPU mode: inference ~10-50ms per image
```

### Quality Gates (4-stage)
1. **Gate 1**: Image quality (resolution, blur, lighting)
2. **Gate 2**: YOLO detection (confidence threshold)
3. **Gate 3**: CNN classification (top-1 confidence)
4. **Gate 4**: Cross-validation (YOLO vs CNN agreement)

### IoT Integration
- Sensor data: temperature, humidity, soil moisture, light
- Disease risk calculation based on environmental conditions
- Early warning alerts when conditions favor specific diseases
- Checks every 30 minutes via Celery Beat

## Rules
- Training lock: only one training job at a time (Redis distributed lock)
- Model promotion: new model must exceed active model mAP50
- Crawler validation: OpenAI Vision must confirm disease class
- Image dedup: file hash + perceptual hash (imagehash)
- Min 100 images per class before training allowed
