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
    from flask import Flask, jsonify, render_template_string
    from flask_cors import CORS
    import logging
    from datetime import datetime

    # استيراد إعدادات قاعدة البيانات المحسنة
    from database import configure_database, create_tables, create_default_data, db

except ImportError as e:
    print(f"❌ Missing required dependencies: {e}")
    sys.exit(1)
    print("📦 Please install requirements: "
          "pip install -r requirements_final.txt")
    sys.exit(1)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


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
        params.append({
            "name": name,
            "in": "path",
            "required": True,
            "schema": {"type": "string"},
            "description": f"Path parameter: {name}"
        })
    return params


def _infer_tags(openapi_path: str) -> list[str]:
    """Infer basic tags from path segments: /api/<tag>/... -> <Tag>."""
    parts = [p for p in openapi_path.split('/') if p]
    # Expect first segment == 'api'
    if len(parts) >= 2:
        main = parts[1]
        # Skip generic terms
        if main in {"v1", "api"}:
            if len(parts) >= 3:
                main = parts[2]
        return [main.replace('-', ' ').replace('_', ' ').title()]
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
        if rule.endpoint == 'static':
            continue
        if not str(rule.rule).startswith('/api'):
            continue
        methods = [m for m in rule.methods if m in {'GET', 'POST', 'PUT', 'PATCH', 'DELETE'}]
        if not methods:
            continue
        openapi_path = _convert_flask_rule_to_openapi(rule.rule)
        path_item = paths.setdefault(openapi_path, {})
        params = _extract_path_parameters(openapi_path)
        tags = _infer_tags(openapi_path)
        for method in methods:
            view_func = app.view_functions.get(rule.endpoint)
            meta = getattr(view_func, '_api_meta', {}) if view_func else {}
            op_id = f"{method.lower()}_{rule.endpoint.replace('.', '_')}"
            summary = meta.get('summary') or f"Auto-generated endpoint for {rule.endpoint}"
            op_tags = meta.get('tags') or tags
            responses = meta.get('responses') or {}
            # Base 200 response fallback
            if '200' not in responses:
                responses['200'] = {
                    "description": "Successful Response",
                    "content": {
                        "application/json": {
                            "schema": {"$ref": "#/components/schemas/GenericSuccess"}
                        }
                    }
                }
            # Standard error responses if not overridden
            for code, desc in [(400, 'Bad Request'), (401, 'Unauthorized'), (403, 'Forbidden'), (404, 'Not Found'), (500, 'Internal Server Error')]:
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
            req_schema_name = meta.get('request_schema')
            if req_schema_name:
                operation['requestBody'] = {
                    "required": True,
                    "content": {
                        "application/json": {
                            "schema": {"$ref": f"#/components/schemas/{req_schema_name}"}
                        }
                    }
                }
            # Replace 200 schema if response_schema given
            resp_schema_name = meta.get('response_schema')
            if resp_schema_name and '200' in responses:
                responses['200'].setdefault('content', {}).setdefault('application/json', {})['schema'] = {
                    "$ref": f"#/components/schemas/{resp_schema_name}"}

            path_item[method.lower()] = operation

    spec = {
        "openapi": "3.0.0",
        "info": {
            "title": "Complete Inventory Management System API",
            "version": "1.5.0",
            "description": (
                "نظام إدارة المخزون المتكامل - واجهة برمجة التطبيقات"
            )
        },
        "servers": [
            {"url": os.environ.get('API_BASE_URL', 'http://localhost:5002'), "description": "Default server"}
        ],
        "paths": paths,
        "components": {
            "schemas": {
                "GenericSuccess": {
                    "type": "object",
                    "properties": {
                        "status": {"type": "string", "example": "success"},
                        "message": {"type": "string"}
                    },
                    "additionalProperties": True
                },
                **SCHEMA_REGISTRY
            },
            "securitySchemes": {
                "bearerAuth": {
                    "type": "http",
                    "scheme": "bearer",
                    "bearerFormat": "JWT"
                }
            }
        },
        "security": [{"bearerAuth": []}]
    }
    return spec


