# GUIDE-drift-detection-tools.md
# Governance: ML/AI Application Framework (Feb 2026 — Updated)

## 1. Evidently AI (Recommended — Primary)
*   **Version:** 0.6+ (25M+ downloads, major rewrite from 0.4.x)
*   **What's New in 0.6:**
    - 100+ built-in metrics and tests (up from ~50)
    - Live monitoring dashboard (UI at localhost:8000)
    - LLM output quality monitoring (hallucination, toxicity, relevance)
    - Embedding drift detection (cosine similarity, Jensen-Shannon)
    - Text descriptor drift (length, sentiment, OOV words)
*   **Pros:** Comprehensive reports (HTML/JSON), integrates with MLflow/Airflow, supports tabular/text/image/embeddings.
*   **Cons:** Requires sampling for very large datasets (>1M rows).
*   **Use Case:** GAARA-AI plant disease model monitoring, LLM output quality tracking.

### Detection Methods (20+ statistical tests):
| Data Type | Methods |
|-----------|---------|
| Numerical | Kolmogorov-Smirnov, Wasserstein, PSI, Jensen-Shannon |
| Categorical | Chi-squared, PSI, Jenson-Shannon |
| Text | Text descriptors (length, sentiment, OOV), embedding drift |
| Embeddings | Cosine similarity, model-based drift |

### Implementation:
```python
from evidently import Report
from evidently.presets import DataDriftPreset

# Generate drift report
report = Report([DataDriftPreset(method="psi")])
report.run(reference_data=train_df, current_data=production_df)
report.save_html("drift_report.html")

# Test Suite (pass/fail gates for CI/CD)
from evidently import TestSuite
from evidently.tests import TestColumnDrift

suite = TestSuite([
    TestColumnDrift(column_name="prediction_confidence", threshold=0.2)
])
suite.run(reference_data=train_df, current_data=production_df)
assert suite.as_dict()["summary"]["all_passed"]
```

### Live Dashboard:
```bash
pip install evidently
evidently ui --workspace ./workspace
# Visit http://localhost:8000
```

### Celery Integration (Scheduled Monitoring):
```python
@app.task
def check_model_drift():
    reference = load_reference_data()  # Training distribution
    current = load_recent_predictions(days=7)  # Last week's predictions

    report = Report([DataDriftPreset()])
    report.run(reference, current)

    result = report.as_dict()
    if result["metrics"][0]["result"]["dataset_drift"]:
        send_alert("⚠️ Model drift detected! Check Evidently dashboard.")
        trigger_retraining.delay()  # Async retraining
```

## 2. NannyML
*   **Version:** 0.12+
*   **Key Strength:** Estimates performance WITHOUT ground truth (CBPE algorithm).
*   **Use Case:** When ground truth is delayed (e.g., crop yield prediction — months to verify).
*   **Note:** More complex setup than Evidently. Use only if you need no-ground-truth estimation.

## 3. Alibi Detect
*   **Version:** 0.12+
*   **Key Strength:** Advanced algorithms (MMD, learned kernel drift).
*   **⚠️ License:** Changed from Apache 2.0 to Elastic License 2.0 — check compliance!
*   **Use Case:** Deep learning image drift (plant disease photo distribution changes).

## 4. Deepchecks
*   **Version:** 0.18+
*   **Key Strength:** Pre-deployment validation suites, CI/CD integration.
*   **Use Case:** Validate new training data quality before model retraining.

## 5. GAARA-AI Drift Strategy

### What to Monitor:
| Component | Drift Type | Tool | Frequency |
|-----------|-----------|------|-----------|
| Plant Disease Model | Data drift (image distribution) | Evidently | Daily |
| Plant Disease Model | Prediction drift (confidence scores) | Evidently | Daily |
| Nutrient Model | Concept drift (accuracy vs ground truth) | Evidently | Weekly |
| LLM Outputs | Quality drift (hallucination, relevance) | Evidently LLM | Daily |
| RAG Retrieval | Embedding drift (query vs stored) | Evidently | Weekly |
| Scraping Data | Data quality drift (missing fields) | Evidently | Per batch |

### Alert Thresholds:
```yaml
# infrastructure/monitoring/drift_config.yaml
plant_disease:
  psi_threshold: 0.2          # Population Stability Index
  confidence_drop: 0.1        # If avg confidence drops >10%
  alert_email: hamfarid@gaara.com
  action: trigger_retraining

llm_output:
  hallucination_rate: 0.15    # >15% hallucinated responses
  relevance_drop: 0.2         # Relevance score drops >20%
  action: alert_team

scraping:
  missing_fields_rate: 0.3    # >30% missing fields
  action: pause_scraping
```
