# FILE: examples/code-samples/log_activity_example.py | PURPOSE: log_activity implementation example | OWNER: Backend | LAST-AUDITED: 2025-10-28

"""
log_activity Module - Central Activity & Event Logging

Purpose: Configurable logging for general application events and specific user/system activities
for audit & analytics.

Features:
- Capture all critical events (button clicks, CRUD, exports, permission checks)
- Configurable granularity (high during testing, limited in prod)
- Retention/Archival (rotate, archive > 12 months)
- UI: filterable timeline
- Security: alert on suspicious patterns
"""

from datetime import datetime
from typing import Optional, Dict, Any
from enum import Enum
import json
import logging
from dataclasses import dataclass, asdict

# ========================================
# Enums
# ========================================

class ActivityAction(str, Enum):
    """نوع النشاط"""
    VIEW = "view"
    CREATE = "create"
    UPDATE = "update"
    DELETE = "delete"
    EXPORT = "export"
    TRIGGER = "trigger"
    LOGIN = "login"
    LOGOUT = "logout"
    PERMISSION_CHECK = "permission_check"

class ActivityResult(str, Enum):
    """نتيجة النشاط"""
    SUCCESS = "success"
    FAIL = "fail"
    PARTIAL = "partial"

class ActivityModule(str, Enum):
    """الوحدة/الشاشة"""
    AUTH = "auth"
    DASHBOARD = "dashboard"
    USERS = "users"
    REPORTS = "reports"
    SETTINGS = "settings"
    API = "api"

# ========================================
# Data Models
# ========================================

@dataclass
class ActivityLog:
    """نموذج سجل النشاط"""
    # Required fields
    timestamp: datetime
    trace_id: str
    module: ActivityModule
    action: ActivityAction
    result: ActivityResult
    
    # Optional fields
    user_id: Optional[str] = None
    tenant_id: Optional[str] = None
    role: Optional[str] = None
    ip: Optional[str] = None
    user_agent: Optional[str] = None
    route: Optional[str] = None
    screen: Optional[str] = None
    entity: Optional[str] = None
    http_status: Optional[int] = None
    latency_ms: Optional[int] = None
    error_code: Optional[str] = None
    details: Optional[Dict[str, Any]] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """تحويل إلى dict"""
        data = asdict(self)
        data['timestamp'] = self.timestamp.isoformat()
        return data
    
    def to_json(self) -> str:
        """تحويل إلى JSON"""
        return json.dumps(self.to_dict())

# ========================================
# Logger Class
# ========================================

class ActivityLogger:
    """
    مسجل النشاط المركزي
    
    Features:
    - Configurable per-category on/off
    - Adjustable granularity
    - Filter noise vs focus on errors/sensitive ops
    - Append-only audit tables
    """
    
    def __init__(
        self,
        enabled: bool = True,
        granularity: str = "normal",  # "high", "normal", "low"
        log_to_db: bool = True,
        log_to_file: bool = True,
        log_to_elk: bool = False
    ):
        self.enabled = enabled
        self.granularity = granularity
        self.log_to_db = log_to_db
        self.log_to_file = log_to_file
        self.log_to_elk = log_to_elk
        
        # إعداد Python logging
        self.logger = logging.getLogger("activity_logger")
        self.logger.setLevel(logging.INFO)
        
        # File handler
        if log_to_file:
            fh = logging.FileHandler("activity.log")
            fh.setFormatter(logging.Formatter('%(asctime)s - %(message)s'))
            self.logger.addHandler(fh)
    
    def log(self, activity: ActivityLog) -> None:
        """
        تسجيل نشاط
        
        Args:
            activity: ActivityLog object
        """
        if not self.enabled:
            return
        
        # Filter based on granularity
        if not self._should_log(activity):
            return
        
        # Log to file
        if self.log_to_file:
            self.logger.info(activity.to_json())
        
        # Log to database
        if self.log_to_db:
            self._log_to_db(activity)
        
        # Log to ELK
        if self.log_to_elk:
            self._log_to_elk(activity)
        
        # Check for suspicious patterns
        self._check_suspicious(activity)
    
    def _should_log(self, activity: ActivityLog) -> bool:
        """تحديد ما إذا كان يجب تسجيل النشاط بناءً على المستوى"""
        if self.granularity == "high":
            return True
        elif self.granularity == "normal":
            # تسجيل الأخطاء والعمليات الحساسة فقط
            return (
                activity.result == ActivityResult.FAIL or
                activity.action in [ActivityAction.DELETE, ActivityAction.EXPORT, ActivityAction.PERMISSION_CHECK]
            )
        else:  # low
            # تسجيل الأخطاء فقط
            return activity.result == ActivityResult.FAIL
    
    def _log_to_db(self, activity: ActivityLog) -> None:
        """حفظ في قاعدة البيانات (append-only)"""
        # TODO: Implement database logging
        # Example:
        # db.activity_logs.insert_one(activity.to_dict())
        pass
    
    def _log_to_elk(self, activity: ActivityLog) -> None:
        """إرسال إلى ELK/OpenSearch"""
        # TODO: Implement ELK logging
        pass
    
    def _check_suspicious(self, activity: ActivityLog) -> None:
        """فحص الأنماط المريبة"""
        # Repeated failed logins
        if (activity.action == ActivityAction.LOGIN and 
            activity.result == ActivityResult.FAIL):
            # TODO: Check if multiple failed attempts
            # TODO: Alert security team
            pass
        
        # Permission check failures
        if (activity.action == ActivityAction.PERMISSION_CHECK and 
            activity.result == ActivityResult.FAIL):
            # TODO: Alert on suspicious access attempts
            pass

