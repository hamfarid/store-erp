# Prompt 73: GAARA AI Settings Page Specification

> **Scope**: Django ERP settings page for GAARA AI ecosystem
> **When to Load**: Building or modifying the AI Settings UI

## Settings Page — 10 Sections

### Navigation (Sidebar)
1. إعدادات التعلم (Learning Settings)
2. النماذج LLM (LLM Models)
3. البحث والكشط (Search & Scraping)
4. معالجة الصور (Image Processing)
5. الخوادم (Servers / Infrastructure)
6. Avatar
7. المراقبة (Monitoring)
8. النسخ الاحتياطي (Backup)
9. ربط ERP (ERP Integration)
10. API Keys

### Section 1: Learning Settings
- **Learning Mode Toggle**: Active/Inactive
- **3 Learning Types**:
  - Continuous Learning: real-time micro-updates from incoming data
  - Batch Learning: scheduled deep learning sessions
  - Drift-Triggered: auto re-learn when PSI threshold exceeded
- **Learning Parameters**:
  - Search Depth: 3 (link levels per page)
  - Max Pages per Session: 50
  - Relevance Threshold: 70% (content below this ignored)
  - PSI Threshold: 0.20 (drift threshold for auto-learning)
  - Search Languages: 2 items (ar, en)
- **Schedule**: Every 12 hours (cron: `0 */12 * * *`)
- **Knowledge Domains**: 7 active domains
  - زراعة وبذور (Agriculture & Seeds)
  - تصدير واستيراد (Export & Import)
  - طاقة شمسية (Solar Energy)
  - أسعار العملات (Currency Rates)
  - ذكاء اصطناعي (AI)
  - لوائح تنظيمية (Regulations)
  - Sakata Seeds

### Section 2: LLM Models
- Primary Model: Ollama (model name, server URL, temperature)
- Fallback Model: selection
- Embedding Model: BGE-M3 (dimensions, batch size)
- Max tokens, context window settings

### Section 3: Search & Scraping
- Engine priority order (drag & drop): Crawl4AI → Firecrawl → ScrapeGraphAI → Playwright
- Rate limits per domain
- robots.txt compliance toggle
- API keys for Google Search, Bing, SerpAPI

### Section 4: Image Processing
- OCR engine: EasyOCR (languages, confidence threshold)
- Analysis engine: CLIP / Florence-2
- Max image size
- Screenshot settings (width, height)

### Section 5: Servers
- Server status cards (4 servers: GPU PC, VPS1, VPS2, Local Server)
- Tailscale IPs, connection status
- Resource usage (CPU, RAM, Disk)

### Section 6: Avatar
- TTS engine: Bark / Coqui (language, voice, speed)
- Avatar engine: SadTalker / Wav2Lip
- Reference face image
- Output quality settings

### Section 7: Monitoring
- Prometheus URL, Grafana URL
- Alert email recipients
- Drift detection schedule
- Health check interval

### Section 8: Backup
- Backup schedule (daily at 3 AM)
- Retention policy (30 days)
- Backup destinations
- Include/exclude patterns

### Section 9: ERP Integration
- Django ERP URL
- API authentication
- Sync schedule
- Module mapping

### Section 10: API Keys
- Encrypted storage for all API keys
- Key rotation reminders
- Usage monitoring per key

### UI Components
- Header: "GAARA AI إعدادات" + "G" logo + status badge ("جميع الخوادم متصلة") + Save button
- Sidebar: 10 section links with icons
- Content: Section-specific forms with real-time validation
- Toast: Success/error notifications on save
