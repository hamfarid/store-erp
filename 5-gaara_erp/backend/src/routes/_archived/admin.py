"""
Admin Routes - Role & Permission Management API

This module provides API endpoints for managing roles, permissions, and system setup.
"""

from flask import Blueprint, request, jsonify, g
from functools import wraps
from datetime import datetime

from src.database import db
from src.models.admin import (
    Role,
    Permission,
    SystemSetup,
    role_permissions,
    user_roles,
    seed_permissions_and_roles,
    DEFAULT_PERMISSIONS,
    DEFAULT_ROLES,
)
from src.models.audit_log import AuditLog
from src.models.user import User

admin_bp = Blueprint("admin", __name__, url_prefix="/api/admin")


# ============================================================================
# Decorators
# ============================================================================


def require_permission(permission_code):
    """Decorator to require a specific permission."""

    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            user = getattr(g, "current_user", None)
            if not user:
                return jsonify({"error": "Authentication required"}), 401

            # Super admin has all permissions
            if hasattr(user, "roles"):
                for role in user.roles:
                    if role.code == "super_admin":
                        return f(*args, **kwargs)
                    if role.has_permission(permission_code):
                        return f(*args, **kwargs)

            return jsonify({"error": "Permission denied"}), 403

        return decorated_function

    return decorator


def log_action(action, resource_type, resource_id=None, details=None):
    """Log an admin action."""
    user = getattr(g, "current_user", None)
    log = AuditLog(
        user_id=user.id if user else None,
        action=action,
        resource_type=resource_type,
        resource_id=resource_id,
        details=details,
        ip_address=request.remote_addr,
        user_agent=request.user_agent.string[:500] if request.user_agent else None,
    )
    db.session.add(log)
    db.session.commit()


# ============================================================================
# Setup Routes
# ============================================================================


@admin_bp.route("/setup/status", methods=["GET"])
def get_setup_status():
    """Get system setup status."""
    setup = SystemSetup.query.first()
    if not setup:
        setup = SystemSetup()
        db.session.add(setup)
        db.session.commit()

    return jsonify({"success": True, "data": setup.to_dict()})


@admin_bp.route("/setup/init", methods=["POST"])
def init_setup():
    """Initialize system with default data."""
    try:
        # Seed permissions and roles
        seed_permissions_and_roles()

        # Update setup status
        setup = SystemSetup.query.first()
        if not setup:
            setup = SystemSetup()
            db.session.add(setup)

        setup.setup_step = 1
        db.session.commit()

        return jsonify(
            {
                "success": True,
                "message": "System initialized successfully",
                "data": setup.to_dict(),
            }
        )
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500


@admin_bp.route("/setup/company", methods=["POST"])
def setup_company():
    """Save company information."""
    data = request.get_json()

    setup = SystemSetup.query.first()
    if not setup:
        setup = SystemSetup()
        db.session.add(setup)

    # Update company info
    setup.company_name = data.get("company_name")
    setup.company_name_ar = data.get("company_name_ar")
    setup.company_email = data.get("company_email")
    setup.company_phone = data.get("company_phone")
    setup.company_address = data.get("company_address")
    setup.tax_number = data.get("tax_number")
    setup.commercial_register = data.get("commercial_register")
    setup.currency = data.get("currency", "SAR")
    setup.timezone = data.get("timezone", "Asia/Riyadh")
    setup.language = data.get("language", "ar")
    setup.fiscal_year_start = data.get("fiscal_year_start", 1)
    setup.setup_step = 2

    db.session.commit()
    log_action("setup", "company", details=data)

    return jsonify(
        {
            "success": True,
            "message": "Company information saved",
            "data": setup.to_dict(),
        }
    )


@admin_bp.route("/setup/admin", methods=["POST"])
def setup_admin():
    """Create initial admin user."""
    data = request.get_json()

    # Validate required fields
    required = ["username", "email", "password", "name"]
    for field in required:
        if not data.get(field):
            return jsonify({"error": f"{field} is required"}), 400

    # Check if admin already exists
    existing = User.query.filter(
        (User.username == data["username"]) | (User.email == data["email"])
    ).first()
    if existing:
        return jsonify({"error": "User already exists"}), 400

    try:
        # Create admin user
        user = User(
            username=data["username"],
            email=data["email"],
            name=data["name"],
            phone=data.get("phone"),
            is_active=True,
        )
        user.set_password(data["password"])
        db.session.add(user)
        db.session.flush()

        # Assign super_admin role
        super_admin_role = Role.query.filter_by(code="super_admin").first()
        if super_admin_role:
            user.roles = [super_admin_role]

        # Update setup
        setup = SystemSetup.query.first()
        if setup:
            setup.admin_created = True
            setup.setup_step = 3

        db.session.commit()
        log_action("create", "admin_user", user.id, {"username": user.username})

        return jsonify(
            {
                "success": True,
                "message": "Admin user created",
                "data": {"user_id": user.id},
            }
        )
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500


