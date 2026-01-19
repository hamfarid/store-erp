#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Generate PDF report of all tools and technologies used in Gaara AI project.
"""

from fpdf import FPDF
import os
from datetime import datetime

class ArabicPDF(FPDF):
    """Custom PDF class with Arabic support."""
    
    def __init__(self):
        super().__init__()
        # Add Arabic-compatible font (DejaVu)
        font_path = os.path.join(os.path.dirname(__file__), 'fonts')
        if os.path.exists(os.path.join(font_path, 'DejaVuSans.ttf')):
            self.add_font('DejaVu', '', os.path.join(font_path, 'DejaVuSans.ttf'), uni=True)
            self.add_font('DejaVu', 'B', os.path.join(font_path, 'DejaVuSans-Bold.ttf'), uni=True)
        
    def header(self):
        self.set_font('Helvetica', 'B', 12)
        self.cell(0, 10, 'Gaara AI - Project Tools & Technologies', 0, 1, 'C')
        self.ln(5)
        
    def footer(self):
        self.set_y(-15)
        self.set_font('Helvetica', 'I', 8)
        self.cell(0, 10, f'Page {self.page_no()}/{{nb}}', 0, 0, 'C')


def create_pdf():
    """Generate the PDF report."""
    
    pdf = ArabicPDF()
    pdf.alias_nb_pages()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)
    
    # Title
    pdf.set_font('Helvetica', 'B', 24)
    pdf.cell(0, 20, 'Gaara AI Project', 0, 1, 'C')
    pdf.set_font('Helvetica', 'B', 18)
    pdf.cell(0, 10, 'Tools & Technologies Report', 0, 1, 'C')
    pdf.set_font('Helvetica', '', 12)
    pdf.cell(0, 10, f'Generated: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}', 0, 1, 'C')
    pdf.cell(0, 10, 'Version: 4.3', 0, 1, 'C')
    pdf.ln(10)
    
    # ===== SECTION 1: Docker Containers =====
    pdf.set_font('Helvetica', 'B', 16)
    pdf.set_fill_color(41, 128, 185)
    pdf.set_text_color(255, 255, 255)
    pdf.cell(0, 10, '1. Docker Containers', 0, 1, 'L', fill=True)
    pdf.set_text_color(0, 0, 0)
    pdf.ln(5)
    
    # Core Containers
    pdf.set_font('Helvetica', 'B', 12)
    pdf.cell(0, 8, '1.1 Core Containers', 0, 1)
    pdf.set_font('Helvetica', '', 10)
    
    core_containers = [
        ('PostgreSQL', 'postgres:16-alpine', 'Main Database', '5432'),
        ('Redis', 'redis:7-alpine', 'Cache & Sessions', '6379'),
        ('Backend', 'Custom Dockerfile', 'FastAPI Backend', '5000'),
        ('Frontend', 'Custom Dockerfile', 'React Frontend', '80/443'),
        ('Nginx', 'nginx:1.25-alpine', 'Reverse Proxy', '8080/8443'),
    ]
    
    # Table header
    pdf.set_fill_color(220, 220, 220)
    pdf.set_font('Helvetica', 'B', 9)
    pdf.cell(40, 7, 'Container', 1, 0, 'C', fill=True)
    pdf.cell(50, 7, 'Image', 1, 0, 'C', fill=True)
    pdf.cell(60, 7, 'Purpose', 1, 0, 'C', fill=True)
    pdf.cell(30, 7, 'Port', 1, 1, 'C', fill=True)
    
    pdf.set_font('Helvetica', '', 9)
    for name, image, purpose, port in core_containers:
        pdf.cell(40, 6, name, 1)
        pdf.cell(50, 6, image, 1)
        pdf.cell(60, 6, purpose, 1)
        pdf.cell(30, 6, port, 1, 1)
    pdf.ln(5)
    
    # Monitoring Containers
    pdf.set_font('Helvetica', 'B', 12)
    pdf.cell(0, 8, '1.2 Monitoring Containers', 0, 1)
    
    monitoring = [
        ('Prometheus', 'prom/prometheus:v2.48.0', 'Metrics Collection', '9090'),
        ('Grafana', 'grafana/grafana:10.2.2', 'Dashboards', '3001'),
        ('Elasticsearch', 'elasticsearch:8.11.0', 'Search & Analytics', '9200'),
        ('Kibana', 'kibana:8.11.0', 'ES Interface', '5601'),
    ]
    
    pdf.set_fill_color(220, 220, 220)
    pdf.set_font('Helvetica', 'B', 9)
    pdf.cell(40, 7, 'Container', 1, 0, 'C', fill=True)
    pdf.cell(55, 7, 'Image', 1, 0, 'C', fill=True)
    pdf.cell(55, 7, 'Purpose', 1, 0, 'C', fill=True)
    pdf.cell(30, 7, 'Port', 1, 1, 'C', fill=True)
    
    pdf.set_font('Helvetica', '', 9)
    for name, image, purpose, port in monitoring:
        pdf.cell(40, 6, name, 1)
        pdf.cell(55, 6, image, 1)
        pdf.cell(55, 6, purpose, 1)
        pdf.cell(30, 6, port, 1, 1)
    pdf.ln(5)
    
    # AI Containers
    pdf.set_font('Helvetica', 'B', 12)
    pdf.cell(0, 8, '1.3 AI/ML Specialized Containers', 0, 1)
    
    ai_containers = [
        'plant_hybridization - Plant Hybridization',
        'plant_disease_advanced - Advanced Plant Disease Detection',
        'gpu_processing - GPU Processing',
        'image_enhancement - Image Enhancement',
        'yolo_detection - YOLO Object Detection',
        'adaptive_learning - Adaptive Learning',
        'resnet50 - ResNet50 Model',
        'diagnosis - Disease Diagnosis',
        'analytics - Analytics Processing',
        'memory_central - Central Memory System',
        'a2a_communication - Agent-to-Agent Communication',
        'auto_learning - Automatic Learning',
    ]
    
    pdf.set_font('Helvetica', '', 9)
    for i, container in enumerate(ai_containers, 1):
        pdf.cell(0, 5, f"  {i}. {container}", 0, 1)
    pdf.ln(5)
    
    # ===== SECTION 2: Security Tools =====
    pdf.add_page()
    pdf.set_font('Helvetica', 'B', 16)
    pdf.set_fill_color(231, 76, 60)
    pdf.set_text_color(255, 255, 255)
    pdf.cell(0, 10, '2. Security Tools', 0, 1, 'L', fill=True)
    pdf.set_text_color(0, 0, 0)
    pdf.ln(5)
    
    # GitHub Actions Security
    pdf.set_font('Helvetica', 'B', 12)
    pdf.cell(0, 8, '2.1 GitHub Actions Security Workflows', 0, 1)
    
    security_workflows = [
        ('Trivy', 'trivy-security.yml', 'Vulnerability Scanning'),
        ('OWASP ZAP', 'dast_zap.yml', 'Dynamic Application Security Testing'),
        ('Secret Scan', 'secret-scan.yml', 'Detect Leaked Secrets'),
        ('SBOM', 'sbom_supply_chain.yml', 'Software Bill of Materials'),
    ]
    
    pdf.set_fill_color(220, 220, 220)
    pdf.set_font('Helvetica', 'B', 9)
    pdf.cell(40, 7, 'Tool', 1, 0, 'C', fill=True)
    pdf.cell(60, 7, 'Workflow File', 1, 0, 'C', fill=True)
    pdf.cell(80, 7, 'Purpose', 1, 1, 'C', fill=True)
    
    pdf.set_font('Helvetica', '', 9)
    for tool, file, purpose in security_workflows:
        pdf.cell(40, 6, tool, 1)
        pdf.cell(60, 6, file, 1)
        pdf.cell(80, 6, purpose, 1, 1)
    pdf.ln(5)
    
    # Trivy Tasks
    pdf.set_font('Helvetica', 'B', 12)
    pdf.cell(0, 8, '2.2 Trivy Security Tasks', 0, 1)
    
    trivy_tasks = [
        'Filesystem Vulnerability Scan',
        'Docker Image Scan (Backend)',
        'Docker Image Scan (Frontend)',
        'Infrastructure as Code (IaC) Scan',
        'Secret Detection',
        'SBOM Generation (CycloneDX format)',
        'Security Report Summary',
    ]
    
    pdf.set_font('Helvetica', '', 9)
    for task in trivy_tasks:
        pdf.cell(0, 5, f"  - {task}", 0, 1)
    pdf.ln(5)
    
    # Security Libraries
    pdf.set_font('Helvetica', 'B', 12)
    pdf.cell(0, 8, '2.3 Security Libraries (Backend)', 0, 1)
    
    security_libs = [
        ('python-jose', '3.3.0', 'JWT Signing'),
        ('passlib', '1.7.4', 'Password Hashing'),
        ('bcrypt', '4.1.2', 'Encryption Algorithm'),
        ('cryptography', '45.0.4', 'Cryptographic Operations'),
        ('PyJWT', '2.10.1', 'JSON Web Tokens'),
        ('pyotp', '2.9.0', 'TOTP (2FA)'),
        ('pyOpenSSL', '25.1.0', 'SSL/TLS'),
    ]
    
    pdf.set_fill_color(220, 220, 220)
    pdf.set_font('Helvetica', 'B', 9)
    pdf.cell(50, 7, 'Library', 1, 0, 'C', fill=True)
    pdf.cell(30, 7, 'Version', 1, 0, 'C', fill=True)
    pdf.cell(100, 7, 'Purpose', 1, 1, 'C', fill=True)
    
    pdf.set_font('Helvetica', '', 9)
    for lib, ver, purpose in security_libs:
        pdf.cell(50, 6, lib, 1)
        pdf.cell(30, 6, ver, 1)
        pdf.cell(100, 6, purpose, 1, 1)
    pdf.ln(5)
    
    # ===== SECTION 3: Testing Tools =====
    pdf.add_page()
    pdf.set_font('Helvetica', 'B', 16)
    pdf.set_fill_color(46, 204, 113)
    pdf.set_text_color(255, 255, 255)
    pdf.cell(0, 10, '3. Testing Tools', 0, 1, 'L', fill=True)
    pdf.set_text_color(0, 0, 0)
    pdf.ln(5)
    
    # Backend Testing
    pdf.set_font('Helvetica', 'B', 12)
    pdf.cell(0, 8, '3.1 Backend Testing', 0, 1)
    
    backend_testing = [
        ('pytest', '8.3.5', 'Test Framework'),
        ('pytest-asyncio', '0.21.1', 'Async Testing'),
        ('pytest-cov', '4.1.0', 'Code Coverage'),
        ('playwright', '1.52.0', 'E2E Testing'),
        ('httpx', '0.25.2', 'HTTP Testing Client'),
    ]
    
    pdf.set_fill_color(220, 220, 220)
    pdf.set_font('Helvetica', 'B', 9)
    pdf.cell(50, 7, 'Tool', 1, 0, 'C', fill=True)
    pdf.cell(30, 7, 'Version', 1, 0, 'C', fill=True)
    pdf.cell(100, 7, 'Purpose', 1, 1, 'C', fill=True)
    
    pdf.set_font('Helvetica', '', 9)
    for tool, ver, purpose in backend_testing:
        pdf.cell(50, 6, tool, 1)
        pdf.cell(30, 6, ver, 1)
        pdf.cell(100, 6, purpose, 1, 1)
    pdf.ln(5)
    
    # Frontend Testing
    pdf.set_font('Helvetica', 'B', 12)
    pdf.cell(0, 8, '3.2 Frontend Testing', 0, 1)
    
    frontend_testing = [
        ('vitest', '1.0.4', 'Test Framework'),
        ('@testing-library/react', '14.1.2', 'React Testing'),
        ('jsdom', '23.0.1', 'Virtual DOM'),
        ('storybook', '7.6.6', 'Component Documentation'),
        ('msw', '2.0.11', 'Mock Service Worker'),
    ]
    
    pdf.set_fill_color(220, 220, 220)
    pdf.set_font('Helvetica', 'B', 9)
    pdf.cell(60, 7, 'Tool', 1, 0, 'C', fill=True)
    pdf.cell(30, 7, 'Version', 1, 0, 'C', fill=True)
    pdf.cell(90, 7, 'Purpose', 1, 1, 'C', fill=True)
    
    pdf.set_font('Helvetica', '', 9)
    for tool, ver, purpose in frontend_testing:
        pdf.cell(60, 6, tool, 1)
        pdf.cell(30, 6, ver, 1)
        pdf.cell(90, 6, purpose, 1, 1)
    pdf.ln(5)
    
    # Performance Testing
    pdf.set_font('Helvetica', 'B', 12)
    pdf.cell(0, 8, '3.3 Performance Testing', 0, 1)
    
    perf_testing = [
        ('k6', 'perf_k6.yml', 'Load Testing'),
        ('Lighthouse', 'lighthouse_ci.yml', 'Frontend Performance'),
    ]
    
    pdf.set_font('Helvetica', '', 9)
    for tool, file, purpose in perf_testing:
        pdf.cell(0, 5, f"  - {tool} ({file}): {purpose}", 0, 1)
    pdf.ln(5)
    
    # ===== SECTION 4: AI/ML Tools =====
    pdf.add_page()
    pdf.set_font('Helvetica', 'B', 16)
    pdf.set_fill_color(155, 89, 182)
    pdf.set_text_color(255, 255, 255)
    pdf.cell(0, 10, '4. AI/ML Tools', 0, 1, 'L', fill=True)
    pdf.set_text_color(0, 0, 0)
    pdf.ln(5)
    
    ai_tools = [
        ('torch', '2.1.1', 'PyTorch Deep Learning'),
        ('tensorflow', '2.15.0', 'TensorFlow'),
        ('scikit-learn', '1.3.2', 'Machine Learning'),
        ('opencv-python', '4.8.1.78', 'Image Processing'),
        ('scikit-image', '0.22.0', 'Image Processing'),
        ('onnx', '1.18.0', 'Model Exchange'),
        ('coremltools', '8.3.0', 'iOS Model Conversion'),
        ('numpy', '2.3.0', 'Numerical Computing'),
        ('pandas', '2.3.0', 'Data Processing'),
        ('Pillow', '11.2.1', 'Image Library'),
        ('matplotlib', '3.10.3', 'Visualization'),
    ]
    
    pdf.set_fill_color(220, 220, 220)
    pdf.set_font('Helvetica', 'B', 9)
    pdf.cell(50, 7, 'Library', 1, 0, 'C', fill=True)
    pdf.cell(30, 7, 'Version', 1, 0, 'C', fill=True)
    pdf.cell(100, 7, 'Purpose', 1, 1, 'C', fill=True)
    
    pdf.set_font('Helvetica', '', 9)
    for lib, ver, purpose in ai_tools:
        pdf.cell(50, 6, lib, 1)
        pdf.cell(30, 6, ver, 1)
        pdf.cell(100, 6, purpose, 1, 1)
    pdf.ln(5)
    
    # ===== SECTION 5: Backend Framework =====
    pdf.add_page()
    pdf.set_font('Helvetica', 'B', 16)
    pdf.set_fill_color(52, 73, 94)
    pdf.set_text_color(255, 255, 255)
    pdf.cell(0, 10, '5. Backend Framework', 0, 1, 'L', fill=True)
    pdf.set_text_color(0, 0, 0)
    pdf.ln(5)
    
    # Core Framework
    pdf.set_font('Helvetica', 'B', 12)
    pdf.cell(0, 8, '5.1 Core Framework', 0, 1)
    
    backend_core = [
        ('fastapi', '0.115.12', 'API Framework'),
        ('uvicorn', '0.24.0', 'ASGI Server'),
        ('pydantic', '2.11.7', 'Data Validation'),
        ('pydantic-settings', '2.1.0', 'Settings Management'),
        ('python-dotenv', '1.1.0', 'Environment Variables'),
    ]
    
    pdf.set_fill_color(220, 220, 220)
    pdf.set_font('Helvetica', 'B', 9)
    pdf.cell(50, 7, 'Library', 1, 0, 'C', fill=True)
    pdf.cell(30, 7, 'Version', 1, 0, 'C', fill=True)
    pdf.cell(100, 7, 'Purpose', 1, 1, 'C', fill=True)
    
    pdf.set_font('Helvetica', '', 9)
    for lib, ver, purpose in backend_core:
        pdf.cell(50, 6, lib, 1)
        pdf.cell(30, 6, ver, 1)
        pdf.cell(100, 6, purpose, 1, 1)
    pdf.ln(5)
    
    # Database
    pdf.set_font('Helvetica', 'B', 12)
    pdf.cell(0, 8, '5.2 Database', 0, 1)
    
    database = [
        ('sqlalchemy', '2.0.23', 'ORM'),
        ('alembic', '1.13.1', 'Database Migrations'),
        ('psycopg2-binary', '2.9.10', 'PostgreSQL Driver'),
        ('redis', '5.0.1', 'Redis Client'),
        ('aioredis', '2.0.1', 'Async Redis'),
    ]
    
    pdf.set_fill_color(220, 220, 220)
    pdf.set_font('Helvetica', 'B', 9)
    pdf.cell(50, 7, 'Library', 1, 0, 'C', fill=True)
    pdf.cell(30, 7, 'Version', 1, 0, 'C', fill=True)
    pdf.cell(100, 7, 'Purpose', 1, 1, 'C', fill=True)
    
    pdf.set_font('Helvetica', '', 9)
    for lib, ver, purpose in database:
        pdf.cell(50, 6, lib, 1)
        pdf.cell(30, 6, ver, 1)
        pdf.cell(100, 6, purpose, 1, 1)
    pdf.ln(5)
    
    # Task Queue
    pdf.set_font('Helvetica', 'B', 12)
    pdf.cell(0, 8, '5.3 Task Queue', 0, 1)
    
    task_queue = [
        ('celery', '5.3.4', 'Distributed Task Queue'),
        ('kombu', '5.3.4', 'Message Transport'),
        ('pika', '1.3.2', 'RabbitMQ Client'),
    ]
    
    pdf.set_fill_color(220, 220, 220)
    pdf.set_font('Helvetica', 'B', 9)
    pdf.cell(50, 7, 'Library', 1, 0, 'C', fill=True)
    pdf.cell(30, 7, 'Version', 1, 0, 'C', fill=True)
    pdf.cell(100, 7, 'Purpose', 1, 1, 'C', fill=True)
    
    pdf.set_font('Helvetica', '', 9)
    for lib, ver, purpose in task_queue:
        pdf.cell(50, 6, lib, 1)
        pdf.cell(30, 6, ver, 1)
        pdf.cell(100, 6, purpose, 1, 1)
    pdf.ln(5)
    
    # ===== SECTION 6: Frontend Framework =====
    pdf.add_page()
    pdf.set_font('Helvetica', 'B', 16)
    pdf.set_fill_color(230, 126, 34)
    pdf.set_text_color(255, 255, 255)
    pdf.cell(0, 10, '6. Frontend Framework', 0, 1, 'L', fill=True)
    pdf.set_text_color(0, 0, 0)
    pdf.ln(5)
    
    # Core Framework
    pdf.set_font('Helvetica', 'B', 12)
    pdf.cell(0, 8, '6.1 Core Framework', 0, 1)
    
    frontend_core = [
        ('react', '18.2.0', 'UI Framework'),
        ('react-dom', '18.2.0', 'DOM Rendering'),
        ('react-router-dom', '6.20.1', 'Routing'),
        ('vite', '5.0.10', 'Build Tool'),
        ('typescript', '5.3.3', 'Type Safety'),
    ]
    
    pdf.set_fill_color(220, 220, 220)
    pdf.set_font('Helvetica', 'B', 9)
    pdf.cell(50, 7, 'Library', 1, 0, 'C', fill=True)
    pdf.cell(30, 7, 'Version', 1, 0, 'C', fill=True)
    pdf.cell(100, 7, 'Purpose', 1, 1, 'C', fill=True)
    
    pdf.set_font('Helvetica', '', 9)
    for lib, ver, purpose in frontend_core:
        pdf.cell(50, 6, lib, 1)
        pdf.cell(30, 6, ver, 1)
        pdf.cell(100, 6, purpose, 1, 1)
    pdf.ln(5)
    
    # UI/Styling
    pdf.set_font('Helvetica', 'B', 12)
    pdf.cell(0, 8, '6.2 UI & Styling', 0, 1)
    
    ui_styling = [
        ('tailwindcss', '3.3.6', 'CSS Framework'),
        ('framer-motion', '10.16.16', 'Animations'),
        ('lucide-react', '0.294.0', 'Icons'),
        ('@radix-ui/*', 'various', 'UI Components'),
        ('react-hot-toast', '2.4.1', 'Notifications'),
    ]
    
    pdf.set_fill_color(220, 220, 220)
    pdf.set_font('Helvetica', 'B', 9)
    pdf.cell(50, 7, 'Library', 1, 0, 'C', fill=True)
    pdf.cell(30, 7, 'Version', 1, 0, 'C', fill=True)
    pdf.cell(100, 7, 'Purpose', 1, 1, 'C', fill=True)
    
    pdf.set_font('Helvetica', '', 9)
    for lib, ver, purpose in ui_styling:
        pdf.cell(50, 6, lib, 1)
        pdf.cell(30, 6, ver, 1)
        pdf.cell(100, 6, purpose, 1, 1)
    pdf.ln(5)
    
    # State Management
    pdf.set_font('Helvetica', 'B', 12)
    pdf.cell(0, 8, '6.3 State Management', 0, 1)
    
    state_mgmt = [
        ('zustand', '4.4.7', 'State Management'),
        ('@tanstack/react-query', '5.14.2', 'Server State'),
        ('immer', '10.0.3', 'Immutable State'),
        ('react-hook-form', '7.48.2', 'Form State'),
        ('zod', '3.22.4', 'Schema Validation'),
    ]
    
    pdf.set_fill_color(220, 220, 220)
    pdf.set_font('Helvetica', 'B', 9)
    pdf.cell(60, 7, 'Library', 1, 0, 'C', fill=True)
    pdf.cell(30, 7, 'Version', 1, 0, 'C', fill=True)
    pdf.cell(90, 7, 'Purpose', 1, 1, 'C', fill=True)
    
    pdf.set_font('Helvetica', '', 9)
    for lib, ver, purpose in state_mgmt:
        pdf.cell(60, 6, lib, 1)
        pdf.cell(30, 6, ver, 1)
        pdf.cell(90, 6, purpose, 1, 1)
    pdf.ln(5)
    
    # ===== SECTION 7: CI/CD =====
    pdf.add_page()
    pdf.set_font('Helvetica', 'B', 16)
    pdf.set_fill_color(26, 188, 156)
    pdf.set_text_color(255, 255, 255)
    pdf.cell(0, 10, '7. CI/CD (GitHub Actions)', 0, 1, 'L', fill=True)
    pdf.set_text_color(0, 0, 0)
    pdf.ln(5)
    
    cicd_workflows = [
        ('ci.yml', 'Continuous Integration'),
        ('deploy.yml', 'Automatic Deployment'),
        ('trivy-security.yml', 'Security Scanning'),
        ('dast_zap.yml', 'Dynamic Security Testing'),
        ('perf_k6.yml', 'Performance Testing'),
        ('lighthouse_ci.yml', 'Frontend Performance'),
        ('secret-scan.yml', 'Secret Detection'),
        ('sbom_supply_chain.yml', 'Supply Chain Security'),
        ('pages.yml', 'GitHub Pages'),
        ('audit.yml', 'Security Audit'),
        ('issues.yml', 'Issue Management'),
    ]
    
    pdf.set_fill_color(220, 220, 220)
    pdf.set_font('Helvetica', 'B', 9)
    pdf.cell(60, 7, 'Workflow', 1, 0, 'C', fill=True)
    pdf.cell(120, 7, 'Purpose', 1, 1, 'C', fill=True)
    
    pdf.set_font('Helvetica', '', 9)
    for workflow, purpose in cicd_workflows:
        pdf.cell(60, 6, workflow, 1)
        pdf.cell(120, 6, purpose, 1, 1)
    pdf.ln(5)
    
    # ===== SECTION 8: Monitoring =====
    pdf.set_font('Helvetica', 'B', 16)
    pdf.set_fill_color(142, 68, 173)
    pdf.set_text_color(255, 255, 255)
    pdf.cell(0, 10, '8. Monitoring & Observability', 0, 1, 'L', fill=True)
    pdf.set_text_color(0, 0, 0)
    pdf.ln(5)
    
    monitoring_tools = [
        ('prometheus-client', '0.22.1', 'Prometheus Metrics'),
        ('psutil', '7.0.0', 'System Monitoring'),
        ('evidently', '0.7.7', 'ML Monitoring'),
        ('langfuse', '3.0.1', 'LLM Monitoring'),
    ]
    
    pdf.set_fill_color(220, 220, 220)
    pdf.set_font('Helvetica', 'B', 9)
    pdf.cell(50, 7, 'Tool', 1, 0, 'C', fill=True)
    pdf.cell(30, 7, 'Version', 1, 0, 'C', fill=True)
    pdf.cell(100, 7, 'Purpose', 1, 1, 'C', fill=True)
    
    pdf.set_font('Helvetica', '', 9)
    for tool, ver, purpose in monitoring_tools:
        pdf.cell(50, 6, tool, 1)
        pdf.cell(30, 6, ver, 1)
        pdf.cell(100, 6, purpose, 1, 1)
    pdf.ln(5)
    
    # ===== SECTION 9: Development Tools =====
    pdf.add_page()
    pdf.set_font('Helvetica', 'B', 16)
    pdf.set_fill_color(44, 62, 80)
    pdf.set_text_color(255, 255, 255)
    pdf.cell(0, 10, '9. Development Tools', 0, 1, 'L', fill=True)
    pdf.set_text_color(0, 0, 0)
    pdf.ln(5)
    
    # Backend Dev Tools
    pdf.set_font('Helvetica', 'B', 12)
    pdf.cell(0, 8, '9.1 Backend Development', 0, 1)
    
    backend_dev = [
        ('black', '23.12.1', 'Code Formatting'),
        ('flake8', '6.1.0', 'Linting'),
        ('isort', '5.13.2', 'Import Sorting'),
        ('mypy', '1.7.1', 'Type Checking'),
        ('pre-commit', '3.6.0', 'Git Hooks'),
    ]
    
    pdf.set_fill_color(220, 220, 220)
    pdf.set_font('Helvetica', 'B', 9)
    pdf.cell(50, 7, 'Tool', 1, 0, 'C', fill=True)
    pdf.cell(30, 7, 'Version', 1, 0, 'C', fill=True)
    pdf.cell(100, 7, 'Purpose', 1, 1, 'C', fill=True)
    
    pdf.set_font('Helvetica', '', 9)
    for tool, ver, purpose in backend_dev:
        pdf.cell(50, 6, tool, 1)
        pdf.cell(30, 6, ver, 1)
        pdf.cell(100, 6, purpose, 1, 1)
    pdf.ln(5)
    
    # Frontend Dev Tools
    pdf.set_font('Helvetica', 'B', 12)
    pdf.cell(0, 8, '9.2 Frontend Development', 0, 1)
    
    frontend_dev = [
        ('eslint', '8.55.0', 'Linting'),
        ('prettier', '3.1.1', 'Code Formatting'),
        ('husky', '8.0.3', 'Git Hooks'),
        ('lint-staged', '15.2.0', 'Staged Files Linting'),
        ('commitizen', '4.3.0', 'Commit Messages'),
    ]
    
    pdf.set_fill_color(220, 220, 220)
    pdf.set_font('Helvetica', 'B', 9)
    pdf.cell(50, 7, 'Tool', 1, 0, 'C', fill=True)
    pdf.cell(30, 7, 'Version', 1, 0, 'C', fill=True)
    pdf.cell(100, 7, 'Purpose', 1, 1, 'C', fill=True)
    
    pdf.set_font('Helvetica', '', 9)
    for tool, ver, purpose in frontend_dev:
        pdf.cell(50, 6, tool, 1)
        pdf.cell(30, 6, ver, 1)
        pdf.cell(100, 6, purpose, 1, 1)
    pdf.ln(10)
    
    # Summary
    pdf.set_font('Helvetica', 'B', 16)
    pdf.set_fill_color(39, 174, 96)
    pdf.set_text_color(255, 255, 255)
    pdf.cell(0, 10, 'Summary', 0, 1, 'L', fill=True)
    pdf.set_text_color(0, 0, 0)
    pdf.ln(5)
    
    pdf.set_font('Helvetica', '', 11)
    summary = [
        'Total Docker Containers: 25+',
        'Total Backend Libraries: 80+',
        'Total Frontend Libraries: 100+',
        'Security Workflows: 4',
        'CI/CD Workflows: 11',
        'AI/ML Frameworks: 3 (PyTorch, TensorFlow, scikit-learn)',
    ]
    
    for item in summary:
        pdf.cell(0, 7, f"  * {item}", 0, 1)
    
    # Save PDF
    output_path = os.path.join(os.path.dirname(__file__), 'docs', 'Gaara_AI_Tools_Technologies.pdf')
    pdf.output(output_path)
    print(f"PDF generated successfully: {output_path}")
    return output_path


if __name__ == '__main__':
    create_pdf()

