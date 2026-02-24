# Learning Container - v2026.2
# Purpose: Model training, fine-tuning, and RAG updates.
# Compliance: Data Validation, Versioning, Reproducibility.

FROM nvidia/cuda:12.4.0-cudnn9-devel-ubuntu22.04

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    DEBIAN_FRONTEND=noninteractive \
    MLFLOW_TRACKING_URI=http://mlflow:5000

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    python3-dev \
    python3-pip \
    git \
    curl \
    libgl1-mesa-glx \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt

# Create non-root user
RUN useradd -m learning_agent
USER learning_agent
WORKDIR /home/learning_agent

# Copy application code
COPY . .

# Entrypoint
ENTRYPOINT ["python3", "train.py"]
