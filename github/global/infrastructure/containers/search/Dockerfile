# Search Container - v2026.2 (Updated Feb 2026)
# PRIMARY: Crawl4AI (VLM Zero-Shot, free, local)
# SECONDARY: Firecrawl (99% success, anti-bot)
# FALLBACK: Playwright (full browser)
# SMART: ScrapeGraphAI (natural language extraction)

FROM python:3.12-slim-bookworm

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# System dependencies (Playwright browsers + build tools)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libssl-dev \
    libffi-dev \
    libxml2-dev \
    libxslt1-dev \
    zlib1g-dev \
    git \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Install Playwright browsers (for fallback engine)
RUN playwright install chromium --with-deps

# Crawl4AI setup (downloads VLM model on first run)
RUN crawl4ai-setup || true

# Non-root user
RUN useradd -m search_agent
USER search_agent
WORKDIR /home/search_agent

COPY . .

# FastAPI service
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8002"]
EXPOSE 8002
