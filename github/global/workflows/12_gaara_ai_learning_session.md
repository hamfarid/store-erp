# Workflow 12: Self-Learning Session

> **Trigger**: User starts learning session via API or Django Learning page
> **Modules Involved**: API Gateway → LLM → Scraper → RAG → Qdrant

## Steps

### Step 1: Define Learning Topic
- User provides: topic, scope, max_pages, max_depth, target collection
- Example: "Learn about tomato disease management in Egypt, max 20 pages, depth 2"

### Step 2: Query Generation
- Send topic to Ollama LLM:
  - "Generate 10 diverse search queries to comprehensively learn about: {topic}"
- LLM returns list of search queries

### Step 3: Multi-Source Gathering
- For each query → execute web search (Google + Bing)
- Collect unique URLs (deduplicate)
- For each URL (up to max_pages):
  - Scrape content (Crawl4AI → Firecrawl → Playwright)
  - If max_depth > 1: follow internal links and scrape child pages
- Celery task in data_processing queue (long-running)

### Step 4: Content Processing
- Clean scraped HTML → extract text
- RecursiveCharacterTextSplitter (800 chars, 120 overlap)
- Generate BGE-M3 embeddings for each chunk

### Step 5: Knowledge Storage
- Store all chunks in target Qdrant collection
- Metadata: source URL, topic, session_id, date, language

### Step 6: Summary Report
- Send all gathered content to LLM:
  - "Summarize everything learned about {topic} in Arabic and English"
- Generate structured learning report
- Save report to PostgreSQL (AILearningSession model)
- Notify user (email or UI notification)

## Scheduling
- Sessions can be scheduled via Celery Beat
- Example: "Learn about cotton pest management every Monday at 6 AM"
- Recurring sessions add to existing knowledge (no duplication)
