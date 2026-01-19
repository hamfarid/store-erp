"""
خدمة المصادقة والتحقق من الهوية
توفر هذه الوحدة خدمات المصادقة وإدارة الجلسات والتحقق من الصلاحيات
"""

import os
import json
import uuid
from datetime import datetime, timezone, timedelta
import hashlib
import jwt
from fastapi import HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from typing import Dict, Any

# مسار ملفات البيانات المؤقتة (في التطبيق الحقيقي سيتم استخدام قاعدة بيانات)
DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data')
USERS_FILE = os.path.join(DATA_DIR, 'users.json')
SESSIONS_FILE = os.path.join(DATA_DIR, 'sessions.json')
ROLES_FILE = os.path.join(DATA_DIR, 'roles.json')
PERMISSIONS_FILE = os.path.join(DATA_DIR, 'permissions.json')

# JWT settings
JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY', 'your-secret-key-here')
JWT_ALGORITHM = 'HS256'
JWT_EXPIRATION_DELTA = timedelta(hours=24)

# FastAPI security
security = HTTPBearer()

# التأكد من وجود مجلد البيانات
os.makedirs(DATA_DIR, exist_ok=True)

# دالة مساعدة لتحميل البيانات من ملف JSON


def load_data(file_path, default_data=None):
    if default_data is None:
        default_data = {}

    if not os.path.exists(file_path):
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(default_data, f, ensure_ascii=False, indent=2)
        return default_data

    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except (json.JSONDecodeError, FileNotFoundError):
        return default_data


# دالة مساعدة لحفظ البيانات في ملف JSON
def save_data(file_path, data):
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

# تهيئة البيانات الافتراضية إذا لم تكن موجودة


