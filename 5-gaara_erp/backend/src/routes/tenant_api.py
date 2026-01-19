"""
Tenant API Routes - Flask Blueprint
مسارات API للمستأجر - Flask Blueprint

RESTful API endpoints for multi-tenancy management.

Author: Global v35.0 Singularity
Version: 1.0.0
Created: 2026-01-17
"""

from __future__ import annotations

import logging
from functools import wraps
from datetime import datetime, timedelta
from typing import Optional, Dict, Any

from flask import Blueprint, request, jsonify, g, current_app
from sqlalchemy import or_

logger = logging.getLogger(__name__)

# Create Blueprint
tenant_bp = Blueprint('tenant', __name__, url_prefix='/api/tenants')


# =============================================================================
# Helper Functions
# =============================================================================

def get_db():
    """Get database session."""
    try:
        from src.models.user import db
        return db
    except ImportError:
        return None


def get_models():
    """Import tenant models."""
    try:
        from src.models.tenant_sqlalchemy import (
            Tenant, TenantPlan, TenantUser, TenantSettings, TenantInvitation
        )
        return Tenant, TenantPlan, TenantUser, TenantSettings, TenantInvitation
    except ImportError as e:
        logger.error(f"Failed to import tenant models: {e}")
        return None, None, None, None, None


def success_response(data: Any = None, message: str = '', message_ar: str = '', status: int = 200):
    """Create standardized success response."""
    response = {
        'success': True,
        'message': message,
        'message_ar': message_ar
    }
    if data is not None:
        response['data'] = data
    return jsonify(response), status


def error_response(error: str, message: str, message_ar: str = '', status: int = 400):
    """Create standardized error response."""
    return jsonify({
        'success': False,
        'error': error,
        'message': message,
        'message_ar': message_ar or message
    }), status


def require_auth(f):
    """Decorator to require authentication."""
    @wraps(f)
    def decorated(*args, **kwargs):
        # Check for user in g (set by auth middleware)
        if not hasattr(g, 'user') or g.user is None:
            # Try to get from session or JWT
            try:
                from auth import AuthManager
                auth = AuthManager()
                user = auth.get_current_user()
                if user:
                    g.user = user
                else:
                    return error_response('UNAUTHORIZED', 'Authentication required',
                                          'المصادقة مطلوبة', 401)
            except Exception:
                return error_response('UNAUTHORIZED', 'Authentication required',
                                      'المصادقة مطلوبة', 401)
        return f(*args, **kwargs)
    return decorated


def require_tenant_admin(f):
    """Decorator to require tenant admin role."""
    @wraps(f)
    @require_auth
    def decorated(*args, **kwargs):
        tenant_id = kwargs.get('tenant_id')
        if not tenant_id:
            return error_response('BAD_REQUEST', 'Tenant ID required', 'معرف المستأجر مطلوب', 400)

        _, _, TenantUser, _, _ = get_models()
        if not TenantUser:
            return error_response('SERVER_ERROR', 'Models not available', 'النماذج غير متاحة', 500)

        db = get_db()
        membership = db.session.query(TenantUser).filter_by(
            tenant_id=tenant_id,
            user_id=g.user.id,
            is_active=True
        ).first()

        if not membership or membership.role not in ['owner', 'admin']:
            return error_response('FORBIDDEN', 'Admin access required',
                                  'صلاحيات المدير مطلوبة', 403)

        g.tenant_membership = membership
        return f(*args, **kwargs)
    return decorated


# =============================================================================
# Tenant CRUD Routes
# =============================================================================

@tenant_bp.route('/', methods=['GET'])
@require_auth
def list_tenants():
    """
    قائمة المستأجرين
    List all tenants the user has access to.

    Returns:
        JSON list of tenants with basic info
    """
    Tenant, _, TenantUser, _, _ = get_models()
    if not Tenant:
        return error_response('SERVER_ERROR', 'Models not available', 'النماذج غير متاحة', 500)

    db = get_db()

    try:
        # Get user's tenant memberships
        if hasattr(g.user, 'is_superuser') and g.user.is_superuser:
            # Superuser sees all
            tenants = db.session.query(Tenant).filter_by(is_active=True).all()
        else:
            # Regular user sees their tenants
            memberships = db.session.query(TenantUser).filter_by(
                user_id=g.user.id,
                is_active=True
            ).all()
            tenant_ids = [m.tenant_id for m in memberships]
            tenants = db.session.query(Tenant).filter(
                Tenant.id.in_(tenant_ids),
                Tenant.is_active == True
            ).all()

        data = [t.to_dict(include_stats=True) for t in tenants]

        return success_response(
            data=data,
            message=f'Found {len(data)} tenants',
            message_ar=f'تم العثور على {len(data)} مستأجر'
        )

    except Exception as e:
        logger.error(f"Error listing tenants: {e}", exc_info=True)
        return error_response('LIST_ERROR', str(e), 'خطأ في جلب القائمة', 500)


