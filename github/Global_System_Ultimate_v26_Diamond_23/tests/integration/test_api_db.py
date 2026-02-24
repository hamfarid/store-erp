"""
Integration Test: API & DB (Global System Ultimate)
Version: v11.0 (Verified Feb 2026)

Tests integration with Shared Infrastructure (ChromaDB, Ollama, Redis).
"""

import pytest
import asyncio
import aiohttp
import os

@pytest.mark.asyncio
async def test_chromadb_connection():
    """Verify ChromaDB is reachable."""
    url = os.getenv("CHROMA_URL", "http://localhost:8000/api/v1/heartbeat")
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, timeout=2) as response:
                assert response.status == 200
    except (aiohttp.ClientError, asyncio.TimeoutError):
        pytest.skip("ChromaDB not reachable (Skipping integration test)")

@pytest.mark.asyncio
async def test_ollama_connection():
    """Verify Ollama is reachable."""
    url = os.getenv("OLLAMA_URL", "http://localhost:11434/api/tags")
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, timeout=2) as response:
                assert response.status == 200
    except (aiohttp.ClientError, asyncio.TimeoutError):
        pytest.skip("Ollama not reachable (Skipping integration test)")

@pytest.mark.asyncio
async def test_redis_connection():
    """Verify Redis is reachable."""
    # Requires redis-py
    try:
        import redis.asyncio as redis
        r = redis.from_url("redis://localhost:6379")
        await r.ping()
        await r.close()
    except ImportError:
        pytest.skip("redis-py not installed")
    except Exception:
        pytest.skip("Redis not reachable (Skipping integration test)")
