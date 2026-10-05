"""Singer tap source mixin — instance creation and tap factory methods.

Split from ``singer_tap.py`` to honour the one-top-level-class-per-module rule
(ENFORCE-067 / NS-000).

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from typing import Self

from flext_meltano import FlextMeltanoServiceBase, c, m, p, r


class FlextMeltanoTapSourceMixin(FlextMeltanoServiceBase):
    """Mixin providing source instance creation and tap factory methods."""

    @classmethod
    def create_tap_source_instance(cls) -> p.Result[Self]:
        """Create a tap abstractions instance wrapped in Result.

        Returns:
            The resulting ``p.Result[Self]``.
        """
        instance: Self = cls()
        ok_result: p.Result[Self] = r.ok(instance)
        return ok_result

    def create_source_instance(
        self,
        source_config: m.Meltano.DataSourceConfig
        | m.Meltano.TapConfig
        | m.Meltano.TapInstance,
    ) -> p.Result[m.Meltano.DataSourceInstance]:
        """Create a source instance from configuration via isinstance narrowing.

        Returns:
            The resulting ``p.Result[m.Meltano.DataSourceInstance]``.
        """

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
                "Source instance created successfully",
                source_name=source_type,
            )
            return r[m.Meltano.DataSourceInstance].ok(source_instance)

        try:
            return _run_create_source_instance()
        except c.Meltano.SINGER_SAFE_EXCEPTIONS as e:
            self.logger.exception("Source instance creation failed", error=str(e))
            return r[m.Meltano.DataSourceInstance].fail_op(
                "Source instance creation",
                e,
            )


__all__: list[str] = ["FlextMeltanoTapSourceMixin"]
