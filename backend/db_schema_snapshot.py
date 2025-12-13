#!/usr/bin/env python3
"""Generate a JSON snapshot of the database schema for RORLOC tests.

This script is read-only and safe to run from CI or locally.
"""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

from sqlalchemy import inspect

from app import create_app  # type: ignore
from src.database import db  # type: ignore


def build_schema() -> dict:
    """Introspect the current database and build a simple schema description."""
    app = create_app()
    with app.app_context():
        inspector = inspect(db.engine)
        tables = []
        for table_name in sorted(inspector.get_table_names()):
            columns = []
            for col in inspector.get_columns(table_name):
                columns.append(
                    {
                        "name": col.get("name"),
                        "type": str(col.get("type")),
                        "nullable": col.get("nullable"),
                        "default": (
                            str(col.get("default"))
                            if col.get("default") is not None
                            else None
                        ),
                    }
                )
            pk = inspector.get_pk_constraint(table_name) or {}
            fks = inspector.get_foreign_keys(table_name) or []
            tables.append(
                {
                    "name": table_name,
                    "primary_key": pk.get("constrained_columns", []),
                    "columns": columns,
                    "foreign_keys": [
                        {
                            "constrained_columns": fk.get("constrained_columns", []),
                            "referred_table": fk.get("referred_table"),
                            "referred_columns": fk.get("referred_columns", []),
                        }
                        for fk in fks
                    ],
                }
            )
        return {"tables": tables}


def main() -> None:
    root = Path(__file__).resolve().parent.parent
    artifacts_dir = root / "artifacts"
    artifacts_dir.mkdir(parents=True, exist_ok=True)
    target = artifacts_dir / "db-schema.json"

    payload = {
        "generatedAt": datetime.utcnow().isoformat() + "Z",
        "schema": build_schema(),
    }
    target.write_text(
        json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8"
    )


if __name__ == "__main__":
    try:
        main()
        print("✅ Database schema snapshot generated at artifacts/db-schema.json")
    except Exception as exc:  # noqa: BLE001
        print(f"⚠️ Failed to generate DB schema snapshot: {exc}")
