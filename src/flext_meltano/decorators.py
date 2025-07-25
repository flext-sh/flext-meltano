"""FLEXT Meltano advanced decorators for maximum code reduction.

Specialized decorators that eliminate repetitive patterns and error handling.
"""

from __future__ import annotations

import asyncio
import functools
import time
from pathlib import Path
from typing import TYPE_CHECKING, ParamSpec, TypeVar

from flext_meltano.helpers.execution import FlextMeltanoResult

if TYPE_CHECKING:
    from collections.abc import Awaitable, Callable

P = ParamSpec("P")
T = TypeVar("T")


def flext_meltano_timing(
    include_stats: bool = True,
) -> Callable[[Callable[P, Awaitable[FlextMeltanoResult]]], Callable[P, Awaitable[FlextMeltanoResult]]]:
    """Decorator for automatic execution timing.

    Eliminates manual timing code in every function.

    Args:
        include_stats: Whether to include timing statistics in result

    Returns:
        Decorated function with timing capabilities

    """
    def decorator(
        func: Callable[P, Awaitable[FlextMeltanoResult]],
    ) -> Callable[P, Awaitable[FlextMeltanoResult]]:
        @functools.wraps(func)
        async def wrapper(*args: P.args, **kwargs: P.kwargs) -> FlextMeltanoResult:
            start_time = time.perf_counter()

            try:
                result = await func(*args, **kwargs)
                end_time = time.perf_counter()
                execution_time = end_time - start_time

                if include_stats and result.success and result.data:
                    # Add timing stats to successful results
                    result.data["execution_time_seconds"] = execution_time
                    result.data["timing_info"] = {
                        "start_time": start_time,
                        "end_time": end_time,
                        "duration": execution_time,
                    }

                return result

            except Exception as e:
                end_time = time.perf_counter()
                execution_time = end_time - start_time
                return FlextMeltanoResult.fail(
                    f"Function failed after {execution_time:.2f}s: {e}",
                )

        return wrapper
    return decorator


def flext_meltano_cache_result(
    cache_key_func: Callable[..., str] | None = None,
    ttl_seconds: int = 300,  # 5 minutes default
) -> Callable[[Callable[P, Awaitable[FlextMeltanoResult]]], Callable[P, Awaitable[FlextMeltanoResult]]]:
    """Decorator for result caching to avoid repeated operations.

    Eliminates repetitive catalog discovery and validation calls.

    Args:
        cache_key_func: Function to generate cache key from args
        ttl_seconds: Time-to-live for cached results

    Returns:
        Decorated function with caching

    """
    cache: dict[str, tuple[FlextMeltanoResult, float]] = {}

    def default_cache_key(*args: object, **kwargs: object) -> str:
        """Generate default cache key from arguments."""
        return f"{args}_{sorted(kwargs.items())}"

    def decorator(
        func: Callable[P, Awaitable[FlextMeltanoResult]],
    ) -> Callable[P, Awaitable[FlextMeltanoResult]]:
        @functools.wraps(func)
        async def wrapper(*args: P.args, **kwargs: P.kwargs) -> FlextMeltanoResult:
            # Generate cache key
            key_func = cache_key_func or default_cache_key
            cache_key = key_func(*args, **kwargs)

            # Check cache
            current_time = time.time()
            if cache_key in cache:
                result, timestamp = cache[cache_key]
                if current_time - timestamp < ttl_seconds:
                    # Return cached result
                    if result.data:
                        result.data["from_cache"] = True
                        result.data["cache_age_seconds"] = current_time - timestamp
                    return result

            # Execute function and cache result
            result = await func(*args, **kwargs)
            if result.success:
                cache[cache_key] = (result, current_time)

            return result

        return wrapper
    return decorator


