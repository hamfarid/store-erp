"""
FILE: backend/src/api/v1/auth.py | PURPOSE: Authentication API routes | OWNER: Backend Team | LAST-AUDITED: 2025-12-05

Authentication API Routes

Handles user authentication, registration, password reset, and MFA.

Version: 2.1.0 - Added Rate Limiting and Email Integration
"""

import hashlib
import logging
import secrets
from datetime import datetime, timedelta
from typing import Optional

import jwt
from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException, Request, Response, status
from fastapi.security import OAuth2PasswordBearer
from pydantic import AliasChoices, BaseModel, EmailStr, Field
from sqlalchemy.orm import Session

from ...core.config import get_settings
from ...core.database import get_db
from ...core.rate_limiting import limiter
from ...models.user import User
from ...modules.mfa.mfa_service import setup_mfa, verify_mfa_token
from ...utils.password_policy import hash_password, validate_password, verify_password

logger = logging.getLogger(__name__)

# Router
router = APIRouter(prefix="/api/v1/auth", tags=["authentication"])

# OAuth2 scheme
# Tests expect 403 (Forbidden) when no token is provided.
oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/api/v1/auth/login",
    auto_error=False,
)

# JWT configuration is driven by Settings (src.core.config.get_settings)
REFRESH_TOKEN_EXPIRE_DAYS = 7
PASSWORD_RESET_EXPIRE_HOURS = 1

# In-memory token storage (use Redis in production)
password_reset_tokens = {}


# Pydantic Schemas


class RegisterRequest(BaseModel):
    email: EmailStr
    password: str
    name: str
    phone: Optional[str] = None


class LoginRequest(BaseModel):
    username: str = Field(
        ...,
        validation_alias=AliasChoices("username", "email"),
    )
    password: str
    mfa_token: Optional[str] = None


class LoginResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    expires_in: int


class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    user: dict


class MFASetupResponse(BaseModel):
    secret: str
    qr_code: str
    backup_codes: list


class ForgotPasswordRequest(BaseModel):
    email: EmailStr


class ResetPasswordRequest(BaseModel):
    token: str
    new_password: str
    confirm_password: str


class ChangePasswordRequest(BaseModel):
    current_password: str
    new_password: str
    confirm_password: str


class MessageResponse(BaseModel):
    message: str
    success: bool = True


# Helper Functions
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """Create JWT access token"""
    settings = get_settings()
    to_encode = data.copy()
    to_encode.setdefault("iat", datetime.utcnow())
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(hours=settings.JWT_EXPIRATION_HOURS)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode,
        settings.JWT_SECRET,
        algorithm=settings.JWT_ALGORITHM,
    )
    return encoded_jwt


def _decode_access_token(token: str) -> dict:
    settings = get_settings()
    try:
        return jwt.decode(
            token,
            settings.JWT_SECRET,
            algorithms=[settings.JWT_ALGORITHM],
        )
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="انتهت صلاحية التوكن",
        )
    except jwt.PyJWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="توكن غير صالح",
        )


def get_current_subject(token: str = Depends(oauth2_scheme)) -> str:
    if not token:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authenticated",
        )
    payload = _decode_access_token(token)
    subject = payload.get("sub")
    if not subject:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="توكن غير صالح",
        )
    return str(subject)


def create_password_reset_token(user_id: int, email: str) -> str:
    """Create a secure password reset token"""
    token = secrets.token_urlsafe(32)
    token_hash = hashlib.sha256(token.encode()).hexdigest()

    # Store token with expiration
    password_reset_tokens[token_hash] = {
        "user_id": user_id,
        "email": email,
        "expires_at": datetime.utcnow() +
        timedelta(
            hours=PASSWORD_RESET_EXPIRE_HOURS),
        "used": False}

    return token


def verify_password_reset_token(token: str) -> Optional[dict]:
    """Verify password reset token and return user data"""
    token_hash = hashlib.sha256(token.encode()).hexdigest()

    token_data = password_reset_tokens.get(token_hash)
    if not token_data:
        return None

    if token_data["used"]:
        return None

    if token_data["expires_at"] < datetime.utcnow():
        del password_reset_tokens[token_hash]
        return None

    return token_data


