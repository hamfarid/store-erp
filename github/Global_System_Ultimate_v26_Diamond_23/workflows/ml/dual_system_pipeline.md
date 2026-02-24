# Dual-System ML Pipeline Workflow (FastAPI + React)

**Version:** 1.0 (Diamond 27)
**Source:** Gold Price Predictor Guide

## 1. Overview
This workflow defines the end-to-end process for the **Dual-System Architecture**, connecting the **FastAPI ML Backend** (Prediction Engine) with the **React Frontend** (Visualization Layer).

## 2. The Pipeline Stages

### Stage 1: Data Ingestion (Daily/Weekly)
*   **Trigger:** Celery Beat Scheduler (Daily 02:00 UTC).
*   **Action:** Fetch OHLCV data for 5 assets (Gold, BTC, ETH, EGP, TRY).
*   **Validation:** Check for missing values, outliers, and data integrity.
*   **Storage:** Save raw data to PostgreSQL (`raw_prices` table).

### Stage 2: Feature Engineering (On-Demand/Batch)
*   **Trigger:** After successful data ingestion.
*   **Action:** Calculate technical indicators (RSI, MACD, Bollinger Bands).
*   **Transformation:** Normalize/Scale data for LSTM (MinMax Scaler).
*   **Storage:** Save processed features to PostgreSQL (`features` table) or Redis (Cache).

### Stage 3: Model Training & Retraining (Scheduled)
*   **Trigger:** Celery Beat Scheduler (Specific times per model type).
*   **Action:**
    1.  **Load Data:** Fetch latest training window (e.g., last 365 days).
    2.  **Train Model:** Execute training script (ARIMA/LSTM/Prophet).
    3.  **Evaluate:** Calculate MAPE on hold-out set (last 30 days).
    4.  **Save Model:** Serialize model (Pickle/PyTorch/JSON) to `models/` directory.
    5.  **Log Metrics:** Record training metrics to MLflow/Weights & Biases.

### Stage 4: Inference & Prediction (Real-Time/Batch)
*   **Trigger:** API Request (`POST /predict`) or Scheduled Batch.
*   **Action:**
    1.  **Load Model:** Load the best-performing model for the requested asset.
    2.  **Preprocess Input:** Apply same transformations as training.
    3.  **Predict:** Generate forecast for requested horizon (7d, 30d, 90d).
    4.  **Postprocess:** Inverse transform predictions to original scale.
    5.  **Return:** JSON response with prediction values and confidence intervals.

### Stage 5: Visualization & Consumption (Frontend)
*   **Trigger:** User interaction or Dashboard refresh.
*   **Action:**
    1.  **Fetch Data:** Call FastAPI endpoints (`GET /forecasts`).
    2.  **Render Charts:** Display historical data + future predictions using Recharts/Chart.js.
    3.  **Alerting:** Highlight significant trends or anomalies.

## 3. Error Handling & Fallback
*   **Model Failure:** If a model fails to load or predict -> **Fallback to Simple Moving Average (SMA)**.
*   **Data Missing:** If live data is unavailable -> **Use last known close price**.
*   **API Timeout:** If backend is slow -> **Show cached predictions (Redis)**.

## 4. Monitoring & Drift Detection
*   **Drift Check:** Compare new data distribution with training data distribution (PSI/KL Divergence).
*   **Performance Check:** Monitor MAPE over time. If MAPE > Threshold -> **Trigger Retraining**.
