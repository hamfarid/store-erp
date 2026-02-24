# GUIDE-ml-tool-versions.md
# Governance: ML/AI Application Framework (Feb 2026)

## 1. Core Libraries
*   **Python:** 3.11.8 (Stable, performant).
*   **PyTorch:** 2.2.1 (CUDA 12.4 support, FlashAttention-2).
*   **TensorFlow:** 2.16.1 (Legacy support only; prefer PyTorch).
*   **Scikit-learn:** 1.4.1.post1 (Improved performance, new estimators).
*   **Pandas:** 2.2.1 (PyArrow backend default).
*   **NumPy:** 1.26.4 (Last version supporting Python < 3.12).

## 2. MLOps Tools
*   **MLflow:** 3.9.0 (Enhanced UI, LLM tracking).
*   **DVC:** 3.48.0 (Data versioning).
*   **Evidently AI:** 0.7.17 (Drift detection).
*   **Great Expectations:** 1.11.3 (Data validation).
*   **Optuna:** 3.5.0 (Hyperparameter optimization).

## 3. Serving & Deployment
*   **FastAPI:** 0.109.2 (High performance async API).
*   **Uvicorn:** 0.27.1 (ASGI server).
*   **Gunicorn:** 21.2.0 (WSGI server).
*   **ONNX Runtime:** 1.17.1 (Inference engine).
*   **Triton Inference Server:** 24.02 (NVIDIA optimized).

## 4. NLP & LLMs
*   **Transformers:** 4.38.2 (Hugging Face).
*   **Tokenizers:** 0.15.2 (Fast tokenization).
*   **LangChain:** 0.1.11 (Orchestration).
*   **LlamaIndex:** 0.10.18 (Data framework for LLMs).

## 5. Computer Vision
*   **Torchvision:** 0.17.1 (Models, datasets, transforms).
*   **Albumentations:** 1.4.0 (Fast image augmentation).
*   **OpenCV-Python:** 4.9.0.80 (Image processing).
*   **Ultralytics (YOLO):** 8.1.24 (Object detection).

## 6. Deprecated/Maintenance Mode
*   **TorchServe:** Maintenance mode (Use Triton or KServe).
*   **Prophet:** Maintenance mode (Use NeuralProphet or StatsForecast).
*   **Keras:** Integrated into TensorFlow (Keras 3.0 supports PyTorch/JAX).
