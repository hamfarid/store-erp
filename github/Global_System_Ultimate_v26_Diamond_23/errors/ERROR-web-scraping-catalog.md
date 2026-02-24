# ERROR-web-scraping-catalog.md
# Governance: ML/AI Application Framework (Feb 2026)
# Tooling: Scrapy, Playwright

## 1. Rate Limiting (High Severity)
**ID:** `WS-RL-001`
**Name:** HTTP 429 Too Many Requests
**Description:** Server rejects requests due to excessive frequency.
**Detection:** HTTP Status Code 429.
**Resolution:** Implement exponential backoff with jitter; respect `Retry-After` header.
**Prevention:** `DOWNLOAD_DELAY = 10` (Scrapy); `AUTOTHROTTLE_ENABLED = True`.

## 2. IP Blocking (Critical Severity)
**ID:** `WS-IP-001`
**Name:** IP Ban
**Description:** Server blocks IP address due to suspicious activity.
**Detection:** HTTP Status Code 403/401; Connection Refused.
**Resolution:** Stop scraping immediately; wait 24 hours. NEVER rotate IPs to circumvent.
**Prevention:** Honest User-Agent; Respect `robots.txt`.

## 3. Dynamic Content Failures (Medium Severity)
**ID:** `WS-DC-001`
**Name:** JavaScript Rendering Failure
**Description:** Scraper fails to extract data loaded via AJAX/JS.
**Detection:** Empty fields; Missing elements.
**Resolution:** Switch to Playwright/Selenium; Use Scrapy-Playwright plugin.
**Prevention:** Inspect network tab; Identify API endpoints.

## 4. Session Expiration (Low Severity)
**ID:** `WS-SE-001`
**Name:** Cookie/Token Expiry
**Description:** Authentication token or session cookie becomes invalid.
**Detection:** HTTP Status Code 401; Redirect to login page.
**Resolution:** Refresh token; Re-login.
**Prevention:** Proactive token refresh; Monitor session lifetime.

## 5. HTML Structure Changes (Medium Severity)
**ID:** `WS-HS-001`
**Name:** Selector Failure
**Description:** Website layout changes break CSS/XPath selectors.
**Detection:** `IndexError`; `AttributeError`; Empty extraction.
**Resolution:** Update selectors; Use multiple selector strategies.
**Prevention:** Schema validation on output (Pydantic/JSON Schema).
