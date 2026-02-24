# ML Scraping Workflow (v18.0)
# Scope: Data Acquisition & Pipeline
# Tools: Scrapy, Selenium, Playwright, Airflow

## 1. Workflow Stages

### 1.1 Discovery (Phase 1)
*   **Goal**: Identify target URLs and structure.
*   **Tool**: Manual inspection / Sitemap parsing.
*   **Output**: `seeds.txt` (List of URLs).

### 1.2 Extraction (Phase 2)
*   **Goal**: Download raw HTML/JSON.
*   **Tool**: Scrapy Spider (Async).
*   **Storage**: Raw S3 Bucket (`s3://raw-data/YYYY-MM-DD/`).
*   **Format**: JSON Lines (`.jsonl`).

### 1.3 Transformation (Phase 3)
*   **Goal**: Clean and structure data.
*   **Tool**: Pandas / Spark.
*   **Steps**:
    1.  Parse HTML (BeautifulSoup/lxml).
    2.  Normalize Text (Unicode, Whitespace).
    3.  Extract Entities (Spacy/Regex).
*   **Storage**: Processed S3 Bucket (`s3://processed-data/`).

### 1.4 Validation (Phase 4)
*   **Goal**: Ensure data quality.
*   **Tool**: Great Expectations.
*   **Checks**: Schema, Nulls, Duplicates.

## 2. Anti-Bot Strategy

### 2.1 User-Agent Rotation
*   **Source**: `fake-useragent` library.
*   **Frequency**: Rotate every request.

### 2.2 Proxy Management
*   **Provider**: Bright Data (Residential).
*   **Rotation**: Rotate IP every 10 requests or on 403/429.

### 2.3 Browser Fingerprinting
*   **Tool**: `scrapy-impersonate` (TLS Fingerprint).
*   **Headless**: Use `undetected-chromedriver`.

## 3. Scheduling (Airflow)

### 3.1 DAG Structure
*   **Task 1**: `check_robots_txt`.
*   **Task 2**: `run_spider` (KubernetesPodOperator).
*   **Task 3**: `validate_data` (GreatExpectationsOperator).
*   **Task 4**: `archive_raw`.

### 3.2 Retries
*   **Policy**: Exponential Backoff (1m, 5m, 15m).
*   **Max Retries**: 3.

## 4. Legal & Ethical Checklist

### 4.1 Pre-Scrape
*   [ ] Check `robots.txt`.
*   [ ] Review Terms of Service (ToS).
*   [ ] Verify no PII collection.

### 4.2 During Scrape
*   [ ] Monitor Error Rates (403/429).
*   [ ] Respect Rate Limits (1 req/sec).

## 5. Code Example (Airflow DAG)

```python
from airflow import DAG
from airflow.providers.cncf.kubernetes.operators.kubernetes_pod import KubernetesPodOperator
from datetime import datetime, timedelta

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email_on_failure': True,
    'retries': 3,
    'retry_delay': timedelta(minutes=5),
}

with DAG(
    'ml_scraping_pipeline',
    default_args=default_args,
    schedule_interval='@daily',
    start_date=datetime(2026, 1, 1),
    catchup=False,
) as dag:

    scrape_task = KubernetesPodOperator(
        namespace='airflow',
        image='gaara/scraper:latest',
        cmds=["scrapy", "crawl", "plant_disease"],
        name="scrape-plant-disease",
        task_id="scrape_task",
        get_logs=True,
    )
```
