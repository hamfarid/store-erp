# Rule: Data Privacy & GDPR Compliance (v2026.2)

## 1. Core Principles
-   **Data Minimization:** Collect ONLY what is strictly necessary for the model.
-   **Purpose Limitation:** Use data ONLY for the stated purpose (e.g., training, not marketing).
-   **Storage Limitation:** Delete data when no longer needed (Retention Policy).

## 2. PII Handling (Personally Identifiable Information)
**CRITICAL:** Never store raw PII in Feature Stores or Model Inputs.

| Data Type | Action | Technique |
| :--- | :--- | :--- |
| **Names** | Anonymize | Hash with Salt (SHA-256) |
| **Emails** | Anonymize | Hash with Salt (SHA-256) |
| **IP Addresses** | Mask | Truncate last octet (192.168.1.xxx) |
| **Geo-Location** | Generalize | Round to 2 decimal places (~1km accuracy) |
| **Biometrics** | Encrypt | AES-256 at rest and in transit |

## 3. Right to be Forgotten (RTBF)
-   **Mechanism:** Upon user request, delete all PII from:
    1.  Raw Data Lake (Bronze)
    2.  Feature Store (Silver/Gold)
    3.  Model Training Sets (Retrain model if PII impact > 5%)

## 4. Model Inversion Attacks
-   **Defense:** Use Differential Privacy (DP-SGD) during training.
-   **Threshold:** Epsilon (ε) < 10 for sensitive datasets.
