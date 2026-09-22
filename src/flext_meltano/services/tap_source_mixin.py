"""Singer tap source mixin — instance creation and tap factory methods.

Split from ``singer_tap.py`` to honour the one-top-level-class-per-module rule
(ENFORCE-067 / NS-000).

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from typing import Self

from flext_meltano import FlextMeltanoServiceBase, c, m, p, r, t


class FlextMeltanoTapSourceMixin(FlextMeltanoServiceBase):
    """Mixin providing source instance creation and tap factory methods."""

    @classmethod
    def create_tap_source_instance(cls) -> p.Result[Self]:
        """Create a tap abstractions instance wrapped in Result."""
        instance: Self = cls()
        ok_result: p.Result[Self] = r.ok(instance)
        return ok_result

    def create_source_instance(
        self,
        source_config: m.Meltano.DataSourceConfig
        | m.Meltano.TapConfig
        | m.Meltano.TapInstance,
    ) -> p.Result[m.Meltano.DataSourceInstance]:
        """Create a source instance from configuration via isinstance narrowing."""

        def _run_create_source_instance() -> p.Result[m.Meltano.DataSourceInstance]:
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
            source_instance = m.Meltano.DataSourceInstance.model_validate({
                "source_type": source_type,
                "settings": settings,
                "status": c.Meltano.OperationStatus.CONFIGURED,
                "source_id": source_id,
            })
            self.logger.info(
                "Source instance created successfully", source_name=source_type
            )
            return r[m.Meltano.DataSourceInstance].ok(source_instance)

        try:
            return _run_create_source_instance()
        except c.Meltano.SINGER_SAFE_EXCEPTIONS as e:
            self.logger.exception("Source instance creation failed", error=str(e))
            return r[m.Meltano.DataSourceInstance].fail_op(
                "Source instance creation", e
            )

    def create_tap_from_config(
        self,
        tap_type: str,
        connection_config: t.JsonMapping,
        stream_config: t.JsonMapping | None = None,
        tap_version: str = "1.0.0",
    ) -> p.Result[m.Meltano.TapInstance]:
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
                lambda inst: m.Meltano.TapInstance.model_validate({
                    "tap_type": inst.source_type,
                    "settings": settings,
                    "tap_id": inst.source_id,
                })
            )
        except c.Meltano.OPERATION_ERRORS as exc:
            return r[m.Meltano.TapInstance].fail(
                f"Failed to create tap: {exc}", exception=exc
            )


__all__: list[str] = ["FlextMeltanoTapSourceMixin"]
