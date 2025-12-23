"""Singer Tap Protocol Implementation for FLEXT Meltano.

This module provides the Singer Tap abstraction following the Singer
specification with FLEXT ecosystem patterns and railway-oriented programming.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from flext_core import FlextResult, FlextService
from singer_sdk import Stream, Tap

from flext_meltano.utilities import u
from flext_meltano.constants import FlextMeltanoConstants
from flext_meltano.models import FlextMeltanoModels
from flext_meltano.settings import FlextMeltanoSettings
from flext_meltano.typings import FlextMeltanoTypes

# Import aliases for simplified usage
r = FlextResult
t = FlextMeltanoTypes
c = FlextMeltanoConstants
m = FlextMeltanoModels
s = FlextService


class FlextMeltanoTapAbstractions(s[t.MeltanoCore.MeltanoConfigDict]):
    """UNIFIED Source Abstractions class consolidating ALL source functionality.

    This single class provides:
    - Complete Singer source protocol implementation
    - Stream discovery and management
    - Configuration validation and processing
    - Railway-oriented error handling throughout

    Following FLEXT 'one class per module' pattern.
    """

    def __init__(self, config: FlextMeltanoSettings | None = None) -> None:
        """Initialize unified source abstractions with FLEXT configuration."""
        # Initialize FlextService parent class
        super().__init__()
        # Store meltano-specific config (use different name to avoid override)
        self._meltano_config: FlextMeltanoSettings = (
            config if config is not None else FlextMeltanoSettings()
        )

    def discover_streams(
        self,
        source_config: m.DataSourceConfig,
    ) -> r[dict[str, object]]:
        """Discover available streams for a source configuration.

        Args:
        source_config: Source configuration with discovery parameters

        Returns:
        FlextResult containing discovered stream catalog

        """
        try:
            self.logger.info(
                "Discovering streams for source",
                source_type=source_config.source_type,
                source_name=source_config.source_type,
            )

            # Validate source configuration
            if not source_config.source_type:
                return r[dict[str, object]].fail(
                    "Source configuration must have name and type for discovery",
                )

            # For now, return empty catalog - would integrate with actual Singer taps
            catalog: dict[str, object] = {
                "streams": [],
                "source_name": source_config.source_type,
                "source_type": source_config.source_type,
            }

            streams_raw = u.get(catalog, "streams", default=[])
            streams = streams_raw if isinstance(streams_raw, list) else []
            stream_count = u.count(streams)
            self.logger.info(
                "Stream discovery completed",
                stream_count=stream_count,
            )

            return r[dict[str, object]].ok(catalog)

        except Exception as e:
            self.logger.exception("Stream discovery failed", error=str(e))
            return r[dict[str, object]].fail(f"Stream discovery failed: {e}")

    def validate_stream_schema(self, stream_def: m.StreamDefinition) -> r[bool]:
        """Validate a stream definition's schema.

        Args:
        stream_def: Stream definition to validate

        Returns:
        FlextResult containing validation result

        """
        try:
            self.logger.debug(
                "Validating stream schema",
                stream_name=stream_def.stream_name,
            )

            # Basic schema validation
            if not stream_def.stream_schema:
                return r[bool].fail("Stream schema cannot be empty")

            # Schema is already typed as dict[str, object] in StreamDefinition
            if "properties" not in stream_def.stream_schema:
                return r[bool].fail("Stream schema must contain properties")

            # Additional validation logic would go here
            # For now, just return success
            return r[bool].ok(True)

        except Exception as e:
            self.logger.exception("Schema validation failed", error=str(e))
            return r[bool].fail(f"Schema validation failed: {e}")

    def create_source_instance(
        self,
        source_config: m.DataSourceConfig,
    ) -> r[m.DataSourceInstance]:
        """Create a source instance from configuration.

        Args:
        source_config: Source configuration

        Returns:
        FlextResult containing configured source instance

        """
        try:
            self.logger.info(
                "Creating source instance",
                source_name=source_config.source_type,
                source_type=source_config.source_type,
            )

            # Create unique source identifier
            source_id = f"{source_config.source_type}:{source_config.source_identifier}"

            # Create source instance
            source_instance = m.DataSourceInstance(
                source_type=source_config.source_type,
                config=source_config,
                status="configured",
                source_id=source_id,
            )

            self.logger.info(
                "Source instance created successfully",
                source_name=source_instance.config.source_type,
            )

            return r[m.DataSourceInstance].ok(source_instance)

        except Exception as e:
            self.logger.exception("Source instance creation failed", error=str(e))
            return r[m.DataSourceInstance].fail(f"Source instance creation failed: {e}")

    def process(self, source_config: m.DataSourceConfig) -> r[bool]:
        """Process a source configuration for validation.

        Args:
        source_config: Source configuration to process

        Returns:
        FlextResult containing validation result

        """
        try:
            self.logger.debug(
                "Processing source configuration",
                source_name=source_config.source_type,
            )

            # Basic validation
            if not source_config.source_type:
                return r[bool].fail("Source configuration must have a type")

            # Additional validation logic would go here
            # For now, just return success
            return r[bool].ok(True)

        except Exception as e:
            self.logger.exception(
                "Source configuration processing failed",
                error=str(e),
            )
            return r[bool].fail(f"Source configuration processing failed: {e}")

    def execute(
        self,
    ) -> r[t.MeltanoCore.MeltanoConfigDict]:
        """Execute source abstraction operations (implements Service)."""
        # This would orchestrate the overall source abstraction workflow
        # For now, return the current configuration
        return r[t.MeltanoCore.MeltanoConfigDict].ok(self._meltano_config.model_dump())


# Export Singer SDK types with FLEXT naming
FlextMeltanoStream = Stream
FlextMeltanoTap = Tap


__all__ = [
    "FlextMeltanoStream",
    "FlextMeltanoTap",
    "FlextMeltanoTapAbstractions",
]