def flext_meltano_project_context(
    auto_validate: bool = True,
) -> Callable[[Callable[P, Awaitable[FlextMeltanoResult]]], Callable[P, Awaitable[FlextMeltanoResult]]]:
    """Decorator for automatic project context setup.

    Eliminates project validation boilerplate in every function.

    Args:
        auto_validate: Whether to automatically validate project before execution

    Returns:
        Decorated function with project context

    """
    def decorator(
        func: Callable[P, Awaitable[FlextMeltanoResult]],
    ) -> Callable[P, Awaitable[FlextMeltanoResult]]:
        @functools.wraps(func)
        async def wrapper(*args: P.args, **kwargs: P.kwargs) -> FlextMeltanoResult:
            if auto_validate:
                # Extract project_root from args/kwargs
                project_root = kwargs.get("project_root", ".")
                if not isinstance(project_root, Path):
                    project_root = Path(project_root)

                # Validate project structure
                if not (project_root / "meltano.yml").exists():
                    return FlextMeltanoResult.fail(
                        f"Invalid Meltano project: meltano.yml not found in {project_root}",
                    )

            return await func(*args, **kwargs)

        return wrapper
    return decorator


def flext_meltano_error_recovery(
    recovery_strategies: dict[type[Exception], Callable[..., FlextMeltanoResult]] | None = None,
) -> Callable[[Callable[P, Awaitable[FlextMeltanoResult]]], Callable[P, Awaitable[FlextMeltanoResult]]]:
    """Decorator for intelligent error recovery.

    Eliminates repetitive try-catch blocks with smart recovery.

    Args:
        recovery_strategies: Mapping of exception types to recovery functions

    Returns:
        Decorated function with error recovery

    """
    def decorator(
        func: Callable[P, Awaitable[FlextMeltanoResult]],
    ) -> Callable[P, Awaitable[FlextMeltanoResult]]:
        @functools.wraps(func)
        async def wrapper(*args: P.args, **kwargs: P.kwargs) -> FlextMeltanoResult:
            try:
                return await func(*args, **kwargs)

            except Exception as e:
                # Try recovery strategies
                if recovery_strategies:
                    for exc_type, recovery_func in recovery_strategies.items():
                        if isinstance(e, exc_type):
                            try:
                                return recovery_func(*args, **kwargs)
                            except Exception:
                                pass  # Recovery failed, continue to default handling

                # Default error handling
                return FlextMeltanoResult.fail(f"Operation failed: {e}")

        return wrapper
    return decorator


def flext_meltano_batch_operation(
    batch_size: int = 10,
    parallel: bool = True,
) -> Callable[[Callable[P, Awaitable[FlextMeltanoResult]]], Callable[P, Awaitable[FlextMeltanoResult]]]:
    """Decorator for automatic batch processing.

    Eliminates manual batching logic for bulk operations.

    Args:
        batch_size: Size of each batch
        parallel: Whether to process batches in parallel

    Returns:
        Decorated function with batch processing

    """
    def decorator(
        func: Callable[P, Awaitable[FlextMeltanoResult]],
    ) -> Callable[P, Awaitable[FlextMeltanoResult]]:
        @functools.wraps(func)
        async def wrapper(*args: P.args, **kwargs: P.kwargs) -> FlextMeltanoResult:
            # Check if args contain a list/iterable to batch
            items = None
            items_key = None

            # Look for common batch parameter names
            for key in ["items", "files", "configs", "streams"]:
                if key in kwargs and isinstance(kwargs[key], (list, tuple)):
                    items = kwargs[key]
                    items_key = key
                    break

            if not items or len(items) <= batch_size:
                # No batching needed
                return await func(*args, **kwargs)

            # Process in batches
            results = []
            errors = []

            for i in range(0, len(items), batch_size):
                batch = items[i:i + batch_size]
                batch_kwargs = {**kwargs, items_key: batch}

                try:
                    if parallel and len([items[i:i + batch_size] for i in range(0, len(items), batch_size)]) > 1:
                        # Process multiple batches in parallel
                        tasks = []
                        for j in range(i, min(i + batch_size * 5, len(items)), batch_size):  # Max 5 parallel batches
                            batch_subset = items[j:j + batch_size]
                            batch_kwargs_subset = {**kwargs, items_key: batch_subset}
                            task = func(*args, **batch_kwargs_subset)
                            tasks.append(task)

                        batch_results = await asyncio.gather(*tasks, return_exceptions=True)
                        for result in batch_results:
                            if isinstance(result, Exception):
                                errors.append(str(result))
                            elif result.success:
                                results.append(result.data)
                            else:
                                errors.append(result.error)
                    else:
                        # Sequential processing
                        result = await func(*args, **batch_kwargs)
                        if result.success:
                            results.append(result.data)
                        else:
                            errors.append(result.error)

                except Exception as e:
                    errors.append(str(e))

            # Aggregate results
            if errors and not results:
                return FlextMeltanoResult.fail(f"All batches failed: {'; '.join(errors)}")

            return FlextMeltanoResult.ok({
                "batch_results": results,
                "batch_errors": errors,
                "total_batches": len(results) + len(errors),
                "success_count": len(results),
                "error_count": len(errors),
            })

        return wrapper
    return decorator


