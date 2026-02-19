"""
Circuit Breaker Pattern - Reliability Engineering Module
Protects distributed systems from cascading failures by managing 
state-based request routing (Closed, Open, Half-Open).
"""

import time
from enum import Enum
from typing import Callable, Any, Optional

class State(Enum):
    CLOSED = "CLOSED"       # Normal: Requests flow through
    OPEN = "OPEN"           # Tripped: Requests fail fast
    HALF_OPEN = "HALF_OPEN" # Testing: Limited requests allowed

class CircuitBreaker:
    """
    Acts as a protective proxy for service calls.
    Transitions states based on failure thresholds and recovery timeouts.
    """

    def __init__(
        self, 
        failure_threshold: int = 3, 
        recovery_timeout: float = 10.0,
        expected_exception: type = Exception
    ):
        self.state = State.CLOSED
        self.failure_threshold = failure_threshold
        self.recovery_timeout = recovery_timeout
        self.expected_exception = expected_exception
        
        # State tracking
        self.failure_count = 0
        self.last_failure_time: Optional[float] = None

    def call(self, func: Callable, *args, **kwargs) -> Any:
        """
        Wraps a function call in circuit breaker logic.
        
        Logic Flow:
        1. Check if the circuit should move from OPEN to HALF_OPEN.
        2. If OPEN, raise an exception immediately (Fail-Fast).
        3. Attempt the call.
        4. Track Success/Failure and transition state.
        """
        
        # 1. State Transition Check: OPEN -> HALF_OPEN
        if self.state == State.OPEN:
            if self.last_failure_time and (time.time() - self.last_failure_time > self.recovery_timeout):
                print("[TIMER] Recovery timeout reached. Transitioning to HALF-OPEN.")
                self.state = State.HALF_OPEN
            else:
                raise Exception(" [CIRCUIT OPEN] Request blocked to prevent cascading failure.")

        # 2. Execute the Call
        try:
            result = func(*args, **kwargs)
            self._handle_success()
            return result
        except self.expected_exception as e:
            self._handle_failure()
            raise e

    def _handle_success(self):
        """Resets the circuit upon successful communication."""
        if self.state == State.HALF_OPEN:
            print("[SUCCESS] Service recovered. Closing circuit.")
            self.state = State.CLOSED
        
        self.failure_count = 0
        self.last_failure_time = None

    def _handle_failure(self):
        """Increments failure count and trips the circuit if threshold met."""
        self.failure_count += 1
        self.last_failure_time = time.time()
        
        if self.state == State.HALF_OPEN or self.failure_count >= self.failure_threshold:
            if self.state != State.OPEN:
                print(f"[TRIPPED] {self.failure_count} failures detected. Opening circuit.")
                self.state = State.OPEN

    @property
    def current_status(self) -> str:
        return f"State: {self.state.value} | Failures: {self.failure_count}"