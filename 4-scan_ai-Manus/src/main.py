#!/usr/bin/env python3
"""
Main entry point for the AI Agricultural System
This module provides the FastAPI application and core functionality.
"""

import sys
import logging
import time
from pathlib import Path
from typing import Dict, Any, List
from datetime import datetime, timedelta

from fastapi import FastAPI, Depends, HTTPException, Request, Response
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST
import jwt

# Add parent directory to path to allow imports when running directly
if __name__ == "__main__":
    sys.path.append(str(Path(__file__).parent.parent))

# Import configuration
from config import settings

# Try different import methods to handle various execution contexts
try:
    from database import init_db, check_db_health
    from modules.image_processing.image_processor import ImageProcessor
    from modules.disease_diagnosis.service import DiseaseDiagnosisService
    from modules.ai_management.service import AIManagementService
    from modules.setup_wizard.api import router as setup_wizard_router
    from api_router import main_router  # إضافة الموجه الموحد
except ImportError:
    try:
        from .database import init_db, check_db_health
        from .modules.image_processing.image_processor import ImageProcessor
        from .modules.disease_diagnosis.service import DiseaseDiagnosisService
        from .modules.ai_management.service import AIManagementService
        from .modules.setup_wizard.api import router as setup_wizard_router
        from .api_router import main_router  # إضافة الموجه الموحد
    except ImportError:
        from src.database import init_db, check_db_health
        from src.modules.image_processing.image_processor import ImageProcessor
        from src.modules.disease_diagnosis.service import DiseaseDiagnosisService
        from src.modules.ai_management.service import AIManagementService
        from src.modules.setup_wizard.api import router as setup_wizard_router
        from src.api_router import main_router  # إضافة الموجه الموحد

# Configure logging
logging.basicConfig(
    level=getattr(logging, settings.LOG_LEVEL),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Security settings from config
SECRET_KEY = settings.SECRET_KEY
ALGORITHM = settings.ALGORITHM
ACCESS_TOKEN_EXPIRE_MINUTES = settings.ACCESS_TOKEN_EXPIRE_MINUTES

# Rate limiting settings from config
RATE_LIMIT_REQUESTS_PER_MINUTE = settings.RATE_LIMIT_REQUESTS_PER_MINUTE
RATE_LIMIT_REQUESTS_PER_HOUR = settings.RATE_LIMIT_REQUESTS_PER_HOUR
request_counts: Dict[str, Dict[str, int]] = {}

# Available modules
AVAILABLE_MODULES: List[str] = [
    "image_processing",
    "disease_diagnosis",
    "ai_service"
]

# Create FastAPI app
app = FastAPI(
    title="AI Agricultural System",
    description="API for agricultural image processing and disease diagnosis",
    version="1.0.0"
)

# Include routers
app.include_router(setup_wizard_router)
app.include_router(main_router)  # إضافة الموجه الموحد

# Security
security = HTTPBearer()

# Prometheus metrics
REQUEST_COUNT = Counter(
    'http_requests_total',
    'Total HTTP requests',
    ['method', 'endpoint', 'status']
)

REQUEST_LATENCY = Histogram(
    'http_request_duration_seconds',
    'HTTP request latency',
    ['method', 'endpoint']
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=settings.ALLOWED_METHODS,
    allow_headers=settings.ALLOWED_HEADERS,
)

# Rate limiting middleware


@app.middleware("http")
async def rate_limit_middleware(request: Request, call_next):
    client_id = request.client.host
    if not check_rate_limit(client_id):
        return JSONResponse(
            status_code=429,
            content={"detail": "Too many requests"}
        )
    response = await call_next(request)
    return response


def check_rate_limit(client_id: str) -> bool:
    """
    Check if a client has exceeded rate limits

    Args:
        client_id (str): Client identifier (IP address)

    Returns:
        bool: True if within limits, False if exceeded
    """
    now = datetime.now()
    if client_id not in request_counts:
        request_counts[client_id] = {
            "minute": {"count": 0, "reset_time": now + timedelta(minutes=1)},
            "hour": {"count": 0, "reset_time": now + timedelta(hours=1)}
        }

    # Reset counters if needed
    for period in ["minute", "hour"]:
        if now >= request_counts[client_id][period]["reset_time"]:
            request_counts[client_id][period]["count"] = 0
            request_counts[client_id][period]["reset_time"] = now + timedelta(
                minutes=1 if period == "minute" else 60
            )

    # Check limits
    if (request_counts[client_id]["minute"]["count"] >= RATE_LIMIT_REQUESTS_PER_MINUTE
            or request_counts[client_id]["hour"]["count"] >= RATE_LIMIT_REQUESTS_PER_HOUR):
        return False

    # Increment counters
    request_counts[client_id]["minute"]["count"] += 1
    request_counts[client_id]["hour"]["count"] += 1
    return True


def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)) -> str:
    """
    Verify JWT token and return user ID

    Args:
        credentials (HTTPAuthorizationCredentials): JWT token credentials

    Returns:
        str: User ID from token

    Raises:
        HTTPException: If token is invalid or expired
    """
    try:
        token = credentials.credentials
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise HTTPException(status_code=401, detail="Invalid token")
        return user_id
    except jwt.ExpiredSignatureError as exc:
        raise HTTPException(status_code=401, detail="Token has expired") from exc
    except Exception as exc:
        raise HTTPException(status_code=401, detail="Invalid token") from exc