def create_app():
    """Create and configure Flask application"""
    app = Flask(__name__, template_folder=str(src_dir / 'templates'))

    # Optional: Flask-Limiter for rate limiting
    try:
        from flask_limiter import Limiter
        from flask_limiter.util import get_remote_address
        limiter = Limiter(key_func=get_remote_address, default_limits=[])
        limiter.init_app(app)
        app.extensions = getattr(app, 'extensions', {})
        app.extensions['limiter'] = limiter
    except Exception as e:
        logger.warning(f"⚠️ Flask-Limiter not available: {e}")
        limiter = None

    # Basic configuration
    app.config['SECRET_KEY'] = os.environ.get(
        'SECRET_KEY', 'dev-secret-key-change-in-production')
    app.config['DEBUG'] = os.environ.get('FLASK_DEBUG', '0') == '1'
    app.config['LOG_LEVEL'] = os.environ.get('LOG_LEVEL', 'INFO')

    # إعداد نظام Logging المتقدم
    try:
        from src.utils.logging_config import setup_logging
        setup_logging(app)
    except ImportError:
        logger.warning("⚠️ Advanced logging system not available")

    # Configure database
    db_instance = configure_database(app)

    # Import all models before creating tables (to avoid duplicate class registration)
    with app.app_context():
        try:
            # Import models in correct order (base models first, then dependent models)
            # المرحلة 0: النماذج المستقلة تماماً
            from src.models.partners import SalesEngineer  # noqa: F401

            # المرحلة 1: النماذج الأساسية (بدون foreign keys)
            from src.models.user_unified import User, Role  # noqa: F401
            from src.models.category import Category  # noqa: F401
            from src.models.supplier import Supplier  # noqa: F401

            # المرحلة 1.5: النماذج المعتمدة على المرحلة 0
            from src.models.customer import Customer  # noqa: F401

            # المرحلة 2: النماذج المعتمدة على المرحلة 1
            from src.models.warehouse_unified import Warehouse  # noqa: F401
            from src.models.product_unified import Product  # noqa: F401
            # المرحلة 2.2: النماذج المتقدمة (تفعيل القراءة أولاً)
            try:
                from src.models.product_advanced import ProductAdvanced  # noqa: F401
                from src.models.lot_advanced import LotAdvanced  # noqa: F401
                # من المهم استيراد ProductAdvanced قبل LotAdvanced لضمان إنشاء FK
                logger.info("✅ Advanced models loaded: ProductAdvanced, LotAdvanced")
            except Exception as adv_err:
                logger.warning(f"⚠️ Could not import advanced models: {adv_err}")



            # المرحلة 2.5: نماذج التبعية المباشرة لعلاقات Warehouse/Product
            from src.models.inventory import Inventory  # noqa: F401
            from src.models.supporting_models import StockMovement  # noqa: F401

            # المرحلة 3: النماذج المعتمدة على المرحلة 1 و 2
            from src.models.invoice_unified import Invoice, InvoiceItem  # noqa: F401
        except ImportError as e:
            logger.warning(f"⚠️ Some models could not be imported: {e}")

        # Check if database exists, if not create it
        db_path = 'instance/inventory.db'

        if not os.path.exists(db_path):
            # Database doesn't exist, create tables
            logger.info("⚠️ Database not found, creating tables...")
            if create_tables(app):
                create_default_data()
                logger.info("✅ Database initialized successfully")
            else:
                logger.error("❌ Failed to initialize database")
        else:
            # Database exists, just verify connection
            logger.info("✅ Database already exists, skipping table creation")
            logger.info("💡 Use 'python simple_recreate_db.py' to recreate database")

    # تسجيل معالجات الأخطاء
    try:
        from src.utils.error_handlers import register_error_handlers
        register_error_handlers(app)
        logger.info("✅ Error handlers registered successfully")
    except ImportError:
        logger.warning("⚠️ Error handlers not available")

    # Enable CORS
    CORS(app, resources={
        r"/api/*": {
            "origins": [
                "http://localhost:3000",
                "http://127.0.0.1:3000",
                "http://localhost:5502",
                "http://127.0.0.1:5502",
                "http://localhost:5503",
                "http://127.0.0.1:5503",
                "http://localhost:5173",
                "http://127.0.0.1:5173"
            ],
            "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],

            "allow_headers": ["Content-Type", "Authorization"],
            "supports_credentials": True
        }
    })

    # Register blueprints with error handling (can be skipped in tests)
    if os.environ.get('SKIP_BLUEPRINTS', '0') != '1':
        register_blueprints(app)
        # Attach rate limits to critical auth endpoints if Flask-Limiter is available
        try:
            limiter = getattr(app, 'extensions', {}).get('limiter')
            if limiter:
                vf = app.view_functions
                if 'auth_unified.login' in vf:
                    vf['auth_unified.login'] = limiter.limit("5 per minute")(vf['auth_unified.login'])
                if 'auth_unified.refresh' in vf:
                    vf['auth_unified.refresh'] = limiter.limit("10 per minute")(vf['auth_unified.refresh'])
                if 'auth.login' in vf:
                    vf['auth.login'] = limiter.limit("5 per minute")(vf['auth.login'])
        except Exception as e:
            logger.warning(f"\u26a0\ufe0f Could not attach rate limits: {e}")

    # Register error handlers
    register_error_handlers(app)

    # Add basic routes
    register_basic_routes(app)

    logger.info("✅ Flask application created successfully")
    return app


