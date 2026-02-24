# Workflow 17: Gaara Scan — Auto-Training Pipeline

> **Trigger**: Celery Beat (every 2h threshold check) or manual
> **System**: Gaara Scan AI — Self-Learning Loop

## Steps

### Step 1: Check Training Threshold
- Celery Beat runs `check_training_threshold` every 2 hours
- Query `v_disease_image_counts` view
- For each disease class: validated_images >= min_images_for_training?
- If yes for any class → proceed to Step 2

### Step 2: Acquire Training Lock
- Attempt Redis distributed lock: `training_lock:{model_type}`
- Lock timeout: 4 hours (14400 seconds)
- If lock busy → skip (another training in progress)
- If acquired → proceed

### Step 3: Prepare Dataset
- Collect all validated images for the disease class
- Split: 80% train / 10% validation / 10% test
- Apply augmentations: flip, rotate, brightness, crop

### Step 4: Train Model
- For YOLO: train YOLOv8 with current dataset
- For CNN: train classifier with current dataset
- Track per-epoch metrics: loss, accuracy, mAP
- Store metrics in training_metrics table

### Step 5: Model Comparison
- Evaluate new model on test set
- Compare mAP50, precision, recall vs active model
- Store comparison in model_comparison table

### Step 6: Promotion Decision
- If new model mAP50 > active model mAP50:
  - Promote new model → set is_active=true
  - Archive old model → set is_active=false
  - Log: "Model promoted: v{new} > v{old}"
- If worse:
  - Discard new model artifact
  - Log: "Model rejected: v{new} < v{old}"

### Step 7: Release Lock & Notify
- Release Redis training lock
- Update training_schedule.last_run_at
- Send notification to admin
