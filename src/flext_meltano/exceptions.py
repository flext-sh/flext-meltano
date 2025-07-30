"""Meltano integration exception hierarchy using flext-core patterns.

Copyright (c) 2025 FLEXT Contributors
SPDX-License-Identifier: MIT

Domain-specific exceptions for Meltano operations inheriting from flext-core.
"""

from __future__ import annotations

from flext_core.exceptions import (
    FlextConfigurationError,
    FlextError,
    FlextProcessingError,
    FlextTimeoutError,
    FlextValidationError,
)


class FlextMeltanoError(FlextError):
    """Base exception for Meltano operations."""

    def __init__(
        self,
        message: str = "Meltano error",
        plugin_name: str | None = None,
        **kwargs: object,
    ) -> None:
        """Initialize Meltano error with context."""
        context = kwargs.copy()
        if plugin_name is not None:
            context["plugin_name"] = plugin_name

        super().__init__(message, error_code="MELTANO_ERROR", context=context)


class FlextMeltanoConfigurationError(FlextConfigurationError):
    """Meltano configuration errors."""

    def __init__(
        self,
        message: str = "Meltano configuration error",
        config_key: str | None = None,
        plugin_name: str | None = None,
        **kwargs: object,
    ) -> None:
        """Initialize Meltano configuration error with context."""
        context = kwargs.copy()
        if config_key is not None:
            context["config_key"] = config_key
        if plugin_name is not None:
            context["plugin_name"] = plugin_name

        super().__init__(f"Meltano config: {message}", **context)


class FlextMeltanoValidationError(FlextValidationError):
    """Meltano validation errors."""

    def __init__(
        self,
        message: str = "Meltano validation failed",
        field: str | None = None,
        value: object = None,
        plugin_name: str | None = None,
        **kwargs: object,
    ) -> None:
        """Initialize Meltano validation error with context."""
        validation_details = {}
        if field is not None:
            validation_details["field"] = field
        if value is not None:
            validation_details["value"] = str(value)[:100]  # Truncate long values

        context = kwargs.copy()
        if plugin_name is not None:
            context["plugin_name"] = plugin_name

        super().__init__(
            f"Meltano validation: {message}",
            validation_details=validation_details,
            context=context,
        )


class FlextMeltanoProcessingError(FlextProcessingError):
    """Meltano processing errors."""

    def __init__(
        self,
        message: str = "Meltano processing failed",
        plugin_name: str | None = None,
        stage: str | None = None,
        **kwargs: object,
    ) -> None:
        """Initialize Meltano processing error with context."""
        context = kwargs.copy()
        if plugin_name is not None:
            context["plugin_name"] = plugin_name
        if stage is not None:
            context["stage"] = stage

        super().__init__(f"Meltano processing: {message}", **context)


class FlextMeltanoTimeoutError(FlextTimeoutError):
    """Meltano timeout errors."""

    def __init__(
        self,
        message: str = "Meltano operation timed out",
        operation: str | None = None,
        timeout_seconds: float | None = None,
        **kwargs: object,
    ) -> None:
        """Initialize Meltano timeout error with context."""
        context = kwargs.copy()
        if operation is not None:
            context["operation"] = operation
        if timeout_seconds is not None:
            context["timeout_seconds"] = timeout_seconds

        super().__init__(f"Meltano timeout: {message}", **context)


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

        super().__init__(f"Meltano plugin: {message}", plugin_name=plugin_name, **context)


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

        super().__init__(f"Meltano execution: {message}", **context)


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

        super().__init__(f"Meltano Singer: {message}", **context)


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

        super().__init__(f"Meltano DBT: {message}", **context)


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
