"""FLEXT Meltano Production Decorators - Decorators consolidados para produção.

Decorators que eliminam código repetitivo e adicionam funcionalidades de produção
como retry, cache, métricas, validação e monitoramento.

Seguem padrões flext-core + SOLID + DRY + KISS.
"""

from __future__ import annotations

import asyncio
import functools
import time
from pathlib import Path
from typing import TYPE_CHECKING, Any, ParamSpec, TypeVar

from flext_meltano.helpers.execution import FlextMeltanoResult

if TYPE_CHECKING:
    from collections.abc import Awaitable, Callable

P = ParamSpec("P")
T = TypeVar("T")


def flext_meltano_auto_retry_smart(
    max_retries: int = 3,
    delay_seconds: float = 1.0,
    backoff_factor: float = 2.0,
    retry_on: tuple[type[Exception], ...] = (Exception,),
    retry_on_result_failure: bool = True,
) -> Callable[[Callable[P, Awaitable[FlextMeltanoResult]]], Callable[P, Awaitable[FlextMeltanoResult]]]:
    """Smart auto-retry decorator with exponential backoff.

    Elimina 20+ linhas de lógica de retry em cada função.

    Args:
        max_retries: Maximum retry attempts
        delay_seconds: Initial delay between retries
        backoff_factor: Exponential backoff multiplier
        retry_on: Exception types to retry on
        retry_on_result_failure: Whether to retry on FlextMeltanoResult.success = False

    Returns:
        Decorated function with smart retry logic

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

                    # Check if we should retry on result failure
                    if result.success:
                        if attempt > 0 and result.data:
                            # Add retry success metadata
                            result.data["retry_info"] = {
                                "attempts": attempt + 1,
                                "succeeded_on_retry": True,
                                "total_delay": sum(delay_seconds * (backoff_factor ** i) for i in range(attempt)),
                            }
                        return result

                    # Result failed - should we retry?
                    if retry_on_result_failure and attempt < max_retries:
                        last_exception = Exception(result.error or "Operation failed")
                    else:
                        # No more retries or not retrying on result failure
                        return result

                except Exception as e:
                    last_exception = e

                    # Check if this exception type should be retried
                    if not any(isinstance(e, exc_type) for exc_type in retry_on):
                        return FlextMeltanoResult.fail(f"Non-retryable error: {e}")

                    # No more retries available
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


def flext_meltano_smart_cache(
    ttl_seconds: int = 300,
    cache_key_func: Callable[..., str] | None = None,
    cache_failed_results: bool = False,
) -> Callable[[Callable[P, Awaitable[FlextMeltanoResult]]], Callable[P, Awaitable[FlextMeltanoResult]]]:
    """Smart caching decorator with TTL and custom key generation.

    Elimina descobertas repetitivas de catalog, plugins, etc.

    Args:
        ttl_seconds: Time-to-live for cached results
        cache_key_func: Custom cache key generation function
        cache_failed_results: Whether to cache failed results

    Returns:
        Decorated function with intelligent caching

    """
    cache: dict[str, tuple[FlextMeltanoResult, float]] = {}

    def default_cache_key(*args: Any, **kwargs: Any) -> str:
        """Generate default cache key from arguments."""
        # Create a stable hash from args and sorted kwargs
        args_str = str(args)
        kwargs_str = str(sorted(kwargs.items()))
        return f"{args_str}_{kwargs_str}"

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
                    # Return cached result with metadata
                    if result.data:
                        result.data["from_cache"] = True
                        result.data["cache_age_seconds"] = current_time - timestamp
                    return result
                # Cache expired, remove entry
                del cache[cache_key]

            # Execute function
            result = await func(*args, **kwargs)

            # Cache result if successful or if caching failed results
            if result.success or cache_failed_results:
                cache[cache_key] = (result, current_time)

            return result

        return wrapper
    return decorator


def flext_meltano_execution_metrics(
    include_performance: bool = True,
    include_memory: bool = False,
    include_detailed_timing: bool = True,
) -> Callable[[Callable[P, Awaitable[FlextMeltanoResult]]], Callable[P, Awaitable[FlextMeltanoResult]]]:
    """Production execution metrics decorator.

    Adiciona métricas de performance automaticamente.

    Args:
        include_performance: Include execution timing
        include_memory: Include memory usage (requires psutil)
        include_detailed_timing: Include detailed timing breakdown

    Returns:
        Decorated function with metrics collection

    """
    def decorator(
        func: Callable[P, Awaitable[FlextMeltanoResult]],
    ) -> Callable[P, Awaitable[FlextMeltanoResult]]:
        @functools.wraps(func)
        async def wrapper(*args: P.args, **kwargs: P.kwargs) -> FlextMeltanoResult:
            metrics = {
                "function_name": func.__name__,
                "start_timestamp": time.time(),
            }

            start_time = time.perf_counter()
            start_memory = 0

            if include_memory:
                try:
                    import psutil
                    process = psutil.Process()
                    start_memory = process.memory_info().rss
                except ImportError:
                    pass

            try:
                result = await func(*args, **kwargs)

                end_time = time.perf_counter()
                execution_time = end_time - start_time

                if include_performance:
                    metrics.update({
                        "execution_time_seconds": execution_time,
                        "end_timestamp": time.time(),
                        "success": result.success,
                    })

                if include_detailed_timing:
                    metrics.update({
                        "start_time_perf": start_time,
                        "end_time_perf": end_time,
                        "duration_perf": execution_time,
                    })

                if include_memory and start_memory > 0:
                    try:
                        import psutil
                        process = psutil.Process()
                        end_memory = process.memory_info().rss
                        metrics.update({
                            "memory_start_bytes": start_memory,
                            "memory_end_bytes": end_memory,
                            "memory_delta_bytes": end_memory - start_memory,
                        })
                    except ImportError:
                        pass

                # Add metrics to result
                if result.data:
                    result.data["execution_metrics"] = metrics

                return result

            except Exception as e:
                end_time = time.perf_counter()
                execution_time = end_time - start_time

                metrics.update({
                    "execution_time_seconds": execution_time,
                    "exception_type": type(e).__name__,
                    "exception_message": str(e),
                    "success": False,
                })

                return FlextMeltanoResult.fail(f"Function failed after {execution_time:.2f}s: {e}")

        return wrapper
    return decorator


def flext_meltano_project_validation(
    auto_validate: bool = True,
    require_meltano_yml: bool = True,
    require_venv: bool = False,
) -> Callable[[Callable[P, Awaitable[FlextMeltanoResult]]], Callable[P, Awaitable[FlextMeltanoResult]]]:
    """Project validation decorator.

    Elimina validação manual repetitiva de projeto em cada função.

    Args:
        auto_validate: Whether to automatically validate project
        require_meltano_yml: Require meltano.yml file
        require_venv: Require virtual environment

    Returns:
        Decorated function with project validation

    """
    def decorator(
        func: Callable[P, Awaitable[FlextMeltanoResult]],
    ) -> Callable[P, Awaitable[FlextMeltanoResult]]:
        @functools.wraps(func)
        async def wrapper(*args: P.args, **kwargs: P.kwargs) -> FlextMeltanoResult:
            if not auto_validate:
                return await func(*args, **kwargs)

            # Extract project_root from args/kwargs
            project_root = kwargs.get("project_root", ".")
            if not isinstance(project_root, Path):
                project_root = Path(project_root)

            # Validation checks
            if require_meltano_yml:
                meltano_yml = project_root / "meltano.yml"
                if not meltano_yml.exists():
                    return FlextMeltanoResult.fail(
                        f"Project validation failed: meltano.yml not found in {project_root}",
                    )

            if require_venv:
                venv_dirs = [
                    project_root / ".venv",
                    project_root / "venv",
                    project_root / ".meltano" / "run" / "bin",
                ]
                if not any(venv_dir.exists() for venv_dir in venv_dirs):
                    return FlextMeltanoResult.fail(
                        f"Project validation failed: No virtual environment found in {project_root}",
                    )

            return await func(*args, **kwargs)

        return wrapper
    return decorator


def flext_meltano_error_recovery(
    recovery_strategies: dict[type[Exception], Callable[..., FlextMeltanoResult]] | None = None,
    fallback_result: FlextMeltanoResult | None = None,
) -> Callable[[Callable[P, Awaitable[FlextMeltanoResult]]], Callable[P, Awaitable[FlextMeltanoResult]]]:
    """Smart error recovery decorator.

    Elimina blocos try-catch repetitivos com estratégias de recuperação.

    Args:
        recovery_strategies: Mapping of exception types to recovery functions
        fallback_result: Default result if all recovery fails

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
                                continue  # Try next strategy

                # Use fallback result if available
                if fallback_result:
                    return fallback_result

                # Default error handling
                return FlextMeltanoResult.fail(f"Operation failed with recovery: {e}")

        return wrapper
    return decorator