@tenant_bp.route('/', methods=['POST'])
@require_auth
def create_tenant():
    """
    إنشاء مستأجر جديد
    Create a new tenant.

    Request Body:
        - name: Organization name (required)
        - slug: URL-safe identifier (required)
        - name_ar: Arabic name (optional)
        - plan_code: Subscription plan (optional, default: 'basic')
        - custom_domain: Custom domain (optional)

    Returns:
        Created tenant data
    """
    Tenant, TenantPlan, TenantUser, TenantSettings, _ = get_models()
    if not Tenant:
        return error_response('SERVER_ERROR', 'Models not available', 'النماذج غير متاحة', 500)

    db = get_db()
    data = request.get_json() or {}

    # Validate required fields
    name = data.get('name', '').strip()
    slug = data.get('slug', '').strip().lower()

    if not name:
        return error_response('VALIDATION_ERROR', 'Name is required', 'الاسم مطلوب', 400)

    if not slug:
        return error_response('VALIDATION_ERROR', 'Slug is required', 'المعرف الفريد مطلوب', 400)

    # Validate slug format
    import re
    if not re.match(r'^[a-z0-9]+(?:-[a-z0-9]+)*$', slug):
        return error_response('VALIDATION_ERROR',
                              'Slug must contain only lowercase letters, numbers, and hyphens',
                              'المعرف يجب أن يحتوي على حروف صغيرة وأرقام وشرطات فقط', 400)

    try:
        # Check slug uniqueness
        existing = db.session.query(Tenant).filter_by(slug=slug).first()
        if existing:
            return error_response('TENANT_EXISTS', f"Tenant with slug '{slug}' already exists",
                                  f"المستأجر '{slug}' موجود مسبقاً", 409)

        # Check custom domain uniqueness
        custom_domain = data.get('custom_domain', '').strip() or None
        if custom_domain:
            existing_domain = db.session.query(Tenant).filter_by(custom_domain=custom_domain).first()
            if existing_domain:
                return error_response('DOMAIN_EXISTS', 'Custom domain already in use',
                                      'النطاق المخصص مستخدم مسبقاً', 409)

        # Get plan
        plan_code = data.get('plan_code', 'basic')
        plan = db.session.query(TenantPlan).filter_by(code=plan_code, is_active=True).first()

        # Calculate trial end
        trial_days = data.get('trial_days', 14)
        trial_ends_at = datetime.utcnow() + timedelta(days=trial_days)

        # Create tenant
        tenant = Tenant(
            name=name,
            name_ar=data.get('name_ar', name),
            slug=slug,
            schema_name=f"tenant_{slug.replace('-', '_')}",
            custom_domain=custom_domain,
            plan_id=plan.id if plan else None,
            owner_id=g.user.id,
            status='trial',
            trial_ends_at=trial_ends_at,
            settings={
                'timezone': 'Asia/Riyadh',
                'language': 'ar',
                'currency': 'SAR'
            }
        )

        db.session.add(tenant)
        db.session.flush()  # Get tenant ID

        # Create default settings
        settings = TenantSettings(
            tenant_id=tenant.id,
            modules_enabled=['core', 'accounting', 'inventory', 'sales', 'purchasing']
        )
        db.session.add(settings)

        # Add owner as TenantUser
        owner_membership = TenantUser(
            tenant_id=tenant.id,
            user_id=g.user.id,
            role='owner',
            is_primary=True
        )
        db.session.add(owner_membership)

        db.session.commit()

        logger.info(f"Created tenant: {tenant.slug} by user {g.user.id}")

        return success_response(
            data=tenant.to_dict(include_stats=True),
            message='Tenant created successfully',
            message_ar='تم إنشاء المستأجر بنجاح',
            status=201
        )

    except Exception as e:
        db.session.rollback()
        logger.error(f"Error creating tenant: {e}", exc_info=True)
        return error_response('CREATE_ERROR', str(e), 'خطأ في إنشاء المستأجر', 500)


