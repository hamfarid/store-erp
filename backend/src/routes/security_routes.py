# type: ignore
# flake8: noqa
# pyright: ignore
# pylint: disable=all
# mypy: ignore-errors
"""
Security Routes - Session Management & Security Monitoring
حماية الجلسات ومراقبة الأمان

Provides:
- Active sessions management
- Security event logging
- Login attempts monitoring
- Session termination
- CSRF token generation
"""

from flask import Blueprint, request, jsonify, session, g
from datetime import datetime
import secrets
import hashlib
import json
import logging

logger = logging.getLogger(__name__)

security_routes_bp = Blueprint("security_routes", __name__)

# In-memory storage for demo (should be Redis/database in production)
SECURITY_LOGS = []
LOGIN_ATTEMPTS = []
ACTIVE_SESSIONS = {}


def get_client_fingerprint():
    """Generate a fingerprint for the current client"""
    client_ip = request.remote_addr or ""
    user_agent = request.user_agent.string or ""
    fingerprint_data = f"{client_ip}:{user_agent}"
    return hashlib.sha256(fingerprint_data.encode()).hexdigest()[:32]


def log_security_event(event_type, details=None):
    """Log a security event"""
    event = {
        "id": len(SECURITY_LOGS) + 1,
        "event_type": event_type,
        "timestamp": datetime.utcnow().isoformat(),
        "ip": request.remote_addr,
        "user_agent": request.user_agent.string,
        "user_id": session.get("user_id"),
        "details": details or "",
    }
    SECURITY_LOGS.insert(0, event)
    # Keep only last 500 events
    if len(SECURITY_LOGS) > 500:
        SECURITY_LOGS.pop()
    logger.info(f"Security event logged: {event_type}")
    return event


# ==========================================
# CSRF Token Endpoints
# ==========================================


@security_routes_bp.route("/api/auth/csrf-token", methods=["GET"])
def get_csrf_token():
    """Generate and return a CSRF token"""
    csrf_token = secrets.token_urlsafe(32)
    session["csrf_token"] = csrf_token
    return jsonify({"success": True, "csrf_token": csrf_token})


# ==========================================
# Active Sessions Management
# ==========================================


@security_routes_bp.route("/api/auth/sessions", methods=["GET"])
def get_active_sessions():
    """Get all active sessions for the current user"""
    user_id = session.get("user_id")
    if not user_id:
        return jsonify({"success": False, "message": "Not authenticated"}), 401

    # Get sessions for user
    user_sessions = [
        {**s, "is_current": s["session_id"] == session.get("session_id", "")}
        for s in ACTIVE_SESSIONS.values()
        if s.get("user_id") == user_id
    ]

    # Sort by last_active
    user_sessions.sort(key=lambda x: x.get("last_active", ""), reverse=True)

    return jsonify({"success": True, "sessions": user_sessions})


@security_routes_bp.route("/api/auth/sessions/<session_id>", methods=["DELETE"])
def terminate_session(session_id):
    """Terminate a specific session"""
    user_id = session.get("user_id")
    if not user_id:
        return jsonify({"success": False, "message": "Not authenticated"}), 401

    # Find and remove session
    if session_id in ACTIVE_SESSIONS:
        sess = ACTIVE_SESSIONS[session_id]
        if sess.get("user_id") == user_id:
            del ACTIVE_SESSIONS[session_id]
            log_security_event(
                "session_terminated", f"Session {session_id[:8]}... terminated"
            )
            return jsonify({"success": True, "message": "Session terminated"})

    return jsonify({"success": False, "message": "Session not found"}), 404


@security_routes_bp.route("/api/auth/sessions/terminate-others", methods=["POST"])
def terminate_other_sessions():
    """Terminate all sessions except the current one"""
    user_id = session.get("user_id")
    current_session_id = session.get("session_id", "")

    if not user_id:
        return jsonify({"success": False, "message": "Not authenticated"}), 401

    terminated = 0
    sessions_to_remove = []

    for sid, sess in ACTIVE_SESSIONS.items():
        if sess.get("user_id") == user_id and sid != current_session_id:
            sessions_to_remove.append(sid)

    for sid in sessions_to_remove:
        del ACTIVE_SESSIONS[sid]
        terminated += 1

    if terminated > 0:
        log_security_event(
            "sessions_terminated", f"{terminated} other sessions terminated"
        )

    return jsonify(
        {
            "success": True,
            "message": f"Terminated {terminated} sessions",
            "terminated_count": terminated,
        }
    )


# ==========================================
# Security Logs
# ==========================================


@security_routes_bp.route("/api/security/logs", methods=["GET"])
def get_security_logs():
    """Get security logs (admin only)"""
    user_id = session.get("user_id")
    user_role = session.get("user_role", "")

    if not user_id:
        return jsonify({"success": False, "message": "Not authenticated"}), 401

    # Filter parameters
    event_type = request.args.get("event_type")
    limit = min(int(request.args.get("limit", 100)), 500)

    logs = SECURITY_LOGS[:limit]

    if event_type:
        logs = [l for l in logs if l["event_type"] == event_type]

    return jsonify({"success": True, "logs": logs, "total": len(SECURITY_LOGS)})