# Cache for module status
module_status_cache: Dict[str, Any] = {}
CACHE_EXPIRY = 300  # 5 minutes


def get_cached_module_status() -> Dict[str, Any]:
    """
    Get cached module status

    Returns:
        Dict[str, Any]: Cached module status
    """
    if module_status_cache and time.time() - module_status_cache.get("timestamp", 0) < CACHE_EXPIRY:
        return module_status_cache["status"]
    return None


def load_modules() -> bool:
    """
    Load system modules

    Returns:
        bool: True if all modules loaded successfully
    """
    try:
        # Try to initialize database, but don't fail if it's not available
        try:
            init_db()
            logger.info("Database initialized successfully")
        except Exception as e:
            logger.warning("Database initialization failed: %s", str(e))
            logger.warning("Application will start without database connection")

        # Initialize services (they should handle missing DB gracefully)
        try:
            # Test that services can be initialized
            ImageProcessor()
            DiseaseDiagnosisService()
            AIManagementService()

            # Log module status
            logger.info("Module loading status:")
            logger.info("Database: %s", 'Connected' if check_db_health()['status'] == 'healthy' else 'Failed')
            logger.info("Image Processing Service: Ready")
            logger.info("Disease Diagnosis Service: Ready")
            logger.info("AI Service: Ready")
        except Exception as e:
            logger.warning("Some services failed to initialize: %s", str(e))

        return True
    except Exception as e:
        logger.error("Critical error loading modules: %s", str(e))
        return False


# Security headers middleware
@app.middleware("http")
async def add_security_headers(request: Request, call_next):
    response = await call_next(request)
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["X-XSS-Protection"] = "1; mode=block"
    response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
    response.headers["Content-Security-Policy"] = "default-src 'self'"
    return response


# Root endpoint
@app.get("/")
async def root():
    """
    Root endpoint - Welcome page

    Returns:
        Dict[str, Any]: Welcome message and useful links
    """
    return {
        "message": "Welcome to Gaara AI Agricultural System",
        "version": "1.0.0",
        "description": "AI-powered agricultural disease diagnosis and image processing system",
        "links": {
            "documentation": "/docs",
            "alternative_docs": "/redoc",
            "health_check": "/health",
            "module_status": "/modules/status",
            "api_schema": "/openapi.json"
        },
        "available_modules": [
            "Disease Diagnosis",
            "Image Processing",
            "AI Management",
            "Plant Hybridization"
        ],
        "timestamp": datetime.now().isoformat()
    }


# Health check endpoint
@app.get("/health")
async def health_check():
    """
    Health check endpoint

    Returns:
        Dict[str, Any]: Health status
    """
    db_health = check_db_health()
    return {
        "status": "healthy" if db_health else "unhealthy",
        "timestamp": datetime.now().isoformat(),
        "database": "connected" if db_health else "disconnected"
    }


# Metrics endpoint
@app.get("/metrics")
async def metrics():
    """
    Prometheus metrics endpoint

    Returns:
        Response: Prometheus metrics
    """
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)


# Module status endpoint
@app.get("/modules/status")
async def get_module_status():
    """
    Get status of all modules

    Returns:
        Dict[str, Any]: Module status
    """
    cached_status = get_cached_module_status()
    if cached_status:
        return cached_status

    status = {
        "timestamp": datetime.now().isoformat(),
        "modules": {}
    }

    for module in AVAILABLE_MODULES:
        try:
            if module == "image_processing":
                ImageProcessor()  # Test initialization
                status["modules"][module] = {
                    "status": "ready",
                    "version": "1.0.0"
                }
            elif module == "disease_diagnosis":
                DiseaseDiagnosisService()  # Test initialization
                status["modules"][module] = {
                    "status": "ready",
                    "version": "1.0.0"
                }
            elif module == "ai_service":
                AIManagementService()  # Test initialization
                status["modules"][module] = {
                    "status": "ready",
                    "version": "1.0.0"
                }
        except Exception as e:
            status["modules"][module] = {
                "status": "error",
                "error": str(e)
            }

    module_status_cache["status"] = status
    module_status_cache["timestamp"] = time.time()
    return status


# Global exception handler
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """
    Global exception handler

    Args:
        request (Request): FastAPI request
        exc (Exception): Exception

    Returns:
        JSONResponse: Error response
    """
    logger.error("Unhandled exception: %s", str(exc))
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error"}
    )


# Startup event
@app.on_event("startup")
async def startup_event():
    """
    Startup event handler
    """
    logger.info("Starting AI Agricultural System...")
    if not load_modules():
        logger.error("Failed to load modules")
        raise RuntimeError("Failed to load modules")
    logger.info("AI Agricultural System started successfully")


# Main entry point
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host=settings.API_HOST, port=settings.API_PORT)
