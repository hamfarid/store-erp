# Workflow 15: Gold Price Predictor — ML Training & Prediction Pipeline

> **Trigger**: Every 24 hours (Celery Beat) or on-demand via API
> **System**: Gold Price Predictor Backend

## Steps

### Step 1: Data Collection
- Fetch latest prices from external APIs (Yahoo Finance, Alpha Vantage, CoinGecko)
- For each of 5 assets: Gold, Bitcoin, Ethereum, EGP_USD, TRY_USD
- Store in historical_prices table with timestamp

### Step 2: Feature Engineering
- Calculate technical indicators: SMA, EMA, RSI, MACD, Bollinger Bands
- Add time-based features: day of week, month, holiday proximity
- Add sentiment features from News Service

### Step 3: Train 4 Models
- **ARIMA**: Fit on last 365 days, predict 7/30/90 days
- **LSTM**: Train on sliding window (60-day lookback), sequence prediction
- **Prophet**: Fit with holidays + seasonality, forecast 7/30/90 days
- **Ensemble**: Weighted Voting (weights from last 30 days performance)

### Step 4: Store Predictions
- Save all predictions with confidence intervals (min, max)
- Generate trading signals (breakout points, buy/sell)
- Calculate trading signal strength

### Step 5: Post-Training Validation
- Compare new predictions vs recent actuals (backtest)
- Calculate OSF metrics
- If accuracy drops → trigger immediate retrain

## Error Handling
- If any model fails → continue with remaining models
- If all models fail → alert admin + use last valid prediction
- If data source unavailable → use cached data (Redis)