def flext_meltano_production_ready_complete(
    max_retries: int = 3,
    cache_ttl: int = 300,
    auto_validate: bool = True,
    include_metrics: bool = True,
    require_meltano_yml: bool = True,
) -> Callable[[Callable[P, Awaitable[FlextMeltanoResult]]], Callable[P, Awaitable[FlextMeltanoResult]]]:
    """Complete production-ready decorator stack.

    Combina retry, cache, métricas, validação em um único decorator.
    Elimina 100+ linhas de código de produção por função.

    Args:
        max_retries: Maximum retry attempts
        cache_ttl: Cache time-to-live seconds
        auto_validate: Auto-validate project
        include_metrics: Include execution metrics
        require_meltano_yml: Require meltano.yml file

    Returns:
        Decorated function with complete production features

    """
    def decorator(
        func: Callable[P, Awaitable[FlextMeltanoResult]],
    ) -> Callable[P, Awaitable[FlextMeltanoResult]]:
        # Apply decorators in optimal order (innermost first)
        decorated = func

        if include_metrics:
            decorated = flext_meltano_execution_metrics()(decorated)

        if cache_ttl > 0:
            decorated = flext_meltano_smart_cache(ttl_seconds=cache_ttl)(decorated)

        if auto_validate:
            decorated = flext_meltano_project_validation(
                auto_validate=auto_validate,
                require_meltano_yml=require_meltano_yml,
            )(decorated)

        if max_retries > 0:
            decorated = flext_meltano_auto_retry_smart(max_retries=max_retries)(decorated)

        return decorated

    return decorator


