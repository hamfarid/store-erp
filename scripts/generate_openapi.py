#!/usr/bin/env python3
# FILE: scripts/generate_openapi.py | PURPOSE: Generate OpenAPI JSON from running Flask app | OWNER: Backend Team | RELATED: backend/app.py | LAST-AUDITED: 2025-10-23

import json
import os
import sys

# Ensure project root is on sys.path
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

from backend.app import app, generate_openapi_spec  # type: ignore


def main():
    spec = generate_openapi_spec(app)
    os.makedirs('contracts', exist_ok=True)
    out_path = os.path.join('contracts', 'openapi.json')
    with open(out_path, 'w', encoding='utf-8') as f:
        json.dump(spec, f, ensure_ascii=False, indent=2)
    print(f"Wrote OpenAPI: {out_path}")


if __name__ == '__main__':
    main()

