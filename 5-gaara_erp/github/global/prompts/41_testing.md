# TESTING PROMPT

**FILE**: github/global/prompts/41_testing.md | **PURPOSE**: Comprehensive testing guidelines | **OWNER**: System | **LAST-AUDITED**: 2025-11-18

## Phase 6: Testing

This prompt guides you through writing comprehensive tests for backend and frontend code.

## Pre-Execution Checklist

- [ ] Code implementation complete
- [ ] Testing frameworks installed
- [ ] Test database configured

## Testing Pyramid

- **Unit Tests**: 70% (fast, isolated)
- **Integration Tests**: 20% (DB, APIs)
- **E2E Tests**: 10% (critical paths)

## Target Coverage

- **Overall**: ≥80%
- **Critical Paths**: 100%
- **Services/Business Logic**: ≥90%
- **Models**: ≥90%
- **Routes/Controllers**: ≥80%
- **Utils**: ≥80%

## Backend Testing (Python/FastAPI)

### Setup

```bash
pip install pytest pytest-cov pytest-asyncio httpx
```

### Test Structure

```
backend/tests/
├── unit/
│   ├── test_models.py
│   ├── test_services.py
│   └── test_utils.py
├── integration/
│   ├── test_api.py
│   └── test_database.py
├── fixtures/
│   └── conftest.py
└── pytest.ini
```

### Unit Tests - Models

```python
# FILE: backend/tests/unit/test_models.py | PURPOSE: Model unit tests | OWNER: QA | LAST-AUDITED: 2025-11-18

import pytest
from models.user import User, UserRole

class TestUserModel:
    """Test User model"""
    
    def test_create_user(self):
        """Test user creation"""
        user = User(
            email="test@example.com",
            role=UserRole.USER
        )
        user.set_password("SecurePassword123!")
        
        assert user.email == "test@example.com"
        assert user.role == UserRole.USER
        assert user.password_hash is not None
        assert user.password_hash != "SecurePassword123!"
    
    def test_verify_password_correct(self):
        """Test password verification with correct password"""
        user = User(email="test@example.com")
        user.set_password("SecurePassword123!")
        
        assert user.verify_password("SecurePassword123!") is True
    
    def test_verify_password_incorrect(self):
        """Test password verification with incorrect password"""
        user = User(email="test@example.com")
        user.set_password("SecurePassword123!")
        
        assert user.verify_password("WrongPassword") is False
    
    def test_user_repr(self):
        """Test user string representation"""
        user = User(email="test@example.com")
        assert repr(user) == "<User test@example.com>"
```

### Unit Tests - Services

```python
# FILE: backend/tests/unit/test_services.py | PURPOSE: Service unit tests | OWNER: QA | LAST-AUDITED: 2025-11-18

import pytest
from unittest.mock import Mock, patch
from services.auth_service import AuthService
from models.user import User, UserRole

class TestAuthService:
    """Test AuthService"""
    
    @pytest.fixture
    def mock_db(self):
        """Mock database session"""
        return Mock()
    
    @pytest.fixture
    def auth_service(self, mock_db):
        """Create AuthService instance"""
        return AuthService(mock_db)
    
    def test_login_success(self, auth_service, mock_db):
        """Test successful login"""
        # Arrange
        user = User(email="test@example.com", role=UserRole.USER)
        user.set_password("SecurePassword123!")
        
        mock_db.query.return_value.filter.return_value.first.return_value = user
        
        # Act
        result = auth_service.login("test@example.com", "SecurePassword123!")
        
        # Assert
        assert "access_token" in result
        assert "refresh_token" in result
        assert result["user"]["email"] == "test@example.com"
    
    def test_login_invalid_credentials(self, auth_service, mock_db):
        """Test login with invalid credentials"""
        # Arrange
        mock_db.query.return_value.filter.return_value.first.return_value = None
        
        # Act & Assert
        with pytest.raises(ValueError, match="Invalid credentials"):
            auth_service.login("test@example.com", "WrongPassword")
```

### Integration Tests - API

```python
# FILE: backend/tests/integration/test_api.py | PURPOSE: API integration tests | OWNER: QA | LAST-AUDITED: 2025-11-18

import pytest
from fastapi.testclient import TestClient
from main import app
from database import get_db, Base, engine

@pytest.fixture(scope="module")
def test_client():
    """Create test client"""
    # Create test database
    Base.metadata.create_all(bind=engine)
    
    client = TestClient(app)
    yield client
    
    # Cleanup
    Base.metadata.drop_all(bind=engine)

class TestAuthAPI:
    """Test authentication API endpoints"""
    
    def test_login_success(self, test_client):
        """Test POST /api/auth/login with valid credentials"""
        # Create test user first
        # (Assume user creation endpoint exists or use direct DB insert)
        
        response = test_client.post(
            "/api/auth/login",
            json={"email": "test@example.com", "password": "SecurePassword123!"}
        )
        
        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        assert "refresh_token" in data
        assert data["user"]["email"] == "test@example.com"
    
    def test_login_invalid_credentials(self, test_client):
        """Test POST /api/auth/login with invalid credentials"""
        response = test_client.post(
            "/api/auth/login",
            json={"email": "test@example.com", "password": "WrongPassword"}
        )
        
        assert response.status_code == 401
        assert "Invalid credentials" in response.json()["detail"]
    
    def test_protected_route_without_token(self, test_client):
        """Test accessing protected route without token"""
        response = test_client.get("/api/users")
        
        assert response.status_code == 401
    
    def test_protected_route_with_token(self, test_client):
        """Test accessing protected route with valid token"""
        # Login first
        login_response = test_client.post(
            "/api/auth/login",
            json={"email": "test@example.com", "password": "SecurePassword123!"}
        )
        token = login_response.json()["access_token"]
        
        # Access protected route
        response = test_client.get(
            "/api/users",
            headers={"Authorization": f"Bearer {token}"}
        )
        
        assert response.status_code == 200
```

