#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
P2.65: Backup and Restore Service

Provides database backup and restore functionality.
"""

import os
import json
import gzip
import shutil
import logging
import subprocess
from datetime import datetime
from typing import List, Optional, Dict, Any
from dataclasses import dataclass
from pathlib import Path

logger = logging.getLogger(__name__)


# =============================================================================
# Configuration
# =============================================================================

BACKUP_DIR = os.environ.get("BACKUP_DIR", "backups")
MAX_BACKUPS = int(os.environ.get("MAX_BACKUPS", 10))
DATABASE_URL = os.environ.get("DATABASE_URL", "")


@dataclass
class BackupInfo:
    """Information about a backup file."""

    filename: str
    filepath: str
    size: int
    created_at: datetime
    backup_type: str  # 'full', 'incremental', 'schema'
    database: str
    compressed: bool

    def to_dict(self) -> Dict[str, Any]:
        return {
            "filename": self.filename,
            "size": self.size,
            "size_formatted": self._format_size(self.size),
            "created_at": self.created_at.isoformat(),
            "backup_type": self.backup_type,
            "database": self.database,
            "compressed": self.compressed,
        }

    @staticmethod
    def _format_size(size: int) -> str:
        for unit in ["B", "KB", "MB", "GB"]:
            if size < 1024:
                return f"{size:.2f} {unit}"
            size /= 1024
        return f"{size:.2f} TB"


class BackupService:
    """
    P2.65: Database backup and restore service.

    Supports:
    - SQLite database backup
    - PostgreSQL database backup (pg_dump)
    - Compressed backups
    - Automatic cleanup of old backups
    - Restore from backup
    """

    def __init__(self, backup_dir: str = None):
        self.backup_dir = Path(backup_dir or BACKUP_DIR)
        self.backup_dir.mkdir(parents=True, exist_ok=True)

    # ==========================================================================
    # Backup Methods
    # ==========================================================================

    def create_backup(
        self, backup_type: str = "full", compress: bool = True, description: str = None
    ) -> BackupInfo:
        """
        Create a database backup.

        Args:
            backup_type: Type of backup ('full', 'schema', 'data')
            compress: Whether to compress the backup
            description: Optional description

        Returns:
            BackupInfo with details about the created backup
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        # Determine database type
        if "sqlite" in DATABASE_URL.lower() or DATABASE_URL.startswith("sqlite"):
            return self._backup_sqlite(timestamp, backup_type, compress)
        elif "postgresql" in DATABASE_URL.lower() or DATABASE_URL.startswith(
            "postgres"
        ):
            return self._backup_postgresql(timestamp, backup_type, compress)
        else:
            # Default to SQLite backup for the instance database
            return self._backup_sqlite(timestamp, backup_type, compress)

    def _backup_sqlite(
        self, timestamp: str, backup_type: str, compress: bool
    ) -> BackupInfo:
        """Backup SQLite database."""
        from flask import current_app

        # Get database path
        db_path = current_app.config.get("SQLALCHEMY_DATABASE_URI", "")
        if db_path.startswith("sqlite:///"):
            db_path = db_path.replace("sqlite:///", "")
        else:
            db_path = "instance/store.db"  # Default path

        if not os.path.exists(db_path):
            raise FileNotFoundError(f"Database file not found: {db_path}")

        # Create backup filename
        filename = f"backup_{timestamp}_{backup_type}"
        if compress:
            filename += ".db.gz"
        else:
            filename += ".db"

        filepath = self.backup_dir / filename

        # Copy or compress the database
        if compress:
            with open(db_path, "rb") as f_in:
                with gzip.open(filepath, "wb") as f_out:
                    shutil.copyfileobj(f_in, f_out)
        else:
            shutil.copy2(db_path, filepath)

        # Get file size
        size = os.path.getsize(filepath)

        # Create metadata
        self._save_metadata(
            filename,
            {
                "backup_type": backup_type,
                "database": "sqlite",
                "original_path": db_path,
                "compressed": compress,
                "created_at": datetime.now().isoformat(),
            },
        )

        logger.info(f"P2.65: Created SQLite backup: {filename}")

        return BackupInfo(
            filename=filename,
            filepath=str(filepath),
            size=size,
            created_at=datetime.now(),
            backup_type=backup_type,
            database="sqlite",
            compressed=compress,
        )

    def _backup_postgresql(
        self, timestamp: str, backup_type: str, compress: bool
    ) -> BackupInfo:
        """Backup PostgreSQL database using pg_dump."""
        # Parse database URL
        import urllib.parse

        parsed = urllib.parse.urlparse(DATABASE_URL)

        db_name = parsed.path[1:]  # Remove leading /
        host = parsed.hostname or "localhost"
        port = parsed.port or 5432
        user = parsed.username
        password = parsed.password

        # Create backup filename
        filename = f"backup_{timestamp}_{backup_type}"
        if compress:
            filename += ".sql.gz"
        else:
            filename += ".sql"

        filepath = self.backup_dir / filename

        # Build pg_dump command
        cmd = [
            "pg_dump",
            "-h",
            host,
            "-p",
            str(port),
            "-U",
            user,
            "-d",
            db_name,
            "-F",
            "p",  # Plain format
        ]

        if backup_type == "schema":
            cmd.append("--schema-only")
        elif backup_type == "data":
            cmd.append("--data-only")

        # Set password environment variable
        env = os.environ.copy()
        if password:
            env["PGPASSWORD"] = password

        # Execute pg_dump
        try:
            if compress:
                with gzip.open(filepath, "wt") as f:
                    result = subprocess.run(
                        cmd, stdout=f, stderr=subprocess.PIPE, env=env, check=True
                    )
            else:
                with open(filepath, "w") as f:
                    result = subprocess.run(
                        cmd, stdout=f, stderr=subprocess.PIPE, env=env, check=True
                    )
        except subprocess.CalledProcessError as e:
            logger.error(f"pg_dump failed: {e.stderr.decode()}")
            raise RuntimeError(f"PostgreSQL backup failed: {e.stderr.decode()}")

        size = os.path.getsize(filepath)

        # Save metadata
        self._save_metadata(
            filename,
            {
                "backup_type": backup_type,
                "database": "postgresql",
                "db_name": db_name,
                "compressed": compress,
                "created_at": datetime.now().isoformat(),
            },
        )

        logger.info(f"P2.65: Created PostgreSQL backup: {filename}")

        return BackupInfo(
            filename=filename,
            filepath=str(filepath),
            size=size,
            created_at=datetime.now(),
            backup_type=backup_type,
            database="postgresql",
            compressed=compress,
        )

    # ==========================================================================
    # Restore Methods
    # ==========================================================================

    def restore_backup(self, filename: str) -> bool:
        """
        Restore database from a backup file.

        Args:
            filename: Name of the backup file

        Returns:
            True if successful
        """
        filepath = self.backup_dir / filename

        if not filepath.exists():
            raise FileNotFoundError(f"Backup file not found: {filename}")

        # Load metadata
        metadata = self._load_metadata(filename)
        database = metadata.get("database", "sqlite")
        compressed = metadata.get("compressed", filename.endswith(".gz"))

        if database == "sqlite":
            return self._restore_sqlite(filepath, compressed, metadata)
        elif database == "postgresql":
            return self._restore_postgresql(filepath, compressed, metadata)
        else:
            raise ValueError(f"Unknown database type: {database}")

    def _restore_sqlite(self, filepath: Path, compressed: bool, metadata: dict) -> bool:
        """Restore SQLite database."""
        from flask import current_app

        # Get target database path
        db_path = metadata.get("original_path", "instance/store.db")

        # Create backup of current database before restore
        if os.path.exists(db_path):
            backup_current = f"{db_path}.before_restore"
            shutil.copy2(db_path, backup_current)
            logger.info(f"P2.65: Backed up current database to {backup_current}")

        # Restore
        try:
            if compressed:
                with gzip.open(filepath, "rb") as f_in:
                    with open(db_path, "wb") as f_out:
                        shutil.copyfileobj(f_in, f_out)
            else:
                shutil.copy2(filepath, db_path)

            logger.info(f"P2.65: Restored SQLite database from {filepath}")
            return True

        except Exception as e:
            logger.error(f"P2.65: Restore failed: {e}")
            # Attempt to restore the backup
            if os.path.exists(f"{db_path}.before_restore"):
                shutil.copy2(f"{db_path}.before_restore", db_path)
            raise

    def _restore_postgresql(
        self, filepath: Path, compressed: bool, metadata: dict
    ) -> bool:
        """Restore PostgreSQL database."""
        import urllib.parse

        parsed = urllib.parse.urlparse(DATABASE_URL)

        db_name = parsed.path[1:]
        host = parsed.hostname or "localhost"
        port = parsed.port or 5432
        user = parsed.username
        password = parsed.password

        env = os.environ.copy()
        if password:
            env["PGPASSWORD"] = password

        # Build psql command
        cmd = [
            "psql",
            "-h",
            host,
            "-p",
            str(port),
            "-U",
            user,
            "-d",
            db_name,
        ]

        try:
            if compressed:
                with gzip.open(filepath, "rt") as f:
                    result = subprocess.run(
                        cmd, stdin=f, stderr=subprocess.PIPE, env=env, check=True
                    )
            else:
                with open(filepath, "r") as f:
                    result = subprocess.run(
                        cmd, stdin=f, stderr=subprocess.PIPE, env=env, check=True
                    )

            logger.info(f"P2.65: Restored PostgreSQL database from {filepath}")
            return True

        except subprocess.CalledProcessError as e:
            logger.error(f"psql restore failed: {e.stderr.decode()}")
            raise RuntimeError(f"PostgreSQL restore failed: {e.stderr.decode()}")

    # ==========================================================================
    # Management Methods
    # ==========================================================================

    def list_backups(self) -> List[BackupInfo]:
        """List all available backups."""
        backups = []

        for filepath in self.backup_dir.glob("backup_*"):
            if filepath.suffix in [".db", ".gz", ".sql"]:
                stat = filepath.stat()
                metadata = self._load_metadata(filepath.name)

                backups.append(
                    BackupInfo(
                        filename=filepath.name,
                        filepath=str(filepath),
                        size=stat.st_size,
                        created_at=datetime.fromtimestamp(stat.st_mtime),
                        backup_type=metadata.get("backup_type", "full"),
                        database=metadata.get("database", "unknown"),
                        compressed=filepath.name.endswith(".gz"),
                    )
                )

        # Sort by date, newest first
        backups.sort(key=lambda x: x.created_at, reverse=True)

        return backups

    def delete_backup(self, filename: str) -> bool:
        """Delete a backup file."""
        filepath = self.backup_dir / filename
        metadata_path = self.backup_dir / f"{filename}.meta.json"

        if filepath.exists():
            filepath.unlink()
            logger.info(f"P2.65: Deleted backup: {filename}")

        if metadata_path.exists():
            metadata_path.unlink()

        return True

    def cleanup_old_backups(self, keep: int = None) -> int:
        """Remove old backups, keeping only the most recent ones."""
        keep = keep or MAX_BACKUPS
        backups = self.list_backups()

        deleted = 0
        if len(backups) > keep:
            for backup in backups[keep:]:
                self.delete_backup(backup.filename)
                deleted += 1

        logger.info(f"P2.65: Cleaned up {deleted} old backups")
        return deleted

    def get_backup_size(self) -> int:
        """Get total size of all backups."""
        total = 0
        for filepath in self.backup_dir.glob("backup_*"):
            total += filepath.stat().st_size
        return total

    # ==========================================================================
    # Helper Methods
    # ==========================================================================

    def _save_metadata(self, filename: str, metadata: dict):
        """Save backup metadata."""
        meta_path = self.backup_dir / f"{filename}.meta.json"
        with open(meta_path, "w") as f:
            json.dump(metadata, f, indent=2)

    def _load_metadata(self, filename: str) -> dict:
        """Load backup metadata."""
        meta_path = self.backup_dir / f"{filename}.meta.json"
        if meta_path.exists():
            with open(meta_path, "r") as f:
                return json.load(f)
        return {}


# =============================================================================
# Export Data Methods
# =============================================================================


def export_data_json(tables: List[str] = None) -> bytes:
    """Export database tables to JSON format."""
    from src.database import db
    from sqlalchemy import inspect

    inspector = inspect(db.engine)
    table_names = tables or inspector.get_table_names()

    data = {}

    for table_name in table_names:
        if table_name.startswith("alembic_"):
            continue

        result = db.session.execute(f"SELECT * FROM {table_name}")
        columns = result.keys()
        rows = [dict(zip(columns, row)) for row in result.fetchall()]
        data[table_name] = rows

    return json.dumps(data, indent=2, default=str).encode("utf-8")


def import_data_json(data: bytes, clear_existing: bool = False):
    """Import database tables from JSON format."""
    from src.database import db

    tables_data = json.loads(data.decode("utf-8"))

    for table_name, rows in tables_data.items():
        if clear_existing:
            db.session.execute(f"DELETE FROM {table_name}")

        for row in rows:
            columns = ", ".join(row.keys())
            placeholders = ", ".join([":" + k for k in row.keys()])
            sql = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"
            db.session.execute(sql, row)

    db.session.commit()


__all__ = ["BackupService", "BackupInfo", "export_data_json", "import_data_json"]