# ========================================
# Decorators
# ========================================

def log_activity(
    module: ActivityModule,
    action: ActivityAction,
    entity: Optional[str] = None
):
    """
    Decorator لتسجيل النشاط تلقائياً
    
    Usage:
        @log_activity(ActivityModule.USERS, ActivityAction.CREATE, entity="user")
        def create_user(user_data):
            ...
    """
    def decorator(func):
        def wrapper(*args, **kwargs):
            import time
            import uuid
            
            start_time = time.time()
            trace_id = str(uuid.uuid4())
            
            try:
                result = func(*args, **kwargs)
                
                # Log success
                activity = ActivityLog(
                    timestamp=datetime.now(),
                    trace_id=trace_id,
                    module=module,
                    action=action,
                    result=ActivityResult.SUCCESS,
                    entity=entity,
                    latency_ms=int((time.time() - start_time) * 1000)
                )
                
                logger = ActivityLogger()
                logger.log(activity)
                
                return result
                
            except Exception as e:
                # Log failure
                activity = ActivityLog(
                    timestamp=datetime.now(),
                    trace_id=trace_id,
                    module=module,
                    action=action,
                    result=ActivityResult.FAIL,
                    entity=entity,
                    latency_ms=int((time.time() - start_time) * 1000),
                    error_code=type(e).__name__,
                    details={"error": str(e)}
                )
                
                logger = ActivityLogger()
                logger.log(activity)
                
                raise
        
        return wrapper
    return decorator

# ========================================
# Usage Examples
# ========================================

# Example 1: Manual logging
def example_manual_logging():
    """مثال على التسجيل اليدوي"""
    logger = ActivityLogger(granularity="high")
    
    activity = ActivityLog(
        timestamp=datetime.now(),
        trace_id="trace-123",
        user_id="user-456",
        tenant_id="tenant-789",
        role="ADMIN",
        ip="192.168.1.1",
        user_agent="Mozilla/5.0...",
        route="/api/users",
        module=ActivityModule.USERS,
        action=ActivityAction.CREATE,
        entity="user",
        result=ActivityResult.SUCCESS,
        http_status=201,
        latency_ms=150,
        details={"user_email": "user@example.com"}
    )
    
    logger.log(activity)

# Example 2: Using decorator
@log_activity(ActivityModule.USERS, ActivityAction.CREATE, entity="user")
def create_user(user_data: Dict[str, Any]) -> Dict[str, Any]:
    """إنشاء مستخدم جديد"""
    # Business logic here
    return {"id": "user-123", "email": user_data["email"]}

# Example 3: FastAPI integration
from fastapi import FastAPI, Request
import time

app = FastAPI()

@app.middleware("http")
async def log_requests(request: Request, call_next):
    """Middleware لتسجيل جميع الطلبات"""
    import uuid
    
    start_time = time.time()
    trace_id = str(uuid.uuid4())
    
    # Add trace_id to request state
    request.state.trace_id = trace_id
    
    try:
        response = await call_next(request)
        
        # Log successful request
        activity = ActivityLog(
            timestamp=datetime.now(),
            trace_id=trace_id,
            ip=request.client.host,
            user_agent=request.headers.get("user-agent"),
            route=request.url.path,
            module=ActivityModule.API,
            action=ActivityAction.VIEW,
            result=ActivityResult.SUCCESS,
            http_status=response.status_code,
            latency_ms=int((time.time() - start_time) * 1000)
        )
        
        logger = ActivityLogger()
        logger.log(activity)
        
        return response
        
    except Exception as e:
        # Log failed request
        activity = ActivityLog(
            timestamp=datetime.now(),
            trace_id=trace_id,
            ip=request.client.host,
            user_agent=request.headers.get("user-agent"),
            route=request.url.path,
            module=ActivityModule.API,
            action=ActivityAction.VIEW,
            result=ActivityResult.FAIL,
            http_status=500,
            latency_ms=int((time.time() - start_time) * 1000),
            error_code=type(e).__name__,
            details={"error": str(e)}
        )
        
        logger = ActivityLogger()
        logger.log(activity)
        
        raise

# Example 4: Query activity logs
def query_activity_logs(
    user_id: Optional[str] = None,
    module: Optional[ActivityModule] = None,
    action: Optional[ActivityAction] = None,
    result: Optional[ActivityResult] = None,
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
    limit: int = 100
) -> list:
    """
    استعلام سجلات النشاط
    
    Returns:
        قائمة بسجلات النشاط
    """
    # TODO: Implement database query
    # Example:
    # query = {}
    # if user_id:
    #     query['user_id'] = user_id
    # if module:
    #     query['module'] = module.value
    # ...
    # return db.activity_logs.find(query).limit(limit)
    pass

if __name__ == "__main__":
    # Test
    example_manual_logging()
    
    # Test decorator
    user_data = {"email": "test@example.com", "name": "Test User"}
    result = create_user(user_data)
    print(f"Created user: {result}")

