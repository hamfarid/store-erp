# Example: Gaara Scan AI — Self-Learning Loop

> **Purpose**: How the system automatically improves itself

## Trigger: Low Confidence Diagnosis
```
User uploads plant image
    → YOLO v8: detects "early_blight" at 55% confidence
    → CNN: classifies "early_blight" at 62% confidence
    → Gate 4: YOLO+CNN agree but low confidence
    → System: diagnosis marked as "low_confidence"
    → Insert into needs_more_data queue:
        disease_class="early_blight", confidence=0.55
```

## Step 1: Celery Beat Triggers (Every 6h)
```
tasks.process_needs_more_data()
    → Query needs_more_data WHERE status='pending'
    → Group by disease_class
    → For each disease with pending items:
        → Check current image count vs min_images_for_training
        → If below threshold → trigger crawler
```

## Step 2: Image Crawler
```
tasks.crawl_images(disease="early_blight", max_images=50)
    → Search queries:
        "early blight plant disease leaf symptoms"
        "early blight crop disease close up photo"
        "النبات مرض أعراض early blight"
    → Sources: Google Custom Search + iNaturalist
    → Download images → dedup (file hash + perceptual hash)
    → Save to crawled/ directory
```

## Step 3: OpenAI Vision Validation
```
For each crawled image:
    → Send to OpenAI Vision API:
        "Is this image showing early blight on a plant leaf?
         Answer: YES or NO with confidence"
    → If YES (confidence > 80%):
        → Move to validated/ directory
        → Mark as accepted in crawler_images table
    → If NO:
        → Delete image
        → Mark as rejected
```

## Step 4: Training Threshold Check (Every 2h)
```
tasks.check_training_threshold()
    → Query v_disease_image_counts view
    → If validated_images >= min_images_for_training (100):
        → Acquire training lock (Redis)
        → Trigger tasks.train_model(model_type="yolo")
```

## Step 5: Training + Model Comparison
```
tasks.train_model(model_type="yolo")
    → Train new YOLO v8 on all validated images
    → Evaluate on held-out test set
    → Compare mAP50 vs active model:
        New model mAP50: 0.89
        Active model mAP50: 0.85
        → New model wins → promote to active
    → Release training lock
```