def flext_meltano_metrics_collection(
    collect_performance: bool = True,
    collect_usage: bool = True,
) -> Callable[[Callable[P, Awaitable[FlextMeltanoResult]]], Callable[P, Awaitable[FlextMeltanoResult]]]:
    """Decorator for automatic metrics collection.

    Eliminates manual metrics tracking in every operation.

    Args:
        collect_performance: Whether to collect performance metrics
        collect_usage: Whether to collect usage metrics

    Returns:
        Decorated function with metrics collection

    """
    def decorator(
        func: Callable[P, Awaitable[FlextMeltanoResult]],
    ) -> Callable[P, Awaitable[FlextMeltanoResult]]:
        @functools.wraps(func)
        async def wrapper(*args: P.args, **kwargs: P.kwargs) -> FlextMeltanoResult:
            metrics = {"function_name": func.__name__}

            if collect_performance:
                start_time = time.perf_counter()

            try:
                result = await func(*args, **kwargs)

                if collect_performance:
                    end_time = time.perf_counter()
                    metrics["execution_time"] = end_time - start_time
                    metrics["memory_delta"] = 0  # Placeholder for memory tracking

                if collect_usage:
                    metrics["success"] = result.success
                    metrics["args_count"] = len(args)
                    metrics["kwargs_count"] = len(kwargs)

                # Add metrics to result
                if result.data:
                    result.data["metrics"] = metrics

                return result

            except Exception as e:
                if collect_performance:
                    end_time = time.perf_counter()
                    metrics["execution_time"] = end_time - start_time

                metrics["exception"] = type(e).__name__
                metrics["success"] = False

                return FlextMeltanoResult.fail(f"Function failed: {e}")

        return wrapper
    return decorator


# Convenience decorator combinations

def flext_meltano_production_ready(
    max_retries: int = 3,
    cache_ttl: int = 300,
    auto_validate: bool = True,
) -> Callable[[Callable[P, Awaitable[FlextMeltanoResult]]], Callable[P, Awaitable[FlextMeltanoResult]]]:
    """Combined decorator for production-ready functions.

    Includes retry, caching, timing, project validation, and metrics.
    Eliminates 50+ lines of production boilerplate per function.

    Args:
        max_retries: Maximum retry attempts
        cache_ttl: Cache time-to-live in seconds
        auto_validate: Whether to auto-validate projects

    Returns:
        Decorated function with full production features

    """
    def decorator(func: Callable[P, Awaitable[FlextMeltanoResult]]) -> Callable[P, Awaitable[FlextMeltanoResult]]:
        # Apply decorators in order (innermost first)
        decorated = func
        decorated = flext_meltano_metrics_collection()(decorated)
        decorated = flext_meltano_timing()(decorated)
        decorated = flext_meltano_cache_result(ttl_seconds=cache_ttl)(decorated)
        decorated = flext_meltano_project_context(auto_validate=auto_validate)(decorated)
        return flext_meltano_auto_retry(max_retries=max_retries)(decorated)

    return decorator


