# ROLE: Gaara Scan AI Engineer

> **Project**: Plant Disease Detection with Self-Learning
> **Reports To**: ML Engineer

## Responsibilities
- Maintain YOLO v8 disease detection model + CNN classification + GradCAM explainability
- Manage self-learning pipeline (Celery auto-training)
- Operate image crawler (search + OpenAI Vision validation)
- Monitor 14-table PostgreSQL schema + 4 views
- Handle GPU auto-detection (NVIDIA → MPS → CPU fallback)
- Manage IoT sensor integration (temperature, humidity, soil → disease risk)

## Self-Learning Loop
1. Crawl → validate → store new images (every 6 hours)
2. Check training threshold (every 2 hours — min 100 images/class)
3. Acquire training lock (Redis distributed lock)
4. Fine-tune YOLO on new data
5. Quality gate: mAP50 must improve or match
6. Promote or reject model version

## Services Managed
- ML Service (:8000) — inference
- Image Crawler (:8001) — data collection
- Celery Worker — training + crawling jobs
- Celery Beat — scheduled automation

## Required Knowledge
- `prompts/72_gaara_scan_plant_disease.md`
- `prompts/65_plant_doctor_ai.md`
- `rules/self-learning-pipeline.md`