def register_blueprints(app):

    @app.after_request
    def apply_default_headers(response):
        # Content-Type defaults
        if not response.headers.get('Content-Type'):
            response.headers['Content-Type'] = 'application/json; charset=utf-8'
        # Basic security headers
        response.headers.setdefault('X-Content-Type-Options', 'nosniff')
        response.headers.setdefault('Referrer-Policy', 'strict-origin-when-cross-origin')
        response.headers.setdefault('X-Frame-Options', 'SAMEORIGIN')
        # Extended security headers
        csp = (
            "default-src 'self'; "
            "base-uri 'self'; "
            "frame-ancestors 'self'; "
            "img-src 'self' data: blob:; "
            "script-src 'self' 'unsafe-inline' 'unsafe-eval' blob:; "
            "style-src 'self' 'unsafe-inline'; "
            "font-src 'self' data:; "
            "connect-src 'self' http://localhost:5173 http://127.0.0.1:5173 http://localhost:3000 http://127.0.0.1:3000;"
        )
        response.headers.setdefault('Content-Security-Policy', csp)
        response.headers.setdefault('X-XSS-Protection', '1; mode=block')
        # HSTS (only meaningful over HTTPS)
        response.headers.setdefault('Strict-Transport-Security', 'max-age=63072000; includeSubDomains; preload')
        # Conservative cache control for API responses
        if str(getattr(response, 'mimetype', '')).startswith('application/json') or str(getattr(response, 'content_type', '')).startswith('application/json'):
            response.headers['Cache-Control'] = 'no-cache, no-store, max-age=0'
            response.headers.pop('Expires', None)
            response.headers.pop('Pragma', None)
            # Harmonize API envelope: if status exists and success missing, add success
            try:
                if str(getattr(response, 'mimetype', '')).startswith('application/json') or str(getattr(response, 'content_type', '')).startswith('application/json'):
                    data = None
                    try:
                        data = response.get_json(silent=True)
                    except Exception:
                        data = None
                    if isinstance(data, dict) and ('status' in data) and ('success' not in data):
                        status_val = str(data.get('status')).lower()
                        data['success'] = status_val in ('success', 'ok', 'true', '1')
                        response.set_data(json.dumps(data, ensure_ascii=False))
            except Exception:
                pass
            return response
        # Always return the response object
        return response


    """Register all available blueprints"""
    blueprints_to_register = [
        # System & Status
        ('routes.temp_api', 'temp_api_bp'),
        ('routes.system_status', 'status_bp'),
        ('routes.dashboard', 'dashboard_bp'),

        # Unified routes (v2.0) - أولوية عالية
        ('routes.auth_unified', 'auth_unified_bp'),
        ('routes.users_unified', 'users_unified_bp'),
        ('routes.products_unified', 'products_unified_bp'),
        ('routes.partners_unified', 'partners_unified_bp'),
        ('routes.invoices_unified', 'invoices_unified_bp'),

        # Legacy routes (v1.x) - للتوافق مع الإصدارات القديمة
        ('routes.products', 'products_bp'),
        ('routes.customers', 'customers_bp'),
        ('routes.suppliers', 'suppliers_bp'),
        ('routes.sales', 'sales_bp'),
        ('routes.inventory', 'inventory_bp'),
        ('routes.reports', 'reports_bp'),
        ('routes.auth_routes', 'auth_bp'),
        ('routes.categories', 'categories_bp'),
        ('routes.warehouses', 'warehouses_bp'),
        ('routes.users', 'users_bp'),

        # Critical Missing Blueprints - Frontend Dependencies
        ('routes.accounting', 'accounting_bp'),
        ('routes.settings', 'settings_bp'),
        ('routes.integration_apis', 'integration_bp'),
        ('routes.rag', 'rag_bp'),

        # Advanced Features
        ('routes.advanced_reports', 'advanced_reports_bp'),
        ('routes.financial_reports', 'financial_reports_bp'),
        ('routes.financial_reports_advanced', 'financial_reports_advanced_bp'),
        ('routes.comprehensive_reports', 'comprehensive_reports_bp'),
        ('routes.products_advanced', 'products_advanced_bp'),
        ('routes.sales_advanced', 'sales_advanced_bp'),
        ('routes.inventory_advanced', 'inventory_advanced_bp'),

        # Management Modules
        ('routes.lot_management', 'lot_bp'),
        ('routes.batch_management', 'batch_bp'),
        ('routes.batch_reports', 'batch_reports_bp'),
        ('routes.warehouse_adjustments', 'warehouse_adjustments_bp'),
        ('routes.warehouse_transfer', 'warehouse_transfer_bp'),
        ('routes.returns_management', 'returns_management_bp'),
        ('routes.payment_management', 'payment_management_bp'),
        ('routes.payment_debt_management', 'payment_debt_management_bp'),
        ('routes.treasury_management', 'treasury_management_bp'),

        # Accounts & Partners
        ('routes.customer_supplier_accounts', 'customer_supplier_accounts_bp'),
        ('routes.partners', 'partners_bp'),

        # Settings & Configuration
        ('routes.company_settings', 'company_settings_bp'),
        ('routes.system_settings_advanced', 'system_settings_advanced_bp'),
        ('routes.permissions', 'permissions_bp'),

        # Import/Export
        ('routes.export', 'export_bp'),
        ('routes.excel_import_clean', 'excel_bp'),
        ('routes.excel_operations', 'excel_operations_bp'),
        ('routes.excel_templates', 'excel_templates_bp'),
        ('routes.import_export_advanced', 'import_export_advanced_bp'),

        # Additional Features
        ('routes.profit_loss', 'profit_loss_bp'),
        # ('routes.profit_loss_system', 'profit_loss_system_bp'),  # disabled to avoid duplicate blueprint name
        ('routes.security_system', 'security_bp'),
        ('routes.automation', 'automation_bp'),
        ('routes.interactive_dashboard', 'interactive_dashboard_bp'),
        ('routes.opening_balances_treasury', 'opening_balances_treasury_bp'),
        ('routes.user_management_advanced', 'user_management_advanced_bp'),
        # ('routes.lot_reports', 'lot_reports_bp'),  # disabled to avoid duplicate blueprint name 'batch_reports'
        # ('routes.sales_simple', 'sales_simple_bp'),  # disabled to avoid duplicate blueprint name 'sales'
        ('routes.user', 'user_bp'),
    ]

    registered_count = 0
    for module_name, blueprint_name in blueprints_to_register:
        try:
            module = __import__(module_name, fromlist=[blueprint_name])
            blueprint = getattr(module, blueprint_name)
            app.register_blueprint(blueprint)
            registered_count += 1
            logger.info(f"✅ Registered blueprint: {blueprint_name}")
        except (ImportError, AttributeError) as e:
            logger.warning(f"⚠️ Could not register blueprint "
                          f"{blueprint_name}: {e}")

    logger.info(f"📦 Registered {registered_count} blueprints successfully")


