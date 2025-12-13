#!/usr/bin/env python3
# type: ignore
# flake8: noqa
# pyright: ignore
# pylint: disable=all
# mypy: ignore-errors
"""
Complete Inventory Management System - Main Application Entry Point
Consolidated Flask application with all routes and configurations
All linting disabled due to complex imports and optional dependencies.
"""

import os
import sys
import re
import json
from pathlib import Path

# Add src directory to Python path
current_dir = Path(__file__).parent
src_dir = current_dir / "src"
sys.path.insert(0, str(src_dir))

try:
    from dotenv import load_dotenv

    # Load environment variables from .env file
    load_dotenv()

    from flask import Flask, jsonify, render_template_string
    from flask_cors import CORS
    import logging
    from datetime import datetime, timedelta

    # استيراد إعدادات قاعدة البيانات المحسنة
    from src.database import configure_database, create_tables, create_default_data, db

    # Import comprehensive logging system
    from src.utils.comprehensive_logger import ComprehensiveLogger, comprehensive_logger
    from src.utils.startup_logger import StartupLogger
    from src.utils.database_audit import create_audit_trail

except ImportError as e:
    print(f"❌ Missing required dependencies: {e}")
    sys.exit(1)
    print("📦 Please install requirements: " "pip install -r requirements_final.txt")
    sys.exit(1)

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# Initialize comprehensive logger
comprehensive_logger._create_log_directories()
comprehensive_logger._setup_loggers()

# Initialize startup logger
startup_logger = StartupLogger(comprehensive_logger)


def _convert_flask_rule_to_openapi(path_rule: str) -> str:
    """Convert Flask style route patterns to OpenAPI path template.

    Examples:
      /api/users/<int:user_id> -> /api/users/{user_id}
      /api/items/<item_id> -> /api/items/{item_id}
    """
    # Replace <converter:name> or <name> with {name}
    return re.sub(r"<(?:[^:<>]+:)?([^<>]+)>", r"{\1}", path_rule)


def _extract_path_parameters(openapi_path: str):
    """Return list of parameter objects for {param} placeholders."""
    params = []
    for name in re.findall(r"{([^/{}]+)}", openapi_path):
        params.append(
            {
                "name": name,
                "in": "path",
                "required": True,
                "schema": {"type": "string"},
                "description": f"Path parameter: {name}",
            }
        )
    return params


def _infer_tags(openapi_path: str) -> list[str]:
    """Infer basic tags from path segments: /api/<tag>/... -> <Tag>."""
    parts = [p for p in openapi_path.split("/") if p]
    # Expect first segment == 'api'
    if len(parts) >= 2:
        main = parts[1]
        # Skip generic terms
        if main in {"v1", "api"}:
            if len(parts) >= 3:
                main = parts[2]
        return [main.replace("-", " ").replace("_", " ").title()]
    return ["General"]


