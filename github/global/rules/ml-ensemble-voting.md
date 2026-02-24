# Rule: ML Ensemble Voting Standards

> **Applies To**: Gold Price Predictor, any multi-model prediction system

## Ensemble Architecture
- Minimum 3 base models required for voting
- Each model must have independent prediction capability
- Ensemble combines predictions using weighted voting

## Weight Optimization
1. Weights MUST be based on actual performance (last 30 days)
2. Never use equal weights unless all models perform identically
3. Recalculate weights automatically after each drift detection cycle
4. Weight formula: `weight_i = accuracy_i / sum(all_accuracies)`

## Model Requirements
| Model | Type | Minimum Accuracy |
|:------|:-----|:----------------|
| ARIMA | Time Series | 85% |
| LSTM | Deep Learning | 88% |
| Prophet | Forecasting | 85% |
| Ensemble | Voting | 95% |

## Drift Detection
- Compare predicted vs actual every 4 hours
- PSI (Population Stability Index) threshold: 0.20
- If drift detected: auto-retrain affected model(s)
- Log all drift events to `drift_reports` table

## Prediction Storage
- All predictions stored with confidence intervals (min, max)
- Trading signals generated from predictions (breakout_points, buy/sell)
- Sentiment score attached from News Service
- Never delete prediction history (used for accuracy tracking)
