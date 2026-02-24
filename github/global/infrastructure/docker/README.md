# Docker — ML Pipeline Images (v26.0.2 Diamond 32)

> Dockerfiles and compose configurations for ML training, serving, and data processing.

## Dockerfiles
| File | Purpose | Base |
|------|---------|------|
| `Dockerfile.ml-serving` | Model inference server (ONNX/TorchServe) | python:3.11-slim |
| `Dockerfile.ml-training` | Training pipeline with GPU support | nvidia/cuda:12.2 |
| `Dockerfile.python` | General Python worker (Celery tasks) | python:3.11-slim |
| `Dockerfile.spark` | Apache Spark ETL jobs | spark:3.5-python3 |

## Compose
- `docker-compose.ml-pipeline.yml` — Full ML pipeline: training → registry → serving

## Related
- `../containers/docker-compose.yml` — GAARA-AI service composition
- `../../DOCKER_GUIDE.md` — Root Docker guide
