# EXAMPLE-realtime-market-data.md
# Governance: ML/AI Application Framework (Feb 2026)
# Tooling: WebSocket, Redis, Kafka

## 1. Project Structure
```
realtime-market-data/
├── configs/
│   ├── config.yaml          # API keys, endpoints
│   └── logging.yaml         # Logging configuration
├── src/
│   ├── websocket/           # WebSocket client (Alpha Vantage/EODHD)
│   ├── processing/          # Data processing pipeline
│   └── storage/             # Data storage (Redis/Kafka)
├── tests/                   # Unit and integration tests
├── Dockerfile               # Multi-stage build
├── requirements.txt         # Pinned dependencies
└── README.md                # Project documentation
```

## 2. API Selection
*   **Alpha Vantage:** Broad coverage (Stocks, Forex, Crypto).
*   **EODHD:** Low latency (< 50ms) WebSocket streaming.
*   **Finnhub:** Generous free tier (US Stocks).
*   **OANDA:** Forex streaming (Requires account).

## 3. WebSocket Governance
*   **Connection Reuse:** Maintain persistent connection (Keep-Alive).
*   **Heartbeat:** Send ping/pong every 30s.
*   **Reconnection:** Exponential backoff (1s, 2s, 4s, 8s, 16s).
*   **Subscription:** Unsubscribe from unused tickers to save bandwidth.

## 4. Data Processing
*   **Normalization:** Convert all prices to float64.
*   **Timestamp:** Convert to UTC immediately (ISO 8601).
*   **Validation:** Check for outliers (e.g., price change > 10% in 1s).
*   **Buffering:** Use Redis/Kafka for high-throughput ingestion.

## 5. Storage Strategy
*   **Hot Data:** Redis (Last 1 hour).
*   **Warm Data:** Kafka (Last 24 hours).
*   **Cold Data:** S3/Parquet (Historical archive).
