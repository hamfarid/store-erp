# Data Pipeline Documentation Template (v17.0)

## 1. Overview
*   **Pipeline Name**: [e.g., Customer Churn ETL]
*   **Owner**: [Data Engineer Name]
*   **Frequency**: [Daily/Hourly/Streaming]
*   **SLA**: [Data available by 08:00 UTC]

## 2. Architecture
*   **Source**: [PostgreSQL Table: users]
*   **Ingestion**: [Airbyte / Spark]
*   **Transformation**: [dbt / PySpark]
*   **Destination**: [Delta Lake: silver.churn_features]

## 3. Schema Definition
| Column Name | Type | Description | PII? | Nullable? |
| :--- | :--- | :--- | :--- | :--- |
| `user_id` | UUID | Unique User Identifier | No | No |
| `email` | String | User Email Address | **Yes** | No |
| `signup_date` | Date | Registration Date | No | No |
| `total_spend` | Float | Lifetime Value (USD) | No | Yes (0.0) |

## 4. Data Quality Checks (Great Expectations)
*   [ ] `user_id` is unique.
*   [ ] `total_spend` >= 0.
*   [ ] `email` matches regex `^[^@]+@[^@]+\.[^@]+$`.
*   [ ] Row count > 1000 (Daily minimum).

## 5. Lineage & Dependencies
*   **Upstream**: `raw.users_table` (Postgres)
*   **Downstream**: `gold.churn_prediction_model` (ML Training)

## 6. Access Control (RBAC)
*   **Read**: Data Scientists, ML Engineers.
*   **Write**: ETL Service Account only.
*   **PII Access**: Restricted (Masked for non-admin).

## 7. Troubleshooting
*   **Common Error 1**: Connection Timeout -> Retry (Max 3).
*   **Common Error 2**: Schema Mismatch -> Alert Data Steward.
*   **Logs**: [Link to Splunk/Datadog Dashboard]
