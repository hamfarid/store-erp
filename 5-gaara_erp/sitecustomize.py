"""
Ensure the inner Django project package (gaara_erp/gaara_erp/...) is importable
before pytest-django initializes. Python automatically imports `sitecustomize`
if it is present on sys.path during interpreter startup.
"""
from __future__ import annotations
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
PROJECT_DIR = ROOT / "gaara_erp"
if PROJECT_DIR.is_dir():
    # Prepend to guarantee import resolution for `import gaara_erp`
    p = str(PROJECT_DIR)
    if p not in sys.path:
        sys.path.insert(0, p)

# Ensure Django settings are discoverable very early for pytest-django
os.environ.setdefault("APP_MODE", "test")
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "gaara_erp.settings.test")
