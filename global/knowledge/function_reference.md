# Function Reference

This file documents shared functions and utilities available across the system, including MCP tools.

## 🔍 Search & Research (Firecrawl / Exa)

### `search(query: string)`
Performs a deep semantic search using Firecrawl or Exa.
- **Usage:** `manus-mcp-cli tool call search --server firecrawl --input '{"query": "..."}'`
- **Returns:** List of relevant search results with snippets and URLs.
- **Best Practice:** Use specific, technical queries. Avoid generic terms.

### `scrape(url: string)`
Extracts clean Markdown content from a specific URL.
- **Usage:** `manus-mcp-cli tool call scrape --server firecrawl --input '{"url": "..."}'`
- **Returns:** Full page content in Markdown format.
- **Best Practice:** Always check `robots.txt` compliance. Use for documentation and technical articles.

### `crawl(url: string, depth: number = 1)`
Crawls a website starting from a URL to a specified depth.
- **Usage:** `manus-mcp-cli tool call crawl --server firecrawl --input '{"url": "...", "depth": 1}'`
- **Returns:** List of pages with their content.
- **Best Practice:** Limit depth to 2 to avoid overwhelming the target server and your context window.

## 🌐 Browser Automation (Playwright)

### `navigate(url: string)`
Navigates the browser to a URL.
- **Usage:** `manus-mcp-cli tool call navigate --server playwright --input '{"url": "..."}'`

### `click(selector: string)`
Clicks an element matching the selector.
- **Usage:** `manus-mcp-cli tool call click --server playwright --input '{"selector": "..."}'`

### `fill(selector: string, value: string)`
Fills an input field.
- **Usage:** `manus-mcp-cli tool call fill --server playwright --input '{"selector": "...", "value": "..."}'`

### `screenshot(path: string)`
Captures a screenshot of the current page.
- **Usage:** `manus-mcp-cli tool call screenshot --server playwright --input '{"path": "..."}'`
