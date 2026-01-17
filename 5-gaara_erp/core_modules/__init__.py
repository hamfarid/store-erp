# FILE: core_modules/__init__.py | PURPOSE: Import shim for core_modules namespace | OWNER: Platform Team | RELATED: gaara_erp/core_modules | LAST-AUDITED: 2025-12-13
"""Compatibility shim for imports like `core_modules.*`.

This repository contains Django apps under `gaara_erp/core_modules`, but many modules
import them as a top-level package (e.g., `core_modules.rag`).

When running from the repo root (common for pytest), `gaara_erp/` is not on
`sys.path`, so `import core_modules` fails. This shim makes `core_modules.*`
resolvable without requiring callers to set PYTHONPATH.

It is intentionally lightweight and has no runtime dependency on Django.
"""

from __future__ import annotations

import pkgutil
import sys
from pathlib import Path

__path__ = pkgutil.extend_path(__path__, __name__)  # type: ignore[name-defined]

# Ensure `gaara_erp/` is on sys.path so `gaara_erp/core_modules/*` can be imported as `core_modules.*`.
_REPO_ROOT = Path(__file__).resolve().parent.parent
_GAARA_ERP_DIR = _REPO_ROOT / "gaara_erp"

if _GAARA_ERP_DIR.is_dir():
    p = str(_GAARA_ERP_DIR)
    if p not in sys.path:
        sys.path.insert(0, p)

    # Also include the actual apps directory as part of this package's search path.
    _CORE_MODULES_DIR = _GAARA_ERP_DIR / "core_modules"
    if _CORE_MODULES_DIR.is_dir():
        core_path = str(_CORE_MODULES_DIR)
        if core_path not in __path__:
            __path__.append(core_path)
