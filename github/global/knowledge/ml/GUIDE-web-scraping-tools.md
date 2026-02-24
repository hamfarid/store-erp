# GUIDE-web-scraping-tools.md
# Governance: ML/AI Application Framework (Feb 2026 — Updated)

## 1. Crawl4AI (PRIMARY — Open Source)
*   **Version:** 0.4+ (58K+ GitHub stars, most popular in 2026)
*   **Architecture:** VLM Zero-Shot extraction — AI understands page structure without selectors
*   **Pros:** Free, local, self-healing (adapts to layout changes), Markdown output (perfect for RAG)
*   **Cons:** Requires local compute for VLM inference
*   **Use Case:** Knowledge base building, agricultural news, competitor monitoring
*   **Install:** `pip install crawl4ai`

## 2. Firecrawl (SECONDARY — SaaS API)
*   **Version:** 1.5+
*   **Success Rate:** 99% across all site types
*   **Pricing:** Free tier (500 credits) → $16/mo (3K) → $83/mo (100K)
*   **Pros:** Handles anti-bot/Cloudflare/CAPTCHA, JavaScript rendering, structured extraction
*   **Cons:** Paid, data goes through API, rate limited
*   **Use Case:** Protected sites, production reliability, complex JS rendering

## 3. ScrapeGraphAI (SMART — Natural Language)
*   **Version:** 1.30+
*   **Architecture:** LLM-powered — describe extraction in plain English/Arabic
*   **Pros:** No coding needed, works with local LLMs (Ollama/Qwen)
*   **Cons:** Slower, quality depends on LLM, not suitable for batch
*   **Use Case:** Ad-hoc extraction, non-technical users, prototyping

## 4. Playwright (FALLBACK — Full Browser)
*   **Version:** 1.49+
*   **Pros:** Real Chromium browser, login flows, screenshots, PDF generation
*   **Cons:** Heavy (1GB+ RAM per browser), slower
*   **Use Case:** Login-required sites, complex interactions, visual testing

## 5. Scrapy (LEGACY — Batch Crawling)
*   **Version:** 2.12+
*   **Note:** Superseded by Crawl4AI for most use cases
*   **Pros:** Mature, fast for static HTML, extensive middleware
*   **Cons:** No JS rendering (needs plugins), rigid architecture
*   **Use Case:** Millions of static pages, existing Scrapy pipelines

## 6. Deprecated Tools (Do NOT Use for New Projects)
| Tool | Status | Replacement |
|------|--------|-------------|
| Selenium | Maintenance mode | Playwright |
| Requests-HTML | Unmaintained (last update 2020) | httpx + Crawl4AI |
| Splash | Dead project | Playwright |
| Scrapy-Splash | Deprecated | scrapy-playwright |
| Beautiful Soup (alone) | Parser only, not a crawler | Crawl4AI |

## 7. Multi-Engine Fallback (GAARA-AI Pattern)
```
Request → Crawl4AI (free, local)
            │ fail?
            ▼
         Firecrawl (paid, anti-bot)
            │ fail?
            ▼
         Playwright (browser, heavy)
            │ fail?
            ▼
         Log error + alert
```

## 8. Compliance Tools
*   **Robots.txt:** Always check `urllib.robotparser`
*   **PII Detection:** Microsoft Presidio (anonymize personal data)
*   **Rate Limiting:** 2-second delay between requests (minimum)
*   **User Agent:** `GAARABot/1.0 (+https://gaara.com/bot)`
