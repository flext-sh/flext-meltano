"""FLEXT Pipeline Services - Generic service orchestration with flext-core patterns.

This module provides generic data pipeline service orchestration following flext-core
patterns with railway-oriented programming, composition, and SOLID principles.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from typing import override

from flext_core import r

from flext_meltano import FlextMeltanoServiceBase, c, t, u


class FlextMeltanoService(FlextMeltanoServiceBase):
    """Generic data pipeline service mixin.

    Provides pipeline orchestration methods using flext-core patterns
    with railway-oriented programming. Configuration via self.settings (MRO).
    """

    @staticmethod
    def _create_service_generic(
        service_type: str,
        name: str,
        **config: t.Scalar,
    ) -> r[FlextMeltanoService]:
        """Generic service factory - delegates to specific creators."""
        if service_type == "source":
            return FlextMeltanoService.create_source_service(name, **config)
        if service_type == "sink":
            return FlextMeltanoService.create_sink_service(name, **config)
        if service_type == "transformation":
            return FlextMeltanoService.create_transformation_service(name, **config)
        return r[FlextMeltanoService].fail(f"Unknown service type: {service_type}")

    @staticmethod
    def configure_environment(
        environment_name: str,
        config: t.Meltano.MeltanoConfigDict | None = None,
    ) -> r[t.Meltano.MeltanoConfigDict]:
        """Configure environment."""
        if not environment_name:
            return r[t.Meltano.MeltanoConfigDict].fail("Environment name is required")
        if environment_name not in c.Meltano.Environments.VALID:
            return r[t.Meltano.MeltanoConfigDict].fail(
                f"Invalid environment: {environment_name}. Valid: {c.Meltano.Environments.VALID}",
            )
        return r[t.Meltano.MeltanoConfigDict].ok({
            "environment": environment_name,
            "configuration": config or {},
            "status": c.Meltano.Enums.OperationStatus.CONFIGURED,
        })

    @staticmethod
    def configure_pipeline(
        source_name: str,
        sink_name: str,
        _config: t.Meltano.MeltanoConfigDict | None = None,
    ) -> r[t.Meltano.MeltanoConfigDict]:
        """Configure generic data pipeline - railway-oriented operation."""
        return r[t.Meltano.MeltanoConfigDict].ok({
            "source": source_name,
            "sink": sink_name,
            "status": c.Meltano.Enums.OperationStatus.CONFIGURED,
        })

    @staticmethod
    def create_dbt_service(dbt_name: str, **config: t.Scalar) -> r[FlextMeltanoService]:
        """Create DBT transformation service - delegates to generic transformation service."""
        return FlextMeltanoService.create_transformation_service(dbt_name, **config)

    @staticmethod
    def create_sink_service(
        sink_name: str,
        **_config: t.Scalar,
    ) -> r[FlextMeltanoService]:
        """Create data sink service using railway pattern."""
        try:
            service = FlextMeltanoService(
                service_name=f"{sink_name}_service",
                service_version=c.Meltano.Defaults.SERVICE_VERSION,
                sink_name=sink_name,
            )
            return r[FlextMeltanoService].ok(service)
        except (ValueError, TypeError, KeyError, AttributeError, OSError) as ex:
            return r[FlextMeltanoService].fail(
                f"Failed to create sink service '{sink_name}': {ex}",
            )

    @staticmethod
    def create_source_service(
        source_name: str,
        **_config: t.Scalar,
    ) -> r[FlextMeltanoService]:
        """Create data source service using railway pattern."""
        try:
            service = FlextMeltanoService(
                service_name=f"{source_name}_service",
                service_version=c.Meltano.Defaults.SERVICE_VERSION,
                source_name=source_name,
            )
            return r[FlextMeltanoService].ok(service)
        except (ValueError, TypeError, KeyError, AttributeError, OSError) as ex:
            return r[FlextMeltanoService].fail(
                f"Failed to create source service '{source_name}': {ex}",
            )

    @staticmethod
    def create_tap_service(tap_name: str, **config: t.Scalar) -> r[FlextMeltanoService]:
        """Create Singer tap service - delegates to generic source service."""
        return FlextMeltanoService.create_source_service(tap_name, **config)

    @staticmethod
    def create_target_service(
        target_name: str,
        **config: t.Scalar,
    ) -> r[FlextMeltanoService]:
        """Create Singer target service - delegates to generic sink service."""
        return FlextMeltanoService.create_sink_service(target_name, **config)

    @staticmethod
    def create_transformation_service(
        transformation_name: str,
        **_config: t.Scalar,
    ) -> r[FlextMeltanoService]:
        """Create transformation service using railway pattern."""
        try:
            service = FlextMeltanoService(
                service_name=f"{transformation_name}_service",
                service_version=c.Meltano.Defaults.SERVICE_VERSION,
                transformation_name=transformation_name,
            )
            return r[FlextMeltanoService].ok(service)
        except (ValueError, TypeError, KeyError, AttributeError, OSError) as ex:
            return r[FlextMeltanoService].fail(
                f"Failed to create transformation service '{transformation_name}': {ex}",
            )

    @staticmethod
    def install_component(
        component_type: str,
        component_name: str,
        config: t.Meltano.MeltanoConfigDict | None = None,
    ) -> r[t.Meltano.MeltanoConfigDict]:
        """Install pipeline component with validation."""
        if not component_type or not component_name:
            return r[t.Meltano.MeltanoConfigDict].fail(
                "Component type and name are required",
            )
        if component_type not in c.Meltano.ComponentTypes.VALID:
            return r[t.Meltano.MeltanoConfigDict].fail(
                f"Invalid component type: {component_type}",
            )
        return r[t.Meltano.MeltanoConfigDict].ok({
            "component_name": component_name,
            "component_type": component_type,
            "status": c.Meltano.Enums.OperationStatus.INSTALLED,
            "configuration": config or {},
        })

    @staticmethod
    def validate_service_config(config: t.Meltano.MeltanoConfigDict) -> r[bool]:
        """Validate service configuration dictionary."""
        if not u.guard(config, dict):
            return r[bool].fail("Configuration must be a dictionary")
        return r[bool].ok(value=True)

    def create_from_config(
        self,
        config: t.Meltano.MeltanoConfigDict | t.NormalizedValue,
    ) -> r[t.Meltano.MeltanoConfigDict]:
        """Create a service instance from configuration (config-as-instance pattern)."""
        if not isinstance(config, dict):
            return r[t.Meltano.MeltanoConfigDict].fail(
                "Configuration must be a dictionary",
            )
        cfg: t.Meltano.MeltanoConfigDict = dict(config)
        return r[t.Meltano.MeltanoConfigDict].ok(cfg)

    @override
    def execute(self) -> r[t.Meltano.MeltanoConfigDict]:
        """Execute service with railway pattern - implements FlextService protocol."""
        return r[t.Meltano.MeltanoConfigDict].ok({
            "service_name": c.Meltano.Metadata.APPLICATION_NAME,
            "version": c.Meltano.FLEXT_MELTANO_VERSION,
            "status": c.CommonStatus.ACTIVE,
            "handlers": list(c.Meltano.Handlers.ALL),
        })

    def get_default_config(self) -> r[t.Meltano.MeltanoConfigDict]:
        """Get default configuration from current settings."""
        return r[t.Meltano.MeltanoConfigDict].ok(self.settings.model_dump())

    def get_info(self) -> r[t.Meltano.PluginInfo]:
        """Get service information."""
        return r[t.Meltano.PluginInfo].ok({
            "name": c.Meltano.Metadata.APPLICATION_NAME,
            "version": c.Meltano.FLEXT_MELTANO_VERSION,
            "type": "pipeline_service",
            "description": c.Meltano.Metadata.APPLICATION_DESCRIPTION,
        })

    def get_service_status(self) -> r[t.Meltano.MeltanoConfigDict]:
        """Get service status."""
        return self.execute()

    def get_version_info(self) -> r[t.Meltano.MeltanoConfigDict]:
        """Get version information."""
        return r[t.Meltano.MeltanoConfigDict].ok({
            "api_version": c.Meltano.FLEXT_MELTANO_VERSION,
            "service_name": c.Meltano.Metadata.APPLICATION_NAME,
        })

    def validate_config(self) -> r[bool]:
        """Validate the current service configuration."""
        return self.validate_service_config(self.settings.model_dump())


__all__ = ["FlextMeltanoService"]
