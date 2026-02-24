#!/usr/bin/env python3
"""
verify_context.py - Anti-Hallucination Protocol Enforcer
Status: Verified Feb 2026

This tool forces the AI to verify the existence and content of a file
before acting on it. It prevents "blind edits" and "phantom file" errors.
"""

import argparse
import os
import sys
import re

def verify_file(target, expect_pattern=None):
    """
    Verifies that a file exists and optionally contains a specific pattern.
    """
    if not os.path.exists(target):
        print(f"❌ ERROR: File not found: {target}")
        return False

    if os.path.isdir(target):
        print(f"✅ Directory exists: {target}")
        return True

    if expect_pattern:
        try:
            with open(target, 'r', encoding='utf-8') as f:
                content = f.read()
                if re.search(expect_pattern, content):
                    print(f"✅ Verified: '{target}' contains pattern '{expect_pattern}'")
                    return True
                else:
                    print(f"❌ ERROR: Pattern '{expect_pattern}' NOT found in '{target}'")
                    return False
        except Exception as e:
            print(f"❌ ERROR: Could not read file '{target}': {e}")
            return False

    print(f"✅ File exists: {target}")
    return True

def main():
    parser = argparse.ArgumentParser(description="Anti-Hallucination Context Verifier")
    parser.add_argument("--target", required=True, help="File or directory to verify")
    parser.add_argument("--expect", help="Regex pattern expected in the file content")
    
    args = parser.parse_args()
    
    success = verify_file(args.target, args.expect)
    
    if success:
        sys.exit(0)
    else:
        sys.exit(1)

if __name__ == "__main__":
    main()
