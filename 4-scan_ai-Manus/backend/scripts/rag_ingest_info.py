# FILE: backend/scripts/rag_ingest_info.py | PURPOSE: RAG ingest task placeholder/info until ingest script exists | OWNER: Maintainers | RELATED: backend/src/core/config.py | LAST-AUDITED: 2025-12-13

from __future__ import annotations

import sys
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(PROJECT_ROOT))


def main() -> int:
    from backend.src.core.config import get_settings

    settings = get_settings()
    print(
        "RAG ingest script is not present in backend/src. "
        "This task currently only reports configuration."
    )
    print(f"FEATURE_RAG_ENABLED={getattr(settings, 'FEATURE_RAG_ENABLED', None)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
