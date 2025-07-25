"""Common base classes for FLEXT Meltano taps and targets.

This module consolidates base class patterns that were duplicated across
multiple tap and target projects, providing consistent inheritance.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from typing import Any

from flext_meltano.common.exceptions import (
    FlextMeltanoCommonConfigurationError,
    FlextMeltanoCommonError,
)
from flext_meltano.common.validation import FlextMeltanoConfigValidator

# Legacy imports for Singer - now using direct Singer SDK
try:
    from singer_sdk import (
        Stream as FlextMeltanoStream,
        Tap as FlextMeltanoTap,
        Target as FlextMeltanoTarget,
    )
except ImportError:
    # Fallback types when Singer SDK not available
    FlextMeltanoStream = FlextMeltanoTap = FlextMeltanoTarget = type(object)  # type: ignore[assignment,misc]


class FlextMeltanoBaseTap(FlextMeltanoTap):
    """Base tap class with common functionality.

    Consolidates tap patterns that were duplicated across Oracle WMS,
    Oracle OIC, LDAP, and other tap projects.
    """

    def __init__(self, config: dict[str, Any] | None = None) -> None:
        """Initialize base tap.

        Args:
            config: Tap configuration
        """
        super().__init__(config)
        self.validator = FlextMeltanoConfigValidator()

    def validate_configuration(self) -> dict[str, Any]:
        """Validate tap configuration using common patterns.

        Consolidates validation logic from multiple tap projects.

        Returns:
            Validation results

        Raises:
            FlextMeltanoCommonConfigurationError: If validation fails
        """
        if not self.config:
            msg = "Configuration is required"
            raise FlextMeltanoCommonConfigurationError(msg)

        if not self.validator.validate_config(self.config):
            errors = self.validator.get_errors()
            msg = f"Configuration validation failed: {'; '.join(errors)}"
            raise FlextMeltanoCommonConfigurationError(msg)

        return {
            "valid": True,
            "errors": [],
            "config": self.config,
        }

    def validate_connection(self) -> bool:
        """Validate connection using common patterns.

        Consolidates connection validation from multiple projects.

        Returns:
            True if connection is valid

        Raises:
            FlextMeltanoCommonError: If connection validation fails
        """
        # Default implementation - can be overridden by specific taps
        if not self.config:
            msg = "Configuration required for connection validation"
            raise FlextMeltanoCommonError(msg)

        return True

    def discover_streams(self) -> list[dict[str, Any]]:
        """Discover streams using common patterns.

        Consolidates stream discovery from multiple tap projects.

        Returns:
            List of discovered stream definitions
        """
        # Default implementation - should be overridden by specific taps
        return []


class FlextMeltanoBaseTarget(FlextMeltanoTarget):
    """Base target class with common functionality.

    Consolidates target patterns that were duplicated across Oracle WMS,
    Oracle OIC, LDAP, LDIF, and other target projects.
    """

    def __init__(self, config: dict[str, Any] | None = None) -> None:
        """Initialize base target.

        Args:
            config: Target configuration
        """
        super().__init__(config)
        self.validator = FlextMeltanoConfigValidator()

    def validate_configuration(self) -> dict[str, Any]:
        """Validate target configuration using common patterns.

        Consolidates validation logic from multiple target projects.

        Returns:
            Validation results

        Raises:
            FlextMeltanoCommonConfigurationError: If validation fails
        """
        if not self.config:
            msg = "Configuration is required"
            raise FlextMeltanoCommonConfigurationError(msg)

        if not self.validator.validate_config(self.config):
            errors = self.validator.get_errors()
            msg = f"Configuration validation failed: {'; '.join(errors)}"
            raise FlextMeltanoCommonConfigurationError(msg)

        return {
            "valid": True,
            "errors": [],
            "config": self.config,
        }

    def validate_connection(self) -> bool:
        """Validate connection using common patterns.

        Consolidates connection validation from multiple projects.

        Returns:
            True if connection is valid

        Raises:
            FlextMeltanoCommonError: If connection validation fails
        """
        # Default implementation - can be overridden by specific targets
        if not self.config:
            msg = "Configuration required for connection validation"
            raise FlextMeltanoCommonError(msg)

        return True

    def validate_record(self, record: dict[str, Any]) -> list[str]:
        """Validate individual record using common patterns.

        Consolidates record validation from target projects.

        Args:
            record: Record to validate

        Returns:
            List of validation errors (empty if valid)
        """
        return self.validator.validate_record(record)

    def validate_batch(self, records: list[dict[str, Any]]) -> dict[str, Any]:
        """Validate batch of records using common patterns.

        Consolidates batch validation from target projects.

        Args:
            records: List of records to validate

        Returns:
            Validation results dictionary
        """
        return self.validator.validate_batch(records)


class FlextMeltanoBaseStream(FlextMeltanoStream):
    """Base stream class with common functionality.

    Consolidates stream patterns that were duplicated across tap projects.
    """

    def __init__(
        self,
        tap: FlextMeltanoBaseTap,
        name: str,
        schema: dict[str, Any],
        **kwargs: object,
    ) -> None:
        """Initialize base stream.

        Args:
            tap: Parent tap instance
            name: Stream name
            schema: Stream schema
            **kwargs: Additional stream configuration
        """
        super().__init__(tap, name, schema, **kwargs)
        self.validator = FlextMeltanoConfigValidator()

    def validate_performance(self, threshold_records_per_second: float = 100.0) -> None:
        """Validate stream performance using common patterns.

        Consolidates performance validation from tap projects.

        Args:
            threshold_records_per_second: Minimum expected performance threshold

        Raises:
            FlextMeltanoCommonError: If performance is below threshold
        """
        # Default implementation - can be enhanced by specific streams
        # This consolidates the performance validation pattern found in Oracle tap

    def validate_schema_compatibility(self, _schema: dict[str, Any]) -> bool:
        """Validate schema compatibility using common patterns.

        Consolidates schema validation from tap projects.

        Args:
            _schema: Schema to validate compatibility against

        Returns:
            True if schemas are compatible
        """
        # Default implementation - can be overridden by specific streams
        return True