def generate_openapi_spec(app) -> dict:
    """Dynamically build a minimal OpenAPI 3.0 specification from registered routes.

    This is a lightweight reflective generator intended as a starting point.
    For production-grade documentation you can extend each path/operation with
    schemas, requestBody, parameters, and detailed responses.
    """
    paths: dict = {}
    try:  # Resilient import; if module path not available continue with empty registry
        from src.api_meta import SCHEMA_REGISTRY  # type: ignore
    except Exception:  # noqa: BLE001
        SCHEMA_REGISTRY = {}

    for rule in app.url_map.iter_rules():
        # Skip static and non-API endpoints unless explicitly under /api
        if rule.endpoint == "static":
            continue
        if not str(rule.rule).startswith("/api"):
            continue
        methods = [
            m for m in rule.methods if m in {"GET", "POST", "PUT", "PATCH", "DELETE"}
        ]
        if not methods:
            continue
        openapi_path = _convert_flask_rule_to_openapi(rule.rule)
        path_item = paths.setdefault(openapi_path, {})
        params = _extract_path_parameters(openapi_path)
        tags = _infer_tags(openapi_path)
        for method in methods:
            view_func = app.view_functions.get(rule.endpoint)
            meta = getattr(view_func, "_api_meta", {}) if view_func else {}
            op_id = f"{method.lower()}_{rule.endpoint.replace('.', '_')}"
            summary = (
                meta.get("summary") or f"Auto-generated endpoint for {rule.endpoint}"
            )
            op_tags = meta.get("tags") or tags
            responses = meta.get("responses") or {}
            # Base 200 response fallback
            if "200" not in responses:
                responses["200"] = {
                    "description": "Successful Response",
                    "content": {
                        "application/json": {
                            "schema": {"$ref": "#/components/schemas/GenericSuccess"}
                        }
                    },
                }
            # Standard error responses if not overridden
            for code, desc in [
                (400, "Bad Request"),
                (401, "Unauthorized"),
                (403, "Forbidden"),
                (404, "Not Found"),
                (500, "Internal Server Error"),
            ]:
                code_str = str(code)
                responses.setdefault(code_str, {"description": desc})

            operation: dict = {
                "operationId": op_id,
                "summary": summary,
                "tags": op_tags,
                "parameters": params,
                "responses": responses,
            }
            # Request body
            req_schema_name = meta.get("request_schema")
            if req_schema_name:
                operation["requestBody"] = {
                    "required": True,
                    "content": {
                        "application/json": {
                            "schema": {
                                "$ref": f"#/components/schemas/{req_schema_name}"
                            }
                        }
                    },
                }
            # Replace 200 schema if response_schema given
            resp_schema_name = meta.get("response_schema")
            if resp_schema_name and "200" in responses:
                responses["200"].setdefault("content", {}).setdefault(
                    "application/json", {}
                )["schema"] = {"$ref": f"#/components/schemas/{resp_schema_name}"}

            path_item[method.lower()] = operation

    spec = {
        "openapi": "3.0.0",
        "info": {
            "title": "Complete Inventory Management System API",
            "version": "1.5.0",
            "description": ("نظام إدارة المخزون المتكامل - واجهة برمجة التطبيقات"),
        },
        "servers": [
            {
                "url": os.environ.get("API_BASE_URL", "http://localhost:5001"),
                "description": "Default server",
            }
        ],
        "paths": paths,
        "components": {
            "schemas": {
                "GenericSuccess": {
                    "type": "object",
                    "properties": {
                        "status": {"type": "string", "example": "success"},
                        "message": {"type": "string"},
                    },
                    "additionalProperties": True,
                },
                **SCHEMA_REGISTRY,
            },
            "securitySchemes": {
                "bearerAuth": {
                    "type": "http",
                    "scheme": "bearer",
                    "bearerFormat": "JWT",
                }
            },
        },
        "security": [{"bearerAuth": []}],
    }
    return spec


