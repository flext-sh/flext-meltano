"""Singer Target Abstractions — MRO mixin for FlextMeltano facade.

Sink configuration, instance creation, and validation.
Moved from singer/target.py (already proper mixin pattern).

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from typing import override

from flext_meltano import FlextMeltanoServiceBase, c, m, p, r, settings, t


class FlextMeltanoTargetAbstractions(FlextMeltanoServiceBase):
    """UNIFIED Sink Abstractions class consolidating ALL sink functionality.

    Provides complete Singer sink protocol implementation including
    sink management, batch processing, configuration validation,
    and railway-oriented error handling.
    """

    def configure_sink(
        self, sink_config: m.Meltano.DataSinkConfig
    ) -> p.Result[m.Meltano.DataSinkDefinition]:
        """Configure a sink for a sink configuration."""
        try:
            self.logger.info(
                "Configuring sink for target",
                target_name=sink_config.sink_type,
                target_type=sink_config.sink_type,
            )
            sink_def = m.Meltano.DataSinkDefinition.model_validate({
                "sink_name": f"{sink_config.sink_type}_sink",
                "sink_type": sink_config.sink_type,
                "settings": sink_config.connection_config,
                "status": c.Meltano.OperationStatus.CONFIGURED,
            })
            self.logger.info(
                "Sink configured successfully", sink_name=sink_def.sink_name
            )
            return r[m.Meltano.DataSinkDefinition].ok(sink_def)
        except c.Meltano.SINGER_SAFE_EXCEPTIONS as e:
            self.logger.exception("Sink configuration failed", error=str(e))
            return r[m.Meltano.DataSinkDefinition].fail_op("Sink configuration", e)

    def create_flext_target(
        self, sink_config: m.Meltano.DataSinkConfig | t.JsonMapping
    ) -> p.Result[m.Meltano.DataSinkInstance]:
        """Create a target instance from configuration."""
        if not isinstance(sink_config, m.Meltano.DataSinkConfig):
            try:
                settings: m.Meltano.DataSinkConfig = (
                    m.Meltano.DataSinkConfig.model_validate(sink_config)
                )
            except c.EXC_ATTR_KEY_TYPE_VALUE as e:
                return r[m.Meltano.DataSinkInstance].fail(
                    f"Invalid target settings: {e}", exception=e
                )
        else:
            settings = sink_config
        return self.create_sink_instance(settings)

    def create_sink_instance(
        self, sink_config: m.Meltano.DataSinkConfig
    ) -> p.Result[m.Meltano.DataSinkInstance]:
        """Create a sink instance from configuration."""
        try:
            self.logger.info(
                "Creating sink instance",
                sink_name=sink_config.sink_type,
                sink_type=sink_config.sink_type,
            )
            sink_instance = m.Meltano.DataSinkInstance.model_validate({
                "sink_type": sink_config.sink_type,
                "settings": sink_config,
                "status": c.Meltano.OperationStatus.CONFIGURED,
            })
            self.logger.info(
                "Sink instance created successfully",
                sink_name=sink_instance.settings.sink_type,
            )
            return r[m.Meltano.DataSinkInstance].ok(sink_instance)
        except c.Meltano.SINGER_SAFE_EXCEPTIONS as e:
            self.logger.exception("Sink instance creation failed", error=str(e))
            return r[m.Meltano.DataSinkInstance].fail_op("Sink instance creation", e)

    @override
    def execute(self) -> p.Result[t.JsonMapping]:
        """Execute sink abstraction operations (implements Service)."""
        return r[t.JsonMapping].ok(settings.model_dump(mode="json"))

    def validate_sink_config(
        self, sink_config: m.Meltano.DataSinkConfig
    ) -> p.Result[bool]:
        """Validate a sink configuration."""
        try:
            self.logger.debug(
                "Validating target configuration", target_name=sink_config.sink_type
            )
            if not sink_config.sink_type:
                return r[bool].fail("Target configuration must have name and type")
            return r[bool].ok(value=True)
        except c.Meltano.SINGER_SAFE_EXCEPTIONS as e:
            self.logger.exception(
                "Target configuration validation failed", error=str(e)
            )
            return r[bool].fail_op("Target configuration validation", e)


__all__: list[str] = ["FlextMeltanoTargetAbstractions"]
