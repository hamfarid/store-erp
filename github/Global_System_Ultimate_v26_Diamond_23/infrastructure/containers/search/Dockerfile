# Search Container - v2026.2
# Purpose: Automated, compliant web scraping and information retrieval.
# Compliance: GDPR, Robots.txt, Rate Limiting.

FROM python:3.11-slim-bookworm

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    SCRAPY_SETTINGS_MODULE=search_agent.settings

# Install system dependencies (including Playwright browsers)
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

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Install Playwright browsers
RUN playwright install chromium --with-deps

# Create non-root user
RUN useradd -m search_agent
USER search_agent
WORKDIR /home/search_agent

# Copy application code
COPY . .

# Entrypoint
ENTRYPOINT ["python", "main.py"]
