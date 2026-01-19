"""
/home/ubuntu/implemented_files/v3/src/modules/user_management/api.py

واجهة برمجة التطبيقات لمديول إدارة المستخدمين

يوفر هذا الملف واجهة برمجة التطبيقات (API) لمديول إدارة المستخدمين في نظام Gaara ERP.
"""

from typing import List, Dict, Any
from fastapi import APIRouter, Depends, HTTPException, status, Query, Path, Body
from sqlalchemy.orm import Session

from ...database import get_db
from ..permissions.service import PermissionService
from .service import UserService
from .schemas import (
    UserCreate,
    UserUpdate,
    UserResponse,
    UserDetailResponse,
    UserProfileCreate,
    UserProfileUpdate,
    UserProfileResponse,
    UserPreferenceCreate,
    UserPreferenceUpdate,
    UserPreferenceResponse,
    RoleCreate,
    RoleUpdate,
    RoleResponse,
    OrganizationCreate,
    OrganizationUpdate,
    OrganizationResponse,
    OrganizationDetailResponse,
    ChangePasswordRequest,
    ChangePasswordResponse,
    AssignRoleRequest,
    AssignRoleResponse,
    UserSearchRequest,
    UserSearchResponse,
)
from ..auth.dependencies import get_current_active_user, get_current_admin_user

# ثوابت الرسائل
ACCESS_DENIED_MESSAGE = "ليس لديك صلاحية للوصول إلى هذا المورد"
USER_NOT_FOUND_MESSAGE = "المستخدم غير موجود"
USER_ID_DESCRIPTION = "معرف المستخدم"

# إنشاء موجه API
router = APIRouter(
    prefix="/api/v1/users",
    tags=["users"],
    responses={404: {"description": "Not found"}},
)

# ==================== نقاط نهاية المستخدمين ====================


@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def create_user(
    user_data: UserCreate,
    db: Session = Depends(get_db),
    current_user: Dict[str, Any] = Depends(get_current_admin_user),
):
    """
    إنشاء مستخدم جديد (للمسؤولين فقط)
    """
    user_service = UserService(db)
    user = user_service.create_user(user_data, current_user["id"])
    return user


@router.get("/", response_model=List[UserResponse])
async def read_users(
    skip: int = Query(0, description="عدد المستخدمين للتخطي"),
    limit: int = Query(100, description="الحد الأقصى لعدد المستخدمين"),
    db: Session = Depends(get_db),
    current_user: Dict[str, Any] = Depends(get_current_active_user),
):
    """
    استرجاع قائمة المستخدمين
    """
    # التحقق من الصلاحيات
    permission_service = PermissionService(db)
    if not permission_service.has_permission(current_user["id"], "users", "read"):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail=ACCESS_DENIED_MESSAGE
        )

    user_service = UserService(db)
    users = user_service.get_users(skip, limit)
    return users


@router.post("/search", response_model=UserSearchResponse)
async def search_users(
    search_data: UserSearchRequest,
    db: Session = Depends(get_db),
    current_user: Dict[str, Any] = Depends(get_current_active_user),
):
    """
    البحث عن المستخدمين
    """
    # التحقق من الصلاحيات
    permission_service = PermissionService(db)
    if not permission_service.has_permission(current_user["id"], "users", "read"):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail=ACCESS_DENIED_MESSAGE
        )

    user_service = UserService(db)
    users, total = user_service.search_users(search_data)
    return {"total": total, "items": users}


@router.get("/me", response_model=UserDetailResponse)
async def read_user_me(
    db: Session = Depends(get_db),
    current_user: Dict[str, Any] = Depends(get_current_active_user),
):
    """
    استرجاع معلومات المستخدم الحالي
    """
    user_service = UserService(db)
    user = user_service.get_user_with_details(current_user["id"])
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=USER_NOT_FOUND_MESSAGE
        )
    return user


@router.get("/{user_id}", response_model=UserDetailResponse)
async def read_user(
    user_id: str = Path(..., description=USER_ID_DESCRIPTION),
    db: Session = Depends(get_db),
    current_user: Dict[str, Any] = Depends(get_current_active_user),
):
    """
    استرجاع معلومات مستخدم محدد
    """
    # التحقق من الصلاحيات
    permission_service = PermissionService(db)
    if current_user["id"] != user_id and not permission_service.has_permission(
        current_user["id"], "users", "read"
    ):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail=ACCESS_DENIED_MESSAGE
        )

    user_service = UserService(db)
    user = user_service.get_user_with_details(user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=USER_NOT_FOUND_MESSAGE
        )
    return user