def create_app(config=None):
    """Create and configure Flask application

    Args:
        config: Optional config name ('testing', 'development', 'production')
    """
    comprehensive_logger.log_startup(event="app_creation_started")

    app = Flask(__name__, template_folder=str(src_dir / "templates"))

    # Basic configuration
    if config == "testing":
        app.config["TESTING"] = True
        app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
        app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    app.config["SECRET_KEY"] = os.environ.get(
        "SECRET_KEY", "dev-secret-key-change-in-production"
    )
    app.config["DEBUG"] = os.environ.get("FLASK_DEBUG", "0") == "1"

    # JWT Configuration (required by flask-jwt-extended)
    app.config["JWT_SECRET_KEY"] = os.environ.get(
        "JWT_SECRET_KEY", app.config["SECRET_KEY"]
    )
    app.config["JWT_TOKEN_LOCATION"] = ["headers"]
    app.config["JWT_HEADER_NAME"] = "Authorization"
    app.config["JWT_HEADER_TYPE"] = "Bearer"
    app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=1)
    app.config["JWT_REFRESH_TOKEN_EXPIRES"] = timedelta(days=30)
    app.config["JWT_IDENTITY_CLAIM"] = (
        "user_id"  # Use 'user_id' instead of default 'sub'
    )

    # Initialize JWT Manager (required for @jwt_required decorator)
    try:
        from flask_jwt_extended import JWTManager

        jwt = JWTManager(app)
        logger.info("✅ JWT Manager initialized successfully")
    except Exception as e:
        logger.warning(f"⚠️ Could not initialize JWT Manager: {e}")

    # Log configuration
    comprehensive_logger.log_startup(event="config_loaded", DEBUG=app.config["DEBUG"])

    # Configure database
    db_instance = configure_database(app)
    comprehensive_logger.log_startup(event="database_configured")

    # Create tables and default data
    with app.app_context():
        result = create_tables(app)
        if result and isinstance(result, tuple):
            success, User, Role, Category, Warehouse = result
            if success:
                # Pass models to avoid duplicate imports/registrations
                create_default_data(User, Role, Category, Warehouse)
                logger.info("✅ Database initialized successfully")
                comprehensive_logger.log_startup(
                    event="database_initialized", status="success"
                )
            else:
                logger.error("❌ Failed to create tables")
                comprehensive_logger.log_startup(
                    event="database_initialized", status="failed"
                )
        elif result is True:
            # Old behavior fallback
            create_default_data()
            logger.info("✅ Database initialized successfully")
            comprehensive_logger.log_startup(
                event="database_initialized", status="success"
            )
        else:
            logger.error("❌ Failed to initialize database")
            comprehensive_logger.log_startup(
                event="database_initialized", status="failed"
            )

    # Enable CORS - Allow all origins in development
    CORS(
        app,
        resources={
            r"/api/*": {
                "origins": "*",  # Allow all origins for development
                "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
                "allow_headers": ["Content-Type", "Authorization", "X-CSRFToken"],
                "supports_credentials": False,  # Must be False when origins is "*"
            }
        },
    )
    comprehensive_logger.log_startup(event="cors_configured")

    # Initialize comprehensive logger with app
    comprehensive_logger.init_app(app)
    comprehensive_logger.log_startup(event="comprehensive_logger_initialized")

    # Create database audit trail
    try:
        audit_trail = create_audit_trail(db, comprehensive_logger)
        comprehensive_logger.log_startup(event="audit_trail_created")
    except Exception as e:
        comprehensive_logger.log_error(f"Failed to create audit trail: {str(e)}")

    # Register blueprints with error handling (can be skipped in tests)
    if os.environ.get("SKIP_BLUEPRINTS", "0") != "1":
        register_blueprints(app)

    # Register error handlers
    register_error_handlers(app)

    # Add basic routes
    register_basic_routes(app)

    logger.info("✅ Flask application created successfully")
    comprehensive_logger.log_startup(event="app_creation_completed")
    return app


