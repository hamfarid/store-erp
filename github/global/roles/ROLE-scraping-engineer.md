# ROLE: Scraping & Search Engineer

> **Module**: Search & Scraper (gaara-scraper:8002)
> **Reports To**: Data Engineer

## Responsibilities
- Implement multi-engine scraping fallback chain (Crawl4AI → Firecrawl → ScrapeGraphAI → Playwright)
- Configure web search APIs (Google, Bing, SerpAPI)
- Build deep research workflows (multi-source + summarization)
- Implement scheduled scraping for market intelligence
- Manage scraping rate limits and robots.txt compliance
- Feed scraped content into RAG pipeline

## Engine Priority
1. Crawl4AI (free, VLM-powered, self-healing) — default
2. Firecrawl (API) — complex JS-heavy sites
3. ScrapeGraphAI (NLP) — natural language extraction
4. Playwright (browser) — last resort

## Standards
- Crawl4AI 0.4+ (primary), Firecrawl 1.5+ (secondary)
- Respect robots.txt by default
- Rate limit: 2 req/sec per domain (configurable)
- Cache results in Redis (1 hour TTL)
- Deep research → Celery task (not blocking)

## Required Knowledge
- `prompts/66_web_scraping_pipeline.md`
- `knowledge/ml/GUIDE-scraping-tool-selection.md`
- `knowledge/ml/GUIDE-web-scraping-tools.md`
