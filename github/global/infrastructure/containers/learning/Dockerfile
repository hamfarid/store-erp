# Learning Container - v2026.2 (Updated Feb 2026)
# Purpose: Model training, fine-tuning, RAG updates, data processing
# GPU: nvidia/cuda:12.6.0 (auto-detected)
# CPU: Falls back to ONNX Runtime

FROM nvidia/cuda:12.6.0-cudnn9-devel-ubuntu24.04

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    DEBIAN_FRONTEND=noninteractive \
    MLFLOW_TRACKING_URI=http://mlflow:5000

# System dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    python3-dev \
    python3-pip \
    python3-venv \
    git \
    curl \
    libgl1-mesa-glx \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

# Python dependencies
COPY requirements.txt .
RUN pip3 install --no-cache-dir --break-system-packages -r requirements.txt

# Non-root user
RUN useradd -m learning_agent
USER learning_agent
WORKDIR /home/learning_agent

COPY . .

ENTRYPOINT ["python3", "train.py"]