@tenant_bp.route('/<tenant_id>', methods=['GET'])
@require_auth
def get_tenant(tenant_id: str):
    """
    تفاصيل المستأجر
    Get tenant details by ID.
    """
    Tenant, _, TenantUser, _, _ = get_models()
    if not Tenant:
        return error_response('SERVER_ERROR', 'Models not available', 'النماذج غير متاحة', 500)

    db = get_db()

    try:
        tenant = db.session.query(Tenant).filter_by(id=tenant_id).first()
        if not tenant:
            return error_response('NOT_FOUND', 'Tenant not found', 'المستأجر غير موجود', 404)

        # Check access permission
        if not (hasattr(g.user, 'is_superuser') and g.user.is_superuser):
            membership = db.session.query(TenantUser).filter_by(
                tenant_id=tenant_id,
                user_id=g.user.id,
                is_active=True
            ).first()
            if not membership:
                return error_response('FORBIDDEN', 'Access denied', 'الوصول مرفوض', 403)

        return success_response(data=tenant.to_dict(include_plan=True, include_stats=True))

    except Exception as e:
        logger.error(f"Error getting tenant: {e}", exc_info=True)
        return error_response('GET_ERROR', str(e), 'خطأ في جلب المستأجر', 500)


@tenant_bp.route('/<tenant_id>', methods=['PUT'])
@require_tenant_admin
def update_tenant(tenant_id: str):
    """
    تحديث المستأجر
    Update tenant information.
    """
    Tenant, _, _, _, _ = get_models()
    if not Tenant:
        return error_response('SERVER_ERROR', 'Models not available', 'النماذج غير متاحة', 500)

    db = get_db()
    data = request.get_json() or {}

    try:
        tenant = db.session.query(Tenant).filter_by(id=tenant_id).first()
        if not tenant:
            return error_response('NOT_FOUND', 'Tenant not found', 'المستأجر غير موجود', 404)

        # Update allowed fields
        allowed_fields = ['name', 'name_ar', 'logo', 'custom_domain']
        for field in allowed_fields:
            if field in data:
                setattr(tenant, field, data[field])

        # Update settings if provided
        if 'settings' in data and isinstance(data['settings'], dict):
            tenant.settings = {**(tenant.settings or {}), **data['settings']}

        db.session.commit()

        logger.info(f"Updated tenant: {tenant.slug}")

        return success_response(
            data=tenant.to_dict(),
            message='Tenant updated successfully',
            message_ar='تم تحديث المستأجر بنجاح'
        )

    except Exception as e:
        db.session.rollback()
        logger.error(f"Error updating tenant: {e}", exc_info=True)
        return error_response('UPDATE_ERROR', str(e), 'خطأ في تحديث المستأجر', 500)


@tenant_bp.route('/<tenant_id>', methods=['DELETE'])
@require_tenant_admin
def delete_tenant(tenant_id: str):
    """
    حذف المستأجر (تعطيل)
    Deactivate tenant (soft delete).
    """
    Tenant, _, TenantUser, _, _ = get_models()
    if not Tenant:
        return error_response('SERVER_ERROR', 'Models not available', 'النماذج غير متاحة', 500)

    db = get_db()

    try:
        tenant = db.session.query(Tenant).filter_by(id=tenant_id).first()
        if not tenant:
            return error_response('NOT_FOUND', 'Tenant not found', 'المستأجر غير موجود', 404)

        # Only owner can delete
        if g.tenant_membership.role != 'owner':
            return error_response('FORBIDDEN', 'Only owner can delete tenant',
                                  'المالك فقط يمكنه حذف المستأجر', 403)

        # Soft delete
        reason = request.get_json().get('reason', 'User requested') if request.get_json() else 'User requested'
        tenant.is_active = False
        tenant.status = 'cancelled'
        tenant.metadata = {**(tenant.metadata or {}), 'deactivation_reason': reason,
                          'deactivated_at': datetime.utcnow().isoformat()}

        db.session.commit()

        logger.info(f"Deactivated tenant: {tenant.slug}, reason: {reason}")

        return success_response(
            message='Tenant deactivated successfully',
            message_ar='تم تعطيل المستأجر بنجاح'
        )

    except Exception as e:
        db.session.rollback()
        logger.error(f"Error deleting tenant: {e}", exc_info=True)
        return error_response('DELETE_ERROR', str(e), 'خطأ في حذف المستأجر', 500)


