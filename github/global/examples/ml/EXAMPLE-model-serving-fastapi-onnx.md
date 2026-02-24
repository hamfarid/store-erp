# EXAMPLE-model-serving-fastapi-onnx.md
# Governance: ML/AI Application Framework (Feb 2026)
# Tooling: FastAPI, ONNX Runtime, Docker

## 1. Project Structure
```
model-serving-fastapi-onnx/
├── app/
│   ├── main.py              # FastAPI application
│   ├── models.py            # Pydantic schemas
│   ├── inference.py         # ONNX Runtime inference
│   └── logging.py           # Logging configuration
├── tests/                   # Unit and integration tests
├── Dockerfile               # Multi-stage build
├── requirements.txt         # Pinned dependencies
└── README.md                # Project documentation
```

## 2. API Endpoints
*   `GET /health`: Health check (200 OK).
*   `POST /predict`: Inference endpoint (JSON input -> JSON output).
*   `GET /metrics`: Prometheus metrics (Latency, Throughput).

## 3. ONNX Runtime Governance
*   **Execution Providers:** `CUDAExecutionProvider` (GPU) -> `CPUExecutionProvider` (Fallback).
*   **Session Options:** `intra_op_num_threads=1`, `inter_op_num_threads=1` (for concurrency).
*   **Optimization:** Use `onnxruntime.quantization` (INT8) for 3x speedup.
*   **Validation:** Verify output against PyTorch model (tolerance < 1e-5).

## 4. Latency SLA
*   **Real-time:** p95 < 100ms.
*   **Near-real-time:** p99 < 500ms.
*   **Batch:** Throughput > 1000 req/s.

## 5. Deployment Governance
*   **Container:** Docker (Multi-stage build).
*   **Orchestration:** Kubernetes (KServe/Seldon Core).
*   **Scaling:** HPA (Horizontal Pod Autoscaler) based on CPU/GPU usage.
*   **Monitoring:** Prometheus/Grafana dashboard.
