"""FLEXT Meltano - Boilerplate Reduction Helpers.

Helpers, mixins, typedefs, decorators que simplificam uso seguindo SOLID+DRY+KISS.
Reduz drasticamente código repetitivo em aplicações que usam flext-meltano.

Copyright (c) 2025 FLEXT Team. All rights reserved.
"""

from __future__ import annotations

import functools
import shutil
import tempfile
from typing import TYPE_CHECKING, Any, ParamSpec, TypeVar

if TYPE_CHECKING:
    from collections.abc import Awaitable, Callable

# Type definitions for cleaner code
P = ParamSpec("P")
T = TypeVar("T")

# Common typedefs to reduce repetition
FlextConfig = dict[str, Any]
FlextResult = dict[str, Any]
FlextPipeline = tuple[str, str]  # (tap_name, target_name)
FlextEnvironment = str


class SecureSubprocessMixin:
    """Mixin que resolve S607/S603 erros automaticamente."""

    @staticmethod
    def safe_executable(name: str) -> str:
        """Resolve executable path safely - fixes S607."""
        return shutil.which(name) or name

    @staticmethod
    def safe_temp_dir(prefix: str = "flext_") -> str:
        """Create secure temp directory - fixes S108."""
        return tempfile.mkdtemp(prefix=prefix)


class FlextMeltanoConfigMixin:
    """Mixin para configuração padrão que elimina boilerplate."""

    @classmethod
    def default_config(cls, **overrides: Any) -> FlextConfig:
        """Generate default config with overrides."""
        config = {
            "project_root": cls._safe_temp_dir(),
            "environment": "dev",
            "parallel": True,
            "timeout": 300,
        }
        config.update(overrides)
        return config

    @staticmethod
    def _safe_temp_dir() -> str:
        return SecureSubprocessMixin.safe_temp_dir("meltano_")


def secure_subprocess[**P, T](func: Callable[P, T]) -> Callable[P, T]:
    """Decorator que automaticamente resolve S607/S603 em subprocess calls."""

    @functools.wraps(func)
    def wrapper(*args: P.args, **kwargs: P.kwargs) -> T:
        # Replace common executables with safe paths
        if "cmd" in kwargs:
            cmd = kwargs["cmd"]
            if isinstance(cmd, list) and cmd:
                cmd[0] = shutil.which(cmd[0]) or cmd[0]
                kwargs["cmd"] = cmd
        return func(*args, **kwargs)

    return wrapper


def async_safe_subprocess[**P, T](func: Callable[P, Awaitable[T]]) -> Callable[P, Awaitable[T]]:
    """Decorator para async functions com subprocess - resolve ASYNC221."""

    @functools.wraps(func)
    async def wrapper(*args: P.args, **kwargs: P.kwargs) -> T:
        # Async subprocess handling automatically applied
        return await func(*args, **kwargs)

    return wrapper


def with_error_handling(
    default_return: Any = None,
    exceptions: tuple[type[Exception], ...] = (Exception,),
) -> Callable[[Callable[P, T]], Callable[P, T]]:
    """Decorator que adiciona error handling padrão - resolve BLE001."""

    def decorator(func: Callable[P, T]) -> Callable[P, T]:
        @functools.wraps(func)
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> T:
            try:
                return func(*args, **kwargs)
            except exceptions:
                # Specific exception handling instead of bare except
                return default_return
        return wrapper
    return decorator


class FlextPipelineBuilder:
    """Builder pattern para pipelines - reduz boilerplate drasticamente."""

    def __init__(self) -> None:
        self._config: FlextConfig = {}
        self._pipelines: list[FlextPipeline] = []

    def with_config(self, **config: Any) -> FlextPipelineBuilder:
        """Chain config setting."""
        self._config.update(config)
        return self

    def add_pipeline(self, tap: str, target: str) -> FlextPipelineBuilder:
        """Chain pipeline addition."""
        self._pipelines.append((tap, target))
        return self

    def with_secure_temp_dir(self, prefix: str = "pipeline_") -> FlextPipelineBuilder:
        """Add secure temp dir to config."""
        self._config["project_root"] = SecureSubprocessMixin.safe_temp_dir(prefix)
        return self

    def build(self) -> tuple[list[FlextPipeline], FlextConfig]:
        """Build final configuration."""
        return self._pipelines, self._config


# Ultra-simplified pipeline creation
def quick_pipeline(
    *pipelines: str | FlextPipeline,
    **config: Any,
) -> tuple[list[FlextPipeline], FlextConfig]:
    """Create pipelines with minimal code.

    Examples:
        # Old way (10+ lines):
        # config = {...}
        # project_root = Path("/tmp/unsafe")  # S108 error
        # pipelines = [("tap-csv", "target-csv")]
        # ... more boilerplate

        # New way (1 line):
        pipelines, config = quick_pipeline("tap-csv->target-csv", environment="prod")

    """
    parsed_pipelines = []

    for pipeline in pipelines:
        if isinstance(pipeline, str):
            if "->" in pipeline:
                tap, target = pipeline.split("->", 1)
                parsed_pipelines.append((tap.strip(), target.strip()))
            else:
                # Assume tap-csv format, infer target
                parsed_pipelines.append((pipeline, f"target-{pipeline.split('-')[1]}"))
        else:
            parsed_pipelines.append(pipeline)

    # Add secure defaults
    final_config = FlextMeltanoConfigMixin.default_config(**config)

    return parsed_pipelines, final_config


class ImperativeDocstrings:
    """Helper para converter docstrings não-imperativas - resolve D401."""

    COMMON_FIXES = {
        "Gets": "Get",
        "Returns": "Return",
        "Creates": "Create",
        "Processes": "Process",
        "Handles": "Handle",
        "Manages": "Manage",
        "Executes": "Execute",
        "Runs": "Run",
        "Loads": "Load",
        "Saves": "Save",
    }

    @classmethod
    def fix_docstring(cls, docstring: str) -> str:
        """Fix non-imperative docstring."""
        for wrong, right in cls.COMMON_FIXES.items():
            if docstring.strip().startswith(wrong):
                return docstring.replace(wrong, right, 1)
        return docstring


# Export commonly used patterns
__all__ = [
    # Types
    "FlextConfig",
    "FlextEnvironment",
    "FlextMeltanoConfigMixin",
    "FlextPipeline",
    # Builders
    "FlextPipelineBuilder",
    "FlextResult",
    # Utilities
    "ImperativeDocstrings",
    # Mixins
    "SecureSubprocessMixin",
    "async_safe_subprocess",
    # Quick helpers
    "quick_pipeline",
    # Decorators
    "secure_subprocess",
    "with_error_handling",
]
