# 69_machine_learning.md - ML/AI Governance & Standards (v26.0.0)

> **Version**: 26.0.0 (Diamond Release)
> **Scope**: Machine Learning, Deep Learning, Generative AI, MLOps, Data Science
> **Compliance**: EU AI Act (2026), GDPR, NIST AI RMF, ISO/IEC 42001

## 1. Core Principles (The "Iron Triangle" + Security)

1.  **Reproducibility**: Every model MUST be reproducible from code + data + config.
    *   **Tool**: MLflow (Tracking), DVC (Data Versioning).
    *   **Rule**: No "magic numbers". All hyperparameters in YAML/Hydra.
    *   **Artifacts**: Save `requirements.txt`, `conda.yaml`, and Dockerfile with every run.
    *   **Seed**: Set global random seeds for NumPy, PyTorch, and Python.

2.  **Explainability**: Black boxes are forbidden in high-risk domains.
    *   **Tool**: SHAP, Lime, Grad-CAM (Vision), BertViz (NLP).
    *   **Rule**: Every prediction must have a local explanation.
    *   **Metric**: Faithfulness, Monotonicity.
    *   **Requirement**: For medical/financial models, provide counterfactual explanations ("If X had been Y, the prediction would be Z").

3.  **Fairness**: Bias detection is mandatory.
    *   **Tool**: Fairlearn, AIF360.
    *   **Rule**: Check for disparate impact on protected groups (Gender, Race, Age).
    *   **Threshold**: Disparate Impact Ratio between 0.8 and 1.25.
    *   **Mitigation**: Use re-weighting or adversarial debiasing if bias is detected.

4.  **Security**: Adversarial robustness and data privacy.
    *   **Tool**: Adversarial Robustness Toolbox (ART), Presidio.
    *   **Rule**: Sanitize all inputs to prevent injection attacks.
    *   **Privacy**: Apply Differential Privacy (DP-SGD) for sensitive data training.

## 2. Technology Stack (Verified Feb 2026)

*   **Frameworks**: PyTorch 2.10.0 (Standard), TensorFlow 2.16 (Legacy Support), JAX (Research).
*   **Tracking**: MLflow 3.9.0, Weights & Biases.
*   **Serving**: FastAPI + ONNX Runtime (CPU/GPU), Triton Inference Server (High Scale), vLLM (LLM Serving).
*   **Data**: Delta Lake 3.1, Apache Spark 3.5, Polars (Single Node).
*   **Orchestration**: Airflow 2.9, Kubeflow Pipelines, Prefect.
*   **Vector DB**: Milvus, Qdrant, ChromaDB (for RAG).

## 3. Project Structure (Standardized)

```
project_root/
├── data/
│   ├── raw/            # Immutable source data (DVC tracked)
│   ├── processed/      # Cleaned features (Parquet/Delta)
│   └── external/       # Third-party data
├── models/             # Model artifacts (registry)
├── notebooks/          # Exploratory analysis (Naming: 01-initial-eda.ipynb)
├── src/
│   ├── data/           # ETL scripts
│   ├── features/       # Feature engineering
│   ├── models/         # Training & Inference code
│   └── visualization/  # Plotting scripts
├── tests/              # Unit & Integration tests
├── dvc.yaml            # Data pipeline definition
├── params.yaml         # Hyperparameters
└── ml_governance/      # Model Cards, Datasheets
```

## 4. Development Workflow (Eval-Driven)

1.  **Define Metrics**: Before coding, define Success Metric (e.g., F1 > 0.85) and Guardrail Metric (e.g., Latency < 200ms).
2.  **Baseline**: Create a "Dummy Classifier" (Majority Class) to establish a baseline.
3.  **Experiment**: Run experiments with MLflow tracking.
    *   Log: Params, Metrics, Artifacts, Git Commit.
4.  **Evaluate**: Compare against baseline and previous SOTA.
5.  **Register**: Promote best model to Model Registry (Stage: Staging).
6.  **Review**: Conduct a Model Review meeting with stakeholders.

## 5. Coding Standards (ML Specific)

*   **Type Hints**: Use `jaxtyping` for tensor shapes (e.g., `Float[Tensor, "batch channels height width"]`).
*   **Config**: Use `Hydra` or `Pydantic` for configuration management.
*   **Logging**: Use `structlog` for structured JSON logging.
*   **Testing**:
    *   **Unit**: Test individual layers/functions.
    *   **Integration**: Test full training pipeline (1 epoch, small data).
    *   **Data**: Test data schema (Pandera/Great Expectations).
    *   **Model**: Test model invariance (e.g., rotation invariance for CNNs).

## 6. Model Card Requirements (Mitchell et al.)