# =============================================================================
# Tenant Users Routes
# =============================================================================

@tenant_bp.route('/<tenant_id>/users', methods=['GET'])
@require_auth
def list_tenant_users(tenant_id: str):
    """
    قائمة مستخدمي المستأجر
    List all users in a tenant.
    """
    Tenant, _, TenantUser, _, _ = get_models()
    if not TenantUser:
        return error_response('SERVER_ERROR', 'Models not available', 'النماذج غير متاحة', 500)

    db = get_db()

    try:
        # Check access
        membership = db.session.query(TenantUser).filter_by(
            tenant_id=tenant_id,
            user_id=g.user.id,
            is_active=True
        ).first()

        if not membership:
            return error_response('FORBIDDEN', 'Access denied', 'الوصول مرفوض', 403)

        users = db.session.query(TenantUser).filter_by(
            tenant_id=tenant_id,
            is_active=True
        ).order_by(TenantUser.role, TenantUser.joined_at).all()

        data = [u.to_dict(include_user=True) for u in users]

        return success_response(data=data)

    except Exception as e:
        logger.error(f"Error listing tenant users: {e}", exc_info=True)
        return error_response('LIST_ERROR', str(e), 'خطأ في جلب المستخدمين', 500)


@tenant_bp.route('/<tenant_id>/users', methods=['POST'])
@require_tenant_admin
def add_tenant_user(tenant_id: str):
    """
    إضافة مستخدم للمستأجر
    Add a user to tenant.
    """
    Tenant, TenantPlan, TenantUser, _, _ = get_models()
    if not TenantUser:
        return error_response('SERVER_ERROR', 'Models not available', 'النماذج غير متاحة', 500)

    db = get_db()
    data = request.get_json() or {}

    user_id = data.get('user_id')
    if not user_id:
        return error_response('VALIDATION_ERROR', 'user_id is required', 'معرف المستخدم مطلوب', 400)

    try:
        tenant = db.session.query(Tenant).filter_by(id=tenant_id).first()
        if not tenant:
            return error_response('NOT_FOUND', 'Tenant not found', 'المستأجر غير موجود', 404)

        # Check user quota
        if tenant.plan:
            current_users = db.session.query(TenantUser).filter_by(
                tenant_id=tenant_id,
                is_active=True
            ).count()
            if current_users >= tenant.plan.max_users:
                return error_response('QUOTA_EXCEEDED',
                                      f'User limit reached ({tenant.plan.max_users})',
                                      f'تم الوصول للحد الأقصى ({tenant.plan.max_users})', 403)

        # Check if already member
        existing = db.session.query(TenantUser).filter_by(
            tenant_id=tenant_id,
            user_id=user_id
        ).first()

        if existing:
            if existing.is_active:
                return error_response('ALREADY_MEMBER', 'User is already a member',
                                      'المستخدم عضو بالفعل', 409)
            else:
                # Reactivate
                existing.is_active = True
                existing.role = data.get('role', 'member')
                db.session.commit()
                return success_response(
                    data=existing.to_dict(include_user=True),
                    message='User reactivated',
                    message_ar='تم إعادة تفعيل المستخدم'
                )

        # Create new membership
        new_member = TenantUser(
            tenant_id=tenant_id,
            user_id=user_id,
            role=data.get('role', 'member'),
            permissions=data.get('permissions', {})
        )
        db.session.add(new_member)
        db.session.commit()

        logger.info(f"Added user {user_id} to tenant {tenant_id}")

        return success_response(
            data=new_member.to_dict(include_user=True),
            message='User added successfully',
            message_ar='تم إضافة المستخدم بنجاح',
            status=201
        )

    except Exception as e:
        db.session.rollback()
        logger.error(f"Error adding user: {e}", exc_info=True)
        return error_response('ADD_ERROR', str(e), 'خطأ في إضافة المستخدم', 500)