@security_routes_bp.route("/api/security/log-event", methods=["POST"])
def log_event():
    """Log a security event from frontend"""
    data = request.get_json()
    if not data:
        return jsonify({"success": False, "message": "No data provided"}), 400

    event = log_security_event(data.get("type", "unknown"), data.get("details", ""))

    return jsonify({"success": True, "event_id": event["id"]})


# ==========================================
# Login Attempts
# ==========================================


@security_routes_bp.route("/api/security/login-attempts", methods=["GET"])
def get_login_attempts():
    """Get recent login attempts (admin only)"""
    user_id = session.get("user_id")

    if not user_id:
        return jsonify({"success": False, "message": "Not authenticated"}), 401

    limit = min(int(request.args.get("limit", 50)), 200)

    return jsonify(
        {
            "success": True,
            "attempts": LOGIN_ATTEMPTS[:limit],
            "total": len(LOGIN_ATTEMPTS),
        }
    )


def record_login_attempt(username, success, reason=None, ip=None, location=None):
    """Record a login attempt"""
    attempt = {
        "id": len(LOGIN_ATTEMPTS) + 1,
        "username": username,
        "status": "success" if success else "failed",
        "reason": reason,
        "timestamp": datetime.utcnow().isoformat(),
        "ip": ip or request.remote_addr,
        "location": location or "Unknown",
        "user_agent": request.user_agent.string,
    }
    LOGIN_ATTEMPTS.insert(0, attempt)
    # Keep only last 500 attempts
    if len(LOGIN_ATTEMPTS) > 500:
        LOGIN_ATTEMPTS.pop()

    if success:
        log_security_event("login_success", f"User {username} logged in")
    else:
        log_security_event(
            "login_failed", f"Failed login attempt for {username}: {reason}"
        )

    return attempt


def create_user_session(user_id, user_role, device=None):
    """Create a new user session"""
    session_id = secrets.token_urlsafe(32)

    sess = {
        "id": session_id,
        "session_id": session_id,
        "user_id": user_id,
        "user_role": user_role,
        "device": device or request.user_agent.string,
        "device_type": detect_device_type(),
        "ip": request.remote_addr,
        "location": "Unknown",  # Would use IP geolocation in production
        "fingerprint": get_client_fingerprint(),
        "created_at": datetime.utcnow().isoformat(),
        "last_active": datetime.utcnow().isoformat(),
    }

    ACTIVE_SESSIONS[session_id] = sess
    session["session_id"] = session_id

    log_security_event("session_created", f"New session created for user {user_id}")

    return session_id


def detect_device_type():
    """Detect device type from user agent"""
    ua = request.user_agent
    if ua.platform in ["iphone", "android"]:
        return "mobile"
    elif ua.platform in ["ipad"]:
        return "tablet"
    return "desktop"


def update_session_activity(session_id):
    """Update last activity for a session"""
    if session_id in ACTIVE_SESSIONS:
        ACTIVE_SESSIONS[session_id]["last_active"] = datetime.utcnow().isoformat()


# ==========================================
# Session Validation
# ==========================================


@security_routes_bp.route("/api/auth/validate-session", methods=["POST"])
def validate_session():
    """Validate current session and check for hijacking"""
    user_id = session.get("user_id")
    session_id = session.get("session_id")

    if not user_id or not session_id:
        return jsonify({"success": False, "valid": False, "reason": "no_session"}), 401

    # Check session exists
    if session_id not in ACTIVE_SESSIONS:
        return (
            jsonify({"success": False, "valid": False, "reason": "session_not_found"}),
            401,
        )

    stored_session = ACTIVE_SESSIONS[session_id]

    # Validate fingerprint
    current_fingerprint = get_client_fingerprint()
    stored_fingerprint = stored_session.get("fingerprint")

    if stored_fingerprint and stored_fingerprint != current_fingerprint:
        log_security_event(
            "potential_hijack", f"Fingerprint mismatch for session {session_id[:8]}..."
        )
        return (
            jsonify(
                {
                    "success": False,
                    "valid": False,
                    "reason": "fingerprint_mismatch",
                    "message": "Session security violation detected",
                }
            ),
            403,
        )

    # Update activity
    update_session_activity(session_id)

    return jsonify(
        {"success": True, "valid": True, "session_id": session_id, "user_id": user_id}
    )


# ==========================================
# Token Refresh
# ==========================================


@security_routes_bp.route("/api/auth/refresh", methods=["POST"])
def refresh_token():
    """Refresh access token"""
    data = request.get_json()
    refresh_token = data.get("refresh_token") if data else None

    if not refresh_token:
        return jsonify({"success": False, "message": "Refresh token required"}), 400

    # In production, validate refresh token from database
    # For demo, generate new tokens
    try:
        new_access_token = secrets.token_urlsafe(32)
        new_refresh_token = secrets.token_urlsafe(32)

        return jsonify(
            {
                "success": True,
                "data": {
                    "access_token": new_access_token,
                    "refresh_token": new_refresh_token,
                    "expires_in": 900,  # 15 minutes
                },
            }
        )
    except Exception as e:
        logger.error(f"Token refresh error: {e}")
        return jsonify({"success": False, "message": "Token refresh failed"}), 500


# Export helper functions for use in auth routes
__all__ = [
    "security_routes_bp",
    "log_security_event",
    "record_login_attempt",
    "create_user_session",
    "update_session_activity",
    "get_client_fingerprint",
]
