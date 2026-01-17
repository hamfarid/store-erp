"""
File: config/ports.py
Port configuration - Single Source of Truth

This file manages all port configurations for the application.
MUST be imported at application startup.
"""

import os
import sys


# ============================================================================
# Port Configuration
# ============================================================================

def get_port(env_var: str, default: int) -> int:
    """Get port from environment with validation"""
    try:
        port = int(os.getenv(env_var, default))
    except ValueError:
        print(f"ERROR: Invalid {env_var} value. Must be an integer.")
        sys.exit(1)
    
    if not (1024 <= port <= 65535):
        print(f"ERROR: {env_var}={port} is invalid. Must be 1024-65535.")
        sys.exit(1)
    
    return port


# Backend port
BACKEND_PORT = get_port('BACKEND_PORT', 8000)

# Frontend port
FRONTEND_PORT = get_port('FRONTEND_PORT', 3000)

# Database port
DATABASE_PORT = get_port('DATABASE_PORT', 5432)

# Redis port
REDIS_PORT = get_port('REDIS_PORT', 6379)


# ============================================================================
# Port Conflict Detection
# ============================================================================

ports = {
    'BACKEND_PORT': BACKEND_PORT,
    'FRONTEND_PORT': FRONTEND_PORT,
    'DATABASE_PORT': DATABASE_PORT,
    'REDIS_PORT': REDIS_PORT,
}

# Check for conflicts
port_values = list(ports.values())
if len(port_values) != len(set(port_values)):
    conflicts = []
    for name1, port1 in ports.items():
        for name2, port2 in ports.items():
            if name1 < name2 and port1 == port2:
                conflicts.append(f"{name1} and {name2} both use port {port1}")
    
    print("ERROR: Port conflicts detected:")
    for conflict in conflicts:
        print(f"  - {conflict}")
    sys.exit(1)


# ============================================================================
# Export
# ============================================================================

__all__ = [
    'BACKEND_PORT',
    'FRONTEND_PORT',
    'DATABASE_PORT',
    'REDIS_PORT',
]


# Print configuration on import (only in development)
if os.getenv('APP_ENV') == 'development':
    print(f"Port Configuration:")
    print(f"  Backend:  {BACKEND_PORT}")
    print(f"  Frontend: {FRONTEND_PORT}")
    print(f"  Database: {DATABASE_PORT}")
    print(f"  Redis:    {REDIS_PORT}")
