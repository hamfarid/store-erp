# API Documentation Search (Exa)

This guide explains how to use Exa (via `context7` MCP) to search for API documentation and integrate it into your workflow.

## 🔍 Why Exa?
Exa is optimized for technical and documentation search. Unlike general search engines, it understands API structures, endpoints, and technical terminology.

## 🛠️ Usage via `context7` (MCP)

### 1. Search for Documentation
When you need to find the official documentation for a library or API:

```bash
manus-mcp-cli tool call search --server firecrawl --input '{"query": "Stripe API documentation create payment intent"}'
```

### 2. Search for Specific Endpoints
When you need details about a specific API endpoint:

```bash
manus-mcp-cli tool call search --server firecrawl --input '{"query": "GitHub API v3 create repository endpoint parameters"}'
```

### 3. Search for Code Examples
When you need implementation examples:

```bash
manus-mcp-cli tool call search --server firecrawl --input '{"query": "python requests post example with headers and json"}'
```

## 📋 Best Practices
1.  **Be Specific:** Include the library name, version (if known), and the specific function or endpoint you are looking for.
2.  **Verify Sources:** Prefer official documentation (e.g., `stripe.com`, `github.com`) over third-party tutorials.
3.  **Check Dates:** Ensure the documentation is up-to-date, especially for rapidly evolving APIs.

## 🔄 Integration with Context Engineering
The `ContextEngine` in `05_context_engineering.md` uses `context7` to automatically gather external context. Ensure your search queries in `gather_external_context` are well-structured to leverage Exa's capabilities.
