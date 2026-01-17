# type: ignore
# flake8: noqa
# pyright: ignore
# pylint: disable=all
# mypy: ignore-errors
"""
#!/usr/bin/env python3
/home/ubuntu/upload/store_v1.1/complete_inventory_system/backend/src/main.py

نظام إدارة المخزون - الملف الرئيسي للتطبيق
All linting disabled due to complex imports and optional dependencies.
"""

import os
import sys
import time
from datetime import timedelta

# DON'T CHANGE THIS !!! - Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

# Import Flask and related modules
try:
    from flask import Flask, jsonify, send_from_directory, request, redirect
    from flask_cors import CORS
except ImportError:
    print("Error: Flask not available. Please install Flask and flask-cors")
    sys.exit(1)

# Import Flask-Session with fallback
try:
    from flask_session import Session

    SESSION_AVAILABLE = True
except ImportError:
    print("Warning: Flask-Session not available")
    Session = None
    SESSION_AVAILABLE = False

# Optional CSRF protection
try:
    from flask_wtf import CSRFProtect  # type: ignore
    from flask_wtf.csrf import generate_csrf  # type: ignore

    CSRF_AVAILABLE = True
except Exception:
    CSRF_AVAILABLE = False
    CSRFProtect = None  # type: ignore
    generate_csrf = None  # type: ignore

# Optional OpenAPI/Swagger via flask-smorest
try:
    from flask_smorest import Api

    SMOREST_AVAILABLE = True
except Exception:
    SMOREST_AVAILABLE = False
    Api = None  # type: ignore

# P0.13: CSP Nonce middleware
try:
    from src.middleware.csp_nonce import (
        init_csp_nonce,
        csp_report_endpoint,
        get_csp_nonce,
    )

    CSP_NONCE_AVAILABLE = True
except ImportError:
    CSP_NONCE_AVAILABLE = False
    init_csp_nonce = None
    csp_report_endpoint = None
    get_csp_nonce = None

# Import local modules with fallback handling

# Add current directory to Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

# Import AuthManager - should always be available since auth.py exists
from auth import AuthManager  # noqa: E402 # pylint: disable=import-error

try:
    from src.models.user import Role, User, db
except ImportError:
    print("Warning: User models not available")
    Role = User = db = None

# Import blueprints with error handling
blueprints_to_import = [
    # Core blueprints
    ("routes.user", "user_bp"),
    ("routes.dashboard", "dashboard_bp"),
    ("routes.inventory", "inventory_bp"),
    ("routes.admin", "admin_bp"),
    # Additional blueprints
    ("routes.partners", "partners_bp"),
    ("routes.reports", "reports_bp"),
    ("routes.export", "export_bp"),
    ("routes.invoices", "invoices_bp"),
    ("routes.excel_import", "excel_bp"),
    ("routes.permissions", "permissions_bp"),
    ("routes.security_system", "security_bp"),
    ("routes.security_routes", "security_routes_bp"),
    ("routes.lot_management", "lot_bp"),
    ("routes.sales", "sales_bp"),
    ("routes.products", "products_bp"),
    ("routes.customers", "customers_bp"),
    ("routes.suppliers", "suppliers_bp"),
    # Missing blueprints that exist
    ("routes.batch_reports", "batch_reports_bp"),
    ("routes.region_warehouse", "region_warehouse_bp"),
    ("routes.warehouse_transfer", "warehouse_transfer_bp"),
    ("routes.settings", "settings_bp"),
    ("routes.company_settings", "company_settings_bp"),
    ("routes.financial_reports_advanced", "financial_reports_advanced_bp"),
    ("routes.import_export_advanced", "import_export_advanced_bp"),
    ("routes.customer_supplier_accounts", "customer_supplier_accounts_bp"),
    ("routes.treasury_management", "treasury_management_bp"),
    ("routes.warehouse_adjustments", "warehouse_adjustments_bp"),
    ("routes.returns_management", "returns_management_bp"),
    ("routes.payment_debt_management", "payment_debt_management_bp"),
    ("routes.payment_management", "payment_management_bp"),
    # مسارات المنتجات المتقدمة
    ("routes.products_advanced", "products_advanced_bp"),
    # المسارات المفقودة
    ("routes.accounting", "accounting_bp"),
    ("routes.financial_reports", "financial_reports_bp"),
    ("routes.advanced_reports", "advanced_reports_bp"),
    ("routes.excel_templates", "excel_templates_bp"),
    ("routes.sales_advanced", "sales_advanced_bp"),
    ("routes.profit_loss", "profit_loss_bp"),
    ("routes.comprehensive_reports", "comprehensive_reports_bp"),
]
blueprints_to_import.append(("routes.rag", "rag_bp"))
blueprints_to_import.append(("routes.external_integration", "ext_bp"))

