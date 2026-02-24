# GUIDE-web-scraping-tools.md
# Governance: ML/AI Application Framework (Feb 2026)

## 1. Scrapy (Recommended)
*   **Version:** 2.11.1
*   **Pros:** Fast, asynchronous, built-in middleware (retry, user-agent), structured data extraction.
*   **Cons:** Doesn't handle JavaScript well (requires Playwright/Splash).
*   **Use Case:** Large-scale scraping of static websites (e.g., news, e-commerce).

## 2. Playwright
*   **Version:** 1.42.0
*   **Pros:** Handles dynamic content (JavaScript/AJAX), headless browser, auto-waiting.
*   **Cons:** Slower than Scrapy (resource intensive).
*   **Use Case:** Single-page applications (SPAs), complex interactions (login, scroll).

## 3. Beautiful Soup 4
*   **Version:** 4.12.3
*   **Pros:** Simple API, robust HTML parsing (lxml backend).
*   **Cons:** Not a crawler (just a parser), synchronous (slow for many pages).
*   **Use Case:** Quick scripts, parsing local HTML files.

## 4. Selenium
*   **Version:** 4.18.1
*   **Pros:** Mature ecosystem, wide browser support.
*   **Cons:** Slower than Playwright, more brittle (flaky tests).
*   **Use Case:** Legacy projects, specific browser testing.

## 5. Requests-HTML
*   **Version:** 0.10.0
*   **Pros:** Combines Requests + PyQuery + Pyppeteer (JS rendering).
*   **Cons:** Less maintained than Scrapy/Playwright.
*   **Use Case:** Simple dynamic scraping tasks.

## 6. Compliance Tools
*   **Robots.txt Parser:** `urllib.robotparser` (Standard library).
*   **Presidio:** Microsoft tool for PII detection/anonymization.
*   **User-Agent:** `fake-useragent` (Use with caution; prefer identifying string).
