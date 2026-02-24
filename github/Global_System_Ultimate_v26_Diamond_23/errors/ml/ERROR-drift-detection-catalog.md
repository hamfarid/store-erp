# Drift Detection Error Catalog (v26.0)

> **Scope**: Embedding Space & Model Performance Drift
> **Compliance**: Multi-View Plant Disease Detection
> **Referenced by**: `errors/DONT_MAKE_THESE_ERRORS_AGAIN.md` → FD-TZ-001
> **Version**: v26.0.0 (Diamond 6)

## Purpose

This catalog documents errors related to embedding drift, data distribution shift, and model performance degradation in the plant disease detection pipeline.

-----

## ERR-DRIFT-001: Centroid Shift Alert Not Firing

**Severity:** 🔴 Critical
**Symptoms:** Embedding distribution has changed significantly but no alert was triggered. Model accuracy has silently degraded in production.
**Root Cause:**

- Drift monitoring job failed silently (cron job not running).
- Threshold set too high (> 0.10 instead of 0.05).
- Centroid computed on stale data (cache not refreshed).

**Resolution:**
- Verify monitoring cron job is active and logging.
- Reset threshold to 0.05 (cosine distance between monthly centroids).
- Force centroid recalculation from live vector DB data.
- Add health check endpoint for drift monitoring service.

**Prevention:**
- Drift monitoring job must have a heartbeat check (alert if no log entry in 24h).
- Threshold: centroid shift > 0.05 over 30-day rolling window, calculated weekly.
- Store centroid history with timestamps for audit trail.

## ERR-DRIFT-002: False Positive Drift Alert (Seasonal Variation)

**Severity:** 🟡 Medium
**Symptoms:** Drift alert fires but model accuracy is unchanged. Alert caused by seasonal changes in plant appearance (e.g., summer vs winter leaf color).
**Root Cause:** Seasonal variation in healthy plant appearance shifts embedding centroids without actual disease distribution change.
**Resolution:**

- Compare drift metrics against per-season baselines (not annual average).
- Validate with accuracy check: if accuracy on recent data > threshold, suppress alert.

**Prevention:**
- Maintain seasonal centroid baselines (Spring, Summer, Autumn, Winter).
- Two-stage drift detection: centroid shift check → accuracy validation check.
- Only trigger retraining if BOTH centroid shift > 0.05 AND accuracy drop > 5%.

## ERR-DRIFT-003: New Disease Class Emergence

**Severity:** 🔴 Critical
**Symptoms:** Cluster of embeddings appears far from all known disease centroids. Model classifies these as low-confidence predictions across multiple classes.
**Root Cause:** New disease or pest has appeared that was not in the training data.
**Resolution:**

- Collect and label samples from the new cluster (minimum 20 samples).
- If < 5 samples: use embedding similarity search only (no classification).
- If 5-20 samples: use few-shot prototypical network classification.
- If > 20 samples: fine-tune model with new class added.
- Re-index vector DB with updated embeddings.

**Prevention:**
- Monitor “outlier ratio” weekly: percentage of predictions with max_confidence < 0.6.
- Alert if outlier ratio > 10% of weekly predictions.
- Maintain “unknown” class in the model to catch novel inputs.

## ERR-DRIFT-004: Embedding Dimension Mismatch After Model Update

**Severity:** 🔴 Critical
**Symptoms:** Vector DB queries return garbage results after model version update. Cosine similarity scores are nonsensical (all near 0 or all near 1).
**Root Cause:** New model version outputs different embedding dimensions (e.g., upgraded from ResNet50 2048d to DINOv2 768d) but vector DB collection was not re-indexed.
**Resolution:**

- Re-generate all embeddings with the new model.
- Create new collection in vector DB with correct dimensions.
- Migrate metadata from old collection to new collection.
- Validate: sample 100 known pairs and verify similarity scores are sensible.

**Prevention:**
- Embedding model version MUST be stored in collection metadata.
- Pre-deployment check: verify model output dimensions match DB collection schema.
- Never overwrite existing collection — create versioned collections (e.g., `diseases_v2`).

## ERR-DRIFT-005: Concept Drift in Feature Extraction

**Severity:** 🟠 High
**Symptoms:** Same disease images produce increasingly different feature vectors over time. GLCM texture features and LBP descriptors show distribution shift.
**Root Cause:**

- Camera/sensor change in the field (new phone model, different resolution).
- Environmental change (new greenhouse lighting, different growth medium).
- Preprocessing pipeline change (different resize interpolation, normalization).

**Resolution:**
- Identify which feature type drifted (embeddings vs texture vs color).
- If sensor change: add sensor normalization layer or recalibrate.
- If preprocessing change: revert to previous preprocessing or retrain on new pipeline.

**Prevention:**
- Log camera/sensor metadata with every image.
- Monitor feature distribution per sensor type independently.
- Standardize image capture protocol (resolution, lighting, distance).

## ERR-DRIFT-006: Retraining Loop (Drift → Retrain → Different Drift)

**Severity:** 🟠 High
**Symptoms:** Model is retrained after drift detection, but new model causes drift in a different disease class. Continuous retraining cycle without convergence.
**Root Cause:** Catastrophic forgetting — model forgets old classes when fine-tuned on new distribution. Replay buffer insufficient or not used.
**Resolution:**

- Use Experience Replay: always include 20% of original training data in retrain set.
- Use Elastic Weight Consolidation (EWC) to protect important weights.
- Validate ALL disease classes after retraining, not just the drifted class.

**Prevention:**
- Mandatory post-retrain validation: per-class accuracy must not drop > 3% for any class.
- Maintain a “golden test set” (100 images per class) that is never used for training.
- Maximum retraining frequency: once per month (prevent thrashing).

-----

## Drift Detection Configuration

### Monitoring Schedule

|Check                   |Frequency|Threshold                          |Action                       |
|:-----------------------|:--------|:----------------------------------|:----------------------------|
|**Centroid Shift**      |Weekly   |> 0.05 cosine distance             |Alert + accuracy check       |
|**Outlier Ratio**       |Weekly   |> 10% predictions < 0.6 confidence |Alert + investigate          |
|**Per-Class Accuracy**  |Weekly   |< 60% recall any class             |Alert + prioritize retraining|
|**Feature Distribution**|Monthly  |KS-test p < 0.01                   |Investigate sensor/pipeline  |
|**Embedding Coherence** |Monthly  |Intra-class variance increase > 20%|Alert + check data quality   |

### Drift-Adapter Pattern (Standard Response)

```
1. Alert fires (centroid shift > 0.05)
   ↓
2. Accuracy validation check (is accuracy actually degraded?)
   ├── NO (seasonal drift) → Suppress alert, log as seasonal baseline
   └── YES (real drift) → Continue
       ↓
3. Collect new samples from drifted distribution (minimum 50)
   ↓
4. Fine-tune model with Experience Replay (80% new + 20% original)
   ↓
5. Validate ALL classes (golden test set): no class drops > 3%
   ├── PASS → Deploy new model, re-index affected vectors
   └── FAIL → Rollback, investigate root cause, escalate
       ↓
6. Log drift event with before/after centroid positions
```

## Cross-References

- **Embedding Rules**: `rules/ml/RULES-embedding-storage.md` → Section 5
- **Master Rules**: `rules/ml/RULES-plant-disease-analysis.md` → Section 7
- **Parent Error File**: `errors/DONT_MAKE_THESE_ERRORS_AGAIN.md` → FD-TZ-001
