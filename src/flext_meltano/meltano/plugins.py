"""FLEXT Pipeline Component Service - Single unified class for component operations.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from typing import override

from flext_meltano import (
    FlextMeltanoAbstractions,
    FlextMeltanoPluginDiscoveryMixin,
    FlextMeltanoServiceBase,
    p,
    r,
    t,
)


class FlextMeltanoComponentService(
    FlextMeltanoPluginDiscoveryMixin, FlextMeltanoServiceBase
):
    """Service for pipeline component operations.

    Handles component discovery, addition, and management following
    FLEXT patterns with railway-oriented programming.
    """

    @staticmethod
    def _validate_plugin_type(plugin_type: str) -> r[str]:
        """Validate plugin type."""
        valid_types = ["extractors", "loaders", "transformers"]
        if plugin_type not in valid_types:
            return r[str].fail(
                f"Invalid plugin type: {plugin_type}. Valid types: {valid_types}"
            )
        return r[str].ok(plugin_type)

    def add_plugin(
        self,
        project: p.Meltano.Project,
        plugin_type: str,
        plugin_name: str,
    ) -> r[t.StrMapping]:
        """Add plugin to Meltano project using railway-oriented validation chain."""
        return (
            self
            ._log_plugin_addition_start(plugin_name, plugin_type)
            .flat_map(lambda _: self._validate_plugin_type(plugin_type))
            .flat_map(
                lambda pt: self._execute_plugin_addition(project, pt, plugin_name)
            )
            .flat_map(
                lambda result: self._build_plugin_addition_result(
                    plugin_name,
                    plugin_type,
                    addition_success=result,
                ),
            )
        )

    @override
    def execute(self) -> r[t.Meltano.MeltanoConfigDict]:
        """Execute the pipeline component service."""
        return r[t.Meltano.MeltanoConfigDict].ok(self.settings.model_dump())

    def _build_plugin_addition_result(
        self,
        plugin_name: str,
        plugin_type: str,
        *,
        addition_success: bool,
    ) -> r[t.StrMapping]:
        """Build successful plugin addition result."""
        plugin_result: t.StrMapping = {
            "success": "true" if addition_success else "false",
            "plugin_name": plugin_name,
            "plugin_type": plugin_type,
            "addition_method": "project_add_service_native",
        }
        self.logger.info(
            "Plugin added successfully",
            plugin_name=plugin_name,
            plugin_type=plugin_type,
        )
        return r[t.StrMapping].ok(plugin_result)

    def _execute_plugin_addition(
        self,
        project: p.Meltano.Project,
        plugin_type_str: str,
        plugin_name: str,
    ) -> r[bool]:
        """Execute the actual plugin addition using abstraction layer."""
        try:
            plugin_config: t.Meltano.PluginConfiguration = {
                "project_root": str(project.root_dir),
                "plugin_type": plugin_type_str,
                "plugin_name": plugin_name,
            }
            abstractions: FlextMeltanoAbstractions = FlextMeltanoAbstractions()
            add_result: r[bool] = abstractions.add_plugin(plugin_config)
            if add_result.is_failure:
                return r[bool].fail(add_result.error or "Plugin addition failed")
            return r[bool].ok(value=True)
        except (ValueError, TypeError, KeyError, AttributeError, OSError) as e:
            return r[bool].fail(f"Plugin addition failed: {e}")

    def _log_plugin_addition_start(self, plugin_name: str, plugin_type: str) -> r[None]:
        """Log plugin addition start."""
        self.logger.info(
            "Adding plugin using ProjectAddService",
            plugin_name=plugin_name,
            plugin_type=plugin_type,
        )
        return r[None].ok(None)


__all__ = ["FlextMeltanoComponentService"]
