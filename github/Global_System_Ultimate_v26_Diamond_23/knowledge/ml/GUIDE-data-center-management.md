# Data Center & Big Data Management Guide (v2026.2)

## 1. Overview
This guide defines the infrastructure and governance for managing large-scale data centers and big data ecosystems (Spark, Hadoop, Kafka).

## 2. Infrastructure Architecture

### 2.1 Compute Layer (Kubernetes)
-   **Node Pools:** Separate pools for CPU (general), GPU (training), and High-Memory (Spark).
-   **Autoscaling:** Use Cluster Autoscaler (CA) and Horizontal Pod Autoscaler (HPA).
-   **Resource Quotas:** Enforce limits per namespace (e.g., `ml-training`, `data-engineering`).

### 2.2 Storage Layer (Data Lake)
-   **Bronze (Raw):** Immutable raw data (JSON, CSV, Logs). Retention: 7 years.
-   **Silver (Cleaned):** Validated, enriched data (Parquet/Delta). Retention: 3 years.
-   **Gold (Aggregated):** Business-ready metrics (Delta Tables). Retention: 1 year.

### 2.3 Streaming Layer (Kafka)
-   **Topics:** Partition by key (e.g., `user_id`, `sensor_id`).
-   **Retention:** 7 days for raw streams, infinite for compacted topics.
-   **Schema Registry:** Enforce Avro schemas for all producers.

## 3. Governance Rules

### 3.1 Data Access Control (RBAC)
-   **Data Engineers:** Read/Write access to Bronze/Silver.
-   **Data Scientists:** Read access to Silver/Gold. Write to `sandbox/`.
-   **Analysts:** Read access to Gold only.

### 3.2 Cost Management (FinOps)
-   **Tagging:** All resources MUST have `CostCenter`, `Owner`, and `Environment` tags.
-   **Spot Instances:** Use Spot instances for stateless workloads (Spark Executors, Batch Jobs).
-   **Lifecycle Policies:** Automatically move cold data to Glacier/Archive storage after 90 days.

### 3.3 Monitoring & Alerting
-   **Prometheus:** Scrape metrics from Spark Drivers, Kafka Brokers, and K8s Nodes.
-   **Grafana:** Dashboards for Cluster Health, Job Latency, and Cost Trends.
-   **AlertManager:** Critical alerts (e.g., `DiskUsage > 90%`, `JobFailureRate > 5%`) sent to PagerDuty.

## 4. Disaster Recovery (DR)
-   **RPO (Recovery Point Objective):** 1 hour for critical data, 24 hours for non-critical.
-   **RTO (Recovery Time Objective):** 4 hours.
-   **Backup Strategy:** Daily snapshots of databases, continuous replication of S3 buckets to DR region.