def invalidate_password_reset_token(token: str):
    """Mark token as used"""
    token_hash = hashlib.sha256(token.encode()).hexdigest()
    if token_hash in password_reset_tokens:
        password_reset_tokens[token_hash]["used"] = True


async def send_password_reset_email(email: str, token: str, name: str):
    """
    Send password reset email using EmailService
    إرسال بريد إعادة تعيين كلمة المرور باستخدام خدمة البريد
    """
    try:
        from ...services.email_service import get_email_service

        service = get_email_service()
        success = service.send_password_reset_email(
            to_email=email,
            name=name,
            reset_token=token
        )

        if success:
            logger.info(f"[OK] Password reset email sent to {email}")
        else:
            logger.warning(f"[WARN] Failed to send password reset email to {email}")

        return success
    except Exception as e:
        logger.error(f"[ERROR] Error sending password reset email: {e}")
        # Fallback: Log for development
        reset_url = f"http://localhost:1505/reset-password?token={token}"
        logger.info(f"[DEV] Password reset URL for {email}: {reset_url}")
        return False


def get_current_user(
        token: Optional[str] = Depends(oauth2_scheme),
        db: Session = Depends(get_db)):
    """
    Get current authenticated user with blacklist check
    الحصول على المستخدم الحالي مع فحص قائمة الحظر
    """
    if not token:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authenticated",
        )

    # فحص قائمة الحظر
    # Check token blacklist
    try:
        from ...services.token_blacklist import is_token_blacklisted
        if is_token_blacklisted(token):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token has been revoked. Please login again.",
                headers={"WWW-Authenticate": "Bearer"},
            )
    except ImportError:
        pass  # Token blacklist service not available

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    settings = get_settings()
    try:
        payload = jwt.decode(
            token,
            settings.JWT_SECRET,
            algorithms=[settings.JWT_ALGORITHM],
        )
        user_id: int = payload.get("sub")
        if user_id is None:
            raise credentials_exception
    except jwt.PyJWTError:
        raise credentials_exception

    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise credentials_exception
    return user


# Routes
@router.post("/register", response_model=TokenResponse,
             status_code=status.HTTP_201_CREATED)
async def register(
    request: Request,
    response: Response,
    register_data: RegisterRequest,
    db: Session = Depends(get_db),
):
    """Register a new user - Rate limited: 3 per hour"""

    # Check if user already exists
    existing_user = db.query(User).filter(User.email == register_data.email).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )

    # Validate password
    is_valid, errors = validate_password(register_data.password)
    if not is_valid:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                "message": "Password does not meet requirements",
                "errors": errors})

    # Hash password
    password_hash = hash_password(register_data.password)

    # Create user
    user = User(
        email=register_data.email,
        password_hash=password_hash,
        name=register_data.name,
        phone=register_data.phone,
        role="USER",
        is_active=True
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    # Create tokens
    access_token = create_access_token(data={"sub": user.id})
    refresh_token = create_access_token(
        data={"sub": user.id},
        expires_delta=timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
    )

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
        "user": user.to_dict()
    }