@router.put("/{user_id}", response_model=UserResponse)
async def update_user(
    user_id: str = Path(..., description=USER_ID_DESCRIPTION),
    user_data: UserUpdate = Body(...),
    db: Session = Depends(get_db),
    current_user: Dict[str, Any] = Depends(get_current_active_user),
):
    """
    تحديث معلومات مستخدم
    """
    # التحقق من الصلاحيات
    permission_service = PermissionService(db)
    if current_user["id"] != user_id and not permission_service.has_permission(
        current_user["id"], "users", "update"
    ):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail=ACCESS_DENIED_MESSAGE
        )

    user_service = UserService(db)
    user = user_service.update_user(user_id, user_data, current_user["id"])
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=USER_NOT_FOUND_MESSAGE
        )
    return user


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(
    user_id: str = Path(..., description=USER_ID_DESCRIPTION),
    db: Session = Depends(get_db),
    current_user: Dict[str, Any] = Depends(get_current_admin_user),
):
    """
    حذف مستخدم (للمسؤولين فقط)
    """
    user_service = UserService(db)
    result = user_service.delete_user(user_id)
    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=USER_NOT_FOUND_MESSAGE
        )
    return None


@router.post("/change-password", response_model=ChangePasswordResponse)
async def change_password(
    password_data: ChangePasswordRequest,
    db: Session = Depends(get_db),
    current_user: Dict[str, Any] = Depends(get_current_active_user),
):
    """
    تغيير كلمة المرور للمستخدم الحالي
    """
    user_service = UserService(db)
    result = user_service.change_password(current_user["id"], password_data)
    if not result:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="فشل في تغيير كلمة المرور، تحقق من كلمة المرور الحالية",
        )
    return result


# ==================== نقاط نهاية الملف الشخصي ====================


@router.post("/profile", response_model=UserProfileResponse)
async def create_user_profile(
    profile_data: UserProfileCreate,
    db: Session = Depends(get_db),
    current_user: Dict[str, Any] = Depends(get_current_active_user),
):
    """
    إنشاء ملف شخصي للمستخدم الحالي
    """
    user_service = UserService(db)
    profile = user_service.create_user_profile(current_user["id"], profile_data)
    return profile


@router.get("/profile/{user_id}", response_model=UserProfileResponse)
async def read_user_profile(
    user_id: str = Path(..., description=USER_ID_DESCRIPTION),
    db: Session = Depends(get_db),
    current_user: Dict[str, Any] = Depends(get_current_active_user),
):
    """
    استرجاع ملف شخصي لمستخدم محدد
    """
    # التحقق من الصلاحيات
    permission_service = PermissionService(db)
    if current_user["id"] != user_id and not permission_service.has_permission(
        current_user["id"], "users", "read"
    ):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail=ACCESS_DENIED_MESSAGE
        )

    user_service = UserService(db)
    profile = user_service.get_user_profile(user_id)
    if not profile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="الملف الشخصي غير موجود"
        )
    return profile


@router.put("/profile/{user_id}", response_model=UserProfileResponse)
async def update_user_profile(
    user_id: str = Path(..., description=USER_ID_DESCRIPTION),
    profile_data: UserProfileUpdate = Body(...),
    db: Session = Depends(get_db),
    current_user: Dict[str, Any] = Depends(get_current_active_user),
):
    """
    تحديث ملف شخصي لمستخدم
    """
    # التحقق من الصلاحيات
    permission_service = PermissionService(db)
    if current_user["id"] != user_id and not permission_service.has_permission(
        current_user["id"], "users", "update"
    ):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail=ACCESS_DENIED_MESSAGE
        )

    user_service = UserService(db)
    profile = user_service.update_user_profile(user_id, profile_data)
    if not profile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="الملف الشخصي غير موجود"
        )
    return profile


# ==================== نقاط نهاية التفضيلات ====================


@router.post("/preferences", response_model=UserPreferenceResponse)
async def create_user_preference(
    preference_data: UserPreferenceCreate,
    db: Session = Depends(get_db),
    current_user: Dict[str, Any] = Depends(get_current_active_user),
):
    """
    إنشاء تفضيلات للمستخدم الحالي
    """
    user_service = UserService(db)
    preference = user_service.create_user_preference(
        current_user["id"], preference_data
    )
    return preference


@router.get("/preferences/{user_id}", response_model=UserPreferenceResponse)
async def read_user_preference(
    user_id: str = Path(..., description=USER_ID_DESCRIPTION),
    db: Session = Depends(get_db),
    current_user: Dict[str, Any] = Depends(get_current_active_user),
):
    """
    استرجاع تفضيلات مستخدم محدد
    """
    # التحقق من الصلاحيات
    permission_service = PermissionService(db)
    if current_user["id"] != user_id and not permission_service.has_permission(
        current_user["id"], "users", "read"
    ):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail=ACCESS_DENIED_MESSAGE
        )

    user_service = UserService(db)
    preference = user_service.get_user_preference(user_id)
    if not preference:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="التفضيلات غير موجودة"
        )
    return preference


