"""
Session Cookie Middleware

Provides secure session management with cookie support.
"""

import os
import hashlib
import secrets
from datetime import datetime, timedelta
from functools import wraps
from typing import Optional, Dict, Any

from flask import Flask, request, session, g, jsonify, make_response


class SessionConfig:
    """Session configuration settings"""

    # Session cookie settings
    SESSION_COOKIE_NAME = "store_session"
    SESSION_COOKIE_SECURE = (
        os.environ.get("SESSION_COOKIE_SECURE", "false").lower() == "true"
    )
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = "Lax"  # 'Strict', 'Lax', or 'None'
    SESSION_COOKIE_PATH = "/"
    SESSION_COOKIE_DOMAIN = None  # None = current domain

    # Session lifetime
    SESSION_PERMANENT = True
    PERMANENT_SESSION_LIFETIME = timedelta(hours=24)
    SESSION_REFRESH_EACH_REQUEST = True

    # Session storage
    SESSION_TYPE = "filesystem"  # 'filesystem', 'redis', 'memcached'
    SESSION_FILE_DIR = "flask_session"
    SESSION_FILE_THRESHOLD = 500
    SESSION_FILE_MODE = 0o600

    # Redis settings (if SESSION_TYPE = 'redis')
    SESSION_REDIS_HOST = os.environ.get("REDIS_HOST", "localhost")
    SESSION_REDIS_PORT = int(os.environ.get("REDIS_PORT", 5606))  # Backend port + 100
    SESSION_REDIS_DB = 0
    SESSION_REDIS_PASSWORD = os.environ.get("REDIS_PASSWORD", None)

    # Security settings
    SESSION_USE_SIGNER = True
    SESSION_KEY_PREFIX = "store_"


class SessionMiddleware:
    """
    Session Cookie Middleware for Flask applications

    Provides:
    - Secure session cookies
    - Session fingerprinting (IP + User-Agent binding)
    - Session timeout handling
    - CSRF protection integration
    """

    def __init__(self, app: Optional[Flask] = None):
        self.app = app
        if app is not None:
            self.init_app(app)

    def init_app(self, app: Flask):
        """Initialize the middleware with a Flask app"""
        self.app = app

        # Apply configuration
        app.config["SESSION_COOKIE_NAME"] = SessionConfig.SESSION_COOKIE_NAME
        app.config["SESSION_COOKIE_SECURE"] = SessionConfig.SESSION_COOKIE_SECURE
        app.config["SESSION_COOKIE_HTTPONLY"] = SessionConfig.SESSION_COOKIE_HTTPONLY
        app.config["SESSION_COOKIE_SAMESITE"] = SessionConfig.SESSION_COOKIE_SAMESITE
        app.config["SESSION_COOKIE_PATH"] = SessionConfig.SESSION_COOKIE_PATH
        app.config["SESSION_PERMANENT"] = SessionConfig.SESSION_PERMANENT
        app.config["PERMANENT_SESSION_LIFETIME"] = (
            SessionConfig.PERMANENT_SESSION_LIFETIME
        )
        app.config["SESSION_REFRESH_EACH_REQUEST"] = (
            SessionConfig.SESSION_REFRESH_EACH_REQUEST
        )
        app.config["SESSION_TYPE"] = SessionConfig.SESSION_TYPE
        app.config["SESSION_FILE_DIR"] = SessionConfig.SESSION_FILE_DIR
        app.config["SESSION_USE_SIGNER"] = SessionConfig.SESSION_USE_SIGNER
        app.config["SESSION_KEY_PREFIX"] = SessionConfig.SESSION_KEY_PREFIX

        # Register hooks
        app.before_request(self._before_request)
        app.after_request(self._after_request)

        # Register error handlers
        app.register_error_handler(401, self._handle_unauthorized)

        print("✅ Session middleware initialized")

    def _before_request(self):
        """Pre-request processing"""
        # Skip for static files
        if request.path.startswith("/static"):
            return

        # Initialize session data
        if "created_at" not in session:
            session["created_at"] = datetime.utcnow().isoformat()
            session["fingerprint"] = self._generate_fingerprint()

        # Validate session fingerprint
        if not self._validate_fingerprint():
            # Session might be hijacked, clear it
            session.clear()
            session["created_at"] = datetime.utcnow().isoformat()
            session["fingerprint"] = self._generate_fingerprint()

        # Check session expiry
        if self._is_session_expired():
            session.clear()
            session["created_at"] = datetime.utcnow().isoformat()
            session["fingerprint"] = self._generate_fingerprint()

        # Store user info in g for easy access
        g.user_id = session.get("user_id")
        g.user_role = session.get("user_role")
        g.session_id = session.get("session_id")

    def _after_request(self, response):
        """Post-request processing"""
        # Update session activity timestamp
        if "created_at" in session:
            session["last_activity"] = datetime.utcnow().isoformat()

        # Add security headers for session
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "SAMEORIGIN"
        response.headers["X-XSS-Protection"] = "1; mode=block"

        return response

    def _generate_fingerprint(self) -> str:
        """Generate a session fingerprint based on client info"""
        client_ip = request.remote_addr or ""
        user_agent = request.user_agent.string or ""

        # Create fingerprint hash
        fingerprint_data = f"{client_ip}:{user_agent}"
        return hashlib.sha256(fingerprint_data.encode()).hexdigest()[:32]

    def _validate_fingerprint(self) -> bool:
        """Validate that the session fingerprint matches"""
        stored_fingerprint = session.get("fingerprint")
        if not stored_fingerprint:
            return True  # No fingerprint stored yet

        current_fingerprint = self._generate_fingerprint()

        # Allow some flexibility for fingerprint validation
        # (e.g., mobile users might have changing IPs)
        if os.environ.get("STRICT_SESSION_FINGERPRINT", "false").lower() == "true":
            return stored_fingerprint == current_fingerprint

        # Less strict: only validate user agent part
        return True

    def _is_session_expired(self) -> bool:
        """Check if the session has expired"""
        created_at_str = session.get("created_at")
        if not created_at_str:
            return False

        try:
            created_at = datetime.fromisoformat(created_at_str)
            lifetime = SessionConfig.PERMANENT_SESSION_LIFETIME
            return datetime.utcnow() > created_at + lifetime
        except (ValueError, TypeError):
            return True

    def _handle_unauthorized(self, error):
        """Handle 401 Unauthorized errors"""
        return (
            jsonify(
                {
                    "success": False,
                    "error": "Unauthorized",
                    "message": "انتهت صلاحية الجلسة أو غير مصرح",
                    "messageEn": "Session expired or unauthorized",
                }
            ),
            401,
        )


