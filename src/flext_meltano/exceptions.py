"""FLEXT Meltano Exceptions - Domain-specific exception management.

SINGLE CLASS PER MODULE: FlextMeltanoExceptions with nested exception types.
FLEXT COMPLIANCE: All exceptions inherit from flext-core foundation.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from flext_core import FlextExceptions


class FlextMeltanoExceptions(FlextExceptions):
    """Single unified meltano exceptions class following FLEXT standards.

    Contains all exception definitions for meltano domain operations.
    Follows FLEXT pattern: one class per module with nested subclasses.
    """

    BaseError = FlextExceptions.BaseError
    Error = FlextExceptions.Error
    ConfigurationError = FlextExceptions.ConfigurationError
    ConnectionError = FlextExceptions.ConnectionError
    ValidationError = FlextExceptions.ValidationError
    AuthenticationError = FlextExceptions.AuthenticationError
    ProcessingError = FlextExceptions.ProcessingError
    TimeoutError = FlextExceptions.TimeoutError

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


__all__ = [
    "FlextMeltanoExceptions",
]