@router.put("/preferences/{user_id}", response_model=UserPreferenceResponse)
async def update_user_preference(
    user_id: str = Path(..., description=USER_ID_DESCRIPTION),
    preference_data: UserPreferenceUpdate = Body(...),
    db: Session = Depends(get_db),
    current_user: Dict[str, Any] = Depends(get_current_active_user),
):
    """
    تحديث تفضيلات مستخدم
    """
    # التحقق من الصلاحيات
    permission_service = PermissionService(db)
    if current_user["id"] != user_id and not permission_service.has_permission(
        current_user["id"], "users", "update"
    ):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail=ACCESS_DENIED_MESSAGE
        )

    user_service = UserService(db)
    preference = user_service.update_user_preference(user_id, preference_data)
    if not preference:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="التفضيلات غير موجودة"
        )
    return preference


# ==================== نقاط نهاية الأدوار ====================


@router.post("/roles", response_model=RoleResponse, status_code=status.HTTP_201_CREATED)
async def create_role(
    role_data: RoleCreate,
    db: Session = Depends(get_db),
    current_user: Dict[str, Any] = Depends(get_current_admin_user),
):
    """
    إنشاء دور جديد (للمسؤولين فقط)
    """
    user_service = UserService(db)
    role = user_service.create_role(role_data, current_user["id"])
    return role


@router.get("/roles", response_model=List[RoleResponse])
async def read_roles(
    skip: int = Query(0, description="عدد الأدوار للتخطي"),
    limit: int = Query(100, description="الحد الأقصى لعدد الأدوار"),
    db: Session = Depends(get_db),
    current_user: Dict[str, Any] = Depends(get_current_active_user),
):
    """
    استرجاع قائمة الأدوار
    """
    # التحقق من الصلاحيات
    permission_service = PermissionService(db)
    if not permission_service.has_permission(current_user["id"], "roles", "read"):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail=ACCESS_DENIED_MESSAGE
        )

    user_service = UserService(db)
    roles = user_service.get_roles(skip, limit)
    return roles


@router.get("/roles/{role_id}", response_model=RoleResponse)
async def read_role(
    role_id: str = Path(..., description="معرف الدور"),
    db: Session = Depends(get_db),
    current_user: Dict[str, Any] = Depends(get_current_active_user),
):
    """
    استرجاع معلومات دور محدد
    """
    # التحقق من الصلاحيات
    permission_service = PermissionService(db)
    if not permission_service.has_permission(current_user["id"], "roles", "read"):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail=ACCESS_DENIED_MESSAGE
        )

    user_service = UserService(db)
    role = user_service.get_role(role_id)
    if not role:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="الدور غير موجود"
        )
    return role


@router.put("/roles/{role_id}", response_model=RoleResponse)
async def update_role(
    role_id: str = Path(..., description="معرف الدور"),
    role_data: RoleUpdate = Body(...),
    db: Session = Depends(get_db),
    current_user: Dict[str, Any] = Depends(get_current_admin_user),
):
    """
    تحديث معلومات دور (للمسؤولين فقط)
    """
    user_service = UserService(db)
    role = user_service.update_role(role_id, role_data, current_user["id"])
    if not role:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="الدور غير موجود"
        )
    return role


@router.delete("/roles/{role_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_role(
    role_id: str = Path(..., description="معرف الدور"),
    db: Session = Depends(get_db),
    current_user: Dict[str, Any] = Depends(get_current_admin_user),
):
    """
    حذف دور (للمسؤولين فقط)
    """
    user_service = UserService(db)
    result = user_service.delete_role(role_id)
    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="الدور غير موجود"
        )
    return None


@router.get("/roles/user/{user_id}", response_model=List[RoleResponse])
async def read_user_roles(
    user_id: str = Path(..., description=USER_ID_DESCRIPTION),
    db: Session = Depends(get_db),
    current_user: Dict[str, Any] = Depends(get_current_active_user),
):
    """
    استرجاع أدوار مستخدم محدد
    """
    # التحقق من الصلاحيات
    permission_service = PermissionService(db)
    if current_user["id"] != user_id and not permission_service.has_permission(
        current_user["id"], "users", "read"
    ):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail=ACCESS_DENIED_MESSAGE
        )

    user_service = UserService(db)
    roles = user_service.get_user_roles(user_id)
    return roles


