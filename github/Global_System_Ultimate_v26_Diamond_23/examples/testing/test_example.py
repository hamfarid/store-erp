"""
### 📊 Logical Chart (Create -> Verify -> Execute)
```mermaid
flowchart TD
    Start([Start]) --> Order[1. Order Requirements]
    Order --> Create[2. Create Artifacts]
    Create --> Verify{3. Verify Success?}
    Verify -- No --> Rollback[Rollback/Fix]
    Rollback --> Create
    Verify -- Yes --> Execute[4. Execute/Deploy]
    Execute --> End([End])
```

### 🔄 Workflow
1.  **Order**: Define prerequisites and inputs.
2.  **Create**: Generate the output (file, data, resource).
3.  **Verify**: Check if the output meets standards (Syntax, Logic, Compliance).
4.  **Execute**: Apply the change or return the result.

### 📥 Imports
os, pytest, unittest.mock

### 📤 Exports
class Service, def mock_repository(), def service(), def test_get_user_success(), def test_get_user_not_found(), def get_user()

### 💡 Example
```python
# Example usage for test_example.py
# from test_example import class Service
```
"""

import os
"""
Standard Unit Test Template (Global System Ultimate)
Engine: Speckit Global System Ultimate
"""

import pytest
from unittest.mock import MagicMock

# Assume we are testing a Service class
class Service:
    def __init__(self, repository):
        self.repository = repository

    def get_user(self, user_id):
        user = self.repository.find_by_id(user_id)
        if not user:
            raise ValueError("User not found")
        return user

# Fixtures
@pytest.fixture
def mock_repository():
    return MagicMock()

@pytest.fixture
def service(mock_repository):
    return Service(mock_repository)

# Tests
def test_get_user_success(service, mock_repository):
    # Arrange
    user_id = 1
    expected_user = {"id": 1, "name": "Test User"}
    mock_repository.find_by_id.return_value = expected_user

    # Act
    result = service.get_user(user_id)

    # Assert
    assert result == expected_user
    mock_repository.find_by_id.assert_called_once_with(user_id)

def test_get_user_not_found(service, mock_repository):
    # Arrange
    user_id = 999
    mock_repository.find_by_id.return_value = None

    # Act & Assert
    with pytest.raises(ValueError, match="User not found"):
        service.get_user(user_id)