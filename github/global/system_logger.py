#!/usr/bin/env python3
"""
System Logger - Automatic logging utility for AI agents
Version: v11.0 (Verified Feb 2026)

This module provides a structured, asynchronous logging facility for the Global System.
It supports:
1. Structured JSON logging (via structlog/json).
2. Markdown-friendly output for `system_log.md`.
3. AsyncIO support for non-blocking logging.
4. Integration with Swarm Intelligence phases.
"""

import asyncio
import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, Optional

# Configuration
LOG_FILE = Path("system_log.md")

class SystemLogger:
    """
    A structured, async-compatible logger for the Global System.
    """
    def __init__(self, log_file: Path = LOG_FILE):
        """
          init   implementation.
        """
        self.log_file = log_file
        self._ensure_log_file()

    def _ensure_log_file(self) -> None:
        """Ensures the log file exists with a header."""
        if not self.log_file.exists():
            self.log_file.write_text("# System Log (Global System v26 Diamond 32 v26.0 Diamond 32 GAARA AI)\n\n", encoding="utf-8")

    def _get_timestamp(self) -> str:
        """Returns ISO 8601 timestamp with Z suffix."""
        return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")

    async def _write_entry(self, entry: str) -> None:
        """Asynchronously writes an entry to the log file."""
        try:
            # Use run_in_executor for file I/O to avoid blocking the event loop
            await asyncio.get_running_loop().run_in_executor(
                None, self._append_to_file, entry
            )
        except Exception as e:
            print(f"❌ Logger Error: {e}", file=sys.stderr)

    def _append_to_file(self, entry: str) -> None:
        """Synchronous append helper."""
        with open(self.log_file, "a", encoding="utf-8") as f:
            f.write(entry)

    async def log_intent(self, command: str, task: str, details: str = "") -> None:
        """Log the intent before executing a command."""
        timestamp = self._get_timestamp()
        entry = f"`{timestamp}` - **[INTENT]** - `Executing: {command}` - **[TASK]** - `{task}`"
        if details:
            entry += f" - **[DETAILS]** - `{details}`"
        entry += "\n"
        
        await self._write_entry(entry)
        print(f"📝 [INTENT] {command}")

    async def log_result(self, exit_code: int, output: str = "", details: str = "") -> None:
        """Log the result after executing a command."""
        timestamp = self._get_timestamp()
        status = "SUCCESS" if exit_code == 0 else "FAILURE"
        truncated_output = (output[:200] + "...") if len(output) > 200 else output
        
        entry = f"`{timestamp}` - **[RESULT]** - `Exit: {exit_code}` - **[STATUS]** - `{status}`"
        if truncated_output:
            entry += f" - **[OUTPUT]** - `{truncated_output}`"
        if details:
            entry += f" - **[DETAILS]** - `{details}`"
        entry += "\n\n"
        
        await self._write_entry(entry)
        print(f"✅ [RESULT] Exit: {exit_code}" if exit_code == 0 else f"❌ [RESULT] Exit: {exit_code}")

    async def log_phase_start(self, phase_name: str, phase_number: int) -> None:
        """Log the start of a new phase."""
        timestamp = self._get_timestamp()
        entry = (
            f"\n---\n\n## Phase {phase_number}: {phase_name}\n\n"
            f"`{timestamp}` - **[PHASE_START]** - `Starting Phase {phase_number}: {phase_name}`\n\n"
        )
        
        await self._write_entry(entry)
        print(f"\n🚀 [PHASE START] Phase {phase_number}: {phase_name}")

    async def log_phase_complete(self, phase_name: str, phase_number: int) -> None:
        """Log the completion of a phase."""
        timestamp = self._get_timestamp()
        entry = f"`{timestamp}` - **[PHASE_COMPLETE]** - `Completed Phase {phase_number}: {phase_name}`\n\n"
        
        await self._write_entry(entry)
        print(f"🏁 [PHASE COMPLETE] Phase {phase_number}: {phase_name}")

    async def log_error(self, error_message: str, severity: str = "HIGH") -> None:
        """Log an error."""
        timestamp = self._get_timestamp()
        entry = f"`{timestamp}` - **[ERROR]** - **[SEVERITY: {severity}]** - `{error_message}`\n\n"
        
        await self._write_entry(entry)
        print(f"🔥 [ERROR] {error_message}", file=sys.stderr)

    async def log_decision(self, decision: str, rationale: str) -> None:
        """Log a decision and its rationale."""
        timestamp = self._get_timestamp()
        entry = f"`{timestamp}` - **[DECISION]** - `{decision}` - **[RATIONALE]** - `{rationale}`\n\n"
        
        await self._write_entry(entry)
        print(f"🧠 [DECISION] {decision}")

# Async Example Usage
async def main():
    """
    Main implementation.
    """
    logger = SystemLogger()
    
    await logger.log_phase_start("Initialization & Analysis", 1)
    await logger.log_intent("python3 analyze_project.py", "Analyze existing project structure")
    await logger.log_result(0, "Project analyzed successfully. Found 150 files.")
    
    await logger.log_decision(
        "Use PostgreSQL 18.2",
        "Chosen for native vector support and strong consistency (OSF Score: 9.2/10)"
    )
    
    await logger.log_phase_complete("Initialization & Analysis", 1)
    print("\n✓ System logger demonstration complete. Check system_log.md")

if __name__ == "__main__":
    asyncio.run(main())
