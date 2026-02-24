# Model Card Template (v26.0)

> **Based on**: Mitchell et al. “Model Cards for Model Reporting” (2019)
> **Usage**: Copy and fill for each production model
> **Version**: v26.0.0 (Diamond 8)

## Model Details

| Field | Value |
| :--- | :--- |
| **Model Name** | [Name] |
| **Version** | [MAJOR.MINOR.PATCH] |
| **Date** | [YYYY-MM-DD] |
| **Owner** | [Data Scientist Name] |
| **Type** | [Classification / Segmentation / Embedding] |
| **Architecture** | [e.g., DINOv2 ViT-B/14 + Linear Head] |
| **Framework** | [e.g., PyTorch 2.1.0, TIMM 0.9.10] |
| **License** | [License Type] |

## Intended Use

- **Primary Use Case**: [Description]
- **Target Users**: [Description]
- **Out-of-Scope Uses**: [What this model should NOT be used for]

## Training Data

- **Dataset Name**: [Name]
- **Dataset Version**: [Version]
- **Total Images**: [Count]
- **Class Distribution**:

| Class | Train | Validation | Test |
| :--- | :--- | :--- | :--- |
| [Class A] | [Count] | [Count] | [Count] |
| [Class B] | [Count] | [Count] | [Count] |

- **Data Split Method**: [e.g., by specimen ID, stratified]
- **Augmentation**: [Reference to config]
- **Preprocessing**: [Resize, normalization details]

## Evaluation Metrics

### Aggregate Metrics

| Metric | Value |
| :--- | :--- |
| **Overall Accuracy** | [Value] |
| **Macro F1** | [Value] |
| **Weighted F1** | [Value] |
| **Macro Precision** | [Value] |
| **Macro Recall** | [Value] |

### Per-Class Metrics

| Class | Precision | Recall | F1 | Support |
| :--- | :--- | :--- | :--- | :--- |
| [Class A] | [Value] | [Value] | [Value] | [Count] |

### Quality Gate Results

| Gate | Threshold | Result | Pass/Fail |
| :--- | :--- | :--- | :--- |
| **ROAD Score** | ≥ 0.3 | [Value] | [Pass/Fail] |
| **GradCAM-Leaf Overlap** | ≥ 70% | [Value] | [Pass/Fail] |
| **Background Activation Ratio** | < 30% | [Value] | [Pass/Fail] |
| **Min Per-Class Recall** | ≥ 60% | [Value] | [Pass/Fail] |
| **Inference Latency (GPU)** | < 150ms | [Value] | [Pass/Fail] |

## Explainability

- **Method**: [GradCAM / Attention Rollout]
- **Target Layer**: [e.g., layer4[-1]]
- **Validation**: [ROAD score, overlap ratio]
- **Sample Heatmaps**: [Link or Attachments]

## Embedding Configuration

- **Dimensions**: [e.g., 768]
- **Normalization**: [L2 / None]
- **Distance Metric**: [Cosine / Euclidean]
- **Vector DB**: [ChromaDB / Qdrant]
- **Collection Name**: [Name]

## Performance & Infrastructure

- **Training Time**: [Hours] on [GPU Type]
- **Inference Latency**: GPU p95=[Value]ms, CPU p95=[Value]ms
- **Model Size**: [Params] parameters, [Disk Size] MB
- **Memory Requirement**: [GPU RAM] GB, [CPU RAM] GB
- **Batch Size**: Training=[Value], Inference=[Value]

## Known Limitations

- [Limitation 1]
- [Limitation 2]

## Ethical Considerations

- [Potential biases]
- [Risk of misdiagnosis]
- [Data privacy]

## Drift Monitoring

- **Frequency**: [Weekly / Daily]
- **Threshold**: Centroid shift > 0.05
- **Retraining Trigger**: Drift + accuracy drop > 5%
- **Last Check**: [Date] - [Status]

## Version History

| Version | Date | Changes | Quality Gate |
| :--- | :--- | :--- | :--- |
| [v1.0.0] | [Date] | [Description] | [Pass/Fail] |

## Cross-References

- **Governance Guide**: `knowledge/ml/GUIDE-model-governance.md`
- **Quality Gate Rules**: `rules/ml/RULES-gradcam-heatmap.md`
- **Master Rules**: `rules/ml/RULES-plant-disease-analysis.md`
