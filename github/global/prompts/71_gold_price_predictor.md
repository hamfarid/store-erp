# Prompt 71: Gold Price Predictor + Asset Predictor UI

> **Project**: Gold Price Predictor (Backend ML) + Asset Predictor UI (Frontend)
> **Framework**: Global System v26 Diamond 32 v26.0 Diamond 23+
> **OSF Score**: 0.97 (target 0.99)

## System Overview — Two Interconnected Systems

### System 1: Gold Price Predictor (Backend ML)
- **API**: FastAPI on Port 8001 (Repository Pattern + Service Layer)
- **ML Models**: 4 models = ARIMA (time series) + LSTM (deep learning) + Prophet (forecasting) + Ensemble (voting)
- **Assets**: Gold, Bitcoin, Ethereum, EGP_USD, TRY_USD
- **Accuracy**: 99.03% (Ensemble), Inference: 85ms, Model Size: 45MB
- **Database**: PostgreSQL 14 (read/write splitting + 11 strategic indexes)
- **Cache**: Redis 7 (cluster mode) — hit rate 60-80%, response ~2ms
- **Security**: AWS Secrets Manager (LRU cache 32 secrets) + JWT + MFA/TOTP (RFC 6238)
- **Monitoring**: Prometheus (9090) + Grafana (3000) + Streamlit (8501)
- **Compliance**: SOC 2, PCI DSS 3.2, NIST 800-63B
- **Tests**: 90%+ coverage (35+ tests, pytest + pytest-asyncio)

### System 2: Asset Predictor UI (Frontend + API)
- **Frontend**: React 19 + TypeScript 5.6 + Tailwind CSS 4 + shadcn/ui — 35+ pages
- **Backend**: Express 4 + tRPC 11 + Drizzle ORM
- **Database**: MySQL 8 — 25 tables
- **AI Assistants**: Goldy (Claude API — paid, unlimited) + Free (Gemini API — 10 msg/day)
- **ML Levels**: Simple (~85%) + Advanced (~92%) + Ensemble (~95%)
- **Time Horizons**: Short (7 days) + Medium (30 days) + Long (90 days)
- **News Service**: Auto-search + Sentiment Analysis + High-impact events + 30min cache
- **Portfolio**: Buy/sell transactions, ROI%, daily snapshots, asset allocation
- **Alert System**: 3 types (above/below/percentage change) + email + push
- **Auth**: JWT + OAuth + 14 permission levels
- **Endpoints**: 65+ API endpoints via tRPC

## Full ML Pipeline
1. Collect historical prices from external APIs
2. Train 4 models every 24 hours or on-demand (ARIMA, LSTM, Prophet, Ensemble)
3. Voting Ensemble combines 3 model predictions with optimized weights
4. Store predictions with confidence intervals (max/min)
5. Auto-monitor every 4 hours: compare prediction vs actual price
6. Drift Detection: if accuracy drops → auto-retrain
7. Trading Signals generated from predictions (breakout_points + trading_signals)
8. News Service adds sentiment score to each prediction
9. AI Assistants integrate: prediction + news + sentiment → comprehensive analysis

## System Integration Flow
```
Gold Price Predictor → trains models + serves prediction API
        ↓
Asset Predictor UI → consumes prediction API + displays to user
        ↓
News Service → feeds AI Assistants with news + sentiment
        ↓
AI Assistants (Goldy/Free) → analyze data + news → recommendations
        ↓
Alert System → monitors prices + sends notifications
        ↓
Portfolio Manager → tracks performance + calculates ROI
```

## Roadmap to OSF 0.99
- Performance: CDN (Cloudflare) + Gzip/Brotli + Celery async
- Usability: OpenAPI docs + SDKs (Python + JavaScript)
- Scalability: Kubernetes + auto-scaling + load balancer
- Inference: Target <50ms (current 85ms)
- Cache: Target 90%+ hit rate (current 60-80%)
- News: Add Arabic sources (Reuters Arabic, Al Jazeera, CNBC Arabic)
- Alerts: Add "AI Recommendation" alert type
- Frontend: Asset comparison page, Dark Mode, WebSocket for live prices
