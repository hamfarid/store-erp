# Global System Ultimate - Backend Dockerfile
# Verified Feb 2026: Python 3.11-slim + Dynamic Ports

FROM python:3.11-slim

WORKDIR /app

# Install uv for fast package management
RUN pip install uv

COPY requirements.txt .
RUN uv pip install --system -r requirements.txt

COPY . .

# Smart Port Orchestration: Port is injected at runtime via $PORT
CMD ["sh", "-c", "uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8000}"]
