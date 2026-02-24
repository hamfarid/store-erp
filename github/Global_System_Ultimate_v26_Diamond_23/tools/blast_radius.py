#!/usr/bin/env python3
import os
import sys
import re

# Load Version
try:
    with open(os.path.join(os.path.dirname(__file__), "../VERSION"), "r") as f:
        VERSION = f.read().strip()
except FileNotFoundError:
    VERSION = "UNKNOWN"

# Global System Ultimate - Blast Radius Tool
# Verified Feb 2026: ByteBell Simulation (Graph + Vector)

def analyze_impact(target_file):
    """
    Simulates ByteBell-style impact analysis.
    Finds files that import or reference the target file.
    """
    print(f"🔍 Analyzing Blast Radius ({VERSION}) for: {target_file}")
    
    impacted_files = []
    target_name = os.path.splitext(os.path.basename(target_file))[0]
    
    # Simple grep-based dependency check (Simulation of Graph Traversal)
    for root, _, files in os.walk("."):
        for file in files:
            if file.endswith((".py", ".ts", ".tsx", ".js")):
                path = os.path.join(root, file)
                try:
                    with open(path, 'r') as f:
                        content = f.read()
                        if target_name in content:
                            impacted_files.append(path)
                except:
                    pass
                    
    print(f"💥 Potential Impact: {len(impacted_files)} files")
    for f in impacted_files:
        print(f"  - {f}")
        
    return impacted_files

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(f"Usage: python3 blast_radius.py <file_path> (v{VERSION})")
        sys.exit(1)
        
    analyze_impact(sys.argv[1])
