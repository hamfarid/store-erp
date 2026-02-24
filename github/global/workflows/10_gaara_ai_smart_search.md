# Workflow 10: GAARA-AI Smart Search → Knowledge Pipeline

> **Trigger**: User submits search query via API or Django UI
> **Modules Involved**: API Gateway → Scraper → LLM → RAG → Qdrant

## Steps

### Step 1: Query Optimization
- Gateway receives user query
- Send to Ollama LLM: "Optimize this search query for web search: {query}"
- LLM returns optimized query + suggested search terms

### Step 2: Multi-Source Search
- Execute Google Custom Search API with optimized query
- Execute Bing Search API with optimized query
- Merge results, deduplicate by URL
- Rank by relevance (combine search engine scores)

### Step 3: Intelligent Scraping
- Take top 5 URLs from search results
- For each URL → Celery task (scraping_tasks queue):
  - Try Crawl4AI first (VLM extraction, no selectors needed)
  - Fallback: Firecrawl if Crawl4AI fails
  - Fallback: Playwright for JS-heavy pages
- Collect raw content from all successful scrapes

### Step 4: Summarization & Extraction
- Send scraped content to Ollama LLM:
  - "Summarize the following content related to: {original_query}"
  - "Extract key facts, data points, and actionable insights"
- LLM returns structured summary + extracted facts

### Step 5: Knowledge Base Storage
- Chunk extracted content (RecursiveCharacterTextSplitter, 800 chars)
- Generate embeddings (BGE-M3, 768 dims)
- Store in Qdrant collection (auto-categorize into 7 collections)
- Attach metadata: source URL, date, query, language

### Step 6: Response Delivery
- Return to user: summary + sources + "saved to knowledge base" confirmation
- If Django UI: display in AI Search page with tabs

## Error Handling
- If all search APIs fail → return error with suggestion to try later
- If scraping fails for a URL → skip and continue with remaining
- If LLM fails → return raw search results without summarization
