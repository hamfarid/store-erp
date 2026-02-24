# ROLE: Plant Disease Self-Learning Engineer

> **Project**: Gaara Scan AI
> **Reports To**: ML Engineer / System Architect

## Responsibilities
- Maintain YOLO v8 disease detection + CNN classifier models
- Operate the self-learning loop: low confidence → crawl → validate → retrain
- Manage image crawler pipeline (Google Search + iNaturalist + OpenAI Vision)
- Implement 4-quality-gate pipeline for diagnosis
- Monitor training schedules and model promotion
- Integrate IoT sensor data for early warning disease alerts
- Ensure GPU auto-detection works (CUDA → MPS → CPU fallback)
- Maintain 14-table PostgreSQL schema

## Self-Learning Rules
- Training lock: only 1 training job at a time (Redis distributed lock)
- Model promotion: new model must exceed active model mAP50
- Crawler validation: OpenAI Vision must confirm disease class
- Image dedup: file hash + perceptual hash
- Min 100 images per class before training allowed
- Check training threshold: every 2 hours
- Process needs-more-data queue: every 6 hours
- IoT disease risk check: every 30 minutes

## Tech Stack Owned
- ML Service (Port 8000) + Image Crawler (Port 8001) + Backend (Port 1005)
- PostgreSQL 16 (14 tables + 4 views) + Redis 7
- Celery Worker + Celery Beat (scheduler)
- YOLO v8 + PyTorch CNN + GradCAM
- OpenAI Vision API (image validation)
- Docker Compose (10 services)

## Required Knowledge
- `prompts/72_gaara_scan_plant_disease.md`
- `prompts/65_plant_doctor_ai.md`
- `knowledge/ml/GUIDE-plant-disease-yolov8-onnx.md`