@tenant_bp.route('/<tenant_id>/users/<user_id>', methods=['PUT'])
@require_tenant_admin
def update_tenant_user(tenant_id: str, user_id: str):
    """
    تحديث مستخدم المستأجر
    Update tenant user role/permissions.
    """
    _, _, TenantUser, _, _ = get_models()
    if not TenantUser:
        return error_response('SERVER_ERROR', 'Models not available', 'النماذج غير متاحة', 500)

    db = get_db()
    data = request.get_json() or {}

    try:
        tenant_user = db.session.query(TenantUser).filter_by(
            tenant_id=tenant_id,
            user_id=user_id
        ).first()

        if not tenant_user:
            return error_response('NOT_FOUND', 'User not found in tenant',
                                  'المستخدم غير موجود في المستأجر', 404)

        # Cannot change owner's role
        if tenant_user.role == 'owner':
            return error_response('FORBIDDEN', 'Cannot modify owner',
                                  'لا يمكن تعديل المالك', 403)

        # Update fields
        if 'role' in data:
            tenant_user.role = data['role']
        if 'permissions' in data:
            tenant_user.permissions = data['permissions']
        if 'is_active' in data:
            tenant_user.is_active = data['is_active']

        db.session.commit()

        return success_response(
            data=tenant_user.to_dict(include_user=True),
            message='User updated',
            message_ar='تم تحديث المستخدم'
        )

    except Exception as e:
        db.session.rollback()
        logger.error(f"Error updating user: {e}", exc_info=True)
        return error_response('UPDATE_ERROR', str(e), 'خطأ في تحديث المستخدم', 500)


@tenant_bp.route('/<tenant_id>/users/<user_id>', methods=['DELETE'])
@require_tenant_admin
def remove_tenant_user(tenant_id: str, user_id: str):
    """
    إزالة مستخدم من المستأجر
    Remove user from tenant.
    """
    _, _, TenantUser, _, _ = get_models()
    if not TenantUser:
        return error_response('SERVER_ERROR', 'Models not available', 'النماذج غير متاحة', 500)

    db = get_db()

    try:
        tenant_user = db.session.query(TenantUser).filter_by(
            tenant_id=tenant_id,
            user_id=user_id
        ).first()

        if not tenant_user:
            return error_response('NOT_FOUND', 'User not found', 'المستخدم غير موجود', 404)

        if tenant_user.role == 'owner':
            return error_response('FORBIDDEN', 'Cannot remove owner',
                                  'لا يمكن إزالة المالك', 403)

        db.session.delete(tenant_user)
        db.session.commit()

        logger.info(f"Removed user {user_id} from tenant {tenant_id}")

        return success_response(
            message='User removed successfully',
            message_ar='تم إزالة المستخدم بنجاح'
        )

    except Exception as e:
        db.session.rollback()
        logger.error(f"Error removing user: {e}", exc_info=True)
        return error_response('REMOVE_ERROR', str(e), 'خطأ في إزالة المستخدم', 500)


# =============================================================================
# Tenant Settings Routes
# =============================================================================

@tenant_bp.route('/<tenant_id>/settings', methods=['GET'])
@require_auth
def get_tenant_settings(tenant_id: str):
    """
    إعدادات المستأجر
    Get tenant settings.
    """
    Tenant, _, TenantUser, TenantSettings, _ = get_models()
    if not TenantSettings:
        return error_response('SERVER_ERROR', 'Models not available', 'النماذج غير متاحة', 500)

    db = get_db()

    try:
        # Check access
        membership = db.session.query(TenantUser).filter_by(
            tenant_id=tenant_id,
            user_id=g.user.id,
            is_active=True
        ).first()

        if not membership:
            return error_response('FORBIDDEN', 'Access denied', 'الوصول مرفوض', 403)

        settings = db.session.query(TenantSettings).filter_by(tenant_id=tenant_id).first()

        if not settings:
            return error_response('NOT_FOUND', 'Settings not found', 'الإعدادات غير موجودة', 404)

        return success_response(data=settings.to_dict())

    except Exception as e:
        logger.error(f"Error getting settings: {e}", exc_info=True)
        return error_response('GET_ERROR', str(e), 'خطأ في جلب الإعدادات', 500)


