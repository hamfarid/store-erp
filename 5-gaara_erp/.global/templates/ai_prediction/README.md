# AI Prediction Template

**Machine Learning prediction and forecasting system**

---

## 📋 Overview

Complete AI prediction system for:
- **Time Series Forecasting** - Sales, demand, trends
- **Classification** - Customer churn, fraud detection
- **Regression** - Price prediction, risk assessment
- **Anomaly Detection** - Outlier detection
- **Recommendation** - Product recommendations

---

## 🏗️ Architecture

### Frontend
- **Framework:** React 18 + TypeScript
- **Charts:** Plotly.js (interactive charts)
- **Data Tables:** TanStack Table
- **Forms:** React Hook Form

### Backend
- **Framework:** FastAPI (Python 3.11+)
- **ML Framework:** Scikit-learn, XGBoost, LightGBM
- **Deep Learning:** TensorFlow / PyTorch
- **Time Series:** Prophet, ARIMA, LSTM
- **MLOps:** MLflow (experiment tracking)

### Database
- **Primary:** PostgreSQL (predictions, metadata)
- **Time Series:** TimescaleDB extension
- **Cache:** Redis

### ML Infrastructure
- **Training:** Jupyter notebooks
- **Serving:** FastAPI + Uvicorn
- **Monitoring:** Prometheus + Grafana
- **Model Registry:** MLflow

---

## 🚀 Features

### Data Management

✅ **Data Upload**
- CSV, Excel, JSON
- Database connection
- API integration
- Real-time streams

✅ **Data Preprocessing**
- Missing value handling
- Outlier detection
- Feature scaling
- Feature engineering

### Model Training

✅ **Algorithms**
- **Regression:** Linear, Ridge, Lasso, XGBoost
- **Classification:** Logistic, Random Forest, SVM
- **Time Series:** ARIMA, Prophet, LSTM
- **Clustering:** K-Means, DBSCAN
- **Ensemble:** Stacking, Voting

✅ **Training Pipeline**
- Data split (train/val/test)
- Cross-validation
- Hyperparameter tuning
- Model evaluation
- Model versioning

### Prediction & Forecasting

✅ **Batch Prediction**
- Upload data file
- Get predictions
- Download results

✅ **Real-time Prediction**
- API endpoint
- Single prediction
- Low latency

✅ **Forecasting**
- Future values
- Confidence intervals
- Trend analysis
- Seasonality detection

### Model Management

✅ **Model Registry**
- Version control
- Model comparison
- A/B testing
- Model deployment

✅ **Monitoring**
- Prediction accuracy
- Model drift detection
- Performance metrics
- Alerts

---

## 🚀 Quick Start

```bash
# 1. Generate from template
python3 ../../tools/template_generator.py \
  --template ai_prediction \
  --output ~/projects/my-ai-prediction

# 2. Navigate
cd ~/projects/my-ai-prediction

# 3. Configure
cp .env.example .env

# 4. Start
docker-compose up -d

# 5. Access Jupyter
# Jupyter: http://localhost:8888
# Token: check logs

# 6. Access app
# Frontend: http://localhost:3000
# Backend API: http://localhost:8000
# MLflow UI: http://localhost:5000
```

---

## 📁 Structure

```
ai_prediction/
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── DataUpload/
│   │   │   ├── ModelTraining/
│   │   │   ├── Prediction/
│   │   │   └── Monitoring/
│   │   ├── pages/
│   │   │   ├── Dashboard.tsx
│   │   │   ├── DataPage.tsx
│   │   │   ├── TrainPage.tsx
│   │   │   └── PredictPage.tsx
│   │   └── services/
│   └── package.json
├── backend/
│   ├── app/
│   │   ├── models/
│   │   │   ├── training.py
│   │   │   ├── prediction.py
│   │   │   └── evaluation.py
│   │   ├── data/
│   │   │   ├── preprocessing.py
│   │   │   ├── features.py
│   │   │   └── validation.py
│   │   ├── api/
│   │   │   ├── routes.py
│   │   │   ├── schemas.py
│   │   │   └── dependencies.py
│   │   └── config/
│   ├── requirements.txt
│   └── main.py
├── notebooks/
│   ├── 01_data_exploration.ipynb
│   ├── 02_feature_engineering.ipynb
│   ├── 03_model_training.ipynb
│   └── 04_model_evaluation.ipynb
├── models/
│   ├── saved_models/
│   └── model_artifacts/
├── data/
│   ├── raw/
│   ├── processed/
│   └── predictions/
├── docker/
├── tests/
├── docs/
├── .env.example
├── config.json
└── README.md
```

