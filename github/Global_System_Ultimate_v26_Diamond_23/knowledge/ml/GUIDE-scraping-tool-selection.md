# Scraping Tool Selection Guide (v17.0)

## 1. Decision Matrix

| Scenario | Recommended Tool | Why? |
| :--- | :--- | :--- |
| **Static HTML** | **Scrapy** | Fast, Async, Middleware support. |
| **Dynamic JS (SPA)** | **Playwright** | Headless browser, reliable rendering. |
| **Anti-Bot (Cloudflare)** | **ZenRows / BrightData** | Rotating proxies, CAPTCHA solving. |
| **Simple API** | **Requests / Httpx** | Lightweight, easy to debug. |
| **Complex Workflow** | **Selenium** | Legacy support, extensive community. |

## 2. Tool Deep Dive

### 2.1 Scrapy (The Workhorse)
*   **Pros**: 100x faster than Selenium, built-in pipelines, extensive ecosystem.
*   **Cons**: Cannot render JS (needs Splash/Playwright integration).
*   **Best For**: E-commerce catalogs, News sites, Forums.

### 2.2 Playwright (The Modern Browser)
*   **Pros**: Auto-wait, trace viewer, multi-tab support.
*   **Cons**: Resource heavy (RAM/CPU).
*   **Best For**: React/Vue/Angular apps, Infinite scroll.

### 2.3 Beautiful Soup (The Parser)
*   **Pros**: Simple API, forgiving of bad HTML.
*   **Cons**: Slow, no networking (needs Requests).
*   **Best For**: Quick scripts, cleaning HTML.

## 3. Compliance Checklist (GDPR/Robots.txt)

1.  **Check robots.txt**: Always respect `User-agent: *` rules.
2.  **Rate Limiting**: Add `DOWNLOAD_DELAY = 2` (Scrapy) or `time.sleep(2)`.
3.  **User Agent**: Identify yourself (e.g., `Bot/1.0 (+http://mysite.com)`).
4.  **PII**: Do NOT scrape emails or phone numbers without consent.

## 4. Architecture Pattern (Universal Spider)

```python
# infrastructure/scraping/spiders/universal_spider.py
class UniversalSpider(scrapy.Spider):
    name = "universal"
    def start_requests(self):
        for target in self.config['targets']:
            yield scrapy.Request(target['url'], callback=self.parse)

    def parse(self, response):
        item = {}
        for field, selector in self.config['selectors'].items():
            item[field] = response.css(selector).get()
        yield item
```
