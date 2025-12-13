# -*- coding: utf-8 -*-
"""
Database Connection Pool Configuration
=======================================

Optimized connection pool settings for production.
Part of T25: Database Optimization

Features:
- Connection pool configuration
- Pool monitoring
- Connection lifecycle management
- Pool health checks
"""

import logging
from typing import Dict, Any, Optional
from sqlalchemy import event, create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.pool import QueuePool, NullPool, StaticPool
import time

logger = logging.getLogger(__name__)


class ConnectionPoolConfig:
    """Connection pool configuration presets."""

    # Development (small pool, quick recycling)
    DEVELOPMENT = {
        "poolclass": StaticPool,
        "pool_size": 5,
        "max_overflow": 10,
        "pool_timeout": 30,
        "pool_recycle": 3600,  # 1 hour
        "pool_pre_ping": True,
        "echo_pool": True,
    }

    # Production (larger pool, optimized for performance)
    PRODUCTION = {
        "poolclass": QueuePool,
        "pool_size": 20,
        "max_overflow": 40,
        "pool_timeout": 30,
        "pool_recycle": 3600,  # 1 hour
        "pool_pre_ping": True,
        "echo_pool": False,
    }

    # Testing (no pooling for isolation)
    TESTING = {"poolclass": NullPool, "pool_pre_ping": False, "echo_pool": False}

    # High traffic (maximum connections)
    HIGH_TRAFFIC = {
        "poolclass": QueuePool,
        "pool_size": 50,
        "max_overflow": 100,
        "pool_timeout": 60,
        "pool_recycle": 1800,  # 30 minutes
        "pool_pre_ping": True,
        "echo_pool": False,
    }

    @classmethod
    def get_config(cls, environment: str = "development") -> Dict[str, Any]:
        """
        Get configuration for environment.

        Args:
            environment: Environment name (development, production, testing, high_traffic)

        Returns:
            Pool configuration dictionary
        """
        configs = {
            "development": cls.DEVELOPMENT,
            "production": cls.PRODUCTION,
            "testing": cls.TESTING,
            "high_traffic": cls.HIGH_TRAFFIC,
        }

        return configs.get(environment.lower(), cls.DEVELOPMENT)


