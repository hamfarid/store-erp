# Example: Django ERP ↔ GAARA-AI Integration

> **Purpose**: How the Django ERP (60+ modules) integrates with the AI Gateway

## Django App: ai_integration

### Directory Structure
```
django_erp/ai_integration/
├── __init__.py
├── admin.py
├── apps.py
├── models.py        # AIDiagnosis, AISearch, AILearningSession, AIAvatar
├── urls.py          # 8 pages
├── views.py         # Dashboard, Settings, Plant Doctor, Search, KB, Learning, Avatar, Monitor
├── forms.py         # Settings form, Upload form
├── api_client.py    # httpx client → FastAPI Gateway
├── templates/ai_integration/
│   ├── dashboard.html
│   ├── settings.html
│   ├── plant_doctor.html
│   ├── search.html
│   ├── knowledge_base.html
│   ├── learning.html
│   ├── avatar_studio.html
│   └── system_monitor.html
└── static/ai_integration/
    ├── css/
    └── js/
```

### 8 Django Pages
| URL | Page | Description |
|:----|:-----|:------------|
| /ai/dashboard/ | Dashboard | Stats, charts, last 10 operations, server status |
| /ai/settings/ | Settings | 10 sections (models, scraping, OCR, servers, API keys) |
| /ai/plant-doctor/ | Plant Doctor | Drag-drop upload, bounding boxes, treatment table |
| /ai/search/ | AI Search | Autocomplete, tabs (Web/Images/Deep), save to KB |
| /ai/knowledge/ | Knowledge Base | Tree view (7 categories), semantic search, CRUD |
| /ai/learning/ | Learning | Start session, progress bars, schedule recurring |
| /ai/avatar/ | Avatar Studio | Text → TTS → Avatar video, voice selector, gallery |
| /ai/monitor/ | System Monitor | Service cards, Grafana embeds, Celery queue viz |

### API Client Pattern
```python
# django_erp/ai_integration/api_client.py
import httpx

class GAARAApiClient:
    def __init__(self):
        self.base_url = settings.GAARA_AI_API_URL  # http://local-server:8000
        self.api_key = settings.GAARA_AI_API_KEY

    async def diagnose_plant(self, image_file):
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.base_url}/api/v1/plant/diagnose",
                files={"image": image_file},
                headers={"Authorization": f"Bearer {self.api_key}"},
                timeout=30.0
            )
            return response.json()
```
