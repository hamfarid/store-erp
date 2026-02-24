# Template: Django AI Integration Page (GAARA-AI)

> **Use For**: Adding new pages to the Django ERP ai_integration app

## Page Structure
```
django_erp/ai_integration/
├── templates/ai/
│   ├── base.html              # Shared layout (sidebar, header)
│   └── {page_name}.html       # Page template
├── views.py                   # Add page view
├── urls.py                    # Add URL pattern
└── static/ai/
    ├── css/{page_name}.css    # Page-specific styles
    └── js/{page_name}.js      # Page-specific JavaScript
```

## 8 Required Pages
| URL | Page | Purpose |
|:----|:-----|:--------|
| /ai/dashboard/ | Dashboard | Statistics, charts, recent operations, server status |
| /ai/settings/ | Settings | 10-section configuration panel |
| /ai/plant-doctor/ | Plant Doctor | Image upload, diagnosis display, history |
| /ai/search/ | AI Search | Search bar, web/images/deep tabs, save to KB |
| /ai/knowledge/ | Knowledge Base | Tree view, semantic search, CRUD, import |
| /ai/learning/ | Learning Sessions | Start new, active progress, completed log |
| /ai/avatar/ | Avatar Studio | TTS, voice selector, video gallery |
| /ai/monitor/ | System Monitor | Service cards, Grafana embeds, Celery tasks |

## View Template
```python
@login_required
def {page_name}_view(request):
    """GAARA-AI {page_name} page."""
    context = {
        'page_title': '{Page Title}',
        'active_page': '{page_name}',
    }
    return render(request, 'ai/{page_name}.html', context)
```

## URL Pattern
```python
urlpatterns = [
    path('{page_name}/', views.{page_name}_view, name='ai_{page_name}'),
]
```

## API Integration (JavaScript)
All pages communicate with the FastAPI Gateway via JavaScript:
```javascript
const API_BASE = 'https://ai.gaara.com/api/v1';
const token = getCookie('jwt_token');

async function apiCall(endpoint, method, body) {
    const response = await fetch(`${API_BASE}${endpoint}`, {
        method: method,
        headers: {
            'Authorization': `Bearer ${token}`,
            'Content-Type': 'application/json'
        },
        body: body ? JSON.stringify(body) : undefined
    });
    return response.json();
}
```

## Checklist
- [ ] View function with @login_required
- [ ] URL pattern in urls.py
- [ ] Template extends ai/base.html
- [ ] active_page set for sidebar highlighting
- [ ] API calls use JWT authentication
- [ ] Loading states for async operations
- [ ] Error handling and user feedback
- [ ] Arabic language support (RTL layout)
