# Rule: Self-Learning Pipeline Standards

> **Applies To**: Gaara Scan AI, any autonomous learning system

## Trigger Conditions
1. **Low Confidence**: Diagnosis confidence < 70% → add to needs_more_data queue
2. **Threshold Reached**: 50+ new validated images per class → trigger training
3. **Scheduled**: Celery Beat checks every 2 hours (training threshold) + every 6 hours (needs-more-data)

## Image Crawler Pipeline
1. Search: Google Custom Search API + iNaturalist API (fallback)
2. Download: with dedup (file hash + perceptual hash via imagehash)
3. Validate: OpenAI Vision API confirms disease class
4. Accept/Reject: only validated images enter training data
5. Rate limits: respect robots.txt, 2 req/sec per domain

## Training Rules
1. **Training Lock**: Only 1 training job at a time (Redis distributed lock, 4hr timeout)
2. **Minimum Data**: 100 images per class before training allowed
3. **Model Comparison**: New model MUST exceed active model mAP50
4. **Promotion**: If better → promote to active + archive old
5. **Rejection**: If worse → discard new model + log reason
6. **Time Limit**: soft 2hr, hard 4hr per training session

## Quality Gates (4-Stage)
| Gate | Check | Threshold |
|:-----|:------|:----------|
| 1 | Image quality (resolution, blur, lighting) | Score > 0.5 |
| 2 | YOLO detection confidence | > 0.5 |
| 3 | CNN classification confidence | > 0.5 |
| 4 | YOLO vs CNN agreement | Classes match |

## IoT Integration
- Sensor readings: temperature, humidity, soil moisture, light
- Disease risk = f(sensor conditions vs disease favorable ranges)
- Check every 30 minutes
- Alert if risk > threshold for any disease
