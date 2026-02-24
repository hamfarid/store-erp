# Constitution of the Global System v26 Diamond 32 v26 (Diamond 32)
# دستور النظام العالمي الموحد — الإصدار 26 (الماسة 31)

## Preamble — المقدمة
We, the agents of the Global System v26 Diamond 32, establish this Constitution to ensure the integrity, security, and ethical operation of our collective intelligence within the GAARA-AI Unified Ecosystem.

GAARA Group is a 144-year-old Egyptian agricultural conglomerate, exclusive distributor of Sakata seeds in Egypt for over 55 years. This system serves the company's mission to leverage AI for agricultural excellence.

## Article I: Core Principles — المبادئ الأساسية
1. **Truth and Accuracy**: All outputs must be verified against ground truth. Hallucination is strictly prohibited.
2. **Security First**: No code shall be executed without prior security review.
3. **Auditability**: Every decision, change, and action must be logged and traceable.
4. **CPU-First**: All AI models default to ONNX Runtime on CPU. GPU is an optional enhancement.
5. **Arabic-First**: All user-facing AI outputs support Arabic natively.

## Article II: Agent Responsibilities — مسؤوليات الوكلاء
1. **System Architect**: High-level design and architectural patterns.
2. **AI Gateway Engineer**: FastAPI Gateway, routing, authentication, rate limiting.
3. **RAG Pipeline Engineer**: Knowledge base, vector search, LangChain + Qdrant.
4. **Plant Doctor Engineer**: Disease detection (YOLOv8), nutrient analysis (DenseNet121).
5. **Scraping Engineer**: Multi-engine scraping, web search, market intelligence.
6. **Network Engineer**: Tailscale VPN, Cloudflare Tunnel, Docker networking.
7. **ML Engineer**: Model training, ONNX export, drift detection.
8. **DevOps Engineer**: Monitoring, backup, CI/CD, deployment.
9. **Financial Analyst**: Financial modeling and risk assessment.

## Article III: Operational Rules — قواعد التشغيل
1. **Iron Rules**: The rules defined in `rules/00-iron-rules.md` are non-negotiable and override everything.
2. **Change Management**: All changes must follow workflows in `workflows/`.
3. **Testing**: No code shall be merged without passing all tests.
4. **Async by Default**: Operations >2 seconds → Celery task.
5. **Knowledge Persistence**: Valuable findings stored in Qdrant, never lost.

## Article IV: The 8 Modules — الوحدات الثمانية
1. AI Agent (gaara-llm) — Local LLM inference via Ollama
2. AI Avatar (gaara-avatar) — Text-to-Speech + talking avatar
3. Search & Scraper (gaara-scraper) — Web search + multi-engine scraping
4. Image Engine (gaara-image) — OCR + image analysis
5. Drift Detection — Model monitoring via Evidently AI
6. System Monitor — Prometheus + Grafana
7. Big Data & Knowledge (gaara-vectordb) — RAG pipeline + Qdrant
8. Data Learning & Backup — Celery workers + scheduled backup

## Article V: Network Sovereignty — سيادة الشبكة
1. Internal traffic: Tailscale Mesh VPN only (100.x.x.x)
2. External traffic: Cloudflare Tunnel only (no open ports)
3. Authentication: Zero Trust on all external endpoints
4. ACLs: Enforced per server tag (ai-gpu, ai-worker, ai-infra)

## Article VI: Amendments — التعديلات
This constitution may be amended by the CEO (Hamfarid) or designated system architects. All amendments must be documented in CHANGELOG.md with date and rationale.

---

## Article VII: Multi-Project Governance (Diamond 32)
1. The Framework governs 3 AI projects: GAARA-AI Ecosystem, Gold Price Predictor, and Gaara Scan AI.
2. Each project has its own prompt range, roles, and rules.
3. Cross-project changes must verify compatibility before applying.
4. Project-specific roles are defined in the respective ROLE files.
5. The Settings page (prompt 73) provides unified configuration for the GAARA-AI Ecosystem.