## Frontend Testing (React/TypeScript)

### Setup

```bash
npm install --save-dev @testing-library/react @testing-library/jest-dom @testing-library/user-event vitest jsdom
```

### Test Structure

```
frontend/tests/
├── unit/
│   ├── components/
│   └── hooks/
├── integration/
│   └── pages/
└── setup.ts
```

### Unit Tests - Components

```typescript
// FILE: frontend/tests/unit/components/Button.test.tsx | PURPOSE: Button component tests | OWNER: QA | LAST-AUDITED: 2025-11-18

import { describe, it, expect, vi } from 'vitest';
import { render, screen, fireEvent } from '@testing-library/react';
import { Button } from '../../../src/components/Button';

describe('Button', () => {
  it('renders with children', () => {
    render(<Button>Click me</Button>);
    expect(screen.getByText('Click me')).toBeInTheDocument();
  });

  it('calls onClick when clicked', () => {
    const handleClick = vi.fn();
    render(<Button onClick={handleClick}>Click me</Button>);
    
    fireEvent.click(screen.getByText('Click me'));
    expect(handleClick).toHaveBeenCalledTimes(1);
  });

  it('does not call onClick when disabled', () => {
    const handleClick = vi.fn();
    render(<Button onClick={handleClick} disabled>Click me</Button>);
    
    fireEvent.click(screen.getByText('Click me'));
    expect(handleClick).not.toHaveBeenCalled();
  });

  it('shows loading state', () => {
    render(<Button loading>Click me</Button>);
    expect(screen.getByText('Loading...')).toBeInTheDocument();
  });

  it('applies correct variant styles', () => {
    const { rerender } = render(<Button variant="primary">Primary</Button>);
    let button = screen.getByText('Primary');
    expect(button).toHaveStyle({ backgroundColor: '#0F6CBD' });

    rerender(<Button variant="secondary">Secondary</Button>);
    button = screen.getByText('Secondary');
    expect(button).toHaveStyle({ backgroundColor: '#F1F5F9' });
  });
});
```

### Integration Tests - Pages

```typescript
// FILE: frontend/tests/integration/pages/LoginPage.test.tsx | PURPOSE: Login page tests | OWNER: QA | LAST-AUDITED: 2025-11-18

import { describe, it, expect, vi, beforeEach } from 'vitest';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import { BrowserRouter } from 'react-router-dom';
import { LoginPage } from '../../../src/pages/LoginPage';
import { api } from '../../../src/services/api';

vi.mock('../../../src/services/api');

describe('LoginPage', () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  it('renders login form', () => {
    render(
      <BrowserRouter>
        <LoginPage />
      </BrowserRouter>
    );

    expect(screen.getByLabelText('Email')).toBeInTheDocument();
    expect(screen.getByLabelText('Password')).toBeInTheDocument();
    expect(screen.getByRole('button', { name: 'Login' })).toBeInTheDocument();
  });

  it('submits form with valid credentials', async () => {
    const mockLogin = vi.fn().mockResolvedValue({
      id: '1',
      email: 'test@example.com',
      role: 'user',
    });
    (api.login as any) = mockLogin;

    render(
      <BrowserRouter>
        <LoginPage />
      </BrowserRouter>
    );

    fireEvent.change(screen.getByLabelText('Email'), {
      target: { value: 'test@example.com' },
    });
    fireEvent.change(screen.getByLabelText('Password'), {
      target: { value: 'SecurePassword123!' },
    });
    fireEvent.click(screen.getByRole('button', { name: 'Login' }));

    await waitFor(() => {
      expect(mockLogin).toHaveBeenCalledWith('test@example.com', 'SecurePassword123!');
    });
  });

  it('shows error message on failed login', async () => {
    const mockLogin = vi.fn().mockRejectedValue(new Error('Invalid credentials'));
    (api.login as any) = mockLogin;

    render(
      <BrowserRouter>
        <LoginPage />
      </BrowserRouter>
    );

    fireEvent.change(screen.getByLabelText('Email'), {
      target: { value: 'test@example.com' },
    });
    fireEvent.change(screen.getByLabelText('Password'), {
      target: { value: 'WrongPassword' },
    });
    fireEvent.click(screen.getByRole('button', { name: 'Login' }));

    await waitFor(() => {
      expect(screen.getByText('Invalid credentials')).toBeInTheDocument();
    });
  });
});
```

## Running Tests

### Backend

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=backend --cov-report=html --cov-report=term

# Run specific test file
pytest backend/tests/unit/test_models.py

# Run specific test
pytest backend/tests/unit/test_models.py::TestUserModel::test_create_user
```

### Frontend

```bash
# Run all tests
npm test

# Run with coverage
npm test -- --coverage

# Run specific test file
npm test Button.test.tsx

# Run in watch mode
npm test -- --watch
```

## Coverage Report

Generate coverage reports:

```bash
# Backend
pytest --cov=backend --cov-report=html
# Open htmlcov/index.html

# Frontend
npm test -- --coverage
# Open coverage/index.html
```

## Log Actions

Log all test results to `logs/info.log`

---

**Completion Criteria**:
- [ ] All unit tests written
- [ ] All integration tests written
- [ ] Coverage ≥80%
- [ ] All tests passing
- [ ] Coverage report generated
- [ ] Actions logged

