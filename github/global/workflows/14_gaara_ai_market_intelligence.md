# Workflow 14: Market Intelligence (Scheduled)

> **Trigger**: Celery Beat — every 6 hours
> **Modules Involved**: Scraper → LLM → Qdrant → Email Alerts

## Steps

### Step 1: Scrape Competitor Sites
- Predefined list of competitor websites and product pages
- Scrape using Crawl4AI (scheduled, rate-limited)

### Step 2: Extract Price & Product Data
- Send scraped content to Ollama LLM:
  - "Extract product names, prices, availability from this content"
- Structure data into comparable format

### Step 3: Compare with GAARA Products
- Load GAARA product catalog from Qdrant (gaara_products collection)
- Compare prices, availability, new products

### Step 4: Change Detection
- Compare current scrape with previous (stored in gaara_market collection)
- Detect: price changes, new products, discontinued items

### Step 5: Report & Alert
- Generate market intelligence report
- Store in Qdrant (gaara_market collection)
- If significant changes detected → email alert to configured recipients
- Display in Django Dashboard
