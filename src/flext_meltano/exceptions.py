"""FLEXT Meltano Exceptions - Domain-specific exception management.

SINGLE CLASS PER MODULE: FlextMeltanoExceptions with nested exception types.
FLEXT COMPLIANCE: All exceptions inherit from flext-core foundation.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from flext_core.exceptions import FlextExceptions as FlextExceptionsModule

from flext_core import FlextExceptions

# Import the actual exception classes for inheritance
_Error = FlextExceptionsModule.Error
_ValidationError = FlextExceptionsModule.ValidationError
_ConfigurationError = FlextExceptionsModule.ConfigurationError

# ============================================================================
# SINGLE UNIFIED EXCEPTION CLASS - FLEXT Architecture Compliance
# ============================================================================


class FlextMeltanoExceptions:
    """Unified exception management for Meltano operations - Single Responsibility Pattern.

    Provides domain-specific exception types for FLEXT Meltano operations while
    maintaining single class per module principle. All exceptions inherit from
    flext-core foundation following FLEXT domain separation standards.

    Usage:
        >>> raise FlextMeltanoExceptions.ConfigurationError("Invalid Meltano config")
        >>> raise FlextMeltanoExceptions.ValidationError("Plugin validation failed")
    """

    # Core exceptions from flext-core foundation
    BaseError = FlextExceptions.BaseError
    Error = FlextExceptions.Error
    ConfigurationError = FlextExceptions.ConfigurationError
    ConnectionError = FlextExceptions.ConnectionError
    ValidationError = FlextExceptions.ValidationError
    AuthenticationError = FlextExceptions.AuthenticationError
    ProcessingError = FlextExceptions.ProcessingError
    TimeoutError = FlextExceptions.TimeoutError

    # Expose Meltano-specific exceptions as class attributes
    @property
    def MeltanoProjectError(self) -> type[MeltanoProjectError]:
        """Meltano project configuration or initialization error."""
        return MeltanoProjectError

    @property
    def PluginError(self) -> type[PluginError]:
        """Meltano plugin installation or execution error."""
        return PluginError

    @property
    def SingerProtocolError(self) -> type[SingerProtocolError]:
        """Singer tap/target protocol compliance error."""
        return SingerProtocolError

    @property
    def DbtExecutionError(self) -> type[DbtExecutionError]:
        """DBT model execution or compilation error."""
        return DbtExecutionError

    @property
    def PipelineError(self) -> type[PipelineError]:
        """ELT pipeline execution error."""
        return PipelineError

    @property
    def CatalogDiscoveryError(self) -> type[CatalogDiscoveryError]:
        """Singer catalog discovery error."""
        return CatalogDiscoveryError

    @property
    def StreamValidationError(self) -> type[StreamValidationError]:
        """Singer stream validation error."""
        return StreamValidationError

    @property
    def ConfigBuilderError(self) -> type[ConfigBuilderError]:
        """Meltano configuration builder error."""
        return ConfigBuilderError


# Meltano-specific exceptions (defined outside class to avoid MyPy inheritance issues)
class MeltanoProjectError(_Error):
    """Meltano project configuration or initialization error."""


class PluginError(_Error):
    """Meltano plugin installation or execution error."""


class SingerProtocolError(_Error):
    """Singer tap/target protocol compliance error."""


class DbtExecutionError(_Error):
    """DBT model execution or compilation error."""


class PipelineError(_Error):
    """ELT pipeline execution error."""


class CatalogDiscoveryError(_Error):
    """Singer catalog discovery error."""


class StreamValidationError(_ValidationError):
    """Singer stream validation error."""


class ConfigBuilderError(_ConfigurationError):
    """Meltano configuration builder error."""


__all__ = [
    "FlextMeltanoExceptions",
]
