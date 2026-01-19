"""
واجهة برمجة التطبيقات للمصادقة والتحقق من الهوية
توفر هذه الوحدة واجهات برمجية للتسجيل الدخول وإدارة الجلسات والصلاحيات
"""

import hashlib
from datetime import datetime
from typing import Any, Dict

from fastapi import APIRouter, Body, Depends, HTTPException

from .auth_service import (
    PERMISSIONS_FILE,
    ROLES_FILE,
    USERS_FILE,
    AuthService,
    check_permission,
    get_current_user,
    load_data,
    save_data,
)

# Constants
NO_USER_MANAGEMENT_PERMISSION = "ليس لديك صلاحية لإدارة المستخدمين"

# إنشاء router للواجهة البرمجية
router = APIRouter(
    prefix="/api/auth",
    tags=["authentication"],
    responses={404: {"description": "Not found"}},
)


@router.post("/login")
async def login(credentials: Dict[str, str] = Body(...)):
    """تسجيل الدخول والحصول على رمز المصادقة"""
    username = credentials.get('username')
    password = credentials.get('password')

    if not username or not password:
        raise HTTPException(status_code=400,
                            detail="Username and password are required")

    auth_result = AuthService.authenticate(username, password)

    if auth_result:
        return auth_result
    else:
        raise HTTPException(
            status_code=401,
            detail="Invalid username or password")


@router.post("/logout")
async def logout(current_user: dict = Depends(get_current_user)):
    """تسجيل الخروج وإلغاء تنشيط الجلسة"""
    # Here we would need the token to logout, but FastAPI doesn't directly expose it
    # For now, we'll return a success message
    return {"message": "Logged out successfully"}


@router.get("/me")
async def get_current_user_info(
        current_user: dict = Depends(get_current_user)):
    """الحصول على معلومات المستخدم الحالي"""
    user = current_user

    # إضافة الصلاحيات والشركات والدول المسموح بها
    permissions = AuthService.get_user_permissions(user['id'])
    companies = AuthService.get_user_companies(user['id'])
    countries = AuthService.get_user_countries(user['id'])

    return {
        "user": user,
        "permissions": permissions,
        "companies": companies,
        "countries": countries
    }


@router.get("/permissions")
async def get_all_permissions(current_user: dict = Depends(get_current_user)):
    """الحصول على جميع الصلاحيات المتاحة في النظام"""
    if not check_permission(current_user, 'manage_roles'):
        raise HTTPException(status_code=403,
                            detail="ليس لديك صلاحية لإدارة الأدوار")

    permissions_data = load_data(PERMISSIONS_FILE)
    return permissions_data['permissions']


@router.get("/roles")
async def get_all_roles(current_user: dict = Depends(get_current_user)):
    """الحصول على جميع الأدوار المتاحة في النظام"""
    if not check_permission(current_user, 'manage_roles'):
        raise HTTPException(status_code=403,
                            detail="ليس لديك صلاحية لإدارة الأدوار")

    roles_data = load_data(ROLES_FILE)
    return roles_data['roles']


@router.get("/users")
async def get_all_users(current_user: dict = Depends(get_current_user)):
    """الحصول على جميع المستخدمين في النظام"""
    if not check_permission(current_user, 'manage_users'):
        raise HTTPException(
            status_code=403,
            detail=NO_USER_MANAGEMENT_PERMISSION)

    users_data = load_data(USERS_FILE)

    # إزالة حقول كلمة المرور من البيانات المرسلة
    users = []
    for user in users_data['users']:
        user_copy = user.copy()
        if 'password_hash' in user_copy:
            del user_copy['password_hash']
        users.append(user_copy)

    return users


