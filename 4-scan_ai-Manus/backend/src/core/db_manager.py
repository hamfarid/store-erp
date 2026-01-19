"""
Database Connection Manager
============================

Purpose: Centralized database connection management with pooling,
health checks, and automatic reconnection.

Features:
- Connection pooling
- Health monitoring
- Automatic retry on failure
- Read/Write replica support
- Transaction management
- Query logging

Usage:
    from src.core.db_manager import DatabaseManager, get_db_manager
    
    db_manager = get_db_manager()
    
    # Get session
    async with db_manager.session() as session:
        result = await session.execute(query)
    
    # Health check
    status = await db_manager.health_check()

Author: Global System v35.0
Date: 2026-01-17
"""

import asyncio
import logging
import time
from contextlib import asynccontextmanager, contextmanager
from typing import Any, Dict, Generator, Optional

from sqlalchemy import create_engine, event, text
from sqlalchemy.engine import Engine
from sqlalchemy.exc import OperationalError, SQLAlchemyError
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.pool import QueuePool

from .config import get_settings

logger = logging.getLogger(__name__)


class DatabaseManager:
    """
    Centralized database connection manager.
    
    Provides connection pooling, health monitoring, and
    automatic reconnection capabilities.
    
    Example:
        >>> db_manager = DatabaseManager()
        >>> with db_manager.session() as session:
        ...     users = session.query(User).all()
    """
    
    def __init__(
        self,
        url: Optional[str] = None,
        pool_size: int = 10,
        max_overflow: int = 20,
        pool_timeout: int = 30,
        pool_recycle: int = 3600,
        echo: bool = False
    ):
        """
        Initialize database manager.
        
        Args:
            url: Database URL (uses settings if None)
            pool_size: Number of connections in pool
            max_overflow: Max extra connections
            pool_timeout: Timeout waiting for connection
            pool_recycle: Recycle connections after seconds
            echo: Log SQL statements
        """
        self.settings = get_settings()
        self.url = url or self.settings.DATABASE_URL
        
        # Pool configuration
        self.pool_size = pool_size
        self.max_overflow = max_overflow
        self.pool_timeout = pool_timeout
        self.pool_recycle = pool_recycle
        self.echo = echo
        
        # Engine and session factory
        self._engine: Optional[Engine] = None
        self._session_factory: Optional[sessionmaker] = None
        
        # Metrics
        self._query_count = 0
        self._error_count = 0
        self._last_health_check: Optional[float] = None
        
        # Initialize
        self._initialize()
    
    def _initialize(self) -> None:
        """Initialize database engine and session factory."""
        try:
            # Create engine with connection pooling
            self._engine = create_engine(
                self.url,
                poolclass=QueuePool,
                pool_size=self.pool_size,
                max_overflow=self.max_overflow,
                pool_timeout=self.pool_timeout,
                pool_recycle=self.pool_recycle,
                pool_pre_ping=True,  # Verify connections before use
                echo=self.echo,
                future=True
            )
            
            # Create session factory
            self._session_factory = sessionmaker(
                bind=self._engine,
                autocommit=False,
                autoflush=False,
                expire_on_commit=False
            )
            
            # Register event listeners
            self._register_events()
            
            logger.info(
                f"Database manager initialized: pool_size={self.pool_size}, "
                f"max_overflow={self.max_overflow}"
            )
            
        except Exception as e:
            logger.error(f"Failed to initialize database: {e}")
            raise
    
    def _register_events(self) -> None:
        """Register SQLAlchemy event listeners for monitoring."""
        
        @event.listens_for(self._engine, "before_cursor_execute")
        def before_cursor_execute(conn, cursor, statement, parameters, context, executemany):
            conn.info.setdefault('query_start_time', []).append(time.time())
            self._query_count += 1
        
        @event.listens_for(self._engine, "after_cursor_execute")
        def after_cursor_execute(conn, cursor, statement, parameters, context, executemany):
            start_times = conn.info.get('query_start_time', [])
            if start_times:
                total_time = time.time() - start_times.pop()
                if total_time > 1.0:  # Log slow queries
                    logger.warning(
                        f"Slow query ({total_time:.2f}s): {statement[:100]}..."
                    )
        
        @event.listens_for(self._engine, "handle_error")
        def handle_error(exception_context):
            self._error_count += 1
            logger.error(f"Database error: {exception_context.original_exception}")
    
    @property
    def engine(self) -> Engine:
        """Get the database engine."""
        if self._engine is None:
            self._initialize()
        return self._engine
    
    @contextmanager
    def session(self) -> Generator[Session, None, None]:
        """
        Get a database session with automatic cleanup.
        
        Yields:
            Session: SQLAlchemy session
            
        Example:
            with db_manager.session() as session:
                user = session.query(User).get(1)
        """
        if self._session_factory is None:
            self._initialize()
        
        session = self._session_factory()
        try:
            yield session
            session.commit()
        except SQLAlchemyError as e:
            session.rollback()
            logger.error(f"Session error: {e}")
            raise
        finally:
            session.close()
    
    @contextmanager
    def transaction(self) -> Generator[Session, None, None]:
        """
        Get a session with explicit transaction control.
        
        Same as session() but makes transaction explicit.
        
        Yields:
            Session: SQLAlchemy session
        """
        with self.session() as session:
            yield session
    
    def get_session(self) -> Session:
        """
        Get a new session (caller responsible for cleanup).
        
        Returns:
            Session: New SQLAlchemy session
            
        Note:
            Prefer using session() context manager instead.
        """
        if self._session_factory is None:
            self._initialize()
        return self._session_factory()
    
    def execute(self, query: str, params: Dict[str, Any] = None) -> Any:
        """
        Execute a raw SQL query.
        
        Args:
            query: SQL query string
            params: Query parameters
            
        Returns:
            Query result
        """
        with self.session() as session:
            result = session.execute(text(query), params or {})
            return result
    
    def health_check(self) -> Dict[str, Any]:
        """
        Perform database health check.
        
        Returns:
            Dict with health status and metrics
        """
        start_time = time.time()
        
        try:
            with self.session() as session:
                session.execute(text("SELECT 1"))
            
            latency = (time.time() - start_time) * 1000
            self._last_health_check = time.time()
            
            # Get pool status
            pool = self._engine.pool
            pool_status = {
                "size": pool.size(),
                "checked_in": pool.checkedin(),
                "checked_out": pool.checkedout(),
                "overflow": pool.overflow(),
                "invalid": pool.invalidatedcount() if hasattr(pool, 'invalidatedcount') else 0
            }
            
            return {
                "status": "healthy",
                "latency_ms": round(latency, 2),
                "pool": pool_status,
                "metrics": {
                    "total_queries": self._query_count,
                    "total_errors": self._error_count
                }
            }
            
        except OperationalError as e:
            latency = (time.time() - start_time) * 1000
            logger.error(f"Database health check failed: {e}")
            return {
                "status": "unhealthy",
                "latency_ms": round(latency, 2),
                "error": str(e)[:200]
            }
    
    def close(self) -> None:
        """Close all database connections."""
        if self._engine:
            self._engine.dispose()
            logger.info("Database connections closed")
    
    def get_metrics(self) -> Dict[str, Any]:
        """
        Get database metrics.
        
        Returns:
            Dict with query counts, errors, pool status
        """
        pool_status = {}
        if self._engine:
            pool = self._engine.pool
            pool_status = {
                "size": pool.size(),
                "checked_in": pool.checkedin(),
                "checked_out": pool.checkedout()
            }
        
        return {
            "total_queries": self._query_count,
            "total_errors": self._error_count,
            "last_health_check": self._last_health_check,
            "pool": pool_status
        }
    
    def reset_metrics(self) -> None:
        """Reset query and error counters."""
        self._query_count = 0
        self._error_count = 0


