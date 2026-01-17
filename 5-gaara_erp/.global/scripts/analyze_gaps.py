#!/usr/bin/env python3
"""
Analyze gaps between design and implementation.

File: scripts/analyze_gaps.py
Module: scripts.analyze_gaps
Created: 2025-01-15
Author: Team
Description: Compare design specs with actual implementation

Dependencies:
- pathlib
- json
- ast
"""

import ast
import json
from pathlib import Path
from typing import Dict, List, Set


def find_api_endpoints() -> Set[str]:
    """Find all defined API endpoints."""
    endpoints = set()

    for py_file in Path('.').rglob('*views.py'):
        try:
            with open(py_file) as f:
                content = f.read()
        except BaseException:
            continue

        # Find @api_view decorators
        import re
        # Find route definitions
        routes = re.findall(r'path\([\'"]([^\'\"]+)[\'"]', content)

        endpoints.update(routes)

    return endpoints


def find_frontend_routes() -> Set[str]:
    """Find all frontend routes."""
    routes = set()

    # Check React Router
    for tsx_file in Path('.').rglob('*.tsx'):
        try:
            with open(tsx_file) as f:
                content = f.read()
        except BaseException:
            continue

        import re
        patterns = re.findall(r'<Route\s+path=[\'"]([^\'\"]+)[\'"]', content)
        routes.update(patterns)

    return routes


def find_database_models() -> Set[str]:
    """Find all database models."""
    models = set()

    for py_file in Path('.').rglob('models.py'):
        try:
            with open(py_file) as f:
                tree = ast.parse(f.read())
        except BaseException:
            continue

        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef):
                # Check if it's a Django model
                for base in node.bases:
                    if isinstance(base, ast.Attribute):
                        if base.attr == 'Model':
                            models.add(node.name)

    return models


def load_design_spec(spec_file: str) -> Dict:
    """Load design specification."""
    with open(spec_file) as f:
        return json.load(f)


def analyze_gaps(spec_file: str = 'docs/design_spec.json'):
    """Analyze gaps between design and implementation."""
    print("🔍 Analyzing Design vs Implementation Gaps\n")

    # Load design spec
    try:
        spec = load_design_spec(spec_file)
    except FileNotFoundError:
        print(f"⚠️  Design spec not found: {spec_file}")
        print("   Create docs/design_spec.json with your design")
        return

    # Find implementation
    api_endpoints = find_api_endpoints()
    frontend_routes = find_frontend_routes()
    db_models = find_database_models()

    # Compare
    gaps = []

    # Check API endpoints
    if 'api_endpoints' in spec:
        for endpoint in spec['api_endpoints']:
            if endpoint not in api_endpoints:
                gaps.append(f"Missing API endpoint: {endpoint}")

    # Check frontend routes
    if 'frontend_routes' in spec:
        for route in spec['frontend_routes']:
            if route not in frontend_routes:
                gaps.append(f"Missing frontend route: {route}")

    # Check database models
    if 'models' in spec:
        for model in spec['models']:
            if model not in db_models:
                gaps.append(f"Missing database model: {model}")

    # Report
    if gaps:
        print("❌ Gaps Found:\n")
        for gap in gaps:
            print(f"  • {gap}")
        print(f"\nTotal gaps: {len(gaps)}")
    else:
        print("✅ No gaps found! Design matches implementation.")

    # Summary
    print("\n📊 Summary:")
    print(f"  API Endpoints: {len(api_endpoints)} implemented")
    print(f"  Frontend Routes: {len(frontend_routes)} implemented")
    print(f"  Database Models: {len(db_models)} implemented")


if __name__ == '__main__':
    analyze_gaps()