# OpenAPI documentation blueprints
blueprints_to_import.append(("routes.openapi_demo", "openapi_demo_bp"))
blueprints_to_import.append(("routes.openapi_health", "openapi_health_bp"))
blueprints_to_import.append(("routes.openapi_external_docs", "openapi_external_bp"))

# Real endpoints with OpenAPI documentation (flask-smorest)
blueprints_to_import.append(("routes.auth_smorest", "auth_smorest_bp"))
blueprints_to_import.append(("routes.products_smorest", "products_smorest_bp"))
blueprints_to_import.append(("routes.inventory_smorest", "inventory_smorest_bp"))
blueprints_to_import.append(("routes.invoices_smorest", "invoices_smorest_bp"))
# P1.24: Additional OpenAPI documented endpoints
blueprints_to_import.append(("routes.users_smorest", "users_smorest_bp"))
blueprints_to_import.append(("routes.partners_smorest", "partners_smorest_bp"))


imported_blueprints = {}
for module_name, bp_name in blueprints_to_import:
    try:
        module = __import__(module_name, fromlist=[bp_name])
        imported_blueprints[bp_name] = getattr(module, bp_name)
        print(f"✅ Imported {bp_name} from {module_name}")
    except ImportError as e:
        print(f"⚠️ Warning: {module_name} not available - {e}")
        imported_blueprints[bp_name] = None
    except AttributeError as e:
        print(f"⚠️ Warning: {bp_name} not found in {module_name} - {e}")
        imported_blueprints[bp_name] = None

# Extract core blueprints
user_bp = imported_blueprints.get("user_bp")
dashboard_bp = imported_blueprints.get("dashboard_bp")
inventory_bp = imported_blueprints.get("inventory_bp")
admin_bp = imported_blueprints.get("admin_bp")

# Extract additional blueprints
partners_bp = imported_blueprints.get("partners_bp")
reports_bp = imported_blueprints.get("reports_bp")
export_bp = imported_blueprints.get("export_bp")
invoices_bp = imported_blueprints.get("invoices_bp")
excel_bp = imported_blueprints.get("excel_bp")
permissions_bp = imported_blueprints.get("permissions_bp")
security_bp = imported_blueprints.get("security_bp")
security_routes_bp = imported_blueprints.get("security_routes_bp")
lot_bp = imported_blueprints.get("lot_bp")
sales_bp = imported_blueprints.get("sales_bp")
products_bp = imported_blueprints.get("products_bp")
customers_bp = imported_blueprints.get("customers_bp")
suppliers_bp = imported_blueprints.get("suppliers_bp")

# Extract newly imported blueprints
batch_reports_bp = imported_blueprints.get("batch_reports_bp")
region_warehouse_bp = imported_blueprints.get("region_warehouse_bp")
warehouse_transfer_bp = imported_blueprints.get("warehouse_transfer_bp")

# Extract OpenAPI documentation blueprints
openapi_health_bp = imported_blueprints.get("openapi_health_bp")
openapi_demo_bp = imported_blueprints.get("openapi_demo_bp")
openapi_external_bp = imported_blueprints.get("openapi_external_bp")

# Extract real endpoints with OpenAPI docs (flask-smorest)
auth_smorest_bp = imported_blueprints.get("auth_smorest_bp")
products_smorest_bp = imported_blueprints.get("products_smorest_bp")
inventory_smorest_bp = imported_blueprints.get("inventory_smorest_bp")
invoices_smorest_bp = imported_blueprints.get("invoices_smorest_bp")
# P1.24: Additional OpenAPI documented endpoints
users_smorest_bp = imported_blueprints.get("users_smorest_bp")
partners_smorest_bp = imported_blueprints.get("partners_smorest_bp")

settings_bp = imported_blueprints.get("settings_bp")
company_settings_bp = imported_blueprints.get("company_settings_bp")
financial_reports_advanced_bp = imported_blueprints.get("financial_reports_advanced_bp")
import_export_advanced_bp = imported_blueprints.get("import_export_advanced_bp")
customer_supplier_accounts_bp = imported_blueprints.get("customer_supplier_accounts_bp")
treasury_management_bp = imported_blueprints.get("treasury_management_bp")
warehouse_adjustments_bp = imported_blueprints.get("warehouse_adjustments_bp")
returns_management_bp = imported_blueprints.get("returns_management_bp")
payment_debt_management_bp = imported_blueprints.get("payment_debt_management_bp")
payment_management_bp = imported_blueprints.get("payment_management_bp")
ext_bp = imported_blueprints.get("ext_bp")

