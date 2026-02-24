# 🧪 Testing & QA Workflow (AI Learning Guide)

This document teaches the AI how to write, organize, and execute tests.

## 1. Standard Test Structure
Every test file (e.g., `test_auth.py`, `test_api_flow.py`) must follow this pattern:

### 📥 Imports (Inputs)
*   **Test Framework**: `pytest`, `unittest`, `jest`.
*   **Target Module**: The code being tested.
*   **Fixtures**: Mock data, DB sessions, API clients.

### 📤 Exports (Outputs)
*   **Test Cases**: Functions starting with `test_`.
*   **Assertions**: Pass/Fail results.
*   **Reports**: Coverage reports, XML results.

### 🔄 Operational Workflow (AAA Pattern)
1.  **Arrange**: Set up the environment (mocks, DB).
2.  **Act**: Execute the function or API call.
3.  **Assert**: Verify the result matches expectations.
4.  **Cleanup**: Teardown resources.

## 2. Example: Unit Test (Pytest)

```python
# tests/unit/test_math.py

# 📥 IMPORTS
import pytest
from utils.calculator import add

# 🔄 WORKFLOW
# 1. Define test cases (positive, negative, edge).
# 2. Call add() function.
# 3. Assert return value.

# 📤 EXPORTS
def test_add_positive_numbers():
    # Arrange
    a, b = 1, 2
    # Act
    result = add(a, b)
    # Assert
    assert result == 3

def test_add_invalid_input():
    # Arrange & Act & Assert
    with pytest.raises(TypeError):
        add("1", 2)
```

## 3. AI Action Items
*   **Coverage**: Aim for >80% code coverage.
*   **Isolation**: Unit tests must not depend on external systems (use Mocks).
*   **Determinism**: Tests must produce the same result every time.
