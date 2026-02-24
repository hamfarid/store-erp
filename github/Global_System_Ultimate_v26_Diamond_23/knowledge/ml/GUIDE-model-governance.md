# Guide: ML Model Governance (v26.0)

> **Scope**: Model Lifecycle Management
> **Audience**: Data Scientists, ML Engineers, Governance Agents
> **Version**: v26.0.0 (Diamond 8)

## 1. Purpose

This guide defines the governance framework for all machine learning models in the plant disease detection pipeline — from initial development through production deployment, monitoring, and retirement.

## 2. Model Lifecycle Stages

### 2.1 Development
- All experiments must be tracked in MLflow/W&B with reproducible configurations.
- Every experiment requires: hypothesis, evaluation criteria, and success threshold defined BEFORE training.
- Tool versions must be pinned per `rules/ml/RULES-plant-disease-analysis.md` Section 1.
- Training data must be split by specimen ID (not image) to prevent data leakage.
- Augmentation must respect disease-safe limits per `rules/ml/RULES-multi-crop-augmentation.md`.

### 2.2 Evaluation
- **Minimum metrics**: Per-class F1 score, confusion matrix, GradCAM validation on 50 samples.
- **Quality gates**: ROAD score ≥ 0.3, BAR < 30%, per-class recall ≥ 60%, GradCAM-Leaf overlap ≥ 70%.
- **Comparison**: New model must outperform current production model on the golden test set.
- **Bias check**: Evaluate performance across different plant species, capture conditions (lab vs field), and camera types.

### 2.3 Staging
- Model deployed to staging environment with production-like data.
- A/B test against current production model for minimum 7 days.
- **Monitor**: inference latency, error rate, prediction distribution, embedding coherence.
- **Approval required from**: Data Scientist (technical), Reviewer Agent (code), Governance Agent (compliance).

### 2.4 Production
- Model served with version tag in metadata.
- Rollback plan documented and tested (< 5 minutes to previous version).
- **Monitoring**: per-class accuracy (weekly), drift detection (weekly), latency (continuous).
- **Alerts**: accuracy drop > 5%, centroid shift > 0.05, latency > 2× baseline.

### 2.5 Retirement
- Model deprecated when replaced by successor that passes all quality gates.
- Deprecated model kept available for 90 days for comparison and audit.
- All associated embeddings in vector DB migrated to successor model’s space.
- Retirement logged with reason and successor model reference.

## 3. Model Registry

Every production model must have a registry entry containing:
- Model name and version (semantic versioning: MAJOR.MINOR.PATCH).
- Training dataset version and size.
- Architecture description and hyperparameters.
- Evaluation metrics (per-class and aggregate).
- Quality gate pass/fail status.
- Deployment date and environment.
- Owner (Data Scientist responsible).

## 4. Retraining Policy

- **Scheduled**: Quarterly retraining with latest data (minimum).
- **Triggered**: When drift detection alerts fire AND accuracy validation confirms degradation.
- **Emergency**: When new disease class emerges with > 20 confirmed samples.
- **Constraints**: Maximum 1 retraining per month (prevent thrashing). Use Experience Replay (80% new + 20% original data).

## 5. Audit Trail

- All model decisions must be traceable: input image → preprocessing → model version → prediction → confidence → explanation (GradCAM).
- Audit logs retained for minimum 1 year.
- Random sample of 100 predictions per week reviewed by human expert for quality assurance.

## 6. Cross-References
- **Quality Gates**: `rules/ml/RULES-gradcam-heatmap.md` → Section 5
- **Drift Detection**: `errors/ml/ERROR-drift-detection-catalog.md`
- **Training Errors**: `errors/ml/ERROR-deep-learning-training-catalog.md`
- **Model Card Template**: `templates/ml/MODEL_CARD.md`
- **Post-Mortem Template**: `templates/ml/TEMPLATE-post-mortem.md`
