# Internet Search Protocol (ISP) - v2026.2
**Governance:** Global System Ultimate
**Compliance:** GDPR, EU AI Act, Robots.txt

## 1. Purpose
To define the mandatory standards for AI agents conducting internet research, web scraping, and external data verification. This protocol ensures legal compliance, data integrity, and ethical conduct.

## 2. The Golden Rules of Search
1.  **Verify, Don't Trust:** Search results are starting points, not facts. Cross-reference at least 3 independent sources.
2.  **Respect Boundaries:** Strictly adhere to `robots.txt` and site terms of service.
3.  **Identify Yourself:** Use a transparent User-Agent string (e.g., `GlobalSystemBot/1.0 (contact@example.com)`).
4.  **Rate Limiting:** Never exceed 1 request per 10 seconds per domain unless explicitly allowed.

## 3. Search Methodology (The 3-Step Process)

### Step 1: Discovery (Broad Search)
*   **Tool:** Search Engine (Google/Bing/Brave).
*   **Query Strategy:** Use specific keywords, boolean operators (`site:`, `filetype:`), and time filters (`after:2025-01-01`).
*   **Goal:** Identify primary sources (official documentation, academic papers, government reports).

### Step 2: Extraction (Targeted Scraping)
*   **Tool:** Scrapy, BeautifulSoup, Playwright.
*   **Governance:** Refer to `ml-ai-governance/rules/RULES-web-scraping-compliance.yaml`.
*   **Constraint:** Do NOT scrape PII (Personally Identifiable Information) without lawful basis.

### Step 3: Verification (Fact-Checking)
*   **Tool:** FINCH-ZK Protocol.
*   **Action:** Verify claims against the extracted primary source.
*   **Output:** A citation link with access date.

## 4. Compliance Checklist
*   [ ] Checked `robots.txt`?
*   [ ] User-Agent configured?
*   [ ] Rate limiting enabled?
*   [ ] PII scanning active?
*   [ ] Data source is reputable?

## 5. Forbidden Actions
*   ❌ Bypassing CAPTCHAs.
*   ❌ Rotating IPs to evade bans.
*   ❌ Scraping behind login walls without authorization.
*   ❌ Using "headless" browsers to deceive anti-bot systems.

## 6. Integration with ML Governance
*   Scraped data MUST be validated against `ml-ai-governance/rules/RULES-data-validation.yaml`.
*   Data lineage MUST be tracked in `ml-ai-governance/templates/TEMPLATE-dataset-datasheet.md`.
