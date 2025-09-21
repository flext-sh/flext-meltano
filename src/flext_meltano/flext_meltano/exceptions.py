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

    class BaseError(FlextExceptions.BaseError):
        """Base exception for Meltano operations."""

    class Error(FlextExceptions.Error):
        """Generic Meltano errors."""

    class ConfigurationError(FlextExceptions.ConfigurationError):
        """Meltano configuration errors."""

    class ConnectionError(FlextExceptions.ConnectionError):
        """Meltano connection errors."""

    class ValidationError(FlextExceptions.ValidationError):
        """Meltano validation errors."""

    class AuthenticationError(FlextExceptions.AuthenticationError):
        """Meltano authentication errors."""

    class ProcessingError(FlextExceptions.ProcessingError):
        """Meltano processing errors."""

    class TimeoutError(FlextExceptions.TimeoutError):
        """Meltano timeout errors."""


__all__ = [
    "FlextMeltanoExceptions",
]