@router.post("/roles/assign", response_model=AssignRoleResponse)
async def assign_role_to_user(
    assign_data: AssignRoleRequest,
    db: Session = Depends(get_db),
    current_user: Dict[str, Any] = Depends(get_current_admin_user),
):
    """
    تعيين دور لمستخدم (للمسؤولين فقط)
    """
    user_service = UserService(db)
    result = user_service.assign_role_to_user(
        assign_data.user_id, assign_data.role_id, current_user["id"]
    )
    return result


@router.delete(
    "/roles/remove/{user_id}/{role_id}", status_code=status.HTTP_204_NO_CONTENT
)
async def remove_role_from_user(
    user_id: str = Path(..., description=USER_ID_DESCRIPTION),
    role_id: str = Path(..., description="معرف الدور"),
    db: Session = Depends(get_db),
    current_user: Dict[str, Any] = Depends(get_current_admin_user),
):
    """
    إزالة دور من مستخدم (للمسؤولين فقط)
    """
    user_service = UserService(db)
    result = user_service.remove_role_from_user(user_id, role_id)
    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="لم يتم العثور على المستخدم أو الدور",
        )
    return None


# ==================== نقاط نهاية المؤسسات ====================


@router.post(
    "/organizations",
    response_model=OrganizationResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_organization(
    org_data: OrganizationCreate,
    db: Session = Depends(get_db),
    current_user: Dict[str, Any] = Depends(get_current_admin_user),
):
    """
    إنشاء مؤسسة جديدة (للمسؤولين فقط)
    """
    user_service = UserService(db)
    organization = user_service.create_organization(org_data, current_user["id"])
    return organization


@router.get("/organizations", response_model=List[OrganizationResponse])
async def read_organizations(
    skip: int = Query(0, description="عدد المؤسسات للتخطي"),
    limit: int = Query(100, description="الحد الأقصى لعدد المؤسسات"),
    db: Session = Depends(get_db),
    current_user: Dict[str, Any] = Depends(get_current_active_user),
):
    """
    استرجاع قائمة المؤسسات
    """
    # التحقق من الصلاحيات
    permission_service = PermissionService(db)
    if not permission_service.has_permission(
        current_user["id"], "organizations", "read"
    ):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail=ACCESS_DENIED_MESSAGE
        )

    user_service = UserService(db)
    organizations = user_service.get_organizations(skip, limit)
    return organizations


@router.get("/organizations/{org_id}", response_model=OrganizationDetailResponse)
async def read_organization(
    org_id: str = Path(..., description="معرف المؤسسة"),
    db: Session = Depends(get_db),
    current_user: Dict[str, Any] = Depends(get_current_active_user),
):
    """
    استرجاع معلومات مؤسسة محددة
    """
    # التحقق من الصلاحيات
    permission_service = PermissionService(db)
    if not permission_service.has_permission(
        current_user["id"], "organizations", "read"
    ):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail=ACCESS_DENIED_MESSAGE
        )

    user_service = UserService(db)
    organization = user_service.get_organization_with_details(org_id)
    if not organization:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="المؤسسة غير موجودة"
        )
    return organization


@router.get(
    "/organizations/{org_id}/branches", response_model=List[OrganizationResponse]
)
async def read_organization_branches(
    org_id: str = Path(..., description="معرف المؤسسة"),
    db: Session = Depends(get_db),
    current_user: Dict[str, Any] = Depends(get_current_active_user),
):
    """
    استرجاع فروع مؤسسة محددة
    """
    # التحقق من الصلاحيات
    permission_service = PermissionService(db)
    if not permission_service.has_permission(
        current_user["id"], "organizations", "read"
    ):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail=ACCESS_DENIED_MESSAGE
        )

    user_service = UserService(db)
    branches = user_service.get_organization_branches(org_id)
    return branches


@router.put("/organizations/{org_id}", response_model=OrganizationResponse)
async def update_organization(
    org_id: str = Path(..., description="معرف المؤسسة"),
    org_data: OrganizationUpdate = Body(...),
    db: Session = Depends(get_db),
    current_user: Dict[str, Any] = Depends(get_current_admin_user),
):
    """
    تحديث معلومات مؤسسة (للمسؤولين فقط)
    """
    user_service = UserService(db)
    organization = user_service.update_organization(
        org_id, org_data, current_user["id"]
    )
    if not organization:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="المؤسسة غير موجودة"
        )
    return organization


@router.delete("/organizations/{org_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_organization(
    org_id: str = Path(..., description="معرف المؤسسة"),
    db: Session = Depends(get_db),
    current_user: Dict[str, Any] = Depends(get_current_admin_user),
):
    """
    حذف مؤسسة (للمسؤولين فقط)
    """
    user_service = UserService(db)
    result = user_service.delete_organization(org_id)
    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="المؤسسة غير موجودة"
        )
    return None


# تصدير الموجه
__all__ = ["router"]
