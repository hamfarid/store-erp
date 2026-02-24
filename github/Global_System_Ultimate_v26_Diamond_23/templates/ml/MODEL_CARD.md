# Model Card Template (v26.0)
# Based on: Mitchell et al. "Model Cards for Model Reporting" (2019)
# Usage: Copy and fill for each production model

---

## Model Details

**Model Name:**
**Version:** (Semantic: MAJOR.MINOR.PATCH)
**Date:** (Training completion date)
**Owner:** (Data Scientist responsible)
**Type:** (Classification / Segmentation / Embedding / Multi-task)
**Architecture:** (e.g., DINOv2 ViT-B/14 + Linear Classification Head)
**Framework:** (e.g., PyTorch 2.10.0, TIMM 1.0.24)
**License:**

## Intended Use

**Primary Use Case:**
**Target Users:**
**Out-of-Scope Uses:** (What this model should NOT be used for)

## Training Data

**Dataset Name:**
**Dataset Version:**
**Total Images:**
**Class Distribution:**

| Class | Train | Validation | Test |
| :--- | :--- | :--- | :--- |
| (class name) | (count) | (count) | (count) |

**Data Split Method:** (e.g., by specimen ID, stratified, temporal)
**Augmentation:** (Reference to augmentation config used)
**Preprocessing:** (Resize, normalization, etc.)

## Evaluation Metrics

### Aggregate Metrics

| Metric | Value |
| :--- | :--- |
| **Overall Accuracy** | |
| **Macro F1** | |
| **Weighted F1** | |
| **Macro Precision** | |
| **Macro Recall** | |

### Per-Class Metrics

| Class | Precision | Recall | F1 | Support |
| :--- | :--- | :--- | :--- | :--- |

### Quality Gate Results

| Gate | Threshold | Result | Pass/Fail |
| :--- | :--- | :--- | :--- |
| ROAD Score | ≥ 0.3 | | |
| GradCAM-Leaf Overlap | ≥ 70% | | |
| Background Activation Ratio | < 30% | | |
| Min Per-Class Recall | ≥ 60% | | |
| Inference Latency (GPU) | < 150ms | | |

## Explainability

**Method:** (GradCAM / Attention Rollout / SHAP)
**Target Layer:** (e.g., layer4[-1] for ResNet)
**Validation:** (ROAD score, overlap ratio, BAR — reference values above)
**Sample Heatmaps:** (Link to sample visualizations or attach images)

## Embedding Configuration

**Dimensions:** (e.g., 768)
**Normalization:** (L2 / None)
**Distance Metric:** (Cosine / Euclidean)
**Vector DB:** (ChromaDB / Qdrant / Milvus)
**Collection Name:**

## Performance & Infrastructure

**Training Time:** (hours, GPU type)
**Inference Latency:** (GPU p50/p95/p99, CPU p50/p95/p99)
**Model Size:** (parameters, disk size)
**Memory Requirement:** (GPU RAM, CPU RAM)
**Batch Size:** (Training / Inference)

## Known Limitations

*   (List known weaknesses, failure modes, edge cases)
*   (e.g., "Poor performance on heavily shadowed images")
*   (e.g., "Confusion between early blight and septoria leaf spot at early stages")

## Ethical Considerations

*   (Potential biases in training data)
*   (Risk of misdiagnosis impact on farmers)
*   (Data privacy considerations for field images with GPS metadata)

## Drift Monitoring

**Monitoring Frequency:** (Weekly / Daily)
**Drift Threshold:** (Centroid shift > 0.05)
**Retraining Trigger:** (Drift + accuracy drop > 5%)
**Last Drift Check:**
**Status:** (Stable / Drifting / Retraining Scheduled)

## Version History

| Version | Date | Changes | Quality Gate |
| :--- | :--- | :--- | :--- |
| | | | |

## Cross-References
*   **Governance Guide**: `knowledge/ml/GUIDE-model-governance.md`
*   **Quality Gate Rules**: `rules/ml/RULES-gradcam-heatmap.md`
*   **Master Rules**: `rules/ml/RULES-plant-disease-analysis.md`
