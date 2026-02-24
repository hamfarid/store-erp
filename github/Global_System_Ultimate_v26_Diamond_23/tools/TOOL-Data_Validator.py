#!/usr/bin/env python3
import json
import sys

def validate_json(file_path):
    try:
        with open(file_path, 'r') as f:
            json.load(f)
        print(f"✅ Valid JSON: {file_path}")
        return True
    except json.JSONDecodeError as e:
        print(f"❌ Invalid JSON: {file_path} - {e}")
        return False
    except FileNotFoundError:
        print(f"❌ File not found: {file_path}")
        return False

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 TOOL-Data_Validator.py <file_path>")
        sys.exit(1)
    validate_json(sys.argv[1])
