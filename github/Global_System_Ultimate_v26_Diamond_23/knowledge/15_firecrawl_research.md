# Firecrawl Research Guidelines

## Overview
Firecrawl is our primary tool for web scraping and deep research. It converts web content into clean, LLM-ready Markdown.

## Capabilities
1.  **Scrape:** Extract content from a single URL.
2.  **Crawl:** Crawl a website (with depth control) to extract multiple pages.
3.  **Search:** Perform semantic search over the web or specific domains.

## Best Practices
1.  **Respect Robots.txt:** Always ensure we are allowed to scrape the target.
2.  **Clean Data:** Firecrawl automatically cleans HTML to Markdown. Review the output to ensure relevance.
3.  **Depth Control:** When crawling documentation, limit depth to avoid fetching irrelevant pages (e.g., `depth: 2`).
4.  **Rate Limiting:** Be mindful of the target server's load.

## Usage in MCP
-   **Search:** `manus-mcp-cli tool call search --server firecrawl --input '{"query": "..."}'`
-   **Scrape:** `manus-mcp-cli tool call scrape --server firecrawl --input '{"url": "..."}'`

## Workflow
1.  **Identify Need:** What information is missing?
2.  **Search/Scrape:** Use Firecrawl to gather data.
3.  **Synthesize:** Summarize findings in `knowledge/` or the current task context.
