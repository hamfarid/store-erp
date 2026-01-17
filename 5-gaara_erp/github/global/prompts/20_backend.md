# BACKEND DEVELOPMENT PROMPT

**FILE**: github/global/prompts/20_backend.md | **PURPOSE**: Backend development guidelines | **OWNER**: System | **LAST-AUDITED**: 2025-11-18

## Phase 4: Code Implementation - Backend

This prompt guides you through building production-ready backend code.

## Pre-Execution Checklist

- [ ] Planning phase complete
- [ ] Task list exists in `docs/Task_List.md`
- [ ] Database schema designed
- [ ] Tech stack selected

## Core Principles

1. **OSF Framework**: Security (35%) > Correctness (20%) > Reliability (15%)
2. **Zero-Tolerance Constraints**: No hardcoded secrets, no SQL injection, no unhandled errors
3. **Test Coverage**: Minimum 80%
4. **Documentation**: Every function must have a docstring

## Step 1: Project Structure

Create the following structure:

```
backend/
├── models/          # Database models
├── services/        # Business logic
├── routes/          # API endpoints
├── middleware/      # Request/response middleware
├── utils/           # Helper functions
├── config/          # Configuration
├── tests/           # Test files
│   ├── unit/
│   ├── integration/
│   └── fixtures/
└── main.py          # Entry point
```

## Step 2: Configuration

### config/settings.py

```python
# FILE: backend/config/settings.py | PURPOSE: Application settings | OWNER: Backend | LAST-AUDITED: 2025-11-18

import os
from pydantic import BaseSettings

class Settings(BaseSettings):
    """Application settings loaded from environment variables"""
    
    # Application
    APP_NAME: str = "MyApp"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = False
    
    # Database
    DATABASE_URL: str
    DB_POOL_SIZE: int = 10
    DB_MAX_OVERFLOW: int = 20
    
    # Security
    SECRET_KEY: str
    JWT_ALGORITHM: str = "HS256"
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES: int = 15
    JWT_REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    
    # CORS
    CORS_ORIGINS: list[str] = ["http://localhost:3000"]
    
    # Rate Limiting
    RATE_LIMIT_PER_MINUTE: int = 100
    
    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings()
```

## Step 3: Database Models

### models/base.py

```python
# FILE: backend/models/base.py | PURPOSE: Base model class | OWNER: Backend | LAST-AUDITED: 2025-11-18

from datetime import datetime
from sqlalchemy import Column, DateTime
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class TimestampMixin:
    """Mixin for created_at and updated_at timestamps"""
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
```

### models/user.py

```python
# FILE: backend/models/user.py | PURPOSE: User model | OWNER: Backend | LAST-AUDITED: 2025-11-18

from sqlalchemy import Column, String, Enum, Boolean
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import uuid
import bcrypt
from .base import Base, TimestampMixin

class UserRole(str, Enum):
    ADMIN = "admin"
    MANAGER = "manager"
    USER = "user"
    GUEST = "guest"

class User(Base, TimestampMixin):
    """User model for authentication and authorization"""
    
    __tablename__ = "users"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(String(255), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)
    role = Column(Enum(UserRole), default=UserRole.USER, nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    deleted_at = Column(DateTime, nullable=True)  # Soft delete
    
    # Relationships
    sessions = relationship("Session", back_populates="user")
    activity_logs = relationship("ActivityLog", back_populates="user")
    
    def set_password(self, password: str) -> None:
        """Hash and set the user's password"""
        salt = bcrypt.gensalt()
        self.password_hash = bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')
    
    def verify_password(self, password: str) -> bool:
        """Verify the user's password"""
        return bcrypt.checkpw(password.encode('utf-8'), self.password_hash.encode('utf-8'))
    
    def __repr__(self):
        return f"<User {self.email}>"
```

## Step 4: Services (Business Logic)

### services/auth_service.py