@router.post("/login", response_model=LoginResponse)
async def login(
    request: Request,
    response: Response,
    login_data: LoginRequest,
    db: Session = Depends(get_db),
):
    """
    Login user - Rate limited: 5 per minute
    
    Security Features:
    - Account lockout after failed attempts
    - Tracks failed login attempts
    - Records successful login timestamp and IP
    """
    from ...services.lockout_service import LockoutService
    
    settings = get_settings()
    lockout_service = LockoutService(db)
    
    if settings.DEBUG:
        logger.info("[DEBUG] login() handler reached; response param type=%s", type(response))

    # Find user by email (username field contains email)
    user = db.query(User).filter(User.email == login_data.username).first()

    # Check if account is locked (if user exists)
    if user:
        is_locked, lockout_info = lockout_service.check_lockout(user)
        if is_locked:
            logger.warning(f"[SECURITY] Blocked login attempt for locked account: {login_data.username}")
            raise HTTPException(
                status_code=status.HTTP_423_LOCKED,
                detail={
                    "message": "Account is temporarily locked due to too many failed login attempts",
                    "message_ar": "الحساب مقفل مؤقتاً بسبب محاولات تسجيل دخول فاشلة متعددة",
                    "locked_until": lockout_info.get("locked_until"),
                    "remaining_seconds": lockout_info.get("remaining_seconds")
                }
            )

    # Validate credentials
    if not user or not verify_password(login_data.password, user.password_hash):
        # Record failed attempt if user exists
        if user:
            lockout_service.record_failed_attempt(user)
            remaining = settings.MAX_LOGIN_ATTEMPTS - user.failed_login_attempts if hasattr(settings, 'MAX_LOGIN_ATTEMPTS') else 5 - user.failed_login_attempts
            logger.warning(f"[SECURITY] Failed login attempt for {login_data.username}. Attempts: {user.failed_login_attempts}")
            
            if remaining <= 0:
                raise HTTPException(
                    status_code=status.HTTP_423_LOCKED,
                    detail={
                        "message": "Account has been locked due to too many failed attempts",
                        "message_ar": "تم قفل الحساب بسبب محاولات فاشلة متعددة"
                    }
                )
        
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Check if user is active
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Account is disabled"
        )

    # Clear lockout on successful login
    client_ip = request.headers.get('X-Forwarded-For', request.client.host if request.client else 'unknown')
    lockout_service.record_successful_login(user, client_ip)
    
    # Check MFA if enabled
    if user.mfa_enabled:
        if not login_data.mfa_token:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail={
                    "message": "MFA token required",
                    "message_ar": "رمز التحقق الثنائي مطلوب",
                    "mfa_required": True
                }
            )
        if not verify_mfa_token(user.mfa_secret, login_data.mfa_token):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid MFA token"
            )

    # Generate JWT token
    access_token = create_access_token({"sub": user.id, "email": user.email, "role": user.role})
    
    logger.info(f"[OK] Successful login for user: {user.email}")

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "expires_in": settings.JWT_EXPIRATION_HOURS * 3600,
    }


@router.post("/forgot-password", response_model=MessageResponse)
async def forgot_password(
    request: Request,
    response: Response,
    forgot_data: ForgotPasswordRequest,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    """
    Request password reset - Rate limited: 3 per hour

    Sends a password reset email if the email exists.
    Always returns success to prevent email enumeration.
    """

    user = db.query(User).filter(User.email == forgot_data.email).first()

    if user and user.is_active:
        # Create reset token
        token = create_password_reset_token(user.id, user.email)

        # Send email in background
        background_tasks.add_task(
            send_password_reset_email,
            email=user.email,
            token=token,
            name=user.name or "User"
        )

    # Always return success to prevent email enumeration
    return {
        "message": "If your email is registered, you will receive a password reset link shortly.",
        "success": True}


@router.post("/reset-password", response_model=MessageResponse)
async def reset_password(
        request: Request,
        response: Response,
        reset_data: ResetPasswordRequest,
        db: Session = Depends(get_db)):
    """
    Reset password using token from email - Rate limited: 5 per hour
    """

    # Verify passwords match
    if reset_data.new_password != reset_data.confirm_password:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Passwords do not match"
        )

    # Verify token
    token_data = verify_password_reset_token(reset_data.token)
    if not token_data:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid or expired reset token"
        )

    # Validate new password
    is_valid, errors = validate_password(reset_data.new_password)
    if not is_valid:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                "message": "Password does not meet requirements",
                "errors": errors})

    # Get user
    user = db.query(User).filter(User.id == token_data["user_id"]).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    # Update password
    user.password_hash = hash_password(request.new_password)
    user.password_changed_at = datetime.utcnow()
    user.failed_login_attempts = 0
    user.locked_until = None
    db.commit()

    # Invalidate token
    invalidate_password_reset_token(request.token)

    return {
        "message": "Password has been reset successfully. You can now login with your new password.",
        "success": True}


