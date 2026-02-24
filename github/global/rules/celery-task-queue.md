# Rule: Celery Task Queue Standards

> **Applies To**: All async operations in GAARA-AI

## When to Use Celery
- ANY operation expected to take >2 seconds
- Batch processing (multiple images, multiple URLs)
- Scheduled operations (drift detection, backup, scraping)
- Long-running AI inference (avatar generation, deep research)

## Task Routing (5 Queues)
| Queue | Workers | Priority | Examples |
|:------|:--------|:---------|:---------|
| ai_tasks | gaara-worker-ai | HIGH | LLM inference, embeddings |
| plant_diagnosis | gaara-worker-ai | HIGH | Disease detection, nutrient analysis |
| search_tasks | gaara-worker-scraping | MEDIUM | Web search, URL scraping |
| scraping_tasks | gaara-worker-scraping | MEDIUM | Deep research, scheduled scraping |
| data_processing | gaara-worker-data | LOW | ETL, learning sessions, backup |

## Task Design Rules
1. `task_acks_late = True` — acknowledge AFTER completion (not before)
2. `max_retries = 3` with exponential backoff (`retry_backoff=True`)
3. `soft_time_limit = 300` (5 min soft), `time_limit = 600` (10 min hard)
4. Serialization: JSON only (never pickle — security risk)
5. Result expiry: 3600 seconds (1 hour)
6. `worker_max_tasks_per_child = 100` for AI workers, 200 for scraping
7. Compression: gzip for large payloads
8. Timezone: Africa/Cairo

## Celery Version
- Celery 5.6.2+ REQUIRED (Jan 2026 — Redis stability fix via Kombu 5.5.0)
