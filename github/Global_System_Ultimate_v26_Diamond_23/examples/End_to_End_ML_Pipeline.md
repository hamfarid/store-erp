# Example: End-to-End ML Pipeline (v2026.2)

## 1. Overview
This example demonstrates a complete ML pipeline for a **Customer Churn Prediction** model, from data ingestion to deployment.

## 2. Architecture
-   **Ingestion:** Kafka (Real-time events) -> Spark Streaming -> Delta Lake (Bronze).
-   **Processing:** Spark Batch (Daily) -> Feature Engineering -> Feature Store (Silver).
-   **Training:** PyTorch (GPU Cluster) -> MLflow (Tracking) -> Model Registry.
-   **Serving:** FastAPI (K8s) -> Redis (Feature Cache) -> User.

## 3. Pipeline Steps

### Step 1: Data Ingestion (Spark)
```python
df = spark.readStream.format("kafka") \
    .option("kafka.bootstrap.servers", "broker:9092") \
    .option("subscribe", "user_events") \
    .load()

df.writeStream.format("delta") \
    .outputMode("append") \
    .option("checkpointLocation", "/tmp/checkpoint") \
    .start("/mnt/delta/bronze/events")
```

### Step 2: Feature Engineering (Pandas/Spark)
```python
def compute_features(df):
    df['days_since_login'] = (current_date - df['last_login']).dt.days
    df['avg_spend_30d'] = df['spend_history'].apply(lambda x: sum(x[-30:]) / 30)
    return df

features = compute_features(raw_data)
features.to_sql('feature_store', con=engine, if_exists='append')
```

### Step 3: Model Training (PyTorch)
```python
model = ChurnModel()
optimizer = torch.optim.Adam(model.parameters(), lr=0.001)

for epoch in range(10):
    train_loss = train_one_epoch(model, train_loader, optimizer)
    val_acc = validate(model, val_loader)
    
    mlflow.log_metric("train_loss", train_loss)
    mlflow.log_metric("val_acc", val_acc)

mlflow.pytorch.log_model(model, "churn_model")
```

### Step 4: Deployment (FastAPI)
```python
app = FastAPI()
model = mlflow.pytorch.load_model("models:/churn_model/Production")

@app.post("/predict")
async def predict(user_id: int):
    features = get_features_from_redis(user_id)
    prediction = model(torch.tensor(features))
    return {"churn_prob": prediction.item()}
```