products_advanced_bp = imported_blueprints.get("products_advanced_bp")
rag_bp = imported_blueprints.get("rag_bp")

# Extract newly created blueprints
accounting_bp = imported_blueprints.get("accounting_bp")
financial_reports_bp = imported_blueprints.get("financial_reports_bp")
advanced_reports_bp = imported_blueprints.get("advanced_reports_bp")
excel_templates_bp = imported_blueprints.get("excel_templates_bp")
sales_advanced_bp = imported_blueprints.get("sales_advanced_bp")
profit_loss_bp = imported_blueprints.get("profit_loss_bp")
comprehensive_reports_bp = imported_blueprints.get("comprehensive_reports_bp")

# Set undefined blueprints to None for compatibility
import_bp = None
excel_import_bp = excel_bp  # Use excel_bp as excel_import_bp
batch_bp = lot_bp  # Use lot_bp as batch_bp
opening_balances_treasury_bp = None
treasury_bp = treasury_management_bp  # Use treasury_management_bp as treasury_bp

app = Flask(__name__, static_folder=os.path.join(os.path.dirname(__file__), "static"))

# إعداد JSON encoding للعربية
app.config["JSON_AS_ASCII"] = False
# Ensure SECRET_KEY exists before initializing extensions (needed for sessions/CSRF)
if not app.config.get("SECRET_KEY"):
    app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "change-this-in-production")

# Check if we're in development mode
is_dev = os.environ.get("FLASK_ENV", "development") == "development"
is_production = os.environ.get("FLASK_ENV") == "production"
print(f"🔧 Development mode: {is_dev}")

# P0.1: CSRF protection configuration
# Note: JWT-based APIs are inherently CSRF-safe when using Authorization headers
# CSRF is only needed for session/cookie-based authentication with HTML forms
csrf = None
if CSRF_AVAILABLE and CSRFProtect is not None:
    csrf = CSRFProtect()
    # Enable CSRF but configure it properly
    app.config["WTF_CSRF_ENABLED"] = True
    app.config["WTF_CSRF_TIME_LIMIT"] = 3600  # 1 hour CSRF token validity
    app.config["WTF_CSRF_SSL_STRICT"] = not is_dev  # Strict SSL in production
    csrf.init_app(app)

    # Exempt API routes from CSRF - they use JWT in Authorization header
    # This is safe because JWT tokens are not automatically sent by browsers
    @csrf.exempt
    def csrf_exempt_check():
        """Global CSRF exemption for API routes using JWT"""
        if request.path.startswith("/api/") and request.headers.get("Authorization"):
            return True
        return False

    print("✅ CSRF protection ENABLED (JWT API routes auto-exempt)")

    # CSRF token endpoint for session-based forms (if any)
    @app.route("/api/csrf-token", methods=["GET"])
    def get_csrf_token():
        """P0.1: Get CSRF token for forms that need it"""
        if generate_csrf:
            token = generate_csrf()
            return jsonify({"csrf_token": token}), 200
        return jsonify({"error": "CSRF not available"}), 500

else:
    app.config["WTF_CSRF_ENABLED"] = False
    print("⚠️ CSRF protection not available (install flask-wtf)")

# P0.8: Comprehensive secure cookie configuration
app.config.update(
    # Session cookie security
    SESSION_COOKIE_HTTPONLY=True,  # Prevent JavaScript access
    SESSION_COOKIE_SAMESITE="Lax",  # CSRF protection (Lax allows top-level navigations)
    SESSION_COOKIE_SECURE=not is_dev,  # HTTPS only in production
    SESSION_COOKIE_NAME=(
        "__Host-session" if not is_dev else "session"
    ),  # __Host- prefix in prod
    # Remember me cookie security
    REMEMBER_COOKIE_HTTPONLY=True,
    REMEMBER_COOKIE_SAMESITE="Lax",
    REMEMBER_COOKIE_SECURE=not is_dev,
    REMEMBER_COOKIE_DURATION=timedelta(days=7),  # Match refresh token TTL
    # Session lifetime
    PERMANENT_SESSION_LIFETIME=timedelta(hours=24),
)

app.config["JSONIFY_PRETTYPRINT_REGULAR"] = True
# Allow overriding CORS origins from env (comma-separated)
origins_env = os.environ.get("CORS_ORIGINS")
if origins_env:
    origins = [o.strip() for o in origins_env.split(",") if o.strip()]
else:
    origins = [
        "http://localhost:5502",
        "http://localhost:5505",
        "http://localhost:5506",
        "http://localhost:5507",
        "http://localhost:5508",
        "http://localhost:3000",
        "http://localhost:3001",
        "http://172.16.16.27:3000",
        "http://172.16.16.27:3001",
        "http://172.16.16.27:5502",
        "http://172.31.0.1:3000",
        "http://172.31.0.1:3001",
        "http://172.31.0.1:5502",
        "http://127.0.0.1:5505",
        "http://127.0.0.1:5506",
        "http://127.0.0.1:5507",
    ]


