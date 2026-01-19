#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Generate PDF report of AI/ML Docker containers for Gaara AI project.
"""

from fpdf import FPDF
import os
from datetime import datetime

class ContainersPDF(FPDF):
    """Custom PDF class for containers documentation."""
    
    def header(self):
        self.set_font('Helvetica', 'B', 11)
        self.cell(0, 8, 'Gaara AI - AI/ML Docker Containers Documentation', 0, 1, 'C')
        self.line(10, 18, 200, 18)
        self.ln(3)
        
    def footer(self):
        self.set_y(-15)
        self.set_font('Helvetica', 'I', 8)
        self.cell(0, 10, f'Page {self.page_no()}/{{nb}} | Generated: {datetime.now().strftime("%Y-%m-%d")}', 0, 0, 'C')

    def add_container_section(self, title, port, base_image, purpose, dockerfile_content):
        """Add a container section to the PDF."""
        # Title with colored background
        self.set_font('Helvetica', 'B', 14)
        self.set_fill_color(41, 128, 185)
        self.set_text_color(255, 255, 255)
        self.cell(0, 10, title, 0, 1, 'L', fill=True)
        self.set_text_color(0, 0, 0)
        self.ln(3)
        
        # Container info table
        self.set_font('Helvetica', 'B', 10)
        self.set_fill_color(230, 230, 230)
        self.cell(40, 7, 'Port:', 1, 0, 'L', fill=True)
        self.set_font('Helvetica', '', 10)
        self.cell(50, 7, port, 1, 0, 'L')
        self.set_font('Helvetica', 'B', 10)
        self.cell(40, 7, 'Base Image:', 1, 0, 'L', fill=True)
        self.set_font('Helvetica', '', 10)
        self.cell(60, 7, base_image, 1, 1, 'L')
        
        # Purpose
        self.set_font('Helvetica', 'B', 10)
        self.cell(40, 7, 'Purpose:', 1, 0, 'L', fill=True)
        self.set_font('Helvetica', '', 10)
        self.multi_cell(150, 7, purpose, 1, 'L')
        self.ln(3)
        
        # Dockerfile content
        self.set_font('Helvetica', 'B', 10)
        self.cell(0, 7, 'Dockerfile:', 0, 1, 'L')
        self.set_font('Courier', '', 7)
        self.set_fill_color(245, 245, 245)
        
        for line in dockerfile_content.split('\n'):
            if line.strip():
                # Truncate long lines
                display_line = line[:100] + '...' if len(line) > 100 else line
                self.cell(0, 4, display_line, 0, 1, 'L', fill=True)
        
        self.ln(5)


def create_pdf():
    """Generate the AI containers PDF report."""
    
    pdf = ContainersPDF()
    pdf.alias_nb_pages()
    pdf.set_auto_page_break(auto=True, margin=15)
    
    # Title Page
    pdf.add_page()
    pdf.set_font('Helvetica', 'B', 28)
    pdf.ln(40)
    pdf.cell(0, 15, 'Gaara AI System', 0, 1, 'C')
    pdf.set_font('Helvetica', 'B', 20)
    pdf.cell(0, 12, 'AI/ML Docker Containers', 0, 1, 'C')
    pdf.set_font('Helvetica', '', 14)
    pdf.cell(0, 10, 'Technical Documentation', 0, 1, 'C')
    pdf.ln(20)
    
    pdf.set_font('Helvetica', '', 12)
    pdf.cell(0, 8, f'Version: 4.3', 0, 1, 'C')
    pdf.cell(0, 8, f'Date: {datetime.now().strftime("%Y-%m-%d")}', 0, 1, 'C')
    pdf.ln(30)
    
    # Table of Contents
    pdf.set_font('Helvetica', 'B', 16)
    pdf.cell(0, 10, 'Table of Contents', 0, 1, 'L')
    pdf.ln(5)
    
    containers_list = [
        ('1. Plant Hybridization Container', 'Port 8022'),
        ('2. Disease Diagnosis Container', 'Port 8001'),
        ('3. YOLO Detection Container', 'Port 8018'),
        ('4. Plant Disease Advanced Container', 'Port 8021'),
        ('5. ResNet-50 Container', 'Port 8003'),
        ('6. GPU Processing Container', 'Port 8020'),
        ('7. Image Enhancement Container', 'Port 8019'),
        ('8. Adaptive Learning Container', 'Port 8017'),
        ('9. Analytics Container', 'Port 8002'),
        ('10. AI Agents Container', 'Port 8016'),
        ('11. Auto Learning Container', 'Port 8015'),
        ('12. Memory Central Container', 'Port 8014'),
    ]
    
    pdf.set_font('Helvetica', '', 11)
    for name, port in containers_list:
        pdf.cell(120, 7, name, 0, 0, 'L')
        pdf.cell(0, 7, port, 0, 1, 'R')
    
    # ===== Container 1: Plant Hybridization =====
    pdf.add_page()
    pdf.add_container_section(
        title='1. Plant Hybridization Container',
        port='8022',
        base_image='python:3.11-slim',
        purpose='Advanced plant hybridization simulations using genetic algorithms and ML models for optimal crop breeding.',
        dockerfile_content='''# Plant Hybridization Container
FROM python:3.11-slim

RUN apt-get update && apt-get install -y \\
    gcc g++ curl git gfortran \\
    liblapack-dev libblas-dev \\
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY src/ ./src/
COPY config/ ./config/
COPY data/ ./data/

RUN mkdir -p /app/data/{varieties,traits,objectives,simulations,results,logs}

ENV PYTHONPATH=/app
ENV HYBRIDIZATION_PORT=8022
ENV SIMULATION_WORKERS=4
ENV MAX_GENERATIONS=100

EXPOSE 8022

HEALTHCHECK --interval=30s --timeout=15s --start-period=60s --retries=3 \\
    CMD curl -f http://localhost:8022/health || exit 1

CMD ["python", "src/plant_hybridization_service.py"]'''
    )
    
    # Key Features
    pdf.set_font('Helvetica', 'B', 10)
    pdf.cell(0, 7, 'Key Features:', 0, 1, 'L')
    pdf.set_font('Helvetica', '', 9)
    features = [
        'Genetic algorithm-based hybridization simulation',
        'Multi-objective optimization for crop traits',
        'Support for up to 100 generations of breeding',
        'Parallel simulation with 4 workers',
        'Integration with plant variety database',
    ]
    for f in features:
        pdf.cell(0, 5, f'  * {f}', 0, 1)
    
    # ===== Container 2: Disease Diagnosis =====
    pdf.add_page()
    pdf.add_container_section(
        title='2. Disease Diagnosis Container',
        port='8001',
        base_image='python:3.11-slim',
        purpose='AI-powered plant disease diagnosis using ResNet-50 and custom trained models for accurate disease identification.',
        dockerfile_content='''# Disease Diagnosis Container
FROM python:3.11-slim as diagnosis-base

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/app

RUN apt-get update && apt-get install -y \\
    libgl1-mesa-glx libglib2.0-0 libsm6 \\
    libxext6 libxrender-dev libgomp1 curl \\
    && rm -rf /var/lib/apt/lists/*

RUN groupadd -r diagnosis && useradd -r -g diagnosis diagnosis
RUN mkdir -p /app /app/models /app/data /app/logs

WORKDIR /app
COPY docker/diagnosis/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY src/modules/disease_diagnosis/ ./diagnosis/
COPY src/modules/plant_disease/ ./plant_disease/
COPY src/advanced_ai_system.py ./

USER diagnosis
EXPOSE 8001

HEALTHCHECK --interval=30s --timeout=10s --retries=3 \\
    CMD curl -f http://localhost:8001/health || exit 1

CMD ["uvicorn", "diagnosis.api:app", "--host", "0.0.0.0", "--port", "8001"]'''
    )
    
    pdf.set_font('Helvetica', 'B', 10)
    pdf.cell(0, 7, 'AI Models Used:', 0, 1, 'L')
    pdf.set_font('Helvetica', '', 9)
    models = [
        'ResNet-50 (Pre-trained on ImageNet)',
        'Custom plant disease classifier',
        'Transfer learning for specific crops',
        'Confidence scoring system',
    ]
    for m in models:
        pdf.cell(0, 5, f'  * {m}', 0, 1)
    
    # ===== Container 3: YOLO Detection =====
    pdf.add_page()
    pdf.add_container_section(
        title='3. YOLO Detection Container',
        port='8018',
        base_image='ultralytics/ultralytics:latest',
        purpose='Real-time object detection for plants, diseases, and pests using YOLOv8 models with GPU acceleration.',
        dockerfile_content='''# YOLO Detection Container
FROM ultralytics/ultralytics:latest

RUN apt-get update && apt-get install -y \\
    gcc g++ curl git \\
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY src/ ./src/
COPY config/ ./config/
COPY models/ ./models/

RUN mkdir -p /app/data/{input,output,models,weights,results,logs}

# Download pre-trained YOLO models
RUN python -c "from ultralytics import YOLO; \\
    YOLO('yolov8n.pt'); YOLO('yolov8s.pt'); YOLO('yolov8m.pt')"

ENV PYTHONPATH=/app
ENV YOLO_PORT=8018
ENV MODEL_PATH=/app/models
ENV WEIGHTS_PATH=/app/data/weights

EXPOSE 8018

HEALTHCHECK --interval=30s --timeout=15s --retries=3 \\
    CMD curl -f http://localhost:8018/health || exit 1

CMD ["python", "src/yolo_detection_service.py"]'''
    )
    
    pdf.set_font('Helvetica', 'B', 10)
    pdf.cell(0, 7, 'YOLO Models Included:', 0, 1, 'L')
    pdf.set_font('Helvetica', '', 9)
    yolo_models = [
        'YOLOv8n (Nano) - Fast inference, lower accuracy',
        'YOLOv8s (Small) - Balanced speed/accuracy',
        'YOLOv8m (Medium) - Higher accuracy',
        'Custom trained models for plant diseases',
    ]
    for m in yolo_models:
        pdf.cell(0, 5, f'  * {m}', 0, 1)
    
    # ===== Container 4: Plant Disease Advanced =====
    pdf.add_page()
    pdf.add_container_section(
        title='4. Plant Disease Advanced Container',
        port='8021',
        base_image='python:3.11-slim',
        purpose='Advanced disease detection with knowledge base integration for symptoms, causes, and treatment recommendations.',
        dockerfile_content='''# Plant Disease Advanced Container
FROM python:3.11-slim

RUN apt-get update && apt-get install -y \\
    gcc g++ curl git \\
    libopencv-dev python3-opencv \\
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY src/ ./src/
COPY config/ ./config/
COPY knowledge_base/ ./knowledge_base/

RUN mkdir -p /app/data/{diseases,symptoms,treatments,models,results,logs}

ENV PYTHONPATH=/app
ENV DISEASE_PORT=8021
ENV KNOWLEDGE_BASE_PATH=/app/knowledge_base
ENV MODELS_PATH=/app/data/models

EXPOSE 8021

HEALTHCHECK --interval=30s --timeout=15s --retries=3 \\
    CMD curl -f http://localhost:8021/health || exit 1

CMD ["python", "src/plant_disease_advanced_service.py"]'''
    )
    
    pdf.set_font('Helvetica', 'B', 10)
    pdf.cell(0, 7, 'Knowledge Base Features:', 0, 1, 'L')
    pdf.set_font('Helvetica', '', 9)
    kb_features = [
        'Disease symptom database',
        'Treatment recommendations',
        'Prevention guidelines',
        'Multi-language support',
    ]
    for f in kb_features:
        pdf.cell(0, 5, f'  * {f}', 0, 1)
    
    # ===== Container 5: ResNet-50 =====
    pdf.add_page()
    pdf.add_container_section(
        title='5. ResNet-50 Container',
        port='8003',
        base_image='python:3.11-slim (multi-stage)',
        purpose='Computer vision service using ResNet-50 for image classification and feature extraction.',
        dockerfile_content='''# ResNet-50 Container (Multi-stage build)
FROM python:3.11-slim as builder

RUN apt-get update && apt-get install -y \\
    build-essential cmake libopencv-dev \\
    libgl1-mesa-glx wget \\
    && rm -rf /var/lib/apt/lists/*

RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Download pre-trained ResNet-50
RUN python -c "import torch; import torchvision.models as models; \\
    model = models.resnet50(pretrained=True); \\
    torch.save(model.state_dict(), '/opt/venv/resnet50_pretrained.pth')"

FROM python:3.11-slim as runtime
COPY --from=builder /opt/venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

WORKDIR /app
COPY src/ ./src/
COPY config/ ./config/

RUN useradd --create-home resnet_user
USER resnet_user

ENV MODEL_PATH=/opt/venv/resnet50_pretrained.pth
ENV OMP_NUM_THREADS=4

EXPOSE 8003

CMD ["uvicorn", "src.resnet50_service:app", "--host", "0.0.0.0", "--port", "8003"]'''
    )
    
    # ===== Container 6: GPU Processing =====
    pdf.add_page()
    pdf.add_container_section(
        title='6. GPU Processing Container',
        port='8020',
        base_image='nvidia/cuda:11.8-devel-ubuntu20.04',
        purpose='GPU-accelerated processing for AI model inference and training with CUDA support.',
        dockerfile_content='''# GPU Processing Container
FROM nvidia/cuda:11.8-devel-ubuntu20.04

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install -y \\
    python3.11 python3.11-dev python3-pip \\
    gcc g++ curl git \\
    libcudnn8 libcudnn8-dev \\
    && rm -rf /var/lib/apt/lists/*

RUN ln -s /usr/bin/python3.11 /usr/bin/python

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY src/ ./src/
COPY config/ ./config/

RUN mkdir -p /app/data/{gpu_cache,models,processing,results,logs}

ENV PYTHONPATH=/app
ENV GPU_PORT=8020
ENV CUDA_VISIBLE_DEVICES=0
ENV NVIDIA_VISIBLE_DEVICES=all
ENV NVIDIA_DRIVER_CAPABILITIES=compute,utility

EXPOSE 8020

CMD ["python", "src/gpu_processing_service.py"]'''
    )
    
    pdf.set_font('Helvetica', 'B', 10)
    pdf.cell(0, 7, 'GPU Capabilities:', 0, 1, 'L')
    pdf.set_font('Helvetica', '', 9)
    gpu_caps = [
        'CUDA 11.8 support',
        'cuDNN 8 for deep learning',
        'Multi-GPU support',
        'Batch processing optimization',
    ]
    for c in gpu_caps:
        pdf.cell(0, 5, f'  * {c}', 0, 1)
    
    # ===== Container 7: Image Enhancement =====
    pdf.add_page()
    pdf.add_container_section(
        title='7. Image Enhancement Container',
        port='8019',
        base_image='python:3.11-slim',
        purpose='AI-powered image enhancement for better disease detection including noise reduction, contrast adjustment, and super-resolution.',
        dockerfile_content='''# Image Enhancement Container
FROM python:3.11-slim

RUN apt-get update && apt-get install -y \\
    gcc g++ curl \\
    libopencv-dev python3-opencv \\
    libglib2.0-0 libsm6 libxext6 libxrender-dev libgomp1 \\
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY src/ ./src/
COPY config/ ./config/

RUN mkdir -p /app/data/{input,output,processed,enhanced,filters,logs}

ENV PYTHONPATH=/app
ENV ENHANCEMENT_PORT=8019
ENV MAX_IMAGE_SIZE=4096
ENV QUALITY_LEVEL=95

EXPOSE 8019

HEALTHCHECK --interval=30s --timeout=10s --retries=3 \\
    CMD curl -f http://localhost:8019/health || exit 1

CMD ["python", "src/image_enhancement_service.py"]'''
    )
    
    # ===== Container 8: Adaptive Learning =====
    pdf.add_page()
    pdf.add_container_section(
        title='8. Adaptive Learning Container',
        port='8017',
        base_image='python:3.11-slim',
        purpose='Self-improving AI system that learns from new data and adapts models based on feedback.',
        dockerfile_content='''# Adaptive Learning Container
FROM python:3.11-slim

RUN apt-get update && apt-get install -y \\
    gcc g++ curl \\
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY src/ ./src/
COPY config/ ./config/

RUN mkdir -p /app/data/{models,training,adaptation,logs}

ENV PYTHONPATH=/app
ENV ADAPTIVE_PORT=8017
ENV LEARNING_RATE=0.001
ENV ADAPTATION_THRESHOLD=0.85

EXPOSE 8017

HEALTHCHECK --interval=30s --timeout=15s --start-period=90s --retries=3 \\
    CMD curl -f http://localhost:8017/health || exit 1

CMD ["python", "src/adaptive_learning_service.py"]'''
    )
    
    # ===== Container 9: Analytics =====
    pdf.add_page()
    pdf.add_container_section(
        title='9. Analytics Container',
        port='8002',
        base_image='python:3.11-slim',
        purpose='Big data analytics and predictions for agricultural data including yield forecasting and trend analysis.',
        dockerfile_content='''# Analytics Container
FROM python:3.11-slim as analytics-base

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/app

RUN apt-get update && apt-get install -y \\
    gcc g++ libgomp1 curl \\
    && rm -rf /var/lib/apt/lists/*

RUN groupadd -r analytics && useradd -r -g analytics analytics
RUN mkdir -p /app /app/data /app/reports /app/logs

WORKDIR /app
COPY docker/analytics/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY src/advanced_analytics_system.py ./
COPY src/big_data_analytics_system.py ./
COPY src/modules/analytics/ ./analytics/

USER analytics
EXPOSE 8002

HEALTHCHECK --interval=30s --timeout=10s --retries=3 \\
    CMD curl -f http://localhost:8002/health || exit 1

CMD ["uvicorn", "analytics.api:app", "--host", "0.0.0.0", "--port", "8002"]'''
    )
    
    # ===== Summary Page =====
    pdf.add_page()
    pdf.set_font('Helvetica', 'B', 18)
    pdf.cell(0, 15, 'Summary: AI/ML Container Architecture', 0, 1, 'C')
    pdf.ln(10)
    
    # Architecture diagram (text representation)
    pdf.set_font('Courier', '', 9)
    architecture = '''
    +----------------------------------------------------------+
    |                    GAARA AI SYSTEM                        |
    +----------------------------------------------------------+
    |                                                          |
    |  +----------------+    +------------------+               |
    |  | Plant Disease  |    | YOLO Detection   |               |
    |  | Diagnosis      |    | (Port 8018)      |               |
    |  | (Port 8001)    |    +------------------+               |
    |  +----------------+                                       |
    |                                                          |
    |  +----------------+    +------------------+               |
    |  | ResNet-50      |    | GPU Processing   |               |
    |  | (Port 8003)    |    | (Port 8020)      |               |
    |  +----------------+    +------------------+               |
    |                                                          |
    |  +----------------+    +------------------+               |
    |  | Plant          |    | Plant Disease    |               |
    |  | Hybridization  |    | Advanced         |               |
    |  | (Port 8022)    |    | (Port 8021)      |               |
    |  +----------------+    +------------------+               |
    |                                                          |
    |  +----------------+    +------------------+               |
    |  | Adaptive       |    | Image            |               |
    |  | Learning       |    | Enhancement      |               |
    |  | (Port 8017)    |    | (Port 8019)      |               |
    |  +----------------+    +------------------+               |
    |                                                          |
    |  +----------------+    +------------------+               |
    |  | Analytics      |    | Memory Central   |               |
    |  | (Port 8002)    |    | (Port 8014)      |               |
    |  +----------------+    +------------------+               |
    |                                                          |
    +----------------------------------------------------------+
    '''
    
    for line in architecture.split('\n'):
        pdf.cell(0, 4, line, 0, 1)
    
    pdf.ln(10)
    
    # Port Summary Table
    pdf.set_font('Helvetica', 'B', 12)
    pdf.cell(0, 8, 'Port Summary:', 0, 1, 'L')
    
    ports_data = [
        ('8001', 'Disease Diagnosis', 'PyTorch, ResNet-50'),
        ('8002', 'Analytics', 'Pandas, NumPy, Scikit-learn'),
        ('8003', 'ResNet-50', 'PyTorch, TorchVision'),
        ('8017', 'Adaptive Learning', 'TensorFlow, Custom ML'),
        ('8018', 'YOLO Detection', 'Ultralytics YOLOv8'),
        ('8019', 'Image Enhancement', 'OpenCV, PIL'),
        ('8020', 'GPU Processing', 'CUDA, cuDNN'),
        ('8021', 'Plant Disease Advanced', 'OpenCV, ML Models'),
        ('8022', 'Plant Hybridization', 'Genetic Algorithms, NumPy'),
    ]
    
    pdf.set_fill_color(220, 220, 220)
    pdf.set_font('Helvetica', 'B', 9)
    pdf.cell(25, 7, 'Port', 1, 0, 'C', fill=True)
    pdf.cell(55, 7, 'Service', 1, 0, 'C', fill=True)
    pdf.cell(110, 7, 'Technologies', 1, 1, 'C', fill=True)
    
    pdf.set_font('Helvetica', '', 9)
    for port, service, tech in ports_data:
        pdf.cell(25, 6, port, 1, 0, 'C')
        pdf.cell(55, 6, service, 1, 0, 'L')
        pdf.cell(110, 6, tech, 1, 1, 'L')
    
    # Save PDF
    output_path = os.path.join(os.path.dirname(__file__), 'docs', 'Gaara_AI_ML_Containers.pdf')
    pdf.output(output_path)
    print(f"PDF generated successfully: {output_path}")
    return output_path


if __name__ == '__main__':
    create_pdf()

