"""Singer Tap Abstractions — MRO mixin for FlextMeltano facade.

Tap/source instance creation and validation. Moved from singer/tap.py
and singer/tap_source.py (already proper mixin pattern).

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from typing import Self

from flext_meltano import FlextMeltanoServiceBase, c, m, r, t


class FlextMeltanoTapSourceMixin(FlextMeltanoServiceBase):
    """Mixin providing source instance creation and tap factory methods."""

    @classmethod
    def create_tap_source_instance(cls) -> r[Self]:
        """Create a tap abstractions instance wrapped in Result."""
        instance: Self = cls()
        return r[Self](value=instance, success=True)

    def create_source_instance(
        self,
        source_config: m.Meltano.DataSourceConfig
        | m.Meltano.TapConfig
        | m.Meltano.TapInstance,
    ) -> r[m.Meltano.DataSourceInstance]:
        """Create a source instance from configuration via isinstance narrowing."""
        try:
            if isinstance(source_config, m.Meltano.DataSourceConfig):
                source_type = source_config.source_type
                source_id = f"{source_type}:{source_type}"
                settings = source_config
            elif isinstance(source_config, m.Meltano.TapConfig):
                source_type = source_config.tap_type
                source_id = f"{source_type}:{source_type}"
                settings = m.Meltano.DataSourceConfig.model_validate({
                    "source_type": source_config.tap_type,
                    "connection_config": source_config.connection_config,
                    "stream_config": source_config.stream_config or {},
                    "source_version": source_config.tap_version,
                })
            else:
                source_type = source_config.tap_type
                source_id = f"{source_type}:{source_config.tap_id}"
                settings = m.Meltano.DataSourceConfig.model_validate({
                    "source_type": source_config.tap_type,
                    "connection_config": source_config.settings.connection_config,
                    "stream_config": source_config.settings.stream_config or {},
                    "source_version": source_config.settings.tap_version,
                })
            self.logger.info(
                "Creating source instance",
                source_name=source_type,
                source_type=source_type,
            )
            source_instance = m.Meltano.DataSourceInstance(
                source_type=source_type,
                settings=settings,
                status=c.Meltano.OperationStatus.CONFIGURED,
                source_id=source_id,
            )
            self.logger.info(
                "Source instance created successfully", source_name=source_type
            )
            return r[m.Meltano.DataSourceInstance].ok(source_instance)
        except c.Meltano.SINGER_SAFE_EXCEPTIONS as e:
            self.logger.exception("Source instance creation failed", error=str(e))
            return r[m.Meltano.DataSourceInstance].fail(
                f"Source instance creation failed: {e}"
            )

    def create_tap_from_config(
        self,
        tap_type: str,
        connection_config: t.RecursiveContainerMapping,
        stream_config: t.RecursiveContainerMapping | None = None,
        tap_version: str = "1.0.0",
    ) -> r[m.Meltano.TapInstance]:
        """Create a tap instance from raw configuration data."""
        try:
            settings = m.Meltano.TapConfig.model_validate({
                "tap_type": tap_type,
                "connection_config": connection_config,
                "stream_config": stream_config or {},
                "tap_version": tap_version,
                "domain_events": [],
            })
            return self.create_source_instance(settings).map(
                lambda inst: m.Meltano.TapInstance(
                    tap_type=inst.source_type,
                    settings=settings,
                    tap_id=inst.source_id,
                ),
            )
        except c.Meltano.OPERATION_ERRORS as exc:
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
        """Process a source configuration for validation via isinstance narrowing."""
        try:
            if isinstance(items, m.Meltano.DataSourceConfig):
                source_type = items.source_type
            elif isinstance(items, m.Meltano.TapConfig):
                source_type = items.tap_type
            else:
                source_type = items.tap_type
            self.logger.debug(
                "Processing source configuration", source_name=source_type
            )
            if not source_type:
                return r[bool].fail("Source configuration must have a type")
            return r[bool].ok(value=True)
        except c.Meltano.SINGER_SAFE_EXCEPTIONS as e:
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
        except c.Meltano.SINGER_SAFE_EXCEPTIONS as e:
            self.logger.exception("Schema validation failed", error=str(e))
            return r[bool].fail(f"Schema validation failed: {e}")


__all__: list[str] = ["FlextMeltanoTapAbstractions", "FlextMeltanoTapSourceMixin"]
