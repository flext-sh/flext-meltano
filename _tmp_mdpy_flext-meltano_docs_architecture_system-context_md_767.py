# from flext-meltano_docs/architecture/system-context.md:767
from __future__ import annotations


class CircuitBreakerIntegration:
    """Circuit breaker pattern for external system integration."""

    def __init__(self, failure_threshold: int = 5, recovery_timeout: int = 60):
        self.failure_threshold = failure_threshold
        self.recovery_timeout = recovery_timeout
        self.failure_count = 0
        self.last_failure_time = None
        self.state = CircuitState.CLOSED

    def execute_with_circuit_breaker(
        self, operation: Callable
    ) -> p.Result[t.JsonValue]:
        """Execute operation with circuit breaker protection."""
        if self.state == CircuitState.OPEN:
            if self._should_attempt_reset():
                self.state = CircuitState.HALF_OPEN
            else:
                return r.fail(CircuitBreakerError("Circuit breaker is OPEN"))

        try:
            result = operation()

            if self.state == CircuitState.HALF_OPEN:
                self._reset_circuit()

            return result

        except Exception as e:
            self._record_failure()
            return r.fail(IntegrationError(f"Operation failed: {e}"))

    def _record_failure(self) -> None:
        """Record operation failure and update circuit state."""
        self.failure_count += 1
        self.last_failure_time = datetime.utcnow()

        if self.failure_count >= self.failure_threshold:
            self.state = CircuitState.OPEN

    def _should_attempt_reset(self) -> bool:
        """Check if circuit should attempt to reset."""
        if self.last_failure_time is None:
            return True

        time_since_failure = (
            datetime.utcnow() - self.last_failure_time
        ).total_seconds()
        return time_since_failure >= self.recovery_timeout```
### Asynchronous Integration Patterns

#### Event-Driven Pattern

