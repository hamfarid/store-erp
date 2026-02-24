# Scraping Tool Selection Guide (v30.0 — Feb 2026)

## 1. Decision Matrix (2026 Updated)

| Scenario | Recommended Tool | Why? |
| :--- | :--- | :--- |
| **General Web (90% of cases)** | **Crawl4AI** | Free, local, VLM-powered, auto-extracts structured data |
| **Complex/Protected Sites** | **Firecrawl** | 99% success, handles Cloudflare/anti-bot, SaaS API |
| **Natural Language Extraction** | **ScrapeGraphAI** | "Get all product prices" → structured JSON |
| **Full Browser Automation** | **Playwright** | Login flows, infinite scroll, screenshots |
| **Legacy/Static HTML** | **Scrapy** | Fast batch crawling, middlewares |
| **Simple API calls** | **httpx** | Async, lightweight, HTTP/2 support |

## 2. Tool Deep Dive (2026)

### 2.1 Crawl4AI (PRIMARY — Open Source)
*   **Version:** 0.4+ (58K+ GitHub stars)
*   **Architecture:** VLM Zero-Shot extraction — uses vision-language models to understand pages without selectors
*   **Pros:**
    - Free and open-source, runs locally
    - No CSS/XPath selectors needed — AI understands page structure
    - Self-healing: adapts when site layout changes
    - Markdown output (perfect for LLM/RAG ingestion)
    - Async + parallel crawling
*   **Cons:** Requires local compute for VLM, slower than pure HTTP
*   **Best For:** RAG knowledge base building, agricultural news scraping, competitor monitoring
*   **Install:** `pip install crawl4ai`

```python
from crawl4ai import AsyncWebCrawler

async def scrape(url):
    async with AsyncWebCrawler() as crawler:
        result = await crawler.arun(url=url)
        return result.markdown  # Clean markdown for LLM
```

### 2.2 Firecrawl (SECONDARY — SaaS API)
*   **Version:** 1.5+ (API-based)
*   **Success Rate:** 99% across all site types
*   **Pricing:** $16/month (500 pages) → $83 (6K) → $333 (50K)
*   **Pros:**
    - Handles anti-bot, Cloudflare, CAPTCHAs automatically
    - JavaScript rendering built-in
    - Structured extraction via schema
    - /crawl endpoint for deep spidering
*   **Cons:** Paid, data goes through API
*   **Best For:** Protected sites, high-value data, production reliability

```python
from firecrawl import FirecrawlApp

app = FirecrawlApp(api_key="fc-xxx")
result = app.scrape_url("https://example.com", params={
    "formats": ["markdown", "extract"],
    "extract": {"schema": {"title": "string", "price": "number"}}
})
```

### 2.3 ScrapeGraphAI (SMART — Natural Language)
*   **Version:** 1.30+
*   **Architecture:** LLM-powered extraction — describe what you want in plain text
*   **Pros:** No coding needed, works with local LLMs (Ollama)
*   **Cons:** Slower, depends on LLM quality
*   **Best For:** Ad-hoc extraction, non-technical users, prototyping

```python
from scrapegraphai.graphs import SmartScraperGraph

graph = SmartScraperGraph(
    prompt="Extract all seed varieties with prices",
    source="https://example.com/catalog",
    config={"llm": {"model": "ollama/qwen2.5:7b", "base_url": "http://ollama:11434"}}
)
result = graph.run()
```

### 2.4 Playwright (FALLBACK — Full Browser)
*   **Version:** 1.49+
*   **Pros:** Real browser, handles any JS, screenshots, PDF generation
*   **Cons:** Heavy (RAM/CPU), slower
*   **Best For:** Login-required sites, screenshots, complex interactions

### 2.5 Scrapy (LEGACY — Batch Crawling)
*   **Version:** 2.12+
*   **Note:** Still viable for large-scale static crawling but superseded by Crawl4AI for most use cases
*   **Best For:** Millions of pages, established pipelines

## 3. Multi-Engine Fallback Pattern (GAARA-AI)

```python
# Pipeline: Try engines in order until success
ENGINES = ["crawl4ai", "firecrawl", "playwright"]

async def scrape_with_fallback(url):
    for engine in ENGINES:
        try:
            result = await scrape_with_engine(engine, url)
            if result and len(result.content) > 100:
                return result
        except Exception as e:
            log.warning(f"{engine} failed for {url}: {e}")
            continue
    raise ScrapingError(f"All engines failed for {url}")
```

## 4. Compliance Checklist (2026)

1.  **Check robots.txt**: Always respect crawl directives.
2.  **Rate Limiting**: Default 2 seconds between requests.
3.  **User Agent**: Identify yourself (e.g., `GAARABot/1.0 (+https://gaara.com)`).
4.  **PII**: Never scrape personal data without consent (GDPR/PDPA).
5.  **Content**: Don't reproduce copyrighted content — summarize via LLM.
6.  **Terms of Service**: Check site ToS before scraping.

## 5. Deprecated Tools (Do NOT Use)

| Tool | Status | Replacement |
|------|--------|-------------|
| Selenium | Maintenance mode | Playwright |
| Requests-HTML | Unmaintained | httpx + Crawl4AI |
| Splash | Dead project | Playwright |
| Scrapy-Splash | Deprecated | scrapy-playwright |
