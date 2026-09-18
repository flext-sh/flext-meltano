# from flext-meltano_docs/architecture/quality-attributes.md:1230
from __future__ import annotations


class CircuitBreaker:
    """Circuit breaker implementation for external service protection."""

    def __init__(
        self,
        failure_threshold: int = 5,
        recovery_timeout: int = 60,
        expected_exception: Type[Exception] = Exception,
    ):
        self.failure_threshold = failure_threshold
        self.recovery_timeout = recovery_timeout
        self.expected_exception = expected_exception

        self.failure_count = 0
        self.last_failure_time = None
        self.state = CircuitBreakerState.CLOSED

    def allow_request(self) -> bool:
        """Check if request should be allowed."""
        if self.state == CircuitBreakerState.CLOSED:
            return True

        if self.state == CircuitBreakerState.OPEN:
            if self._should_attempt_reset():
                self.state = CircuitBreakerState.HALF_OPEN
                return True
            return False

        if self.state == CircuitBreakerState.HALF_OPEN:
            # Allow request to test recovery
            return True

        return False

    def record_success(self) -> None:
        """Record successful operation."""
        if self.state == CircuitBreakerState.HALF_OPEN:
            # Successful test - close circuit
            self._reset_circuit()
        # For CLOSED state, no action needed

    def record_failure(self) -> None:
        """Record failed operation."""
        self.failure_count += 1
        self.last_failure_time = datetime.utcnow()

        if self.failure_count >= self.failure_threshold:
            self.state = CircuitBreakerState.OPEN

    def _should_attempt_reset(self) -> bool:
        """Check if circuit should attempt to reset."""
        if self.last_failure_time is None:
            return True

        time_since_failure = (
            datetime.utcnow() - self.last_failure_time
        ).total_seconds()
        return time_since_failure >= self.recovery_timeout

    def _reset_circuit(self) -> None:
        """Reset circuit breaker to closed state."""
        self.failure_count = 0
        self.last_failure_time = None
        self.state = CircuitBreakerState.CLOSED```
#### 3. Retry with Exponential Backoff

