"""FLEXT Meltano Exceptions - Single Class Architecture (Flext[Area][Module] pattern).

**Architecture Compliance**: Single main class FlextMeltanoExceptions following Flext[Area][Module] pattern
**Hierarchical Inheritance**: Inherits from flext-core exception hierarchies
**SOLID Principles**: Single Responsibility - All Meltano exceptions organized under one class
**ZERO Duplication**: Uses internal classes with aliases, delegates to base implementations

Domain-specific exceptions using facade pattern to eliminate duplication while maintaining compatibility.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from flext_core import (
    FlextExceptions,
)

# =============================================================================
# MAIN EXCEPTIONS CLASS - Following Flext[Area][Module] pattern
# =============================================================================


class FlextMeltanoExceptions:
    """Single main exceptions class for all Meltano errors (Flext[Area][Module] pattern).

    Architectural Compliance:
    - All Meltano exceptions organized under single class
    - Nested classes implement specific error types
    - Aliases for backward compatibility
    - Hierarchical inheritance from flext-core

    SOLID Principles:
    - Single Responsibility: All Meltano error handling in one place
    - Open/Closed: Extensible through inheritance
    - Dependency Inversion: Depends on flext-core abstractions
    """

    # =================================================================
    # NESTED EXCEPTION CLASSES - Actual implementations
    # =================================================================

    class MeltanoError(FlextExceptions):
        """Base Meltano error inheriting from flext-core generic error."""

    class MeltanoValidationError(MeltanoError, FlextExceptions):
        """Validation error for Meltano domain inheriting from Meltano base and core validation error."""

        def __init__(self, message: str = "Validation error", **kwargs: object) -> None:
            """Allow arbitrary context kwargs and forward to base class."""
            context = dict(kwargs) if kwargs else None
            super().__init__(message, context=context)

    class MeltanoConfigurationError(MeltanoError, FlextExceptions):
        """Configuration error for Meltano domain."""

        def __init__(
            self,
            message: str = "Configuration error",
            *,
            config_file: str | None = None,
            section: str | None = None,
            **kwargs: object,
        ) -> None:
            """Initialize configuration error with nested context expected by tests."""
            super().__init__(f"Configuration: {message}", context={})
            nested: dict[str, object] = dict(kwargs)
            if config_file is not None:
                nested["config_file"] = config_file
            if section is not None:
                nested["section"] = section
            self.context = {"context": nested}

    class MeltanoConnectionError(MeltanoError):
        """Connection error for Meltano domain."""

        def __init__(
            self,
            message: str = "Connection error",
            *,
            host: str | None = None,
            port: int | None = None,
            **kwargs: object,
        ) -> None:
            """Initialize connection error with network context."""
            nested: dict[str, object] = {}
            if host is not None:
                nested["host"] = host
            if port is not None:
                nested["port"] = port
            super().__init__(f"Connection: {message}", context={})
            if kwargs:
                nested.update(dict(kwargs))
            self.context = {"context": nested}

    class MeltanoProcessingError(MeltanoError):
        """Processing error for Meltano domain."""

        def __init__(
            self,
            message: str = "Processing error",
            *,
            operation: str | None = None,
            records_processed: int | None = None,
            context: dict[str, object] | None = None,
            **kwargs: object,
        ) -> None:
            """Initialize processing error with operation context."""
            super().__init__(f"Processing: {message}", context={})
            nested_context: dict[str, object] = dict(context or {})
            if kwargs:
                nested_context.update(dict(kwargs))
            if operation is not None:
                nested_context["operation"] = operation
            if records_processed is not None:
                nested_context["records_processed"] = records_processed
            self.context = {"context": nested_context}

    class MeltanoAuthenticationError(MeltanoError):
        """Authentication error for Meltano domain."""

        def __init__(
            self,
            message: str = "Authentication error",
            *,
            username: str | None = None,
            auth_type: str | None = None,
            **kwargs: object,
        ) -> None:
            """Initialize authentication error with auth context."""
            super().__init__(f"Authentication: {message}", context={})
            nested = dict(kwargs)
            if username is not None:
                nested["user"] = username
            if auth_type is not None:
                nested["method"] = auth_type
            self.context = {"context": nested}

    class MeltanoTimeoutError(MeltanoError):
        """Timeout error for Meltano domain."""

        def __init__(
            self,
            message: str = "Timeout error",
            *,
            timeout_seconds: int | None = None,
            operation: str | None = None,
            **kwargs: object,
        ) -> None:
            """Initialize timeout error with timing context nested under 'context'."""
            super().__init__(f"Timeout: {message}", context={})
            nested: dict[str, object] = {}
            if timeout_seconds is not None:
                nested["timeout"] = timeout_seconds
            if operation is not None:
                nested["operation"] = operation
            if kwargs:
                nested.update(dict(kwargs))
            self.context = {"context": nested}

    class MeltanoPluginError(MeltanoError):
        """Plugin-specific errors with enhanced context using DRY foundation."""

        def __init__(
            self,
            message: str = "Plugin error",
            *,
            plugin_name: str | None = None,
            plugin_type: str | None = None,
            plugin_command: str | None = None,
            **kwargs: object,
        ) -> None:
            """Initialize plugin error with rich context."""
            context = dict(kwargs)
            if plugin_name is not None:
                context["plugin_name"] = plugin_name
            if plugin_type is not None:
                context["plugin_type"] = plugin_type
            if plugin_command is not None:
                context["plugin_command"] = plugin_command
            super().__init__(f"Plugin: {message}", context=context)

    class MeltanoExecutionError(MeltanoProcessingError):
        """Execution errors with command context using DRY foundation."""

        def __init__(
            self,
            message: str = "Execution error",
            *,
            command: str | None = None,
            exit_code: int | None = None,
            **kwargs: object,
        ) -> None:
            """Initialize execution error with command context."""
            nested: dict[str, object] = dict(kwargs)
            if command is not None:
                nested["command"] = command
            if exit_code is not None:
                nested["exit_code"] = exit_code
            # Bypass nested context from processing error: set flat context as tests expect
            FlextMeltanoExceptions.MeltanoError.__init__(
                self, f"Execution: {message}", context=nested
            )

    class MeltanoSingerError(MeltanoError):
        """Singer protocol-specific errors using DRY foundation."""

        def __init__(
            self,
            message: str = "Singer error",
            *,
            stream_name: str | None = None,
            record_count: int | None = None,
            **kwargs: object,
        ) -> None:
            """Initialize Singer error with stream context."""
            context = dict(kwargs)
            if stream_name is not None:
                context["stream_name"] = stream_name
            if record_count is not None:
                context["record_count"] = record_count
            super().__init__(f"Singer: {message}", context=context)

    class MeltanoDBTError(MeltanoError):
        """DBT integration errors using DRY foundation."""

        def __init__(
            self,
            message: str = "DBT error",
            *,
            model_name: str | None = None,
            **kwargs: object,
        ) -> None:
            """Initialize DBT error with model context."""
            context = dict(kwargs)
            if model_name is not None:
                context["model_name"] = model_name
            super().__init__(f"DBT: {message}", context=context)

    # =================================================================
    # ALIASES FOR BACKWARD COMPATIBILITY - FlextMeltano[ErrorType]
    # =================================================================

    # Main class aliases (preferred names)
    FlextMeltanoError = MeltanoError
    FlextMeltanoValidationError = MeltanoValidationError
    FlextMeltanoConfigurationError = MeltanoConfigurationError
    FlextMeltanoConnectionError = MeltanoConnectionError
    FlextMeltanoProcessingError = MeltanoProcessingError
    FlextMeltanoAuthenticationError = MeltanoAuthenticationError
    FlextMeltanoTimeoutError = MeltanoTimeoutError
    FlextMeltanoPluginError = MeltanoPluginError
    FlextMeltanoExecutionError = MeltanoExecutionError
    FlextMeltanoSingerError = MeltanoSingerError
    FlextMeltanoDBTError = MeltanoDBTError


# =============================================================================
# MODULE-LEVEL ALIASES FOR BACKWARD COMPATIBILITY
# =============================================================================

# Export all nested classes as module-level aliases for backward compatibility
FlextMeltanoError = FlextMeltanoExceptions.MeltanoError
FlextMeltanoValidationError = FlextMeltanoExceptions.MeltanoValidationError
FlextMeltanoConfigurationError = FlextMeltanoExceptions.MeltanoConfigurationError
FlextMeltanoConnectionError = FlextMeltanoExceptions.MeltanoConnectionError
FlextMeltanoProcessingError = FlextMeltanoExceptions.MeltanoProcessingError
FlextMeltanoAuthenticationError = FlextMeltanoExceptions.MeltanoAuthenticationError
FlextMeltanoTimeoutError = FlextMeltanoExceptions.MeltanoTimeoutError
FlextMeltanoPluginError = FlextMeltanoExceptions.MeltanoPluginError
FlextMeltanoExecutionError = FlextMeltanoExceptions.MeltanoExecutionError
FlextMeltanoSingerError = FlextMeltanoExceptions.MeltanoSingerError
FlextMeltanoDBTError = FlextMeltanoExceptions.MeltanoDBTError


__all__: list[str] = [
    "FlextMeltanoAuthenticationError",
    "FlextMeltanoConfigurationError",
    "FlextMeltanoConnectionError",
    "FlextMeltanoDBTError",
    "FlextMeltanoError",
    "FlextMeltanoExecutionError",
    "FlextMeltanoPluginError",
    "FlextMeltanoProcessingError",
    "FlextMeltanoSingerError",
    "FlextMeltanoTimeoutError",
    "FlextMeltanoValidationError",
]
