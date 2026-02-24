# ML Model Backup & Retention Policy (v18.0)
# Scope: Disaster Recovery & Compliance
# Tools: AWS S3, Azure Blob, MinIO

## 1. Backup Frequency

### 1.1 Training Checkpoints
*   **Rule**: Save checkpoint every epoch.
*   **Retention**: Keep last 5 checkpoints only (Rolling Window).
*   **Storage**: Ephemeral storage (Scratchpad).

### 1.2 Final Models
*   **Rule**: Every successful training run MUST be backed up.
*   **Storage**: Durable Object Storage (S3 Standard).
*   **Replication**: Cross-Region Replication (CRR) enabled (e.g., us-east-1 -> eu-central-1).

## 2. Retention Schedule

### 2.1 Development Models
*   **Retention**: 30 days.
*   **Lifecycle**: Auto-delete after 30 days via S3 Lifecycle Rule.

### 2.2 Staging Models
*   **Retention**: 90 days.
*   **Lifecycle**: Transition to Glacier Instant Retrieval after 30 days.

### 2.3 Production Models
*   **Retention**: 7 years (Regulatory Requirement).
*   **Lifecycle**:
    *   Day 0-90: Standard Tier.
    *   Day 91-365: Glacier Instant Retrieval.
    *   Day 366+: Glacier Deep Archive.

## 3. Disaster Recovery (DR)

### 3.1 RPO (Recovery Point Objective)
*   **Target**: < 1 hour.
*   **Strategy**: Continuous replication of Model Registry database.

### 3.2 RTO (Recovery Time Objective)
*   **Target**: < 4 hours.
*   **Strategy**: Automated redeployment pipeline from backup region.

## 4. Security & Access

### 4.1 Encryption
*   **Rule**: Server-Side Encryption (SSE-KMS) with Customer Managed Keys (CMK).
*   **Key Rotation**: Automatic every year.

### 4.2 Immutability
*   **Rule**: Object Lock (WORM) enabled for Production models.
*   **Duration**: 7 years.

## 5. Code Example (S3 Lifecycle Config)

```json
{
    "Rules": [
        {
            "ID": "MoveToGlacier",
            "Prefix": "models/production/",
            "Status": "Enabled",
            "Transitions": [
                {
                    "Days": 90,
                    "StorageClass": "GLACIER_IR"
                },
                {
                    "Days": 365,
                    "StorageClass": "DEEP_ARCHIVE"
                }
            ],
            "Expiration": {
                "Days": 2555
            }
        }
    ]
}
```