@admin_bp.route("/setup/complete", methods=["POST"])
def complete_setup():
    """Mark setup as complete."""
    setup = SystemSetup.query.first()
    if setup:
        setup.is_completed = True
        setup.setup_step = 4
        db.session.commit()
        log_action("complete", "setup")

    return jsonify(
        {
            "success": True,
            "message": "Setup completed",
            "data": setup.to_dict() if setup else None,
        }
    )


# ============================================================================
# Permission Routes
# ============================================================================


@admin_bp.route("/permissions", methods=["GET"])
@require_permission("roles.view")
def get_permissions():
    """Get all permissions grouped by module."""
    permissions = Permission.query.filter_by(is_active=True).all()

    # Group by module
    grouped = {}
    for perm in permissions:
        if perm.module not in grouped:
            grouped[perm.module] = []
        grouped[perm.module].append(perm.to_dict())

    return jsonify(
        {
            "success": True,
            "data": {
                "permissions": [p.to_dict() for p in permissions],
                "grouped": grouped,
                "modules": list(grouped.keys()),
            },
        }
    )


# ============================================================================
# Role Routes
# ============================================================================


@admin_bp.route("/roles", methods=["GET"])
@require_permission("roles.view")
def get_roles():
    """Get all roles."""
    roles = Role.query.filter_by(is_active=True).order_by(Role.priority.desc()).all()

    return jsonify(
        {"success": True, "data": [r.to_dict(include_permissions=True) for r in roles]}
    )


@admin_bp.route("/roles/<int:role_id>", methods=["GET"])
@require_permission("roles.view")
def get_role(role_id):
    """Get a specific role."""
    role = Role.query.get_or_404(role_id)

    return jsonify({"success": True, "data": role.to_dict(include_permissions=True)})


@admin_bp.route("/roles", methods=["POST"])
@require_permission("roles.create")
def create_role():
    """Create a new role."""
    data = request.get_json()

    # Validate
    if not data.get("code") or not data.get("name"):
        return jsonify({"error": "Code and name are required"}), 400

    if Role.query.filter_by(code=data["code"]).first():
        return jsonify({"error": "Role code already exists"}), 400

    try:
        role = Role(
            code=data["code"],
            name=data["name"],
            name_ar=data.get("name_ar", data["name"]),
            description=data.get("description"),
            description_ar=data.get("description_ar"),
            color=data.get("color", "blue"),
            icon=data.get("icon", "shield"),
            priority=data.get("priority", 0),
            created_by=g.current_user.id if hasattr(g, "current_user") else None,
        )

        # Assign permissions
        if data.get("permissions"):
            perms = Permission.query.filter(
                Permission.id.in_(data["permissions"])
            ).all()
            role.permissions = perms

        db.session.add(role)
        db.session.commit()
        log_action("create", "role", role.id, {"code": role.code})

        return (
            jsonify(
                {
                    "success": True,
                    "message": "Role created",
                    "data": role.to_dict(include_permissions=True),
                }
            ),
            201,
        )
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500


@admin_bp.route("/roles/<int:role_id>", methods=["PUT"])
@require_permission("roles.edit")
def update_role(role_id):
    """Update a role."""
    role = Role.query.get_or_404(role_id)

    if role.is_system:
        return jsonify({"error": "Cannot modify system roles"}), 400

    data = request.get_json()

    try:
        role.name = data.get("name", role.name)
        role.name_ar = data.get("name_ar", role.name_ar)
        role.description = data.get("description", role.description)
        role.description_ar = data.get("description_ar", role.description_ar)
        role.color = data.get("color", role.color)
        role.icon = data.get("icon", role.icon)
        role.priority = data.get("priority", role.priority)

        # Update permissions
        if "permissions" in data:
            perms = Permission.query.filter(
                Permission.id.in_(data["permissions"])
            ).all()
            role.permissions = perms

        db.session.commit()
        log_action("update", "role", role.id, data)

        return jsonify(
            {
                "success": True,
                "message": "Role updated",
                "data": role.to_dict(include_permissions=True),
            }
        )
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500


