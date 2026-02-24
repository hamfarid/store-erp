# ML/AI Development Workflow (End-to-End) v26.0.2

> **Version**: 26.0.0 (Diamond Release)
> **Standard**: MLOps Level 2 (Automated Pipeline) + LLMOps Level 1
> **Roles**: ML Engineer, Data Scientist, Reviewer, Governance Agent
> **Compliance**: EU AI Act, NIST AI RMF

## 1. Phase 1: Problem Definition & Design (Day 0-2)

### 1.1 Define Objectives
*   **Business Goal**: What are we solving? (e.g., "Reduce churn by 5%", "Automate customer support").
*   **ML Task**: Classification, Regression, Clustering, Generation (LLM).
*   **Success Metric**: F1-Score, RMSE, MAP@K, ROUGE-L (for text).
*   **Guardrail Metric**: Latency < 100ms, Fairness > 0.8, Cost < $0.01/query.

### 1.2 Feasibility Check
*   **Data Availability**: Do we have labeled data? (Min: 1000 samples/class for Supervised, 100 for Few-Shot).
*   **Data Quality**: Missing values < 5%, Noise level acceptable.
*   **Compute**: GPU availability (A100/H100 for LLMs).
*   **Legal**: Is the data usage compliant with GDPR/CCPA?

### 1.3 Design Doc (RFC)
*   Create `docs/design/ML-RFC-001.md`.
*   Review with Architect and Stakeholders.
*   **Decision Log**: Record architectural decisions (e.g., "Why we chose Llama-3 over GPT-4").

## 2. Phase 2: Data Engineering (Day 3-5)

### 2.1 Ingestion
*   **Source**: SQL, S3, API, Web Scraping.
*   **Tool**: Spark, Airbyte, Kafka (Streaming).
*   **Output**: Raw data in `data/raw/` (Immutable).
*   **Lineage**: Track source origin and extraction timestamp.

### 2.2 Versioning
*   **Tool**: DVC (Data Version Control).
*   **Command**: `dvc add data/raw/dataset.csv`.
*   **Commit**: `git commit -m "Add raw data v1"`.
*   **Remote**: Push to S3/GCS bucket.

### 2.3 Validation (Schema)
*   **Tool**: Great Expectations / Pandera.
*   **Checks**:
    *   Column types (int, float, string).
    *   Value ranges (age > 0, probability 0-1).
    *   Null checks (critical columns must not be null).
    *   Uniqueness checks (ID columns).
*   **Action**: Fail pipeline if validation fails.

### 2.4 Feature Engineering
*   **Transformation**: Scaling, Encoding, Embedding (BERT/ResNet).
*   **Feature Store**: Register features in Feast (if applicable).
*   **Output**: Processed data in `data/processed/`.
*   **Documentation**: Update `data/README.md` with feature definitions.

## 3. Phase 3: Experimentation (Day 6-10)

### 3.1 Baseline
*   Train a simple model (Logistic Regression, Random Forest, Zero-Shot LLM).
*   Log metrics to MLflow.
*   **Goal**: Establish a performance floor.

### 3.2 Iteration
*   **Hyperparameter Tuning**: Optuna / Ray Tune.
*   **Architecture Search**: Try different backbones (ResNet, EfficientNet, Transformer).
*   **Tracking**:
    *   `mlflow.log_param("lr", 0.001)`
    *   `mlflow.log_metric("val_loss", 0.2)`
    *   `mlflow.log_artifact("confusion_matrix.png")`
    *   `mlflow.log_artifact("shap_summary.png")`

### 3.3 Evaluation
*   **Holdout Set**: Evaluate on unseen test set (never used in training/tuning).
*   **Error Analysis**: Inspect misclassified examples (Confusion Matrix).
*   **Bias Check**: Run Fairlearn audit for protected groups.
*   **Robustness**: Test against adversarial examples (ART).

## 4. Phase 4: Productionization (Day 11-13)

### 4.1 Code Refactoring
*   Convert Notebooks to Python Modules (`src/models/`).
*   Add Type Hints (`jaxtyping`) and Docstrings.
*   Run Linters (Ruff, Black, MyPy).
*   **Security**: Remove hardcoded secrets/API keys.

### 4.2 Testing
*   **Unit Tests**: `pytest tests/unit/` (Test individual functions).
*   **Integration Tests**: `pytest tests/integration/` (Test full pipeline).
*   **Regression Tests**: Ensure performance >= Baseline.
*   **Load Testing**: Simulate high concurrency (Locust).

### 4.3 Containerization
*   Build Docker Image: `docker build -t my-model:v1 .`.
*   **Optimization**: Use multi-stage builds to reduce image size.
*   Scan Image: `trivy image my-model:v1` (Check for CVEs).

## 5. Phase 5: Deployment (Day 14)

### 5.1 Staging
*   Deploy to Staging Environment (K8s Namespace: `staging`).
*   Run Smoke Tests (API Health Check).
*   **Integration Test**: Verify end-to-end flow with frontend/backend.

