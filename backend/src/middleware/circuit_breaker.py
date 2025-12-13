"""
Circuit Breaker Middleware - Resilience Pattern Implementation

Implements the circuit breaker pattern for fault tolerance:
- CLOSED: Normal operation, all requests pass
- OPEN: Repeated failures, reject requests immediately (fail-fast)
- HALF_OPEN: Recovery probe, allow limited trial requests

Aligned to GLOBAL_GUIDELINES_UNIFIED_v8.0.0 Section XLV (Resilience & Circuit Breakers)
"""

import time
import logging
from enum import Enum
from typing import Any, Callable, Dict, Optional
from datetime import datetime
from dataclasses import dataclass, field

logger = logging.getLogger(__name__)


class CircuitState(Enum):
    """Circuit breaker states"""

    CLOSED = "closed"  # Normal operation
    OPEN = "open"  # Failing, reject requests
    HALF_OPEN = "half_open"  # Recovery probe


@dataclass
class CircuitBreakerConfig:
    """Configuration for a circuit breaker"""

    name: str
    failure_rate_threshold: float = 0.50  # 50% failure rate
    rolling_window_seconds: int = 60  # 60 second window
    minimum_throughput: int = 20  # Minimum requests to evaluate
    open_state_duration: int = 60  # 60 seconds in OPEN state
    half_open_max_in_flight: int = 10  # Max concurrent requests in HALF_OPEN
    success_quorum_to_close: float = 0.80  # 80% success to close
    timeout_seconds: int = 5  # Request timeout
    max_retries: int = 2  # Retry attempts
    fallback_strategy: str = "fail"  # fail, cached, graceful


@dataclass
class CircuitBreakerMetrics:
    """Metrics for a circuit breaker"""

    name: str
    state: CircuitState = CircuitState.CLOSED
    failures_total: int = 0
    successes_total: int = 0
    rejections_total: int = 0
    half_open_probes: int = 0
    last_failure_time: Optional[datetime] = None
    last_success_time: Optional[datetime] = None
    state_change_time: datetime = field(default_factory=datetime.now)
    recent_failures: list = field(default_factory=list)  # Last N failures

    def get_failure_rate(self) -> float:
        """Calculate current failure rate"""
        total = self.failures_total + self.successes_total
        if total == 0:
            return 0.0
        return self.failures_total / total


class CircuitBreaker:
    """
    Circuit breaker for fault tolerance.

    Usage:
        breaker = CircuitBreaker(config)
        try:
            result = breaker.call(func, *args, **kwargs)
        except CircuitBreakerOpen:
            # Handle open circuit
            result = fallback()
    """

    def __init__(self, config: CircuitBreakerConfig):
        self.config = config
        self.metrics = CircuitBreakerMetrics(name=config.name)
        self._half_open_in_flight = 0
        self._last_open_time: Optional[datetime] = None

    def call(self, func: Callable, *args, **kwargs) -> Any:
        """
        Execute function with circuit breaker protection.

        Args:
            func: Function to execute
            *args: Positional arguments
            **kwargs: Keyword arguments

        Returns:
            Function result

        Raises:
            CircuitBreakerOpen: If circuit is open
            CircuitBreakerError: If function fails
        """
        # Check state
        if self.metrics.state == CircuitState.OPEN:
            if self._should_attempt_reset():
                self.metrics.state = CircuitState.HALF_OPEN
                self.metrics.state_change_time = datetime.now()
                logger.info(
                    f"Circuit breaker '{self.config.name}' transitioning to HALF_OPEN"
                )
            else:
                self.metrics.rejections_total += 1
                raise CircuitBreakerOpen(
                    f"Circuit breaker '{self.config.name}' is OPEN"
                )

        # Execute with retries
        for attempt in range(self.config.max_retries + 1):
            try:
                result = func(*args, **kwargs)
                self._on_success()
                return result
            except Exception as e:
                if attempt < self.config.max_retries:
                    time.sleep(0.1 * (2**attempt))  # Exponential backoff
                    continue
                self._on_failure(e)
                raise

    def _should_attempt_reset(self) -> bool:
        """Check if enough time has passed to attempt reset"""
        if self._last_open_time is None:
            return False

        elapsed = (datetime.now() - self._last_open_time).total_seconds()
        return elapsed >= self.config.open_state_duration

    def _on_success(self):
        """Handle successful call"""
        self.metrics.successes_total += 1
        self.metrics.last_success_time = datetime.now()

        # If in HALF_OPEN, check if we can close
        if self.metrics.state == CircuitState.HALF_OPEN:
            self.metrics.half_open_probes += 1
            success_rate = self.metrics.half_open_probes / max(
                1, self.metrics.half_open_probes
            )

            if success_rate >= self.config.success_quorum_to_close:
                self._close()

    def _on_failure(self, error: Exception):
        """Handle failed call"""
        self.metrics.failures_total += 1
        self.metrics.last_failure_time = datetime.now()
        self.metrics.recent_failures.append(
            {
                "time": datetime.now().isoformat(),
                "error": str(error),
                "type": type(error).__name__,
            }
        )

        # Keep only last 10 failures
        if len(self.metrics.recent_failures) > 10:
            self.metrics.recent_failures = self.metrics.recent_failures[-10:]

        # Check if should open
        total = self.metrics.failures_total + self.metrics.successes_total
        if total >= self.config.minimum_throughput:
            failure_rate = self.metrics.get_failure_rate()
            if failure_rate >= self.config.failure_rate_threshold:
                self._open()

    def _open(self):
        """Transition to OPEN state"""
        if self.metrics.state != CircuitState.OPEN:
            self.metrics.state = CircuitState.OPEN
            self.metrics.state_change_time = datetime.now()
            self._last_open_time = datetime.now()
            logger.warning(
                f"Circuit breaker '{self.config.name}' opened. "
                f"Failure rate: {self.metrics.get_failure_rate():.2%}"
            )

    def _close(self):
        """Transition to CLOSED state"""
        if self.metrics.state != CircuitState.CLOSED:
            self.metrics.state = CircuitState.CLOSED
            self.metrics.state_change_time = datetime.now()
            self.metrics.failures_total = 0
            self.metrics.successes_total = 0
            self.metrics.half_open_probes = 0
            logger.info(f"Circuit breaker '{self.config.name}' closed")

    def get_metrics(self) -> Dict[str, Any]:
        """Get current metrics"""
        return {
            "name": self.config.name,
            "state": self.metrics.state.value,
            "failures_total": self.metrics.failures_total,
            "successes_total": self.metrics.successes_total,
            "rejections_total": self.metrics.rejections_total,
            "failure_rate": self.metrics.get_failure_rate(),
            "half_open_probes": self.metrics.half_open_probes,
            "last_failure_time": (
                self.metrics.last_failure_time.isoformat()
                if self.metrics.last_failure_time
                else None
            ),
            "last_success_time": (
                self.metrics.last_success_time.isoformat()
                if self.metrics.last_success_time
                else None
            ),
            "state_change_time": self.metrics.state_change_time.isoformat(),
            "recent_failures": self.metrics.recent_failures[-5:],  # Last 5
        }


class CircuitBreakerOpen(Exception):
    """Raised when circuit breaker is open"""

    pass


class CircuitBreakerError(Exception):
    """Raised when circuit breaker encounters an error"""

    pass
