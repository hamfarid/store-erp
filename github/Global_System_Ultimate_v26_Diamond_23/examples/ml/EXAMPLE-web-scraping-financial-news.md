# EXAMPLE-web-scraping-financial-news.md
# Governance: ML/AI Application Framework (Feb 2026)
# Tooling: Scrapy, Playwright

## 1. Project Structure
```
financial-news-scraper/
├── configs/
│   ├── settings.py          # Scrapy settings (Rate limits, User-Agent)
│   └── items.py             # Data schema (Pydantic)
├── spiders/
│   ├── bloomberg.py         # Bloomberg spider
│   ├── reuters.py           # Reuters spider
│   └── wsj.py               # WSJ spider
├── pipelines/
│   ├── validation.py        # Data validation pipeline
│   └── storage.py           # Data storage pipeline (S3/DB)
├── middlewares/
│   ├── playwright.py        # Playwright middleware (JS rendering)
│   └── retry.py             # Retry middleware (Exponential backoff)
├── tests/                   # Unit and integration tests
├── Dockerfile               # Scrapy container
├── requirements.txt         # Pinned dependencies
└── README.md                # Project documentation
```

## 2. Compliance Rules
*   **Robots.txt:** `ROBOTSTXT_OBEY = True`.
*   **Rate Limiting:** `DOWNLOAD_DELAY = 10` (1 request per 10s).
*   **User-Agent:** `GlobalSystemBot/1.0 (contact@example.com)`.
*   **Concurrency:** `CONCURRENT_REQUESTS_PER_DOMAIN = 1`.

## 3. Data Schema (Pydantic)
```python
class NewsItem(BaseModel):
    url: HttpUrl
    title: str
    content: str
    published_at: datetime
    source: str
    tickers: List[str]
    sentiment: Optional[float]
```

## 4. Validation Pipeline
*   **Schema Check:** Validate against `NewsItem` schema.
*   **Completeness:** Check for missing fields (title, content, date).
*   **Uniqueness:** Deduplicate based on URL or content hash.
*   **PII Scan:** Scan content for PII using Presidio.

## 5. Storage
*   **Format:** Parquet (efficient storage) or JSONL (streaming).
*   **Location:** S3 Bucket (`s3://financial-news/raw/`).
*   **Partitioning:** By date (`YYYY/MM/DD`).
