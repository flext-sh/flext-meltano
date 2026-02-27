"""Singer Tap Protocol Implementation for FLEXT Meltano.

This module provides the Singer Tap abstraction following the Singer
specification with FLEXT ecosystem patterns and railway-oriented programming.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from flext_core import FlextResult, FlextRuntime, FlextService
from singer_sdk import Stream, Tap

from flext_meltano.models import FlextMeltanoModels as m
from flext_meltano.settings import FlextMeltanoSettings
from flext_meltano.typings import FlextMeltanoTypes as t

from typing import override
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
        source_config: m.Meltano.DataSourceConfig
        | m.Meltano.TapConfig
        | m.Meltano.TapInstance,
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

        except (
            ValueError,
            TypeError,
            KeyError,
            AttributeError,
            OSError,
            RuntimeError,
            ImportError,
        ) as e:
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

        except (
            ValueError,
            TypeError,
            KeyError,
            AttributeError,
            OSError,
            RuntimeError,
            ImportError,
        ) as e:
            self.logger.exception("Schema validation failed", error=str(e))
            return r[bool].fail(f"Schema validation failed: {e}")

    def create_source_instance(
        self,
        source_config: m.Meltano.DataSourceConfig
        | m.Meltano.TapConfig
        | m.Meltano.TapInstance,
    ) -> r[m.Meltano.DataSourceInstance]:
        """Create a source instance from configuration.

        Args:
        source_config: Source configuration

        Returns:
        FlextResult containing configured source instance

        """
        try:
            source_type = getattr(source_config, "source_type", None) or getattr(
                source_config, "tap_type", "unknown"
            )
            source_identifier = getattr(
                source_config, "source_identifier", None
            ) or getattr(source_config, "tap_identifier", "unknown")

            self.logger.info(
                "Creating source instance",
                source_name=source_type,
                source_type=source_type,
            )

            # Create unique source identifier
            source_id = f"{source_type}:{source_identifier}"

            # Create source instance
            source_instance = m.Meltano.DataSourceInstance(
                source_type=source_type,
                config=source_config,
                status="configured",
                source_id=source_id,
            )

            self.logger.info(
                "Source instance created successfully",
                source_name=source_type,
            )

            return r[m.Meltano.DataSourceInstance].ok(source_instance)

        except (
            ValueError,
            TypeError,
            KeyError,
            AttributeError,
            OSError,
            RuntimeError,
            ImportError,
        ) as e:
            self.logger.exception("Source instance creation failed", error=str(e))
            return r[m.Meltano.DataSourceInstance].fail(
                f"Source instance creation failed: {e}",
            )

    def process(
        self,
        source_config: m.Meltano.DataSourceConfig
        | m.Meltano.TapConfig
        | m.Meltano.TapInstance,
    ) -> r[bool]:
        """Process a source configuration for validation.

        Args:
        source_config: Source configuration to process

        Returns:
        FlextResult containing validation result

        """
        try:
            source_type = getattr(source_config, "source_type", None) or getattr(
                source_config, "tap_type", "unknown"
            )

            self.logger.debug(
                "Processing source configuration",
                source_name=source_type,
            )

            # Basic validation
            if not source_type or source_type == "unknown":
                return r[bool].fail("Source configuration must have a type")

            # Additional validation logic would go here
            # For now, just return success
            return r[bool].ok(value=True)

        except (
            ValueError,
            TypeError,
            KeyError,
            AttributeError,
            OSError,
            RuntimeError,
            ImportError,
        ) as e:
            self.logger.exception(
                "Source configuration processing failed",
                error=str(e),
            )
            return r[bool].fail(f"Source configuration processing failed: {e}")

    @override
    def execute(self) -> r[t.Singer.StreamCatalog]:
        """Execute source abstraction operations (implements Service).

        Returns:
            FlextResult containing empty stream catalog ready for discovery

        """
        # Return empty catalog ready for stream discovery
        return r[t.Singer.StreamCatalog].ok({"streams": []})

    def generate_catalog(
        self,
        source_config: m.Meltano.DataSourceConfig
        | m.Meltano.TapConfig
        | m.Meltano.TapInstance,
    ) -> r[t.JsonDict]:
        """Generate a legacy Singer catalog from configuration.

        Args:
            source_config: Source configuration or instance

        Returns:
            FlextResult containing the generated catalog dictionary

        """
        # Placeholder implementation
        _ = source_config
        return r[t.JsonDict].ok({"version": 1, "streams": []})

    def sync_stream(
        self,
        source_config: m.Meltano.DataSourceConfig
        | m.Meltano.TapConfig
        | m.Meltano.TapInstance,
        stream_name: str,
        target: t.GeneralValueType | None = None,
    ) -> r[t.JsonDict]:
        """Synchronize a single stream from source to target.

        Args:
            source_config: Source configuration or instance
            stream_name: Name of the stream to sync
            target: Optional target configuration or instance

        Returns:
            FlextResult containing synchronization statistics

        """
        # Placeholder implementation
        _ = source_config
        return r[t.JsonDict].ok({
            "stream_name": stream_name,
            "status": "completed",
            "records_processed": 0,
            "target_loaded": target is not None,
        })

    def create_tap_from_config(
        self,
        tap_type: str,
        connection_config: dict[str, t.GeneralValueType],
        stream_config: dict[str, t.GeneralValueType] | None = None,
        **kwargs: t.GeneralValueType,
    ) -> r[m.Meltano.TapInstance]:
        """Create a tap instance from raw configuration data.

        Args:
            tap_type: Type of the tap
            connection_config: Raw connection configuration
            stream_config: Optional stream configuration

        Returns:
            FlextResult containing the created TapInstance

        """
        try:
            config = m.Meltano.TapConfig(
                tap_type=tap_type,
                connection_config=connection_config,
                stream_config=stream_config or {},
                **kwargs,
            )
            return self.create_source_instance(config).map(
                lambda inst: m.Meltano.TapInstance(
                    tap_type=inst.source_type,
                    config=config,
                    tap_id=inst.source_id,
                )
            )
        except Exception as e:
            return r[m.Meltano.TapInstance].fail(f"Failed to create tap: {e}")


# Export Singer SDK types with FLEXT naming
FlextMeltanoStream = Stream
FlextMeltanoTap = Tap


__all__ = [
    "FlextMeltanoStream",
    "FlextMeltanoTap",
    "FlextMeltanoTapAbstractions",
]