class ConnectionPoolMonitor:
    """Monitor connection pool health and performance."""

    def __init__(self, engine: Engine):
        """
        Initialize monitor.

        Args:
            engine: SQLAlchemy engine
        """
        self.engine = engine
        self.stats = {
            "connections_created": 0,
            "connections_closed": 0,
            "checkouts": 0,
            "checkins": 0,
            "checkout_times": [],
        }

        # Register event listeners
        self._register_listeners()

    def _register_listeners(self):
        """Register SQLAlchemy event listeners."""

        @event.listens_for(self.engine, "connect")
        def receive_connect(dbapi_conn, connection_record):
            """Track connection creation."""
            self.stats["connections_created"] += 1
            logger.debug(
                f"Connection created (total: {self.stats['connections_created']})"
            )

        @event.listens_for(self.engine, "close")
        def receive_close(dbapi_conn, connection_record):
            """Track connection closure."""
            self.stats["connections_closed"] += 1
            logger.debug(
                f"Connection closed (total: {self.stats['connections_closed']})"
            )

        @event.listens_for(self.engine, "checkout")
        def receive_checkout(dbapi_conn, connection_record, connection_proxy):
            """Track connection checkout."""
            self.stats["checkouts"] += 1
            connection_record.checkout_time = time.time()

        @event.listens_for(self.engine, "checkin")
        def receive_checkin(dbapi_conn, connection_record):
            """Track connection checkin."""
            self.stats["checkins"] += 1

            if hasattr(connection_record, "checkout_time"):
                duration = time.time() - connection_record.checkout_time
                self.stats["checkout_times"].append(duration)

                # Keep only last 1000 checkout times
                if len(self.stats["checkout_times"]) > 1000:
                    self.stats["checkout_times"] = self.stats["checkout_times"][-1000:]

    def get_pool_status(self) -> Dict[str, Any]:
        """
        Get current pool status.

        Returns:
            Pool status dictionary
        """
        pool = self.engine.pool

        return {
            "size": pool.size(),
            "checked_in": pool.checkedin(),
            "checked_out": pool.checkedout(),
            "overflow": pool.overflow(),
            "total_connections": pool.size() + pool.overflow(),
            "utilization_percent": (
                (pool.checkedout() / pool.size() * 100) if pool.size() > 0 else 0
            ),
        }

    def get_statistics(self) -> Dict[str, Any]:
        """
        Get pool statistics.

        Returns:
            Statistics dictionary
        """
        checkout_times = self.stats["checkout_times"]

        avg_checkout_time = (
            sum(checkout_times) / len(checkout_times) if checkout_times else 0
        )
        max_checkout_time = max(checkout_times) if checkout_times else 0

        return {
            "connections_created": self.stats["connections_created"],
            "connections_closed": self.stats["connections_closed"],
            "active_connections": self.stats["connections_created"]
            - self.stats["connections_closed"],
            "checkouts": self.stats["checkouts"],
            "checkins": self.stats["checkins"],
            "avg_checkout_time_seconds": avg_checkout_time,
            "max_checkout_time_seconds": max_checkout_time,
            "pool_status": self.get_pool_status(),
        }

    def print_status(self):
        """Print pool status to console."""
        status = self.get_pool_status()
        stats = self.get_statistics()

        print("\n" + "=" * 60)
        print("🔌 CONNECTION POOL STATUS")
        print("=" * 60)

        print("\n📊 Pool Status:")
        print(f"  - Size: {status['size']}")
        print(f"  - Checked out: {status['checked_out']}")
        print(f"  - Checked in: {status['checked_in']}")
        print(f"  - Overflow: {status['overflow']}")
        print(f"  - Total connections: {status['total_connections']}")
        print(f"  - Utilization: {status['utilization_percent']:.1f}%")

        print("\n📈 Statistics:")
        print(f"  - Connections created: {stats['connections_created']}")
        print(f"  - Connections closed: {stats['connections_closed']}")
        print(f"  - Active connections: {stats['active_connections']}")
        print(f"  - Checkouts: {stats['checkouts']}")
        print(f"  - Checkins: {stats['checkins']}")
        print(f"  - Avg checkout time: {stats['avg_checkout_time_seconds']:.3f}s")
        print(f"  - Max checkout time: {stats['max_checkout_time_seconds']:.3f}s")

        print("\n" + "=" * 60)

    def check_health(self) -> Dict[str, Any]:
        """
        Check pool health.

        Returns:
            Health check result
        """
        status = self.get_pool_status()
        stats = self.get_statistics()

        issues = []
        warnings = []

        # Check utilization
        if status["utilization_percent"] > 90:
            issues.append("Pool utilization > 90% - consider increasing pool size")
        elif status["utilization_percent"] > 75:
            warnings.append("Pool utilization > 75% - monitor closely")

        # Check overflow
        if status["overflow"] > status["size"] * 0.5:
            warnings.append("High overflow usage - consider increasing pool size")

        # Check checkout time
        if stats["avg_checkout_time_seconds"] > 5.0:
            issues.append("Average checkout time > 5s - connections held too long")
        elif stats["avg_checkout_time_seconds"] > 2.0:
            warnings.append("Average checkout time > 2s - monitor query performance")

        # Check connection leaks
        if stats["checkouts"] > stats["checkins"] + 10:
            leak_count = stats["checkouts"] - stats["checkins"]
            issues.append(
                f"Possible connection leak: {leak_count} unchecked connections"
            )

        health_status = "healthy"
        if issues:
            health_status = "critical"
        elif warnings:
            health_status = "warning"

        return {
            "status": health_status,
            "issues": issues,
            "warnings": warnings,
            "pool_status": status,
            "statistics": stats,
        }


def configure_pool(database_url: str, environment: str = "development") -> Engine:
    """
    Create engine with optimized pool configuration.

    Args:
        database_url: Database connection URL
        environment: Environment name

    Returns:
        Configured SQLAlchemy engine
    """
    config = ConnectionPoolConfig.get_config(environment)

    engine = create_engine(database_url, **config)

    logger.info(f"Connection pool configured for {environment} environment")
    logger.info(
        f"Pool size: {config.get('pool_size', 'N/A')}, "
        f"Max overflow: {config.get('max_overflow', 'N/A')}"
    )

    return engine


def test_pool_performance(engine: Engine, num_connections: int = 100):
    """
    Test pool performance.

    Args:
        engine: SQLAlchemy engine
        num_connections: Number of connections to test
    """
    print(f"\n🧪 Testing pool performance with {num_connections} connections...")

    start_time = time.time()

    for i in range(num_connections):
        conn = engine.connect()
        conn.execute("SELECT 1")
        conn.close()

    duration = time.time() - start_time

    print(f"✅ Completed {num_connections} connections in {duration:.2f}s")
    print(f"   Average: {duration / num_connections * 1000:.2f}ms per connection")