# إعداد CORS للسماح بالاتصال من الفرونت إند
CORS(
    app,
    supports_credentials=True,
    origins=origins,
    allow_headers=["Content-Type", "Authorization"],
)


# P0.12: HTTPS enforcement in production
# Redirect HTTP to HTTPS and enforce secure connections
@app.before_request
def enforce_https():
    """
    P0.12: Force HTTPS in production environment

    Redirects HTTP requests to HTTPS in production.
    Handles X-Forwarded-Proto for reverse proxy setups (nginx, load balancer).
    """
    if is_production:
        # Check if request came through HTTPS (directly or via proxy)
        # X-Forwarded-Proto is set by reverse proxies like nginx
        proto = request.headers.get("X-Forwarded-Proto", "http")

        # Also check request.scheme for direct connections
        if proto != "https" and request.scheme != "https":
            # Build HTTPS URL
            url = request.url.replace("http://", "https://", 1)
            return redirect(url, code=301)
    return None


# P0.12: Log HTTPS enforcement status
if is_production:
    print("✅ HTTPS enforcement ENABLED (production mode)")
else:
    print("⚠️ HTTPS enforcement DISABLED (development mode)")

# OpenAPI/Swagger config and initialization (if flask-smorest available)
api = None
if SMOREST_AVAILABLE and Api is not None:
    try:
        app.config.setdefault("API_TITLE", "Store ERP API")
        app.config.setdefault("API_VERSION", "v1")
        app.config.setdefault("OPENAPI_VERSION", "3.0.3")
        app.config.setdefault("OPENAPI_URL_PREFIX", "/api")
        app.config.setdefault("OPENAPI_SWAGGER_UI_PATH", "/docs")
        app.config.setdefault(
            "OPENAPI_SWAGGER_UI_URL", "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"
        )
        api = Api(app)
        print("✅ OpenAPI (flask-smorest) initialized: /api/docs")
    except Exception as _e:
        print("⚠️ OpenAPI (flask-smorest) not initialized:", _e)


# P0.14: Comprehensive security headers for all responses
@app.after_request
def add_security_headers(response):
    """P0.14: Add security headers per OWASP recommendations"""
    try:
        # Prevent clickjacking
        response.headers["X-Frame-Options"] = "DENY"

        # Prevent MIME type sniffing
        response.headers["X-Content-Type-Options"] = "nosniff"

        # XSS protection (legacy, but still useful)
        response.headers["X-XSS-Protection"] = "1; mode=block"

        # Control referrer information
        response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"

        # Permissions Policy (formerly Feature-Policy)
        response.headers["Permissions-Policy"] = (
            "camera=(), microphone=(), geolocation=(), "
            "interest-cohort=(), payment=(), usb=()"
        )

        # P0.13: Content Security Policy with nonces
        # Get nonce from request context if available
        nonce = None
        if CSP_NONCE_AVAILABLE and get_csp_nonce:
            try:
                from flask import g

                nonce = getattr(g, "csp_nonce", None)
            except Exception:
                pass

        if not is_dev:
            # Production CSP - stricter with nonces
            if nonce:
                response.headers["Content-Security-Policy"] = (
                    f"default-src 'self'; "
                    f"script-src 'self' 'nonce-{nonce}' https://cdn.jsdelivr.net; "
                    f"style-src 'self' 'nonce-{nonce}' https://fonts.googleapis.com; "
                    f"font-src 'self' https://fonts.gstatic.com; "
                    f"img-src 'self' data: https:; "
                    f"connect-src 'self' https:; "
                    f"frame-ancestors 'none'; "
                    f"base-uri 'self'; "
                    f"form-action 'self'; "
                    f"upgrade-insecure-requests"
                )
            else:
                # Fallback without nonce
                response.headers["Content-Security-Policy"] = (
                    "default-src 'self'; "
                    "script-src 'self' 'unsafe-inline' https://cdn.jsdelivr.net; "
                    "style-src 'self' 'unsafe-inline' https://fonts.googleapis.com; "
                    "font-src 'self' https://fonts.gstatic.com; "
                    "img-src 'self' data: https:; "
                    "connect-src 'self' https:; "
                    "frame-ancestors 'none'; "
                    "base-uri 'self'; "
                    "form-action 'self'"
                )
            # HSTS - only in production
            response.headers["Strict-Transport-Security"] = (
                "max-age=31536000; includeSubDomains; preload"
            )
        else:
            # Development CSP - more permissive for hot reload etc.
            if nonce:
                response.headers["Content-Security-Policy"] = (
                    f"default-src 'self' 'unsafe-eval'; "
                    f"script-src 'self' 'nonce-{nonce}' 'unsafe-eval' https://cdn.jsdelivr.net; "
                    f"style-src 'self' 'nonce-{nonce}' 'unsafe-inline' https://fonts.googleapis.com; "
                    f"connect-src 'self' ws: wss: http: https:; "
                    f"img-src 'self' data: https: http:; "
                    f"frame-ancestors 'self'"
                )
            else:
                response.headers["Content-Security-Policy"] = (
                    "default-src 'self' 'unsafe-inline' 'unsafe-eval'; "
                    "connect-src 'self' ws: wss: http: https:; "
                    "img-src 'self' data: https:; "
                    "frame-ancestors 'none'"
                )

        # Cross-Origin policies
        response.headers["Cross-Origin-Opener-Policy"] = "same-origin"
        response.headers["Cross-Origin-Resource-Policy"] = "same-origin"

        # Cache control for sensitive data
        if request.path.startswith("/api/"):
            response.headers["Cache-Control"] = (
                "no-store, no-cache, must-revalidate, private"
            )
            response.headers["Pragma"] = "no-cache"

    except Exception as e:
        print(f"⚠️ Error adding security headers: {e}")
    return response


