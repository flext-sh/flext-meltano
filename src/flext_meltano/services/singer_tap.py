"""Singer Tap Abstractions — MRO mixin for FlextMeltano facade.

Tap/source instance creation and validation. Moved from singer/tap.py
and singer/tap_source.py (already proper mixin pattern).

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from flext_core import FlextRuntime, r

from flext_meltano import FlextMeltanoServiceBase, c, m, t


class FlextMeltanoTapSourceMixin(FlextMeltanoServiceBase):
    """Mixin providing source instance creation and tap factory methods."""

    @classmethod
    def create_result_instance(cls) -> r[FlextMeltanoTapSourceMixin]:
        """Create a tap abstractions instance wrapped in Result."""
        return r[FlextMeltanoTapSourceMixin].ok(FlextRuntime.create_instance(cls))

    def create_source_instance(
        self,
        source_config: m.Meltano.DataSourceConfig
        | m.Meltano.TapConfig
        | m.Meltano.TapInstance,
    ) -> r[m.Meltano.DataSourceInstance]:
        """Create a source instance from configuration."""
        try:
            source_type = getattr(source_config, "source_type", None) or getattr(
                source_config,
                "tap_type",
                c.IDENTIFIER_UNKNOWN,
            )
            if not isinstance(source_type, str):
                source_type = c.IDENTIFIER_UNKNOWN
            source_identifier = getattr(
                source_config,
                "source_identifier",
                None,
            ) or getattr(source_config, "tap_identifier", c.IDENTIFIER_UNKNOWN)
            self.logger.info(
                "Creating source instance",
                source_name=source_type,
                source_type=source_type,
            )
            source_id = f"{source_type}:{source_identifier}"
            if isinstance(source_config, m.Meltano.DataSourceConfig):
                config = source_config
            elif isinstance(source_config, m.Meltano.TapConfig):
                config = m.Meltano.DataSourceConfig.model_validate({
                    "source_type": source_config.tap_type,
                    "connection_config": source_config.connection_config,
                    "stream_config": source_config.stream_config or {},
                    "source_version": source_config.tap_version,
                })
            else:
                config = m.Meltano.DataSourceConfig.model_validate({
                    "source_type": source_config.tap_type,
                    "connection_config": source_config.config.connection_config,
                    "stream_config": source_config.config.stream_config or {},
                    "source_version": source_config.config.tap_version,
                })
            source_instance = m.Meltano.DataSourceInstance(
                source_type=source_type,
                config=config,
                status=c.Meltano.Enums.OperationStatus.CONFIGURED,
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
        connection_config: t.ConfigurationMapping,
        stream_config: t.ConfigurationMapping | None = None,
        tap_version: str = "1.0.0",
    ) -> r[m.Meltano.TapInstance]:
        """Create a tap instance from raw configuration data."""
        try:
            config = m.Meltano.TapConfig.model_validate({
                "tap_type": tap_type,
                "connection_config": connection_config,
                "stream_config": stream_config or {},
                "tap_version": tap_version,
                "domain_events": [],
            })
            return self.create_source_instance(config).map(
                lambda inst: m.Meltano.TapInstance(
                    tap_type=inst.source_type,
                    config=config,
                    tap_id=inst.source_id,
                ),
            )
        except Exception as exc:
            return r[m.Meltano.TapInstance].fail(f"Failed to create tap: {exc}")


class FlextMeltanoTapAbstractions(FlextMeltanoTapSourceMixin, FlextMeltanoServiceBase):
    """Concrete source abstraction operations.

    Only real implementations live here. Abstract contracts
    (discover_streams, sync_stream, etc.) are defined in
    p.Meltano.Singer.Tap and p.Meltano.Singer.SingerTap protocols.
    Consumers implement those protocols directly.
    """

    def process_source(
        self,
        items: m.Meltano.DataSourceConfig | m.Meltano.TapConfig | m.Meltano.TapInstance,
    ) -> r[bool]:
        """Process a source configuration for validation."""
        try:
            source_type = getattr(items, "source_type", None) or getattr(
                items,
                "tap_type",
                c.IDENTIFIER_UNKNOWN,
            )
            self.logger.debug(
                "Processing source configuration", source_name=source_type
            )
            if not source_type or source_type == c.IDENTIFIER_UNKNOWN:
                return r[bool].fail("Source configuration must have a type")
            return r[bool].ok(value=True)
        except c.Meltano.Singer.SAFE_EXCEPTIONS as e:
            self.logger.exception(
                "Source configuration processing failed", error=str(e)
            )
            return r[bool].fail(f"Source configuration processing failed: {e}")

    def validate_stream_schema(self, stream_def: m.Meltano.StreamDefinition) -> r[bool]:
        """Validate a stream definition's schema."""
        try:
            self.logger.debug(
                "Validating stream schema", stream_name=stream_def.stream_name
            )
            if not stream_def.stream_schema:
                return r[bool].fail("Stream schema cannot be empty")
            if "properties" not in stream_def.stream_schema:
                return r[bool].fail("Stream schema must contain properties")
            return r[bool].ok(value=True)
        except c.Meltano.Singer.SAFE_EXCEPTIONS as e:
            self.logger.exception("Schema validation failed", error=str(e))
            return r[bool].fail(f"Schema validation failed: {e}")


__all__ = ["FlextMeltanoTapAbstractions", "FlextMeltanoTapSourceMixin"]
