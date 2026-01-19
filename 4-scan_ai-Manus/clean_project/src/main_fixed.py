#!/usr/bin/env python3
"""
Main entry point for the AI Agricultural System
This file aggregates all API modules from subdirectories and provides a unified endpoint for the application
"""

from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, RedirectResponse, JSONResponse
from fastapi import FastAPI, Request
import uvicorn
import sys
import logging
from datetime import datetime
from pathlib import Path

# Add project root to sys.path (must be before module imports)
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

# Standard library imports

# Third-party imports

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("system.log"),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

# System information
SYSTEM_NAME = "Smart Agricultural AI System"
SYSTEM_VERSION = "1.0.0"
SYSTEM_DESCRIPTION = "Comprehensive AI-powered agricultural management system"

# Available modules
AVAILABLE_MODULES = [
    {"name": "ai_management", "title": "AI Management", "status": "loaded"},
    {"name": "image_processing", "title": "Image Processing", "status": "loaded"},
    {"name": "disease_diagnosis", "title": "Disease Diagnosis", "status": "loaded"},
    {"name": "backup_restore", "title": "Backup & Restore", "status": "loaded"},
    {"name": "settings", "title": "Settings", "status": "loaded"},
    {"name": "auth", "title": "Authentication", "status": "loaded"},
    {"name": "plant_hybridization", "title": "Plant Hybridization", "status": "loaded"},
    {"name": "resource_monitoring", "title": "Resource Monitoring", "status": "loaded"}
]