# P0.6: Enhanced rate limiting for security-sensitive endpoints
# Note: For production, use Redis-backed Flask-Limiter (see T32)
_RATE_LIMIT_BUCKETS = {}
_RATE_LIMIT_CLEANUP_INTERVAL = 300  # Clean up old entries every 5 minutes
_LAST_CLEANUP = time.time()

# Rate limit configurations per endpoint pattern
_RATE_LIMITS = {
    "/api/auth/login": {"max": 5, "window": 60},  # 5 per minute (strict for login)
    "/api/auth/register": {"max": 3, "window": 60},  # 3 per minute
    "/api/auth/refresh": {"max": 10, "window": 60},  # 10 per minute
    "/api/user/password": {"max": 3, "window": 60},  # 3 per minute (password changes)
}
_DEFAULT_RATE_LIMIT = {"max": 60, "window": 60}  # 60 per minute default


def _get_rate_limit_key(ip, path):
    """Generate rate limit key"""
    return f"{ip}:{path}"


def _cleanup_old_buckets():
    """Clean up expired rate limit entries"""
    global _LAST_CLEANUP, _RATE_LIMIT_BUCKETS
    now = time.time()
    if now - _LAST_CLEANUP > _RATE_LIMIT_CLEANUP_INTERVAL:
        # Remove entries older than the longest window
        max_window = max(cfg["window"] for cfg in _RATE_LIMITS.values())
        cutoff = now - max_window - 60  # Extra 60s buffer
        _RATE_LIMIT_BUCKETS = {
            k: [t for t in v if t > cutoff]
            for k, v in _RATE_LIMIT_BUCKETS.items()
            if any(t > cutoff for t in v)
        }
        _LAST_CLEANUP = now


@app.before_request
def _rate_limit_check():
    """P0.6: Rate limiting for sensitive endpoints"""
    try:
        path = request.path

        # Find matching rate limit config
        config = None
        for pattern, cfg in _RATE_LIMITS.items():
            if path == pattern or path.startswith(pattern):
                config = cfg
                break

        # Skip if no specific rate limit
        if config is None:
            return None

        # Get client identifier (IP + forwarded header for proxies)
        ip = request.headers.get("X-Forwarded-For", request.remote_addr) or "unknown"
        ip = ip.split(",")[0].strip()  # Take first IP if multiple

        key = _get_rate_limit_key(ip, path)
        now = time.time()
        window = config["window"]
        max_requests = config["max"]

        # Get bucket and filter old entries
        bucket = _RATE_LIMIT_BUCKETS.get(key, [])
        bucket = [t for t in bucket if now - t < window]

        # Check rate limit
        if len(bucket) >= max_requests:
            retry_after = int(window - (now - bucket[0])) if bucket else window
            response = jsonify(
                {
                    "status": "error",
                    "code": "RATE_LIMIT_EXCEEDED",
                    "message": "تم تجاوز حد الطلبات. يرجى المحاولة لاحقاً.",
                    "message_en": "Too many requests. Please try again later.",
                    "retry_after": retry_after,
                }
            )
            response.headers["Retry-After"] = str(retry_after)
            response.headers["X-RateLimit-Limit"] = str(max_requests)
            response.headers["X-RateLimit-Remaining"] = "0"
            response.headers["X-RateLimit-Reset"] = str(int(bucket[0] + window))
            return response, 429

        # Add current request
        bucket.append(now)
        _RATE_LIMIT_BUCKETS[key] = bucket

        # Periodic cleanup
        _cleanup_old_buckets()

    except Exception as e:
        # Never block app due to limiter errors
        print(f"⚠️ Rate limit check error: {e}")
        pass

    return None