def register_blueprints(app):
    """Register all available blueprints - FULL ADVANCED FEATURES ENABLED"""
    blueprints_to_register = [
        # Core System
        ("routes.temp_api", "temp_api_bp"),
        ("routes.system_status", "status_bp"),
        ("routes.dashboard", "dashboard_bp"),
        ("routes.interactive_dashboard", "interactive_dashboard_bp"),
        # Auth & Users
        ("routes.auth_unified", "auth_unified_bp"),
        ("routes.users_unified", "users_unified_bp"),
        ("routes.mfa_routes", "mfa_bp"),
        # ('routes.permissions', 'permissions_bp'),  # Model file, not route
        # ('routes.user_management_advanced', 'user_management_advanced_bp'),  # Model file, not route
        # Products & Inventory
        ("routes.products_unified", "products_unified_bp"),
        ("routes.inventory", "inventory_bp"),
        ("routes.categories", "categories_bp"),
        ("routes.lot_management", "lot_bp"),
        ("routes.batch_management", "batch_bp"),
        ("routes.batch_reports", "batch_reports_bp"),
        ("routes.batches_advanced", "batches_bp"),
        # ('routes.lot_reports', 'batch_reports_bp'),  # Duplicate - lot_reports imports from batch_reports
        # ('routes.region_warehouse', 'region_warehouse_bp'),  # Model file, not route
        # Partners & CRM
        ("routes.partners_unified", "partners_unified_bp"),
        ("routes.customer_supplier_accounts", "customer_supplier_accounts_bp"),
        # Sales & Invoices
        ("routes.sales", "sales_bp"),
        # Purchases
        ("routes.purchases", "purchases_bp"),
        # POS
        ("routes.pos", "pos_bp"),
        # ('routes.sales_advanced', 'sales_advanced_bp'),  # Model file, not route
        ("routes.invoices_unified", "invoices_unified_bp"),
        # ('routes.returns_management', 'returns_management_bp'),  # Model file, not route
        # Accounting & Finance
        ("routes.accounting", "accounting_simple_bp"),
        # ('routes.accounting_system', 'accounting_system_bp'),  # Model file, not route
        ("routes.treasury_management", "treasury_management_bp"),
        # ('routes.opening_balances_treasury', 'opening_balances_treasury_bp'),  # Model file, not route
        # ('routes.payment_management', 'payment_management_bp'),  # Model file, not route
        ("routes.payment_debt_management", "payment_debt_management_bp"),
        ("routes.profit_loss", "profit_loss_bp"),
        # ('routes.profit_loss_system', 'profit_loss_bp'),  # Model file, not route (duplicate)
        # Reports
        ("routes.reports", "reports_bp"),
        ("routes.reports_system", "reports_system_bp"),
        ("routes.advanced_reports", "advanced_reports_bp"),
        ("routes.comprehensive_reports", "comprehensive_reports_bp"),
        ("routes.financial_reports", "financial_reports_bp"),
        ("routes.financial_reports_advanced", "financial_reports_advanced_bp"),
        # Import/Export
        ("routes.excel_operations", "excel_bp"),
        ("routes.excel_import", "excel_bp"),
        ("routes.excel_templates", "excel_templates_bp"),
        ("routes.import_data", "import_bp"),
        ("routes.export", "export_bp"),
        ("routes.import_export_advanced", "import_export_advanced_bp"),
        # Settings & Admin
        ("routes.settings", "settings_bp"),
        ("routes.company_settings", "company_settings_bp"),
        # ('routes.system_settings_advanced', 'system_settings_advanced_bp'),  # Model file, not route
        ("routes.admin_panel", "admin_panel_bp"),
        # Integration & Automation
        ("routes.integration_apis", "integration_bp"),
        ("routes.external_integration", "ext_bp"),
        ("routes.automation", "automation_bp"),
        ("routes.rag", "rag_bp"),
        # OpenAPI & Errors
        ("routes.openapi_demo", "openapi_demo_bp"),
        ("routes.openapi_health", "openapi_health_bp"),
        ("routes.openapi_external_docs", "openapi_external_bp"),
        ("routes.errors", "errors_bp"),
    ]

    registered_count = 0
    for module_name, blueprint_name in blueprints_to_register:
        try:
            # Log import attempt
            comprehensive_logger.log_startup(event="import_attempt", module=module_name)

            module = __import__(module_name, fromlist=[blueprint_name])
            blueprint = getattr(module, blueprint_name)

            # Skip None blueprints (e.g., OpenAPI blueprints when flask-smorest not installed)
            if blueprint is None:
                logger.info(f"ℹ️ Skipping blueprint {blueprint_name} (not available)")
                continue

            app.register_blueprint(blueprint)
            registered_count += 1

            # Log successful blueprint registration
            comprehensive_logger.log_startup(
                event="blueprint_registered", blueprint=blueprint_name
            )
            logger.info(f"✅ Registered blueprint: {blueprint_name}")

        except (ImportError, AttributeError) as e:
            # Log failed blueprint registration
            comprehensive_logger.log_startup(
                event="blueprint_failed", blueprint=blueprint_name, error=str(e)
            )
            logger.warning(f"⚠️ Could not register blueprint " f"{blueprint_name}: {e}")

    logger.info(f"📦 Registered {registered_count} blueprints successfully")
    comprehensive_logger.log_startup(
        event="blueprints_registered",
        total=len(blueprints_to_register),
        successful=registered_count,
        failed=len(blueprints_to_register) - registered_count,
    )


