"""Common exception classes for FLEXT Meltano taps and targets.

This module consolidates exception patterns that were duplicated across
multiple tap and target projects, providing consistent error handling.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from typing import Any

from flext_core.exceptions import FlextException


class FlextMeltanoError(FlextException):
    """Base exception for FLEXT Meltano operations."""


class FlextMeltanoConfigurationError(FlextException):
    """Base exception for FLEXT Meltano operations."""


class FlextMeltanoValidationError(FlextException):
    """Base exception for FLEXT Meltano operations."""


class FlextMeltanoOrchestrationError(FlextMeltanoError):
    """Orchestration-related errors."""


class FlextMeltanoPipelineError(FlextMeltanoOrchestrationError):
    """Pipeline execution errors."""


class FlextMeltanoSingerError(FlextMeltanoError):
    """Singer protocol errors."""


class FlextMeltanoTapError(FlextMeltanoSingerError):
    """Singer tap errors."""


class FlextMeltanoDbtError(FlextMeltanoError):
    """DBT-related errors."""


class FlextMeltanoDbtRunError(FlextMeltanoDbtError):
    """DBT run errors."""


class FlextMeltanoProjectError(FlextMeltanoError):
    """Project-related errors."""


class FlextMeltanoExecutionError(FlextMeltanoError):
    """Execution errors."""


class FlextMeltanoPluginError(FlextMeltanoError):
    """Plugin-related errors."""


class FlextMeltanoStateError(FlextMeltanoError):
    """State management errors."""


class FlextMeltanoCommonError(FlextMeltanoError):
    """Base error for common module.

    Consolidates error patterns from tap/target projects.
    """


class FlextMeltanoCommonConfigurationError(FlextMeltanoConfigurationError):
    """Configuration error in common module.

    Consolidates configuration error patterns from multiple projects.
    """


class FlextMeltanoCommonValidationError(FlextMeltanoValidationError):
    """Validation error in common module.

    Consolidates validation error patterns from multiple projects.
    """


class FlextMeltanoCommonConnectionError(FlextMeltanoCommonError):
    """Connection error in common module.

    Consolidates connection error patterns from Oracle WMS, Oracle OIC, LDAP projects.
    """

    def __init__(
        self,
        message: str,
        host: str | None = None,
        port: int | None = None,
    ) -> None:
        """Initialize connection error.

        Args:
            message: Error message
            host: Optional host that failed to connect
            port: Optional port that failed to connect

        """
        if host and port:
            message = f"{message} (host: {host}, port: {(port,)})"
        elif host:
            message = f"{message} (host: {(host,)})"

        super().__init__(message)
        self.host = host
        self.port = port


# Base Target Exception Pattern (consolidates 167+ lines of duplication)
class FlextMeltanoTargetError(FlextMeltanoCommonError):
    """Base target exception consolidating patterns from all target projects."""

    def __init__(self, message: str, details: dict[str, Any] | None = None) -> None:
        """Initialize with optional error details."""
        super().__init__(message)
        self.message = message
        self.details = details or {}


class FlextMeltanoTargetAuthenticationError(FlextMeltanoTargetError):
    """Authentication-related target errors."""


class FlextMeltanoTargetTransformationError(FlextMeltanoTargetError):
    """Data transformation target errors."""


class FlextMeltanoTargetProcessingError(FlextMeltanoTargetError):
    """Record processing target errors."""
