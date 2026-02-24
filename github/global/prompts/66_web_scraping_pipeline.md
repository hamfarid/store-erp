# Prompt 66: Web Scraping & Search Pipeline

> **Scope**: Multi-engine scraping strategy for GAARA-AI
> **Container**: gaara-scraper (port 8002)

## Engine Priority (Fallback Chain)

| Priority | Engine | Type | Use When |
|:---------|:-------|:-----|:---------|
| 1st | Crawl4AI | Free, local, VLM-powered | Default for all sites — self-healing, no selectors needed |
| 2nd | Firecrawl | API-based | Complex JS-heavy sites that Crawl4AI cannot handle |
| 3rd | ScrapeGraphAI | NLP extraction | Natural language extraction ("get all prices from this page") |
| 4th | Playwright | Full browser | Last resort — full browser automation with screenshots |

## Search APIs
- **Google Custom Search API** — primary web search
- **Bing Search API** — secondary/validation
- **SerpAPI** — fallback aggregator
- **Unsplash + Pexels API** — free image sources

## Workflow Chains

### Chain: Smart Search → Knowledge
```
User Query → LLM optimize query → Web Search (Google+Bing)
→ Scrape Top 5 Results (Crawl4AI) → LLM summarize + extract facts
→ BGE-M3 embeddings → Store in Qdrant → Return Summary + Sources
```

### Chain: Market Intelligence (Scheduled)
```
Cron Trigger → Scrape Competitor Sites → Extract Price Data
→ Compare with GAARA Products → Detect Changes
→ Generate Report → Store in KB → Alert if threshold exceeded
```

## Rules
- Always try Crawl4AI first (free, no API key needed)
- Respect robots.txt unless explicitly overridden
- Rate limit: configurable per domain (default 2 req/sec)
- All scrape results cached in Redis for 1 hour
- Deep research tasks → Celery task (can take minutes)
- Save valuable findings to Qdrant knowledge base automatically