def init_default_data():
    # التأكد من وجود مجلد البيانات
    os.makedirs(DATA_DIR, exist_ok=True)

    # البيانات الافتراضية للمستخدمين
    default_users = {
        "users": [
            {
                "id": "user1",
                "username": "admin",
                "password_hash": hashlib.sha256("admin123".encode()).hexdigest(),
                "name_ar": "مدير النظام",
                "name_en": "System Admin",
                "email": "admin@example.com",
                "is_active": True,
                "is_admin": True,
                "created_at": (datetime.now() - timedelta(days=30)).isoformat(),
                "last_login": datetime.now().isoformat()
            },
            {
                "id": "user2",
                "username": "manager",
                "password_hash": hashlib.sha256("manager123".encode()).hexdigest(),
                "name_ar": "مدير",
                "name_en": "Manager",
                "email": "manager@example.com",
                "is_active": True,
                "is_admin": False,
                "created_at": (datetime.now() - timedelta(days=20)).isoformat(),
                "last_login": datetime.now().isoformat()
            },
            {
                "id": "user3",
                "username": "user",
                "password_hash": hashlib.sha256("user123".encode()).hexdigest(),
                "name_ar": "مستخدم",
                "name_en": "User",
                "email": "user@example.com",
                "is_active": True,
                "is_admin": False,
                "created_at": (datetime.now() - timedelta(days=10)).isoformat(),
                "last_login": datetime.now().isoformat()
            }
        ]
    }

    # البيانات الافتراضية للجلسات
    default_sessions = {
        "sessions": []
    }

    # البيانات الافتراضية للأدوار
    default_roles = {
        "roles": [
            {
                "id": "admin",
                "name_ar": "مدير",
                "name_en": "Admin",
                "description_ar": "صلاحيات كاملة للنظام",
                "description_en": "Full system permissions"
            },
            {
                "id": "manager",
                "name_ar": "مشرف",
                "name_en": "Manager",
                "description_ar": "صلاحيات إدارة المديولات والمستخدمين",
                "description_en": "Module and user management permissions"
            },
            {
                "id": "user",
                "name_ar": "مستخدم",
                "name_en": "User",
                "description_ar": "صلاحيات استخدام النظام الأساسية",
                "description_en": "Basic system usage permissions"
            }
        ],
        "user_roles": [
            {"user_id": "user1", "role_id": "admin"},
            {"user_id": "user2", "role_id": "manager"},
            {"user_id": "user3", "role_id": "user"}
        ]
    }

    # البيانات الافتراضية للصلاحيات
    default_permissions = {
        "permissions": [
            {
                "id": "view_dashboard",
                "name_ar": "عرض لوحة التحكم",
                "name_en": "View Dashboard",
                "module": "core"
            },
            {
                "id": "manage_users",
                "name_ar": "إدارة المستخدمين",
                "name_en": "Manage Users",
                "module": "core"
            },
            {
                "id": "manage_roles",
                "name_ar": "إدارة الأدوار",
                "name_en": "Manage Roles",
                "module": "core"
            },
            {
                "id": "manage_modules",
                "name_ar": "إدارة المديولات",
                "name_en": "Manage Modules",
                "module": "module_management"
            },
            {
                "id": "view_resources",
                "name_ar": "عرض الموارد",
                "name_en": "View Resources",
                "module": "resource_monitoring"
            },
            {
                "id": "manage_alerts",
                "name_ar": "إدارة التنبيهات",
                "name_en": "Manage Alerts",
                "module": "alert_management"
            },
            {
                "id": "manage_ai_agents",
                "name_ar": "إدارة وكلاء الذكاء الصناعي",
                "name_en": "Manage AI Agents",
                "module": "ai_management"
            },
            {
                "id": "view_ai_stats",
                "name_ar": "عرض إحصائيات الذكاء الصناعي",
                "name_en": "View AI Stats",
                "module": "ai_management"
            },
            {
                "id": "manage_backups",
                "name_ar": "إدارة النسخ الاحتياطي",
                "name_en": "Manage Backups",
                "module": "backup_module"
            },
            {
                "id": "manage_data_validation",
                "name_ar": "إدارة التحقق من صحة البيانات",
                "name_en": "Manage Data Validation",
                "module": "data_validation"
            },
            {
                "id": "manage_settings",
                "name_ar": "إدارة الإعدادات",
                "name_en": "Manage Settings",
                "module": "core"
            }
        ],
        "role_permissions": [
            {"role_id": "admin", "permission_id": "view_dashboard"},
            {"role_id": "admin", "permission_id": "manage_users"},
            {"role_id": "admin", "permission_id": "manage_roles"},
            {"role_id": "admin", "permission_id": "manage_modules"},
            {"role_id": "admin", "permission_id": "view_resources"},
            {"role_id": "admin", "permission_id": "manage_alerts"},
            {"role_id": "admin", "permission_id": "manage_ai_agents"},
            {"role_id": "admin", "permission_id": "view_ai_stats"},
            {"role_id": "admin", "permission_id": "manage_backups"},
            {"role_id": "admin", "permission_id": "manage_data_validation"},
            {"role_id": "admin", "permission_id": "manage_settings"},

            {"role_id": "manager", "permission_id": "view_dashboard"},
            {"role_id": "manager", "permission_id": "manage_modules"},
            {"role_id": "manager", "permission_id": "view_resources"},
            {"role_id": "manager", "permission_id": "manage_alerts"},
            {"role_id": "manager", "permission_id": "manage_ai_agents"},
            {"role_id": "manager", "permission_id": "view_ai_stats"},

            {"role_id": "user", "permission_id": "view_dashboard"},
            {"role_id": "user", "permission_id": "view_resources"},
            {"role_id": "user", "permission_id": "view_ai_stats"}
        ],
        "company_permissions": [
            {"user_id": "user1", "company_id": "all"},
            {"user_id": "user2", "company_id": "company1"},
            {"user_id": "user3", "company_id": "company1"}
        ],
        "country_permissions": [
            {"user_id": "user1", "country_id": "all"},
            {"user_id": "user2", "country_id": "country1"},
            {"user_id": "user3", "country_id": "country1"}
        ]
    }

    # حفظ البيانات الافتراضية إذا لم تكن الملفات موجودة
    if not os.path.exists(USERS_FILE):
        save_data(USERS_FILE, default_users)

    if not os.path.exists(SESSIONS_FILE):
        save_data(SESSIONS_FILE, default_sessions)

    if not os.path.exists(ROLES_FILE):
        save_data(ROLES_FILE, default_roles)

    if not os.path.exists(PERMISSIONS_FILE):
        save_data(PERMISSIONS_FILE, default_permissions)


