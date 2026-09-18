# from flext-meltano/docs/architecture/quality-attributes.md:1300
from __future__ import annotations


class RetryExecutor:
    """Retry executor with exponential backoff and jitter."""

    def __init__(
        self,
        max_attempts: int = 3,
        base_delay: float = 1.0,
        max_delay: float = 60.0,
        backoff_factor: float = 2.0,
    ):
        self.max_attempts = max_attempts
        self.base_delay = base_delay
        self.max_delay = max_delay
        self.backoff_factor = backoff_factor

    def execute_with_retry(self, operation: Callable[[], T]) -> p.Result[T]:
        """Execute operation with retry logic."""
        last_exception = None

        for attempt in range(self.max_attempts):
            try:
                result = operation()
                return r.ok(result)

            except self.retryable_exceptions as e:
                last_exception = e

                if attempt < self.max_attempts - 1:  # Not the last attempt
                    delay = self._calculate_delay(attempt)
                    self.logger.warning(
                        f"Operation failed (attempt {attempt + 1}/{self.max_attempts}), "
                        f"retrying in {delay:.2f} seconds: {e}"
                    )
                    time.sleep(delay)
                else:
                    # Last attempt failed
                    self.logger.error(
                        f"Operation failed after {self.max_attempts} attempts: {e}"
                    )

            except Exception as e:
                # Non-retryable exception
                return r.fail(OperationError(f"Non-retryable error: {e}"))

        # All retry attempts exhausted
        return r.fail(
            RetryExhaustedError(
                f"Operation failed after {self.max_attempts} attempts. "
                f"Last error: {last_exception}"
            )
        )

    def _calculate_delay(self, attempt: int) -> float:
        """Calculate delay for retry attempt with jitter."""
        # Exponential backoff
        delay = self.base_delay * (self.backoff_factor**attempt)

        # Add jitter to prevent thundering herd
        jitter = random.uniform(0.5, 1.5)
        delay *= jitter

        # Cap at maximum delay
        delay = min(delay, self.max_delay)

        return delay

    @property
    def retryable_exceptions(self) -> Tuple[Type[Exception], ...]:
        """Exceptions that should be retried."""
        return (ConnectionError, TimeoutError, TemporaryServiceError, RateLimitError)```
### Reliability Monitoring

