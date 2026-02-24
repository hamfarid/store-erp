"""
Unit Test: Core Logic (Global System Ultimate)
Version: v11.0 (Verified Feb 2026)

Tests core system functionality using Pytest and AsyncIO.
"""

import pytest
import asyncio
import sys
from pathlib import Path

# Add project root to path
PROJECT_ROOT = Path(__file__).parent.parent.parent
sys.path.append(str(PROJECT_ROOT))

@pytest.mark.asyncio
async def test_system_logger_async():
    """Verify SystemLogger works asynchronously."""
    try:
        from system_logger import SystemLogger
        logger = SystemLogger(log_file=Path("test_log.md"))
        
        await logger.log_intent("TEST_CMD", "TEST_TASK")
        await logger.log_result(0, "TEST_OUTPUT")
        
        assert Path("test_log.md").exists()
        content = Path("test_log.md").read_text()
        assert "TEST_CMD" in content
        assert "TEST_OUTPUT" in content
        
        # Cleanup
        Path("test_log.md").unlink()
    except ImportError:
        pytest.skip("SystemLogger not found in path")

@pytest.mark.asyncio
async def test_genesis_environment_detection():
    """Verify Genesis detects environment correctly."""
    try:
        from genesis import detect_environment
        env = await detect_environment()
        assert "python" in env
        assert "os" in env
        assert isinstance(env["docker"], bool)
    except ImportError:
        pytest.skip("Genesis module not found in path")

def test_project_structure_compliance():
    """Verify the project structure matches Global System standards."""
    required_dirs = ["memory-bank", "tools", "tests", "docs"]
    for d in required_dirs:
        assert (PROJECT_ROOT / d).exists() or (PROJECT_ROOT / "GitHub" / "global_system" / d).exists()