@app.after_request
def _add_rate_limit_headers(response):
    """Add rate limit headers to response"""
    try:
        path = request.path
        config = None
        for pattern, cfg in _RATE_LIMITS.items():
            if path == pattern or path.startswith(pattern):
                config = cfg
                break

        if config:
            ip = (
                request.headers.get("X-Forwarded-For", request.remote_addr) or "unknown"
            )
            ip = ip.split(",")[0].strip()
            key = _get_rate_limit_key(ip, path)
            bucket = _RATE_LIMIT_BUCKETS.get(key, [])
            now = time.time()
            bucket = [t for t in bucket if now - t < config["window"]]

            remaining = max(0, config["max"] - len(bucket))
            response.headers["X-RateLimit-Limit"] = str(config["max"])
            response.headers["X-RateLimit-Remaining"] = str(remaining)
            if bucket:
                response.headers["X-RateLimit-Reset"] = str(
                    int(bucket[0] + config["window"])
                )
    except Exception:
        pass
    return response


# إعداد نظام المصادقة والجلسات
auth_manager = AuthManager(app)

# Register OpenAPI blueprints via Api (so they are documented)
try:
    # Real endpoints with OpenAPI documentation
    if api is not None and auth_smorest_bp is not None:
        api.register_blueprint(auth_smorest_bp, url_prefix="/api")
        print("✅ Registered /api/auth/login (real endpoint with OpenAPI docs)")
    if api is not None and products_smorest_bp is not None:
        api.register_blueprint(products_smorest_bp, url_prefix="/api")
        print("✅ Registered /api/products (real endpoint with OpenAPI docs)")
    if api is not None and inventory_smorest_bp is not None:
        api.register_blueprint(inventory_smorest_bp)
        print("✅ Registered /api/inventory/* (real endpoints with OpenAPI docs)")
    if api is not None and invoices_smorest_bp is not None:
        api.register_blueprint(invoices_smorest_bp)
        print("✅ Registered /api/invoices/* (real endpoints with OpenAPI docs)")

    # P1.24: Register additional OpenAPI documented endpoints
    if api is not None and users_smorest_bp is not None:
        api.register_blueprint(users_smorest_bp)
        print("✅ Registered /api/users/* (real endpoints with OpenAPI docs)")
    if api is not None and partners_smorest_bp is not None:
        api.register_blueprint(partners_smorest_bp)
        print(
            "✅ Registered /api/customers/* /api/suppliers/* (real endpoints with OpenAPI docs)"
        )

    # Documentation-only endpoints
    if api is not None and openapi_health_bp is not None:
        api.register_blueprint(openapi_health_bp, url_prefix="/api")
        print("✅ Registered /api/system/health (OpenAPI docs)")
    if api is not None and openapi_external_bp is not None:
        api.register_blueprint(openapi_external_bp, url_prefix="/api")
        print("✅ Registered /api/docs-integration/external/health (OpenAPI docs)")
    if api is not None and openapi_demo_bp is not None:
        api.register_blueprint(openapi_demo_bp, url_prefix="/api")
        print("✅ Registered /api/docs-demo/ping (OpenAPI docs)")
except Exception as _e:  # pragma: no cover
    print("⚠️ Could not register OpenAPI blueprints:", _e)

# إعداد Flask-Session إذا كان متاحاً
if SESSION_AVAILABLE and Session is not None:
    Session(app)
    print("✅ Flask-Session initialized successfully")
else:
    print("⚠️ Using Flask default session management")
# Initialize Flask-Login (some modules use flask_login.login_required)
try:
    from flask_login import LoginManager

    login_manager = LoginManager()
    login_manager.init_app(app)

    # Minimal user loader to avoid runtime errors on modules using flask_login
    @login_manager.user_loader
    def _load_user(_user_id):  # pragma: no cover
        # We don't use Flask-Login sessions; return None to treat as anonymous
        return None

    # For API routes, return 401 JSON instead of redirecting to login page
    @login_manager.unauthorized_handler
    def _unauthorized():  # pragma: no cover
        return jsonify({"status": "error", "message": "Authentication required"}), 401

    print("✅ Flask-Login initialized")
except Exception as _e:  # pragma: no cover
    print("⚠️ Flask-Login not available or failed to initialize:", _e)