def register_error_handlers(app):
    """Register error handlers"""

    @app.errorhandler(404)
    def not_found(_error):
        # If the path starts with /api return JSON, else render template
        try:
            from flask import request, render_template
            if request.path.startswith('/api'):
                return jsonify({
                    'success': False,
                    'error': 'Resource not found',
                    'message': 'The requested resource was not found on this server.'
                }), 404
            return render_template('404.html'), 404
        except Exception:  # pragma: no cover - fallback to JSON only
            return jsonify({
                'success': False,
                'error': 'Resource not found',
                'message': 'The requested resource was not found on this server.'
            }), 404

    @app.errorhandler(500)
    def internal_error(_error):
        try:
            from flask import request, render_template
            if request.path.startswith('/api'):
                return jsonify({
                    'success': False,
                    'error': 'Internal server error',
                    'message': 'An internal server error occurred.'
                }), 500
            return render_template('500.html'), 500
        except Exception:  # pragma: no cover
            return jsonify({
                'success': False,
                'error': 'Internal server error',
                'message': 'An internal server error occurred.'
            }), 500

    @app.errorhandler(403)
    def forbidden(_error):
        try:
            from flask import request, render_template
            if request.path.startswith('/api'):
                return jsonify({
                    'success': False,
                    'error': 'Forbidden',
                    'message': 'You do not have permission to access this resource.'
                }), 403
            return render_template('403.html'), 403
        except Exception:  # pragma: no cover
            return jsonify({
                'success': False,
                'error': 'Forbidden',
                'message': 'You do not have permission to access this resource.'
            }), 403


