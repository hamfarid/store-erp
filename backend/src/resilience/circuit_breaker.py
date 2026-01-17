"""
Simple, dependency-free Circuit Breaker implementation.

States:
- CLOSED: all calls pass through; track rolling failure rate.
- OPEN: short-circuit calls; after open_state_seconds, allow half-open probes.
- HALF_OPEN: allow limited concurrent probes; if success quorum reached -> CLOSE;
  if any failure -> OPEN again.

Thread-safe and per-service named breakers via a registry.
"""

from __future__ import annotations

import threading
import time
from collections import deque
from dataclasses import dataclass
from typing import Deque, Dict, Tuple


class CircuitOpenError(RuntimeError):
    """Raised when circuit is OPEN and request is short-circuited."""


@dataclass
class _Token:
    name: str
    is_probe: bool


class CircuitBreaker:
    def __init__(
        self,
        name: str,
        *,
        failure_threshold: float = 0.5,
        rolling_window_seconds: int = 60,
        min_throughput: int = 20,
        open_state_seconds: float = 60.0,
        half_open_max_in_flight: int = 10,
        success_quorum_percent: float = 0.8,
    ) -> None:
        self.name = name
        self.failure_threshold = failure_threshold
        self.rolling_window_seconds = rolling_window_seconds
        self.min_throughput = min_throughput
        self.open_state_seconds = open_state_seconds
        self.half_open_max_in_flight = half_open_max_in_flight
        self.success_quorum_percent = success_quorum_percent

        self._state = "CLOSED"
        self._opened_at: float | None = None
        self._lock = threading.Lock()
        self._events: Deque[Tuple[float, bool]] = deque()  # (timestamp, success)

        # Half-open tracking
        self._half_open_in_flight = 0
        self._half_open_total = 0
        self._half_open_success = 0

    # ---------------------- internal utils ----------------------
    def _now(self) -> float:
        return time.time()

    def _prune(self, now: float) -> None:
        cutoff = now - self.rolling_window_seconds
        while self._events and self._events[0][0] < cutoff:
            self._events.popleft()

    def _failure_rate_and_count(self, now: float) -> Tuple[float, int]:
        self._prune(now)
        total = len(self._events)
        if total == 0:
            return (0.0, 0)
        failures = sum(1 for _, ok in self._events if not ok)
        return (failures / total, total)

    def _open(self, now: float) -> None:
        self._state = "OPEN"
        self._opened_at = now
        # Reset half-open counters
        self._half_open_in_flight = 0
        self._half_open_total = 0
        self._half_open_success = 0

    def _to_half_open_if_ready(self, now: float) -> bool:
        if self._opened_at is None:
            return False
        if (now - self._opened_at) >= self.open_state_seconds:
            # move to HALF_OPEN (idempotent)
            self._state = "HALF_OPEN"
            return True
        return False

    def _maybe_trip_from_closed(self, now: float) -> None:
        rate, total = self._failure_rate_and_count(now)
        if total >= self.min_throughput and rate >= self.failure_threshold:
            self._open(now)

    # ---------------------- public API ----------------------
    @property
    def state(self) -> str:
        with self._lock:
            return self._state

    def before_call(self) -> _Token:
        """Check circuit state and return a token.

        Raises CircuitOpenError if circuit is OPEN and not yet ready for probes or
        half-open concurrency is saturated.
        """
        now = self._now()
        with self._lock:
            if self._state == "OPEN":
                if not self._to_half_open_if_ready(now):
                    raise CircuitOpenError(f"Circuit '{self.name}' is OPEN")
                # fallthrough to HALF_OPEN logic

            if self._state == "HALF_OPEN":
                if self._half_open_in_flight >= self.half_open_max_in_flight:
                    raise CircuitOpenError(
                        f"Circuit '{self.name}' is HALF_OPEN and saturated"
                    )
                self._half_open_in_flight += 1
                return _Token(self.name, is_probe=True)

            # CLOSED
            return _Token(self.name, is_probe=False)

    def after_call(self, token: _Token, success: bool) -> None:
        now = self._now()
        with self._lock:
            # Record outcome in rolling window (only count 5xx/network failures as
            # failures at caller)
            self._events.append((now, success))
            self._prune(now)

            if token.is_probe:
                # Update half-open counters
                self._half_open_total += 1
                if success:
                    self._half_open_success += 1
                # Release in-flight slot
                if self._half_open_in_flight > 0:
                    self._half_open_in_flight -= 1

                if not success:
                    # Immediate reopen
                    self._open(now)
                    return

                # Success path: if quorum reached, close
                if self._half_open_total >= max(1, self.half_open_max_in_flight):
                    success_ratio = self._half_open_success / max(
                        1, self._half_open_total
                    )
                    if success_ratio >= self.success_quorum_percent:
                        # close and reset counters
                        self._state = "CLOSED"
                        self._opened_at = None
                        self._half_open_in_flight = 0
                        self._half_open_total = 0
                        self._half_open_success = 0
                    else:
                        # Not enough success -> OPEN again
                        self._open(now)
                return

            # CLOSED state update: maybe trip (evaluate on every event)
            if self._state == "CLOSED":
                self._maybe_trip_from_closed(now)


# ---------------------- registry ----------------------
_registry_lock = threading.Lock()
_registry: Dict[str, CircuitBreaker] = {}


def get_circuit_breaker(
    name: str,
    **kwargs,
) -> CircuitBreaker:
    """Get or create a named circuit breaker instance."""
    with _registry_lock:
        br = _registry.get(name)
        if br is None:
            br = CircuitBreaker(name, **kwargs)
            _registry[name] = br
        return br
