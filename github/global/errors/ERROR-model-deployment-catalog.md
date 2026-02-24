# ERROR-model-deployment-catalog.md
# Governance: ML/AI Application Framework (Feb 2026)
# Tooling: ONNX Runtime, PyTorch, Docker

## 1. Serialization Failures (High Severity)
**ID:** `MD-SF-001`
**Name:** Pickle Compatibility
**Description:** Model saved with newer Python/Library version fails to load on older version.
**Detection:** `ModuleNotFoundError`; `AttributeError`.
**Resolution:** Use ONNX for interoperability; Match environment versions.
**Prevention:** Docker containerization; Strict version pinning.

**ID:** `MD-SF-002`
**Name:** ONNX Protobuf Limit
**Description:** Model size exceeds 2GB protobuf limit.
**Detection:** `ValueError: Message exceeds 2GB limit`.
**Resolution:** Save with external data (`save_as_external_data=True`).
**Prevention:** Check model size before export.

## 2. Version Mismatches (Critical Severity)
**ID:** `MD-VM-001`
**Name:** CUDA Version Mismatch
**Description:** PyTorch/TensorFlow compiled with different CUDA version than runtime.
**Detection:** `RuntimeError: CUDA error: no kernel image is available`.
**Resolution:** Match CUDA versions (e.g., 12.1); Use NVIDIA Container Toolkit.
**Prevention:** Use official NVIDIA Docker images.

**ID:** `MD-VM-002`
**Name:** Library Version Conflict
**Description:** Dependency hell (e.g., NumPy 1.x vs 2.x).
**Detection:** `ImportError`; `VersionConflict`.
**Resolution:** Use `pip-compile` or `poetry` for lock files.
**Prevention:** Renovate bot; CI/CD dependency checks.

## 3. Inference Failures (High Severity)
**ID:** `MD-IF-001`
**Name:** Cold Start Latency
**Description:** First request takes 10-100x longer due to model loading/JIT compilation.
**Detection:** Latency spike on startup.
**Resolution:** Implement warm-up script (send dummy requests).
**Prevention:** Keep containers warm; Use provisioned concurrency.

**ID:** `MD-IF-002`
**Name:** Memory Leak
**Description:** RAM usage grows over time until OOM kill.
**Detection:** Prometheus memory metric increasing linearly.
**Resolution:** Restart container; Profile with `memory_profiler`.
**Prevention:** Avoid global variables; Close sessions/connections.
