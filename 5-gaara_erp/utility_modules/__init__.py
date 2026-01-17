# FILE: utility_modules/__init__.py | PURPOSE: Import shim for utility_modules namespace | OWNER: Platform Team | RELATED: gaara_erp/utility_modules | LAST-AUDITED: 2025-12-13
"""Compatibility shim for imports like `utility_modules.*`.

The Django project stores these apps under `gaara_erp/utility_modules`, but many
modules import them as a top-level package. Running from the repo root (e.g. pytest)
won't have `gaara_erp/` on `sys.path`, so `utility_modules.*` fails.

This shim makes those imports work without requiring PYTHONPATH.
"""

from __future__ import annotations

import pkgutil
import sys
from pathlib import Path

__path__ = pkgutil.extend_path(__path__, __name__)  # type: ignore[name-defined]

_REPO_ROOT = Path(__file__).resolve().parent.parent
_GAARA_ERP_DIR = _REPO_ROOT / "gaara_erp"

# Make sure `gaara_erp/` itself is importable.
if _GAARA_ERP_DIR.is_dir():
    gaara_path = str(_GAARA_ERP_DIR)
    if gaara_path not in sys.path:
        sys.path.insert(0, gaara_path)

    _UTILITY_DIR = _GAARA_ERP_DIR / "utility_modules"
    if _UTILITY_DIR.is_dir():
        util_path = str(_UTILITY_DIR)
        if util_path not in __path__:
            __path__.append(util_path)
