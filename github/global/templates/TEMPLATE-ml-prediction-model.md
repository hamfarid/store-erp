# Template: ML Prediction Model

> **Use For**: Adding new prediction models to Gold Price Predictor or any time-series system

## Model Registration
```python
class PredictionModel:
    name: str              # e.g., "ARIMA", "LSTM", "Prophet", "XGBoost"
    version: int           # auto-increment
    asset: str             # e.g., "gold", "bitcoin"
    timeframes: list       # ["short", "medium", "long"] → [7d, 30d, 90d]
    accuracy_30d: float    # accuracy over last 30 days
    ensemble_weight: float # weight in voting ensemble
```

## Prediction Output Schema
```python
class Prediction:
    asset: str
    timeframe: str
    predicted_price: float
    confidence_min: float
    confidence_max: float
    model_name: str
    model_version: int
    trading_signal: str    # BUY / SELL / HOLD
    signal_strength: float # 0.0 - 1.0
    created_at: datetime
```

## Integration Checklist
- [ ] Model trained on historical data
- [ ] Backtest results documented
- [ ] Ensemble weights updated
- [ ] API endpoint added: `GET /api/v2/predictions/{asset}?model={name}`
- [ ] Drift detection configured
- [ ] OSF Score recalculated
