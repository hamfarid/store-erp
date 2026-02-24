# Financial Forecasting & ML Rules (Dual-System)

**Version:** 1.0 (Diamond 27)
**Source:** Gold Price Predictor Guide

## 1. Data Precision & Handling
*   **Decimal Precision:** All financial values (prices, predictions) MUST be stored and processed with at least **4 decimal places** (e.g., `1234.5678`).
*   **Currency Handling:** NEVER use floating-point arithmetic for currency calculations. Use `Decimal` types in Python and appropriate fixed-point libraries in JS.
*   **Time Zones:** All timestamps MUST be stored in **UTC**. Conversions to local time (e.g., Cairo Time) happen ONLY at the presentation layer.

## 2. Model Architecture (The 4-Pillar Strategy)
We use a specific ensemble of 4 model types for robust prediction:

| Model Type | Library | Role | Strengths | Weaknesses |
| :--- | :--- | :--- | :--- | :--- |
| **ARIMA** | `statsmodels` | Short-term linear trends | Excellent for immediate next-step prediction | Fails on non-linear/complex patterns |
| **LSTM** | `PyTorch` | Complex non-linear patterns | Captures long-term dependencies | Requires GPU for training, data-hungry |
| **Prophet** | `prophet` | Seasonality & Holidays | Handles missing data, strong seasonal decomposition | Can overfit if not tuned |
| **Ensemble** | `scikit-learn` | Weighted Average | Balances errors from individual models | Only as good as its components |

## 3. Training & Retraining Schedule
Strict adherence to this schedule is required to maintain model freshness without wasting resources.

*   **ARIMA:** Retrain **DAILY** (Rolling window: 365-500 days).
    *   *Reason:* Highly sensitive to recent autocorrelation.
*   **LSTM:** Retrain **WEEKLY** (Sunday 03:00 AM UTC).
    *   *Reason:* Computationally expensive, marginal gain from daily retraining.
*   **Prophet:** Retrain **WEEKLY** (Sunday 03:30 AM UTC).
    *   *Reason:* Seasonality patterns change slowly.
*   **Ensemble Weights:** Update **DAILY** based on the last 30 days of prediction error (MAPE).

## 4. Docker & Deployment Constraints
*   **Prophet Complexity:** Prophet requires `g++` and `cmdstanpy`. Use the **Multi-Stage Build** pattern:
    *   *Builder Stage:* Install compilers, build wheels.
    *   *Runtime Stage:* Copy wheels, keep image slim (~3-4GB with CUDA, ~1.5GB CPU-only).
*   **GPU/CPU Hybrid:**
    *   **Inference:** Run ALL models on CPU (ONNX Runtime preferred) for cost efficiency.
    *   **Training:** Route LSTM training to GPU nodes (if available); fallback to CPU if not.

## 5. Validation Metrics
*   **Primary Metric:** MAPE (Mean Absolute Percentage Error).
*   **Secondary Metric:** RMSE (Root Mean Square Error).
*   **Directional Accuracy:** % of times the model correctly predicted the direction (Up/Down).

## 6. Anti-Hallucination in Finance
*   **Source of Truth:** All historical data MUST be verified against trusted APIs (e.g., Yahoo Finance, Alpha Vantage).
*   **Sanity Checks:**
    *   If prediction deviates > 5% from current price in 24h -> **FLAG WARNING**.
    *   If prediction is negative -> **REJECT**.