# Create FastAPI application
app = FastAPI(
    title=SYSTEM_NAME,
    description=SYSTEM_DESCRIPTION,
    version=SYSTEM_VERSION,
    docs_url="/docs",
    redoc_url="/redoc"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def load_modules():
    """Load all system modules"""
    try:
        # Load system modules
        from modules.auth import api as auth_api
        from modules.settings import api as settings_api
        from modules.backup_restore import api as backup_api
        from modules.ai_management import api as ai_api
        from modules.image_processing import api as image_api
        from modules.disease_diagnosis import api as disease_api

        # Register modules
        app.include_router(auth_api.router, prefix="/api/auth", tags=["Authentication"])
        app.include_router(settings_api.router, prefix="/api/settings", tags=["Settings"])
        app.include_router(backup_api.router, prefix="/api/backup", tags=["Backup"])
        app.include_router(ai_api.router, prefix="/api/ai", tags=["AI Management"])
        app.include_router(image_api.router, prefix="/api/image", tags=["Image Processing"])
        app.include_router(disease_api.router, prefix="/api/disease", tags=["Disease Diagnosis"])

        logger.info("All modules loaded successfully")
        return True

    except Exception as e:
        logger.error(f"Error loading modules: {e}")
        return False


# Basic system endpoints


@app.get("/")
async def root():
    """Root endpoint"""
    return RedirectResponse(url="/login")


@app.get("/health")
async def health_check():
    """System health check"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "modules": {
            "total": len(AVAILABLE_MODULES),
            "loaded": len([m for m in AVAILABLE_MODULES if m["status"] == "loaded"]),
            "failed": len([m for m in AVAILABLE_MODULES if m["status"] == "failed"])
        },
        "version": SYSTEM_VERSION
    }


@app.get("/api/modules/status")
async def get_modules_status():
    """Get status of all modules"""
    return {
        "modules": AVAILABLE_MODULES,
        "summary": {
            "total": len(AVAILABLE_MODULES),
            "loaded": len([m for m in AVAILABLE_MODULES if m["status"] == "loaded"]),
            "failed": len([m for m in AVAILABLE_MODULES if m["status"] == "failed"]),
            "success_rate": (len([m for m in AVAILABLE_MODULES if m["status"] == "loaded"]) / len(AVAILABLE_MODULES) * 100) if AVAILABLE_MODULES else 0
        },
        "timestamp": datetime.now().isoformat()
    }


@app.get("/api/info")
async def get_system_info():
    """System information"""
    return {
        "name": SYSTEM_NAME,
        "version": SYSTEM_VERSION,
        "description": SYSTEM_DESCRIPTION,
        "modules": len(AVAILABLE_MODULES),
        "status": "running",
        "timestamp": datetime.now().isoformat()
    }


@app.get("/login", response_class=HTMLResponse)
async def login_page(username: str = "", password: str = ""):
    """Main login screen"""
    username_value = username or 'admin'
    password_value = password or 'admin123'

    html = f"""
    <!DOCTYPE html>
    <html lang="ar" dir="rtl">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Login - {SYSTEM_NAME}</title>
        <style>
            * {{ margin: 0; padding: 0; box-sizing: border-box; }}
            body {{
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                min-height: 100vh;
                display: flex;
                align-items: center;
                justify-content: center;
                color: white;
            }}
            .login-container {{
                background: rgba(255, 255, 255, 0.1);
                padding: 3rem;
                border-radius: 20px;
                backdrop-filter: blur(10px);
                box-shadow: 0 8px 32px rgba(31, 38, 135, 0.37);
                border: 1px solid rgba(255, 255, 255, 0.18);
                max-width: 400px;
                width: 90%;
                text-align: center;
            }}
            h1 {{
                font-size: 2rem;
                margin-bottom: 1rem;
                color: #fff;
            }}
            .form-group {{
                margin: 1.5rem 0;
                text-align: right;
            }}
            label {{
                display: block;
                margin-bottom: 0.5rem;
                font-weight: 500;
            }}
            input {{
                width: 100%;
                padding: 0.8rem;
                border: none;
                border-radius: 10px;
                background: rgba(255, 255, 255, 0.2);
                color: white;
                font-size: 1rem;
            }}
            input::placeholder {{
                color: rgba(255, 255, 255, 0.7);
            }}
            .btn {{
                background: #4CAF50;
                color: white;
                border: none;
                padding: 1rem 2rem;
                border-radius: 25px;
                cursor: pointer;
                font-size: 1rem;
                width: 100%;
                transition: all 0.3s;
                margin: 1rem 0;
            }}
            .btn:hover {{
                background: #45a049;
                transform: translateY(-2px);
            }}
            .admin-info {{
                background: rgba(255, 255, 255, 0.1);
                padding: 1.5rem;
                border-radius: 10px;
                margin: 1.5rem 0;
                border: 1px solid rgba(255, 255, 255, 0.2);
                text-align: center;
            }}
            .admin-info h4 {{
                color: #4CAF50;
                margin-bottom: 1rem;
                font-size: 1.1rem;
            }}
            .admin-info p {{
                margin: 0.5rem 0;
                font-size: 1rem;
            }}
            .footer {{
                margin-top: 2rem;
                opacity: 0.8;
                font-size: 0.9rem;
            }}
        </style>
    </head>
    <body>
        <div class="login-container">
            <h1>🌱 {SYSTEM_NAME}</h1>
            <p>Login to access the system</p>

            <form onsubmit="handleLogin(event)">
                <div class="form-group">
                    <label for="username">Username:</label>
                    <input type="text" id="username" name="username" placeholder="Enter username" value="{username_value}" required>
                </div>
                <div class="form-group">
                    <label for="password">Password:</label>
                    <input type="password" id="password" name="password" placeholder="Enter password" value="{password_value}" required>
                </div>
                <button type="submit" class="btn">Login</button>
            </form>

            <div class="admin-info">
                <h4>🔑 Default Admin Credentials:</h4>
                <p><strong>Username:</strong> admin</p>
                <p><strong>Password:</strong> admin123</p>
                <small>You can change these credentials from the admin panel</small>
            </div>

            <div class="footer">
                <p>Version {SYSTEM_VERSION} | {SYSTEM_NAME}</p>
            </div>
        </div>

        <script>
            function handleLogin(event) {{
                event.preventDefault();
                const username = document.getElementById('username').value;
                const password = document.getElementById('password').value;

                if (username === 'admin' && password === 'admin123') {{
                    localStorage.setItem('user', JSON.stringify({{
                        username: username,
                        role: 'admin',
                        loginTime: new Date().toISOString()
                    }}));
                    window.location.href = '/admin';
                }} else {{
                    alert('❌ Invalid username or password!\\n\\nUse:\\nUsername: admin\\nPassword: admin123');
                }}
            }}
        </script>
    </body>
    </html>
    """
    return html


@app.post("/api/login")
async def api_login(username: str, password: str):
    """API login endpoint"""
    if username == "admin" and password == "admin123":
        return {
            "success": True,
            "message": "Login successful",
            "user": {
                "username": username,
                "role": "admin",
                "loginTime": datetime.now().isoformat()
            },
            "redirect": "/admin"
        }
    else:
        return {
            "success": False,
            "message": "Invalid username or password"
        }


@app.get("/admin")
async def admin_redirect():
    """Redirect to admin panel"""
    return RedirectResponse(url="/admin/", status_code=302)


# Exception handler


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """Global exception handler"""
    logger.error(f"Unhandled exception: {str(exc)}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error"}
    )


# Load modules on startup


@app.on_event("startup")
async def startup_event():
    """Startup events"""
    logger.info(f"Starting {SYSTEM_NAME} version {SYSTEM_VERSION}")

    # Load modules
    if load_modules():
        logger.info("All modules loaded successfully")
    else:
        logger.warning("Some modules failed to load")


if __name__ == "__main__":
    # Run the server
    uvicorn.run(
        "main_fixed:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
