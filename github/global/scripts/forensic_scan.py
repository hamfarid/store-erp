"""
Module: forensic_scan.py
Forensic Scan — part of Global System v26.0.2 Diamond 32.
"""
import os
import re

# Define the hallucinations to hunt down
HALLUCINATIONS = {
    "FastAPI 2.0": r"FastAPI\s*2\.0",
    "Chain-of-Vibes": r"Chain-of-Vibes",
    "Agentic Workflows v2": r"Agentic\s*Workflows\s*v2",
    "PostgreSQL 17": r"PostgreSQL\s*17",
    "React 19 (Unverified)": r"React\s*19(?!\.2\.4)",  # Catch generic React 19 references
}

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

def scan_files():
    """
    Scan files implementation.
    """
    print(f"🔍 Starting Forensic Deep Scan in: {ROOT_DIR}")
    print("=" * 60)
    
    found_count = 0
    
    for root, dirs, files in os.walk(ROOT_DIR):
        # Skip hidden folders and pycache
        dirs[:] = [d for d in dirs if not d.startswith('.') and d != '__pycache__']
        
        for file in files:
            if file.endswith(('.md', '.txt', '.py', '.json', '.yaml', '.sh')):
                file_path = os.path.join(root, file)
                try:
                    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                        content = f.read()
                        
                    for name, pattern in HALLUCINATIONS.items():
                        matches = list(re.finditer(pattern, content, re.IGNORECASE))
                        if matches:
                            print(f"🚨 FOUND {name} in: {file_path}")
                            for match in matches:
                                line_num = content[:match.start()].count('\n') + 1
                                print(f"   Line {line_num}: ...{content[match.start()-20:match.end()+20].replace(chr(10), ' ')}...")
                            found_count += 1
                            
                except Exception as e:
                    print(f"⚠️ Error reading {file_path}: {e}")

    print("=" * 60)
    if found_count == 0:
        print("✅ SYSTEM CLEAN: No hallucinations found.")
    else:
        print(f"❌ SYSTEM COMPROMISED: Found {found_count} instances of hallucinations.")

if __name__ == "__main__":
    scan_files()
