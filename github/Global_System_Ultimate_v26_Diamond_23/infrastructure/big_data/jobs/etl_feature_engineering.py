from pyspark.sql import SparkSession
from pyspark.ml.feature import VectorAssembler, StandardScaler
from pyspark.ml import Pipeline
import mlflow

def main():
    spark = SparkSession.builder \
        .appName("FeatureEngineeringJob") \
        .getOrCreate()

    # 1. Load Raw Data (Parquet/Delta)
    raw_df = spark.read.format("delta").load("s3a://datalake/raw/transactions")

    # 2. Feature Engineering
    assembler = VectorAssembler(
        inputCols=["amount", "hour_of_day", "category_encoded"],
        outputCol="features_vec"
    )
    
    scaler = StandardScaler(
        inputCol="features_vec",
        outputCol="scaled_features",
        withStd=True, withMean=False
    )

    pipeline = Pipeline(stages=[assembler, scaler])
    
    # 3. Fit & Transform
    model = pipeline.fit(raw_df)
    transformed_df = model.transform(raw_df)

    # 4. Save to Feature Store (PostgreSQL via JDBC)
    transformed_df.select("user_id", "timestamp", "scaled_features") \
        .write \
        .format("jdbc") \
        .option("url", "jdbc:postgresql://db:5432/feature_store") \
        .option("dbtable", "user_features") \
        .option("user", "admin") \
        .option("password", "secret") \
        .save()

    # 5. Log Model to MLflow
    with mlflow.start_run():
        mlflow.spark.log_model(model, "feature_pipeline")

if __name__ == "__main__":
    main()
