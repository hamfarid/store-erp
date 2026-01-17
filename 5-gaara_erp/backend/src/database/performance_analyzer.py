# -*- coding: utf-8 -*-
"""
Database Performance Analyzer
==============================

Analyze database performance and identify optimization opportunities.
Part of T25: Database Optimization

Features:
- Query analysis
- Index recommendations
- Slow query detection
- Table statistics
- Connection pool monitoring
"""

import time
import logging
from typing import List, Dict, Any, Optional
from datetime import datetime, timedelta
from collections import defaultdict
from sqlalchemy import text, inspect
from sqlalchemy.engine import Engine
from database import db

logger = logging.getLogger(__name__)


class QueryStats:
    """Track query statistics."""

    def __init__(self):
        self.queries: Dict[str, Dict[str, Any]] = defaultdict(
            lambda: {
                "count": 0,
                "total_time": 0.0,
                "min_time": float("inf"),
                "max_time": 0.0,
                "avg_time": 0.0,
            }
        )

    def record_query(self, query: str, duration: float):
        """Record query execution."""
        stats = self.queries[query]
        stats["count"] += 1
        stats["total_time"] += duration
        stats["min_time"] = min(stats["min_time"], duration)
        stats["max_time"] = max(stats["max_time"], duration)
        stats["avg_time"] = stats["total_time"] / stats["count"]

    def get_slow_queries(self, threshold_ms: float = 100.0) -> List[Dict[str, Any]]:
        """Get queries slower than threshold."""
        slow_queries = []

        for query, stats in self.queries.items():
            if stats["avg_time"] * 1000 > threshold_ms:
                slow_queries.append(
                    {
                        "query": query[:200],  # Truncate long queries
                        "count": stats["count"],
                        "avg_time_ms": stats["avg_time"] * 1000,
                        "max_time_ms": stats["max_time"] * 1000,
                        "total_time_ms": stats["total_time"] * 1000,
                    }
                )

        # Sort by total time (most impactful first)
        slow_queries.sort(key=lambda x: x["total_time_ms"], reverse=True)

        return slow_queries

    def get_most_frequent(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Get most frequently executed queries."""
        frequent = []

        for query, stats in self.queries.items():
            frequent.append(
                {
                    "query": query[:200],
                    "count": stats["count"],
                    "avg_time_ms": stats["avg_time"] * 1000,
                }
            )

        frequent.sort(key=lambda x: x["count"], reverse=True)

        return frequent[:limit]


class DatabasePerformanceAnalyzer:
    """Analyze database performance."""

    def __init__(self, engine: Optional[Engine] = None):
        """
        Initialize analyzer.

        Args:
            engine: SQLAlchemy engine (uses db.engine if not provided)
        """
        self.engine = engine or db.engine
        self.query_stats = QueryStats()

    def analyze_tables(self) -> List[Dict[str, Any]]:
        """
        Analyze all tables.

        Returns:
            List of table statistics
        """
        inspector = inspect(self.engine)
        tables = []

        for table_name in inspector.get_table_names():
            try:
                # Get row count
                result = db.session.execute(
                    text(f"SELECT COUNT(*) FROM {table_name}")
                ).fetchone()
                row_count = result[0] if result else 0

                # Get columns
                columns = inspector.get_columns(table_name)

                # Get indexes
                indexes = inspector.get_indexes(table_name)

                # Get foreign keys
                foreign_keys = inspector.get_foreign_keys(table_name)

                tables.append(
                    {
                        "name": table_name,
                        "row_count": row_count,
                        "column_count": len(columns),
                        "index_count": len(indexes),
                        "foreign_key_count": len(foreign_keys),
                        "columns": [col["name"] for col in columns],
                        "indexes": [idx["name"] for idx in indexes],
                    }
                )

            except Exception as e:
                logger.error(f"Error analyzing table {table_name}: {e}")

        return tables

    def find_missing_indexes(self) -> List[Dict[str, Any]]:
        """
        Find columns that might benefit from indexes.

        Returns:
            List of index recommendations
        """
        inspector = inspect(self.engine)
        recommendations = []

        for table_name in inspector.get_table_names():
            try:
                # Get existing indexes
                existing_indexes = inspector.get_indexes(table_name)
                indexed_columns = set()
                for idx in existing_indexes:
                    indexed_columns.update(idx["column_names"])

                # Get foreign keys (should be indexed)
                foreign_keys = inspector.get_foreign_keys(table_name)
                for fk in foreign_keys:
                    for col in fk["constrained_columns"]:
                        if col not in indexed_columns:
                            recommendations.append(
                                {
                                    "table": table_name,
                                    "column": col,
                                    "reason": "Foreign key without index",
                                    "priority": "HIGH",
                                    "index_name": f"idx_{table_name}_{col}",
                                }
                            )

                # Check for common query patterns
                # (This is simplified - in production, analyze actual query logs)
                columns = inspector.get_columns(table_name)
                for col in columns:
                    col_name = col["name"]

                    # Skip if already indexed
                    if col_name in indexed_columns:
                        continue

                    # Recommend indexes for common patterns
                    if col_name in ["created_at", "updated_at"]:
                        recommendations.append(
                            {
                                "table": table_name,
                                "column": col_name,
                                "reason": "Timestamp column (common in WHERE/ORDER BY)",
                                "priority": "MEDIUM",
                                "index_name": f"idx_{table_name}_{col_name}",
                            }
                        )
                    elif col_name in ["is_active", "status", "type"]:
                        recommendations.append(
                            {
                                "table": table_name,
                                "column": col_name,
                                "reason": "Status/filter column (common in WHERE)",
                                "priority": "MEDIUM",
                                "index_name": f"idx_{table_name}_{col_name}",
                            }
                        )
                    elif col_name.endswith("_id") and col_name not in indexed_columns:
                        recommendations.append(
                            {
                                "table": table_name,
                                "column": col_name,
                                "reason": "ID column (likely used in joins)",
                                "priority": "HIGH",
                                "index_name": f"idx_{table_name}_{col_name}",
                            }
                        )

            except Exception as e:
                logger.error(f"Error finding missing indexes for {table_name}: {e}")

        return recommendations

    def analyze_connection_pool(self) -> Dict[str, Any]:
        """
        Analyze connection pool status.

        Returns:
            Connection pool statistics
        """
        pool = self.engine.pool

        return {
            "size": pool.size(),
            "checked_in": pool.checkedin(),
            "checked_out": pool.checkedout(),
            "overflow": pool.overflow(),
            "total_connections": pool.size() + pool.overflow(),
            "utilization": (
                (pool.checkedout() / pool.size() * 100) if pool.size() > 0 else 0
            ),
        }

    def get_table_sizes(self) -> List[Dict[str, Any]]:
        """
        Get table sizes (PostgreSQL only).

        Returns:
            List of table sizes
        """
        try:
            # This works for PostgreSQL
            result = db.session.execute(
                text(
                    """
                SELECT
                    table_name,
                    pg_size_pretty(pg_total_relation_size(quote_ident(table_name))) as size,
                    pg_total_relation_size(quote_ident(table_name)) as size_bytes
                FROM information_schema.tables
                WHERE table_schema = 'public'
                ORDER BY pg_total_relation_size(quote_ident(table_name)) DESC
            """
                )
            )

            return [
                {"table": row[0], "size": row[1], "size_bytes": row[2]}
                for row in result
            ]
        except Exception as e:
            logger.warning(f"Could not get table sizes (PostgreSQL only): {e}")
            return []

    def generate_report(self) -> Dict[str, Any]:
        """
        Generate comprehensive performance report.

        Returns:
            Performance report
        """
        return {
            "timestamp": datetime.utcnow().isoformat(),
            "tables": self.analyze_tables(),
            "missing_indexes": self.find_missing_indexes(),
            "connection_pool": self.analyze_connection_pool(),
            "slow_queries": self.query_stats.get_slow_queries(),
            "frequent_queries": self.query_stats.get_most_frequent(),
            "table_sizes": self.get_table_sizes(),
        }

    def print_report(self):
        """Print performance report to console."""
        report = self.generate_report()

        print("\n" + "=" * 80)
        print("📊 DATABASE PERFORMANCE REPORT")
        print("=" * 80)
        print(f"Generated: {report['timestamp']}")

        # Tables
        print("\n📋 TABLES:")
        for table in report["tables"]:
            print(
                f"  - {table['name']}: {table['row_count']} rows, "
                f"{table['index_count']} indexes"
            )

        # Missing indexes
        print("\n🔍 MISSING INDEXES:")
        if report["missing_indexes"]:
            for rec in report["missing_indexes"][:10]:  # Top 10
                print(
                    f"  - {rec['table']}.{rec['column']} ({rec['priority']}): {rec['reason']}"
                )
        else:
            print("  ✅ No missing indexes found")

        # Connection pool
        print("\n🔌 CONNECTION POOL:")
        pool = report["connection_pool"]
        print(f"  - Size: {pool['size']}")
        print(f"  - Checked out: {pool['checked_out']}")
        print(f"  - Utilization: {pool['utilization']:.1f}%")

        # Slow queries
        print("\n🐌 SLOW QUERIES:")
        if report["slow_queries"]:
            for query in report["slow_queries"][:5]:  # Top 5
                print(f"  - {query['query'][:100]}...")
                print(
                    f"    Avg: {query['avg_time_ms']:.2f}ms, "
                    f"Max: {query['max_time_ms']:.2f}ms, "
                    f"Count: {query['count']}"
                )
        else:
            print("  ✅ No slow queries detected")

        print("\n" + "=" * 80)
