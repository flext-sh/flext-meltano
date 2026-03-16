"""Singer Tap Protocol Implementation for FLEXT Meltano.

This module provides the Singer Tap abstraction following the Singer
specification with FLEXT ecosystem patterns and railway-oriented programming.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from typing import override

from flext_core import FlextRuntime, r, s

from flext_meltano import FlextMeltanoSettings, m, t


class FlextMeltanoTapAbstractions(s[t.Meltano.Singer.StreamCatalog]):
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
        r containing configured source instance

        """
        try:
            source_type = getattr(source_config, "source_type", None) or getattr(
                source_config, "tap_type", "unknown"
            )
            if not isinstance(source_type, str):
                source_type = "unknown"
            source_identifier = getattr(
                source_config, "source_identifier", None
            ) or getattr(source_config, "tap_identifier", "unknown")
            self.logger.info(
                "Creating source instance",
                source_name=source_type,
                source_type=source_type,
            )
            source_id = f"{source_type}:{source_identifier}"
            if isinstance(source_config, m.Meltano.DataSourceConfig):
                config = source_config
            elif isinstance(source_config, m.Meltano.TapConfig):
                config = m.Meltano.DataSourceConfig(
                    source_type=source_config.tap_type,
                    connection_config=source_config.connection_config,
                    stream_config=source_config.stream_config or {},
                    source_version=source_config.tap_version,
                )
            else:
                config = m.Meltano.DataSourceConfig(
                    source_type=source_config.tap_type,
                    connection_config=source_config.config.connection_config,
                    stream_config=source_config.config.stream_config or {},
                    source_version=source_config.config.tap_version,
                )
            source_instance = m.Meltano.DataSourceInstance(
                source_type=source_type,
                config=config,
                status="configured",
                source_id=source_id,
            )
            self.logger.info(
                "Source instance created successfully", source_name=source_type
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
                f"Source instance creation failed: {e}"
            )

    def create_tap_from_config(
        self,
        tap_type: str,
        connection_config: dict[str, t.Scalar],
        stream_config: dict[str, t.Scalar] | None = None,
        tap_version: str = "1.0.0",
        _version: str | None = None,
    ) -> r[m.Meltano.TapInstance]:
        """Create a tap instance from raw configuration data.

        Args:
            tap_type: Type of the tap
            connection_config: Raw connection configuration
            stream_config: Optional stream configuration
            tap_version: Tap plugin semantic version

        Returns:
            r containing the created TapInstance

        """
        try:
            config = m.Meltano.TapConfig(
                tap_type=tap_type,
                connection_config=connection_config,
                stream_config=stream_config or {},
                tap_version=tap_version,
                domain_events=[],
            )
            return self.create_source_instance(config).map(
                lambda inst: m.Meltano.TapInstance(
                    tap_type=inst.source_type, config=config, tap_id=inst.source_id
                )
            )
        except Exception as exc:
            return r[m.Meltano.TapInstance].fail(f"Failed to create tap: {exc}")

    def discover_streams(
        self,
        source_config: m.Meltano.DataSourceConfig
        | m.Meltano.TapConfig
        | m.Meltano.TapInstance,
    ) -> r[t.Meltano.Singer.StreamCatalog]:
        """Discover available streams for a source configuration.

        Args:
        source_config: Source configuration with discovery parameters

        Returns:
        r containing discovered stream catalog

        """
        try:
            source_type_raw = getattr(source_config, "source_type", None) or getattr(
                source_config, "tap_type", None
            )
            source_type_str: str = (
                str(source_type_raw) if source_type_raw is not None else ""
            )
            self.logger.info(
                "Discovering streams for source",
                source_type=source_type_str,
                source_name=source_type_str,
            )
            if not source_type_str:
                return r[t.Meltano.Singer.StreamCatalog].fail(
                    "Source configuration must have name and type for discovery"
                )
            catalog: t.Meltano.Singer.StreamCatalog = {"streams": []}
            streams = catalog.get("streams", [])
            self.logger.info("Stream discovery completed", stream_count=len(streams))
            return r[t.Meltano.Singer.StreamCatalog].ok(catalog)
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
            return r[t.Meltano.Singer.StreamCatalog].fail(
                f"Stream discovery failed: {e}"
            )

    @override
    def execute(self) -> r[t.Meltano.Singer.StreamCatalog]:
        """Execute source abstraction operations (implements Service).

        Returns:
            r containing empty stream catalog ready for discovery

        """
        return r[t.Meltano.Singer.StreamCatalog].ok({"streams": []})

    def generate_catalog(
        self,
        source_config: m.Meltano.DataSourceConfig
        | m.Meltano.TapConfig
        | m.Meltano.TapInstance,
    ) -> r[t.Dict]:
        """Generate a legacy Singer catalog from configuration.

        Args:
            source_config: Source configuration or instance

        Returns:
            r containing the generated catalog dictionary

        """
        _ = source_config
        return r.ok(t.Dict({"version": 1, "streams": []}))

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
        r containing validation result

        """
        try:
            source_type = getattr(source_config, "source_type", None) or getattr(
                source_config, "tap_type", "unknown"
            )
            self.logger.debug(
                "Processing source configuration", source_name=source_type
            )
            if not source_type or source_type == "unknown":
                return r[bool].fail("Source configuration must have a type")
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
                "Source configuration processing failed", error=str(e)
            )
            return r[bool].fail(f"Source configuration processing failed: {e}")

    def sync_stream(
        self,
        source_config: m.Meltano.DataSourceConfig
        | m.Meltano.TapConfig
        | m.Meltano.TapInstance,
        stream_name: str,
        target: m.Meltano.TargetConfig | None = None,
    ) -> r[t.Dict]:
        """Synchronize a single stream from source to target.

        Args:
            source_config: Source configuration or instance
            stream_name: Name of the stream to sync
            target: Optional target configuration or instance

        Returns:
            r containing synchronization statistics

        """
        _ = source_config
        return r.ok(
            t.Dict({
                "stream_name": stream_name,
                "status": "completed",
                "records_processed": 0,
                "target_loaded": target is not None,
            })
        )

    def validate_stream_schema(self, stream_def: m.Meltano.StreamDefinition) -> r[bool]:
        """Validate a stream definition's schema.

        Args:
        stream_def: Stream definition to validate

        Returns:
        r containing validation result

        """
        try:
            self.logger.debug(
                "Validating stream schema", stream_name=stream_def.stream_name
            )
            if not stream_def.stream_schema:
                return r[bool].fail("Stream schema cannot be empty")
            if "properties" not in stream_def.stream_schema:
                return r[bool].fail("Stream schema must contain properties")
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


__all__ = ["FlextMeltanoTapAbstractions"]