# Specialized decorators for common use cases
def flext_meltano_discovery_optimized(
    cache_ttl: int = 600,  # 10 minutes for discovery
    max_retries: int = 2,
) -> Callable[[Callable[P, Awaitable[FlextMeltanoResult]]], Callable[P, Awaitable[FlextMeltanoResult]]]:
    """Optimized decorator for discovery operations."""
    return flext_meltano_production_ready_complete(
        max_retries=max_retries,
        cache_ttl=cache_ttl,
        auto_validate=True,
        include_metrics=True,
    )


def flext_meltano_execution_optimized(
    max_retries: int = 3,
    include_detailed_metrics: bool = True,
) -> Callable[[Callable[P, Awaitable[FlextMeltanoResult]]], Callable[P, Awaitable[FlextMeltanoResult]]]:
    """Optimized decorator for execution operations."""
    def decorator(
        func: Callable[P, Awaitable[FlextMeltanoResult]],
    ) -> Callable[P, Awaitable[FlextMeltanoResult]]:
        decorated = func

        if include_detailed_metrics:
            decorated = flext_meltano_execution_metrics(
                include_performance=True,
                include_memory=True,
                include_detailed_timing=True,
            )(decorated)

        decorated = flext_meltano_project_validation(auto_validate=True)(decorated)
        return flext_meltano_auto_retry_smart(
            max_retries=max_retries,
            delay_seconds=2.0,
            backoff_factor=2.0,
        )(decorated)


    return decorator


def flext_meltano_validation_optimized(
    cache_ttl: int = 180,  # 3 minutes for validation
    auto_validate: bool = False,  # Validation functions don't need auto-validation
) -> Callable[[Callable[P, Awaitable[FlextMeltanoResult]]], Callable[P, Awaitable[FlextMeltanoResult]]]:
    """Optimized decorator for validation operations."""
    return flext_meltano_production_ready_complete(
        max_retries=1,  # Validation usually doesn't benefit from retries
        cache_ttl=cache_ttl,
        auto_validate=auto_validate,
        include_metrics=True,
    )