def register_error_handlers(app):
    """Register error handlers"""

    @app.errorhandler(404)
    def not_found(_error):
        # If the path starts with /api return JSON, else render template
        try:
            from flask import request, render_template

            if request.path.startswith("/api"):
                return (
                    jsonify(
                        {
                            "success": False,
                            "error": "Resource not found",
                            "message": "The requested resource was not found on this server.",
                        }
                    ),
                    404,
                )
            return render_template("404.html"), 404
        except Exception:  # pragma: no cover - fallback to JSON only
            return (
                jsonify(
                    {
                        "success": False,
                        "error": "Resource not found",
                        "message": "The requested resource was not found on this server.",
                    }
                ),
                404,
            )

    @app.errorhandler(500)
    def internal_error(_error):
        try:
            from flask import request, render_template

            if request.path.startswith("/api"):
                return (
                    jsonify(
                        {
                            "success": False,
                            "error": "Internal server error",
                            "message": "An internal server error occurred.",
                        }
                    ),
                    500,
                )
            return render_template("500.html"), 500
        except Exception:  # pragma: no cover
            return (
                jsonify(
                    {
                        "success": False,
                        "error": "Internal server error",
                        "message": "An internal server error occurred.",
                    }
                ),
                500,
            )

    @app.errorhandler(403)
    def forbidden(_error):
        try:
            from flask import request, render_template

            if request.path.startswith("/api"):
                return (
                    jsonify(
                        {
                            "success": False,
                            "error": "Forbidden",
                            "message": "You do not have permission to access this resource.",
                        }
                    ),
                    403,
                )
            return render_template("403.html"), 403
        except Exception:  # pragma: no cover
            return (
                jsonify(
                    {
                        "success": False,
                        "error": "Forbidden",
                        "message": "You do not have permission to access this resource.",
                    }
                ),
                403,
            )

    @app.errorhandler(400)
    def bad_request(_error):
        try:
            from flask import request, render_template

            if request.path.startswith("/api"):
                return (
                    jsonify(
                        {
                            "success": False,
                            "error": "Bad Request",
                            "message": "The request is invalid or malformed.",
                        }
                    ),
                    400,
                )
            return render_template("400.html"), 400
        except Exception:  # pragma: no cover
            return (
                jsonify(
                    {
                        "success": False,
                        "error": "Bad Request",
                        "message": "The request is invalid or malformed.",
                    }
                ),
                400,
            )

    @app.errorhandler(401)
    def unauthorized(_error):
        try:
            from flask import request, render_template

            if request.path.startswith("/api"):
                return (
                    jsonify(
                        {
                            "success": False,
                            "error": "Unauthorized",
                            "message": "Authentication is required to access this resource.",
                        }
                    ),
                    401,
                )
            return render_template("401.html"), 401
        except Exception:  # pragma: no cover
            return (
                jsonify(
                    {
                        "success": False,
                        "error": "Unauthorized",
                        "message": "Authentication is required to access this resource.",
                    }
                ),
                401,
            )

    @app.errorhandler(501)
    def not_implemented(_error):
        try:
            from flask import request, render_template

            if request.path.startswith("/api"):
                return (
                    jsonify(
                        {
                            "success": False,
                            "error": "Not Implemented",
                            "message": "The server does not support the functionality required.",
                        }
                    ),
                    501,
                )
            return render_template("501.html"), 501
        except Exception:  # pragma: no cover
            return (
                jsonify(
                    {
                        "success": False,
                        "error": "Not Implemented",
                        "message": "The server does not support the functionality required.",
                    }
                ),
                501,
            )

    @app.errorhandler(502)
    def bad_gateway(_error):
        try:
            from flask import request, render_template

            if request.path.startswith("/api"):
                return (
                    jsonify(
                        {
                            "success": False,
                            "error": "Bad Gateway",
                            "message": "The server received an invalid response from upstream.",
                        }
                    ),
                    502,
                )
            return render_template("502.html"), 502
        except Exception:  # pragma: no cover
            return (
                jsonify(
                    {
                        "success": False,
                        "error": "Bad Gateway",
                        "message": "The server received an invalid response from upstream.",
                    }
                ),
                502,
            )

    @app.errorhandler(503)
    def service_unavailable(_error):
        try:
            from flask import request, render_template

            if request.path.startswith("/api"):
                return (
                    jsonify(
                        {
                            "success": False,
                            "error": "Service Unavailable",
                            "message": "The server is temporarily unavailable.",
                        }
                    ),
                    503,
                )
            return render_template("503.html"), 503
        except Exception:  # pragma: no cover
            return (
                jsonify(
                    {
                        "success": False,
                        "error": "Service Unavailable",
                        "message": "The server is temporarily unavailable.",
                    }
                ),
                503,
            )

    @app.errorhandler(504)
    def gateway_timeout(_error):
        try:
            from flask import request, render_template

            if request.path.startswith("/api"):
                return (
                    jsonify(
                        {
                            "success": False,
                            "error": "Gateway Timeout",
                            "message": "The server did not receive a timely response.",
                        }
                    ),
                    504,
                )
            return render_template("504.html"), 504
        except Exception:  # pragma: no cover
            return (
                jsonify(
                    {
                        "success": False,
                        "error": "Gateway Timeout",
                        "message": "The server did not receive a timely response.",
                    }
                ),
                504,
            )


