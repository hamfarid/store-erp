# type: ignore
# flake8: noqa
# pyright: ignore
# pylint: disable=all
# mypy: ignore-errors
"""
User models and authentication
All linting disabled due to SQLAlchemy and optional dependencies.
"""

from datetime import datetime, timezone, timedelta

try:
    import bcrypt

    BCRYPT_AVAILABLE = True
except ImportError:
    BCRYPT_AVAILABLE = False
    print("⚠️ bcrypt not available, using simple password hashing")

# Import shared db instance instead of creating a new one
try:
    from src.database import db
except ImportError:
    try:
        from database import db
    except ImportError:
        # Fallback for isolated execution
        from flask_sqlalchemy import SQLAlchemy

        db = SQLAlchemy()


class Role(db.Model):
    """نموذج الأدوار والصلاحيات"""

    __tablename__ = "roles"
    __table_args__ = {"extend_existing": True}

    id = db.Column(db.Integer, primary_key=True)
    # Some parts of the codebase define an extended Role model (see admin.py)
    # with required `code` and Arabic fields. Keep this model compatible.
    code = db.Column(db.String(50), unique=True, nullable=False)
    name = db.Column(db.String(80), unique=True, nullable=False)
    name_ar = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    description_ar = db.Column(db.Text)
    permissions = db.Column(db.JSON)  # صلاحيات مخزنة كـ JSON
    color = db.Column(db.String(20), default="blue")
    icon = db.Column(db.String(50), default="shield")
    is_system = db.Column(db.Boolean, default=False)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = db.Column(
        db.DateTime,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )
    created_by = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=True)
    priority = db.Column(db.Integer, default=0)

    # العلاقات (defined here to avoid backref conflicts)
    # users relationship defined explicitly instead of using backref

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Ensure required fields exist even if callers provide only `name`.
        if not getattr(self, "code", None):
            self.code = getattr(self, "name", None) or "role"
        if not getattr(self, "name_ar", None):
            self.name_ar = getattr(self, "name", None) or "دور"

    def __repr__(self):
        return f"<Role {self.name}>"

    def to_dict(self):
        return {
            "id": self.id,
            "code": getattr(self, "code", None),
            "name": self.name,
            "name_ar": getattr(self, "name_ar", None),
            "description": self.description,
            "description_ar": getattr(self, "description_ar", None),
            "permissions": self.permissions,
            "is_active": self.is_active,
            "is_system": getattr(self, "is_system", False),
            "priority": getattr(self, "priority", 0),
            "color": getattr(self, "color", None),
            "icon": getattr(self, "icon", None),
            "created_at": (self.created_at.isoformat() if self.created_at else None),
            "updated_at": (self.updated_at.isoformat() if self.updated_at else None),
        }


