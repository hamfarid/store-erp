# ML Data Validation Rules (v18.0)
# Scope: Data Quality & Schema Enforcement
# Tools: Great Expectations, Pandera, Pydantic

## 1. Schema Validation (Pandera)

### 1.1 Column Types
*   **Rule**: All columns must have explicit types (int64, float32, category, datetime64[ns]).
*   **Check**: `pa.Check.isin(['Apple', 'Tomato'])` for categorical columns.
*   **Nullable**: Explicitly define nullable columns (default: False).

### 1.2 Range Checks
*   **Rule**: Numerical features must be within [min, max] bounds.
*   **Example**: `ph_level` must be between 0.0 and 14.0.
*   **Example**: `humidity` must be between 0.0 and 100.0.

## 2. Data Quality Gates (Great Expectations)

### 2.1 Completeness
*   **Rule**: `expect_column_values_to_not_be_null` > 99% for critical features.
*   **Action**: Fail pipeline if > 1% missing values in `image_path`.

### 2.2 Uniqueness
*   **Rule**: `expect_column_values_to_be_unique` for `image_id`.
*   **Action**: Drop duplicates, log warning if > 0.1% duplicates.

### 2.3 Distribution Checks
*   **Rule**: `expect_column_kl_divergence_to_be_less_than` (0.1) vs Reference Set.
*   **Action**: Trigger Drift Alert if distribution shifts significantly.

## 3. Image Data Validation

### 3.1 File Integrity
*   **Rule**: All files must be valid images (JPEG/PNG).
*   **Check**: `PIL.Image.verify()` must pass.
*   **Action**: Quarantine corrupt files to `data/quarantine/`.

### 3.2 Dimensions
*   **Rule**: Minimum resolution 224x224.
*   **Check**: `width >= 224 AND height >= 224`.
*   **Action**: Resize or discard if too small.

### 3.3 Channels
*   **Rule**: Must be RGB (3 channels).
*   **Check**: Convert RGBA/Grayscale to RGB.

## 4. Label Validation

### 4.1 Class Balance
*   **Rule**: No class should have < 100 samples.
*   **Action**: Augment minority classes or drop if < 10 samples.

### 4.2 Label Format
*   **Rule**: Labels must match `classes.json` exactly.
*   **Check**: Set difference must be empty.

## 5. Code Example (Pandera Schema)

```python
import pandera as pa
from pandera.typing import Series

class PlantDiseaseSchema(pa.SchemaModel):
    image_id: Series[str] = pa.Field(unique=True, allow_duplicates=False)
    label: Series[str] = pa.Field(isin=["Healthy", "Rust", "Scab"])
    confidence: Series[float] = pa.Field(ge=0.0, le=1.0)
    timestamp: Series[pa.DateTime]
    
    class Config:
        coerce = True
        strict = True

def validate_dataframe(df):
    try:
        PlantDiseaseSchema.validate(df, lazy=True)
        print("Validation Passed")
    except pa.errors.SchemaErrors as err:
        print("Schema Errors:", err.failure_cases)
        raise
```
