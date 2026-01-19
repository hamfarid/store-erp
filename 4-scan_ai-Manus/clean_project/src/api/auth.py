"""
API المصادقة - تسجيل الدخول والخروج وإدارة الجلسات
Authentication API - Login, logout and session management
"""

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel
from datetime import datetime, timedelta
import jwt
import hashlib
import logging

from src.core.config import get_settings

logger = logging.getLogger(__name__)
router = APIRouter()
security = HTTPBearer()
settings = get_settings()

class LoginRequest(BaseModel):
    username: str
    password: str

class LoginResponse(BaseModel):
    access_token: str
    token_type: str
    expires_in: int

class UserInfo(BaseModel):
    username: str
    email: str = None
    created_at: datetime

@router.post("/login", response_model=LoginResponse)
async def login(request: LoginRequest):
    """
    تسجيل الدخول
    User login
    """
    try:
        # التحقق من بيانات المستخدم (مؤقت - يجب استبداله بقاعدة البيانات)
        if request.username == "admin" and request.password == "admin123":
            # إنشاء JWT token
            payload = {
                "sub": request.username,
                "exp": datetime.utcnow() + timedelta(hours=settings.JWT_EXPIRATION_HOURS),
                "iat": datetime.utcnow(),
                "type": "access_token"
            }
            
            token = jwt.encode(payload, settings.JWT_SECRET, algorithm=settings.JWT_ALGORITHM)
            
            logger.info(f"تسجيل دخول ناجح للمستخدم: {request.username}")
            
            return LoginResponse(
                access_token=token,
                token_type="bearer",
                expires_in=settings.JWT_EXPIRATION_HOURS * 3600
            )
        else:
            logger.warning(f"محاولة تسجيل دخول فاشلة للمستخدم: {request.username}")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="اسم المستخدم أو كلمة المرور غير صحيحة"
            )
            
    except Exception as e:
        logger.error(f"خطأ في تسجيل الدخول: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="خطأ في تسجيل الدخول"
        )

@router.post("/logout")
async def logout(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """
    تسجيل الخروج
    User logout
    """
    try:
        # في التطبيق الحقيقي، يجب إضافة التوكن لقائمة سوداء
        logger.info("تسجيل خروج ناجح")
        return {"message": "تم تسجيل الخروج بنجاح"}
        
    except Exception as e:
        logger.error(f"خطأ في تسجيل الخروج: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="خطأ في تسجيل الخروج"
        )

@router.get("/me", response_model=UserInfo)
async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """
    الحصول على معلومات المستخدم الحالي
    Get current user information
    """
    try:
        token = credentials.credentials
        payload = jwt.decode(token, settings.JWT_SECRET, algorithms=[settings.JWT_ALGORITHM])
        username = payload.get("sub")
        
        if username is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="توكن غير صالح"
            )
        
        # إرجاع معلومات المستخدم (مؤقت)
        return UserInfo(
            username=username,
            email=f"{username}@gaara-scan.ai",
            created_at=datetime.now()
        )
        
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="انتهت صلاحية التوكن"
        )
    except jwt.InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="توكن غير صالح"
        )
    except Exception as e:
        logger.error(f"خطأ في الحصول على معلومات المستخدم: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="خطأ في الحصول على معلومات المستخدم"
        )

