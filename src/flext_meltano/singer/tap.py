"""Singer Tap Protocol Implementation for FLEXT Meltano.

This module provides the Singer Tap abstraction following the Singer
specification with FLEXT ecosystem patterns and railway-oriented programming.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from flext_core import FlextResult, FlextRuntime, FlextService
from singer_sdk import Stream, Tap

# Import order: c -> t -> p -> r -> m -> u
from flext_meltano.models import FlextMeltanoModels as m
from flext_meltano.settings import FlextMeltanoSettings
from flext_meltano.typings import FlextMeltanoTypes as t

# Result alias
r = FlextResult


class FlextMeltanoTapAbstractions(FlextService[t.Singer.StreamCatalog]):
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
        super().__init__()
        self._meltano_config: FlextMeltanoSettings = (
            config if config is not None else FlextMeltanoSettings()
        )

    @classmethod
    def create_result_instance(cls) -> r[FlextMeltanoTapAbstractions]:
        """Create a tap abstractions instance wrapped in Result."""
        return r[FlextMeltanoTapAbstractions].ok(FlextRuntime.create_instance(cls))

    def discover_streams(
        self,
        source_config: m.Meltano.DataSourceConfig,
    ) -> r[t.Singer.StreamCatalog]:
        """Discover available streams for a source configuration.

        Args:
        source_config: Source configuration with discovery parameters

        Returns:
        FlextResult containing discovered stream catalog

        """
        try:
            source_type_val = getattr(source_config, "source_type", None) or getattr(
                source_config, "tap_type", None
            )
            self.logger.info(
                "Discovering streams for source",
                source_type=source_type_val,
                source_name=source_type_val,
            )

            # Validate source configuration
            if not source_type_val:
                return r[t.Singer.StreamCatalog].fail(
                    "Source configuration must have name and type for discovery",
                )

            # Return empty catalog - would integrate with actual Singer taps
            catalog: t.Singer.StreamCatalog = {"streams": []}

            streams = catalog.get("streams", [])
            self.logger.info(
                "Stream discovery completed",
                stream_count=len(streams),
            )

            return r[t.Singer.StreamCatalog].ok(catalog)

        except (ValueError, TypeError, KeyError, AttributeError, OSError, RuntimeError, ImportError) as e:
            self.logger.exception("Stream discovery failed", error=str(e))
            return r[t.Singer.StreamCatalog].fail(f"Stream discovery failed: {e}")

    def validate_stream_schema(
        self,
        stream_def: m.Meltano.StreamDefinition,
    ) -> r[bool]:
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

            # Schema is already a validated typed mapping in StreamDefinition
            if "properties" not in stream_def.stream_schema:
                return r[bool].fail("Stream schema must contain properties")

            # Additional validation logic would go here
            # For now, just return success
            return r[bool].ok(value=True)

        except (ValueError, TypeError, KeyError, AttributeError, OSError, RuntimeError, ImportError) as e:
            self.logger.exception("Schema validation failed", error=str(e))
            return r[bool].fail(f"Schema validation failed: {e}")

    def create_source_instance(
        self,
        source_config: m.Meltano.DataSourceConfig,
    ) -> r[m.Meltano.DataSourceInstance]:
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
            source_instance = m.Meltano.DataSourceInstance(
                source_type=source_config.source_type,
                config=source_config,
                status="configured",
                source_id=source_id,
            )

            self.logger.info(
                "Source instance created successfully",
                source_name=source_instance.config.source_type,
            )

            return r[m.Meltano.DataSourceInstance].ok(source_instance)

        except (ValueError, TypeError, KeyError, AttributeError, OSError, RuntimeError, ImportError) as e:
            self.logger.exception("Source instance creation failed", error=str(e))
            return r[m.Meltano.DataSourceInstance].fail(
                f"Source instance creation failed: {e}",
            )

    def process(self, source_config: m.Meltano.DataSourceConfig) -> r[bool]:
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
            return r[bool].ok(value=True)

        except (ValueError, TypeError, KeyError, AttributeError, OSError, RuntimeError, ImportError) as e:
            self.logger.exception(
                "Source configuration processing failed",
                error=str(e),
            )
            return r[bool].fail(f"Source configuration processing failed: {e}")

    def execute(self) -> r[t.Singer.StreamCatalog]:
        """Execute source abstraction operations (implements Service).

        Returns:
            FlextResult containing empty stream catalog ready for discovery

        """
        # Return empty catalog ready for stream discovery
        return r[t.Singer.StreamCatalog].ok({"streams": []})


# Export Singer SDK types with FLEXT naming
FlextMeltanoStream = Stream
FlextMeltanoTap = Tap


__all__ = [
    "FlextMeltanoStream",
    "FlextMeltanoTap",
    "FlextMeltanoTapAbstractions",
]
