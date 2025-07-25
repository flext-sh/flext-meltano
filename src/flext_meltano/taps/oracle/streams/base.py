"""Base stream class with enterprise features for Oracle data extraction.

This module provides a common base class for all Oracle streams with
enterprise-grade features like circuit breakers, metrics, and error handling.
"""

from __future__ import annotations

import logging
import time
from abc import abstractmethod
from typing import TYPE_CHECKING, Any

from flext_db_oracle.utils.exceptions import (
    FlextDbOracleConnectionError as OracleConnectionError,
    FlextDbOraclePerformanceError as OraclePerformanceError,
    FlextDbOracleQueryError as OracleQueryError,
)

from flext_meltano import Stream


def get_logger(name: str) -> logging.Logger:
    return logging.getLogger(name)




if TYPE_CHECKING:
    from collections.abc import Callable, Iterable


# Simple performance tracking decorator
def track_performance(
    name: Callable[..., Any] | str | None = None,
) -> Callable[..., Any]:
    """Simple performance tracking decorator."""

    def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
        return func

    if callable(name):
        # Used without parameters: @track_performance
        return name
    # Used with parameters: @track_performance("name")
    return decorator


logger = get_logger(__name__)


class BaseOracleStream(Stream):
    """Base class for Oracle streams with enterprise features.

    Provides common functionality for all Oracle data source streams:
    - Circuit breaker pattern for resilience
    - Performance monitoring and metrics
    - Enterprise error handling
    - Configurable timeouts and retries
    - Async support for high-performance operations
    """

    def __init__(self, *args: object, **kwargs: object) -> None:
        """Initialize the base Oracle stream."""
        super().__init__(*args, **kwargs)

        # Circuit breaker state
        self._circuit_breaker_failures = 0
        self._circuit_breaker_last_failure: float | None = None
        self._max_circuit_breaker_failures = 5
        self._circuit_breaker_timeout = 60  # seconds

        # Performance tracking
        self._records_processed = 0
        self._start_time: float | None = None
        self._last_record_time: float | None = None
        self._errors_count = 0

        # Stream-specific configuration (fallback to defaults if tap config
        # not available)
        if hasattr(self, "tap") and hasattr(self.tap, "config"):
            self._batch_size = getattr(self.tap.config, "batch_size", 10000)
            self._query_timeout = getattr(self.tap.config, "query_timeout", 300)
            self._enable_circuit_breaker = getattr(
                self.tap.config,
                "enable_circuit_breaker",
                True,
            )
            self._enable_metrics = getattr(self.tap.config, "enable_metrics", True)
        else:
            # Fallback defaults when tap config is not available
            self._batch_size = 10000
            self._query_timeout = 300
            self._enable_circuit_breaker = True
            self._enable_metrics = True

    @property
    def is_circuit_breaker_open(self) -> bool:
        """Check if circuit breaker is open (blocking requests).

        Returns:
            True if circuit breaker is open and blocking requests

        """
        if not self._enable_circuit_breaker:
            return False

        if self._circuit_breaker_failures < self._max_circuit_breaker_failures:
            return False

        if self._circuit_breaker_last_failure is None:
            return False

        # Check if timeout has passed
        elapsed = time.time() - self._circuit_breaker_last_failure
        return elapsed < self._circuit_breaker_timeout

    def _record_circuit_breaker_failure(self) -> None:
        """Record a circuit breaker failure."""
        if not self._enable_circuit_breaker:
            return

        self._circuit_breaker_failures += 1
        self._circuit_breaker_last_failure = time.time()
        self._errors_count += 1

        if self.is_circuit_breaker_open:
            logger.warning(
                "Circuit breaker opened for stream %s after %d failures",
                self.name,
                self._circuit_breaker_failures,
            )

    def _reset_circuit_breaker(self) -> None:
        """Reset circuit breaker state after successful operation."""
        if self._circuit_breaker_failures > 0:
            logger.info("Circuit breaker reset for stream %s", self.name)

        self._circuit_breaker_failures = 0
        self._circuit_breaker_last_failure = None

    def _check_circuit_breaker(self) -> None:
        """Check circuit breaker and raise exception if open.

        Raises:
            OracleConnectionError: If circuit breaker is open

        """
        if self.is_circuit_breaker_open:
            msg = (
                f"Circuit breaker is open for stream {self.name}. "
                f"Too many failures ({self._circuit_breaker_failures}). "
                f"Will retry after {self._circuit_breaker_timeout} seconds."
            )
            raise OracleConnectionError(msg)

    @track_performance("oracle_stream.get_records")
    def get_records(
        self,
        context: dict[str, Any] | None = None,
    ) -> Iterable[dict[str, Any]]:
        """Get records with enterprise error handling and monitoring.

        Args:
            context: Stream context

        Yields:
            Record dictionaries

        Raises:
            OracleConnectionError: If circuit breaker is open
            OraclePerformanceError: If performance thresholds are exceeded

        """
        self._check_circuit_breaker()

        self._start_time = time.time()
        self._records_processed = 0

        try:
            # Get records from the specific implementation
            for record in self._get_records_impl(context):
                self._records_processed += 1
                self._last_record_time = time.time()

                # Track performance
                if self._enable_metrics and self._records_processed % 10000 == 0:
                    self._log_performance_metrics()

                yield record

            # Reset circuit breaker on successful completion
            self._reset_circuit_breaker()
        except Exception as e:
            self._record_circuit_breaker_failure()

            # Enhance error with stream context
            if isinstance(e, (OracleConnectionError, OracleQueryError)):
                # Already a well-formed Oracle exception
                raise
            else:
                # Wrap other exceptions
                msg = f"Unexpected error in Oracle stream {self.name}: {e}"
                raise OracleQueryError(
                    msg,
                    sql=None,
                    oracle_code=None,
                ) from e
        finally:
            # Always log final metrics
            if self._enable_metrics:
                self._log_final_metrics()

    @abstractmethod
    def _get_records_impl(
        self,
        context: dict[str, Any] | None = None,
    ) -> Iterable[dict[str, Any]]:
        """Implementation-specific record retrieval.

        This method must be implemented by subclasses to provide
        the actual data retrieval logic.

        Args:
            context: Stream context

        Yields:
            Record dictionaries

        """
        raise NotImplementedError

    def _log_performance_metrics(self) -> None:
        """Log current performance metrics."""
        if not self._enable_metrics or not self._start_time:
            return

        elapsed = time.time() - self._start_time
        records_per_second = self._records_processed / elapsed if elapsed > 0 else 0

        logger.info(
            "Stream %s progress: %d records in %.2f seconds (%.2f records/sec)",
            self.name,
            self._records_processed,
            elapsed,
            records_per_second,
        )

    def _log_final_metrics(self) -> None:
        """Log final performance metrics."""
        if not self._enable_metrics or not self._start_time:
            return

        elapsed = time.time() - self._start_time
        records_per_second = self._records_processed / elapsed if elapsed > 0 else 0

        # Check for performance issues
        perf_threshold = 100
        min_records_for_check = 1000
        if (
            records_per_second < perf_threshold
            and self._records_processed > min_records_for_check
        ):
            logger.warning(
                "Slow performance detected for stream %s: %.2f records/sec",
                self.name,
                records_per_second,
            )

        logger.info(
            "Stream %s completed: %d records in %.2f seconds "
            "(%.2f records/sec, %d errors)",
            self.name,
            self._records_processed,
            elapsed,
            records_per_second,
            self._errors_count,
        )

    def get_stream_metrics(self) -> dict[str, Any]:
        """Get comprehensive stream metrics.

        Returns:
            Dictionary containing performance and operational metrics

        """
        if not self._enable_metrics:
            return {}

        elapsed = time.time() - self._start_time if self._start_time else 0
        records_per_second = self._records_processed / elapsed if elapsed > 0 else 0

        return {
            "stream_name": self.name,
            "records_processed": self._records_processed,
            "errors_count": self._errors_count,
            "elapsed_seconds": elapsed,
            "records_per_second": records_per_second,
            "circuit_breaker": {
                "enabled": self._enable_circuit_breaker,
                "failures": self._circuit_breaker_failures,
                "is_open": self.is_circuit_breaker_open,
                "last_failure": self._circuit_breaker_last_failure,
            },
            "configuration": {
                "batch_size": self._batch_size,
                "query_timeout": self._query_timeout,
            },
        }

    def validate_performance(self, threshold_records_per_second: float = 100.0) -> None:
        """Validate stream performance against thresholds.

        Args:
            threshold_records_per_second: Minimum acceptable records per second

        Raises:
            OraclePerformanceError: If performance is below threshold

        """
        if not self._enable_metrics or not self._start_time:
            return

        elapsed = time.time() - self._start_time
        records_per_second = self._records_processed / elapsed if elapsed > 0 else 0

        min_records_for_check = 1000
        min_elapsed_time = 10
        if (
            records_per_second < threshold_records_per_second
            and self._records_processed > min_records_for_check
            and elapsed > min_elapsed_time
        ):
            msg = (
                f"Stream performance below threshold: "
                f"{records_per_second:.2f} < {threshold_records_per_second} "
                f"records/sec"
            )
            raise OraclePerformanceError(
                msg,
                operation="stream_processing",
                duration=elapsed,
            )

    def reset_metrics(self) -> None:
        """Reset all stream metrics."""
        self._records_processed = 0
        self._start_time = None
        self._last_record_time = None
        self._errors_count = 0
        self._reset_circuit_breaker()

    async def sync_async(self) -> None:
        """Async version of stream synchronization for high performance.

        This provides an async interface for streams that support it,
        allowing for better performance in async environments.
        """
        # Default implementation falls back to synchronous sync
        # Subclasses can override for true async implementation
        return self.sync()

    def __repr__(self) -> str:
        """String representation of the stream."""
        return (
            f"{self.__class__.__name__}("
            f"name='{self.name}', "
            f"records_processed={self._records_processed}, "
            f"errors={self._errors_count}, "
            f"circuit_breaker_open={self.is_circuit_breaker_open}"
            f")"
        )
