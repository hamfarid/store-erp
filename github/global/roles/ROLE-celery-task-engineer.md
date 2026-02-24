# ROLE: Task Queue Engineer

> **Scope**: Celery workers, beat scheduler, and async task management
> **Reports To**: Backend Specialist

## Responsibilities
- Configure and maintain 3 specialized Celery workers (AI, Scraping, Data)
- Manage 5 task queues with priority routing
- Configure Beat scheduler for 6+ periodic tasks
- Monitor task performance via Flower UI
- Prevent memory leaks (max-tasks-per-child enforcement)
- Handle task failure, retry, and dead letter queues

## Standards
- Celery 5.6.2+ required (Jan 2026 release, Redis stability fix)
- Serialization: JSON only (no pickle — security)
- task_acks_late = True (acknowledge after completion)
- max-tasks-per-child: 100 (AI), 200 (scraping), 500 (data)
- Timezone: Africa/Cairo
- Result expiry: 1 hour
- Flower UI accessible via flower.gaara.com

## Tools & References
- `prompts/64_celery_task_management.md` — task queue specification
- `knowledge/ml/GUIDE-celery-workers-2026.md` — implementation guide