---

## 🔧 Configuration

### Environment Variables

```env
# Project
PROJECT_NAME={{PROJECT_NAME}}

# Database
DATABASE_URL=postgresql://user:pass@db:5432/{{DATABASE_NAME}}
REDIS_URL=redis://redis:6379/0

# MLflow
MLFLOW_TRACKING_URI=http://mlflow:5000
MLFLOW_EXPERIMENT_NAME={{PROJECT_NAME}}

# Model Configuration
DEFAULT_MODEL_TYPE=xgboost
MAX_TRAINING_TIME=3600
AUTO_RETRAIN=true
RETRAIN_INTERVAL=86400  # 24 hours

# Prediction
BATCH_SIZE=1000
PREDICTION_TIMEOUT=30
ENABLE_CACHING=true

# Monitoring
ENABLE_DRIFT_DETECTION=true
DRIFT_THRESHOLD=0.1
ALERT_EMAIL={{ADMIN_EMAIL}}

# Ports
FRONTEND_PORT={{FRONTEND_PORT}}
BACKEND_PORT={{BACKEND_PORT}}
MLFLOW_PORT=5000
JUPYTER_PORT=8888
```

---

## 🤖 ML Models

### Time Series Forecasting

```python
# Prophet for time series
from prophet import Prophet

model = Prophet(
    yearly_seasonality=True,
    weekly_seasonality=True,
    daily_seasonality=False
)

model.fit(df)
future = model.make_future_dataframe(periods=30)
forecast = model.predict(future)
```

### Classification

```python
# XGBoost for classification
import xgboost as xgb

model = xgb.XGBClassifier(
    max_depth=6,
    learning_rate=0.1,
    n_estimators=100,
    objective='binary:logistic'
)

model.fit(X_train, y_train)
predictions = model.predict(X_test)
```

### Regression

```python
# LightGBM for regression
import lightgbm as lgb

model = lgb.LGBMRegressor(
    num_leaves=31,
    learning_rate=0.05,
    n_estimators=100
)

model.fit(X_train, y_train)
predictions = model.predict(X_test)
```

---

## 📊 API Endpoints

### Data

- `POST /api/data/upload` - Upload dataset
- `GET /api/data/datasets` - List datasets
- `GET /api/data/{id}/preview` - Preview data
- `POST /api/data/{id}/preprocess` - Preprocess data

### Training

- `POST /api/train/start` - Start training
- `GET /api/train/status/{job_id}` - Training status
- `GET /api/train/models` - List trained models
- `GET /api/train/metrics/{model_id}` - Model metrics

### Prediction

- `POST /api/predict/single` - Single prediction
- `POST /api/predict/batch` - Batch prediction
- `POST /api/predict/forecast` - Time series forecast
- `GET /api/predict/history` - Prediction history

### Monitoring

- `GET /api/monitor/metrics` - Current metrics
- `GET /api/monitor/drift` - Drift detection
- `GET /api/monitor/alerts` - Active alerts

---

## 📈 Training Pipeline

### 1. Data Preparation

```python
from app.data.preprocessing import DataPreprocessor

preprocessor = DataPreprocessor()
X_train, X_test, y_train, y_test = preprocessor.prepare_data(
    df,
    target_column='target',
    test_size=0.2
)
```

