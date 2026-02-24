# GUIDE-celery-workers-2026.md
# Governance: ML/AI Application Framework (Feb 2026)

## 1. Celery 5.6.2 (January 2026 — Current Stable)

### Key Improvements Over 5.4.x:
- Memory leak fix (Python 3.11+ traceback cycles)
- Security: Broker credentials no longer logged plaintext
- Redis stability via Kombu 5.5.0
- `exception_safe_to_retry` for automatic recovery
- Pydantic model support for type-safe tasks
- Python 3.9-3.13 supported (3.8 dropped)

## 2. Architecture: 3 Priority Queues

```
┌──────────────────────────────────────────────┐
│                 REDIS BROKER                  │
│              (redis:7-alpine)                 │
│                                               │
│  Queue: ai_tasks ────► Worker AI (×4)         │
│  Queue: search_tasks ─► Worker Scraping (×8)  │
│  Queue: data_tasks ──► Worker Data (×4)       │
│                                               │
│  Beat Scheduler ──► Periodic Tasks            │
│  Flower UI (port 5555) ──► Monitoring         │
└──────────────────────────────────────────────┘
```

## 3. Configuration (Production-Ready)

```python
# core/celery_app.py
import os
from celery import Celery
from celery.schedules import crontab

app = Celery('gaara_ai')

# Broker & Backend (Redis for both)
app.conf.broker_url = os.getenv('REDIS_URL', 'redis://redis:6379/0')
app.conf.result_backend = os.getenv('REDIS_URL', 'redis://redis:6379/0')

# Serialization
app.conf.accept_content = ['json']
app.conf.task_serializer = 'json'
app.conf.result_serializer = 'json'
app.conf.timezone = 'Africa/Cairo'

# Reliability (Critical for Production)
app.conf.broker_connection_retry_on_startup = True
app.conf.task_acks_late = True              # Acknowledge AFTER completion
app.conf.worker_prefetch_multiplier = 1     # Fair scheduling
app.conf.task_reject_on_worker_lost = True  # Requeue if worker dies
app.conf.task_compression = 'gzip'

# Results
app.conf.result_expires = 3600  # 1 hour
app.conf.task_track_started = True

# Memory Management
# CRITICAL: Prevent memory leaks in long-running AI tasks
app.conf.worker_max_tasks_per_child = 100  # Restart worker after 100 tasks

# Task Routing
app.conf.task_routes = {
    'tasks.ai_tasks.*': {'queue': 'ai_tasks'},
    'tasks.plant_tasks.*': {'queue': 'ai_tasks'},
    'tasks.search_tasks.*': {'queue': 'search_tasks'},
    'tasks.learning_tasks.*': {'queue': 'data_tasks'},
    'tasks.data_tasks.*': {'queue': 'data_tasks'},
}

# Beat Schedule
app.conf.beat_schedule = {
    'health-check-5min': {
        'task': 'tasks.scheduled_tasks.health_check_all',
        'schedule': 300.0,
    },
    'drift-detection-daily': {
        'task': 'tasks.scheduled_tasks.check_model_drift',
        'schedule': crontab(hour=2, minute=0),
    },
    'backup-daily': {
        'task': 'tasks.scheduled_tasks.run_backup',
        'schedule': crontab(hour=3, minute=0),
    },
}

app.autodiscover_tasks(['tasks'])
```

## 4. Task Patterns

### 4.1 Standard Task with Retry
```python
@app.task(
    bind=True,
    autoretry_for=(Exception,),
    retry_backoff=True,        # Exponential: 1s, 2s, 4s, 8s...
    retry_backoff_max=600,     # Max 10 minutes
    max_retries=3,
    rate_limit='100/m',        # Max 100 executions per minute
    time_limit=300,            # Hard kill after 5 minutes
    soft_time_limit=240,       # Soft warning at 4 minutes
)
def diagnose_plant(self, image_path, crop_type=None):
    try:
        result = plant_doctor.diagnose(image_path, crop_type)
        return result
    except SoftTimeLimitExceeded:
        return {"error": "Diagnosis timed out", "partial": True}
```

### 4.2 Chain (Sequential Pipeline)
```python
from celery import chain

# Search → Scrape → Summarize → Store
pipeline = chain(
    web_search.s(query),
    scrape_top_results.s(),
    summarize_with_llm.s(),
    store_in_knowledge_base.s()
)
pipeline.delay()
```

### 4.3 Group (Parallel Execution)
```python
from celery import group

# Diagnose 10 images in parallel
batch = group(
    diagnose_plant.s(img) for img in image_paths
)
result = batch.delay()
```

## 5. Docker Compose (Workers)

```yaml
celery-worker-ai:
  build: ./services/gateway
  command: >
    celery -A core.celery_app worker
    -Q ai_tasks -n worker_ai@%h
    --concurrency=4 --max-tasks-per-child=100 --loglevel=info
  depends_on: [redis]

celery-worker-scraping:
  build: ./services/scraper
  command: >
    celery -A core.celery_app worker
    -Q search_tasks -n worker_scrape@%h
    --concurrency=8 --max-tasks-per-child=200 --loglevel=info
  depends_on: [redis]

celery-worker-data:
  build: ./services/gateway
  command: >
    celery -A core.celery_app worker
    -Q data_tasks -n worker_data@%h
    --concurrency=4 --max-tasks-per-child=50 --loglevel=info
  depends_on: [redis]

celery-beat:
  build: ./services/gateway
  command: celery -A core.celery_app beat --loglevel=info
  depends_on: [redis]

flower:
  build: ./services/gateway
  command: celery -A core.celery_app flower --port=5555
  ports: ["5555:5555"]
  depends_on: [redis]
```

## 6. Redis Configuration

```yaml
redis:
  image: redis:7-alpine
  command: >
    redis-server
    --appendonly yes              # AOF persistence
    --maxmemory 512mb
    --maxmemory-policy allkeys-lru
    --requirepass ${REDIS_PASS}
  volumes:
    - redis_data:/data
```

**Key Settings:**
- `appendonly yes`: Persist tasks to disk (survive restart)
- `visibility_timeout`: Must be > longest task time (default 1 hour)
- `maxmemory-policy allkeys-lru`: Evict old results when full

## 7. Monitoring with Flower

Access at `http://localhost:5555` or via Cloudflare Tunnel.

**Flower Shows:**
- Active/Reserved/Scheduled tasks per worker
- Task success/failure rates
- Worker CPU/memory usage
- Task execution times
- Queue depths (backlog indicator)

## 8. Common Pitfalls

| Pitfall | Solution |
|---------|----------|
| Memory leak in AI tasks | `worker_max_tasks_per_child=100` |
| Task lost on crash | `task_acks_late=True` |
| Redis connection drops | `broker_connection_retry_on_startup=True` |
| Duplicate task execution | Use idempotency keys |
| Worker overwhelmed | `worker_prefetch_multiplier=1` |
| Long tasks blocking | Use `soft_time_limit` + `time_limit` |
| Results filling Redis | `result_expires=3600` |
