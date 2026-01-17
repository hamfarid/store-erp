"""
Circuit Breaker Management Routes

Provides REST API endpoints for monitoring and managing circuit breakers.

Endpoints:
- GET /api/circuit-breakers - List all circuit breakers and their status
- GET /api/circuit-breakers/{name} - Get specific breaker metrics
- POST /api/circuit-breakers/{name}/reset - Reset a circuit breaker
- POST /api/circuit-breakers/reset-all - Reset all circuit breakers
"""

from flask import Blueprint, jsonify, request
from functools import wraps
import logging

logger = logging.getLogger(__name__)

circuit_breaker_bp = Blueprint("circuit_breaker", __name__, url_prefix="/api")


def require_admin(f):
    """Decorator to require admin role for circuit breaker management"""

    @wraps(f)
    def decorated_function(*args, **kwargs):
        # TODO: Implement proper admin check
        # For now, allow all authenticated users
        return f(*args, **kwargs)

    return decorated_function


@circuit_breaker_bp.route("/circuit-breakers", methods=["GET"])
def list_circuit_breakers():
    """
    List all circuit breakers and their current status.

    Response:
    {
        "breakers": {
            "database": {
                "state": "closed",
                "failures_total": 5,
                "successes_total": 100,
                "failure_rate": 0.048,
                ...
            },
            ...
        }
    }
    """
    try:
        from services.circuit_breaker_manager import get_circuit_breaker_manager

        manager = get_circuit_breaker_manager()
        metrics = manager.get_all_metrics()

        return (
            jsonify({"success": True, "breakers": metrics, "count": len(metrics)}),
            200,
        )
    except Exception as e:
        logger.error(f"Error listing circuit breakers: {e}")
        return jsonify({"success": False, "error": str(e)}), 500


@circuit_breaker_bp.route("/circuit-breakers/<name>", methods=["GET"])
def get_circuit_breaker(name):
    """
    Get metrics for a specific circuit breaker.

    Args:
        name: Circuit breaker name (database, external_api, cache, rag_service)

    Response:
    {
        "success": true,
        "breaker": {
            "name": "database",
            "state": "closed",
            "failures_total": 5,
            ...
        }
    }
    """
    try:
        from services.circuit_breaker_manager import get_circuit_breaker_manager

        manager = get_circuit_breaker_manager()
        metrics = manager.get_breaker_metrics(name)

        if not metrics:
            return (
                jsonify(
                    {"success": False, "error": f"Circuit breaker '{name}' not found"}
                ),
                404,
            )

        return jsonify({"success": True, "breaker": metrics}), 200
    except Exception as e:
        logger.error(f"Error getting circuit breaker '{name}': {e}")
        return jsonify({"success": False, "error": str(e)}), 500


@circuit_breaker_bp.route("/circuit-breakers/<name>/reset", methods=["POST"])
@require_admin
def reset_circuit_breaker(name):
    """
    Reset a circuit breaker to CLOSED state.

    Args:
        name: Circuit breaker name

    Response:
    {
        "success": true,
        "message": "Circuit breaker 'database' reset to CLOSED"
    }
    """
    try:
        from services.circuit_breaker_manager import get_circuit_breaker_manager

        manager = get_circuit_breaker_manager()

        if manager.reset_breaker(name):
            return (
                jsonify(
                    {
                        "success": True,
                        "message": f"Circuit breaker '{name}' reset to CLOSED",
                    }
                ),
                200,
            )
        else:
            return (
                jsonify(
                    {"success": False, "error": f"Circuit breaker '{name}' not found"}
                ),
                404,
            )
    except Exception as e:
        logger.error(f"Error resetting circuit breaker '{name}': {e}")
        return jsonify({"success": False, "error": str(e)}), 500


@circuit_breaker_bp.route("/circuit-breakers/reset-all", methods=["POST"])
@require_admin
def reset_all_circuit_breakers():
    """
    Reset all circuit breakers to CLOSED state.

    Response:
    {
        "success": true,
        "message": "All circuit breakers reset to CLOSED"
    }
    """
    try:
        from services.circuit_breaker_manager import get_circuit_breaker_manager

        manager = get_circuit_breaker_manager()
        manager.reset_all()

        return (
            jsonify(
                {"success": True, "message": "All circuit breakers reset to CLOSED"}
            ),
            200,
        )
    except Exception as e:
        logger.error(f"Error resetting all circuit breakers: {e}")
        return jsonify({"success": False, "error": str(e)}), 500


@circuit_breaker_bp.route("/circuit-breakers/health", methods=["GET"])
def circuit_breaker_health():
    """
    Get overall circuit breaker health status.

    Response:
    {
        "success": true,
        "health": "healthy",
        "open_breakers": [],
        "half_open_breakers": ["external_api"],
        "closed_breakers": ["database", "cache", "rag_service"]
    }
    """
    try:
        from services.circuit_breaker_manager import get_circuit_breaker_manager

        manager = get_circuit_breaker_manager()
        metrics = manager.get_all_metrics()

        open_breakers = [m["name"] for m in metrics.values() if m["state"] == "open"]
        half_open_breakers = [
            m["name"] for m in metrics.values() if m["state"] == "half_open"
        ]
        closed_breakers = [
            m["name"] for m in metrics.values() if m["state"] == "closed"
        ]

        health = "healthy" if not open_breakers else "degraded"

        return (
            jsonify(
                {
                    "success": True,
                    "health": health,
                    "open_breakers": open_breakers,
                    "half_open_breakers": half_open_breakers,
                    "closed_breakers": closed_breakers,
                    "total_breakers": len(metrics),
                }
            ),
            200,
        )
    except Exception as e:
        logger.error(f"Error getting circuit breaker health: {e}")
        return jsonify({"success": False, "error": str(e)}), 500
