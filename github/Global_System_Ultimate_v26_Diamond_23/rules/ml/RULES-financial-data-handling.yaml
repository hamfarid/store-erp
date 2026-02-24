# Financial Data Handling Rules (v17.0)
# Scope: FinTech & Banking ML
# Compliance: SOX, PCI-DSS, GDPR

## 1. Data Precision & Types

### 1.1 Decimal Handling
*   **Rule**: NEVER use floating-point types (float32/float64) for currency.
*   **Type**: Use `Decimal` (Python) or `NUMERIC(19,4)` (SQL).
*   **Reason**: IEEE 754 floating-point errors (0.1 + 0.2 != 0.3).

### 1.2 Time Handling
*   **Rule**: All timestamps MUST be UTC.
*   **Format**: ISO 8601 (`YYYY-MM-DDTHH:MM:SSZ`).
*   **DST**: Daylight Saving Time adjustments handled at presentation layer only.

## 2. PII & PCI Compliance

### 2.1 Masking
*   **Credit Card**: Mask all but last 4 digits (`****-****-****-1234`).
*   **SSN/ID**: Hash with salt (SHA-256).
*   **Email**: Mask local part (`j***@example.com`).

### 2.2 Encryption
*   **At Rest**: AES-256.
*   **In Transit**: TLS 1.3.
*   **Key Management**: Rotate keys every 90 days (AWS KMS / Vault).

## 3. Audit Trails (Immutable Logs)

### 3.1 Transaction Logs
*   **Requirement**: Every write operation must be logged.
*   **Fields**: `transaction_id`, `user_id`, `timestamp`, `action`, `ip_address`.
*   **Storage**: WORM (Write Once Read Many) storage (S3 Object Lock).

### 3.2 Model Explainability
*   **Requirement**: Every credit decision (Loan Approval/Denial) must have a reason code.
*   **Method**: SHAP values for top 3 features.
*   **Retention**: 7 years (Regulatory requirement).

## 4. Fraud Detection Rules

### 4.1 Velocity Checks
*   **Rule**: > 3 transactions from same IP in 1 minute -> Flag.
*   **Rule**: > 0,000 transfer -> Manual Review.

### 4.2 Geolocation
*   **Rule**: Transaction > 500 miles from last location in < 1 hour -> Block.

## 5. Code Example (Python Decimal)

```python
from decimal import Decimal, getcontext

# Set precision
getcontext().prec = 28

def calculate_interest(principal: Decimal, rate: Decimal, time: Decimal) -> Decimal:
    """
    Calculate compound interest with high precision.
    """
    if not isinstance(principal, Decimal):
        raise TypeError("Principal must be Decimal")
    
    amount = principal * (1 + rate) ** time
    return amount.quantize(Decimal("0.01"))  # Round to 2 decimal places

# Usage
p = Decimal("1000.00")
r = Decimal("0.05")
t = Decimal("10")
print(calculate_interest(p, r, t))
```
