# Guide: Gold Price Predictor + Asset Predictor UI — Architecture Reference

> **Source**: GOLD_PREDICTOR_WHAT_TO_SAY.pdf (February 2026)

## System 1: Gold Price Predictor (Backend ML)

### Stack
- FastAPI (Python 3.11) — API v2 on Port 8001
- PostgreSQL 14 (read/write splitting + 11 strategic indexes)
- Redis 7 (cluster mode — hit rate 60-80%)
- Docker Compose (scalable to 3 instances)

### ML Models (4)
| Model | Type | Purpose |
|:------|:-----|:--------|
| ARIMA | Time Series | Statistical forecasting |
| LSTM | Deep Learning | Neural sequence prediction |
| Prophet | Forecasting | Trend + seasonality |
| Ensemble | Voting | Combines 3 models with optimized weights |

### Assets (5)
Gold, Bitcoin, Ethereum, EGP_USD, TRY_USD

### Metrics
- Accuracy: 99.03% (Ensemble)
- Inference: 85ms → target 50ms
- Model size: 45MB
- Query perf: 158ms → 12ms (92.4% improvement)
- OSF: 0.97 → target 0.99

### Security
- AWS Secrets Manager (LRU cache, 32 secrets)
- JWT + MFA/TOTP (RFC 6238)
- Rate Limiting per user + per IP
- Compliance: SOC 2, PCI DSS 3.2, NIST 800-63B

## System 2: Asset Predictor UI (Frontend + API)

### Stack
- React 19 + TypeScript 5.6 + Tailwind CSS 4 + shadcn/ui (35+ pages)
- Express 4 + tRPC 11 + Drizzle ORM
- MySQL 8 (25 tables)
- 65+ API endpoints via tRPC

### Features
- AI Assistants: Goldy (Claude, unlimited) + Free (Gemini, 10/day)
- News Service: auto search + sentiment analysis + 30min cache
- Portfolio: buy/sell transactions, daily snapshots, ROI
- Alert System: 3 types + email + push
- Auth: JWT + OAuth + 14 permission levels
- Task Scheduler: node-cron (daily analytics, weekly reports, auto alerts)

### Known Issues & Improvements Needed
- LSTM giving 91% instead of 99% — analyze drift
- Ensemble voting uses equal weights — optimize based on 30-day performance
- Goldy doesn't integrate prediction data — fix integration
- Free assistant exceeds 10 msgs/day — fix rate limiting
- Sentiment Analysis returns neutral for most news — improve prompt
- Cache too long for breaking news (30min) — add dual-layer: 5min + 30min
- Portfolio ROI inaccurate with multiple currencies — fix base currency conversion
- Email alerts disabled — fix email_settings
- Predictions page charts slow (>3s) — optimize Recharts
- ChatWidget loses state on navigation — fix state management
- Missing: asset comparison page, dark mode, Arabic news sources
- Missing: WebSocket for real-time prices, Kubernetes deployment
