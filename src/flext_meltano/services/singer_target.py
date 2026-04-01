"""Singer Target Abstractions — MRO mixin for FlextMeltano facade.

Sink configuration, instance creation, and validation.
Moved from singer/target.py (already proper mixin pattern).

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from typing import override

from flext_core import r

from flext_meltano import FlextMeltanoServiceBase, c, m, t, u


class FlextMeltanoTargetAbstractions(FlextMeltanoServiceBase):
    """UNIFIED Sink Abstractions class consolidating ALL sink functionality.

    Provides complete Singer sink protocol implementation including
    sink management, batch processing, configuration validation,
    and railway-oriented error handling.
    """

    def configure_sink(
        self,
        sink_config: m.Meltano.DataSinkConfig,
    ) -> r[m.Meltano.DataSinkDefinition]:
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
                "config": sink_config.connection_config,
                "status": c.Meltano.Enums.OperationStatus.CONFIGURED,
            })
            self.logger.info(
                "Sink configured successfully",
                sink_name=sink_def.sink_name,
            )
            return r[m.Meltano.DataSinkDefinition].ok(sink_def)
        except (
            ValueError,
            TypeError,
            KeyError,
            AttributeError,
            OSError,
            RuntimeError,
            ImportError,
        ) as e:
            self.logger.exception("Sink configuration failed", error=str(e))
            return r[m.Meltano.DataSinkDefinition].fail(
                f"Sink configuration failed: {e}",
            )

    def create_flext_target(
        self,
        sink_config: m.Meltano.DataSinkConfig | t.ContainerMapping,
    ) -> r[m.Meltano.DataSinkInstance]:
        """Create a target instance from configuration."""
        if not isinstance(sink_config, m.Meltano.DataSinkConfig):
            try:
                config: m.Meltano.DataSinkConfig = (
                    m.Meltano.DataSinkConfig.model_validate(dict(sink_config))
                )
            except (ValueError, TypeError, KeyError, AttributeError) as e:
                return r[m.Meltano.DataSinkInstance].fail(f"Invalid target config: {e}")
        else:
            config = sink_config
        return self.create_sink_instance(config)

    def create_sink_instance(
        self,
        sink_config: m.Meltano.DataSinkConfig,
    ) -> r[m.Meltano.DataSinkInstance]:
        """Create a sink instance from configuration."""
        try:
            self.logger.info(
                "Creating sink instance",
                sink_name=sink_config.sink_type,
                sink_type=sink_config.sink_type,
            )
            sink_instance = m.Meltano.DataSinkInstance(
                sink_type=sink_config.sink_type,
                config=sink_config,
                status=c.Meltano.Enums.OperationStatus.CONFIGURED,
            )
            self.logger.info(
                "Sink instance created successfully",
                sink_name=sink_instance.config.sink_type,
            )
            return r[m.Meltano.DataSinkInstance].ok(sink_instance)
        except (
            ValueError,
            TypeError,
            KeyError,
            AttributeError,
            OSError,
            RuntimeError,
            ImportError,
        ) as e:
            self.logger.exception("Sink instance creation failed", error=str(e))
            return r[m.Meltano.DataSinkInstance].fail(
                f"Sink instance creation failed: {e}",
            )

    @override
    def execute(self) -> r[t.Meltano.MeltanoConfigDict]:
        """Execute sink abstraction operations (implements Service)."""
        return r[t.Meltano.MeltanoConfigDict].ok(
            u.Meltano.coerce_config_mapping(self.settings)
        )

    def validate_sink_config(self, sink_config: m.Meltano.DataSinkConfig) -> r[bool]:
        """Validate a sink configuration."""
        try:
            self.logger.debug(
                "Validating target configuration",
                target_name=sink_config.sink_type,
            )
            if not sink_config.sink_type:
                return r[bool].fail("Target configuration must have name and type")
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
                "Target configuration validation failed",
                error=str(e),
            )
            return r[bool].fail(f"Target configuration validation failed: {e}")


__all__ = ["FlextMeltanoTargetAbstractions"]