@tenant_bp.route('/<tenant_id>/settings', methods=['PUT'])
@require_tenant_admin
def update_tenant_settings(tenant_id: str):
    """
    تحديث إعدادات المستأجر
    Update tenant settings.
    """
    _, _, _, TenantSettings, _ = get_models()
    if not TenantSettings:
        return error_response('SERVER_ERROR', 'Models not available', 'النماذج غير متاحة', 500)

    db = get_db()
    data = request.get_json() or {}

    try:
        settings = db.session.query(TenantSettings).filter_by(tenant_id=tenant_id).first()

        if not settings:
            settings = TenantSettings(tenant_id=tenant_id)
            db.session.add(settings)

        # Update allowed fields
        allowed_fields = [
            'timezone', 'language', 'secondary_language',
            'date_format', 'time_format', 'currency', 'currency_symbol',
            'fiscal_year_start_month', 'modules_enabled',
            'theme_settings', 'notification_settings', 'security_settings'
        ]

        for field in allowed_fields:
            if field in data:
                setattr(settings, field, data[field])

        db.session.commit()

        return success_response(
            data=settings.to_dict(),
            message='Settings updated',
            message_ar='تم تحديث الإعدادات'
        )

    except Exception as e:
        db.session.rollback()
        logger.error(f"Error updating settings: {e}", exc_info=True)
        return error_response('UPDATE_ERROR', str(e), 'خطأ في تحديث الإعدادات', 500)


# =============================================================================
# Plans Route
# =============================================================================

@tenant_bp.route('/plans', methods=['GET'])
def list_plans():
    """
    قائمة خطط الاشتراك
    List available subscription plans.
    """
    _, TenantPlan, _, _, _ = get_models()
    if not TenantPlan:
        return error_response('SERVER_ERROR', 'Models not available', 'النماذج غير متاحة', 500)

    db = get_db()

    try:
        plans = db.session.query(TenantPlan).filter_by(is_active=True).order_by(
            TenantPlan.price_monthly
        ).all()

        data = [p.to_dict() for p in plans]

        return success_response(data=data)

    except Exception as e:
        logger.error(f"Error listing plans: {e}", exc_info=True)
        return error_response('LIST_ERROR', str(e), 'خطأ في جلب الخطط', 500)


# =============================================================================
# Utility Routes
# =============================================================================

@tenant_bp.route('/check-slug', methods=['GET'])
def check_slug_availability():
    """
    التحقق من توفر المعرف
    Check if slug is available.
    """
    Tenant, _, _, _, _ = get_models()
    if not Tenant:
        return error_response('SERVER_ERROR', 'Models not available', 'النماذج غير متاحة', 500)

    db = get_db()
    slug = request.args.get('slug', '').strip().lower()

    if not slug:
        return error_response('VALIDATION_ERROR', 'Slug is required', 'المعرف مطلوب', 400)

    try:
        existing = db.session.query(Tenant).filter_by(slug=slug).first()
        available = existing is None

        return success_response(data={
            'slug': slug,
            'available': available
        })

    except Exception as e:
        logger.error(f"Error checking slug: {e}", exc_info=True)
        return error_response('CHECK_ERROR', str(e), 'خطأ في التحقق', 500)


# =============================================================================
# Statistics Route
# =============================================================================

@tenant_bp.route('/stats', methods=['GET'])
@require_auth
def get_tenant_stats():
    """
    إحصائيات المستأجرين
    Get tenant statistics (admin only).
    """
    if not (hasattr(g.user, 'is_superuser') and g.user.is_superuser):
        return error_response('FORBIDDEN', 'Admin access required', 'صلاحيات المدير مطلوبة', 403)

    Tenant, TenantPlan, TenantUser, _, _ = get_models()
    if not Tenant:
        return error_response('SERVER_ERROR', 'Models not available', 'النماذج غير متاحة', 500)

    db = get_db()

    try:
        total_tenants = db.session.query(Tenant).count()
        active_tenants = db.session.query(Tenant).filter_by(status='active', is_active=True).count()
        trial_tenants = db.session.query(Tenant).filter_by(status='trial', is_active=True).count()
        total_users = db.session.query(TenantUser).filter_by(is_active=True).count()

        return success_response(data={
            'total_tenants': total_tenants,
            'active_tenants': active_tenants,
            'trial_tenants': trial_tenants,
            'suspended_tenants': total_tenants - active_tenants - trial_tenants,
            'total_tenant_users': total_users
        })

    except Exception as e:
        logger.error(f"Error getting stats: {e}", exc_info=True)
        return error_response('STATS_ERROR', str(e), 'خطأ في الإحصائيات', 500)
