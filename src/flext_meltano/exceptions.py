"""FLEXT Meltano Exceptions - Single Class Architecture.

Domain-specific exceptions using facade pattern to eliminate duplication while maintaining
compatibility with the Flext[Area][Module] pattern and hierarchical inheritance from flext-core.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from flext_core import FlextExceptions, FlextTypes
from pydantic import BaseModel, Field

# =============================================================================
# PYDANTIC MODELS FOR EXCEPTION CONTEXT - ELIMINATES MULTIPLE PARAMETERS
# =============================================================================


class ValidationErrorContext(BaseModel):
    """Context for validation errors - ELIMINATES 6+ parameters."""

    field_name: str | None = Field(
        default=None, description="Field that failed validation"
    )
    expected_type: str | None = Field(
        default=None, description="Expected type or format"
    )
    actual_value: str | None = Field(default=None, description="Actual value received")
    validation_rule: str | None = Field(
        default=None, description="Validation rule violated"
    )
    additional_info: FlextTypes.Core.Dict = Field(
        default_factory=dict, description="Additional context"
    )


class ConfigurationErrorContext(BaseModel):
    """Context for configuration errors - ELIMINATES 6+ parameters."""

    config_file: str | None = Field(default=None, description="Configuration file path")
    section: str | None = Field(default=None, description="Configuration section")
    key: str | None = Field(default=None, description="Configuration key")
    expected_format: str | None = Field(default=None, description="Expected format")
    additional_info: FlextTypes.Core.Dict = Field(
        default_factory=dict, description="Additional context"
    )


class ConnectionErrorContext(BaseModel):
    """Context for connection errors - ELIMINATES 6+ parameters."""

    host: str | None = Field(default=None, description="Target host")
    port: int | None = Field(default=None, description="Target port")
    protocol: str | None = Field(default=None, description="Connection protocol")
    timeout: int | None = Field(default=None, description="Connection timeout")
    retry_count: int = Field(default=0, description="Number of retries attempted")
    additional_info: FlextTypes.Core.Dict = Field(
        default_factory=dict, description="Additional context"
    )


class ProcessingErrorContext(BaseModel):
    """Context for processing errors - ELIMINATES 6+ parameters."""

    operation: str | None = Field(default=None, description="Operation being performed")
    records_processed: int = Field(default=0, description="Number of records processed")
    batch_id: str | None = Field(default=None, description="Batch identifier")
    stream_name: str | None = Field(default=None, description="Stream being processed")
    stage: str | None = Field(default=None, description="Processing stage")
    additional_info: FlextTypes.Core.Dict = Field(
        default_factory=dict, description="Additional context"
    )


class PluginErrorContext(BaseModel):
    """Context for plugin errors - ELIMINATES 6+ parameters."""

    plugin_name: str | None = Field(default=None, description="Plugin name")
    plugin_type: str | None = Field(default=None, description="Plugin type")
    version: str | None = Field(default=None, description="Plugin version")
    command: str | None = Field(default=None, description="Command executed")
    exit_code: int | None = Field(default=None, description="Exit code")
    additional_info: FlextTypes.Core.Dict = Field(
        default_factory=dict, description="Additional context"
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
        """Validation error using Pydantic context - ELIMINATES parameter explosion."""

        def __init__(
            self,
            message: str = "Validation error",
            context: ValidationErrorContext | None = None,
        ) -> None:
            """Initialize with Pydantic context model - ELIMINATES multiple parameters."""
            super().__init__()
            self.message = message
            self.context = {"context": context.model_dump() if context else {}}

    class MeltanoConfigurationError(MeltanoError, FlextExceptions):
        """Configuration error using Pydantic context - ELIMINATES 6+ parameters."""

        def __init__(
            self,
            message: str = "Configuration error",
            context: ConfigurationErrorContext | None = None,
        ) -> None:
            """Initialize with Pydantic context model - ELIMINATES manual parameter handling."""
            super().__init__()
            self.message = f"Configuration: {message}"
            self.context = {"context": context.model_dump() if context else {}}

    class MeltanoConnectionError(MeltanoError):
        """Connection error using Pydantic context - ELIMINATES 6+ parameters."""

        def __init__(
            self,
            message: str = "Connection error",
            context: ConnectionErrorContext | None = None,
        ) -> None:
            """Initialize with Pydantic context model - ELIMINATES manual parameter assembly."""
            super().__init__()
            self.message = f"Connection: {message}"
            self.context = {"context": context.model_dump() if context else {}}

    class MeltanoProcessingError(MeltanoError):
        """Processing error using Pydantic context - ELIMINATES 6+ parameters."""

        def __init__(
            self,
            message: str = "Processing error",
            context: ProcessingErrorContext | None = None,
        ) -> None:
            """Initialize with Pydantic context model - ELIMINATES parameter explosion."""
            super().__init__()
            self.message = f"Processing: {message}"
            self.context = {"context": context.model_dump() if context else {}}

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
            super().__init__()
            self.message = f"Authentication: {message}"
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
            super().__init__()
            self.message = f"Timeout: {message}"
            nested: FlextTypes.Core.Dict = {}
            if timeout_seconds is not None:
                nested["timeout"] = timeout_seconds
            if operation is not None:
                nested["operation"] = operation
            if kwargs:
                nested.update(dict(kwargs))
            self.context = {"context": nested}

    class MeltanoPluginError(MeltanoError):
        """Plugin-specific errors with enhanced context using Pydantic model."""

        def __init__(
            self,
            message: str = "Plugin error",
            context: PluginErrorContext | None = None,
        ) -> None:
            """Initialize plugin error with Pydantic context - ELIMINATES multiple parameters."""
            super().__init__()
            self.message = f"Plugin: {message}"
            self.context = {"context": context.model_dump() if context else {}}

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
            nested: FlextTypes.Core.Dict = dict(kwargs)
            if command is not None:
                nested["command"] = command
            if exit_code is not None:
                nested["exit_code"] = exit_code
            # Bypass nested context from processing error: set flat context as tests expect
            FlextMeltanoExceptions.MeltanoError.__init__(self)
            self.message = f"Execution: {message}"
            self.context = {"context": nested}

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
            super().__init__()
            self.message = f"Singer: {message}"
            self.context = {"context": context}

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
            super().__init__()
            self.message = f"DBT: {message}"
            self.context = {"context": context}


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


__all__: FlextTypes.Core.StringList = [
    # Individual exception types
    "FlextMeltanoAuthenticationError",
    "FlextMeltanoConfigurationError",
    "FlextMeltanoConnectionError",
    "FlextMeltanoDBTError",
    "FlextMeltanoError",
    # Main exceptions class
    "FlextMeltanoExceptions",
    "FlextMeltanoExecutionError",
    "FlextMeltanoPluginError",
    "FlextMeltanoProcessingError",
    "FlextMeltanoSingerError",
    "FlextMeltanoTimeoutError",
    "FlextMeltanoValidationError",
]
