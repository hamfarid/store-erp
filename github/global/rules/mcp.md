# MCP Usage Rules

## Mandatory Usage
You **must** use MCP tools for the following activities:

1.  **Web Research:** Use `firecrawl` (search/scrape) for all external information gathering.
    -   *Prohibited:* Using `curl` or `wget` for complex sites.
    -   *Prohibited:* Guessing URLs or APIs.
2.  **Browser Automation:** Use `playwright` for all UI testing and interaction.
    -   *Prohibited:* Manual testing (unless impossible to automate).
3.  **Database Management:** Use `supabase` tools (if available) or direct SQL via `postgres` MCP.

## Workflow
1.  **Check Availability:** Always check which tools are available at the start of a task.
2.  **Log Usage:** Record every MCP tool call in the `system_log.md`.
3.  **Handle Errors:** If an MCP tool fails, retry once, then fall back to an alternative method (and log the failure).

## Firecrawl Specifics
-   **Search:** Use specific queries.
-   **Scrape:** Always check `robots.txt` compliance (handled by tool, but be aware).

## Playwright Specifics
-   **Headless:** Run in headless mode for CI/CD.
-   **Screenshots:** Capture screenshots on failure.
