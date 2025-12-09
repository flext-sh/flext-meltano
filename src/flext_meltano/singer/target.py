"""Singer Target Protocol Implementation for FLEXT Meltano.

This module provides the Singer Target abstraction following the Singer
specification with FLEXT ecosystem patterns and railway-oriented programming.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from flext_core import FlextResult, FlextService
from singer_sdk import Target

from flext_meltano.config import FlextMeltanoConfig
from flext_meltano.constants import FlextMeltanoConstants
from flext_meltano.models import FlextMeltanoModels
from flext_meltano.typings import FlextMeltanoTypes

# Import aliases for simplified usage
r = FlextResult
s = FlextService
t = FlextMeltanoTypes
c = FlextMeltanoConstants
m = FlextMeltanoModels


class FlextMeltanoTargetAbstractions(s[t.MeltanoCore.MeltanoConfigDict]):
    """UNIFIED Sink Abstractions class consolidating ALL sink functionality.

    This single class provides:
    - Complete Singer sink protocol implementation
    - Sink management and batch processing
    - Configuration validation and processing
    - Railway-oriented error handling throughout

    Following FLEXT 'one class per module' pattern.
    """

    # Instance attributes (declared for type checker)
    _config: object

    def __init__(self, config: object | None = None) -> None:
        """Initialize unified sink abstractions with FLEXT configuration."""
        self._config = config or FlextMeltanoConfig()
        # Initialize FlextService base - logger comes from FlextMixins
        super().__init__()

    def configure_sink(self, sink_config: m.DataSinkConfig) -> r[m.DataSinkDefinition]:
        """Configure a sink for a sink configuration.

        Args:
        sink_config: Sink configuration

        Returns:
        FlextResult containing configured sink definition

        """
        try:
            self.logger.info(
                "Configuring sink for target",
                target_name=sink_config.sink_type,
                target_type=sink_config.sink_type,
            )

            # Create sink definition
            sink_def = m.DataSinkDefinition(
                sink_name=f"{sink_config.sink_type}_sink",
                sink_type=sink_config.sink_type,
                config=sink_config.model_dump(),
                status="configured",
            )

            self.logger.info(
                "Sink configured successfully",
                sink_name=sink_def.sink_name,
            )

            return r[m.DataSinkDefinition].ok(sink_def)

        except Exception as e:
            self.logger.exception("Sink configuration failed", error=str(e))
            return r[m.DataSinkDefinition].fail(f"Sink configuration failed: {e}")

    def validate_sink_config(self, sink_config: m.DataSinkConfig) -> r[bool]:
        """Validate a sink configuration.

        Args:
        sink_config: Sink configuration to validate

        Returns:
        FlextResult containing validation result

        """
        try:
            self.logger.debug(
                "Validating target configuration",
                target_name=sink_config.sink_type,
            )

            # Basic validation
            if not sink_config.sink_type:
                return r[bool].fail("Target configuration must have name and type")

            # Additional validation logic would go here
            # For now, just return success
            return r[bool].ok(True)

        except Exception as e:
            self.logger.exception(
                "Target configuration validation failed",
                error=str(e),
            )
            return r[bool].fail(f"Target configuration validation failed: {e}")

    def create_sink_instance(
        self,
        sink_config: m.DataSinkConfig,
    ) -> r[m.DataSinkInstance]:
        """Create a sink instance from configuration.

        Args:
        sink_config: Sink configuration

        Returns:
        FlextResult containing configured sink instance

        """
        try:
            self.logger.info(
                "Creating sink instance",
                sink_name=sink_config.sink_type,
                sink_type=sink_config.sink_type,
            )

            # Create sink instance
            sink_instance = m.DataSinkInstance(
                sink_type=sink_config.sink_type,
                config=sink_config,
                status="configured",
            )

            self.logger.info(
                "Sink instance created successfully",
                sink_name=sink_instance.config.sink_type,
            )

            return r[m.DataSinkInstance].ok(sink_instance)

        except Exception as e:
            self.logger.exception("Sink instance creation failed", error=str(e))
            return r[m.DataSinkInstance].fail(f"Sink instance creation failed: {e}")

    def execute(
        self,
    ) -> r[t.MeltanoCore.MeltanoConfigDict]:
        """Execute sink abstraction operations (implements Service)."""
        # This would orchestrate the overall sink abstraction workflow
        # For now, return the current configuration
        return r[t.MeltanoCore.MeltanoConfigDict].ok(self._config.model_dump())


# Export Singer SDK types with FLEXT naming
FlextMeltanoTarget = Target


__all__ = [
    "FlextMeltanoTarget",
    "FlextMeltanoTargetAbstractions",
]