class User(db.Model):
    """نموذج المستخدمين مع نظام المصادقة المتقدم"""

    __tablename__ = "users"
    __table_args__ = {"extend_existing": True}

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    full_name = db.Column(db.String(200), nullable=False)
    role_id = db.Column(db.Integer, db.ForeignKey("roles.id"), nullable=False)
    is_active = db.Column(db.Boolean, default=True)
    last_login = db.Column(db.DateTime)
    login_count = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = db.Column(
        db.DateTime,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )

    # P0.5: Account lockout fields for security
    failed_login_count = db.Column(db.Integer, default=0)
    locked_until = db.Column(db.DateTime, nullable=True)
    last_failed_login = db.Column(db.DateTime, nullable=True)

    # معلومات إضافية
    phone = db.Column(db.String(20))
    department = db.Column(db.String(50))
    notes = db.Column(db.Text)

    # العلاقات
    # role = db.relationship('src.models.user.Role')  # Commented out to avoid mapper conflicts

    @property
    def role(self):
        """Get the user's role"""
        if self.role_id:
            return Role.query.get(self.role_id)
        return None

    def __init__(
        self,
        username,
        email,
        full_name,
        role_id,
        password_hash="",
        phone=None,
        department=None,
        notes=None,
        **kwargs,
    ):
        """تهيئة مستخدم جديد"""
        self.username = username
        self.email = email
        self.full_name = full_name
        self.role_id = role_id
        self.password_hash = password_hash
        self.phone = phone
        self.department = department
        self.notes = notes
        # Set any additional keyword arguments
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)

    def set_password(self, password):
        """تعيين كلمة مرور مشفرة"""
        # Import locally to avoid circular imports
        try:
            from src.auth import AuthManager

            self.password_hash = AuthManager.hash_password(password)
        except ImportError:
            # Fallback for testing
            import hashlib

            self.password_hash = hashlib.sha256(password.encode()).hexdigest()

    def check_password(self, password):
        """التحقق من كلمة المرور"""
        # Import locally to avoid circular imports
        try:
            from src.auth import AuthManager

            return AuthManager.verify_password(password, self.password_hash)
        except ImportError:
            # Fallback for testing
            import hashlib

            return self.password_hash == hashlib.sha256(password.encode()).hexdigest()
        except Exception:
            # Unexpected error, fallback to sha256
            import hashlib

            return self.password_hash == hashlib.sha256(password.encode()).hexdigest()

    def update_login_info(self):
        """تحديث معلومات تسجيل الدخول"""
        self.last_login = datetime.now(timezone.utc)
        self.login_count = (self.login_count or 0) + 1
        # P0.5: Reset failed login count on successful login
        self.failed_login_count = 0
        self.locked_until = None
        db.session.commit()

    # P0.5: Account lockout constants
    MAX_FAILED_ATTEMPTS = 5
    LOCKOUT_DURATION_MINUTES = 15

    def is_locked(self):
        """P0.5: Check if account is locked"""
        if self.locked_until is None:
            return False
        now = datetime.now(timezone.utc)
        if self.locked_until > now:
            return True
        # Lock expired, reset
        self.locked_until = None
        self.failed_login_count = 0
        db.session.commit()
        return False

    def record_failed_login(self):
        """P0.5: Record a failed login attempt"""
        self.failed_login_count = (self.failed_login_count or 0) + 1
        self.last_failed_login = datetime.now(timezone.utc)

        # Lock account if max attempts reached
        if self.failed_login_count >= self.MAX_FAILED_ATTEMPTS:
            self.locked_until = datetime.now(timezone.utc) + timedelta(
                minutes=self.LOCKOUT_DURATION_MINUTES
            )
        db.session.commit()

    def get_lockout_remaining_seconds(self):
        """P0.5: Get remaining lockout time in seconds"""
        if self.locked_until is None:
            return 0
        now = datetime.now(timezone.utc)
        if self.locked_until > now:
            return int((self.locked_until - now).total_seconds())
        return 0

    def __repr__(self):
        return f"<User {self.username}>"

    def to_dict(self, include_sensitive=False):
        data = {
            "id": self.id,
            "username": self.username,
            "email": self.email,
            "full_name": self.full_name,
            "role": self.role.name if self.role else "مستخدم",
            "role_id": self.role_id,
            "is_active": self.is_active,
            "last_login": (self.last_login.isoformat() if self.last_login else None),
            "login_count": self.login_count,
            "created_at": (self.created_at.isoformat() if self.created_at else None),
            "updated_at": (self.updated_at.isoformat() if self.updated_at else None),
            "phone": self.phone,
            "department": self.department,
            "notes": self.notes,
        }

        if include_sensitive:
            # معلومات حساسة للمديرين فقط
            data["password_hash"] = self.password_hash

        return data

    @staticmethod
    def authenticate(username, password):
        """
        مصادقة المستخدم مع دعم قفل الحساب
        P0.5: Implements account lockout after failed login attempts

        Returns:
            User: The authenticated user, or None if authentication failed

        Raises:
            AccountLockedError: If account is locked (check remaining_seconds)
        """
        # Use db.session directly to avoid SQLAlchemy relationship resolution issues
        from sqlalchemy import and_

        user = (
            db.session.query(User)
            .filter(and_(User.username == username, User.is_active))
            .first()
        )

        if not user:
            return None

        # P0.5: Check if account is locked
        if user.is_locked():
            remaining = user.get_lockout_remaining_seconds()
            raise AccountLockedError(
                f"Account locked. Try again in {remaining // 60} minutes.",
                remaining_seconds=remaining,
            )

        if user.check_password(password):
            user.update_login_info()
            return user

        # P0.5: Record failed login attempt
        user.record_failed_login()
        return None


