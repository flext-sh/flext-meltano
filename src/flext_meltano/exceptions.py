"""FLEXT Meltano Exceptions - Consolidated from client-b-meltano-native.

This module provides a comprehensive exception hierarchy following FLEXT standards,
Clean Architecture principles, and proper inheritance patterns.

Consolidated from client-b-meltano-native/exceptions.py to centralize error handling
for all Singer/Meltano/DBT components in the FLEXT ecosystem.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from typing import Any


class FlextMeltanoError(Exception):
    """Base exception for all FLEXT Meltano errors.

    This is the root exception class that all other exceptions inherit from.
    Follows FLEXT standards for exception hierarchies.
    """

    def __init__(
        self,
        message: str,
        *,
        error_code: str | None = None,
        context: dict[str, Any] | None = None,
    ) -> None:
        """Initialize the base exception.

        Args:
            message: Human-readable error message
            error_code: Optional machine-readable error code
            context: Optional additional context information

        """
        super().__init__(message)
        self.message = message
        self.error_code = error_code or self.__class__.__name__
        self.context = context or {}

    def __str__(self) -> str:
        """Return string representation of the exception."""
        if self.context:
            return f"{self.message} (Context: {self.context})"
        return self.message

    def __repr__(self) -> str:
        """Return detailed representation of the exception."""
        return (
            f"{self.__class__.__name__}("
            f"message={self.message!r}, "
            f"error_code={self.error_code!r}, "
            f"context={self.context!r})"
        )


# ================================
# CONFIGURATION EXCEPTIONS
# ================================


class FlextMeltanoConfigurationError(FlextMeltanoError):
    """Exception raised for configuration-related errors."""


class FlextMeltanoValidationError(FlextMeltanoConfigurationError):
    """Exception raised for validation errors in configuration."""


class FlextMeltanoMissingConfigError(FlextMeltanoConfigurationError):
    """Exception raised when required configuration is missing."""


# ================================
# ORCHESTRATION EXCEPTIONS
# ================================


class FlextMeltanoOrchestrationError(FlextMeltanoError):
    """Exception raised for orchestration-related errors."""


class FlextMeltanoPipelineError(FlextMeltanoOrchestrationError):
    """Exception raised for pipeline execution errors."""


class FlextMeltanoPipelineTimeoutError(FlextMeltanoPipelineError):
    """Exception raised when pipeline execution times out."""


class FlextMeltanoPipelineValidationError(FlextMeltanoPipelineError):
    """Exception raised when pipeline validation fails."""


# ================================
# ORACLE CONNECTION EXCEPTIONS
# ================================


class FlextMeltanoOracleError(FlextMeltanoError):
    """Exception raised for Oracle database-related errors."""


class FlextMeltanoOracleConnectionError(FlextMeltanoOracleError):
    """Exception raised for Oracle connection errors."""


class FlextMeltanoOracleQueryError(FlextMeltanoOracleError):
    """Exception raised for Oracle query execution errors."""


class FlextMeltanoOracleTimeoutError(FlextMeltanoOracleError):
    """Exception raised when Oracle operations timeout."""


# ================================
# MONITORING & ALERT EXCEPTIONS
# ================================


class FlextMeltanoMonitoringError(FlextMeltanoError):
    """Exception raised for monitoring system errors."""


class FlextMeltanoAlertError(FlextMeltanoMonitoringError):
    """Exception raised for alert system errors."""


class FlextMeltanoAlertDeliveryError(FlextMeltanoAlertError):
    """Exception raised when alert delivery fails."""


# ================================
# DATA VALIDATION EXCEPTIONS
# ================================


class FlextMeltanoDataError(FlextMeltanoError):
    """Exception raised for data-related errors."""


class FlextMeltanoDataValidationError(FlextMeltanoDataError):
    """Exception raised for data validation errors."""


class FlextMeltanoDataQualityError(FlextMeltanoDataError):
    """Exception raised for data quality issues."""


# ================================
# SINGER PROTOCOL EXCEPTIONS
# ================================


class FlextMeltanoSingerError(FlextMeltanoError):
    """Exception raised for Singer protocol errors."""


class FlextMeltanoTapError(FlextMeltanoSingerError):
    """Exception raised for Singer tap errors."""


class FlextMeltanoTargetError(FlextMeltanoSingerError):
    """Exception raised for Singer target errors."""


# ================================
# DBT EXCEPTIONS
# ================================


class FlextMeltanoDbtError(FlextMeltanoError):
    """Exception raised for DBT-related errors."""


class FlextMeltanoDbtCompilationError(FlextMeltanoDbtError):
    """Exception raised for DBT compilation errors."""


class FlextMeltanoDbtRunError(FlextMeltanoDbtError):
    """Exception raised for DBT run errors."""


class FlextMeltanoDbtTestError(FlextMeltanoDbtError):
    """Exception raised for DBT test errors."""


# ================================
# PROJECT EXCEPTIONS
# ================================


class FlextMeltanoProjectError(FlextMeltanoError):
    """Exception raised for project-related errors."""


class FlextMeltanoExecutionError(FlextMeltanoError):
    """Exception raised for execution errors."""


class FlextMeltanoPluginError(FlextMeltanoError):
    """Exception raised for plugin-related errors."""


class FlextMeltanoStateError(FlextMeltanoError):
    """Exception raised for state management errors."""


class FlextMeltanoConfigError(FlextMeltanoError):
    """Exception raised for configuration errors."""


# ================================
# BACKWARD COMPATIBILITY ALIASES
# ================================

# client-b compatibility aliases - for backward compatibility
client-bMeltanoError = FlextMeltanoError
client-bMeltanoConfigurationError = FlextMeltanoConfigurationError
client-bMeltanoValidationError = FlextMeltanoValidationError
client-bMeltanoMissingConfigError = FlextMeltanoMissingConfigError
client-bMeltanoOrchestrationError = FlextMeltanoOrchestrationError
client-bMeltanoPipelineError = FlextMeltanoPipelineError
client-bMeltanoPipelineTimeoutError = FlextMeltanoPipelineTimeoutError
client-bMeltanoPipelineValidationError = FlextMeltanoPipelineValidationError
client-bMeltanoOracleError = FlextMeltanoOracleError
client-bMeltanoOracleConnectionError = FlextMeltanoOracleConnectionError
client-bMeltanoOracleQueryError = FlextMeltanoOracleQueryError
client-bMeltanoOracleTimeoutError = FlextMeltanoOracleTimeoutError
client-bMeltanoMonitoringError = FlextMeltanoMonitoringError
client-bMeltanoAlertError = FlextMeltanoAlertError
client-bMeltanoAlertDeliveryError = FlextMeltanoAlertDeliveryError
client-bMeltanoDataError = FlextMeltanoDataError
client-bMeltanoDataValidationError = FlextMeltanoDataValidationError
client-bMeltanoDataQualityError = FlextMeltanoDataQualityError
client-bMeltanoSingerError = FlextMeltanoSingerError
client-bMeltanoTapError = FlextMeltanoTapError
client-bMeltanoTargetError = FlextMeltanoTargetError


# ================================
# PUBLIC API
# ================================

__all__ = [
    "FlextMeltanoAlertDeliveryError",
    "FlextMeltanoAlertError",
    "FlextMeltanoConfigError",
    "FlextMeltanoConfigurationError",
    "FlextMeltanoDataError",
    "FlextMeltanoDataQualityError",
    "FlextMeltanoDataValidationError",
    "FlextMeltanoDbtCompilationError",
    "FlextMeltanoDbtError",
    "FlextMeltanoDbtRunError",
    "FlextMeltanoDbtTestError",
    # Core FLEXT Meltano exceptions
    "FlextMeltanoError",
    "FlextMeltanoExecutionError",
    "FlextMeltanoMissingConfigError",
    "FlextMeltanoMonitoringError",
    "FlextMeltanoOracleConnectionError",
    "FlextMeltanoOracleError",
    "FlextMeltanoOracleQueryError",
    "FlextMeltanoOracleTimeoutError",
    "FlextMeltanoOrchestrationError",
    "FlextMeltanoPipelineError",
    "FlextMeltanoPipelineTimeoutError",
    "FlextMeltanoPipelineValidationError",
    "FlextMeltanoPluginError",
    "FlextMeltanoProjectError",
    "FlextMeltanoSingerError",
    "FlextMeltanoStateError",
    "FlextMeltanoTapError",
    "FlextMeltanoTargetError",
    "FlextMeltanoValidationError",
    "client-bMeltanoAlertDeliveryError",
    "client-bMeltanoAlertError",
    "client-bMeltanoConfigurationError",
    "client-bMeltanoDataError",
    "client-bMeltanoDataQualityError",
    "client-bMeltanoDataValidationError",
    # client-b backward compatibility aliases
    "client-bMeltanoError",
    "client-bMeltanoMissingConfigError",
    "client-bMeltanoMonitoringError",
    "client-bMeltanoOracleConnectionError",
    "client-bMeltanoOracleError",
    "client-bMeltanoOracleQueryError",
    "client-bMeltanoOracleTimeoutError",
    "client-bMeltanoOrchestrationError",
    "client-bMeltanoPipelineError",
    "client-bMeltanoPipelineTimeoutError",
    "client-bMeltanoPipelineValidationError",
    "client-bMeltanoSingerError",
    "client-bMeltanoTapError",
    "client-bMeltanoTargetError",
    "client-bMeltanoValidationError",
]
