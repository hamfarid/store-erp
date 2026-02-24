# GUIDE-ml-tool-versions.md
# Governance: ML/AI Application Framework (Feb 2026 — Updated)

## 1. Core Libraries
*   **Python:** 3.12+ (Performance improvements, better typing, required for latest libs).
*   **PyTorch:** 2.5+ (CUDA 12.6, torch.compile mature, FlashAttention-3).
*   **Scikit-learn:** 1.6+ (Array API support, improved histograms).
*   **Pandas:** 2.2+ (PyArrow backend default, CoW).
*   **NumPy:** 2.0+ (StringDType, major performance improvements).

## 2. MLOps Tools
*   **MLflow:** 3.9+ (Enhanced LLM tracking, model registry).
*   **DVC:** 3.55+ (Data versioning).
*   **Evidently AI:** 0.6+ (100+ built-in metrics, LLM observability, live dashboard UI).
*   **Great Expectations:** 1.11+ (Data validation).
*   **Optuna:** 3.6+ (Hyperparameter optimization, CMA-ES sampler).

## 3. Serving & Deployment
*   **FastAPI:** 0.115+ (ASGI 4.0 standards, production-ready).
*   **Uvicorn:** 0.34+ (ASGI server, HTTP/2).
*   **Gunicorn:** 23+ (WSGI/ASGI manager, Uvicorn workers).
*   **ONNX Runtime:** 1.20+ (2-5x CPU speedup over PyTorch inference).
*   **Celery:** 5.6.2+ (Jan 2026 — memory leak fixes, Redis stability via Kombu 5.5.0).

## 4. NLP & LLMs
*   **Transformers:** 4.47+ (Hugging Face, GGUF support).
*   **LangChain:** 0.3+ (LCEL syntax, LangGraph for agents, dominant RAG framework).
*   **LlamaIndex:** 0.11+ (Data-centric RAG framework).
*   **Ollama:** Latest (Local LLM serving, 100+ models, REST API).
*   **vLLM:** 0.6+ (High-throughput LLM inference, PagedAttention).

## 5. Computer Vision
*   **Torchvision:** 0.20+ (Models, transforms v2 default).
*   **Albumentations:** 1.4+ (Fast augmentation, bounding box support).
*   **OpenCV-Python:** 4.10+ (Headless variant for servers).
*   **Ultralytics (YOLO):** 8.3+ (YOLOv8/v10, ONNX export, CPU+GPU).

## 6. Vector Databases & Embeddings
*   **Qdrant:** 1.13+ (Hybrid Search via Query API, Rust performance).
*   **langchain-qdrant:** 0.2+ (Official LangChain integration).
*   **FastEmbed:** 0.4+ (Lightweight embedding inference, ONNX-based).
*   **BGE-M3:** BAAI/bge-m3 (768-dim, multilingual incl. Arabic, best value).
*   **ChromaDB:** 0.5+ (Prototyping only — Rust rewrite, 4x faster).

## 7. Web Scraping (2026 Revolution)
*   **Crawl4AI:** 0.4+ (VLM Zero-Shot, 58K stars, FREE, self-healing).
*   **Firecrawl:** 1.5+ (99% success rate, anti-bot bypass, SaaS API).
*   **ScrapeGraphAI:** 1.30+ (Natural language extraction, local LLM).
*   **Playwright:** 1.49+ (Browser automation fallback).
*   **Scrapy:** 2.12+ (Legacy batch crawling).

## 8. OCR & Image Processing
*   **EasyOCR:** 1.7+ (Arabic + English, GPU/CPU, 80+ languages).
*   **PaddleOCR:** 2.8+ (Alternative with better Asian lang support).
*   **Tesseract:** 5.4+ (Open-source, less accurate than EasyOCR for Arabic).

## 9. Avatar & TTS
*   **Bark:** 0.1.5+ (Realistic multilingual TTS, Suno AI).
*   **Coqui TTS:** 0.22+ (Arabic support, open-source, custom voices).
*   **SadTalker:** Latest (Audio → talking head video).
*   **Wav2Lip:** Latest (Lip sync for any video/audio pair).

## 10. Networking & Infrastructure
*   **Tailscale:** Stable (WireGuard-based mesh VPN, zero-config, MagicDNS).
*   **Cloudflare Tunnel:** cloudflared latest (Zero Trust, HTTPS auto, DDoS/WAF).
*   **Docker:** 27+ with Compose v2 (BuildKit default).
*   **Redis:** 7+ Alpine (Broker + Cache + Result backend).
*   **PostgreSQL:** 16+ Alpine (JSONB, parallel queries).
*   **MinIO:** Latest (S3-compatible object storage for models/files).

## 11. Monitoring & Observability
*   **Prometheus:** Latest (Metrics collection, PromQL).
*   **Grafana:** Latest (Dashboards, alerting).
*   **Flower:** 2.0+ (Celery task monitoring web UI).
*   **structlog:** 24+ (Structured JSON logging → Loki/ELK).

## 12. Deprecated/Replaced
| Tool | Status | Replacement |
|------|--------|-------------|
| TensorFlow | Legacy only | PyTorch |
| Selenium | Maintenance | Playwright |
| ChromaDB (production) | Prototyping only | Qdrant |
| Scrapy (primary) | Batch only | Crawl4AI |
| WireGuard (manual) | Complex setup | Tailscale |
| Nginx + Let's Encrypt | Manual certs | Cloudflare Tunnel |
| TorchServe | Maintenance | ONNX Runtime / vLLM |
| LangChain 0.1.x | Deprecated API | LangChain 0.3+ (LCEL) |
