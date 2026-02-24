# Guide: Gaara Scan AI — Infrastructure Reference

> **Source**: gaara-scan-infra.tar (February 2026)

## Docker Services (10 containers)

| Service | Container | Port | Image/Build | Memory |
|:--------|:----------|:-----|:------------|:-------|
| ML Service | gaara-ml-service | 8000 | Dockerfile.ml-service | 4G limit / 2G reserved |
| Image Crawler | gaara-crawler | 8001 | Dockerfile.crawler | 2G limit |
| Backend | gaara-backend | 1005 | Dockerfile.backend | — |
| Frontend | gaara-frontend | 1505 | Dockerfile (React) | — |
| Celery Worker | gaara-celery-worker | — | Dockerfile.ml-service | 6G limit / 3G reserved |
| Celery Beat | gaara-celery-beat | — | Dockerfile.ml-service | — |
| PostgreSQL | gaara-postgres | 5432 | postgres:16-alpine | — |
| Redis | gaara-redis | 6379 | redis:7-alpine | 256MB maxmemory |
| Nginx | gaara-nginx | 80/443 | nginx:alpine | — |

## Docker Volumes (10)
pg-data, redis-data, model-data, training-data, image-uploads, crawled-images, validated-images, ml-logs, crawler-logs, celery-beat-data

## GPU Override (docker-compose.gpu.yml)
```yaml
services:
  ml-service:
    deploy:
      resources:
        reservations:
          devices:
            - driver: nvidia
              count: 1
              capabilities: [gpu]
    environment:
      NVIDIA_VISIBLE_DEVICES: all
  celery-worker:
    deploy:
      resources:
        reservations:
          devices:
            - driver: nvidia
              count: 1
              capabilities: [gpu]
```

## Environment Variables (.env.example)
- DB_PASSWORD — PostgreSQL password
- REDIS_PASSWORD — Redis password
- OPENAI_API_KEY — For crawler image validation
- GOOGLE_SEARCH_API_KEY — For image search
- GOOGLE_SEARCH_CX — Search engine ID
- JWT_SECRET — Backend JWT signing

## Model Manager — GPU Auto-Detection
```
detect_device() flow:
    1. torch.cuda.is_available() → CUDA GPU (fastest)
    2. torch.backends.mps.is_available() → Apple MPS
    3. fallback → CPU (still functional, 100-500ms/image)
```
Models loaded at startup:
- YOLO: yolo_plant_disease.pt (or yolov8n.pt fallback)
- CNN: cnn_classifier.pt

## Celery Configuration
- Broker: Redis DB 1 (redis://redis:6379/1)
- Backend: Redis DB 2 (redis://redis:6379/2)
- Queues: training, crawler, default
- Concurrency: 1 (due to GPU memory constraints)
- Max tasks per child: 5 (memory leak prevention)
- Timezone: UTC
- Beat Schedule:
  - check_training_threshold: every 2 hours
  - process_needs_more_data: every 6 hours
  - update_image_counts: daily at 1 AM
  - iot_disease_risk: every 30 minutes

## Database Schema Summary
14 tables + 4 views in PostgreSQL 16:
- Core: images, disease_classes, model_versions
- Training: training_sessions, training_metrics, model_comparison
- Crawler: crawler_jobs, crawler_images
- Diagnosis: quality_gate_results, diagnosis_results
- Self-Learning: needs_more_data, training_schedule
- IoT: iot_sensor_data, disease_alerts
- System: system_metrics
- Views: v_disease_image_counts, v_quality_gate_stats, v_active_models, v_crawler_summary