def register_basic_routes(app):
    """Register basic application routes (kept thin)."""
    _register_index(app)
    _register_health(app)
    _register_docs(app)


def _register_index(app):
    @app.route("/")
    def index():  # noqa: D401
        return render_template_string(
            """<!DOCTYPE html><html dir=\"rtl\" lang=\"ar\"><head>
            <meta charset=\"UTF-8\"><meta name=\"viewport\" content=\"width=device-width,initial-scale=1.0\">
            <title>نظام إدارة المخزون المتكامل v1.5</title>
            <style>body{font-family:'Segoe UI',Tahoma,sans-serif;margin:0;padding:20px;background:linear-gradient(135deg,#667eea,#764ba2);color:#fff;min-height:100vh} .container{max-width:800px;margin:0 auto;text-align:center} .header,.status{background:rgba(255,255,255,0.1);padding:25px;border-radius:15px;backdrop-filter:blur(10px)} .header{margin-bottom:30px} .success{color:#4CAF50} .api-list{text-align:right;margin-top:20px} .api-item{background:rgba(255,255,255,0.05);padding:8px;margin:4px 0;border-radius:6px;font-size:14px}</style>
            </head><body><div class=\"container\"><div class=\"header\"><h1>🏪 نظام إدارة المخزون المتكامل v1.5</h1><p>Complete Inventory Management System</p><p class=\"success\">✅ النظام يعمل بنجاح</p></div><div class=\"status\"><h2>📊 حالة النظام</h2><p><strong>الوقت:</strong> {{ current_time }}</p><p><strong>الإصدار:</strong> 1.5.0</p><p><strong>البيئة:</strong> {{ environment }}</p><div class=\"api-list\"><h3>🔗 نقاط الوصول المتاحة:</h3><div class=\"api-item\">📈 /api/dashboard</div><div class=\"api-item\">📦 /api/products</div><div class=\"api-item\">👥 /api/customers</div><div class=\"api-item\">🏭 /api/suppliers</div><div class=\"api-item\">💰 /api/sales</div><div class=\"api-item\">📊 /api/reports</div><div class=\"api-item\">🔐 /api/auth</div><div class=\"api-item\">❤️ /api/health</div></div></div></div></body></html>""",
            current_time=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            environment=os.environ.get("FLASK_ENV", "development"),
        )


