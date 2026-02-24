# Example: Gold Price Predictor — Full ML Pipeline

> **Purpose**: End-to-end flow from data collection to trading signals

## Phase 1: Data Collection
```
External APIs (Yahoo Finance, Alpha Vantage, CoinGecko)
    → historical_prices table
    → 5 assets: Gold, Bitcoin, Ethereum, EGP_USD, TRY_USD
    → Daily + hourly granularity
```

## Phase 2: Model Training (Every 24h or On-Demand)
```
For each asset:
    1. ARIMA → fit on last 365 days → predict next 7/30/90 days
    2. LSTM → train on sliding window → sequence prediction
    3. Prophet → fit with holidays + seasonality → forecast
    4. Ensemble → Weighted Voting of ARIMA + LSTM + Prophet
       → Weights based on last 30 days accuracy
       → Example: ARIMA=0.25, LSTM=0.40, Prophet=0.35
```

## Phase 3: Prediction Storage
```
predictions table:
    asset, timeframe, predicted_price, confidence_min, confidence_max,
    arima_prediction, lstm_prediction, prophet_prediction,
    ensemble_prediction, ensemble_weights, created_at
```

## Phase 4: Drift Detection (Every 4h)
```
Compare:
    predicted_price vs actual_price
    Calculate: MAE, RMSE, directional accuracy
    If PSI > 0.20 → trigger auto-retrain
    Log to drift_reports table
```

## Phase 5: Trading Signals
```
From predictions → generate:
    breakout_points (support/resistance levels)
    trading_signals (BUY/SELL/HOLD)
    sentiment_score (from News Service)
```

## Phase 6: AI Assistant Integration
```
User asks Goldy: "What about gold this week?"
    1. Goldy → GET /api/v2/predictions/gold?timeframe=short
    2. Goldy → GET /api/v2/news/gold?sentiment=true
    3. Goldy → Claude prompt: prediction + news + sentiment
    4. Return: comprehensive analysis with confidence intervals
```
