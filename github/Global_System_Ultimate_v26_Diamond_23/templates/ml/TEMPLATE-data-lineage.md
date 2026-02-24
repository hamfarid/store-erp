# Data Lineage Template
# Tooling: Amundsen, DataHub, OpenLineage

## Dataset Overview
*   **Dataset Name:** [e.g., `processed_customer_transactions`]
*   **Version:** [e.g., `v2.0`]
*   **Owner:** [Data Engineering Team]
*   **Last Updated:** [YYYY-MM-DD HH:MM:SS]

## Upstream Dependencies (Sources)
*   **Source 1:**
    *   **Name:** [e.g., `raw_transactions_kafka`]
    *   **Type:** [Kafka Topic]
    *   **Location:** [Cluster A, Topic B]
    *   **Transformation:** [e.g., JSON parsing, filtering nulls.]
*   **Source 2:**
    *   **Name:** [e.g., `customer_profiles_db`]
    *   **Type:** [PostgreSQL Table]
    *   **Location:** [DB Server C, Schema D, Table E]
    *   **Transformation:** [e.g., Join on `customer_id`.]

## Downstream Consumers (Targets)
*   **Consumer 1:**
    *   **Name:** [e.g., `churn_prediction_model`]
    *   **Type:** [ML Model]
    *   **Usage:** [Training data.]
*   **Consumer 2:**
    *   **Name:** [e.g., `marketing_dashboard`]
    *   **Type:** [Tableau Dashboard]
    *   **Usage:** [Daily reporting.]

## Transformation Logic
*   **Job Name:** [e.g., `etl_transactions_daily`]
*   **Engine:** [Spark 3.5]
*   **Code Repository:** [GitHub Link]
*   **Schedule:** [Daily at 02:00 UTC]

## Quality Checks
*   **Great Expectations Suite:** [Link to suite]
*   **Last Run Status:** [Success/Failure]
*   **Key Metrics:**
    *   `row_count`: [Value]
    *   `null_percentage`: [Value]
    *   `unique_ids`: [Value]