@router.post("/users")
async def create_user(
    user_data: Dict[str, Any] = Body(...),
    current_user: dict = Depends(get_current_user)
):
    """إنشاء مستخدم جديد"""
    if not check_permission(current_user, 'manage_users'):
        raise HTTPException(
            status_code=403,
            detail=NO_USER_MANAGEMENT_PERMISSION)

    # التحقق من البيانات المطلوبة
    required_fields = ['username', 'password', 'name_ar', 'name_en', 'email']
    for field in required_fields:
        if field not in user_data:
            raise HTTPException(
                status_code=400,
                detail=f"Field '{field}' is required")

    # التحقق من عدم وجود مستخدم بنفس اسم المستخدم أو البريد الإلكتروني
    users_data = load_data(USERS_FILE)
    if any(u['username'] == user_data['username']
           for u in users_data['users']):
        raise HTTPException(status_code=400, detail="Username already exists")

    if any(u['email'] == user_data['email'] for u in users_data['users']):
        raise HTTPException(status_code=400, detail="Email already exists")

    # إنشاء المستخدم الجديد
    new_user = {
        "id": f"user{len(users_data['users']) + 1}",
        "username": user_data['username'],
        "password_hash": hashlib.sha256(
            user_data['password'].encode()).hexdigest(),
        "name_ar": user_data['name_ar'],
        "name_en": user_data['name_en'],
        "email": user_data['email'],
        "is_active": user_data.get(
            'is_active',
            True),
        "is_admin": user_data.get(
            'is_admin',
                False),
        "created_at": datetime.now().isoformat(),
        "last_login": None}

    users_data['users'].append(new_user)
    save_data(USERS_FILE, users_data)

    # إزالة حقل كلمة المرور من البيانات المرسلة
    user_copy = new_user.copy()
    del user_copy['password_hash']

    return user_copy


@router.put("/users/{user_id}")
async def update_user(
    user_id: str,
    user_data: Dict[str, Any] = Body(...),
    current_user: dict = Depends(get_current_user)
):
    """تحديث مستخدم موجود"""
    if not check_permission(current_user, 'manage_users'):
        raise HTTPException(
            status_code=403,
            detail=NO_USER_MANAGEMENT_PERMISSION)

    # التحقق من وجود المستخدم
    users_data = load_data(USERS_FILE)
    user_index = next((i for i, u in enumerate(
        users_data['users']) if u['id'] == user_id), None)

    if user_index is None:
        raise HTTPException(status_code=404, detail="User not found")

    # التحقق من عدم وجود مستخدم آخر بنفس اسم المستخدم أو البريد الإلكتروني
    if 'username' in user_data:
        if any(u['username'] == user_data['username'] and u['id']
               != user_id for u in users_data['users']):
            raise HTTPException(
                status_code=400,
                detail="Username already exists")

    if 'email' in user_data:
        if any(u['email'] == user_data['email'] and u['id']
               != user_id for u in users_data['users']):
            raise HTTPException(status_code=400, detail="Email already exists")

    # تحديث بيانات المستخدم
    user = users_data['users'][user_index]

    if 'username' in user_data:
        user['username'] = user_data['username']

    if 'password' in user_data:
        user['password_hash'] = hashlib.sha256(
            user_data['password'].encode()).hexdigest()

    if 'name_ar' in user_data:
        user['name_ar'] = user_data['name_ar']

    if 'name_en' in user_data:
        user['name_en'] = user_data['name_en']

    if 'email' in user_data:
        user['email'] = user_data['email']

    if 'is_active' in user_data:
        user['is_active'] = user_data['is_active']

    if 'is_admin' in user_data:
        user['is_admin'] = user_data['is_admin']

    save_data(USERS_FILE, users_data)

    # إزالة حقل كلمة المرور من البيانات المرسلة
    user_copy = user.copy()
    if 'password_hash' in user_copy:
        del user_copy['password_hash']

    return user_copy


@router.delete("/users/{user_id}")
async def delete_user(
    user_id: str,
    current_user: dict = Depends(get_current_user)
):
    """حذف مستخدم موجود"""
    if not check_permission(current_user, 'manage_users'):
        raise HTTPException(
            status_code=403,
            detail=NO_USER_MANAGEMENT_PERMISSION)

    # التحقق من وجود المستخدم
    users_data = load_data(USERS_FILE)
    user_index = next((i for i, u in enumerate(
        users_data['users']) if u['id'] == user_id), None)

    if user_index is None:
        raise HTTPException(status_code=404, detail="User not found")

    # حذف المستخدم
    deleted_user = users_data['users'].pop(user_index)
    save_data(USERS_FILE, users_data)

    return {"message": f"User {deleted_user['username']} deleted successfully"}


@router.post("/check-permission")
async def check_user_permission(
    permission_data: Dict[str, str] = Body(...),
    current_user: dict = Depends(get_current_user)
):
    """التحقق من صلاحية محددة للمستخدم الحالي"""
    permission_id = permission_data.get('permission_id')

    if not permission_id:
        raise HTTPException(
            status_code=400,
            detail="Permission ID is required")

    has_permission = check_permission(current_user, permission_id)

    return {"has_permission": has_permission}
