# EXAMPLE-containerized-ml-training.md
# Governance: ML/AI Application Framework (Feb 2026)
# Tooling: Docker, NVIDIA Container Toolkit

## 1. Project Structure
```
containerized-ml-training/
├── configs/
│   ├── config.yaml          # Hyperparameters, paths
│   └── logging.yaml         # Logging configuration
├── data/
│   ├── raw/                 # Immutable raw data
│   ├── processed/           # Cleaned and tokenized data
│   └── splits/              # Train/Val/Test splits (stratified)
├── src/
│   ├── data/                # Data loading and preprocessing scripts
│   ├── models/              # Model definition
│   ├── training/            # Training loop and evaluation
│   └── optimization/        # Hyperparameter tuning (Optuna)
├── notebooks/               # EDA and experimentation notebooks
├── tests/                   # Unit and integration tests
├── Dockerfile               # Multi-stage build
├── requirements.txt         # Pinned dependencies
└── README.md                # Project documentation
```

## 2. Dockerfile Governance
*   **Base Image:** `nvidia/cuda:12.4.0-cudnn9-devel-ubuntu22.04` (Training).
*   **Runtime Image:** `nvidia/cuda:12.4.0-cudnn9-runtime-ubuntu22.04` (Serving).
*   **User:** `USER 1000:1000` (Non-root).
*   **Secrets:** Use Docker Secrets or Environment Variables (NEVER hardcode).
*   **Scanning:** Use `docker scout` or `trivy` to scan for vulnerabilities.

## 3. Docker Compose Governance
*   **Services:** `training`, `mlflow`, `postgres` (MLflow backend).
*   **Volumes:** `data:/data`, `models:/models`, `mlruns:/mlruns`.
*   **Networks:** `ml-network` (Isolated).
*   **GPU:** `deploy.resources.reservations.devices` (NVIDIA Driver).

## 4. Kubernetes Governance
*   **Resources:** `requests` and `limits` for CPU/Memory/GPU.
*   **Probes:** `livenessProbe` and `readinessProbe` (HTTP/TCP).
*   **Security Context:** `runAsNonRoot: true`, `readOnlyRootFilesystem: true`.
*   **Affinity:** `nodeAffinity` for GPU nodes.
