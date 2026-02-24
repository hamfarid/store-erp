# Template: Celery Task Definition

> **Use For**: Creating new async tasks in GAARA-AI

## Task Structure
```python
from celery import shared_task
from celery.utils.log import get_task_logger

logger = get_task_logger(__name__)

@shared_task(
    bind=True,
    name='tasks.{module}_tasks.{task_name}',
    queue='{queue_name}',
    max_retries=3,
    soft_time_limit=300,
    time_limit=600,
    acks_late=True,
    retry_backoff=True,
)
def task_name(self, param1: str, param2: dict) -> dict:
    """
    Description of what this task does.
    
    Args:
        param1: Description
        param2: Description
    
    Returns:
        dict with results
    """
    try:
        logger.info(f"Starting {self.name}", extra={"params": param2})
        
        # Update progress
        self.update_state(state='PROGRESS', meta={'step': 1, 'total': 3, 'detail': 'Processing...'})
        
        # ... actual work ...
        
        result = {"success": True, "data": {}}
        logger.info(f"Completed {self.name}", extra={"result_keys": list(result.keys())})
        return result
        
    except Exception as exc:
        logger.error(f"Failed {self.name}: {exc}", exc_info=True)
        raise self.retry(exc=exc)
```

## Queue Assignment
| Task Type | Queue | Worker |
|:----------|:------|:-------|
| LLM inference, embeddings | ai_tasks | gaara-worker-ai |
| Plant diagnosis | plant_diagnosis | gaara-worker-ai |
| Web search | search_tasks | gaara-worker-scraping |
| URL scraping, deep research | scraping_tasks | gaara-worker-scraping |
| ETL, learning, backup | data_processing | gaara-worker-data |

## Checklist
- [ ] Task name follows convention: `tasks.{module}_tasks.{name}`
- [ ] Queue assigned correctly
- [ ] max_retries set (default 3)
- [ ] soft_time_limit and time_limit set
- [ ] acks_late = True
- [ ] Logging at start, progress, and completion
- [ ] Exception handling with retry
- [ ] update_state for long-running tasks