# تهيئة البيانات الافتراضية
init_default_data()


class AuthService:
    """خدمة المصادقة والتحقق من الهوية"""

    @staticmethod
    def authenticate(username, password):
        """التحقق من صحة بيانات المستخدم"""
        users_data = load_data(USERS_FILE)
        password_hash = hashlib.sha256(password.encode()).hexdigest()

        for user in users_data['users']:
            if user['username'] == username and user['password_hash'] == password_hash and user['is_active']:
                # تحديث وقت آخر تسجيل دخول
                user['last_login'] = datetime.now().isoformat()
                save_data(USERS_FILE, users_data)

                # إنشاء جلسة جديدة
                session_id = str(uuid.uuid4())
                token = AuthService.generate_token(user['id'], session_id)

                # حفظ الجلسة
                sessions_data = load_data(SESSIONS_FILE)
                sessions_data['sessions'].append({
                    'id': session_id,
                    'user_id': user['id'],
                    'created_at': datetime.now().isoformat(),
                    'expires_at': (datetime.now() + timedelta(hours=24)).isoformat(),
                    'is_active': True
                })
                save_data(SESSIONS_FILE, sessions_data)

                return {
                    'token': token,
                    'user': {
                        'id': user['id'],
                        'username': user['username'],
                        'name_ar': user['name_ar'],
                        'name_en': user['name_en'],
                        'email': user['email'],
                        'is_admin': user['is_admin']
                    }
                }

        return None

    @staticmethod
    def generate_token(user_id, session_id):
        """إنشاء رمز المصادقة JWT"""
        payload = {
            'user_id': user_id,
            'session_id': session_id,
            'exp': datetime.now(timezone.utc) + JWT_EXPIRATION_DELTA
        }
        return jwt.encode(payload, JWT_SECRET_KEY, algorithm=JWT_ALGORITHM)

    @staticmethod
    def verify_token(token):
        """التحقق من صحة رمز المصادقة"""
        try:
            payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[JWT_ALGORITHM])
            user_id = payload['user_id']
            session_id = payload['session_id']

            # التحقق من وجود الجلسة ونشاطها
            sessions_data = load_data(SESSIONS_FILE)
            session = next((s for s in sessions_data['sessions'] if s['id'] == session_id and s['is_active']), None)

            if session:
                # التحقق من وجود المستخدم ونشاطه
                users_data = load_data(USERS_FILE)
                user = next((u for u in users_data['users'] if u['id'] == user_id and u['is_active']), None)

                if user:
                    return user

            return None
        except jwt.ExpiredSignatureError:
            return None
        except jwt.InvalidTokenError:
            return None

    @staticmethod
    def logout(token):
        """تسجيل الخروج وإلغاء تنشيط الجلسة"""
        try:
            payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[JWT_ALGORITHM])
            session_id = payload['session_id']

            # إلغاء تنشيط الجلسة
            sessions_data = load_data(SESSIONS_FILE)
            for session in sessions_data['sessions']:
                if session['id'] == session_id:
                    session['is_active'] = False
                    save_data(SESSIONS_FILE, sessions_data)
                    return True

            return False
        except BaseException:
            return False

    @staticmethod
    def get_user_permissions(user_id):
        """الحصول على صلاحيات المستخدم"""
        roles_data = load_data(ROLES_FILE)
        permissions_data = load_data(PERMISSIONS_FILE)

        # الحصول على أدوار المستخدم
        user_roles = [ur['role_id'] for ur in roles_data['user_roles'] if ur['user_id'] == user_id]

        # الحصول على صلاحيات الأدوار
        user_permissions = []
        for role_id in user_roles:
            role_perms = [rp['permission_id'] for rp in permissions_data['role_permissions'] if rp['role_id'] == role_id]
            user_permissions.extend(role_perms)

        # إزالة التكرارات
        user_permissions = list(set(user_permissions))

        # الحصول على تفاصيل الصلاحيات
        permissions = []
        for perm_id in user_permissions:
            perm = next((p for p in permissions_data['permissions'] if p['id'] == perm_id), None)
            if perm:
                permissions.append(perm)

        return permissions

    @staticmethod
    def get_user_companies(user_id):
        """الحصول على الشركات المسموح بها للمستخدم"""
        permissions_data = load_data(PERMISSIONS_FILE)

        # التحقق من وجود صلاحية لجميع الشركات
        all_companies = next((cp['company_id'] for cp in permissions_data['company_permissions'] if cp['user_id'] == user_id and cp['company_id'] == 'all'), None)

        if all_companies:
            return ['all']

        # الحصول على الشركات المحددة
        companies = [cp['company_id'] for cp in permissions_data['company_permissions'] if cp['user_id'] == user_id]

        return companies

    @staticmethod
    def get_user_countries(user_id):
        """الحصول على الدول المسموح بها للمستخدم"""
        permissions_data = load_data(PERMISSIONS_FILE)

        # التحقق من وجود صلاحية لجميع الدول
        all_countries = next((cp['country_id'] for cp in permissions_data['country_permissions'] if cp['user_id'] == user_id and cp['country_id'] == 'all'), None)

        if all_countries:
            return ['all']

        # الحصول على الدول المحددة
        countries = [cp['country_id'] for cp in permissions_data['country_permissions'] if cp['user_id'] == user_id]

        return countries

    @staticmethod
    def has_permission(user_id, permission_id):
        """التحقق من وجود صلاحية محددة للمستخدم"""
        permissions = AuthService.get_user_permissions(user_id)
        return any(p['id'] == permission_id for p in permissions)

    @staticmethod
    def has_company_access(user_id, company_id):
        """التحقق من وجود صلاحية للشركة المحددة"""
        companies = AuthService.get_user_companies(user_id)
        return 'all' in companies or company_id in companies

    @staticmethod
    def has_country_access(user_id, country_id):
        """التحقق من وجود صلاحية للدولة المحددة"""
        countries = AuthService.get_user_countries(user_id)
        return 'all' in countries or country_id in countries

# FastAPI authentication functions


async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)) -> Dict[str, Any]:
    """Get current user from JWT token"""
    if not credentials:
        raise HTTPException(status_code=401, detail="Authentication credentials required")

    user_data = AuthService.verify_token(credentials.credentials)
    if not user_data:
        raise HTTPException(status_code=401, detail="Invalid or expired token")

    return user_data


def check_permission(user: Dict[str, Any], permission: str) -> bool:
    """Check if user has specific permission"""
    if not user:
        return False

    user_id = user.get('id')  # Changed from 'user_id' to 'id' based on the user structure
    if not user_id:
        return False

    return AuthService.has_permission(user_id, permission)


def check_company_access(user: Dict[str, Any], company_id: str) -> bool:
    """Check if user has access to specific company"""
    if not user:
        return False

    user_id = user.get('id')
    if not user_id:
        return False

    return AuthService.has_company_access(user_id, company_id)


def check_country_access(user: Dict[str, Any], country_id: str) -> bool:
    """Check if user has access to specific country"""
    if not user:
        return False

    user_id = user.get('id')
    if not user_id:
        return False

    return AuthService.has_country_access(user_id, country_id)
