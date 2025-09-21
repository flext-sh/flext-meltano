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

    # Use public aliases from FlextExceptions - these are the correct class references
    BaseError = FlextExceptions.BaseError
    Error = FlextExceptions.Error
    ConfigurationError = FlextExceptions.ConfigurationError
    ConnectionError = FlextExceptions.ConnectionError
    ValidationError = FlextExceptions.ValidationError
    AuthenticationError = FlextExceptions.AuthenticationError
    ProcessingError = FlextExceptions.ProcessingError
    TimeoutError = FlextExceptions.TimeoutError


__all__ = [
    "FlextMeltanoExceptions",
]