### 2. Model Training

```python
from app.models.training import ModelTrainer

trainer = ModelTrainer(model_type='xgboost')
model, metrics = trainer.train(
    X_train, y_train,
    X_test, y_test,
    hyperparameters={'max_depth': 6}
)
```

### 3. Model Evaluation

```python
from app.models.evaluation import ModelEvaluator

evaluator = ModelEvaluator()
metrics = evaluator.evaluate(
    model, X_test, y_test
)

# Metrics: accuracy, precision, recall, F1, AUC
```

### 4. Model Deployment

```python
from app.models.deployment import ModelDeployer

deployer = ModelDeployer()
deployer.deploy(
    model,
    model_name='my_model',
    version='1.0.0'
)
```

---

## 🔍 Prediction Examples

### Single Prediction

```python
# Request
POST /api/predict/single
{
  "model_id": "model_123",
  "features": {
    "age": 35,
    "income": 50000,
    "credit_score": 720
  }
}

# Response
{
  "prediction": 0.85,
  "confidence": 0.92,
  "model_version": "1.0.0"
}
```

### Batch Prediction

```python
# Request
POST /api/predict/batch
{
  "model_id": "model_123",
  "data": [
    {"age": 35, "income": 50000},
    {"age": 42, "income": 75000}
  ]
}

# Response
{
  "predictions": [0.85, 0.72],
  "count": 2,
  "processing_time": 0.05
}
```

### Time Series Forecast

```python
# Request
POST /api/predict/forecast
{
  "model_id": "model_456",
  "periods": 30,
  "frequency": "D"
}

# Response
{
  "forecast": [100, 105, 110, ...],
  "lower_bound": [95, 98, 102, ...],
  "upper_bound": [105, 112, 118, ...],
  "dates": ["2025-01-01", "2025-01-02", ...]
}
```

---

## 📊 MLflow Integration

### Experiment Tracking

```python
import mlflow

with mlflow.start_run():
    # Log parameters
    mlflow.log_param("max_depth", 6)
    mlflow.log_param("learning_rate", 0.1)
    
    # Train model
    model.fit(X_train, y_train)
    
    # Log metrics
    mlflow.log_metric("accuracy", accuracy)
    mlflow.log_metric("f1_score", f1)
    
    # Log model
    mlflow.sklearn.log_model(model, "model")
```

### Model Registry

```python
# Register model
mlflow.register_model(
    "runs:/<run_id>/model",
    "my_prediction_model"
)

# Transition to production
client = mlflow.tracking.MlflowClient()
client.transition_model_version_stage(
    name="my_prediction_model",
    version=1,
    stage="Production"
)
```

---

## 🧪 Testing

```bash
# Unit tests
pytest tests/test_models.py

# Integration tests
pytest tests/test_api.py

# Performance tests
pytest tests/test_performance.py --benchmark
```

---

## 📈 Monitoring

### Model Drift Detection

```python
from app.monitoring.drift import DriftDetector

detector = DriftDetector()
drift_score = detector.detect_drift(
    reference_data=X_train,
    current_data=X_new
)

if drift_score > threshold:
    # Trigger retraining
    retrain_model()
```

### Performance Monitoring

- Prediction latency
- Throughput (predictions/sec)
- Model accuracy over time
- Resource usage (CPU, memory)

---

## ✅ Summary

**Complete AI prediction system** with:

✅ **Multiple algorithms** - Regression, classification, forecasting  
✅ **MLOps ready** - MLflow, monitoring, drift detection  
✅ **Production ready** - API, caching, scaling  
✅ **Jupyter notebooks** - Interactive development  
✅ **Real-time & batch** - Flexible prediction modes  
✅ **Model management** - Versioning, A/B testing

**Build intelligent prediction systems!** 🔮

---

**Template Version:** 1.0.0  
**Last Updated:** 2025-11-02  
**Status:** ✅ Production Ready

