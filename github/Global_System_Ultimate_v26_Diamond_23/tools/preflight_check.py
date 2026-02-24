#!/usr/bin/env python3
"""
Pre-flight Check (Global System Ultimate)
Ensures system integrity, security, memory bank readiness, and port availability.
"""

import asyncio
import os
import re
import sys
import socket
from pathlib import Path
from typing import List, Dict

# Load Version
try:
    with open(os.path.join(os.path.dirname(__file__), "../VERSION"), "r") as f:
        VERSION = f.read().strip()
except FileNotFoundError:
    VERSION = "UNKNOWN"

# --- Configuration ---
TOOLS_DIR = Path(__file__).parent.absolute()
GLOBAL_DIR = TOOLS_DIR.parent
GITHUB_DIR = GLOBAL_DIR.parent
PROJECT_ROOT = GITHUB_DIR.parent

# Unified Memory Bank (Global System Ultimate)
MEMORY_DIR = PROJECT_ROOT / "memory-bank"

CRITICAL_MEMORY_FILES = [
    "activeContext.md",
    "systemContext.md",
    "projectBrief.md",
    "decisionLog.md"
]

SENSITIVE_PATTERNS = [
    r"sk-[a-zA-Z0-9]{48}",  # OpenAI Key
    r"xox[baprs]-([0-9a-zA-Z]{10,48})",  # Slack Token
    r"gh[pousr]_[a-zA-Z0-9]{36}",  # GitHub Token
]

INJECTION_PATTERNS = [
    r"ignore previous instructions",
    r"system override",
    r"delete all files"
]

def load_env_ports() -> Dict[str, int]:
    """Loads ports from .env file."""
    ports = {}
    env_path = PROJECT_ROOT / ".env"
    if env_path.exists():
        with open(env_path, "r") as f:
            for line in f:
                if "=" in line and not line.startswith("#"):
                    key, value = line.strip().split("=", 1)
                    if "_PORT" in key:
                        try:
                            ports[key] = int(value)
                        except ValueError:
                            pass
    return ports

async def check_ports() -> bool:
    """Verifies that configured ports are available."""
    print("🔌 Checking Port Availability...")
    ports = load_env_ports()
    
    if not ports:
        print("⚠️  No ports found in .env (or .env missing). Skipping port check.")
        return True

    conflict = False
    for name, port in ports.items():
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        result = sock.connect_ex(('127.0.0.1', port))
        if result == 0:
            print(f"❌ Port Conflict: {name} ({port}) is already in use.")
            conflict = True
        sock.close()
    
    if conflict:
        return False
        
    print(f"✅ All {len(ports)} ports are available.")
    return True

async def check_security() -> bool:
    """Scans for prompt injection attempts in recent context."""
    print("🛡️  Running Security Scan...")
    if MEMORY_DIR.exists():
        for path in MEMORY_DIR.rglob("*.md"):
            try:
                content = path.read_text(encoding="utf-8")
                for pattern in INJECTION_PATTERNS:
                    if re.search(pattern, content, re.IGNORECASE):
                        print(f"❌ Security Alert: Potential prompt injection in {path}")
                        return False
            except Exception as e:
                print(f"⚠️  Could not read {path}: {e}")
    print("✅ Security Scan Passed")
    return True

async def check_environment() -> bool:
    """Verifies runtime environment and lockfiles."""
    print("🌍 Checking Environment...")
    # Check for lockfiles if package.json exists
    if (PROJECT_ROOT / "package.json").exists() and not any([
        (PROJECT_ROOT / "package-lock.json").exists(),
        (PROJECT_ROOT / "pnpm-lock.yaml").exists(),
        (PROJECT_ROOT / "yarn.lock").exists(),
        (PROJECT_ROOT / "bun.lockb").exists()
    ]):
        print("⚠️  Warning: Missing lockfile for Node project")
    
    print("✅ Environment Check Passed")
    return True

async def check_secrets() -> bool:
    """Scans for hardcoded secrets."""
    print("🔑 Scanning for Secrets...")
    
    # Define ignore directories
    ignore_dirs = {".git", "node_modules", "__pycache__", "venv", ".venv"}
    
    for path in PROJECT_ROOT.rglob("*"):
        if any(part in ignore_dirs for part in path.parts):
            continue
            
        if path.is_file() and path.suffix in {".py", ".js", ".ts", ".md", ".json"}:
            try:
                content = path.read_text(encoding="utf-8")
                for pattern in SENSITIVE_PATTERNS:
                    if re.search(pattern, content):
                        print(f"❌ Secret detected in {path}")
                        return False
            except:
                pass
                
    print("✅ Secret Scan Passed")
    return True

async def check_memory() -> bool:
    """Verifies memory bank integrity."""
    print("🧠 Verifying Memory Bank...")
    
    if not MEMORY_DIR.exists():
        print(f"❌ Memory Bank not found at {MEMORY_DIR}")
        print("🔧 Attempting self-healing (Genesis)...")
        genesis_script = GLOBAL_DIR / "genesis.py"
        
        if genesis_script.exists():
            proc = await asyncio.create_subprocess_exec(
                sys.executable, str(genesis_script),
                cwd=str(PROJECT_ROOT),
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            await proc.communicate()
            return True
        else:
            print(f"❌ Genesis script missing at {genesis_script}. Cannot heal.")
            return False
    
    missing = [f for f in CRITICAL_MEMORY_FILES if not (MEMORY_DIR / f).exists()]
    
    if missing:
        print(f"❌ Missing critical memory files: {missing}")
        print("🔧 Attempting self-healing...")
        try:
            for filename in missing:
                file_path = MEMORY_DIR / filename
                file_path.write_text(f"# {filename}\n\nInitialized by Pre-flight Check (Global System Ultimate {VERSION})\n", encoding="utf-8")
            print("✅ Self-healing successful.")
            return True
        except Exception as e:
            print(f"❌ Self-healing failed: {e}")
            return False
    
    print("✅ Memory Bank Integrity Verified")
    return True

async def main() -> None:
    """Main execution flow."""
    print(f"🚀 Starting Pre-Flight Checks (Global System Ultimate {VERSION})...")
    print(f"📍 Project Root: {PROJECT_ROOT}")
    
    checks = [check_ports, check_security, check_environment, check_secrets, check_memory]
    
    for check in checks:
        if not await check():
            print("🚨 Pre-flight Check FAILED")
            sys.exit(1)
    
    print("✈️  Pre-flight Check PASSED. Ready for takeoff.")
    sys.exit(0)

if __name__ == "__main__":
    asyncio.run(main())