@admin_bp.route("/roles/<int:role_id>", methods=["DELETE"])
@require_permission("roles.delete")
def delete_role(role_id):
    """Delete a role."""
    role = Role.query.get_or_404(role_id)

    if role.is_system:
        return jsonify({"error": "Cannot delete system roles"}), 400

    try:
        log_action("delete", "role", role.id, {"code": role.code})
        db.session.delete(role)
        db.session.commit()

        return jsonify({"success": True, "message": "Role deleted"})
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500


# ============================================================================
# User-Role Assignment Routes
# ============================================================================


@admin_bp.route("/users/<int:user_id>/roles", methods=["GET"])
@require_permission("users.view")
def get_user_roles(user_id):
    """Get roles assigned to a user."""
    user = User.query.get_or_404(user_id)

    return jsonify(
        {
            "success": True,
            "data": {
                "user_id": user.id,
                "username": user.username,
                "roles": [r.to_dict() for r in user.roles],
            },
        }
    )


@admin_bp.route("/users/<int:user_id>/roles", methods=["PUT"])
@require_permission("roles.assign")
def assign_user_roles(user_id):
    """Assign roles to a user."""
    user = User.query.get_or_404(user_id)
    data = request.get_json()

    try:
        role_ids = data.get("role_ids", [])
        roles = Role.query.filter(Role.id.in_(role_ids)).all()
        user.roles = roles

        db.session.commit()
        log_action("assign_roles", "user", user.id, {"role_ids": role_ids})

        return jsonify(
            {
                "success": True,
                "message": "Roles assigned",
                "data": {
                    "user_id": user.id,
                    "roles": [r.to_dict() for r in user.roles],
                },
            }
        )
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500


# ============================================================================
# Audit Log Routes
# ============================================================================


@admin_bp.route("/audit-logs", methods=["GET"])
@require_permission("admin.audit")
def get_audit_logs():
    """Get audit logs with pagination and filtering."""
    page = request.args.get("page", 1, type=int)
    per_page = request.args.get("per_page", 50, type=int)
    user_id = request.args.get("user_id", type=int)
    action = request.args.get("action")
    resource_type = request.args.get("resource_type")

    query = AuditLog.query.order_by(AuditLog.created_at.desc())

    if user_id:
        query = query.filter_by(user_id=user_id)
    if action:
        query = query.filter_by(action=action)
    if resource_type:
        query = query.filter_by(resource_type=resource_type)

    pagination = query.paginate(page=page, per_page=per_page, error_out=False)

    return jsonify(
        {
            "success": True,
            "data": {
                "logs": [log.to_dict() for log in pagination.items],
                "pagination": {
                    "page": pagination.page,
                    "per_page": pagination.per_page,
                    "total": pagination.total,
                    "pages": pagination.pages,
                },
            },
        }
    )


# ============================================================================
# Stats Routes
# ============================================================================


@admin_bp.route("/stats", methods=["GET"])
@require_permission("admin.view")
def get_admin_stats():
    """Get admin dashboard statistics."""
    return jsonify(
        {
            "success": True,
            "data": {
                "users": {
                    "total": User.query.count(),
                    "active": User.query.filter_by(is_active=True).count(),
                },
                "roles": {
                    "total": Role.query.count(),
                    "system": Role.query.filter_by(is_system=True).count(),
                },
                "permissions": {
                    "total": Permission.query.count(),
                    "modules": db.session.query(Permission.module).distinct().count(),
                },
                "audit_logs": {
                    "total": AuditLog.query.count(),
                    "today": AuditLog.query.filter(
                        AuditLog.created_at
                        >= datetime.utcnow().replace(hour=0, minute=0, second=0)
                    ).count(),
                },
            },
        }
    )


# ============================================================================
# Check Permission Route
# ============================================================================


@admin_bp.route("/check-permission", methods=["POST"])
def check_permission():
    """Check if current user has a specific permission."""
    data = request.get_json()
    permission_code = data.get("permission")

    if not permission_code:
        return jsonify({"error": "Permission code required"}), 400

    user = getattr(g, "current_user", None)
    if not user:
        return jsonify({"has_permission": False})

    has_permission = False
    if hasattr(user, "roles"):
        for role in user.roles:
            if role.code == "super_admin" or role.has_permission(permission_code):
                has_permission = True
                break

    return jsonify(
        {
            "success": True,
            "data": {"permission": permission_code, "has_permission": has_permission},
        }
    )
