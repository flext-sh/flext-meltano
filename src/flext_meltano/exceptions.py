"""Meltano integration exception hierarchy using flext-core DRY patterns.

Copyright (c) 2025 FLEXT Contributors
SPDX-License-Identifier: MIT

Domain-specific exceptions using factory pattern to eliminate 150+ lines of duplication.
"""

from __future__ import annotations

from flext_core.exceptions import (
    create_module_exception_classes,
)

# Create all standard exception classes using factory pattern - eliminates duplication
meltano_exceptions = create_module_exception_classes("flext_meltano")

# Import generated classes for clean usage
FlextMeltanoError = meltano_exceptions["FlextMeltanoError"]
FlextMeltanoValidationError = meltano_exceptions["FlextMeltanoValidationError"]
FlextMeltanoConfigurationError = meltano_exceptions["FlextMeltanoConfigurationError"]
FlextMeltanoConnectionError = meltano_exceptions["FlextMeltanoConnectionError"]
FlextMeltanoProcessingError = meltano_exceptions["FlextMeltanoProcessingError"]
FlextMeltanoAuthenticationError = meltano_exceptions["FlextMeltanoAuthenticationError"]
FlextMeltanoTimeoutError = meltano_exceptions["FlextMeltanoTimeoutError"]


class FlextMeltanoPluginError(FlextMeltanoError):
    """Meltano plugin-specific errors."""

    def __init__(
        self,
        message: str = "Meltano plugin error",
        plugin_name: str | None = None,
        plugin_type: str | None = None,
        **kwargs: object,
    ) -> None:
        """Initialize Meltano plugin error with context."""
        context = kwargs.copy()
        if plugin_type is not None:
            context["plugin_type"] = plugin_type

        super().__init__(
            f"Meltano plugin: {message}",
            plugin_name=plugin_name,
            **context,
        )


class FlextMeltanoExecutionError(FlextMeltanoError):
    """Meltano execution errors."""

    def __init__(
        self,
        message: str = "Meltano execution failed",
        command: str | None = None,
        exit_code: int | None = None,
        **kwargs: object,
    ) -> None:
        """Initialize Meltano execution error with context."""
        context = kwargs.copy()
        if command is not None:
            context["command"] = command
        if exit_code is not None:
            context["exit_code"] = exit_code

        super().__init__(f"Meltano execution: {message}", plugin_name=None, **context)


class FlextMeltanoSingerError(FlextMeltanoError):
    """Meltano Singer-specific errors."""

    def __init__(
        self,
        message: str = "Meltano Singer error",
        tap_name: str | None = None,
        target_name: str | None = None,
        **kwargs: object,
    ) -> None:
        """Initialize Meltano Singer error with context."""
        context = kwargs.copy()
        if tap_name is not None:
            context["tap_name"] = tap_name
        if target_name is not None:
            context["target_name"] = target_name

        super().__init__(f"Meltano Singer: {message}", plugin_name=None, **context)


class FlextMeltanoDBTError(FlextMeltanoError):
    """Meltano DBT-specific errors."""

    def __init__(
        self,
        message: str = "Meltano DBT error",
        project_name: str | None = None,
        model_name: str | None = None,
        **kwargs: object,
    ) -> None:
        """Initialize Meltano DBT error with context."""
        context = kwargs.copy()
        if project_name is not None:
            context["project_name"] = project_name
        if model_name is not None:
            context["model_name"] = model_name

        super().__init__(f"Meltano DBT: {message}", plugin_name=None, **context)


__all__ = [
    "FlextMeltanoConfigurationError",
    "FlextMeltanoDBTError",
    "FlextMeltanoError",
    "FlextMeltanoExecutionError",
    "FlextMeltanoPluginError",
    "FlextMeltanoProcessingError",
    "FlextMeltanoSingerError",
    "FlextMeltanoTimeoutError",
    "FlextMeltanoValidationError",
]
