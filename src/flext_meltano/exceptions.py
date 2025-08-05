"""FLEXT Meltano Exceptions - Enterprise Error Handling.

**Architecture Layer**: Foundation Layer
**Status**: ✅ STABLE - Exception hierarchy and error handling patterns
**Dependencies**: flext-core (exception hierarchy), enterprise error patterns

## Module Purpose

This module provides **comprehensive exception hierarchy** for FLEXT Meltano's
bridge architecture, implementing domain-specific exceptions that extend
flext-core base classes for consistent error handling across the ecosystem.

## Design Principles

1. **Exception Hierarchy**: Domain-specific exceptions extending flext-core patterns
2. **Context-Rich Errors**: Detailed error context for debugging and troubleshooting
3. **Bridge-Friendly**: JSON-serializable exceptions for Go service integration
4. **Enterprise Patterns**: Structured error handling with correlation IDs
5. **Meltano-Specific**: Plugin, pipeline, and configuration-specific error types

## Core Components

### Base Exception Classes
- `FlextMeltanoError`: Base exception for all Meltano integration errors
- Plugin-specific error context and metadata
- Integration with flext-core exception hierarchy
- Bridge-compatible error serialization

### Domain-Specific Exceptions
- `FlextMeltanoPluginError`: Plugin-related errors
- `FlextMeltanoPipelineError`: Pipeline execution errors
- `FlextMeltanoConfigurationError`: Configuration validation errors
- `FlextMeltanoConnectionError`: Connection and networking errors

Copyright (c) 2025 FLEXT Contributors
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from flext_core.exceptions import (
    FlextAuthenticationError,
    FlextConfigurationError,
    FlextConnectionError,
    FlextError,
    FlextProcessingError,
    FlextTimeoutError,
    FlextValidationError,
)


class FlextMeltanoError(FlextError):
    """Base exception for all Meltano integration errors."""

    def __init__(
        self,
        message: str = "Meltano error",
        plugin_name: str | None = None,
        context: dict[str, object] | None = None,
        **kwargs: object,
    ) -> None:
        """Initialize Meltano error with context."""
        error_context = dict(context) if context else {}
        error_context.update(kwargs)
        if plugin_name is not None:
            error_context["plugin_name"] = plugin_name
        super().__init__(f"Meltano: {message}", context=error_context)


class FlextMeltanoValidationError(FlextValidationError):
    """Meltano validation errors."""

    def __init__(
        self,
        message: str = "Validation error",
        plugin_name: str | None = None,
        **kwargs: object,
    ) -> None:
        """Initialize Meltano validation error with context."""
        context = dict(kwargs)
        if plugin_name is not None:
            context["plugin_name"] = plugin_name
        super().__init__(f"Meltano validation: {message}", context=context)


class FlextMeltanoConfigurationError(FlextConfigurationError):
    """Meltano configuration errors."""

    def __init__(
        self,
        message: str = "Configuration error",
        plugin_name: str | None = None,
        **kwargs: object,
    ) -> None:
        """Initialize Meltano configuration error with context."""
        context = dict(kwargs)
        if plugin_name is not None:
            context["plugin_name"] = plugin_name
        super().__init__(f"Meltano config: {message}", context=context)


class FlextMeltanoConnectionError(FlextConnectionError):
    """Meltano connection errors."""

    def __init__(
        self,
        message: str = "Connection error",
        plugin_name: str | None = None,
        **kwargs: object,
    ) -> None:
        """Initialize Meltano connection error with context."""
        context = dict(kwargs)
        if plugin_name is not None:
            context["plugin_name"] = plugin_name
        super().__init__(f"Meltano connection: {message}", context=context)


class FlextMeltanoProcessingError(FlextProcessingError):
    """Meltano processing errors."""

    def __init__(
        self,
        message: str = "Processing error",
        plugin_name: str | None = None,
        **kwargs: object,
    ) -> None:
        """Initialize Meltano processing error with context."""
        context = dict(kwargs)
        if plugin_name is not None:
            context["plugin_name"] = plugin_name
        super().__init__(f"Meltano processing: {message}", context=context)


class FlextMeltanoAuthenticationError(FlextAuthenticationError):
    """Meltano authentication errors."""

    def __init__(
        self,
        message: str = "Authentication error",
        plugin_name: str | None = None,
        **kwargs: object,
    ) -> None:
        """Initialize Meltano authentication error with context."""
        context = dict(kwargs)
        if plugin_name is not None:
            context["plugin_name"] = plugin_name
        super().__init__(f"Meltano auth: {message}", context=context)


class FlextMeltanoTimeoutError(FlextTimeoutError):
    """Meltano timeout errors."""

    def __init__(
        self,
        message: str = "Timeout error",
        plugin_name: str | None = None,
        **kwargs: object,
    ) -> None:
        """Initialize Meltano timeout error with context."""
        context = dict(kwargs)
        if plugin_name is not None:
            context["plugin_name"] = plugin_name
        super().__init__(f"Meltano timeout: {message}", context=context)


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
        context = dict(kwargs)
        if plugin_type is not None:
            context["plugin_type"] = plugin_type

        super().__init__(
            f"Plugin: {message}",
            plugin_name=plugin_name,
            context=context,
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
        context = dict(kwargs)
        if command is not None:
            context["command"] = command
        if exit_code is not None:
            context["exit_code"] = exit_code

        super().__init__(f"Execution: {message}", plugin_name=None, context=context)


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
        context = dict(kwargs)
        if tap_name is not None:
            context["tap_name"] = tap_name
        if target_name is not None:
            context["target_name"] = target_name

        super().__init__(f"Singer: {message}", plugin_name=None, context=context)


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
        context = dict(kwargs)
        if project_name is not None:
            context["project_name"] = project_name
        if model_name is not None:
            context["model_name"] = model_name

        super().__init__(f"DBT: {message}", plugin_name=None, context=context)


__all__: list[str] = [
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