class AccountLockedError(Exception):
    """P0.5: Exception raised when account is locked due to failed login attempts"""

    def __init__(self, message, remaining_seconds=0):
        self.message = message
        self.remaining_seconds = remaining_seconds
        super().__init__(self.message)

    @staticmethod
    def get_by_username(username):
        """الحصول على مستخدم بالاسم"""
        return User.query.filter_by(username=username).first()

    @staticmethod
    def get_by_email(email):
        """الحصول على مستخدم بالبريد الإلكتروني"""
        return User.query.filter_by(email=email).first()

    @staticmethod
    def create_user(username, password, email, full_name, role_id, **kwargs):
        """إنشاء مستخدم جديد"""
        # التحقق من عدم وجود المستخدم
        if User.get_by_username(username):
            raise ValueError("اسم المستخدم موجود بالفعل")

        if User.get_by_email(email):
            raise ValueError("البريد الإلكتروني موجود بالفعل")

        user = User(
            username=username,
            email=email,
            full_name=full_name,
            role_id=role_id,
            **kwargs,
        )
        user.set_password(password)

        db.session.add(user)
        db.session.commit()

        return user


class UserSession(db.Model):
    """نموذج جلسات المستخدمين"""

    __tablename__ = "user_sessions"
    __table_args__ = {"extend_existing": True}

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    session_id = db.Column(db.String(255), unique=True, nullable=False)
    ip_address = db.Column(db.String(45))
    user_agent = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    last_activity = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    is_active = db.Column(db.Boolean, default=True)

    # العلاقات
    user = db.relationship("src.models.user.User", viewonly=True)

    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "session_id": self.session_id,
            "ip_address": self.ip_address,
            "user_agent": self.user_agent,
            "created_at": (self.created_at.isoformat() if self.created_at else None),
            "last_activity": (
                self.last_activity.isoformat() if self.last_activity else None
            ),
            "is_active": self.is_active,
        }


class UserActivity(db.Model):
    """نموذج نشاطات المستخدمين"""

    __tablename__ = "user_activities"
    __table_args__ = {"extend_existing": True}

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    action = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    ip_address = db.Column(db.String(45))
    user_agent = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    # العلاقات
    user = db.relationship("src.models.user.User", viewonly=True)

    def __init__(
        self,
        user_id,
        action,
        description=None,
        ip_address=None,
        user_agent=None,
        **kwargs,
    ):
        """تهيئة نشاط مستخدم جديد"""
        self.user_id = user_id
        self.action = action
        self.description = description
        self.ip_address = ip_address
        self.user_agent = user_agent
        # Set any additional keyword arguments
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)

    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "action": self.action,
            "description": self.description,
            "ip_address": self.ip_address,
            "user_agent": self.user_agent,
            "created_at": (self.created_at.isoformat() if self.created_at else None),
            "user": self.user.full_name if self.user else "مستخدم غير معروف",
        }

    @staticmethod
    def log_activity(user_id, action, description=None, request=None):
        """تسجيل نشاط المستخدم"""
        activity = UserActivity(user_id=user_id, action=action, description=description)

        if request:
            activity.ip_address = request.remote_addr
            activity.user_agent = request.headers.get("User-Agent")

        db.session.add(activity)
        db.session.commit()

        return activity