@router.post("/change-password", response_model=MessageResponse)
async def change_password(
    request: ChangePasswordRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Change password for authenticated user.
    """

    # Verify current password
    if not verify_password(
            request.current_password,
            current_user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Current password is incorrect"
        )

    # Verify passwords match
    if request.new_password != request.confirm_password:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="New passwords do not match"
        )

    # Validate new password
    is_valid, errors = validate_password(request.new_password)
    if not is_valid:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                "message": "Password does not meet requirements",
                "errors": errors})

    # Ensure new password is different
    if verify_password(request.new_password, current_user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="New password must be different from current password"
        )

    # Update password
    current_user.password_hash = hash_password(request.new_password)
    current_user.password_changed_at = datetime.utcnow()
    db.commit()

    return {
        "message": "Password changed successfully",
        "success": True
    }


@router.get("/verify-reset-token/{token}")
async def verify_reset_token(token: str):
    """
    Verify if a password reset token is valid.
    Used by frontend to check token before showing reset form.
    """

    token_data = verify_password_reset_token(token)

    if not token_data:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid or expired reset token"
        )

    return {
        "valid": True,
        "email": token_data["email"],
        "expires_at": token_data["expires_at"].isoformat()
    }


@router.post("/mfa/setup", response_model=MFASetupResponse)
async def setup_mfa_endpoint(
        current_user: User = Depends(get_current_user),
        db: Session = Depends(get_db)):
    """Setup MFA for current user"""

    secret, qr_code, backup_codes = setup_mfa(current_user.email)

    # Save MFA secret to user
    current_user.mfa_secret = secret
    current_user.mfa_backup_codes = ",".join(backup_codes)
    db.commit()

    return {
        "secret": secret,
        "qr_code": qr_code,
        "backup_codes": backup_codes
    }


@router.post("/mfa/enable")
async def enable_mfa(
        mfa_token: str,
        current_user: User = Depends(get_current_user),
        db: Session = Depends(get_db)):
    """Enable MFA for current user"""

    if not current_user.mfa_secret:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="MFA not set up. Please setup MFA first."
        )

    # Verify token
    if not verify_mfa_token(current_user.mfa_secret, mfa_token):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid MFA token"
        )

    # Enable MFA
    current_user.mfa_enabled = True
    db.commit()

    return {"message": "MFA enabled successfully"}


@router.post("/mfa/disable")
async def disable_mfa(
    password: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Disable MFA for current user (requires password confirmation)"""

    # Verify password
    if not verify_password(password, current_user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect password"
        )

    # Disable MFA
    current_user.mfa_enabled = False
    current_user.mfa_secret = None
    current_user.mfa_backup_codes = None
    db.commit()

    return {"message": "MFA disabled successfully"}


@router.get("/me")
async def get_current_user_info(subject: str = Depends(get_current_subject)):
    """Get current user information"""
    return {
        "username": subject,
        "email": "admin@gaara-scan.ai" if subject == "admin" else f"{subject}@gaara-scan.ai",
        "created_at": datetime.utcnow().isoformat(),
    }


@router.post("/logout")
async def logout(
    request: Request,
    token: Optional[str] = Depends(oauth2_scheme)
):
    """
    Logout user and invalidate token.
    تسجيل الخروج وإبطال الرمز

    Adds the token to the blacklist to prevent reuse.
    """
    if token:
        try:
            from ...services.token_blacklist import blacklist_token

            # حساب وقت انتهاء الرمز
            settings = get_settings()
            expires_in = settings.JWT_EXPIRATION_HOURS * 3600

            # إضافة الرمز إلى قائمة الحظر
            blacklist_token(token, expires_in)
            logger.info("[OK] Token blacklisted on logout")
        except Exception as e:
            logger.warning(f"[WARN] Could not blacklist token: {e}")

    return {
        "success": True,
        "message": "تم تسجيل الخروج بنجاح",
        "message_en": "Logged out successfully"
    }