```python
# FILE: backend/services/auth_service.py | PURPOSE: Authentication service | OWNER: Backend | LAST-AUDITED: 2025-11-18

from datetime import datetime, timedelta
from typing import Optional
import jwt
from sqlalchemy.orm import Session
from models.user import User
from models.session import Session as UserSession
from config.settings import settings
import uuid

class AuthService:
    """Authentication service for login, logout, and token management"""
    
    def __init__(self, db: Session):
        self.db = db
    
    def login(self, email: str, password: str) -> dict:
        """
        Authenticate user and return access and refresh tokens
        
        Args:
            email: User's email
            password: User's password
        
        Returns:
            dict with access_token, refresh_token, and user info
        
        Raises:
            ValueError: If credentials are invalid
        """
        # Find user
        user = self.db.query(User).filter(User.email == email, User.is_active == True).first()
        
        if not user or not user.verify_password(password):
            raise ValueError("Invalid credentials")
        
        # Generate tokens
        access_token = self._generate_access_token(user)
        refresh_token = self._generate_refresh_token(user)
        
        # Create session
        session = UserSession(
            id=uuid.uuid4(),
            user_id=user.id,
            refresh_token=refresh_token,
            expires_at=datetime.utcnow() + timedelta(days=settings.JWT_REFRESH_TOKEN_EXPIRE_DAYS)
        )
        self.db.add(session)
        self.db.commit()
        
        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "bearer",
            "user": {
                "id": str(user.id),
                "email": user.email,
                "role": user.role.value
            }
        }
    
    def _generate_access_token(self, user: User) -> str:
        """Generate JWT access token"""
        payload = {
            "sub": str(user.id),
            "email": user.email,
            "role": user.role.value,
            "exp": datetime.utcnow() + timedelta(minutes=settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES)
        }
        return jwt.encode(payload, settings.SECRET_KEY, algorithm=settings.JWT_ALGORITHM)
    
    def _generate_refresh_token(self, user: User) -> str:
        """Generate JWT refresh token"""
        payload = {
            "sub": str(user.id),
            "type": "refresh",
            "exp": datetime.utcnow() + timedelta(days=settings.JWT_REFRESH_TOKEN_EXPIRE_DAYS)
        }
        return jwt.encode(payload, settings.SECRET_KEY, algorithm=settings.JWT_ALGORITHM)
```

## Step 5: API Routes

### routes/auth.py

```python
# FILE: backend/routes/auth.py | PURPOSE: Authentication routes | OWNER: Backend | LAST-AUDITED: 2025-11-18

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from pydantic import BaseModel, EmailStr
from services.auth_service import AuthService
from database import get_db

router = APIRouter(prefix="/api/auth", tags=["authentication"])

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

@router.post("/login")
def login(request: LoginRequest, db: Session = Depends(get_db)):
    """
    User login endpoint
    
    Returns access and refresh tokens
    """
    try:
        auth_service = AuthService(db)
        result = auth_service.login(request.email, request.password)
        return result
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e)
        )
    except Exception as e:
        # Log the error
        print(f"Login error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred during login"
        )
```

## Step 6: Middleware

### middleware/auth.py

```python
# FILE: backend/middleware/auth.py | PURPOSE: Authentication middleware | OWNER: Backend | LAST-AUDITED: 2025-11-18

from fastapi import Request, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import jwt
from config.settings import settings

security = HTTPBearer()

async def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """Verify JWT token and return user info"""
    try:
        token = credentials.credentials
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has expired"
        )
    except jwt.InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token"
        )
```

## Step 7: Write Tests

For every service and route, write comprehensive tests.

See `41_testing.md` for detailed testing guidelines.

## Step 8: Log Actions

Log all implementation to `logs/info.log`

---

**Completion Criteria**:
- [ ] All models created
- [ ] All services implemented
- [ ] All routes implemented
- [ ] All middleware implemented
- [ ] All tests written (≥80% coverage)
- [ ] All functions documented
- [ ] No hardcoded secrets
- [ ] All errors handled
- [ ] Actions logged

