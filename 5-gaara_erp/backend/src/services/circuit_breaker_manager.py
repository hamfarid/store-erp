"""
Circuit Breaker Manager - Registry and Configuration

Manages all circuit breakers in the system, provides centralized configuration,
and handles metrics aggregation.

Aligned to GLOBAL_GUIDELINES_UNIFIED_v8.0.0 Section XLV (Resilience & Circuit Breakers)
"""

import os
import logging
from typing import Dict, Any, Optional, Callable
from src.middleware.circuit_breaker import (
    CircuitBreaker,
    CircuitBreakerConfig,
    CircuitBreakerOpen,
)

logger = logging.getLogger(__name__)


class CircuitBreakerManager:
    """
    Centralized manager for all circuit breakers.

    Usage:
        manager = CircuitBreakerManager()
        manager.register_breaker("database", config)
        manager.register_breaker("external_api", config)

        # Use breaker
        result = manager.call("database", query_func, *args)
    """

    def __init__(self):
        self.breakers: Dict[str, CircuitBreaker] = {}
        self._initialize_default_breakers()

    def _initialize_default_breakers(self):
        """Initialize default circuit breakers"""

        # Database breaker
        db_config = CircuitBreakerConfig(
            name="database",
            failure_rate_threshold=float(os.getenv("CB_DB_FAILURE_RATE", "0.50")),
            rolling_window_seconds=int(os.getenv("CB_DB_WINDOW", "60")),
            minimum_throughput=int(os.getenv("CB_DB_MIN_THROUGHPUT", "20")),
            open_state_duration=int(os.getenv("CB_DB_OPEN_DURATION", "60")),
            timeout_seconds=int(os.getenv("CB_DB_TIMEOUT", "5")),
            max_retries=int(os.getenv("CB_DB_RETRIES", "2")),
            fallback_strategy="cached",
        )
        self.register_breaker("database", db_config)

        # External API breaker
        api_config = CircuitBreakerConfig(
            name="external_api",
            failure_rate_threshold=float(os.getenv("CB_API_FAILURE_RATE", "0.50")),
            rolling_window_seconds=int(os.getenv("CB_API_WINDOW", "60")),
            minimum_throughput=int(os.getenv("CB_API_MIN_THROUGHPUT", "10")),
            open_state_duration=int(os.getenv("CB_API_OPEN_DURATION", "120")),
            timeout_seconds=int(os.getenv("CB_API_TIMEOUT", "10")),
            max_retries=int(os.getenv("CB_API_RETRIES", "1")),
            fallback_strategy="graceful",
        )
        self.register_breaker("external_api", api_config)

        # Cache breaker
        cache_config = CircuitBreakerConfig(
            name="cache",
            failure_rate_threshold=float(os.getenv("CB_CACHE_FAILURE_RATE", "0.70")),
            rolling_window_seconds=int(os.getenv("CB_CACHE_WINDOW", "30")),
            minimum_throughput=int(os.getenv("CB_CACHE_MIN_THROUGHPUT", "50")),
            open_state_duration=int(os.getenv("CB_CACHE_OPEN_DURATION", "30")),
            timeout_seconds=int(os.getenv("CB_CACHE_TIMEOUT", "2")),
            max_retries=int(os.getenv("CB_CACHE_RETRIES", "0")),
            fallback_strategy="fail",
        )
        self.register_breaker("cache", cache_config)

        # RAG service breaker
        rag_config = CircuitBreakerConfig(
            name="rag_service",
            failure_rate_threshold=float(os.getenv("CB_RAG_FAILURE_RATE", "0.50")),
            rolling_window_seconds=int(os.getenv("CB_RAG_WINDOW", "60")),
            minimum_throughput=int(os.getenv("CB_RAG_MIN_THROUGHPUT", "10")),
            open_state_duration=int(os.getenv("CB_RAG_OPEN_DURATION", "60")),
            timeout_seconds=int(os.getenv("CB_RAG_TIMEOUT", "5")),
            max_retries=int(os.getenv("CB_RAG_RETRIES", "1")),
            fallback_strategy="graceful",
        )
        self.register_breaker("rag_service", rag_config)

    def register_breaker(self, name: str, config: CircuitBreakerConfig):
        """Register a new circuit breaker"""
        self.breakers[name] = CircuitBreaker(config)
        logger.info(f"Registered circuit breaker: {name}")

    def get_breaker(self, name: str) -> Optional[CircuitBreaker]:
        """Get a circuit breaker by name"""
        return self.breakers.get(name)

    def call(
        self,
        breaker_name: str,
        func: Callable,
        *args,
        fallback: Optional[Callable] = None,
        **kwargs,
    ) -> Any:
        """
        Execute function with circuit breaker protection.

        Args:
            breaker_name: Name of the circuit breaker
            func: Function to execute
            *args: Positional arguments
            fallback: Fallback function if circuit is open
            **kwargs: Keyword arguments

        Returns:
            Function result or fallback result
        """
        breaker = self.get_breaker(breaker_name)
        if not breaker:
            logger.warning(
                f"Circuit breaker '{breaker_name}' not found, executing without protection"
            )
            return func(*args, **kwargs)

        try:
            return breaker.call(func, *args, **kwargs)
        except CircuitBreakerOpen as e:
            logger.warning(f"Circuit breaker open: {breaker_name}")
            if fallback:
                logger.info(f"Executing fallback for {breaker_name}")
                return fallback(*args, **kwargs)
            raise

    def get_all_metrics(self) -> Dict[str, Any]:
        """Get metrics for all circuit breakers"""
        return {name: breaker.get_metrics() for name, breaker in self.breakers.items()}

    def get_breaker_metrics(self, name: str) -> Optional[Dict[str, Any]]:
        """Get metrics for a specific circuit breaker"""
        breaker = self.get_breaker(name)
        if breaker:
            return breaker.get_metrics()
        return None

    def reset_breaker(self, name: str) -> bool:
        """Reset a circuit breaker to CLOSED state"""
        breaker = self.get_breaker(name)
        if breaker:
            breaker._close()
            logger.info(f"Reset circuit breaker: {name}")
            return True
        return False

    def reset_all(self):
        """Reset all circuit breakers"""
        for name, breaker in self.breakers.items():
            breaker._close()
        logger.info("Reset all circuit breakers")


# Global instance
_manager: Optional[CircuitBreakerManager] = None


def get_circuit_breaker_manager() -> CircuitBreakerManager:
    """Get or create the global circuit breaker manager"""
    global _manager
    if _manager is None:
        _manager = CircuitBreakerManager()
    return _manager