def flext_meltano_auto_retry(
    max_retries: int = 3,
    delay_seconds: float = 1.0,
    backoff_factor: float = 2.0,
    retry_on: tuple[type[Exception], ...] = (Exception,),
) -> Callable[[Callable[P, Awaitable[FlextMeltanoResult]]], Callable[P, Awaitable[FlextMeltanoResult]]]:
    """Decorator for automatic retry with exponential backoff.

    Eliminates repetitive retry logic for unreliable operations.

    Args:
        max_retries: Maximum number of retry attempts
        delay_seconds: Initial delay between retries
        backoff_factor: Multiplier for delay after each retry
        retry_on: Tuple of exception types to retry on

    Returns:
        Decorated function with retry capabilities

    """
    def decorator(
        func: Callable[P, Awaitable[FlextMeltanoResult]],
    ) -> Callable[P, Awaitable[FlextMeltanoResult]]:
        @functools.wraps(func)
        async def wrapper(*args: P.args, **kwargs: P.kwargs) -> FlextMeltanoResult:
            last_exception = None
            delay = delay_seconds

            for attempt in range(max_retries + 1):
                try:
                    result = await func(*args, **kwargs)

                    # If result is successful, return immediately
                    if result.success:
                        if attempt > 0 and result.data:
                            # Add retry information to successful result
                            result.data["retry_info"] = {
                                "attempts": attempt + 1,
                                "succeeded_on_retry": attempt > 0,
                                "total_delay": sum(delay_seconds * (backoff_factor ** i) for i in range(attempt)),
                            }
                        return result

                    # If result failed and we have retries left, prepare for retry
                    if attempt < max_retries:
                        last_exception = Exception(result.error or "Operation failed")
                    else:
                        # No more retries, return the failed result
                        return result

                except Exception as e:
                    last_exception = e

                    # Check if this exception type should be retried
                    if not any(isinstance(e, exc_type) for exc_type in retry_on):
                        return FlextMeltanoResult.fail(f"Non-retryable error: {e}")

                    # If no more retries, fail
                    if attempt >= max_retries:
                        break

                # Wait before retry (except on last attempt)
                if attempt < max_retries:
                    await asyncio.sleep(delay)
                    delay *= backoff_factor

            # All retries exhausted
            return FlextMeltanoResult.fail(
                f"Operation failed after {max_retries + 1} attempts. Last error: {last_exception}",
            )

        return wrapper
    return decorator


def flext_meltano_validate_config(
    required_fields: list[str] | None = None,
    validate_plugins: bool = True,
) -> Callable[[Callable[P, Awaitable[FlextMeltanoResult]]], Callable[P, Awaitable[FlextMeltanoResult]]]:
    """Decorator for automatic configuration validation.

    Eliminates repetitive config validation logic.

    Args:
        required_fields: List of required configuration fields
        validate_plugins: Whether to validate plugin configurations

    Returns:
        Decorated function with config validation

    """
    def decorator(
        func: Callable[P, Awaitable[FlextMeltanoResult]],
    ) -> Callable[P, Awaitable[FlextMeltanoResult]]:
        @functools.wraps(func)
        async def wrapper(*args: P.args, **kwargs: P.kwargs) -> FlextMeltanoResult:
            # Validate required fields
            if required_fields:
                for field in required_fields:
                    if field not in kwargs or kwargs[field] is None:
                        return FlextMeltanoResult.fail(f"Required configuration field missing: {field}")

            # Validate plugin configs if requested
            if validate_plugins:
                config = kwargs.get("config", {})
                if not isinstance(config, dict):
                    return FlextMeltanoResult.fail("Configuration must be a dictionary")

            return await func(*args, **kwargs)

        return wrapper
    return decorator