def _register_health(app):
    # Register schemas & apply metadata decorators if available
    try:
        from src.api_meta import register_schema, api_endpoint as api_meta

        register_schema(
            "HealthStatus",
            {
                "type": "object",
                "properties": {
                    "status": {"type": "string"},
                    "timestamp": {"type": "string", "format": "date-time"},
                    "version": {"type": "string"},
                    "environment": {"type": "string"},
                    "message": {"type": "string"},
                },
                "required": ["status", "timestamp"],
            },
        )
        register_schema(
            "SystemInfo",
            {
                "type": "object",
                "properties": {
                    "system": {"type": "string"},
                    "version": {"type": "string"},
                    "python_version": {"type": "string"},
                    "flask_env": {"type": "string"},
                    "debug_mode": {"type": "boolean"},
                    "timestamp": {"type": "string", "format": "date-time"},
                },
                "required": ["system", "version", "timestamp"],
            },
        )
    except Exception:  # noqa: BLE001
        api_meta = None  # type: ignore

    decorator_health = (
        api_meta(
            summary="Health Check",
            description="Quick health probe for uptime monitoring",
            tags=["System"],
            response_schema="HealthStatus",
        )
        if api_meta
        else (lambda f: f)
    )
    decorator_info = (
        api_meta(
            summary="System information",
            description="Basic system & runtime metadata",
            tags=["System"],
            response_schema="SystemInfo",
        )
        if api_meta
        else (lambda f: f)
    )

    @app.route("/api/health")
    @decorator_health
    def health_check():
        return jsonify(
            {
                "status": "healthy",
                "timestamp": datetime.now().isoformat(),
                "version": "1.5.0",
                "environment": os.environ.get("FLASK_ENV", "development"),
                "message": "Complete Inventory Management System v1.5 is running",
            }
        )

    @app.route("/api/info")
    @decorator_info
    def system_info():
        return jsonify(
            {
                "system": "Complete Inventory Management System",
                "version": "1.5.0",
                "python_version": sys.version,
                "flask_env": os.environ.get("FLASK_ENV", "development"),
                "debug_mode": app.config.get("DEBUG", False),
                "timestamp": datetime.now().isoformat(),
            }
        )


def _register_docs(app):
    @app.route("/api/openapi.json")
    def openapi_spec():
        return jsonify(generate_openapi_spec(app))

    @app.route("/api/docs")
    def swagger_docs():
        return """<!DOCTYPE html><html><head><title>Swagger UI - Inventory API</title>
        <link rel=\"stylesheet\" type=\"text/css\" href=\"https://unpkg.com/swagger-ui-dist@3.52.5/swagger-ui.css\" />
        <style>html{box-sizing:border-box;overflow:-moz-scrollbars-vertical;overflow-y:scroll}*,*:before,*:after{box-sizing:inherit}body{margin:0;background:#fafafa}</style>
        </head><body><div id=\"swagger-ui\"></div>
        <script src=\"https://unpkg.com/swagger-ui-dist@3.52.5/swagger-ui-bundle.js\"></script>
        <script>SwaggerUIBundle({url:'/api/openapi.json',dom_id:'#swagger-ui',deepLinking:true,presets:[SwaggerUIBundle.presets.apis,SwaggerUIBundle.presets.standalone]})</script>
        </body></html>""".strip()

    @app.route("/api/redoc")
    def redoc_docs():
        return """<!DOCTYPE html><html><head><title>ReDoc - Inventory API</title>
        <meta charset=\"utf-8\"/><style>body{margin:0;padding:0}</style>
        <script src=\"https://cdn.jsdelivr.net/npm/redoc@next/bundles/redoc.standalone.js\"></script>
        </head><body><redoc spec-url=\"/api/openapi.json\"></redoc></body></html>""".strip()


# Create the Flask application
app = create_app()

if __name__ == "__main__":
    # Development server
    port = int(os.environ.get("PORT", 5005))
    host = os.environ.get("HOST", "0.0.0.0")
    debug = os.environ.get("FLASK_DEBUG", "0") == "1"

    logger.info("🚀 Starting Complete Inventory Management System v1.5")
    logger.info(f"🌐 Server: http://{host}:{port}")
    logger.info(f"🔧 Debug mode: {debug}")

    # Log server start
    comprehensive_logger.log_startup(
        event="server_start", host=host, port=port, debug=debug
    )

    app.run(host=host, port=port, debug=debug)