Every model MUST have a `MODEL_CARD.md` containing:
1.  **Model Details**: Architecture, Version, Date, Author.
2.  **Intended Use**: Primary use case, Out-of-scope use cases.
3.  **Factors**: Groups evaluated (Demographics, Environment).
4.  **Metrics**: Performance measures (Accuracy, Precision, Recall).
5.  **Evaluation Data**: Datasets used for testing.
6.  **Training Data**: Datasets used for training (with DVC hash).
7.  **Ethical Considerations**: Bias, Safety, Environmental Impact.
8.  **Caveats**: Known limitations.
9.  **Carbon Footprint**: Estimated CO2 emissions for training.

## 7. Generative AI & LLM Governance

### 7.1 RAG (Retrieval-Augmented Generation)
-   **Chunking**: Must optimize chunk size (e.g., 512 tokens) with overlap (e.g., 50 tokens).
-   **Retrieval**: Use Hybrid Search (Dense + Sparse/BM25).
-   **Evaluation**: Use RAGAS metrics (Context Precision, Context Recall, Faithfulness, Answer Relevance).
-   **Hallucination**: Implement Hallucination Detection (e.g., SelfCheckGPT).

### 7.2 LLM Fine-Tuning
-   **Technique**: Use LoRA/QLoRA for parameter-efficient fine-tuning.
-   **Data Quality**: Deduplicate and sanitize instruction datasets.
-   **Evaluation**: Use LLM-as-a-Judge (e.g., GPT-4 evaluating Llama-3 outputs).

### 7.3 Prompt Engineering
-   **Versioning**: Track prompts as code (Git).
-   **Security**: Test against Prompt Injection and Jailbreaking (e.g., Garak).
-   **Structure**: Use Chain-of-Thought (CoT) for complex reasoning.

## 8. Error Handling (ML Specific)

*   **Data Drift**: If drift detected (PSI > 0.2), trigger retraining or alert.
*   **Training Divergence**: If Loss is NaN or Inf, stop immediately.
*   **OOM (Out of Memory)**: Use Gradient Accumulation or Mixed Precision (AMP).
*   **Inference Latency**: If p99 > SLA, scale out or quantize model.

## 9. Security (Adversarial Robustness)

*   **Input Validation**: Sanitize all inputs (Image size, Text length).
*   **Dependency Scan**: Scan `requirements.txt` with Snyk/Trivy.
*   **Model Scan**: Scan pickle files for malware (ModelScan).
*   **Rate Limiting**: Protect inference API from DoS.
*   **Output Filtering**: Filter toxic or PII-leaking outputs (Guardrails AI).

## 10. Roles & Responsibilities

*   **ML Engineer**: Pipeline, Training, Deployment.
*   **Data Scientist**: Feature Engineering, Model Selection.
*   **Reviewer**: Code Review, Model Card Audit.
*   **Governance Agent**: Compliance Check.
*   **Security Agent**: Threat Modeling, Penetration Testing.

## 11. Checklist (Pre-Commit)

- [ ] Code formatted (Ruff/Black).
- [ ] Types checked (MyPy).
- [ ] Tests passed (Pytest).
- [ ] Data versioned (DVC).
- [ ] Model tracked (MLflow).
- [ ] Model Card updated.
- [ ] Security scan passed.
- [ ] Bias audit completed.
- [ ] Carbon footprint calculated.

## 12. Advanced MLOps Integration

### 12.1 Model Registry Standards
- All models must be registered in MLflow with semantic versioning.
- Metadata must include: training dataset hash, hyperparameters, and evaluation metrics.
- Model artifacts must be stored in S3 with strict access controls.

### 12.2 Deployment Strategies
- Use Canary deployments for all critical models (1% -> 10% -> 100%).
- Implement Blue-Green deployment for zero-downtime updates.
- Rollback triggers must be defined based on error rates and latency.
- Shadow Deployment: Run new model in parallel with production model to compare results without affecting users.

### 12.3 Monitoring and Alerting
- Real-time monitoring of model drift using Evidently AI.
- Alerts for data quality issues (missing values, schema changes).
- Dashboard for model performance metrics (accuracy, F1-score, AUC).
- Business Metrics: Monitor impact on business KPIs (e.g., conversion rate).

### 12.4 Security and Compliance
- Ensure GDPR compliance for all training data (Right to be Forgotten).
- Implement differential privacy techniques where applicable.
- Regular security audits of ML pipelines.
- Access Logs: Audit all access to model endpoints and data.

### 12.5 Scalability and Performance
- Optimize model inference using TensorRT or ONNX Runtime.
- Use Kubernetes (KServe) for auto-scaling model serving pods.
- Implement caching strategies for frequent predictions (Redis).
- Batch Inference: Use Ray for high-throughput batch processing.

### 12.6 Collaboration and Documentation
- Maintain comprehensive documentation for all ML experiments.
- Use Jupyter Notebooks for exploratory data analysis (EDA).
- Share knowledge through regular tech talks and code reviews.
- Decision Log: Document architectural decisions (ADR).

### 12.7 Continuous Improvement
- Regularly retrain models with new data (CT - Continuous Training).
- Experiment with new architectures and algorithms.
- Stay updated with the latest research in ML/AI.
- Feedback Loop: Collect user feedback to improve model performance.
