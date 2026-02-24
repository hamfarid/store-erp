from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os
import structlog

# Global System Ultimate - Backend Template
# Verified Feb 2026: FastAPI 0.129+

logger = structlog.get_logger()

# Load Version
try:
    with open(os.path.join(os.path.dirname(__file__), "../../VERSION"), "r") as f:
        VERSION = f.read().strip()
except FileNotFoundError:
    VERSION = "UNKNOWN"

app = FastAPI(
    title="Global System Ultimate API",
    version=VERSION,
    description="Universal AI Backend with Smart Port Orchestration"
)

# CORS Configuration (Dynamic)
origins = [
    "http://localhost:3000",
    "http://localhost:5173",
    os.getenv("FRONTEND_URL", "*")
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    logger.info("root_endpoint_accessed")
    return {
        "system": "Global System Ultimate",
        "version": VERSION,
        "status": "operational",
        "mode": os.getenv("DEPLOYMENT_MODE", "unknown")
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy"}