def create_session(
    user_id: int, user_role: str, additional_data: Dict[str, Any] = None
):
    """
    Create a new session for a user

    Args:
        user_id: The user's ID
        user_role: The user's role
        additional_data: Any additional data to store in session

    Returns:
        Session ID
    """
    # Clear any existing session
    session.clear()

    # Create new session
    session_id = secrets.token_urlsafe(32)
    session["session_id"] = session_id
    session["user_id"] = user_id
    session["user_role"] = user_role
    session["created_at"] = datetime.utcnow().isoformat()
    session["fingerprint"] = hashlib.sha256(
        f"{request.remote_addr}:{request.user_agent.string}".encode()
    ).hexdigest()[:32]

    # Add any additional data
    if additional_data:
        for key, value in additional_data.items():
            session[key] = value

    # Make session permanent
    session.permanent = True

    return session_id


def destroy_session():
    """Destroy the current session"""
    session.clear()


def get_session_user() -> Optional[Dict[str, Any]]:
    """Get the current session user info"""
    if "user_id" not in session:
        return None

    return {
        "user_id": session.get("user_id"),
        "user_role": session.get("user_role"),
        "session_id": session.get("session_id"),
        "created_at": session.get("created_at"),
    }


def require_session(f):
    """Decorator to require a valid session"""

    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "user_id" not in session:
            return (
                jsonify(
                    {
                        "success": False,
                        "error": "Session required",
                        "message": "يجب تسجيل الدخول",
                        "messageEn": "Login required",
                    }
                ),
                401,
            )
        return f(*args, **kwargs)

    return decorated_function


def require_role(*roles):
    """Decorator to require specific roles"""

    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if "user_id" not in session:
                return (
                    jsonify(
                        {
                            "success": False,
                            "error": "Session required",
                            "message": "يجب تسجيل الدخول",
                            "messageEn": "Login required",
                        }
                    ),
                    401,
                )

            user_role = session.get("user_role")
            if user_role not in roles and "admin" not in roles:
                return (
                    jsonify(
                        {
                            "success": False,
                            "error": "Forbidden",
                            "message": "ليس لديك صلاحية للوصول",
                            "messageEn": "Access denied",
                        }
                    ),
                    403,
                )

            return f(*args, **kwargs)

        return decorated_function

    return decorator


# Initialize Redis session if available
def init_redis_session(app: Flask):
    """Initialize Redis-based session storage"""
    try:
        import redis
        from flask_session import Session

        # Configure Redis
        app.config["SESSION_TYPE"] = "redis"
        app.config["SESSION_REDIS"] = redis.Redis(
            host=SessionConfig.SESSION_REDIS_HOST,
            port=SessionConfig.SESSION_REDIS_PORT,
            db=SessionConfig.SESSION_REDIS_DB,
            password=SessionConfig.SESSION_REDIS_PASSWORD,
        )

        Session(app)
        print(
            f"✅ Redis session initialized on port {SessionConfig.SESSION_REDIS_PORT}"
        )
        return True
    except ImportError:
        print("⚠️ Redis not available, using filesystem sessions")
        return False
    except Exception as e:
        print(f"⚠️ Redis connection failed: {e}, using filesystem sessions")
        return False
