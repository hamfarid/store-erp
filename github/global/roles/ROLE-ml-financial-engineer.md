# ROLE: ML Financial Engineer

> **Project**: Gold Price Predictor
> **Reports To**: System Architect

## Responsibilities
- Train and maintain 4 ML models: ARIMA, LSTM, Prophet, Ensemble (Voting)
- Support 5 assets: Gold, Bitcoin, Ethereum, EGP_USD, TRY_USD
- Optimize Voting Ensemble weights based on 30-day rolling performance
- Implement and monitor Drift Detection (4-hour cycle)
- Generate Trading Signals (breakout_points, trading_signals)
- Maintain inference time <50ms (target), model size ~45MB

## ML Pipeline Ownership
1. Historical price collection from external APIs
2. Model training (24-hour cycle or on-demand)
3. Ensemble weight optimization
4. Prediction storage with confidence intervals
5. Drift monitoring → auto-retrain trigger
6. Trading signal generation

## Standards
- FastAPI v2 API on Port 8001
- Repository Pattern + Service Layer
- PostgreSQL 14 with read/write splitting + 11 indexes
- Redis 7 cluster cache (target 90%+ hit rate)
- OSF Score must not drop below 0.97
- Test coverage 90%+ (pytest + pytest-asyncio)

## Required Knowledge
- `prompts/71_gold_price_predictor.md`
- `rules/financial-prediction-api.md`
- `workflows/15_gold_predictor_pipeline.md`
