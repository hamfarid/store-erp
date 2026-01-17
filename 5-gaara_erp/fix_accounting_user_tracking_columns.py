"""Utility script to backfill missing created_by_id / updated_by_id columns
for legacy accounting tables that now inherit from BaseModel / BaseModelWithCompany.

This is a temporary manual remediation because generating formal migrations
is currently blocked by system check errors. Once those are resolved, a proper
schema migration should replace this ad-hoc fix.
"""
from __future__ import annotations
import sqlite3
from pathlib import Path

DB_PATH = Path('gaara_erp') / 'db.sqlite3'

TABLES = [
    'accounting_accounttype',
    'accounting_currency',
    'accounting_account',
    'accounting_fiscalyear',
    'accounting_fiscalperiod',
    'accounting_journal',
    'accounting_journalentry',
    'accounting_analyticaccount',
    'accounting_tax',
]


def ensure_columns(conn: sqlite3.Connection, table: str) -> list[str]:
    cur = conn.cursor()
    cur.execute(f'PRAGMA table_info({table})')
    existing = [r[1] for r in cur.fetchall()]
    statements = []

    if 'created_by_id' not in existing:
        try:
            cur.execute(f'ALTER TABLE {table} ADD COLUMN created_by_id bigint')
            statements.append('added created_by_id')
        except Exception as e:  # noqa: BLE001
            statements.append(f'failed created_by_id: {e}')

    if 'updated_by_id' not in existing:
        try:
            cur.execute(f'ALTER TABLE {table} ADD COLUMN updated_by_id bigint')
            statements.append('added updated_by_id')
        except Exception as e:  # noqa: BLE001
            statements.append(f'failed updated_by_id: {e}')

    # Return final columns
    cur.execute(f'PRAGMA table_info({table})')
    final_cols = [r[1] for r in cur.fetchall()]
    return [f"{table}: {', '.join(statements)} -> {final_cols}"]


def main() -> None:
    if not DB_PATH.exists():
        raise SystemExit(f'Database not found at {DB_PATH}')
    conn = sqlite3.connect(DB_PATH)
    try:
        report: list[str] = []
        for table in TABLES:
            report.extend(ensure_columns(conn, table))
        conn.commit()
    finally:
        conn.close()

    print('\n'.join(report))


if __name__ == '__main__':  # pragma: no cover
    main()