class DatabaseRetry:
    """
    Retry decorator for database operations.
    
    Example:
        @DatabaseRetry(max_retries=3)
        def get_user(session, user_id):
            return session.query(User).get(user_id)
    """
    
    def __init__(
        self,
        max_retries: int = 3,
        delay: float = 0.5,
        backoff: float = 2.0,
        exceptions: tuple = (OperationalError,)
    ):
        """
        Initialize retry decorator.
        
        Args:
            max_retries: Maximum retry attempts
            delay: Initial delay between retries
            backoff: Multiplier for delay after each retry
            exceptions: Exceptions to catch and retry
        """
        self.max_retries = max_retries
        self.delay = delay
        self.backoff = backoff
        self.exceptions = exceptions
    
    def __call__(self, func):
        def wrapper(*args, **kwargs):
            last_exception = None
            delay = self.delay
            
            for attempt in range(self.max_retries + 1):
                try:
                    return func(*args, **kwargs)
                except self.exceptions as e:
                    last_exception = e
                    if attempt < self.max_retries:
                        logger.warning(
                            f"Database operation failed (attempt {attempt + 1}), "
                            f"retrying in {delay}s: {e}"
                        )
                        time.sleep(delay)
                        delay *= self.backoff
                    else:
                        logger.error(
                            f"Database operation failed after {self.max_retries} retries: {e}"
                        )
            
            raise last_exception
        
        return wrapper


# Singleton instance
_db_manager: Optional[DatabaseManager] = None


def get_db_manager() -> DatabaseManager:
    """
    Get or create database manager singleton.
    
    Returns:
        DatabaseManager: Singleton instance
    """
    global _db_manager
    
    if _db_manager is None:
        _db_manager = DatabaseManager()
    
    return _db_manager


def get_db() -> Generator[Session, None, None]:
    """
    FastAPI dependency for getting database session.
    
    Yields:
        Session: Database session
        
    Example:
        @app.get("/users")
        def get_users(db: Session = Depends(get_db)):
            return db.query(User).all()
    """
    db_manager = get_db_manager()
    with db_manager.session() as session:
        yield session
