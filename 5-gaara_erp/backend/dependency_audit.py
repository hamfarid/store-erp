#!/usr/bin/env python3
"""Dependency Usage vs Requirements Report Generator.

Scans the backend src directory for imported top-level modules and compares
against the locked requirements list (requirements_final.txt). Produces:
- used_only: modules imported but not in requirements (potential missing pin)
 - declared_only: packages in requirements never imported
     (could be unused, optional, or runtime-only)
- summary counts

Usage:
    python dependency_audit.py [--json] [--limit N]

Assumptions:
- requirements_final.txt is authoritative
- Optional (commented) dependencies are ignored unless uncommented
- Maps simple import names to requirement package names heuristically
"""
from __future__ import annotations
import ast
import pathlib
import re
import json
import argparse
from typing import Set, Dict

ROOT = pathlib.Path(__file__).parent
SRC = ROOT / "src"
REQ_FILE = ROOT / "requirements_final.txt"

PACKAGE_NAME_MAP = {
    "flask_cors": "Flask-CORS",
    "flask_sqlalchemy": "Flask-SQLAlchemy",
    "flask_jwt_extended": "Flask-JWT-Extended",
    "flask_session": "Flask-Session",
    "flask_login": "Flask-Login",
    "flask_wtf": "Flask-WTF",
    "flask_migrate": "Flask-Migrate",
    "flask_mail": "Flask-Mail",
    "flask_limiter": "Flask-Limiter",
    "werkzeug": "Werkzeug",
    "jinja2": "Jinja2",
    "itsdangerous": "itsdangerous",
    "sqlalchemy": "SQLAlchemy",
    "alembic": "alembic",
    "bcrypt": "bcrypt",
    "cryptography": "cryptography",
    "jwt": "PyJWT",  # rare alias
    "pyjwt": "PyJWT",
    "passlib": "passlib",
    "dotenv": "python-dotenv",
    "pandas": "pandas",
    "numpy": "numpy",
    "matplotlib": "matplotlib",
    "seaborn": "seaborn",
    "plotly": "plotly",
    "requests": "requests",
    "httpx": "httpx",
    "psutil": "psutil",
    "schedule": "schedule",
    "apscheduler": "APScheduler",
    "jsonschema": "jsonschema",
    "marshmallow": "marshmallow",
    "cerberus": "cerberus",
    "email_validator": "email-validator",
    "pytest": "pytest",
    "faker": "faker",
    "factory": "factory-boy",
    "reportlab": "reportlab",
    "fpdf": "fpdf2",
    "PIL": "Pillow",
    "openpyxl": "openpyxl",
    "xlsxwriter": "xlsxwriter",
    "python_barcode": "python-barcode",
    "qrcode": "qrcode",
    "celery": "celery",
    "redis": "redis",
    "loguru": "loguru",
    "colorama": "colorama",
    "arabic_reshaper": "arabic-reshaper",
    "bidi": "python-bidi",
}

REQ_LINE_RE = re.compile(r"^([A-Za-z0-9_.\-]+)==")


def parse_requirements() -> Set[str]:
    pkgs: Set[str] = set()
    for line in REQ_FILE.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        m = REQ_LINE_RE.match(line)
        if m:
            pkgs.add(m.group(1))
    return pkgs


def collect_imports() -> Set[str]:
    """Parse all Python files and collect top-level import roots.

    Reduced branching to lower cognitive complexity.
    """
    found: Set[str] = set()
    for py_file in SRC.rglob("*.py"):
        try:
            source = py_file.read_text(encoding="utf-8")
            tree = ast.parse(source)
        except Exception:  # noqa: BLE001
            continue
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    found.add(alias.name.split(".")[0])
            elif isinstance(node, ast.ImportFrom) and node.module:
                found.add(node.module.split(".")[0])
    return found


def map_import_to_requirement(name: str) -> str | None:
    lowered = name.lower()
    return PACKAGE_NAME_MAP.get(lowered)


def build_report() -> Dict[str, object]:
    declared = parse_requirements()
    imported_raw = collect_imports()

    imported_mapped: Set[str] = set()
    for imp in imported_raw:
        mapped = map_import_to_requirement(imp)
        if mapped:
            imported_mapped.add(mapped)

    used_only = sorted(pkg for pkg in imported_mapped if pkg not in declared)
    declared_only = sorted(pkg for pkg in declared if pkg not in imported_mapped)

    return {
        "summary": {
            "declared_total": len(declared),
            "imported_total": len(imported_mapped),
            "declared_only": len(declared_only),
            "used_only": len(used_only),
        },
        "used_only": used_only,
        "declared_only": declared_only,
        "imported_modules_raw": sorted(imported_raw),
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--json", action="store_true", help="Output JSON")
    args = parser.parse_args()
    report = build_report()
    if args.json:
        print(json.dumps(report, indent=2, ensure_ascii=False))
    else:
        print("Dependency Usage Report")
        print("=======================")
        print(json.dumps(report["summary"], indent=2, ensure_ascii=False))
        used_only_list = list(report["used_only"])  # type: ignore[index]
        if used_only_list:
            print("\nPackages imported but NOT declared:")
            for p in used_only_list:
                print(f"  - {p}")
        declared_only_list = list(report["declared_only"])  # type: ignore[index]
        if declared_only_list:
            print("\nPackages declared but not imported:")
            for p in declared_only_list:
                print(f"  - {p}")
        print("\nDone.")


if __name__ == "__main__":
    main()
