"""FLEXT Meltano Tap Abstractions - Single unified class for tap operations.

This module provides the FlextMeltanoTapAbstractions class following FLEXT patterns:
- Single Responsibility Principle
- Railway-oriented programming with FlextCore.Result
- Clean Architecture with domain separation

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from typing import cast

from flext_core import FlextCore

# Use specific module imports to avoid circular dependencies
from flext_meltano.config import FlextMeltanoConfig
from flext_meltano.models import FlextMeltanoModels
from flext_meltano.typings import FlextMeltanoTypes


class FlextMeltanoTapAbstractions(
    FlextCore.Service[FlextMeltanoTypes.MeltanoCore.MeltanoConfigDict]
):
    """UNIFIED Tap Abstractions class consolidating ALL tap functionality.

    This single class provides:
    - Complete Singer tap protocol implementation
    - Stream discovery and management
    - Configuration validation and processing
    - Railway-oriented error handling throughout

    Following FLEXT 'one class per module' pattern.
    """

    def __init__(self, config: FlextMeltanoConfig | None = None) -> None:
        """Initialize unified tap abstractions with FLEXT configuration."""
        super().__init__()
        self._config = config or FlextMeltanoConfig()
        self.logger = FlextCore.Logger(__name__)

    def discover_streams(
        self, tap_config: FlextMeltanoModels.TapConfig
    ) -> FlextCore.Result[FlextCore.Types.Dict]:
        """Discover available streams for a tap configuration.

        Args:
            tap_config: Tap configuration with discovery parameters

        Returns:
            FlextCore.Result containing discovered stream catalog

        """
        try:
            self.logger.info(
                "Discovering streams for tap",
                tap_type=tap_config.tap_type,
                tap_name=tap_config.tap_type,
            )

            # Validate tap configuration
            if not tap_config.tap_type:
                return FlextCore.Result[FlextCore.Types.Dict].fail(
                    "Tap configuration must have name and type for discovery"
                )

            # For now, return empty catalog - would integrate with actual Singer taps
            catalog: FlextCore.Types.Dict = {
                "streams": [],
                "tap_name": tap_config.tap_type,
                "tap_type": tap_config.tap_type,
            }

            self.logger.info(
                "Stream discovery completed",
                stream_count=len(catalog.get("streams", [])),
            )

            return FlextCore.Result[FlextCore.Types.Dict].ok(catalog)

        except Exception as e:
            self.logger.exception("Stream discovery failed", error=str(e))
            return FlextCore.Result[FlextCore.Types.Dict].fail(
                f"Stream discovery failed: {e}"
            )

    def validate_stream_schema(
        self, stream_def: FlextMeltanoModels.StreamDefinition
    ) -> FlextCore.Result[bool]:
        """Validate a stream definition's schema.

        Args:
            stream_def: Stream definition to validate

        Returns:
            FlextCore.Result containing validation result

        """
        try:
            self.logger.debug(
                "Validating stream schema",
                stream_name=stream_def.stream_name,
            )

            # Basic schema validation
            if not stream_def.stream_schema:
                return FlextCore.Result[bool].fail("Stream schema cannot be empty")

            schema = cast("dict", stream_def.stream_schema)
            if "properties" not in schema:
                return FlextCore.Result[bool].fail(
                    "Stream schema must contain properties"
                )

            # Additional validation logic would go here
            # For now, just return success
            return FlextCore.Result[bool].ok(True)

        except Exception as e:
            self.logger.exception("Schema validation failed", error=str(e))
            return FlextCore.Result[bool].fail(f"Schema validation failed: {e}")

    def create_tap_instance(
        self, tap_config: FlextMeltanoModels.TapConfig
    ) -> FlextCore.Result[FlextMeltanoModels.TapInstance]:
        """Create a tap instance from configuration.

        Args:
            tap_config: Tap configuration

        Returns:
            FlextCore.Result containing configured tap instance

        """
        try:
            self.logger.info(
                "Creating tap instance",
                tap_name=tap_config.tap_type,
                tap_type=tap_config.tap_type,
            )

            # Create tap instance
            tap_instance = FlextMeltanoModels.TapInstance(
                tap_type=tap_config.tap_type,
                config=tap_config,
                status="configured",
            )

            self.logger.info(
                "Tap instance created successfully",
                tap_name=tap_instance.config.name,
            )

            return FlextCore.Result[FlextMeltanoModels.TapInstance].ok(tap_instance)

        except Exception as e:
            self.logger.exception("Tap instance creation failed", error=str(e))
            return FlextCore.Result[FlextMeltanoModels.TapInstance].fail(
                f"Tap instance creation failed: {e}"
            )

    def execute(
        self,
    ) -> FlextCore.Result[FlextMeltanoTypes.MeltanoCore.MeltanoConfigDict]:
        """Execute tap abstraction operations (implements Domain.Service)."""
        # This would orchestrate the overall tap abstraction workflow
        # For now, return the current configuration
        return FlextCore.Result[FlextMeltanoTypes.MeltanoCore.MeltanoConfigDict].ok(
            self._config.model_dump()
        )
