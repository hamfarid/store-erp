# ML Web Scraping Compliance Rules (v18.0)
# Scope: Data Collection & Ethical Scraping
# Tools: Scrapy, Selenium, Playwright

## 1. Robots.txt Compliance

### 1.1 Mandatory Check
*   **Rule**: MUST respect `robots.txt` directives.
*   **Tool**: Use `urllib.robotparser` or Scrapy's `ROBOTSTXT_OBEY = True`.
*   **Exception**: Only with explicit written permission from site owner.

### 1.2 User-Agent Identification
*   **Rule**: MUST identify as a bot.
*   **Format**: `BotName/1.0 (+https://gaaragroup.com/bot-policy)`.
*   **Contact**: Include email/link for opt-out.

## 2. Rate Limiting & Politeness

### 2.1 Request Delay
*   **Rule**: Minimum 1 second delay between requests to same domain.
*   **Tool**: `DOWNLOAD_DELAY = 1.0` (Scrapy).
*   **Auto-Throttle**: Enable `AUTOTHROTTLE_ENABLED = True`.

### 2.2 Concurrency
*   **Rule**: Max 1 concurrent request per domain (unless API allows more).
*   **Tool**: `CONCURRENT_REQUESTS_PER_DOMAIN = 1`.

### 2.3 Time of Day
*   **Rule**: Schedule heavy scraping during off-peak hours (02:00 - 06:00 Local Time).

## 3. Data Privacy (GDPR/CCPA)

### 3.1 PII Handling
*   **Rule**: Do NOT scrape PII (Names, Emails, Phones) unless critical.
*   **Action**: If scraped, must be hashed/anonymized immediately.
*   **Storage**: Encrypted at rest.

### 3.2 Copyrighted Content
*   **Rule**: Do NOT scrape full articles/images for republication.
*   **Usage**: Fair Use (Snippets, Analysis) only.
*   **Attribution**: Always store source URL and timestamp.

## 4. Anti-Blocking Strategies (Ethical)

### 4.1 Headers
*   **Rule**: Use standard browser headers (Accept, Accept-Language).
*   **Rotation**: Rotate User-Agents from a valid list (no fake/malicious agents).

### 4.2 Proxies
*   **Rule**: Use residential proxies responsibly.
*   **Provider**: Bright Data / Smartproxy (Paid services only).

## 5. Code Example (Scrapy Settings)

```python
# settings.py

BOT_NAME = 'GaaraBot'

SPIDER_MODULES = ['gaara_scraper.spiders']
NEWSPIDER_MODULE = 'gaara_scraper.spiders'

# Obey robots.txt rules
ROBOTSTXT_OBEY = True

# Configure maximum concurrent requests performed by Scrapy (default: 16)
CONCURRENT_REQUESTS = 16

# Configure a delay for requests for the same website (default: 0)
DOWNLOAD_DELAY = 2.0
CONCURRENT_REQUESTS_PER_DOMAIN = 1
CONCURRENT_REQUESTS_PER_IP = 1

# Disable cookies (enabled by default)
COOKIES_ENABLED = False

# Identify the bot
USER_AGENT = 'GaaraBot/1.0 (+https://gaaragroup.com/bot-policy)'

# Enable AutoThrottle
AUTOTHROTTLE_ENABLED = True
AUTOTHROTTLE_START_DELAY = 5.0
AUTOTHROTTLE_MAX_DELAY = 60.0
```
