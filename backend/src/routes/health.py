"""
Health Check Routes
Provides health check endpoints for monitoring and load balancers.
"""

from flask import Blueprint, jsonify
from datetime import datetime
import os
import psutil

health_bp = Blueprint('health', __name__)


@health_bp.route('/health', methods=['GET'])
def health_check():
    """
    Basic health check endpoint.
    Returns 200 if the service is running.
    """
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.utcnow().isoformat(),
        'version': os.getenv('APP_VERSION', '2.0.0')
    }), 200


@health_bp.route('/health/detailed', methods=['GET'])
def detailed_health_check():
    """
    Detailed health check with system metrics.
    """
    try:
        # System metrics
        cpu_percent = psutil.cpu_percent(interval=0.1)
        memory = psutil.virtual_memory()
        disk = psutil.disk_usage('/')
        
        # Database check
        db_status = check_database()
        
        health_data = {
            'status': 'healthy' if db_status else 'degraded',
            'timestamp': datetime.utcnow().isoformat(),
            'version': os.getenv('APP_VERSION', '2.0.0'),
            'checks': {
                'database': {
                    'status': 'healthy' if db_status else 'unhealthy',
                    'message': 'Connected' if db_status else 'Connection failed'
                },
                'system': {
                    'status': 'healthy',
                    'cpu_percent': cpu_percent,
                    'memory_percent': memory.percent,
                    'disk_percent': disk.percent
                }
            },
            'metrics': {
                'cpu': {
                    'percent': cpu_percent
                },
                'memory': {
                    'total': memory.total,
                    'available': memory.available,
                    'percent': memory.percent
                },
                'disk': {
                    'total': disk.total,
                    'used': disk.used,
                    'free': disk.free,
                    'percent': disk.percent
                }
            }
        }
        
        status_code = 200 if db_status else 503
        return jsonify(health_data), status_code
        
    except Exception as e:
        return jsonify({
            'status': 'unhealthy',
            'timestamp': datetime.utcnow().isoformat(),
            'error': str(e)
        }), 503


@health_bp.route('/health/ready', methods=['GET'])
def readiness_check():
    """
    Readiness check for Kubernetes/load balancers.
    Returns 200 only when the service is ready to accept traffic.
    """
    try:
        # Check database connection
        db_ready = check_database()
        
        if db_ready:
            return jsonify({
                'status': 'ready',
                'timestamp': datetime.utcnow().isoformat()
            }), 200
        else:
            return jsonify({
                'status': 'not_ready',
                'reason': 'database_unavailable',
                'timestamp': datetime.utcnow().isoformat()
            }), 503
            
    except Exception as e:
        return jsonify({
            'status': 'not_ready',
            'reason': str(e),
            'timestamp': datetime.utcnow().isoformat()
        }), 503


@health_bp.route('/health/live', methods=['GET'])
def liveness_check():
    """
    Liveness check for Kubernetes.
    Returns 200 if the application is alive (not deadlocked).
    """
    return jsonify({
        'status': 'alive',
        'timestamp': datetime.utcnow().isoformat()
    }), 200


def check_database():
    """
    Check database connectivity.
    """
    try:
        from src.database import db
        # Execute a simple query
        db.session.execute('SELECT 1')
        return True
    except Exception:
        try:
            # Alternative check using text()
            from sqlalchemy import text
            from src.database import db
            db.session.execute(text('SELECT 1'))
            return True
        except Exception:
            return False


@health_bp.route('/api/health', methods=['GET'])
def api_health():
    """
    API health endpoint at /api/health for consistency.
    """
    return health_check()


@health_bp.route('/api/health/detailed', methods=['GET'])
def api_detailed_health():
    """
    API detailed health at /api/health/detailed.
    """
    return detailed_health_check()