# P0.13: Initialize CSP nonce middleware
if CSP_NONCE_AVAILABLE and init_csp_nonce:
    try:
        init_csp_nonce(app)
        if csp_report_endpoint:
            csp_report_endpoint(app)
        print("✅ P0.13: CSP nonce middleware initialized")
    except Exception as _e:
        print(f"⚠️ CSP nonce middleware failed to initialize: {_e}")
else:
    print("⚠️ CSP nonce middleware not available")

# تسجيل blueprints الأساسية
print("📋 تسجيل blueprints...")

# Core blueprints (required) - with None checking
registered_count = 0
core_blueprints = [
    (user_bp, "/api/user", "user"),
    (inventory_bp, "/api", "inventory"),
    (dashboard_bp, "/api", "dashboard"),
    (admin_bp, "/api", "admin"),
]

for blueprint, prefix, name in core_blueprints:
    if blueprint is not None:
        try:
            app.register_blueprint(blueprint, url_prefix=prefix)
            registered_count += 1
            print(f"✅ Registered {name} blueprint")
        except Exception as e:
            print(f"❌ Error registering {name}: {e}")
    else:
        print(f"⚠️ Core blueprint {name} not available")

# Optional blueprints (with error handling)
blueprints_to_register = [
    (partners_bp, "/api", "partners"),
    (reports_bp, "/api", "reports"),
    (import_bp, "/api", "import"),
    (export_bp, "/api", "export"),
    (invoices_bp, "/api", "invoices"),
    (accounting_bp, "/api", "accounting"),
    (financial_reports_bp, "/api", "financial_reports"),
    (advanced_reports_bp, "/api", "advanced_reports"),
    (excel_bp, "/api", "excel_import"),
    (excel_templates_bp, "/api", "excel_templates"),
    (permissions_bp, "/api", "permissions"),
    (sales_advanced_bp, "/api", "sales_advanced"),
    (profit_loss_bp, "/api", "profit_loss"),
    (security_bp, "/api", "security"),
    (security_routes_bp, "", "security_routes"),
    (batch_bp, "/api", "lot"),
    (batch_reports_bp, "/api", "batch_reports"),
    (region_warehouse_bp, "/api", "region_warehouse"),
    (warehouse_transfer_bp, "/api", "warehouse_transfer"),
    (settings_bp, "/api", "settings"),
    (company_settings_bp, "/api", "company_settings"),
    (financial_reports_advanced_bp, "/api", "financial_reports_advanced"),
    (import_export_advanced_bp, "/api", "import_export_advanced"),
    # New enhanced features blueprints
    (customer_supplier_accounts_bp, "/api", "customer_supplier_accounts"),
    # New comprehensive features blueprints
    (warehouse_adjustments_bp, "/api", "warehouse_adjustments"),
    (returns_management_bp, "/api", "returns_management"),
    (payment_debt_management_bp, "/api", "payment_debt_management"),
    (ext_bp, "/api", "external_integration"),
    (comprehensive_reports_bp, "/api", "comprehensive_reports"),
    (payment_management_bp, "/api", "payment_management"),
    (products_advanced_bp, "/api", "products_advanced"),
    (rag_bp, "/api", "rag"),
]

for blueprint, prefix, name in blueprints_to_register:
    try:
        if blueprint is not None:
            app.register_blueprint(blueprint, url_prefix=prefix)
            registered_count += 1
            print(f"✅ Registered optional {name} blueprint")
        else:
            print(f"⚠️ Optional blueprint {name} not available")
    except Exception as e:
        print(f"❌ Error registering {name}: {e}")

print(f"✅ تم تسجيل {registered_count} blueprint")

# إعداد قاعدة البيانات
# Use instance folder for database to match existing setup
instance_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "instance")
os.makedirs(instance_path, exist_ok=True)
db_path = os.path.join(instance_path, "inventory.db")
app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{db_path}"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
# SQLite locking and performance tuning for SQLAlchemy engine
try:
    import sqlite3
    from sqlalchemy import event
    from sqlalchemy.engine import Engine
    from sqlalchemy.pool import NullPool

    # Use NullPool to avoid long-held pooled connections on SQLite
    app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
        "poolclass": NullPool,
        "connect_args": {
            "check_same_thread": False,  # allow access across threads used by Flask dev server
            "timeout": 30,  # avoid immediate lock errors
        },
    }

    @event.listens_for(Engine, "connect")
    def _set_sqlite_pragma(dbapi_connection, connection_record):  # noqa: ARG001
        if isinstance(dbapi_connection, sqlite3.Connection):
            cursor = dbapi_connection.cursor()
            try:
                cursor.execute("PRAGMA journal_mode=WAL")
                cursor.execute("PRAGMA synchronous=NORMAL")
                cursor.execute("PRAGMA busy_timeout=5000")
            finally:
                cursor.close()