### 5.2 Production (Canary)
*   Route 5% traffic to new model.
*   Monitor Error Rate and Latency.
*   Promote to 100% if stable for 1 hour.
*   **Shadow Mode**: Run new model in parallel with old model (logging only) to compare results safely.

### 5.3 Rollback Plan
*   **Trigger**: Error Rate > 1%, Latency p99 > 500ms.
*   **Action**: Revert to previous version immediately.
*   **Command**: `kubectl rollout undo deployment/my-model`.
*   **Post-Mortem**: Analyze why the failure occurred.

## 6. Phase 6: Monitoring & Maintenance (Day 15+)

### 6.1 Observability
*   **Metrics**: Request Count, Latency, Error Rate (Prometheus).
*   **Logs**: Structured Logs (ELK/Splunk) with Request ID.
*   **Traces**: OpenTelemetry (Jaeger) for distributed tracing.

### 6.2 Drift Detection
*   **Tool**: Evidently AI / Arize.
*   **Schedule**: Daily.
*   **Metric**: PSI (Population Stability Index), KL Divergence, Wasserstein Distance.
*   **Action**: Trigger Retraining if Drift > Threshold.

### 6.3 Retraining
*   **Trigger**: Drift Alert or Schedule (Monthly).
*   **Process**: Re-run Pipeline with new data.
*   **Validation**: Must beat current production model on "Golden Dataset".
*   **Approval**: Manual approval required for major version updates.

## 7. Governance Gates

| Gate | Approver | Criteria |
| :--- | :--- | :--- |
| **Design Review** | Architect | Feasibility, Cost, Ethics |
| **Data Review** | Data Steward | PII Compliance, Quality, Lineage |
| **Model Review** | Lead Data Scientist | Performance, Fairness, Code Quality |
| **Security Review** | InfoSec | Vulnerability Scan, Access Control |
| **Deployment Review** | DevOps | Scalability, Rollback Plan, Resource Quotas |

## 8. LLM Specific Workflow (Generative AI)

### 8.1 Prompt Engineering
*   **Version Control**: Store prompts in Git (`prompts/v1/`).
*   **Evaluation**: Use LLM-as-a-Judge to score outputs.
*   **Optimization**: Use DSPy to optimize prompts automatically.

### 8.2 RAG Pipeline
*   **Ingestion**: Chunk documents -> Embed -> Store in Vector DB.
*   **Retrieval**: Hybrid Search (Dense + Sparse).
*   **Generation**: Context + Query -> LLM -> Answer.
*   **Eval**: RAGAS metrics (Context Precision, Faithfulness).

### 8.3 Fine-Tuning
*   **Data**: Instruction tuning dataset (Input/Output pairs).
*   **Technique**: LoRA / QLoRA (Parameter Efficient).
*   **Compute**: Multi-GPU training (FSDP / DeepSpeed).

## 9. Tools & References

*   **Tracking**: [MLflow](https://mlflow.org/)
*   **Versioning**: [DVC](https://dvc.org/)
*   **Validation**: [Great Expectations](https://greatexpectations.io/)
*   **Serving**: [FastAPI](https://fastapi.tiangolo.com/), [Triton](https://developer.nvidia.com/triton-inference-server)
*   **Monitoring**: [Evidently AI](https://www.evidentlyai.com/)
*   **Orchestration**: [Airflow](https://airflow.apache.org/), [Kubeflow](https://www.kubeflow.org/)

## 10. Detailed Execution Steps Checklist

### Phase 1: Data Preparation
1. [ ] **Data Ingestion**: Connect to sources, validate schema.
2. [ ] **Feature Engineering**: Create features, normalize, encode.
3. [ ] **Data Splitting**: Stratified split (Train/Val/Test).
4. [ ] **Versioning**: DVC commit and push.

### Phase 2: Model Training
1. [ ] **Experiment Setup**: Define search space, config.
2. [ ] **Training Loop**: Implement early stopping, checkpointing.
3. [ ] **Hyperparameter Tuning**: Run optimization jobs.
4. [ ] **Selection**: Pick best model based on Val Metric.

### Phase 3: Model Evaluation
1. [ ] **Performance Metrics**: Calculate F1, AUC, etc.
2. [ ] **Bias Audit**: Check fairness across groups.
3. [ ] **Error Analysis**: Review confusion matrix.
4. [ ] **Model Card**: Generate `MODEL_CARD.md`.

### Phase 4: Deployment
1. [ ] **Packaging**: Docker build, optimize, scan.
2. [ ] **Infrastructure**: K8s deployment, HPA.
3. [ ] **Monitoring**: Set up dashboards and alerts.
4. [ ] **Canary Release**: Gradual rollout.

### Phase 5: Maintenance
1. [ ] **Retraining**: Schedule jobs.
2. [ ] **Feedback Loop**: Collect user feedback.
3. [ ] **Drift Monitoring**: Check daily reports.
4. [ ] **Cost Optimization**: Review resource usage monthly.
