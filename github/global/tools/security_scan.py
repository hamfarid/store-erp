"""
Module: security_scan.py
Security Scan — part of Global System v26.0.2 Diamond 32.
"""
#!/usr/bin/env python3
import re
import os
import sys

# Load Version
try:
    with open(os.path.join(os.path.dirname(__file__), "../VERSION"), "r") as f:
        VERSION = f.read().strip()
except FileNotFoundError:
    VERSION = "UNKNOWN"

# Simple Regex-based Security Scanner
PATTERNS = {
    "API Key Leak": r"(?i)(api_key|secret|token)\s*=\s*['\"][a-zA-Z0-9_\-]{20,}['\"]",
    "Hardcoded Password": r"(?i)(password|passwd|pwd)\s*=\s*['\"][^'\"]{3,}['\"]",
    "Insecure Eval": r"eval\(",
    "Insecure Exec": r"exec\(",
    "SQL Injection": r"execute\(['\"]SELECT.*\%s",
}

def scan_file(filepath):
    """
    Scan file implementation.
    """
    issues = []
    try:
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
            for name, pattern in PATTERNS.items():
                if re.search(pattern, content):
                    issues.append(name)
    except Exception as e:
        print(f"⚠️ Error reading {filepath}: {e}")
    return issues

def main():
    """
    Main implementation.
    """
    print(f"🛡️ Starting Security Scan ({VERSION})...")
    found_issues = False
    for root, _, files in os.walk("."):
        if "node_modules" in root or ".git" in root or ".venv" in root:
            continue
        for file in files:
            if file.endswith(('.py', '.js', '.ts', '.env')):
                path = os.path.join(root, file)
                issues = scan_file(path)
                if issues:
                    print(f"❌ {path}: {', '.join(issues)}")
                    found_issues = True
    
    if not found_issues:
        print("✅ No obvious security issues found.")
        sys.exit(0)
    else:
        sys.exit(1)

if __name__ == "__main__":
    main()
