# ERROR-financial-data-catalog.md
# Governance: ML/AI Application Framework (Feb 2026)
# Tooling: Pandas, NumPy, QuantLib

## 1. Timezone Mishandling (Critical Severity)
**ID:** `FD-TZ-001`
**Name:** DST Transition Error
**Description:** Spring-forward (missing hour) or Fall-back (doubled hour) corrupts dataset.
**Detection:** `pd.to_datetime(utc=True)` fails; Duplicate timestamps.
**Resolution:** Convert to UTC immediately upon ingestion.
**Prevention:** Store, transmit, compute, and log in UTC.

## 2. Stale Data (High Severity)
**ID:** `FD-SD-001`
**Name:** Stale Quote
**Description:** Price feed stops updating, leading to outdated trading decisions.
**Detection:** Timestamp difference > threshold (e.g., 1 min).
**Resolution:** Switch to secondary provider; Halt trading.
**Prevention:** Heartbeat monitoring; Redundant feeds.

## 3. Corporate Actions (Medium Severity)
**ID:** `FD-CA-001`
**Name:** Unadjusted Price
**Description:** Stock split or dividend not reflected in historical data.
**Detection:** Sudden price drop (e.g., 50% for 2:1 split).
**Resolution:** Apply adjustment factor from corporate action feed.
**Prevention:** Use adjusted close prices; Monitor corporate action calendar.

## 4. API Limits (Low Severity)
**ID:** `FD-AL-001`
**Name:** Rate Limit Exceeded
**Description:** API provider blocks requests due to excessive frequency.
**Detection:** HTTP 429; `RateLimitError`.
**Resolution:** Implement exponential backoff; Cache responses.
**Prevention:** Respect provider limits; Use bulk endpoints.