def register_basic_routes(app):
    """Register basic application routes (kept thin)."""
    _register_index(app)
    _register_health(app)
    _register_docs(app)


def _register_index(app):
    @app.route('/')
    def index():  # noqa: D401
        return render_template_string(
            """<!DOCTYPE html><html dir=\"rtl\" lang=\"ar\"><head>
            <meta charset=\"UTF-8\"><meta name=\"viewport\" content=\"width=device-width,initial-scale=1.0\">
            <title>نظام إدارة المخزون المتكامل v1.5</title>
            <style>body{font-family:'Segoe UI',Tahoma,sans-serif;margin:0;padding:20px;background:linear-gradient(135deg,#667eea,#764ba2);color:#fff;min-height:100vh} .container{max-width:800px;margin:0 auto;text-align:center} .header,.status{background:rgba(255,255,255,0.1);padding:25px;border-radius:15px;backdrop-filter:blur(10px)} .header{margin-bottom:30px} .success{color:#4CAF50} .api-list{text-align:right;margin-top:20px} .api-item{background:rgba(255,255,255,0.05);padding:8px;margin:4px 0;border-radius:6px;font-size:14px}</style>
            </head><body><div class=\"container\"><div class=\"header\"><h1>🏪 نظام إدارة المخزون المتكامل v1.5</h1><p>Complete Inventory Management System</p><p class=\"success\">✅ النظام يعمل بنجاح</p></div><div class=\"status\"><h2>📊 حالة النظام</h2><p><strong>الوقت:</strong> {{ current_time }}</p><p><strong>الإصدار:</strong> 1.5.0</p><p><strong>البيئة:</strong> {{ environment }}</p><div class=\"api-list\"><h3>🔗 نقاط الوصول المتاحة:</h3><div class=\"api-item\">📈 /api/dashboard</div><div class=\"api-item\">📦 /api/products</div><div class=\"api-item\">👥 /api/customers</div><div class=\"api-item\">🏭 /api/suppliers</div><div class=\"api-item\">💰 /api/sales</div><div class=\"api-item\">📊 /api/reports</div><div class=\"api-item\">🔐 /api/auth</div><div class=\"api-item\">❤️ /api/health</div></div></div></div></body></html>""",
            current_time=datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            environment=os.environ.get('FLASK_ENV', 'development'),
        )


