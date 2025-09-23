"""FLEXT Meltano Exceptions - Domain-specific exception management.

SINGLE CLASS PER MODULE: FlextMeltanoExceptions with nested exception types.
FLEXT COMPLIANCE: All exceptions inherit from flext-core foundation.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from flext_core import FlextExceptions

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

    BaseError = FlextExceptions.BaseError
    Error = FlextExceptions.Error
    ConfigurationError = FlextExceptions.ConfigurationError
    ConnectionError = FlextExceptions.ConnectionError
    ValidationError = FlextExceptions.ValidationError
    AuthenticationError = FlextExceptions.AuthenticationError
    ProcessingError = FlextExceptions.ProcessingError
    TimeoutError = FlextExceptions.TimeoutError

    # Forward declarations for Meltano-specific exceptions (defined below)
    MeltanoProjectError: type[Exception]
    PluginError: type[Exception]
    SingerProtocolError: type[Exception]
    DbtExecutionError: type[Exception]
    PipelineError: type[Exception]
    CatalogDiscoveryError: type[Exception]
    StreamValidationError: type[Exception]
    ConfigBuilderError: type[Exception]


# Meltano-specific exceptions (defined outside class to avoid MyPy inheritance issues)
class MeltanoProjectError(FlextExceptions.BaseError):
    """Meltano project configuration or initialization error."""


class PluginError(FlextExceptions.BaseError):
    """Meltano plugin installation or execution error."""


class SingerProtocolError(FlextExceptions.BaseError):
    """Singer tap/target protocol compliance error."""


class DbtExecutionError(FlextExceptions.BaseError):
    """DBT model execution or compilation error."""


class PipelineError(FlextExceptions.BaseError):
    """ELT pipeline execution error."""


class CatalogDiscoveryError(FlextExceptions.BaseError):
    """Singer catalog discovery error."""


class StreamValidationError(FlextExceptions.BaseError):
    """Singer stream validation error."""


class ConfigBuilderError(FlextExceptions.BaseError):
    """Meltano configuration builder error."""


# Assign Meltano-specific exceptions to FlextMeltanoExceptions after definition
FlextMeltanoExceptions.MeltanoProjectError = MeltanoProjectError
FlextMeltanoExceptions.PluginError = PluginError
FlextMeltanoExceptions.SingerProtocolError = SingerProtocolError
FlextMeltanoExceptions.DbtExecutionError = DbtExecutionError
FlextMeltanoExceptions.PipelineError = PipelineError
FlextMeltanoExceptions.CatalogDiscoveryError = CatalogDiscoveryError
FlextMeltanoExceptions.StreamValidationError = StreamValidationError
FlextMeltanoExceptions.ConfigBuilderError = ConfigBuilderError

__all__ = [
    "FlextMeltanoExceptions",
]