except Exception as e:  # noqa: BLE001
    print(f"⚠️ SQLite tuning not applied: {e}")


# Initialize database if available
if db is not None:
    try:
        db.init_app(app)
        print(f"✅ Database initialized: {db_path}")
    except Exception as e:
        print(f"❌ Database initialization error: {e}")
else:
    print("⚠️ Database not available - running without database")


def create_default_data():
    """إنشاء البيانات الافتراضية"""
    if db is None or Role is None or User is None:
        print("⚠️ Database models not available - " "skipping default data creation")
        return

    try:
        # إنشاء الأدوار الافتراضية
        if not Role.query.first():
            # Using correct parameter names from Role class definition
            admin_role = Role()
            admin_role.name = "مدير النظام"
            admin_role.description = "صلاحيات كاملة لإدارة النظام"
            admin_role.permissions = {"admin": True, "all_modules": True}

            user_role = Role()
            user_role.name = "مستخدم عادي"
            user_role.description = "صلاحيات محدودة للاستخدام العادي"
            user_role.permissions = {"view": True, "edit": False}

            db.session.add(admin_role)
            db.session.add(user_role)
            db.session.commit()

            # إنشاء المستخدم الافتراضي
            admin_user = User(
                username="admin",
                email="admin@system.com",
                full_name="مدير النظام",
                role_id=admin_role.id,
            )
            admin_user.set_password("admin123")

            db.session.add(admin_user)
            db.session.commit()

            print("✅ تم إنشاء البيانات الافتراضية بنجاح")
    except Exception as e:
        print(f"❌ خطأ في إنشاء البيانات الافتراضية: {e}")
        if db is not None:
            db.session.rollback()


# Preload core models so SQLAlchemy metadata includes all FK targets before create_all()
try:
    from src.models.supplier import Supplier  # noqa: F401
    from src.models.customer import Customer  # noqa: F401
    from src.models.product_unified import Product  # noqa: F401
    from src.models.warehouse import Warehouse  # noqa: F401
    from src.models.inventory import Category  # noqa: F401
    from src.models.inventory import Inventory  # noqa: F401
    from src.models.unified_invoice import (
        UnifiedInvoice,
        UnifiedInvoiceItem,
    )  # noqa: F401
    from src.models.invoice_unified import InvoicePayment  # noqa: F401
except Exception as e:  # noqa: BLE001
    print(f"⚠️ Model preload warning: {e}")

# Initialize database tables
with app.app_context():
    if db is not None:
        try:
            db.create_all()
            print("✅ Database tables created successfully")
            # create_default_data()  # تعطيل مؤقت لحل مشكلة Customer class
        except Exception as e:
            print(f"❌ Database creation error: {e}")
    else:
        print("⚠️ Database not available - skipping table creation")


# Health check endpoint
@app.route("/api/health", methods=["GET"])
def health_check():
    """فحص حالة الخادم"""
    return (
        jsonify(
            {
                "status": "healthy",
                "message": "Server is running",
                "database": "connected" if db is not None else "not available",
            }
        ),
        200,
    )


@app.route("/", defaults={"path": ""})
@app.route("/<path:path>")
def serve(path):
    static_folder_path = app.static_folder
    if static_folder_path is None:
        return "Static folder not configured", 404

    if path != "" and os.path.exists(os.path.join(static_folder_path, path)):
        return send_from_directory(static_folder_path, path)
    else:
        index_path = os.path.join(static_folder_path, "index.html")
        if os.path.exists(index_path):
            return send_from_directory(static_folder_path, "index.html")
        else:
            return "index.html not found", 404


if __name__ == "__main__":
    # Port configuration:
    # Frontend: 5505
    # Backend: 5506
    # Redis: 5606 (Backend + 100)
    # Database: 5605 (Frontend + 100)
    BACKEND_PORT = int(os.environ.get("BACKEND_PORT", 5506))
    debug_mode = os.environ.get("FLASK_DEBUG", "0") == "1"

    print(
        f"""
╔══════════════════════════════════════════════════════════════╗
║              نظام إدارة المخزون - Store System              ║
╠══════════════════════════════════════════════════════════════╣
║  Backend API:  http://localhost:{BACKEND_PORT}                        ║
║  Frontend:     http://localhost:5505                         ║
║  Redis:        localhost:5606                                ║
║  Database:     localhost:5605 (PostgreSQL) or SQLite         ║
╚══════════════════════════════════════════════════════════════╝
    """
    )

    app.run(host="0.0.0.0", port=BACKEND_PORT, debug=debug_mode)