def _register_health(app):
    # Register schemas & apply metadata decorators if available
    try:
        from src.api_meta import register_schema, api_meta
        register_schema('HealthStatus', {
            'type': 'object',
            'properties': {
                'status': {'type': 'string'},
                'timestamp': {'type': 'string', 'format': 'date-time'},
                'version': {'type': 'string'},
                'environment': {'type': 'string'},
                'message': {'type': 'string'}
            },
            'required': ['status', 'timestamp']
        })
        register_schema('SystemInfo', {
            'type': 'object',
            'properties': {
                'system': {'type': 'string'},
                'version': {'type': 'string'},
                'python_version': {'type': 'string'},
                'flask_env': {'type': 'string'},
                'debug_mode': {'type': 'boolean'},
                'timestamp': {'type': 'string', 'format': 'date-time'}
            },
            'required': ['system', 'version', 'timestamp']
        })
    except Exception:  # noqa: BLE001
        api_meta = None  # type: ignore

    decorator_health = api_meta(summary='Health Check',
                                description='Quick health probe for uptime monitoring',
                                tags=['System'],
                                response_schema='HealthStatus') if api_meta else (lambda f: f)
    decorator_info = api_meta(summary='System information',
                              description='Basic system & runtime metadata',
                              tags=['System'],
                              response_schema='SystemInfo') if api_meta else (lambda f: f)

    @app.route('/api/health')
    @decorator_health
    def health_check():
        return jsonify({
            'status': 'healthy',
            'timestamp': datetime.now().isoformat(),
            'version': '1.5.0',
            'environment': os.environ.get('FLASK_ENV', 'development'),
            'message': 'Complete Inventory Management System v1.5 is running'
        })

    @app.route('/api/info')
    @decorator_info
    def system_info():
        return jsonify({
            'system': 'Complete Inventory Management System',
            'version': '1.5.0',
            'python_version': sys.version,
            'flask_env': os.environ.get('FLASK_ENV', 'development'),
            'debug_mode': app.config.get('DEBUG', False),
            'timestamp': datetime.now().isoformat()
        })


def _register_docs(app):
    @app.route('/api/openapi.json')
    def openapi_spec():
        return jsonify(generate_openapi_spec(app))

    @app.route('/api/docs')
    def swagger_docs():
        return ("""<!DOCTYPE html><html><head><title>Swagger UI - Inventory API</title>
        <link rel=\"stylesheet\" type=\"text/css\" href=\"https://unpkg.com/swagger-ui-dist@3.52.5/swagger-ui.css\" />
        <style>html{box-sizing:border-box;overflow:-moz-scrollbars-vertical;overflow-y:scroll}*,*:before,*:after{box-sizing:inherit}body{margin:0;background:#fafafa}</style>
        </head><body><div id=\"swagger-ui\"></div>
        <script src=\"https://unpkg.com/swagger-ui-dist@3.52.5/swagger-ui-bundle.js\"></script>
        <script>SwaggerUIBundle({url:'/api/openapi.json',dom_id:'#swagger-ui',deepLinking:true,presets:[SwaggerUIBundle.presets.apis,SwaggerUIBundle.presets.standalone]})</script>
        </body></html>""".strip())

    @app.route('/api/redoc')
    def redoc_docs():
        return ("""<!DOCTYPE html><html><head><title>ReDoc - Inventory API</title>
        <meta charset=\"utf-8\"/><style>body{margin:0;padding:0}</style>
        <script src=\"https://cdn.jsdelivr.net/npm/redoc@next/bundles/redoc.standalone.js\"></script>
        </head><body><redoc spec-url=\"/api/openapi.json\"></redoc></body></html>""".strip())


# Create the Flask application
app = create_app()

if __name__ == '__main__':
    # Development server
    port = int(os.environ.get('PORT', 5002))
    host = os.environ.get('HOST', '0.0.0.0')
    debug = True  # تفعيل Debug mode دائماً في التطوير

    logger.info("🚀 Starting Complete Inventory Management System v1.5")
    logger.info(f"🌐 Server: http://{host}:{port}")
    logger.info(f"🔧 Debug mode: {debug}")

    app.run(host=host, port=port, debug=debug)
