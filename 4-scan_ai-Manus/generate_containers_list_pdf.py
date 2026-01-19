#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Generate PDF with AI/ML Container Names for Gaara AI project.
"""

from fpdf import FPDF
from datetime import datetime

class ContainersPDF(FPDF):
    def header(self):
        self.set_font('Helvetica', 'B', 14)
        self.set_fill_color(46, 134, 193)
        self.set_text_color(255, 255, 255)
        self.cell(0, 12, 'Gaara AI - Container Names Reference', 0, new_y='NEXT', align='C', fill=True)
        self.set_text_color(0, 0, 0)
        self.ln(5)
        
    def footer(self):
        self.set_y(-15)
        self.set_font('Helvetica', 'I', 8)
        self.cell(0, 10, f'Page {self.page_no()} | {datetime.now().strftime("%Y-%m-%d")}', 0, align='C')


def create_pdf():
    pdf = ContainersPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    
    # Title
    pdf.set_font('Helvetica', 'B', 24)
    pdf.ln(10)
    pdf.cell(0, 15, 'AI/ML Container Names', new_y='NEXT', align='C')
    pdf.set_font('Helvetica', '', 12)
    pdf.cell(0, 8, 'Hybridization, Diagnosis & Detection Services', new_y='NEXT', align='C')
    pdf.ln(15)
    
    # ===== Section 1: Hybridization =====
    pdf.set_font('Helvetica', 'B', 14)
    pdf.set_fill_color(39, 174, 96)
    pdf.set_text_color(255, 255, 255)
    pdf.cell(0, 10, '1. HYBRIDIZATION (Plant Breeding)', fill=True, new_y='NEXT')
    pdf.set_text_color(0, 0, 0)
    pdf.ln(3)
    
    pdf.set_font('Courier', 'B', 11)
    pdf.set_fill_color(240, 240, 240)
    pdf.cell(0, 8, 'Container: gaara-plant-hybridization-service', fill=True, new_y='NEXT')
    pdf.set_font('Helvetica', '', 10)
    pdf.cell(50, 6, 'Port:', new_x='RIGHT')
    pdf.cell(0, 6, '8022', new_y='NEXT')
    pdf.cell(50, 6, 'Dockerfile:', new_x='RIGHT')
    pdf.cell(0, 6, 'docker/plant_hybridization/Dockerfile', new_y='NEXT')
    pdf.cell(50, 6, 'Base Image:', new_x='RIGHT')
    pdf.cell(0, 6, 'python:3.11-slim', new_y='NEXT')
    pdf.cell(50, 6, 'Purpose:', new_x='RIGHT')
    pdf.cell(0, 6, 'Genetic algorithms for plant breeding simulation', new_y='NEXT')
    pdf.ln(8)
    
    # ===== Section 2: Diagnosis =====
    pdf.set_font('Helvetica', 'B', 14)
    pdf.set_fill_color(231, 76, 60)
    pdf.set_text_color(255, 255, 255)
    pdf.cell(0, 10, '2. DIAGNOSIS (Disease Detection)', fill=True, new_y='NEXT')
    pdf.set_text_color(0, 0, 0)
    pdf.ln(3)
    
    # Diagnosis Service
    pdf.set_font('Courier', 'B', 11)
    pdf.set_fill_color(240, 240, 240)
    pdf.cell(0, 8, 'Container: gaara-diagnosis-service', fill=True, new_y='NEXT')
    pdf.set_font('Helvetica', '', 10)
    pdf.cell(50, 6, 'Port:', new_x='RIGHT')
    pdf.cell(0, 6, '8001', new_y='NEXT')
    pdf.cell(50, 6, 'Dockerfile:', new_x='RIGHT')
    pdf.cell(0, 6, 'docker/diagnosis/Dockerfile', new_y='NEXT')
    pdf.cell(50, 6, 'Base Image:', new_x='RIGHT')
    pdf.cell(0, 6, 'python:3.11-slim', new_y='NEXT')
    pdf.cell(50, 6, 'Purpose:', new_x='RIGHT')
    pdf.cell(0, 6, 'AI-powered plant disease diagnosis with ResNet-50', new_y='NEXT')
    pdf.ln(5)
    
    # Plant Disease Advanced
    pdf.set_font('Courier', 'B', 11)
    pdf.cell(0, 8, 'Container: gaara-plant-disease-advanced-service', fill=True, new_y='NEXT')
    pdf.set_font('Helvetica', '', 10)
    pdf.cell(50, 6, 'Port:', new_x='RIGHT')
    pdf.cell(0, 6, '8021', new_y='NEXT')
    pdf.cell(50, 6, 'Dockerfile:', new_x='RIGHT')
    pdf.cell(0, 6, 'docker/plant_disease_advanced/Dockerfile', new_y='NEXT')
    pdf.cell(50, 6, 'Base Image:', new_x='RIGHT')
    pdf.cell(0, 6, 'python:3.11-slim', new_y='NEXT')
    pdf.cell(50, 6, 'Purpose:', new_x='RIGHT')
    pdf.cell(0, 6, 'Advanced disease detection with knowledge base', new_y='NEXT')
    pdf.ln(8)
    
    # ===== Section 3: YOLO Detection =====
    pdf.set_font('Helvetica', 'B', 14)
    pdf.set_fill_color(155, 89, 182)
    pdf.set_text_color(255, 255, 255)
    pdf.cell(0, 10, '3. YOLO DETECTION (Object Detection)', fill=True, new_y='NEXT')
    pdf.set_text_color(0, 0, 0)
    pdf.ln(3)
    
    pdf.set_font('Courier', 'B', 11)
    pdf.set_fill_color(240, 240, 240)
    pdf.cell(0, 8, 'Container: gaara-yolo-detection-service', fill=True, new_y='NEXT')
    pdf.set_font('Helvetica', '', 10)
    pdf.cell(50, 6, 'Port:', new_x='RIGHT')
    pdf.cell(0, 6, '8018', new_y='NEXT')
    pdf.cell(50, 6, 'Dockerfile:', new_x='RIGHT')
    pdf.cell(0, 6, 'docker/yolo_detection/Dockerfile', new_y='NEXT')
    pdf.cell(50, 6, 'Base Image:', new_x='RIGHT')
    pdf.cell(0, 6, 'ultralytics/ultralytics:latest', new_y='NEXT')
    pdf.cell(50, 6, 'Models:', new_x='RIGHT')
    pdf.cell(0, 6, 'YOLOv8n, YOLOv8s, YOLOv8m', new_y='NEXT')
    pdf.cell(50, 6, 'Purpose:', new_x='RIGHT')
    pdf.cell(0, 6, 'Real-time object & disease detection', new_y='NEXT')
    pdf.ln(8)
    
    # ===== Section 4: ResNet-50 =====
    pdf.set_font('Helvetica', 'B', 14)
    pdf.set_fill_color(41, 128, 185)
    pdf.set_text_color(255, 255, 255)
    pdf.cell(0, 10, '4. RESNET-50 (Computer Vision)', fill=True, new_y='NEXT')
    pdf.set_text_color(0, 0, 0)
    pdf.ln(3)
    
    pdf.set_font('Courier', 'B', 11)
    pdf.set_fill_color(240, 240, 240)
    pdf.cell(0, 8, 'Container: gaara-resnet50-service', fill=True, new_y='NEXT')
    pdf.set_font('Helvetica', '', 10)
    pdf.cell(50, 6, 'Port:', new_x='RIGHT')
    pdf.cell(0, 6, '8003', new_y='NEXT')
    pdf.cell(50, 6, 'Dockerfile:', new_x='RIGHT')
    pdf.cell(0, 6, 'docker/resnet50/Dockerfile', new_y='NEXT')
    pdf.cell(50, 6, 'Base Image:', new_x='RIGHT')
    pdf.cell(0, 6, 'python:3.11-slim (multi-stage)', new_y='NEXT')
    pdf.cell(50, 6, 'Model:', new_x='RIGHT')
    pdf.cell(0, 6, 'ResNet-50 (pre-trained on ImageNet)', new_y='NEXT')
    pdf.cell(50, 6, 'Purpose:', new_x='RIGHT')
    pdf.cell(0, 6, 'Image classification & feature extraction', new_y='NEXT')
    pdf.ln(8)
    
    # ===== Section 5: GPU Processing =====
    pdf.set_font('Helvetica', 'B', 14)
    pdf.set_fill_color(243, 156, 18)
    pdf.set_text_color(255, 255, 255)
    pdf.cell(0, 10, '5. GPU PROCESSING (CUDA Acceleration)', fill=True, new_y='NEXT')
    pdf.set_text_color(0, 0, 0)
    pdf.ln(3)
    
    pdf.set_font('Courier', 'B', 11)
    pdf.set_fill_color(240, 240, 240)
    pdf.cell(0, 8, 'Container: gaara-gpu-processing-service', fill=True, new_y='NEXT')
    pdf.set_font('Helvetica', '', 10)
    pdf.cell(50, 6, 'Port:', new_x='RIGHT')
    pdf.cell(0, 6, '8020', new_y='NEXT')
    pdf.cell(50, 6, 'Dockerfile:', new_x='RIGHT')
    pdf.cell(0, 6, 'docker/gpu_processing/Dockerfile', new_y='NEXT')
    pdf.cell(50, 6, 'Base Image:', new_x='RIGHT')
    pdf.cell(0, 6, 'nvidia/cuda:11.8-devel-ubuntu20.04', new_y='NEXT')
    pdf.cell(50, 6, 'Purpose:', new_x='RIGHT')
    pdf.cell(0, 6, 'GPU-accelerated AI model inference', new_y='NEXT')
    
    # ===== Page 2 =====
    pdf.add_page()
    
    # ===== Section 6: Image Enhancement =====
    pdf.set_font('Helvetica', 'B', 14)
    pdf.set_fill_color(26, 188, 156)
    pdf.set_text_color(255, 255, 255)
    pdf.cell(0, 10, '6. IMAGE ENHANCEMENT', fill=True, new_y='NEXT')
    pdf.set_text_color(0, 0, 0)
    pdf.ln(3)
    
    pdf.set_font('Courier', 'B', 11)
    pdf.set_fill_color(240, 240, 240)
    pdf.cell(0, 8, 'Container: gaara-image-enhancement-service', fill=True, new_y='NEXT')
    pdf.set_font('Helvetica', '', 10)
    pdf.cell(50, 6, 'Port:', new_x='RIGHT')
    pdf.cell(0, 6, '8019', new_y='NEXT')
    pdf.cell(50, 6, 'Dockerfile:', new_x='RIGHT')
    pdf.cell(0, 6, 'docker/image_enhancement/Dockerfile', new_y='NEXT')
    pdf.cell(50, 6, 'Base Image:', new_x='RIGHT')
    pdf.cell(0, 6, 'python:3.11-slim', new_y='NEXT')
    pdf.cell(50, 6, 'Purpose:', new_x='RIGHT')
    pdf.cell(0, 6, 'Image preprocessing & quality enhancement', new_y='NEXT')
    pdf.ln(8)
    
    # ===== Section 7: Learning Services =====
    pdf.set_font('Helvetica', 'B', 14)
    pdf.set_fill_color(52, 73, 94)
    pdf.set_text_color(255, 255, 255)
    pdf.cell(0, 10, '7. LEARNING SERVICES', fill=True, new_y='NEXT')
    pdf.set_text_color(0, 0, 0)
    pdf.ln(3)
    
    # Adaptive Learning
    pdf.set_font('Courier', 'B', 11)
    pdf.set_fill_color(240, 240, 240)
    pdf.cell(0, 8, 'Container: gaara-adaptive-learning-service', fill=True, new_y='NEXT')
    pdf.set_font('Helvetica', '', 10)
    pdf.cell(50, 6, 'Port:', new_x='RIGHT')
    pdf.cell(0, 6, '8017', new_y='NEXT')
    pdf.cell(50, 6, 'Dockerfile:', new_x='RIGHT')
    pdf.cell(0, 6, 'docker/adaptive_learning/Dockerfile', new_y='NEXT')
    pdf.cell(50, 6, 'Purpose:', new_x='RIGHT')
    pdf.cell(0, 6, 'Self-improving AI models based on feedback', new_y='NEXT')
    pdf.ln(5)
    
    # Auto Learning
    pdf.set_font('Courier', 'B', 11)
    pdf.cell(0, 8, 'Container: gaara-auto-learning-service', fill=True, new_y='NEXT')
    pdf.set_font('Helvetica', '', 10)
    pdf.cell(50, 6, 'Port:', new_x='RIGHT')
    pdf.cell(0, 6, '8015', new_y='NEXT')
    pdf.cell(50, 6, 'Dockerfile:', new_x='RIGHT')
    pdf.cell(0, 6, 'docker/auto_learning/Dockerfile', new_y='NEXT')
    pdf.cell(50, 6, 'Purpose:', new_x='RIGHT')
    pdf.cell(0, 6, 'Automatic model training & updates', new_y='NEXT')
    pdf.ln(8)
    
    # ===== Section 8: Analytics =====
    pdf.set_font('Helvetica', 'B', 14)
    pdf.set_fill_color(142, 68, 173)
    pdf.set_text_color(255, 255, 255)
    pdf.cell(0, 10, '8. ANALYTICS', fill=True, new_y='NEXT')
    pdf.set_text_color(0, 0, 0)
    pdf.ln(3)
    
    pdf.set_font('Courier', 'B', 11)
    pdf.set_fill_color(240, 240, 240)
    pdf.cell(0, 8, 'Container: gaara-analytics-service', fill=True, new_y='NEXT')
    pdf.set_font('Helvetica', '', 10)
    pdf.cell(50, 6, 'Port:', new_x='RIGHT')
    pdf.cell(0, 6, '8002', new_y='NEXT')
    pdf.cell(50, 6, 'Dockerfile:', new_x='RIGHT')
    pdf.cell(0, 6, 'docker/analytics/Dockerfile', new_y='NEXT')
    pdf.cell(50, 6, 'Purpose:', new_x='RIGHT')
    pdf.cell(0, 6, 'Big data analytics & predictions', new_y='NEXT')
    pdf.ln(8)
    
    # ===== Section 9: AI Agents =====
    pdf.set_font('Helvetica', 'B', 14)
    pdf.set_fill_color(230, 126, 34)
    pdf.set_text_color(255, 255, 255)
    pdf.cell(0, 10, '9. AI AGENTS', fill=True, new_y='NEXT')
    pdf.set_text_color(0, 0, 0)
    pdf.ln(3)
    
    pdf.set_font('Courier', 'B', 11)
    pdf.set_fill_color(240, 240, 240)
    pdf.cell(0, 8, 'Container: gaara-ai-agents-service', fill=True, new_y='NEXT')
    pdf.set_font('Helvetica', '', 10)
    pdf.cell(50, 6, 'Port:', new_x='RIGHT')
    pdf.cell(0, 6, '8004', new_y='NEXT')
    pdf.cell(50, 6, 'Dockerfile:', new_x='RIGHT')
    pdf.cell(0, 6, 'docker/ai_agents/Dockerfile', new_y='NEXT')
    pdf.cell(50, 6, 'Purpose:', new_x='RIGHT')
    pdf.cell(0, 6, 'Multi-agent AI coordination system', new_y='NEXT')
    pdf.ln(10)
    
    # ===== Quick Reference Table =====
    pdf.set_font('Helvetica', 'B', 14)
    pdf.set_fill_color(44, 62, 80)
    pdf.set_text_color(255, 255, 255)
    pdf.cell(0, 10, 'QUICK REFERENCE TABLE', fill=True, new_y='NEXT')
    pdf.set_text_color(0, 0, 0)
    pdf.ln(5)
    
    # Table header
    pdf.set_font('Helvetica', 'B', 9)
    pdf.set_fill_color(200, 200, 200)
    pdf.cell(75, 7, 'Container Name', 1, align='C', fill=True)
    pdf.cell(20, 7, 'Port', 1, align='C', fill=True)
    pdf.cell(95, 7, 'Service', 1, new_y='NEXT', align='C', fill=True)
    
    # Table data
    containers = [
        ('gaara-plant-hybridization-service', '8022', 'Plant Hybridization'),
        ('gaara-diagnosis-service', '8001', 'Disease Diagnosis'),
        ('gaara-plant-disease-advanced-service', '8021', 'Advanced Disease Detection'),
        ('gaara-yolo-detection-service', '8018', 'YOLO Object Detection'),
        ('gaara-resnet50-service', '8003', 'ResNet-50 Vision'),
        ('gaara-gpu-processing-service', '8020', 'GPU Processing'),
        ('gaara-image-enhancement-service', '8019', 'Image Enhancement'),
        ('gaara-adaptive-learning-service', '8017', 'Adaptive Learning'),
        ('gaara-auto-learning-service', '8015', 'Auto Learning'),
        ('gaara-analytics-service', '8002', 'Analytics'),
        ('gaara-ai-agents-service', '8004', 'AI Agents'),
        ('gaara-memory-service', '8005', 'Memory System'),
        ('gaara-vector-db-service', '8006', 'Vector Database'),
    ]
    
    pdf.set_font('Courier', '', 8)
    for name, port, service in containers:
        pdf.cell(75, 6, name, 1)
        pdf.cell(20, 6, port, 1, align='C')
        pdf.cell(95, 6, service, 1, new_y='NEXT')
    
    # Save
    output_path = 'docs/Gaara_AI_Container_Names.pdf'
    pdf.output(output_path)
    print(f"PDF generated: {output_path}")
    return output_path


if __name__ == '__main__':
    create_pdf()

