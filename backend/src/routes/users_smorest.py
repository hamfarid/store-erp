# FILE: backend/src/routes/users_smorest.py | PURPOSE: P1.24 OpenAPI
# documented user management endpoints | OWNER: Backend
"""
P1.24: Users Management API with OpenAPI 3.0 documentation via flask-smorest
"""
from __future__ import annotations

try:
    from flask.views import MethodView
    from flask_smorest import Blueprint  # type: ignore
    from marshmallow import Schema, fields, validate

    SMOREST_AVAILABLE = True
except Exception:  # pragma: no cover - optional dependency
    Blueprint = None  # type: ignore
    MethodView = None  # type: ignore
    Schema = None  # type: ignore
    fields = None  # type: ignore
    SMOREST_AVAILABLE = False

users_smorest_bp = None

if SMOREST_AVAILABLE and Blueprint is not None:
    users_smorest_bp = Blueprint(
        "users_smorest",
        __name__,
        description="User Management API - إدارة المستخدمين والأدوار",
        url_prefix="/api",
    )

    # ========================================================================
    # Schemas
    # ========================================================================

    class RoleSchema(Schema):
        """Role information schema."""

        id = fields.Integer(dump_only=True, metadata={"example": 1})
        name = fields.String(
            required=True, metadata={"example": "admin", "description": "Role name"}
        )
        name_ar = fields.String(
            metadata={"example": "مدير", "description": "Arabic role name"}
        )
        description = fields.String(metadata={"example": "Full system access"})
        permissions = fields.List(
            fields.String(),
            metadata={"example": ["admin_full", "user_management_view"]},
        )
        is_system = fields.Boolean(
            metadata={"example": True, "description": "System role (cannot be deleted)"}
        )
        # Use String for datetime since to_dict() returns ISO format strings
        created_at = fields.String(
            dump_only=True, metadata={"example": "2025-01-01T00:00:00+00:00"}
        )

    class UserSchema(Schema):
        """User information schema."""

        id = fields.Integer(dump_only=True, metadata={"example": 1})
        username = fields.String(
            required=True,
            validate=validate.Length(min=3, max=50),
            metadata={"example": "ahmed_ali", "description": "Unique username"},
        )
        email = fields.Email(required=True, metadata={"example": "ahmed@example.com"})
        full_name = fields.String(
            metadata={"example": "أحمد علي", "description": "Full name"}
        )
        role = fields.String(metadata={"example": "admin"})
        role_id = fields.Integer(metadata={"example": 1})
        is_active = fields.Boolean(metadata={"example": True})
        # Use String for datetime since to_dict() returns ISO format strings
        last_login = fields.String(
            dump_only=True, metadata={"example": "2025-01-01T00:00:00+00:00"}
        )
        created_at = fields.String(
            dump_only=True, metadata={"example": "2025-01-01T00:00:00+00:00"}
        )
        updated_at = fields.String(
            dump_only=True, metadata={"example": "2025-01-01T00:00:00+00:00"}
        )

    class UserCreateSchema(Schema):
        """Schema for creating a new user."""

        username = fields.String(
            required=True,
            validate=validate.Length(min=3, max=50),
            metadata={
                "example": "new_user",
                "description": "Unique username (3-50 characters)",
            },
        )
        email = fields.Email(required=True, metadata={"example": "user@example.com"})
        password = fields.String(
            required=True,
            load_only=True,
            validate=validate.Length(min=8),
            metadata={
                "example": "SecurePass123!",
                "description": "Password (min 8 characters)",
            },
        )
        full_name = fields.String(metadata={"example": "محمد أحمد"})
        role_id = fields.Integer(
            metadata={"example": 2, "description": "Role ID to assign"}
        )
        is_active = fields.Boolean(load_default=True, metadata={"example": True})

    class UserUpdateSchema(Schema):
        """Schema for updating a user."""

        email = fields.Email(metadata={"example": "updated@example.com"})
        full_name = fields.String(metadata={"example": "أحمد محمد"})
        role_id = fields.Integer(metadata={"example": 2})
        is_active = fields.Boolean(metadata={"example": True})

    class UserListSchema(Schema):
        """Paginated user list response."""

        success = fields.Boolean(metadata={"example": True})
        data = fields.Nested(
            lambda: UserListDataSchema(), metadata={"description": "Paginated users"}
        )
        message = fields.String(metadata={"example": "Users retrieved successfully"})

    class UserListDataSchema(Schema):
        """User list data with pagination."""

        users = fields.List(fields.Nested(UserSchema))
        total = fields.Integer(metadata={"example": 50})
        page = fields.Integer(metadata={"example": 1})
        per_page = fields.Integer(metadata={"example": 10})
        pages = fields.Integer(metadata={"example": 5})

    class UserResponseSchema(Schema):
        """Single user response."""

        success = fields.Boolean(metadata={"example": True})
        data = fields.Nested(UserSchema)
        message = fields.String(metadata={"example": "User retrieved successfully"})

    class RoleListSchema(Schema):
        """Role list response."""

        success = fields.Boolean(metadata={"example": True})
        data = fields.List(fields.Nested(RoleSchema))
        message = fields.String(metadata={"example": "Roles retrieved successfully"})

    class ErrorSchema(Schema):
        """Standard error response."""

        success = fields.Boolean(metadata={"example": False})
        error = fields.String(metadata={"example": "Validation error"})
        code = fields.String(metadata={"example": "VALIDATION_ERROR"})
        details = fields.Dict(
            metadata={"example": {"username": ["Username already exists"]}}
        )

    # ========================================================================
    # Endpoints
    # ========================================================================

    @users_smorest_bp.route("/users")
    class UsersCollection(MethodView):
        """User collection endpoints."""

        @users_smorest_bp.arguments(
            Schema.from_dict(
                {
                    "page": fields.Integer(load_default=1),
                    "per_page": fields.Integer(load_default=10),
                    "search": fields.String(),
                    "role": fields.String(),
                    "is_active": fields.Boolean(),
                }
            )(),
            location="query",
        )
        @users_smorest_bp.response(200, UserListSchema)
        @users_smorest_bp.alt_response(401, schema=ErrorSchema)
        def get(self, args):
            """
            Get paginated list of users.

            Returns all users with optional filtering by search term, role, or status.
            Requires `user_management_view` permission.
            """
            from src.database import db
            from src.models.user import User

            page = args.get("page", 1)
            per_page = args.get("per_page", 10)
            search = args.get("search")
            role = args.get("role")
            is_active = args.get("is_active")

            query = User.query

            if search:
                query = query.filter(
                    db.or_(
                        User.username.ilike(f"%{search}%"),
                        User.email.ilike(f"%{search}%"),
                        User.full_name.ilike(f"%{search}%"),
                    )
                )

            if role:
                query = query.filter(User.role == role)

            if is_active is not None:
                query = query.filter(User.is_active == is_active)

            pagination = query.paginate(page=page, per_page=per_page, error_out=False)

            return {
                "success": True,
                "data": {
                    "users": [u.to_dict() for u in pagination.items],
                    "total": pagination.total,
                    "page": pagination.page,
                    "per_page": pagination.per_page,
                    "pages": pagination.pages,
                },
                "message": "تم استرجاع المستخدمين بنجاح",
            }

        @users_smorest_bp.arguments(UserCreateSchema)
        @users_smorest_bp.response(201, UserResponseSchema)
        @users_smorest_bp.alt_response(400, schema=ErrorSchema)
        @users_smorest_bp.alt_response(409, schema=ErrorSchema)
        def post(self, json_data):
            """
            Create a new user.

            Creates a new user account with the specified details.
            Requires `user_management_add` permission.
            """
            from src.database import db
            from src.models.user import User

            # Check if username exists
            if User.query.filter_by(username=json_data["username"]).first():
                return {
                    "success": False,
                    "error": "Username already exists",
                    "code": "DUPLICATE_USERNAME",
                }, 409

            # Check if email exists
            if User.query.filter_by(email=json_data["email"]).first():
                return {
                    "success": False,
                    "error": "Email already exists",
                    "code": "DUPLICATE_EMAIL",
                }, 409

            user = User(
                username=json_data["username"],
                email=json_data["email"],
                full_name=json_data.get("full_name"),
                role_id=json_data.get("role_id"),
                is_active=json_data.get("is_active", True),
            )
            user.set_password(json_data["password"])

            db.session.add(user)
            db.session.commit()

            return {
                "success": True,
                "data": user.to_dict(),
                "message": "تم إنشاء المستخدم بنجاح",
            }, 201

    @users_smorest_bp.route("/users/<int:user_id>")
    class UserResource(MethodView):
        """Single user resource endpoints."""

        @users_smorest_bp.response(200, UserResponseSchema)
        @users_smorest_bp.alt_response(404, schema=ErrorSchema)
        def get(self, user_id):
            """
            Get user by ID.

            Returns detailed information about a specific user.
            Requires `user_management_view` permission.
            """
            from src.models.user import User

            user = User.query.get(user_id)
            if not user:
                return {
                    "success": False,
                    "error": "User not found",
                    "code": "NOT_FOUND",
                }, 404

            return {
                "success": True,
                "data": user.to_dict(),
                "message": "تم استرجاع المستخدم بنجاح",
            }

        @users_smorest_bp.arguments(UserUpdateSchema)
        @users_smorest_bp.response(200, UserResponseSchema)
        @users_smorest_bp.alt_response(404, schema=ErrorSchema)
        def put(self, json_data, user_id):
            """
            Update user by ID.

            Updates the specified user's information.
            Requires `user_management_edit` permission.
            """
            from src.database import db
            from src.models.user import User

            user = User.query.get(user_id)
            if not user:
                return {
                    "success": False,
                    "error": "User not found",
                    "code": "NOT_FOUND",
                }, 404

            if "email" in json_data:
                user.email = json_data["email"]
            if "full_name" in json_data:
                user.full_name = json_data["full_name"]
            if "role_id" in json_data:
                user.role_id = json_data["role_id"]
            if "is_active" in json_data:
                user.is_active = json_data["is_active"]

            db.session.commit()

            return {
                "success": True,
                "data": user.to_dict(),
                "message": "تم تحديث المستخدم بنجاح",
            }

        @users_smorest_bp.response(
            200,
            Schema.from_dict(
                {"success": fields.Boolean(), "message": fields.String()}
            )(),
        )
        @users_smorest_bp.alt_response(404, schema=ErrorSchema)
        def delete(self, user_id):
            """
            Delete user by ID.

            Permanently removes a user from the system.
            Requires `user_management_delete` permission.
            """
            from src.database import db
            from src.models.user import User

            user = User.query.get(user_id)
            if not user:
                return {
                    "success": False,
                    "error": "User not found",
                    "code": "NOT_FOUND",
                }, 404

            db.session.delete(user)
            db.session.commit()

            return {"success": True, "message": "تم حذف المستخدم بنجاح"}

    @users_smorest_bp.route("/roles")
    class RolesCollection(MethodView):
        """Role collection endpoints."""

        @users_smorest_bp.response(200, RoleListSchema)
        def get(self):
            """
            Get all roles.

            Returns list of all available roles in the system.
            Requires `user_management_view` permission.
            """
            from src.models.user import Role

            roles = Role.query.all()

            return {
                "success": True,
                "data": [r.to_dict() for r in roles],
                "message": "تم استرجاع الأدوار بنجاح",
            }
