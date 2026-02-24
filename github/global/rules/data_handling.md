# Data Handling Rules

## Overview
These rules govern the handling, processing, and storage of all data within the Gaara AI ecosystem. They are designed to ensure data integrity, security, and compliance with all applicable regulations.

## Data Acquisition
1. **Source Verification**: All data must be sourced from reputable and verified providers (e.g., Bloomberg, Reuters, official exchanges).
2. **Data Integrity**: Implement checksums and validation checks to detect and prevent data corruption during transmission and storage.
3. **Currency Standardization**: All monetary values must be clearly denominated in their respective currencies (e.g., USD, EGP, TRY). Use ISO 4217 currency codes.
4. **Decimal Precision**: Maintain a minimum of 4 decimal places for currency exchange rates and 2 decimal places for asset prices, unless otherwise specified.
5. **Time Synchronization**: Ensure all timestamps are synchronized to UTC and clearly labeled with the time zone.

## Data Processing
1. **Data Cleaning**: Implement robust data cleaning procedures to handle missing values, outliers, and inconsistencies.
2. **Feature Engineering**: Develop and maintain a library of standardized features for use in predictive models.
3. **Normalization**: Normalize all numerical data to a common scale (e.g., 0-1) to improve model performance.
4. **Categorical Encoding**: Encode categorical variables using appropriate techniques (e.g., one-hot encoding, label encoding).
5. **Data Transformation**: Apply necessary transformations (e.g., log transformation, differencing) to stabilize variance and improve model accuracy.

## Mandatory Logging Requirements
**CRITICAL: All data operations MUST be logged using the `logger` module.**

### 1. Data Ingestion Logging (System Log)
- **Source**: Log the origin of every data batch (e.g., "Ingested 500 records from Binance API").
- **Volume**: Log the size and record count of ingested data.
- **Status**: Log success or failure of the ingestion process.
- **Code Example**:
    ```python
    logger.log_system("INFO", "Data Ingestion", "Binance API", "500 records", "Success")
    ```

### 2. Processing Logging (AI Log)
- **Transformations**: Log every transformation applied to the data (e.g., "Normalized price column using MinMaxScaler").
- **Cleaning**: Log details of data cleaning operations (e.g., "Imputed 5 missing values in 'volume' column").
- **Feature Engineering**: Log the creation of new features (e.g., "Generated 'RSI_14' feature").
- **Code Example**:
    ```python
    logger.log_ai("Data Processor", "Feature Engineering", "RSI_14", "Created", "Success")
    ```

### 3. Data Access Logging (IP Log)
- **Query Access**: Log the IP address and user ID of any entity querying the database.
- **Export**: Log any data export operations, including the destination and volume.
- **Code Example**:
    ```python
    logger.log_ip("192.168.1.50", "Analyst_01", "SELECT * FROM market_data", "Query", "Success")
    ```

### 4. Audit Trail (System Log)
- **Schema Changes**: Log any changes to database schemas (e.g., "Added 'sentiment_score' column to 'market_data' table").
- **Policy Updates**: Log updates to data retention or privacy policies.
- **Code Example**:
    ```python
    logger.log_system("WARN", "Schema Change", "Added column 'sentiment_score'", "Approved by Architect")
    ```

## Data Storage
1. **Database Selection**: Utilize appropriate databases for different data types (e.g., PostgreSQL for structured data, Redis for caching, Qdrant for vector embeddings).
2. **Data Partitioning**: Implement data partitioning strategies (e.g., time-based partitioning) to optimize query performance and storage efficiency.
3. **Backup & Recovery**: Establish regular backup schedules and test recovery procedures to ensure data availability in case of failure.
4. **Access Control**: Implement strict access controls (RBAC) to restrict data access to authorized personnel only.
5. **Encryption**: Encrypt sensitive data at rest and in transit using industry-standard encryption algorithms (e.g., AES-256).

## Data Governance
1. **Data Catalog**: Maintain a comprehensive data catalog documenting all data sources, schemas, and lineage.
2. **Data Quality Monitoring**: Continuously monitor data quality metrics (e.g., completeness, accuracy, consistency) and alert on anomalies.
3. **Data Retention**: Define and enforce data retention policies based on legal and business requirements.
4. **Data Privacy**: Ensure compliance with data privacy regulations (e.g., GDPR, CCPA) by implementing data anonymization and pseudonymization techniques where applicable.
5. **Audit Trail**: Maintain a comprehensive audit trail of all data access, modifications, and deletions for accountability.

## TimescaleDB Schema (Example)
```sql
CREATE TABLE IF NOT EXISTS market_data (
    time TIMESTAMPTZ NOT NULL,
    symbol TEXT NOT NULL,
    price DOUBLE PRECISION NOT NULL,
    volume DOUBLE PRECISION NOT NULL,
    source TEXT NOT NULL
);

SELECT create_hypertable('market_data', 'time');
```

## Redis Key Naming Convention
- **Format**: `service:entity:id:attribute`
- **Example**: `market:gold:price:latest`
- **Example**: `user:12345:session:token`

## Backup Procedures
1. **PostgreSQL**: Daily full backup using `pg_dump` to S3 bucket `gaara-backups-db`. **Log to System Log.**
2. **Redis**: Hourly RDB snapshots to S3 bucket `gaara-backups-redis`. **Log to System Log.**
3. **Qdrant**: Daily snapshot of collections to S3 bucket `gaara-backups-qdrant`. **Log to System Log.**
4. **Retention**: Keep daily backups for 30 days, weekly backups for 1 year.
