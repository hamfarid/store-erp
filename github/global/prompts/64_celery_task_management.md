# Prompt 64: Celery Task Management

> **Scope**: Async task queue patterns for GAARA-AI
> **When to Load**: Building task queues, background jobs, scheduled tasks

## Task Routing — 5 Queues
```python
task_routes = {
    'tasks.ai_tasks.*':        {'queue': 'ai_tasks'},          # HIGH priority
    'tasks.plant_tasks.*':     {'queue': 'plant_diagnosis'},    # HIGH priority
    'tasks.search_tasks.*':    {'queue': 'search_tasks'},       # MEDIUM priority
    'tasks.data_tasks.*':      {'queue': 'data_processing'},    # LOW priority
    'tasks.learning_tasks.*':  {'queue': 'learning_tasks'},     # LOW priority
}
```

## 3 Specialized Workers
| Worker | Container | Queues | Concurrency |
|:-------|:----------|:-------|:------------|
| AI Worker | gaara-worker-ai | ai_tasks, plant_diagnosis | 4 |
| Scraping Worker | gaara-worker-scraping | scraping_tasks, search_tasks | 8 |
| Data Worker | gaara-worker-data | data_processing, learning_tasks | 4 |

## Beat Schedule (Periodic Tasks)
```python
beat_schedule = {
    'health-check-5min':       {'schedule': 300.0},
    'drift-detection-daily':   {'schedule': crontab(hour=2, minute=0)},
    'knowledge-sync-hourly':   {'schedule': crontab(minute=0)},
    'backup-daily-3am':        {'schedule': crontab(hour=3, minute=0)},
    'scheduled-scraping-6h':   {'schedule': crontab(hour='*/6')},
    'metrics-collection-1min': {'schedule': 60.0},
}
```

## Rules
- Any API operation >2 seconds → MUST be a Celery task
- Always use `task_acks_late = True` (acknowledge after completion)
- Set `max-tasks-per-child` to prevent memory leaks (100 for AI, 200 for scraping)
- Celery 5.6.2+ required (Jan 2026 — Redis stability fix via Kombu 5.5.0)
- Timezone: Africa/Cairo
- Serialization: JSON only (no pickle for security)
- Result expiry: 1 hour
- Compression: gzip
