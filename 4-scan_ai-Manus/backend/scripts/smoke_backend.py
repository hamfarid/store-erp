# FILE: backend/scripts/smoke_backend.py | PURPOSE: Minimal backend smoke check (settings + app creation) | OWNER: Maintainers | RELATED: backend/src/core/config.py, backend/src/core/app_factory.py | LAST-AUDITED: 2025-12-13

from __future__ import annotations

import sys
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(PROJECT_ROOT))


def main() -> int:
    from backend.src.core.app_factory import create_app
    from backend.src.core.config import get_settings

    settings = get_settings()
    app = create_app(settings)

    print("OK: settings loaded and app created")
    print(f"ALLOWED_ORIGINS={settings.ALLOWED_ORIGINS}")
    print(f"APP_TYPE={type(app).__name__}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
