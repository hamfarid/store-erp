# GUIDE-gpu-container-setup.md
# Governance: ML/AI Application Framework (Feb 2026 — Updated)

## 1. Prerequisites
*   **Host OS:** Ubuntu 24.04 LTS (Recommended) or 22.04 LTS.
*   **NVIDIA Driver:** Version 565+ (CUDA 12.6 support).
*   **Docker:** Version 27+ (Engine, BuildKit default).
*   **NVIDIA Container Toolkit:** Version 1.16+.

## 2. Installation Steps

### 2.1 Install NVIDIA Driver
```bash
sudo apt update
sudo apt install nvidia-driver-565
sudo reboot
nvidia-smi  # Verify: should show GPU + Driver 565.xx + CUDA 12.6
```

### 2.2 Install Docker
```bash
curl -fsSL https://get.docker.com | sh
sudo usermod -aG docker $USER
newgrp docker
docker --version  # Verify: 27.x+
```

### 2.3 Install NVIDIA Container Toolkit
```bash
curl -fsSL https://nvidia.github.io/libnvidia-container/gpgkey | \
  sudo gpg --dearmor -o /usr/share/keyrings/nvidia-container-toolkit-keyring.gpg
curl -s -L https://nvidia.github.io/libnvidia-container/stable/deb/nvidia-container-toolkit.list | \
  sed 's#deb https://#deb [signed-by=/usr/share/keyrings/nvidia-container-toolkit-keyring.gpg] https://#g' | \
  sudo tee /etc/apt/sources.list.d/nvidia-container-toolkit.list
sudo apt-get update
sudo apt-get install -y nvidia-container-toolkit
sudo nvidia-ctk runtime configure --runtime=docker
sudo systemctl restart docker
```

### 2.4 Verify GPU in Docker
```bash
docker run --rm --gpus all nvidia/cuda:12.6.0-base-ubuntu24.04 nvidia-smi
```

## 3. Docker Compose GPU Configuration

### 3.1 Ollama with GPU (LLM Serving)
```yaml
ollama:
  image: ollama/ollama:latest
  container_name: gaara-ollama
  volumes:
    - ollama_data:/root/.ollama
  ports:
    - "11434:11434"
  deploy:
    resources:
      reservations:
        devices:
          - driver: nvidia
            count: 1
            capabilities: [gpu]
  restart: unless-stopped
```

### 3.2 Training Container with GPU
```yaml
training:
  build:
    context: ./services/plant-doctor
    dockerfile: Dockerfile.training
  deploy:
    resources:
      reservations:
        devices:
          - driver: nvidia
            count: all    # Use ALL GPUs
            capabilities: [gpu]
  environment:
    - CUDA_VISIBLE_DEVICES=0
  volumes:
    - ./models:/app/models
    - ./data:/app/data
```

### 3.3 CPU-Only Fallback (ONNX Runtime)
```yaml
plant-doctor:
  build: ./services/plant-doctor
  environment:
    - DEVICE=cpu                    # Force CPU
    - DISEASE_MODEL=models/plant_disease.onnx
    - NUTRIENT_MODEL=models/nutrient_deficiency.onnx
  # No GPU reservation needed — ONNX Runtime CPU is 2-5x faster than PyTorch CPU
```

## 4. GPU Auto-Detection Pattern

```python
# core/device.py
import torch
import os

def get_device():
    """Auto-detect best available device."""
    if os.getenv("DEVICE", "auto") == "cpu":
        return "cpu"
    if torch.cuda.is_available():
        gpu_name = torch.cuda.get_device_name(0)
        gpu_mem = torch.cuda.get_device_properties(0).total_mem / 1e9
        print(f"✅ GPU: {gpu_name} ({gpu_mem:.1f}GB)")
        return "cuda"
    print("⚠️ No GPU — using CPU (ONNX recommended)")
    return "cpu"

def get_onnx_providers():
    """Get ONNX Runtime execution providers."""
    import onnxruntime as ort
    available = ort.get_available_providers()
    if "CUDAExecutionProvider" in available:
        return ['CUDAExecutionProvider', 'CPUExecutionProvider']
    return ['CPUExecutionProvider']
```

## 5. Base Images

| Use Case | Image | Size |
|----------|-------|------|
| GPU Training | `nvidia/cuda:12.6.0-cudnn9-devel-ubuntu24.04` | ~5GB |
| GPU Inference | `nvidia/cuda:12.6.0-cudnn9-runtime-ubuntu24.04` | ~3GB |
| CPU Inference (ONNX) | `python:3.12-slim` | ~150MB |
| Ollama | `ollama/ollama:latest` | ~1.2GB |

## 6. GAARA-AI GPU Strategy

**CPU-First Design (ONNX):**
- Everything works on CPU by default
- ONNX Runtime provides 2-5x speedup over PyTorch on CPU
- GPU is an optional upgrade, not a requirement

**When GPU is Available:**
- Ollama loads larger models (Llama 3.1 8B vs Qwen 2.5 3B)
- Training is 10-50x faster
- Batch inference for 100+ images
- Avatar generation (SadTalker lip sync)

**When GPU is NOT Available:**
- ONNX models for inference (YOLOv8n: 45ms, DenseNet121: 25ms)
- Smaller Ollama models (Qwen 2.5 3B, Phi-3 Mini 3.8B)
- No avatar video — TTS only (Bark/Coqui)
